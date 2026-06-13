from src.apps.base_app import BaseApp
class SlskdApp(BaseApp):
    key = "slskd"
    name = "Slskd"
    port = 5030
    category = "slskd"
    description = "Modern, headless Soulseek client designed for servers, featuring a clean web interface for music sharing and discovery."
    stack_group = "downloaders"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  slskd:
    image: slskd/slskd:latest
    container_name: slskd
    <<: *common-keys-apps
    environment:
      - SLSKD_PUID=$PUID
      - SLSKD_PGID=$PGID
      - SLSKD_TZ=$TZ
      - SLSKD_SLSK_LISTEN_PORT=50300
    volumes:
      - $DOCKERDIR/appdata/slskd/config:/app/config
      - $DATADRIVE/music:/app/music
      - $DATADRIVE/downloads/slskd:/app/downloads
    ports:
      - 50300:50300
      - 5030:5030
"""
