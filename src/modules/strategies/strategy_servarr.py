import os
import re
from src.utils.logger import write_log, write_step

def run_servarr_strategy(selected, keys, registry_list, http_user, http_pass, rest_invoker):
    """
    Handles authentication injection and cross-linking for Servarr applications (Sonarr, Radarr, etc.)
    """
    results = []
    # Apps that support the standard v3/v1 Servarr API for auth and linking
    arr_apps = ["sonarr", "radarr", "lidarr", "readarr", "mylar", "prowlarr"]
    
    # 1. Authentication Injection (Forms-based auth with management credentials)
    for app in arr_apps:
        if app in selected and app in keys and app != "prowlarr":
            reg_entry = next((e for e in registry_list if e.key == app), None)
            if reg_entry:
                write_step(f"Injecting Authentication for {app}...")
                # Sonarr/Radarr/Readarr use v3, Lidarr/Mylar/Prowlarr use v1
                api_version = "v1" if app in ["prowlarr", "lidarr", "mylar"] else "v3"
                api_url = f"http://localhost:{reg_entry.port}/api/{api_version}/config/host"
                api_key = keys[app]
                headers = {"X-Api-Key": api_key}
                
                try:
                    current_config = rest_invoker(api_url, method="GET", headers=headers)
                    if current_config:
                        current_config["authenticationMethod"] = "Forms"
                        current_config["username"] = http_user
                        current_config["password"] = http_pass
                        
                        rest_invoker(api_url, method="PUT", json_payload=current_config, headers=headers)
                        results.append(f"Secured {app} with management credentials")
                except Exception as e:
                    write_log(f"Failed to inject auth for {app}: {str(e)}", level="WARN")

    # 2. Prowlarr Stitching (Linking Indexers to PVRs)
    if "prowlarr" in keys:
        p_key = keys["prowlarr"]
        p_url = f"http://localhost:9696/api/v1/applications?apikey={p_key}"
        
        # PVRs to link to Prowlarr
        pvrs = ["sonarr", "radarr", "lidarr", "readarr", "mylar"]
        for app in pvrs:
            if app in selected and app in keys:
                write_log(f"Stitching Prowlarr to {app}...")
                reg_entry = next((e for e in registry_list if e.key == app), None)
                if reg_entry:
                    payload = {
                        "name": app.upper(),
                        "configContract": f"{app.capitalize()}Settings",
                        "implementation": app.capitalize(),
                        "fields": [
                            {"name": "prowlarrUrl", "value": "http://prowlarr:9696"},
                            {"name": "baseUrl", "value": f"http://{app}:{reg_entry.port}"},
                            {"name": "apiKey", "value": keys[app]},
                            {"name": "syncLevel", "value": "fullSync"}
                        ]
                    }
                    try:
                        rest_invoker(p_url, method="POST", json_payload=payload)
                        results.append(f"Linked Prowlarr to {app}")
                    except Exception as e:
                        write_log(f"Failed to link Prowlarr to {app}: {str(e)}", level="WARN")

        # 3. Flaresolverr Proxy (Anti-Cloudflare for Indexers)
        if "flaresolverr" in selected:
            write_log("Adding FlareSolverr proxy to Prowlarr...")
            proxy_url = f"http://localhost:9696/api/v1/indexerproxy?apikey={p_key}"
            proxy_payload = {
                "name": "FlareSolverr",
                "implementation": "FlareSolverr",
                "configContract": "FlareSolverrSettings",
                "fields": [
                    {"name": "host", "value": "http://flaresolverr:8191"},
                    {"name": "requestTimeout", "value": 60}
                ]
            }
            try:
                rest_invoker(proxy_url, method="POST", json_payload=proxy_payload)
                results.append("Added FlareSolverr proxy to Prowlarr")
            except Exception as e:
                write_log(f"Failed to add FlareSolverr proxy to Prowlarr: {str(e)}", level="WARN")

    return results