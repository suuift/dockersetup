from src.apps.base_app import BaseApp
class TautulliApp(BaseApp):
    key = "tautulli"
    name = "Tautulli"
    port = 8181
    category = "stats"
    description = "Comprehensive monitoring and analytics tool for Plex that provides detailed statistics on watch history and user activity."
    stack_group = "media-server"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  tautulli:
    image: lscr.io/linuxserver/tautulli:latest
    container_name: tautulli
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/tautulli/config:/config
    ports:
      - 8181:8181
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log
        import configparser
        import os
        results = []
        if self.key in keys:
            plex_token = os.getenv("PLEX_TOKEN")
            if plex_token and plex_token.strip():
                config_file = os.path.join(deploy_dir, "appdata", "tautulli", "config.ini")
                # Ensure the folder structure exists
                os.makedirs(os.path.dirname(config_file), exist_ok=True)
                try:
                    config = configparser.ConfigParser(strict=False, empty_lines_in_values=False)
                    if os.path.exists(config_file):
                        config.read(config_file, encoding="utf-8")
                    if not config.has_section("General"):
                        config.add_section("General")
                    config.set("General", "pms_url", "http://plex:32400")
                    config.set("General", "pms_token", plex_token.strip())
                    with open(config_file, "w", encoding="utf-8") as f:
                        config.write(f)
                    write_log("Successfully pre-seeded Tautulli config.ini with Plex token and URL.", level="INFO")
                    results.append("Configured Tautulli connection to Plex")
                except Exception as e:
                    write_log(f"Warning: Failed to seed Tautulli config.ini: {str(e)}", level="WARN")
        return results
