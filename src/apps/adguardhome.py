from src.apps.base_app import BaseApp

class AdguardHomeApp(BaseApp):
    key = "adguardhome"
    name = "AdGuard Home"
    port = 3010
    category = "networking"
    description = "DNS-based network tracker blocker with DNS-over-HTTPS built-in natively."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dns_resolver"

    def get_compose_template(self) -> str:
        return f"""  adguardhome:
    image: adguard/adguardhome:latest
    container_name: adguardhome
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}/workdir:/opt/adguardhome/work
      - {self.get_appdata_dir()}/confdir:/opt/adguardhome/conf
    ports:
      - 3010:3000
      - 53:53/tcp
      - 53:53/udp
"""
