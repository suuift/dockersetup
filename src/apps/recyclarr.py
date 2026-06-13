from src.apps.base_app import BaseApp
class RecyclarrApp(BaseApp):
    key = "recyclarr"
    name = "Recyclarr"
    port = 0
    category = "none"
    description = "Syncs recommended settings from TRaSH Guides to Sonarr and Radarr to ensure your media quality profiles are always optimal."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  recyclarr:
    image: ghcr.io/recyclarr/recyclarr:latest
    container_name: recyclarr
    user: $PUID:$PGID
    volumes:
      - $DOCKERDIR/appdata/recyclarr/config:/config
    environment:
      - TZ=$TZ
    restart: unless-stopped
"""
