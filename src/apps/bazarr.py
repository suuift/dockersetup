from src.apps.base_app import BaseApp
class BazarrApp(BaseApp):
    key = "bazarr"
    name = "Bazarr"
    port = 6767
    category = "subs"
    description = "Companion to Sonarr and Radarr that automatically manages and downloads subtitles for your media collection."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  bazarr:
    image: lscr.io/linuxserver/bazarr:1.5.1
    container_name: bazarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/bazarr/config:/config
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/tv:/tv
    ports:
      - ${BAZARR_PORT:-6767}:6767
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log
        import os
        results = []
        if self.key in keys:
            b_key = keys[self.key]
            b_headers = {"X-Api-Key": b_key}
            
            env_port = os.getenv("BAZARR_PORT")
            bazarr_port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            bazarr_api_url = f"http://localhost:{bazarr_port}/api"

            if "sonarr" in keys:
                write_log("Linking Sonarr to Bazarr...")
                payload = {
                    "enabled": True,
                    "name": "Sonarr",
                    "host": "sonarr",
                    "port": 8989,
                    "apikey": keys["sonarr"],
                    "ssl": False,
                    "base_url": ""
                }
                try:
                    rest_invoker(f"{bazarr_api_url}/settings/sonarr", method="POST", json_payload=payload, headers=b_headers)
                    results.append("Connected Sonarr to Bazarr")
                except Exception as e:
                    write_log(f"Failed to link Sonarr to Bazarr: {str(e)}", level="WARN")

            if "radarr" in keys:
                write_log("Linking Radarr to Bazarr...")
                payload = {
                    "enabled": True,
                    "name": "Radarr",
                    "host": "radarr",
                    "port": 7878,
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
