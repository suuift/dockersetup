from src.apps.base_app import BaseApp

class DokployApp(BaseApp):
    key = "dokploy"
    name = "Dokploy"
    port = 3005
    category = "tools"
    description = "Self-hosted PaaS platform built on Docker for deploying applications and databases."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  dokploy:
    image: dokploy/dokploy:latest
    container_name: dokploy
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 3005:3000
"""
