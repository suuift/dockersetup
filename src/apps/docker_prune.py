from src.apps.base_app import BaseApp
class DockerPruneApp(BaseApp):
    key = "docker-prune"
    name = "Docker-Prune"
    port = 0
    category = "none"
    description = "Utility that automatically cleans up unused Docker images, containers, and networks daily to keep your system lean."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  docker-prune:
    image: softonic/docker-system-prune:latest
    container_name: docker-prune
    <<: *common-keys-core
    entrypoint: ["/bin/sh", "-c", "while true; do /run.sh --volumes --all; sleep 86400; done"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
"""
