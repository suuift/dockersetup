import os
from src.utils.logger import write_log, write_step

def run_bazarr_strategy(selected, keys, registry_list, rest_invoker):
    """
    Handles automatic connection stitching of Sonarr/Radarr into Bazarr.
    """
    results = []

    if "bazarr" in selected and "bazarr" in keys:
        b_key = keys["bazarr"]
        b_headers = {"X-Api-Key": b_key}
        
        # Determine Bazarr port (default 6767)
        env_port = os.getenv("BAZARR_PORT")
        if env_port and env_port.isdigit():
            bazarr_port = int(env_port)
        else:
            bazarr_port = 6767
            reg_b = next((e for e in registry_list if e.key == "bazarr"), None)
            if reg_b and reg_b.port:
                bazarr_port = int(reg_b.port)
            
        bazarr_api_url = f"http://localhost:{bazarr_port}/api"

        # Sonarr Integration in Bazarr
        if "sonarr" in selected and "sonarr" in keys:
            write_log("Linking Sonarr to Bazarr...")
            reg_s = next((e for e in registry_list if e.key == "sonarr"), None)
            if reg_s:
                payload = {
                    "enabled": True,
                    "name": "Sonarr",
                    "host": "sonarr",
                    "port": int(reg_s.port),
                    "apikey": keys["sonarr"],
                    "ssl": False,
                    "base_url": ""
                }
                try:
                    rest_invoker(f"{bazarr_api_url}/settings/sonarr", method="POST", json_payload=payload, headers=b_headers)
                    results.append("Connected Sonarr to Bazarr")
                except Exception as e:
                    write_log(f"Failed to link Sonarr to Bazarr: {str(e)}", level="WARN")

        # Radarr Integration in Bazarr
        if "radarr" in selected and "radarr" in keys:
            write_log("Linking Radarr to Bazarr...")
            reg_r = next((e for e in registry_list if e.key == "radarr"), None)
            if reg_r:
                payload = {
                    "enabled": True,
                    "name": "Radarr",
                    "host": "radarr",
                    "port": int(reg_r.port),
                    "apikey": keys["radarr"],
                    "ssl": False,
                    "base_url": ""
                }
                try:
                    rest_invoker(f"{bazarr_api_url}/settings/radarr", method="POST", json_payload=payload, headers=b_headers)
                    results.append("Connected Radarr to Bazarr")
                except Exception as e:
                    write_log(f"Failed to link Radarr to Bazarr: {str(e)}", level="WARN")

    return results
