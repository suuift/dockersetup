from src.apps.base_app import BaseApp
class AutheliaApp(BaseApp):
    key = "authelia"
    name = "Authelia"
    port = 9091
    category = "auth"
    description = "Open-source authentication server providing 2FA and SSO to secure all your services behind a single login portal."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  authelia:
    image: authelia/authelia:latest
    container_name: authelia
    <<: *common-keys-core
    volumes:
      - $DOCKERDIR/appdata/authelia/config:/config
    ports:
      - 9091:9091
"""
