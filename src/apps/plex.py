from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class PlexConfig(BaseModel):
    PLEX_CLAIM: str = Field(
        default="", 
        description="Plex Claim Token", 
        json_schema_extra={
            "help_url": "https://www.plex.tv/claim",
            "is_secret": True
        }
    )

class PlexApp(BaseApp):
    key = "plex"
    name = "Plex"
    port = 32400
    category = "plex"
    description = "Premium media server that organizes your collections and streams them to any device, featuring rich metadata and remote access."
    stack_group = "media-server"
    recommendations = ['tautulli', 'seerr', 'watchtower', 'plextraktsync']
    is_configurable = False
    has_widget = True
    config_model = PlexConfig

    def get_compose_template(self) -> str:
        return """  plex:
    image: lscr.io/linuxserver/plex:latest
    container_name: plex
    <<: *common-keys-core
    environment:
      - VERSION=docker
      - PLEX_CLAIM=$PLEX_CLAIM
      - TZ=$TZ
      - PUID=$PUID
      - PGID=$PGID
      - NVIDIA_VISIBLE_DEVICES=all
    ports:
      - 32400:32400
      - 1900:1900/udp
      - 3005:3005
      - 8324:8324/tcp
      - 32410:32410/udp
      - 32412:32412/udp
      - 32413:32413/udp
      - 32414:32414/udp
      - 32469:32469
    volumes:
      - $DOCKERDIR/appdata/plex/config:/config
      - $DATADRIVE/tv:/tv
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/anime:/anime
      - $DATADRIVE/music:/music
      - $DATADRIVE/audiobooks:/audiobooks
"""
