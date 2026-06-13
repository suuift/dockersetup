from src.apps.base_app import BaseApp
class PortainerApp(BaseApp):
    key = "portainer"
    name = "Portainer"
    port = 9443
    category = "docker"
    description = "Powerful GUI for managing Docker containers, images, and networks through a user-friendly web interface."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  portainer:
    container_name: portainer
    image: portainer/portainer-ce:latest
    command: -H unix:///var/run/docker.sock
    ports:
      - 9443:9443
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - $DOCKERDIR/appdata/portainer/data:/data
    <<: *common-keys-core
    environment:
      <<: *default-tz-puid-pgid
"""
