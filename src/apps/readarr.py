from src.apps.base_app import BaseApp
class ReadarrApp(BaseApp):
    key = "readarr"
    name = "Readarr"
    port = 8787
    category = "books"
    description = "Book downloader and library manager that automatically handles both E-books and Audiobooks via Usenet and BitTorrent."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  readarr:
    image: lscr.io/linuxserver/readarr:develop
    container_name: readarr
    <<: *common-keys-apps
    environment:
      <<: *default-tz-puid-pgid
    volumes:
      - $DOCKERDIR/appdata/readarr/config:/config
      - $DATADRIVE/books:/books
      - $DATADRIVE/audiobooks:/audiobooks
      - $DATADRIVE/downloads:/downloads
    ports:
      - 8787:8787
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        import os
        results = []
        if self.key in keys:
            api_key = keys[self.key]
            headers = {"X-Api-Key": api_key}
            env_port = os.getenv("READARR_PORT")
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
        return results
