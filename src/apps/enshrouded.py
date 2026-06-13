from src.apps.base_app import BaseApp
class EnshroudedApp(BaseApp):
    key = "enshrouded"
    name = "Enshrouded"
    port = 15636
    category = "enshrouded"
    description = "Dedicated server for cooperative multiplayer in the voxel-based survival world of Enshrouded."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  enshrouded:
    image: mornedhels/enshrouded-server:latest
    container_name: enshrouded
    hostname: enshrouded
    <<: *common-keys-apps
    stop_grace_period: 90s
    ports:
      - "15637:15637/udp"
    volumes:
      - $DOCKERDIR/appdata/enshrouded/data:/opt/enshrouded
    environment:
      - SERVER_NAME=Enshrouded Server
      - SERVER_PASSWORD=secret
      - UPDATE_CRON=*/30 * * * *
      - PUID=4711
      - PGID=4711
"""
