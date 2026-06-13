from src.apps.base_app import BaseApp

class BeszelApp(BaseApp):
    key = "beszel"
    name = "Beszel"
    port = 8090
    category = "management"
    description = "Lightweight resource monitor offering CPU, RAM, disk, and Docker container stats."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  beszel:
    image: henrygd/beszel:latest
    container_name: beszel
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/beszel_data
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - 8090:8090
"""
