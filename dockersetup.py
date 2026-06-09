import os
import sys
import shutil
import hashlib
import platform
import subprocess
import questionary
from rich.console import Console

# Bootstrap utilities
from src.utils.paths import get_project_root, get_deploy_dir, resolve_path_slash, get_resource_path
from src.utils.logger import write_log, write_step, set_log_path, enable_debug_logging, get_log_path, invoke_external_command
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list
from src.utils.updater import invoke_self_update, VERSION

# Import modules
from src.modules.preflight import run_system_preflight
from src.modules.deploy_preflight import run_deploy_preflight
from src.modules.tier_select import select_services
from src.modules.env_wizard import configure_environment
from src.modules.directories import setup_directories
from src.modules.network import setup_networks
from src.modules.compose_build import build_compose_stacks
from src.modules.deploy_start import deploy_stacks
from src.modules.auto_configure import auto_stitch_services, test_port

console = Console()

def sync_dot_env(source_env: str, target_dir: str):
    write_log("Syncing environment variables to stack folders...", level="DEBUG")
    stacks_dir = resolve_path_slash(os.path.join(target_dir, "stacks"))
    if os.path.exists(stacks_dir):
        for name in os.listdir(stacks_dir):
            folder_path = resolve_path_slash(os.path.join(stacks_dir, name))
            if os.path.isdir(folder_path):
                try:
                    shutil.copy(source_env, resolve_path_slash(os.path.join(folder_path, ".env")))
                except Exception as e:
                    write_log(f"Failed to copy .env to {folder_path}: {str(e)}", level="WARN")

def invoke_token_wizard(target_dir: str):
    metadata = get_metadata()
    selected = metadata.get("selected_services", [])
    if not selected:
        return

    env_path = resolve_path_slash(os.path.join(target_dir, ".env"))
    if not os.path.exists(env_path):
        return

    manual_services = {
        "plex": {"Name": "Plex", "Var": "PLEX_TOKEN", "Url": "http://localhost:32400", "Hint": "Open Plex -> Settings -> Web Client (General) -> 'Show Advanced' -> Scroll to bottom for 'Plex Token'."},
        "jellyfin": {"Name": "Jellyfin", "Var": "JELLYFIN_KEY", "Url": "http://localhost:8096", "Hint": "Open Jellyfin -> Dashboard -> API Keys -> Create a new key named 'Homepage'."},
        "portainer": {"Name": "Portainer", "Var": "PORTAINER_KEY", "Url": "http://localhost:9443", "Hint": "Open Portainer -> User Settings -> Access Tokens -> Create a new token named 'Homepage'."}
    }

    to_configure = []
    # Read env file content
    env_content = ""
    with open(env_path, "r", encoding="utf-8") as f:
        env_content = f.read()

    for svc, info in manual_services.items():
        if svc in selected:
            if not re.search(fr"^{info['Var']}=", env_content, re.MULTILINE):
                to_configure.append(svc)

    import re
    if to_configure and os.getenv("DS_HEADLESS") != "true":
        console.print("\n----------------------------------------------------------", style="cyan")
        console.print("             HOMEPAGE WIDGET SETUP", style="cyan")
        console.print("----------------------------------------------------------", style="cyan")
        console.print("I noticed some services are running that require a manual")
        console.print("API token to enable rich data widgets in your Dashboard:")
        for s in to_configure:
            console.print(f" - {manual_services[s]['Name']}", style="yellow")
        console.print("")
        
        do_setup = questionary.confirm("Would you like to set these up now?", default=False).ask()
        if do_setup:
            from src.utils.state import set_env_var
            for s in to_configure:
                cfg = manual_services[s]
                console.print(f"\n>> Configuring {cfg['Name']}", style="cyan")
                console.print(f"1. Open: {cfg['Url']}", style="grey50")
                console.print(f"2. {cfg['Hint']}", style="grey50")
                
                token = questionary.password(f"Paste the Token/Key here (leave blank to skip):").ask()
                if token and token.strip():
                    set_env_var(cfg["Var"], token.strip(), file_path=env_path)
                    console.print(f"[OK] Saved {cfg['Var']} to .env", style="green")

            # Restart maintenance stack
            hp_path = resolve_path_slash(os.path.join(target_dir, "stacks", "maintenance"))
            if os.path.exists(hp_path):
                write_step("Reloading Dashboard to apply new tokens...")
                try:
                    invoke_external_command("docker compose up -d --remove-orphans", description="Reloading Maintenance stack")
                except Exception:
                    pass

def get_default_deployment_dir() -> str:
    if sys.platform == "win32":
        return "C:/docker"
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return "/opt/docker"
    return resolve_path_slash(os.path.expanduser("~/docker"))

