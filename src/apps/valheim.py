from src.apps.base_app import BaseApp
class ValheimApp(BaseApp):
    key = "valheim"
    name = "Valheim"
    port = 2456
    category = "valheim"
    description = "Persistent dedicated server for Valheim, enabling you and your friends to explore and survive in a shared Viking world."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  valheim:
    image: lloesche/valheim-server:latest
    container_name: valheim
    <<: *common-keys-apps
    ports:
      - "2456-2457:2456-2457/udp"
    volumes:
      - $DOCKERDIR/appdata/valheim/config:/config
      - $DOCKERDIR/appdata/valheim/data:/opt/valheim
    environment:
      - SERVER_NAME=Valheim Server
      - WORLD_NAME=Bussh
      - SERVER_PASS=busting
"""
