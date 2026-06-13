from src.apps.base_app import BaseApp

class ChangedetectionApp(BaseApp):
    key = "changedetection"
    name = "Changedetection.io"
    port = 5002
    category = "tools"
    description = "Self-hosted web page change detection, monitoring, and notification tool."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  changedetection:
    image: dgtlmoon/changedetection.io:latest
    container_name: changedetection
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/datastore
    ports:
      - 5002:5000
"""
