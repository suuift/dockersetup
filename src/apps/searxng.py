from src.apps.base_app import BaseApp

class SearxngApp(BaseApp):
    key = "searxng"
    name = "SearXNG"
    port = 8087
    category = "tools"
    description = "Privacy metasearch engine aggregating queries anonymously from multiple sites."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/etc/searxng
    ports:
      - 8087:8080
"""
