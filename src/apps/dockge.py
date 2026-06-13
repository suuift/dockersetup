from src.apps.base_app import BaseApp
class DockgeApp(BaseApp):
    key = "dockge"
    name = "Dockge"
    port = 5001
    category = "stacks"
    description = "Modern and intuitive manager for Docker Compose stacks that simplifies editing and monitoring your deployments."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  dockge:
    image: louislam/dockge:1
    container_name: dockge
    restart: unless-stopped
    ports:
      - 5001:5001
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - $DOCKERDIR/appdata/dockge/data:/app/data
      - $DOCKERDIR/stacks:/app/stacks
    environment:
      - DOCKGE_STACKS_DIR=$DOCKERDIR/stacks
"""
