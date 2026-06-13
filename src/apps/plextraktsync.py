from src.apps.base_app import BaseApp
class PlextraktsyncApp(BaseApp):
    key = "plextraktsync"
    name = "Plextraktsync"
    port = 0
    category = "none"
    description = "Dynamic two-way synchronization tool between your Plex media library and Trakt.tv profiles."
    stack_group = "media-server"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  plextraktsync:
    image: ghcr.io/taxel/plextraktsync:latest
    container_name: plextraktsync
    <<: *common-keys-apps
    command: watch
    volumes:
      - $DOCKERDIR/appdata/plextraktsync:/app/config
"""
