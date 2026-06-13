from src.apps.base_app import BaseApp
class NavidromeApp(BaseApp):
    key = "navidrome"
    name = "Navidrome"
    port = 4533
    category = "music"
    description = "High-performance music streaming server and library. The perfect companion to Lidarr for listening to your music collection anywhere."
    stack_group = "media-server"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    <<: *common-keys-apps
    environment:
      - ND_SCANSCHEDULE=1h
      - ND_LOGLEVEL=info
      - ND_BASEURL=""
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/navidrome/data:/data
      - $DATADRIVE/music:/music:ro
    ports:
      - 4533:4533
"""
