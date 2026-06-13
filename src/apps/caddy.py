from src.apps.base_app import BaseApp

class CaddyApp(BaseApp):
    key = "caddy"
    name = "Caddy"
    port = 80
    category = "networking"
    description = "Lightweight reverse proxy and web server with automated HTTPS certificate management."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "reverse_proxy"

    def get_compose_template(self) -> str:
        return f"""  caddy:
    image: caddy:latest
    container_name: caddy
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}/Caddyfile:/etc/caddy/Caddyfile
      - {self.get_appdata_dir()}/data:/data
      - {self.get_appdata_dir()}/config:/config
    ports:
      - 80:80
      - 443:443
"""
