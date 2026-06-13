from src.apps.base_app import BaseApp
class HomepageApp(BaseApp):
    key = "homepage"
    name = "Homepage"
    port = 3000
    category = "dash"
    description = "Highly customizable dashboard that provides a unified landing page and real-time status for all your services."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    <<: *common-keys-apps
    ports:
      - 3000:3000
    volumes:
      - $DOCKERDIR/appdata/homepage/config:/app/config
      - /var/run/docker.sock:/var/run/docker.sock
      - $USERDIR:/c
      - $DATADRIVE:/h
    environment:
      <<: *default-tz-puid-pgid
"""
