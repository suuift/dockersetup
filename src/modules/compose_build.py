import os
import re
import hashlib
from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path, resolve_path_slash
from src.utils.logger import write_log, console, write_step
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_template_blocks, get_registry_list

def indent_service_block(block: str) -> str:
    """
    Reconstructs 2-space indentation for loaded templates to match services block nesting (Edge Case 12).
    """
    return "\n".join("  " + line if line.strip() else "" for line in block.splitlines())

def build_compose_stacks() -> bool:
    write_step("Generating Docker Compose stack configurations")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    env_path = resolve_path_slash(os.path.join(deploy_dir, ".env"))
    template_path = get_resource_path("templates.yml")
    services_path = get_resource_path("services.yml")

    # Load Master Registry
    master_registry = get_yaml_content(services_path)
    if "STACK_GROUPS" not in master_registry or not master_registry["STACK_GROUPS"]:
        raise ValueError("STACK_GROUPS section missing in services.yml")

    # Load State
    metadata = get_metadata()
    selected_services = metadata.get("selected_services", [])

    # Database Manager dependency logic
    db_addons = {
        "mariadb (+adminer)": "adminer",
        "postgresql (+cloudbeaver)": "cloudbeaver",
        "mongodb (+mongo-express)": "mongo-express"
    }
    for db, addon in db_addons.items():
        if db in selected_services and addon not in selected_services:
            selected_services.append(addon)

    # Load templates
    templates = get_template_blocks(template_path)

    # Update Hash in Metadata
    sha256 = hashlib.sha256()
    with open(template_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    current_hash = sha256.hexdigest().upper()
    metadata["template_hash"] = current_hash
    set_metadata(metadata)

    stacks_dir = resolve_path_slash(os.path.join(deploy_dir, "stacks"))
    os.makedirs(stacks_dir, exist_ok=True)

    generated_stacks = []
    homepage_services = []

    # Pre-compute dynamic mounts string (Edge Case 16)
    extra_mounts = os.getenv("EXTRA_MOUNTS", "")
    if not extra_mounts and os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"^EXTRA_MOUNTS=(.*)", line)
                if match:
                    extra_mounts = match.group(1)
                    break

    dynamic_mounts_string = ""
    if extra_mounts:
        mounts = [m.strip() for m in extra_mounts.split(",") if m.strip()]
        for m in mounts:
            clean_m = m.replace('"', '').replace("'", "")
            # Windows drive parsing or Linux paths
            drive_letter = clean_m.replace(":/", "").replace(":\\", "").replace(":", "")
            dynamic_mounts_string += f"      - {clean_m}:/srv/{drive_letter}_Drive\n"

    # --- STACK GENERATION LOOP ---
    for group in master_registry["STACK_GROUPS"]:
        stack_name = group.name
        group_services = group.services
        active_services = [s for s in selected_services if s in group_services]

        if active_services:
            write_log(f"Generating stack: {stack_name} ({len(active_services)} services)")
            stack_path = os.path.join(stacks_dir, stack_name)
            os.makedirs(stack_path, exist_ok=True)

            # Build Compose
            output = templates.get("header", "")
            for svc in active_services:
                write_log(f"Adding service to {stack_name}: {svc}", level="DEBUG")
                if svc in templates:
                    svc_content = templates[svc]

                    # Security warning for privileged containers
                    if "privileged: true" in svc_content or "cap_add:" in svc_content and "SYS_ADMIN" in svc_content:
                        write_step(f"Security Warning: Service '{svc}' in stack '{stack_name}' is privileged.", level="WARN")

                    # Audit template version tags for critical services (Verbose only)
                    critical_services = ["mariadb (+adminer)", "postgresql (+cloudbeaver)", "mongodb (+mongo-express)", "authelia"]
                    if svc in critical_services:
                        match_img = re.search(r"image:\s*([^\s]+)", svc_content)
                        if match_img:
                            image = match_img.group(1)
                            if image.endswith(":latest") or ":" not in image:
                                write_log(
                                    f"[AUDIT] Insecure tag found in critical service '{svc}': image is using '{image}'. Consider pinning to a stable version.",
                                    level="DEBUG"
                                )

                    if "{{DYNAMIC_MOUNTS}}" in svc_content:
                        svc_content = svc_content.replace("{{DYNAMIC_MOUNTS}}", dynamic_mounts_string)

                    output += "\n" + indent_service_block(svc_content)
                else:
                    write_log(f"Template NOT FOUND for service: {svc}", level="DEBUG")

            # Write Compose File
            compose_file_path = os.path.join(stack_path, "docker-compose.yml")
            with open(compose_file_path, "w", encoding="utf-8") as f:
                f.write(output)

            # --- PHASE 4: SECRET ISOLATION (FILTERED .ENV) ---
            write_log(f"Isolating secrets for stack: {stack_name}", level="DEBUG")
            master_env_lines = []
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    master_env_lines = f.readlines()

            # Global defaults always included
            required_vars = {"PUID", "PGID", "TZ", "DOCKERDIR", "DRIVEPOOL", "USERDIR"}

            # Scan compose for variables using exact regex mapping (Edge Case 14)
            var_matches = re.findall(r'\$\{?(\w+)(?:[:?#-][^}]*)?\}?', output)
            for var_name in var_matches:
                required_vars.add(var_name)

            # Special case for maintenance stack: Include all API keys and HTTP credentials for Homepage Widgets
            if stack_name == "maintenance":
                required_vars.update({"HTTP_USERNAME", "HTTP_PASSWORD"})
                for line in master_env_lines:
                    match = re.match(r"^([A-Z0-9_]+_API_KEY|[A-Z0-9_]+_TOKEN|[A-Z0-9_]+_KEY)=", line)
                    if match:
                        required_vars.add(match.group(1))

            # Filter and Write Stack-Local .env
            filtered_env = []
            for line in master_env_lines:
                match = re.match(r"^([^=]+)=", line)
                if match:
                    key = match.group(1).strip()
                    if key in required_vars:
                        filtered_env.append(line)
                elif line.startswith("#") or not line.strip():
                    filtered_env.append(line)

            with open(os.path.join(stack_path, ".env"), "w", encoding="utf-8") as f:
                f.writelines(filtered_env)

            generated_stacks.append({
                "Name": stack_name,
                "Apps": ", ".join(active_services)
            })

            # Collect for Homepage (excluding helper DB apps)
            db_helpers = ["adminer", "cloudbeaver", "mongo-express"]
            for svc in active_services:
                if svc not in db_helpers:
                    homepage_services.append({"Name": svc, "Stack": stack_name})

    # --- HOMEPAGE GENERATOR ---
    if "homepage" in selected_services:
        write_log("Generating Homepage services configuration...")
        hp_path = os.path.join(deploy_dir, "appdata", "homepage", "config")
        os.makedirs(hp_path, exist_ok=True)

        hp_output = ""
        hp_env_mappings = []
        active_hp_groups = []

        registry_list = get_registry_list(master_registry)

        supported_widgets = {}
        if "SUPPORTED_WIDGETS" in master_registry:
            for widget in master_registry["SUPPORTED_WIDGETS"]:
                supported_widgets[widget.name] = widget.alias

        def make_friendly_name(name: str) -> str:
            # Converts 'media-pvr' to 'Media PVR', 'media-server' to 'Media Server'
            parts = name.split('-')
            return " ".join([p.upper() if p.lower() in ["pvr", "vpn"] else p.capitalize() for p in parts])

        for group in master_registry["STACK_GROUPS"]:
            stack_name = group.name
            stack_apps = [a for a in homepage_services if a["Stack"] == stack_name]

            if stack_apps:
                friendly_group_name = make_friendly_name(stack_name)
                active_hp_groups.append(friendly_group_name)
                hp_output += f"- {friendly_group_name}:\n"
                for app in stack_apps:
                    svc_key = app["Name"]
                    
                    # Find registry entry
                    reg_entry = None
                    for entry in registry_list:
                        if entry.key == svc_key:
                            reg_entry = entry
                            break
                    
                    alias = svc_key
                    port = "0"
                    if reg_entry:
                        if reg_entry.description and reg_entry.description != "none":
                            alias = reg_entry.description  # Fallback to key or alias
                        # Wait, original script has: if ($regEntry.Alias)
                        # In Python, ConfigurableApp properties mapping uses name/alias.
                        # Let's map it safely.
                        port = reg_entry.port

                    svc_template = templates.get(svc_key, "")
                    # Check for explicit PORT override
                    match_port = re.search(r"#\s*PORT:\s*(\d+)", svc_template)
                    if match_port:
                        port = match_port.group(1)
                    elif port == "0":
                        # Regex fallback check
                        match_regex_port = re.search(r"-\s*(\d+):", svc_template)
                        if match_regex_port:
                            port = match_regex_port.group(1)

                    clean_key = svc_key.split(" ")[0]
                    hp_output += f"    - {svc_key}:\n"
                    hp_output += f"        icon: {clean_key}.png\n"

                    if port and port != "0":
                        url = f"http://localhost:{port}"
                        base_domain = "local.host"
                        # Fetch base domain from env
                        base_domain_env = os.getenv("BASE_DOMAIN", "")
                        if not base_domain_env and os.path.exists(env_path):
                            with open(env_path, "r", encoding="utf-8") as f:
                                for line in f:
                                    match = re.match(r"^BASE_DOMAIN=(.*)", line)
                                    if match:
                                        base_domain_env = match.group(1)
                                        break
                        if base_domain_env:
                            base_domain = base_domain_env

                        if "npm plus (+goaccess)" in selected_services and base_domain != "local.host":
                            url = f"https://{alias.split(' ')[0]}.{base_domain}"

                        # Get a clean description from the registry entry type
                        reg = next((e for e in registry_list if e.key == svc_key), None)
                        description = reg.type.capitalize() if reg and hasattr(reg, 'type') else alias

                        hp_output += f"        href: {url}\n"
                        hp_output += f"        description: {description}\n"
                        hp_output += f"        ping: http://{clean_key}:{port}\n"

                        # --- WIDGET LOGIC ---
                        w_key = clean_key.lower()
                        if w_key in ["qbit-vpn", "qbit"]:
                            w_key = "qbittorrent"
                        if w_key == "uptimekuma":
                            w_key = "uptime-kuma"

                        if w_key in supported_widgets and url:
                            w_type = supported_widgets[w_key]
                            hp_output += "        widget:\n"
                            hp_output += f"          type: {w_type}\n"
                            hp_output += f"          url: http://{clean_key}:{port}\n"

                            env_key_base = svc_key.upper().replace("-", "_").replace(" ", "_")

                            if w_type == "qbittorrent":
                                hp_output += "          username: {{HOMEPAGE_VAR_HTTP_USERNAME}}\n"
                                hp_output += "          password: {{HOMEPAGE_VAR_HTTP_PASSWORD}}\n"
                                hp_env_mappings.append("      - HOMEPAGE_VAR_HTTP_USERNAME=${HTTP_USERNAME}")
                                hp_env_mappings.append("      - HOMEPAGE_VAR_HTTP_PASSWORD=${HTTP_PASSWORD}")
                            else:
                                api_key_var = f"{env_key_base}_API_KEY"
                                # Jellyfin widget uses 'apiKey', all others use 'key'
                                key_field = "key"
                                if w_type == "plex":
                                    api_key_var = "PLEX_TOKEN"
                                elif w_type == "jellyfin":
                                    api_key_var = "JELLYFIN_KEY"
                                    key_field = "apiKey"
                                elif w_type == "portainer":
                                    api_key_var = "PORTAINER_KEY"

                                hp_output += f"          {key_field}: {{{{HOMEPAGE_VAR_{api_key_var}}}}}\n"
                                hp_env_mappings.append(f"      - HOMEPAGE_VAR_{api_key_var}=${api_key_var}")
                    else:
                        hp_output += "        description: Background Service\n"
                hp_output += "\n"

        # Write Homepage services.yaml
        with open(os.path.join(hp_path, "services.yaml"), "w", encoding="utf-8") as f:
            f.write(hp_output)

        # Write Homepage settings.yaml (Layout configuration) - Safe Merge
        from ruamel.yaml import YAML
        yaml = YAML()
        yaml.preserve_quotes = True
        
        settings_file = os.path.join(hp_path, "settings.yaml")
        settings_data = {}
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    loaded = yaml.load(f)
                    if loaded:
                        settings_data = loaded
            except Exception as e:
                write_log(f"Failed to load existing settings.yaml: {str(e)}", level="WARN")

        # Set defaults if not present
        if "title" not in settings_data:
            settings_data["title"] = "Home Server Dashboard"
        if "theme" not in settings_data:
            settings_data["theme"] = "dark"
        if "fullWidth" not in settings_data:
            settings_data["fullWidth"] = True
        
        # Determine strict priority order for top rows
        priority_order = ["Media Server", "Media PVR", "Downloaders", "Maintenance"]
        ordered_groups = []
        
        # 1. Add priority groups if active
        for p_group in priority_order:
            if p_group in active_hp_groups:
                ordered_groups.append(p_group)
                
        # 2. Add any remaining active groups
        for a_group in active_hp_groups:
            if a_group not in ordered_groups:
                ordered_groups.append(a_group)
                
        # Build the layout dictionary
        layout_list = []
        for layout_group in ordered_groups:
            # We construct a dict like: {"Media Server": {"style": "row", "columns": 4}}
            layout_list.append({layout_group: {"style": "row", "columns": 4}})
            
        settings_data["layout"] = layout_list
        
        with open(settings_file, "w", encoding="utf-8") as f:
            yaml.dump(settings_data, f)

        # Write Homepage widgets.yaml
        widgets_file = os.path.join(hp_path, "widgets.yaml")
        if not os.path.exists(widgets_file) or os.getenv("TEST_MODE") != "true":
            # Determine disk path
            drive = os.path.splitdrive(deploy_dir)[0]
            if drive:
                disk_path = "/" + drive.replace(":", "")
            else:
                disk_path = "/"
                
            widgets_content = f"""---
# For configuration options and examples, please see:
# https://gethomepage.dev/en/configs/widgets

- resources:
    cpu: true
    memory: true
    disk: {disk_path}

- search:
    provider: google
    target: _blank
    
- datetime:
    text_size: xl
    format:
      dateStyle: short
      timeStyle: short
      hour12: true
"""
            with open(widgets_file, "w", encoding="utf-8") as f:
                f.write(widgets_content)

        # Write Homepage bookmarks.yaml
        bookmarks_file = os.path.join(hp_path, "bookmarks.yaml")
        if not os.path.exists(bookmarks_file) or os.getenv("TEST_MODE") != "true":
            bookmarks_content = """- Developer:
    - github.com/suuift/dockersetup:
        - abbr: GH
          href: https://github.com/suuift/dockersetup
- Windows Debloat Scripts:
    - Github/ChrisTitusTech/winutil/:
        - abbr: RE
          href: https://github.com/ChrisTitusTech/winutil/
"""
            with open(bookmarks_file, "w", encoding="utf-8") as f:
                f.write(bookmarks_content)

        # Write Homepage docker.yaml (Local Socket connection)
        docker_file = os.path.join(hp_path, "docker.yaml")
        if not os.path.exists(docker_file) or os.getenv("TEST_MODE") != "true":
            docker_data = {
                "my-docker": {
                    "socket": "/var/run/docker.sock"
                }
            }
            with open(docker_file, "w", encoding="utf-8") as f:
                yaml.dump(docker_data, f)        # Update the Homepage Compose with dynamic mappings
        hp_compose_path = os.path.join(stacks_dir, "maintenance", "docker-compose.yml")
        if os.path.exists(hp_compose_path):
            unique_mappings = sorted(list(set(hp_env_mappings)))
            mapping_str = "\n".join(unique_mappings)
            with open(hp_compose_path, "r", encoding="utf-8") as f:
                hp_compose = f.read()
            new_hp_compose = hp_compose.replace("{{HOMEPAGE_MAPPINGS}}", mapping_str)
            with open(hp_compose_path, "w", encoding="utf-8") as f:
                f.write(new_hp_compose)
    # Finalize State
    metadata["generated_stacks"] = generated_stacks
    set_metadata(metadata)

    write_log(f"Multi-stack build complete at {stacks_dir}", level="DEBUG")
    console.print("[✓] Docker Compose stack configurations generated", style="green")
    return True
