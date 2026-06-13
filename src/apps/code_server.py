from src.apps.base_app import BaseApp

class CodeServerApp(BaseApp):
    key = "code-server"
    name = "Code-Server"
    port = 8443
    category = "tools"
    description = "Run VS Code on your home server in a secure web browser workspace."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  code-server:
    image: linuxserver/code-server:latest
    container_name: code-server
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 8443:8443
"""