def get_deployment_dir_interactive(project_root: str, required: bool = True) -> str:
    console.print("\n--- Deployment Folder Selection ---", style="yellow")
    default_path = get_default_deployment_dir()
    if os.getenv("DS_HEADLESS") == "true":
        path = default_path
    else:
        path = questionary.text(f"Please provide the full path to your Docker deployment folder (default: {default_path}):").ask()
        if not path or not path.strip():
            path = default_path
        else:
            path = path.strip().replace("'", "").replace('"', "")

    norm_path = resolve_path_slash(path)
    
    if not os.path.exists(norm_path) and required:
        if os.getenv("DS_HEADLESS") == "true":
            create = True
        else:
            create = questionary.confirm(f"Folder '{norm_path}' does not exist. Create it?", default=True).ask()
        if create:
            os.makedirs(norm_path, exist_ok=True)
        else:
            return None

    if os.getenv("TEST_MODE") == "true":
        if "testing" not in norm_path.lower():
            raise RuntimeError(f"SECURITY FAULT: AIT tried to deploy to '{norm_path}' which is outside the testing/ sandbox.")

    return norm_path

def main():
    try:
        # UTF-8 Console encoding
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

        project_root = get_project_root()
        
        # Self-Update check (Headless/CI skips update)
        if os.getenv("TEST_MODE") != "true" and os.getenv("DS_HEADLESS") != "true":
            if invoke_self_update(project_root):
                write_log("Setup updated. Please restart the script.", level="INFO")
                sys.exit(0)

        debug_logging_enabled = False
        exit_script = False

        while not exit_script:
            console.print(f"\n--- Media Stack Manager v{VERSION} ---", style="cyan")
            console.print("[1] Install / Reconfigure / Upgrade Stack")
            console.print("[2] Force Update All Containers (Existing Setup)")
            console.print("[3] Uninstall Stack")
            debug_label = "[ENABLED]" if debug_logging_enabled else "[DISABLED]"
            console.print(f"[4] Toggle Verbose (Debug) Logging {debug_label}")
            console.print("[Q] Exit")
            console.print("")

            if os.getenv("DS_HEADLESS") == "true":
                choice = "1"
                exit_script = True
            else:
                choice = questionary.text("Select an option:").ask()

            if not choice or choice.strip().lower() == "q":
                exit_script = True
                break

            choice = choice.strip()
            
            if choice == "4":
                if debug_logging_enabled:
                    debug_logging_enabled = False
                    os.environ["DEBUG_LOGGING"] = "false"
                else:
                    debug_logging_enabled = True
                    enable_debug_logging()
                console.print(f"Verbose logging {'ENABLED' if debug_logging_enabled else 'DISABLED'} for this session.", style="yellow")
            
            elif choice == "1":
                d_dir = get_deployment_dir_interactive(project_root)
                if not d_dir:
                    continue
                os.environ["DEPLOY_DIR"] = d_dir

                # Smart Reconfigure / Upgrade menu
                metadata = get_metadata()
                os.environ["SKIP_SELECTION"] = "false"

                if metadata.get("selected_services"):
                    write_step(f"Existing Deployment Detected at {d_dir}", level="WARN")
                    
                    # Check for template updates
                    needs_upgrade = False
                    template_path = get_resource_path("templates.yml")
                    
                    sha256 = hashlib.sha256()
                    with open(template_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256.update(chunk)
                    current_hash = sha256.hexdigest().upper()
                    
                    if metadata.get("template_hash") != current_hash:
                        needs_upgrade = True

                    if os.getenv("DS_HEADLESS") != "true":
                        console.print("What would you like to do?")
                        console.print("[1] Add / Remove Services (Re-run Wizard)")
                        upgrade_label = "[2] Upgrade Templates (NEW UPDATES AVAILABLE!)" if needs_upgrade else "[2] Re-generate Stacks (Upgrade Templates)"
                        upgrade_style = "green" if needs_upgrade else "white"
                        console.print(upgrade_label, style=upgrade_style)
                        console.print("[3] Full Reset (Wipe selection/config and start fresh)")
                        console.print("[4] Cancel")
                        
                        sub_choice = questionary.text("Select an option:").ask()
                        if sub_choice == "2":
                            os.environ["SKIP_SELECTION"] = "true"
                            console.print("[UPGRADE] Regenerating stacks with latest templates...", style="cyan")
                        elif sub_choice == "3":
                            console.print("\n[bold red][!] WARNING: A Full Reset will completely destroy all active containers,[/bold red]")
                            console.print("[bold red]    remove docker volumes, and delete all configuration folders (appdata) under:[/bold red]")
                            console.print(f"    [cyan]{d_dir}[/cyan]\n")
                            confirm = questionary.confirm("Are you sure you want to permanently wipe all containers and configurations?", default=False).ask()
                            if confirm:
                                # Stop containers and clean volumes first if stacks exist
                                stacks_dir = resolve_path_slash(os.path.join(d_dir, "stacks"))
                                if os.path.exists(stacks_dir):
                                    for stack in os.listdir(stacks_dir):
                                        full_path = resolve_path_slash(os.path.join(stacks_dir, stack))
                                        if os.path.isdir(full_path):
                                            compose_file = resolve_path_slash(os.path.join(full_path, "docker-compose.yml"))
                                            if os.path.exists(compose_file):
                                                write_step(f"Removing containers & volumes for stack: {stack}")
                                                try:
                                                    subprocess.run(["docker", "compose", "down", "-v", "--remove-orphans"], cwd=full_path, capture_output=True)
                                                except Exception as e:
                                                    write_log(f"Failed to compose down stack {stack}: {str(e)}", level="WARN")

                                # Remove directories
                                write_step("Deleting configuration and stack directories")
                                shutil.rmtree(stacks_dir, ignore_errors=True)
                                shutil.rmtree(resolve_path_slash(os.path.join(d_dir, "appdata")), ignore_errors=True)
                                
                                # Remove metadata and environment files
                                for file in [".metadata.json", ".env"]:
                                    file_p = resolve_path_slash(os.path.join(d_dir, file))
                                    if os.path.exists(file_p):
                                        try:
                                            shutil.copy2(file_p, file_p + ".bak")
                                            console.print(f"[Backup] Saved backup to {file}.bak", style="grey50")
                                        except Exception:
                                            pass
                                        try:
                                            os.remove(file_p)
                                        except Exception:
                                            pass
                                console.print("Settings and configurations wiped. Starting fresh install...", style="green")
                            else:
                                console.print("[i] Reset cancelled. No containers or configurations were modified.", style="yellow")
                                continue
                        elif sub_choice == "4" or not sub_choice:
                            continue
                    else:
                        os.environ["SKIP_SELECTION"] = "true"

                set_log_path(d_dir)
                write_log(f"Initializing install at {d_dir}...", level="INFO", clear=True)

                failed = False
                try:
                    # Run linear modules
                    run_system_preflight()
                    select_services()
                    if not run_deploy_preflight():
                        # If user declined due to port conflicts
                        continue
                    configure_environment()
                    setup_directories()
                    setup_networks()
                    build_compose_stacks()
                    deploy_stacks()
                    auto_stitch_services()
                except Exception as e:
                    import traceback
                    err_msg = traceback.format_exc()
                    write_log(f"Fatal error in setup execution: {err_msg}", level="ERROR")
                    console.print(f"\n[!] SETUP FAILED\nReason: {str(e)}", style="bold red")
                    console.print(f"Please check the log for details: {get_log_path()}", style="grey50")
                    failed = True

                if not failed:
                    metadata = get_metadata()  # Reload metadata
                    console.print("\n==========================================", style="cyan")
                    console.print("         INSTALLATION SUMMARY", style="cyan")
                    console.print("==========================================", style="cyan")
                    console.print(f"Docker Dir:   {d_dir}")

                    if metadata.get("generated_stacks"):
                        console.print("\nGENERATED STACKS (Managed in Dockge):")
                        for stack in metadata["generated_stacks"]:
                            console.print(f" [OK] {stack.get('Name')}: {stack.get('Apps')}", style="green")

                    # Health check summary
                    if metadata.get("selected_services") and os.getenv("TEST_MODE") != "true":
                        console.print("\nSERVICE HEALTH STATUS:", style="yellow")
                        services_path = get_resource_path("services.yml")
                        master_registry = get_yaml_content(services_path)
                        registry_list = get_registry_list(master_registry)

                        for svc in metadata["selected_services"]:
                            reg = next((e for e in registry_list if e.key == svc), None)
                            if reg and reg.port != "0":
                                port = int(reg.port)
                                status = "ONLINE " if test_port("localhost", port) else "OFFLINE"
                                color = "green" if status == "ONLINE " else "red"
                                console.print(f" [{status}] ", end="", style=color)
                                console.print(f"{svc} (Port {port})")

                    console.print("==========================================", style="cyan")
                    console.print("\nSetup Complete! Your Media Stack is running.", style="green")

                    # Copy setup.log to deploy folder
                    log_file = resolve_path_slash(get_log_path())
                    d_dir_slash = resolve_path_slash(d_dir)
                    if os.path.exists(log_file):
                        try:
                            shutil.copy(log_file, d_dir_slash)
                        except shutil.SameFileError:
                            pass
                        except Exception as e:
                            write_log(f"Failed to copy log file: {str(e)}", level="DEBUG")

                    console.print("\nNEXT STEPS:", style="yellow")
                    console.print("1. Access your Dashboard at http://localhost:3000")
                    console.print("2. Access Dockge Management at http://localhost:5001")

                    # Extract credentials for printout
                    h_user = "admin"
                    h_pass = "[CHECK .ENV]"
                    env_file = resolve_path_slash(os.path.join(d_dir, ".env"))
                    if os.path.exists(env_file):
                        with open(env_file, "r", encoding="utf-8") as f:
                            for line in f:
                                match_u = re.match(r"^HTTP_USERNAME=(.*)", line)
                                match_p = re.match(r"^HTTP_PASSWORD=(.*)", line)
                                if match_u:
                                    h_user = match_u.group(1).strip()
                                if match_p:
                                    h_pass = match_p.group(1).strip()

                    console.print("3. Web Management Credentials:", style="cyan")
                    console.print(f"   - Username: {h_user}")
                    console.print(f"   - Password: {h_pass}")

                    console.print("\n4. Automated Configurations:", style="yellow")
                    if metadata.get("auto_config_results"):
                        for r in metadata["auto_config_results"]:
                            console.print(f"   [x] {r}", style="green")
                    else:
                        console.print("   [!] No automated configurations were performed.", style="grey50")

                    invoke_token_wizard(d_dir)
                    exit_script = True

            elif choice == "2":
                d_dir = get_deployment_dir_interactive(project_root)
                if d_dir and os.path.exists(resolve_path_slash(os.path.join(d_dir, "stacks"))):
                    os.environ["DEPLOY_DIR"] = d_dir
                    stacks_dir = resolve_path_slash(os.path.join(d_dir, "stacks"))
                    for stack in os.listdir(stacks_dir):
                        full_path = resolve_path_slash(os.path.join(stacks_dir, stack))
                        if os.path.isdir(full_path):
                            write_step(f"Updating Stack: {stack}")
                            # Execute docker compose pull and up
                            try:
                                subprocess.run(["docker", "compose", "up", "-d", "--pull", "always", "--remove-orphans"], cwd=full_path, check=True)
                            except Exception as e:
                                write_log(f"Failed to update stack {stack}: {str(e)}", level="ERROR")
                    exit_script = True
                else:
                    console.print("[!] Error: Deployment stacks not found.", style="red")

            elif choice == "3":
                d_dir = get_deployment_dir_interactive(project_root)
                if d_dir and os.path.exists(resolve_path_slash(os.path.join(d_dir, "stacks"))):
                    os.environ["DEPLOY_DIR"] = d_dir
                    
                    # Call uninstall utility
                    uninstall_script = resolve_path_slash(os.path.join(project_root, "src", "utils", "uninstall.py"))
                    if os.path.exists(uninstall_script):
                        subprocess.run([sys.executable, uninstall_script])
                    else:
                        # Manual inline uninstall
                        console.print("\n--- Uninstalling Stack ---", style="bold red")
                        confirm = questionary.confirm("Are you sure you want to completely uninstall all services and docker stacks?", default=False).ask()
                        if confirm:
                            stacks_dir = resolve_path_slash(os.path.join(d_dir, "stacks"))
                            for stack in os.listdir(stacks_dir):
                                full_path = resolve_path_slash(os.path.join(stacks_dir, stack))
                                if os.path.isdir(full_path):
                                    subprocess.run(["docker", "compose", "down", "-v", "--remove-orphans"], cwd=full_path)
                            shutil.rmtree(stacks_dir, ignore_errors=True)
                            console.print("Stacks and services successfully removed.", style="green")
                    exit_script = True
                else:
                    console.print("[!] Error: Invalid deployment folder.", style="red")

    except Exception as e:
        import traceback
        from rich.panel import Panel
        
        # Write traceback to setup.log
        error_trace = traceback.format_exc()
        write_log(f"CRITICAL EXCEPTION OCCURRED:\n{error_trace}", level="ERROR")
        
        log_path = get_log_path()
        error_msg = f"[bold red]An unexpected error occurred during execution.[/bold red]\n\n" \
                    f"[bold white]Reason:[/bold white] {str(e)}\n\n" \
                    f"Please review the logs for the full stack trace:\n" \
                    f"[cyan]{log_path}[/cyan]"
                    
        console.print(Panel(error_msg, title="[bold red]Critical Script Error[/bold red]", border_style="red"))
        
        if os.getenv("TEST_MODE") == "true":
            sys.exit(1)
    finally:
        if os.getenv("TEST_MODE") != "true" and os.getenv("DS_HEADLESS") != "true":
            input("\nPress Enter to close this window...")

if __name__ == "__main__":
    main()
