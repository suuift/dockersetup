from src.apps.base_app import BaseApp

class AutheliaApp(BaseApp):
    key = "authelia"
    name = "Authelia"
    port = 9091
    category = "networking"
    description = "Lightweight Single Sign-On and 2FA authentication portal for reverse proxies."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  authelia:
    image: authelia/authelia:latest
    container_name: authelia
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 9091:9090
"""
