from src.apps.base_app import BaseApp

class DocmostApp(BaseApp):
    key = "docmost"
    name = "Docmost"
    port = 3006
    category = "tools"
    description = "Collaborative documentation, wiki, and knowledge base platform."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    required_database_type = "postgres"

    def get_compose_template(self) -> str:
        return f"""  docmost:
    image: docmost/docmost:latest
    container_name: docmost
    <<: *common-keys-apps
    environment:
      - APP_URL=http://localhost:3006
      - DB_URL=postgresql://postgres:${{DB_PASS}}@postgresql:5432/docmost
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 3006:3000
"""
