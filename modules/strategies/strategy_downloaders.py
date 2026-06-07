import os
import re
import json
import requests
from utils.logger import write_log, write_step

def run_downloaders_strategy(selected, keys, registry_list, http_user, http_pass, deploy_dir, rest_invoker):
    """
    Handles authentication and connection stitching for Download Clients (qBit, SABnzbd).
    """
    results = []

    # 1. SABnzbd Config Injection (Direct INI manipulation)
    if "sabnzbd" in selected and "sabnzbd" in keys:
        write_step("Injecting Authentication for SABnzbd...")
        sab_ini = os.path.join(deploy_dir, "appdata", "sabnzbd", "config", "sabnzbd.ini")
        if os.path.exists(sab_ini):
            try:
                with open(sab_ini, "r", encoding="utf-8") as f:
                    ini_content = f.read()
                
                # Replace username and password in the INI file
                new_ini = re.sub(r"^username\s*=.*", f"username = {http_user}", ini_content, flags=re.MULTILINE)
                new_ini = re.sub(r"^password\s*=.*", f"password = {http_pass}", new_ini, flags=re.MULTILINE)
                
                with open(sab_ini, "w", encoding="utf-8") as f:
                    f.write(new_ini)
                results.append("Secured SABnzbd with management credentials")
            except Exception as e:
                write_log(f"Failed to write SABnzbd auth configurations: {str(e)}", level="WARN")

    # 2. qBittorrent API Handshake (Requires cookie-based session)
    if "qbittorrent" in selected or "qbittorrent-vpn" in selected:
        qbit_port = 8081
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
                app_url = f"http://localhost:{reg_entry.port}/api/v3/downloadclient?apikey={keys[app]}"
                
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
