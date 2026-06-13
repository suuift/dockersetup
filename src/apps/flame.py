from src.apps.base_app import BaseApp

class FlameApp(BaseApp):
    key = "flame"
    name = "Flame"
    port = 5005
    category = "networking"
    description = "Minimalist dashboard for self-hosted services and bookmarks."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dashboard"

    def get_compose_template(self) -> str:
        return f"""  flame:
    image: pawelmalak/flame:latest
    container_name: flame
    <<: *common-keys-apps
    environment:
      - PASSWORD=${{HTTP_PASSWORD}}
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 5005:5005
"""
