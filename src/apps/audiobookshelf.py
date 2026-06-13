from src.apps.base_app import BaseApp
class AudiobookshelfApp(BaseApp):
    key = "audiobookshelf"
    name = "Audiobookshelf"
    port = 13378
    category = "books"
    description = "Self-hosted audiobook and podcast server with a beautiful web UI and full-featured mobile apps."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    container_name: audiobookshelf
    <<: *common-keys-apps
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/audiobookshelf/config:/config
      - $DOCKERDIR/appdata/audiobookshelf/metadata:/metadata
      - $DATADRIVE/audiobooks:/audiobooks
      - $DATADRIVE/books:/books
      - $DATADRIVE/podcasts:/podcasts
    ports:
      - 13378:80
"""
