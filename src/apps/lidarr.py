from src.apps.base_app import BaseApp
class LidarrApp(BaseApp):
    key = "lidarr"
    name = "Lidarr"
    port = 8686
    category = "music"
    description = "Music collection manager that automatically discovers and downloads music from various providers."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  lidarr:
    image: lscr.io/linuxserver/lidarr:nightly
    container_name: lidarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/lidarr/config:/config
      - $DATADRIVE/music:/music
      - $DATADRIVE/downloads:/downloads
    ports:
      - ${LIDARR_PORT:-8686}:8686
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
            env_port = os.getenv("LIDARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            base_url = f"http://localhost:{port}/api/v1"
            
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
                    naming_config["renameTracks"] = True
                    rest_invoker(f"{base_url}/config/naming", method="PUT", json_payload=naming_config, headers=headers)
                    results.append(f"Enabled renaming rules for {self.name}")
            except Exception as e:
                write_log(f"Failed to enable renaming for {self.name}: {str(e)}", level="WARN")

            try:
                rest_invoker(f"{base_url}/rootfolder", method="POST", json_payload={"path": "/music"}, headers=headers)
                results.append(f"Configured default root path '/music' for {self.name}")
            except Exception:
                pass
        return results
