from src.apps.base_app import BaseApp

class ItToolsApp(BaseApp):
    key = "it-tools"
    name = "IT-Tools"
    port = 8086
    category = "tools"
    description = "Useful offline-capable client-side tools for developers and IT professionals."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  it-tools:
    image: corentinth/it-tools:latest
    container_name: it-tools
    <<: *common-keys-apps
    ports:
      - 8086:80
"""
