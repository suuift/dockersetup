import os
import re
import json
import requests
from src.utils.logger import write_log, write_step

def run_downloaders_strategy(selected, keys, registry_list, http_user, http_pass, deploy_dir, rest_invoker, tier="1"):
    """
    Handles authentication and connection stitching for Download Clients (qBit, SABnzbd).
    """
    results = []
    
    # Check if centralized identity provider / SSO is enabled
    identity_providers = ["authelia", "authentik"]
    sso_enabled = any(provider in selected for provider in identity_providers)

    # 1. SABnzbd Config Injection (Direct INI manipulation)
    if "sabnzbd" in selected and "sabnzbd" in keys:
        if sso_enabled:
            write_log("Skipping SABnzbd credentials injection (delegated to SSO gateway).", level="DEBUG")
            results.append("SABnzbd configured unauthenticated (delegated to SSO gateway)")
        elif tier == "1":
            write_log("Skipping SABnzbd credentials injection for minimal installation.", level="DEBUG")
            results.append("SABnzbd configured unauthenticated")
            # Prompts user for Usenet provider credentials interactively (automated helper)
            import questionary
            from src.utils.logger import safe_confirm, console
            sab_ini = os.path.join(deploy_dir, "appdata", "sabnzbd", "config", "sabnzbd.ini")
            
            # Seed default ini structure if missing so we can search/replace
            if not os.path.exists(sab_ini):
                os.makedirs(os.path.dirname(sab_ini), exist_ok=True)
                default_ini = "[misc]\nusername =\npassword =\n[servers]\n"
                with open(sab_ini, "w", encoding="utf-8") as f:
                    f.write(default_ini)

            if os.getenv("DS_HEADLESS") != "true" and safe_confirm("\nWould you like to configure your USENET news server details now?", default=True):
                host = questionary.text("Enter USENET Server Host (e.g. news.newsgroup.ninja):").ask()
                if host and host.strip():
                    port = questionary.text("Enter Port (e.g. 563 for SSL, 119 for non-SSL):", default="563").ask()
                    username = questionary.text("Enter Newsgroup Username:").ask()
                    password = questionary.password("Enter Newsgroup Password:").ask()
                    
                    server_section = f"""
[[{host}]]
name = {host}
host = {host}
port = {port}
username = {username}
password = {password}
connections = 20
ssl = 1
ssl_verify = 2
enable = 1
"""
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

            write_step("Injecting Authentication for SABnzbd...")
            if os.path.exists(sab_ini):
                try:
                    with open(sab_ini, "r", encoding="utf-8") as f:
                        ini_content = f.read()
                    
                    # Replace username and password in the INI file
                    new_ini = re.sub(r"^username\s*=.*", f"username = {http_user}", ini_content, flags=re.MULTILINE)
                    new_ini = re.sub(r"^password\s*=.*", f"password = {http_pass}", new_ini, flags=re.MULTILINE)
                    
                    # Ensure host_whitelist includes sabnzbd, localhost, 127.0.0.1, and subnets
                    whitelist_value = "host_whitelist = sabnzbd, localhost, 127.0.0.1, 192.168.90.11"
                    if "host_whitelist" in new_ini:
                        new_ini = re.sub(r"^host_whitelist\s*=.*", whitelist_value, new_ini, flags=re.MULTILINE)
                    else:
                        # Append it under [misc] section if possible, or just append to end of file if section not found easily
                        # Usually it is under [misc] section. Let's find [misc] and insert it
                        if "[misc]" in new_ini:
                            new_ini = new_ini.replace("[misc]", f"[misc]\n{whitelist_value}")
                        else:
                            new_ini += f"\n{whitelist_value}\n"
                    
                    with open(sab_ini, "w", encoding="utf-8") as f:
                        f.write(new_ini)
                    results.append("Secured SABnzbd and configured host whitelist")
                except Exception as e:
                    write_log(f"Failed to write SABnzbd configurations: {str(e)}", level="WARN")

    # 2. qBittorrent API Handshake (Requires cookie-based session)
    if "qbittorrent" in selected or "qbittorrent-vpn" in selected:
        if sso_enabled:
            write_log("Skipping qBittorrent credentials injection (delegated to SSO gateway).", level="DEBUG")
            results.append("qBittorrent configured with default credentials (delegated to SSO gateway)")
        elif tier == "1":
            write_log("Skipping qBittorrent credentials injection for minimal installation.", level="DEBUG")
            results.append("qBittorrent configured with default credentials")
        else:
            qbit_port = int(os.getenv("QBITTORRENT_PORT", "8081"))
            write_step("Injecting Authentication for qBittorrent...")
            
            # Try both the new management credentials and the default admin/adminadmin
            creds_to_try = [
                {"u": http_user, "p": http_pass},
                {"u": "admin", "p": "adminadmin"}
            ]
            
            login_success = False
            qbit_session = requests.Session()
            
            for cred in creds_to_try:
                try:
                    payload = {"username": cred["u"], "password": cred["p"]}
                    # Localhost always uses verify=False (Edge Case 1)
                    res = qbit_session.post(
                        f"http://localhost:{qbit_port}/api/v2/auth/login",
                        data=payload,
                        timeout=5,
                        verify=False
                    )
                    if res.text.strip() == "Ok.":
                        login_success = True
                        break
                except Exception:
                    pass
            
            if login_success:
                try:
                    prefs = {"web_ui_username": http_user, "web_ui_password": http_pass}
                    qbit_session.post(
                        f"http://localhost:{qbit_port}/api/v2/app/setPreferences",
                        data={"json": json.dumps(prefs)},
                        timeout=5,
                        verify=False
                    )
                    results.append("Secured qBittorrent with management credentials")
                except Exception as e:
                    write_log(f"Failed to set qBittorrent preferences: {str(e)}", level="WARN")

    # 3. Downloaders -> PVRs (Linking clients into Sonarr/Radarr/Lidarr)
    pvr_apps = ["sonarr", "radarr", "lidarr"]
    for app in pvr_apps:
        if app in selected and app in keys:
            reg_entry = next((e for e in registry_list if e.key == app), None)
            if reg_entry:
                env_port = os.getenv(f"{app.upper()}_PORT")
                port = int(env_port) if (env_port and env_port.isdigit()) else int(reg_entry.port)
                app_url = f"http://localhost:{port}/api/v3/downloadclient?apikey={keys[app]}"
                
                # SABnzbd Linking
                if "sabnzbd" in selected and "sabnzbd" in keys:
                    write_log(f"Linking SABnzbd to {app}...")
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
