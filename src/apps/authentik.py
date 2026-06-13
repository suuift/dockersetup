from src.apps.base_app import BaseApp

class AuthentikApp(BaseApp):
    key = "authentik"
    name = "Authentik"
    port = 9002
    category = "networking"
    description = "Feature-rich Identity Provider (SSO) with custom user flows and app portals."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    required_database_type = "postgres"

    def get_compose_template(self) -> str:
        return f"""  authentik:
    image: ghcr.io/goauthentik/server:latest
    container_name: authentik
    <<: *common-keys-apps
    command: start
    environment:
      - AUTHENTIK_REDIS__HOST=valkey
      - AUTHENTIK_POSTGRESQL__HOST=postgresql
      - AUTHENTIK_POSTGRESQL__USER=postgres
      - AUTHENTIK_POSTGRESQL__PASSWORD=${{DB_PASS}}
      - AUTHENTIK_POSTGRESQL__DB=authentik
    volumes:
      - {self.get_appdata_dir()}/media:/media
      - {self.get_appdata_dir()}/templates:/templates
    ports:
      - 9002:9000
      - 9443:9443
"""
