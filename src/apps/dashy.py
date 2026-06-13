from src.apps.base_app import BaseApp

class DashyApp(BaseApp):
    key = "dashy"
    name = "Dashy"
    port = 8095
    category = "networking"
    description = "Highly customizable, themeable personal dashboard for self-hosted apps."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dashboard"

    def get_compose_template(self) -> str:
        return f"""  dashy:
    image: lissy93/dashy:latest
    container_name: dashy
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/public
    ports:
      - 8095:80
"""
