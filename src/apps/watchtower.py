from src.apps.base_app import BaseApp
class WatchtowerApp(BaseApp):
    key = "watchtower"
    name = "Watchtower"
    port = 0
    category = "none"
    description = "Automates Docker base image updates by watching your running containers and restarting them when a new image version is available."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    <<: *common-keys-core
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      DOCKER_API_VERSION: 1.44
      <<: *default-tz-puid-pgid
"""
