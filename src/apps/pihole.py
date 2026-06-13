from src.apps.base_app import BaseApp

class PiholeApp(BaseApp):
    key = "pihole"
    name = "Pi-hole"
    port = 8081
    category = "networking"
    description = "Network-wide DNS tracker and ad-blocker sinkhole."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dns_resolver"

    def get_compose_template(self) -> str:
        return f"""  pihole:
    image: pihole/pihole:latest
    container_name: pihole
    <<: *common-keys-apps
    environment:
      - TZ=${{TZ}}
      - WEBPASSWORD=${{HTTP_PASSWORD}}
    volumes:
      - {self.get_appdata_dir()}/etc:/etc/pihole
      - {self.get_appdata_dir()}/dnsmasq:/etc/dnsmasq.d
    ports:
      - 53:53/tcp
      - 53:53/udp
      - 8081:80
"""
