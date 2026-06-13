from src.apps.base_app import BaseApp

class UptimeKumaApp(BaseApp):
    key = "uptime-kuma"
    name = "Uptime Kuma"
    port = 3001
    category = "management"
    description = "Beautiful monitoring tool to check the status of your stack and send alert notifications."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 3001:3001
"""
