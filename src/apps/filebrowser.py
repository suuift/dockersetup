from src.apps.base_app import BaseApp
class FilebrowserApp(BaseApp):
    key = "filebrowser"
    name = "Filebrowser"
    port = 8082
    category = "files"
    description = "Modern, fast web file browser. Replaces traditional FTP and provides a beautiful interface for managing server files."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    <<: *common-keys-apps
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/filebrowser/config/filebrowser.db:/database/filebrowser.db
      - $DOCKERDIR/appdata/filebrowser/config/settings.json:/config/settings.json
      - $DATADRIVE:/srv/Media
      - $DOCKERDIR:/srv/DockerData
"""
