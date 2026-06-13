from src.apps.base_app import BaseApp

class FileflowsApp(BaseApp):
    key = "fileflows"
    name = "FileFlows"
    port = 5001
    category = "tools"
    description = "Create automated workflows to process files (transcode, rename, move, clean)."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  fileflows:
    image: fileflows/fileflows:latest
    container_name: fileflows
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}/Data:/app/Data
      - {self.get_appdata_dir()}/Logs:/app/Logs
    ports:
      - 5001:5000
"""
