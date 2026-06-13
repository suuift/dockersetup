from src.apps.base_app import BaseApp
class UptimeApp(BaseApp):
    key = "uptime"
    name = "Uptime"
    port = 3001
    category = "status"
    description = "Self-hosted monitoring tool that watches your services for downtime and provides a modern status dashboard with notifications."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  uptime:
    image: louislam/uptime-kuma:1
    container_name: uptime
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/uptime/data:/app/data
    ports:
      - 3001:3001
"""
