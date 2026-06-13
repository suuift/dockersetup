from src.apps.base_app import BaseApp

class MealieApp(BaseApp):
    key = "mealie"
    name = "Mealie"
    port = 9005
    category = "tools"
    description = "Self-hosted recipe manager and meal planner with website recipe scraper."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  mealie:
    image: ghcr.io/mealie-recipes/mealie:latest
    container_name: mealie
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 9005:9000
"""
