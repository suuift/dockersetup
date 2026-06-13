from src.apps.base_app import BaseApp
class SabnzbdApp(BaseApp):
    key = "sabnzbd"
    name = "Sabnzbd"
    port = 8080
    category = "usenet"
    description = "Automated Usenet download tool that handles all file processing and verification with a simple web-based interface."
    stack_group = "downloaders"
    recommendations = ['prowlarr', 'sonarr', 'radarr']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  sabnzbd:
    image: lscr.io/linuxserver/sabnzbd:latest
    container_name: sabnzbd
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/sabnzbd/config:/config
      - $DATADRIVE/downloads:/downloads
      - $DATADRIVE/downloads/incomplete:/incompletedownloads
    ports:
      - 8080:8080
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        from src.utils.state import get_metadata
        import os
        import re
        results = []
        if self.key in keys:
            metadata = get_metadata()
            selected = metadata.get("selected_services", [])
            sso_enabled = any(provider in selected for provider in ["authelia", "authentik"])
            tier = os.getenv("DEPLOY_TIER", "1")
            http_user = os.getenv("HTTP_USERNAME", "admin")
            http_pass = os.getenv("HTTP_PASSWORD", "")

            sab_ini = os.path.join(deploy_dir, "appdata", "sabnzbd", "config", "sabnzbd.ini")
            if sso_enabled:
                write_log("Skipping SABnzbd credentials injection (delegated to SSO gateway).", level="DEBUG")
                results.append("SABnzbd configured unauthenticated (delegated to SSO gateway)")
            elif tier == "1":
                write_log("Skipping SABnzbd credentials injection for minimal installation.", level="DEBUG")
                results.append("SABnzbd configured unauthenticated")
                
                if not os.path.exists(sab_ini):
                    os.makedirs(os.path.dirname(sab_ini), exist_ok=True)
                    default_ini = "[misc]\nusername =\npassword =\n[servers]\n"
                    with open(sab_ini, "w", encoding="utf-8") as f:
                        f.write(default_ini)

                if os.getenv("DS_HEADLESS") != "true":
                    import questionary
                    from src.utils.logger import safe_confirm, console
                    if safe_confirm("\nWould you like to configure your USENET news server details now?", default=True):
                        host = questionary.text("Enter USENET Server Host (e.g. news.newsgroup.ninja):").ask()
                        if host and host.strip():
                            port = questionary.text("Enter Port (e.g. 563 for SSL, 119 for non-SSL):", default="563").ask()
                            username = questionary.text("Enter Newsgroup Username:").ask()
                            password = questionary.password("Enter Newsgroup Password:").ask()
                            
                            server_section = f"\n[[{host}]]\nname = {host}\nhost = {host}\nport = {port}\nusername = {username}\npassword = {password}\nconnections = 20\nssl = 1\nssl_verify = 2\nenable = 1\n"
                            try:
                                with open(sab_ini, "r", encoding="utf-8") as f:
                                    content = f.read()
                                if "[servers]" in content:
                                    content = content.replace("[servers]", f"[servers]\n{server_section}")
                                else:
                                    content += f"\n[servers]\n{server_section}"
                                with open(sab_ini, "w", encoding="utf-8") as f:
                                    f.write(content)
                                results.append("Configured primary USENET Server connection in SABnzbd")
                            except Exception as e:
                                write_log(f"Failed to pre-seed USENET server configuration: {str(e)}", level="WARN")

            if not sso_enabled and http_pass:
                write_step("Injecting Authentication for SABnzbd...")
                if os.path.exists(sab_ini):
                    try:
                        with open(sab_ini, "r", encoding="utf-8") as f:
                            ini_content = f.read()
                        
                        new_ini = re.sub(r"^username\s*=.*", f"username = {http_user}", ini_content, flags=re.MULTILINE)
                        new_ini = re.sub(r"^password\s*=.*", f"password = {http_pass}", new_ini, flags=re.MULTILINE)
                        
                        whitelist_value = "host_whitelist = sabnzbd, localhost, 127.0.0.1, 192.168.90.11"
                        if "host_whitelist" in new_ini:
                            new_ini = re.sub(r"^host_whitelist\s*=.*", whitelist_value, new_ini, flags=re.MULTILINE)
                        else:
                            if "[misc]" in new_ini:
                                new_ini = new_ini.replace("[misc]", f"[misc]\n{whitelist_value}")
                            else:
                                new_ini += f"\n{whitelist_value}\n"
                        
                        with open(sab_ini, "w", encoding="utf-8") as f:
                            f.write(new_ini)
                        results.append("Secured SABnzbd and configured host whitelist")
                    except Exception as e:
                        write_log(f"Failed to write SABnzbd configurations: {str(e)}", level="WARN")

            # Link SABnzbd to PVRs
            pvr_apps = ["sonarr", "radarr", "lidarr"]
            for app in pvr_apps:
                if app in keys:
                    write_log(f"Linking SABnzbd to {app}...")
                    pvr_port = 7878 if app == "radarr" else (8686 if app == "lidarr" else 8989)
                    api_v = "v1" if app == "lidarr" else "v3"
                    app_url = f"http://localhost:{pvr_port}/api/{api_v}/downloadclient?apikey={keys[app]}"
                    
                    sab_payload = {
                        "enable": True, 
                        "priority": 1, 
                        "name": "SABnzbd", 
                        "implementation": "Sabnzbd", 
                        "configContract": "SabnzbdSettings",
                        "fields": [
                            {"name": "host", "value": "sabnzbd"}, 
                            {"name": "port", "value": 8080},
                            {"name": "apiKey", "value": keys["sabnzbd"]}, 
                            {"name": "movieCategory", "value": "movies"},
                            {"name": "tvCategory", "value": "tv"}
                        ]
                    }
                    try:
                        rest_invoker(app_url, method="POST", json_payload=sab_payload)
                        results.append(f"Connected SABnzbd to {app}")
                    except Exception as e:
                        write_log(f"Failed to connect SABnzbd to {app}: {str(e)}", level="WARN")

        return results
