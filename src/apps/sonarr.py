from src.apps.base_app import BaseApp
class SonarrApp(BaseApp):
    key = "sonarr"
    name = "Sonarr"
    port = 8989
    category = "tv"
    description = "Smart TV show PVR for Usenet and BitTorrent. Monitors RSS feeds for new episodes and handles grabbing, sorting, and renaming."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'bazarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  # PORT: 8989
  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/sonarr/config:/config
      - $DATADRIVE/tv:/tv
      - $DATADRIVE/anime:/anime
      - $DATADRIVE/downloads:/downloads
    ports:
      - ${SONARR_PORT:-8989}:8989
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
            env_port = os.getenv("SONARR_PORT")
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
                rest_invoker(f"{base_url}/rootfolder", method="POST", json_payload={"path": "/tv"}, headers=headers)
                results.append(f"Configured default root path '/tv' for {self.name}")
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
                        "rootFolderPath": "/tv",
                        "searchOnAdd": True,
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
        return results
