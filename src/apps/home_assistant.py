from src.apps.base_app import BaseApp

class HomeAssistantApp(BaseApp):
    key = "home-assistant"
    name = "Home Assistant"
    port = 8123
    category = "networking"
    description = "Home automation hub that aggregates and controls smart devices locally."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  home-assistant:
    image: homeassistant/home-assistant:stable
    container_name: home-assistant
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
      - /run/dbus:/run/dbus:ro
    ports:
      - 8123:8123
"""
