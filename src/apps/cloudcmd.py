from src.apps.base_app import BaseApp
class CloudcmdApp(BaseApp):
    key = "cloudcmd"
    name = "Cloudcmd"
    port = 8000
    category = "files"
    description = "Web-based file manager with a built-in editor and terminal for managing your server files directly from your browser."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  cloudcmd:
    image: coderaiser/cloudcmd:latest
    container_name: cloudcmd
    <<: *common-keys-apps
    environment:
      - CLOUDCMD_AUTHENTICATION=true
      - CLOUDCMD_USERNAME=$HTTP_USERNAME
      - CLOUDCMD_PASSWORD=$HTTP_PASSWORD
    volumes:
      - $DATADRIVE:/media_pool
      - $DOCKERDIR:/docker_data
"""
