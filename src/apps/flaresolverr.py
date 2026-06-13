from src.apps.base_app import BaseApp
class FlaresolverrApp(BaseApp):
    key = "flaresolverr"
    name = "Flaresolverr"
    port = 8191
    category = "none"
    description = "Proxy server to bypass Cloudflare and DDOS-Guard protections on torrent trackers, ensuring your indexers stay online."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = True
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  flaresolverr:
    image: ghcr.io/flaresolverr/flaresolverr:latest
    container_name: flaresolverr
    <<: *common-keys-apps
    environment:
      - LOG_LEVEL=info
      - TZ=$TZ
    ports:
      - ${FLARESOLVERR_PORT:-8191}:8191
"""
