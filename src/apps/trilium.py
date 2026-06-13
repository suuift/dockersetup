from src.apps.base_app import BaseApp

class TriliumApp(BaseApp):
    key = "trilium"
    name = "Trilium Notes"
    port = 8091
    category = "tools"
    description = "Hierarchical note-taking application designed for constructing large personal knowledge bases."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  trilium:
    image: zadam/trilium:latest
    container_name: trilium
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/home/node/trilium-data
    ports:
      - 8091:8080
"""
