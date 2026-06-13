from src.apps.base_app import BaseApp
class ScrutinyApp(BaseApp):
    key = "scrutiny"
    name = "Scrutiny"
    port = 8086
    category = "status"
    description = "Hard drive S.M.A.R.T. monitoring dashboard that tracks disk health and alerts you to potential failures before they happen."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  scrutiny:
    image: ghcr.io/analogj/scrutiny:latest-omnibus
    container_name: scrutiny
    <<: *common-keys-apps
    cap_add:
      - SYS_RAWIO
      - SYS_ADMIN
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - /run/udev:/run/udev:ro
      - $DOCKERDIR/appdata/scrutiny/config:/opt/scrutiny/config
      - $DOCKERDIR/appdata/scrutiny/influxdb:/opt/scrutiny/influxdb
    ports:
      - 8086:8080
"""
