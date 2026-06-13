from src.apps.base_app import BaseApp
class RadarrApp(BaseApp):
    key = "radarr"
    name = "Radarr"
    port = 7878
    category = "movies"
    description = "Movie PVR for Usenet and BitTorrent. Automatically monitors for new movies and interfaces with download clients to organize your library."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'bazarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/radarr/config:/config
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/downloads:/downloads
    ports:
      - ${RADARR_PORT:-7878}:7878
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        import os
        results = []
        if self.key in keys:
            api_key = keys[self.key]
            headers = {"X-Api-Key": api_key}
            env_port = os.getenv("RADARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            base_url = f"http://localhost:{port}/api/v3"
            
            write_step(f"Injecting Authentication for {self.name}...")
            try:
                current_config = rest_invoker(f"{base_url}/config/host", method="GET", headers=headers)
                if current_config:
                    current_config["authenticationMethod"] = "external"
                    rest_invoker(f"{base_url}/config/host", method="PUT", json_payload=current_config, headers=headers)
                    results.append(f"Configured {self.name} with external authentication")
            except Exception as e:
                write_log(f"Failed to inject auth for {self.name}: {str(e)}", level="WARN")

            try:
                naming_config = rest_invoker(f"{base_url}/config/naming", method="GET", headers=headers)
                if naming_config:
                    naming_config["renameEpisodes"] = True
                    rest_invoker(f"{base_url}/config/naming", method="PUT", json_payload=naming_config, headers=headers)
                    results.append(f"Enabled renaming rules for {self.name}")
            except Exception as e:
                write_log(f"Failed to enable renaming for {self.name}: {str(e)}", level="WARN")

            try:
                rest_invoker(f"{base_url}/rootfolder", method="POST", json_payload={"path": "/movies"}, headers=headers)
                results.append(f"Configured default root path '/movies' for {self.name}")
            except Exception:
                pass

            plex_token = os.getenv("PLEX_TOKEN")
            if plex_token and plex_token.strip():
                try:
                    payload = {
                        "name": "Plex Watchlist",
                        "enableAuto": True,
                        "enabled": True,
                        "shouldMonitor": True,
                        "listType": "plex",
                        "implementation": "PlexWatchlistImport",
                        "configContract": "PlexWatchlistSettings",
                        "qualityProfileId": 1,
                        "rootFolderPath": "/movies",
                        "searchOnAdd": True,
                        "minimumAvailability": "announced",
                        "fields": [
                            {"name": "plexToken", "value": plex_token.strip()},
                            {"name": "syncInterval", "value": 180}
                        ],
                        "tags": []
                    }
                    rest_invoker(f"{base_url}/importlist", method="POST", json_payload=payload, headers=headers)
                    results.append(f"Configured Plex Watchlist import list for {self.name}")
                except Exception as e:
                    write_log(f"Failed to configure Plex Watchlist for {self.name}: {str(e)}", level="WARN")

            try:
                stevenlu_payload = {
                    "name": "StevenLu List",
                    "enableAuto": True,
                    "enabled": True,
                    "shouldMonitor": True,
                    "listType": "popular",
                    "implementation": "StevenLuImport",
                    "configContract": "StevenLuSettings",
                    "qualityProfileId": 1,
                    "rootFolderPath": "/movies",
                    "searchOnAdd": False,
                    "minimumAvailability": "announced",
                    "fields": [
                        {"name": "baseUrl", "value": "https://api.radarr.video/v1/ma/movie/popular"}
                    ],
                    "tags": []
                }
                rest_invoker(f"{base_url}/importlist", method="POST", json_payload=stevenlu_payload, headers=headers)
                results.append("Configured StevenLu Movie List for Radarr")
            except Exception as e:
                write_log(f"Failed to configure StevenLu list for Radarr: {str(e)}", level="WARN")

        return results
