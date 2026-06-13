from src.apps.base_app import BaseApp
class JellyfinApp(BaseApp):
    key = "jellyfin"
    name = "Jellyfin"
    port = 8096
    category = "jellyfin"
    description = "Free, open-source media system that provides total control over managing and streaming your media with no strings attached."
    stack_group = "media-server"
    recommendations = ['seerr', 'watchtower']
    is_configurable = False
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    <<: *common-keys-core
    environment:
      <<: *default-tz-puid-pgid
    ports:
      - 8096:8096
    volumes:
      - $DOCKERDIR/appdata/jellyfin/config:/config
      - $DATADRIVE/tv:/tv
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/anime:/anime
      - $DATADRIVE/music:/music
      - $DATADRIVE/audiobooks:/audiobooks
      - $DATADRIVE/books:/books
"""
