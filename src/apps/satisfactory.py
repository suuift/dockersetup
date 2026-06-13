from src.apps.base_app import BaseApp
class SatisfactoryApp(BaseApp):
    key = "satisfactory"
    name = "Satisfactory"
    port = 15777
    category = "satisfactory"
    description = "Dedicated server for hosting Satisfactory games, allowing players to build massive factories together on a persistent world."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  satisfactory:
    container_name: 'satisfactory-server'
    hostname: 'satisfactory-server'
    image: 'wolveix/satisfactory-server:latest'
    ports:
      - '8012:7777/tcp'
      - '8012:7777/udp'
      - '8888:8888/tcp'
    volumes:
      - $DOCKERDIR/appdata/satisfactory/config:/config
    environment:
      - MAXPLAYERS=10
      - PGID=1000
      - PUID=1000
      - STEAMBETA=true
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G
"""
