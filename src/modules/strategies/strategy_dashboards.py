from src.utils.logger import write_log, write_step

def run_dashboards_strategy(selected, keys, registry_list, rest_invoker):
    """
    Handles connection stitching for Dashboard and Request management apps (Seerr).
    """
    results = []

    # 1. Seerr Linking (Connecting to Sonarr/Radarr)
    if "seerr" in selected and "seerr" in keys:
        s_key = keys["seerr"]
        s_header = {"X-Api-Key": s_key}
        for app in ["sonarr", "radarr"]:
            if app in selected and app in keys:
                write_log(f"Linking {app} to Seerr...")
                reg_entry = next((e for e in registry_list if e.key == app), None)
                if reg_entry:
                    endpoint = "settings/radarr" if app == "radarr" else "settings/sonarr"
                    active_dir = "/movies" if app == "radarr" else "/tv"
                    
                    payload = {
                        "name": f"{app.upper()} (Auto)", 
                        "hostname": app, 
                        "port": int(reg_entry.port),
                        "apiKey": keys[app], 
                        "useSsl": False, 
                        "isDefault": True,
                        "activeProfileId": 1, 
                        "activeDirectory": active_dir
                    }
                    if app == "sonarr":
                        payload["activeLanguageProfileId"] = 1
                    
                    try:
                        rest_invoker(f"http://localhost:5055/api/v1/{endpoint}", method="POST", json_payload=payload, headers=s_header)
                        results.append(f"Linked {app} to Seerr")
                    except Exception as e:
                        write_log(f"Failed to link {app} to Seerr: {str(e)}", level="WARN")
    
    return results
