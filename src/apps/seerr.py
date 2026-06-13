from src.apps.base_app import BaseApp
class SeerrApp(BaseApp):
    key = "seerr"
    name = "Seerr"
    port = 5055
    category = "requests"
    description = "Unified request management and media discovery dashboard for your Plex or Jellyfin ecosystem."
    stack_group = "media-server"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  seerr:
    image: ghcr.io/seerr-team/seerr:latest
    container_name: seerr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/seerr/config:/config
    ports:
      - 5055:5055
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log
        results = []
        if self.key in keys:
            s_key = keys[self.key]
            s_header = {"X-Api-Key": s_key}
            for app in ["sonarr", "radarr"]:
                if app in keys:
                    write_log(f"Linking {app} to Seerr...")
                    endpoint = "settings/radarr" if app == "radarr" else "settings/sonarr"
                    active_dir = "/movies" if app == "radarr" else "/tv"
                    port = 7878 if app == "radarr" else 8989
                    
                    payload = {
                        "name": f"{app.upper()} (Auto)", 
                        "hostname": app, 
                        "port": port,
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
