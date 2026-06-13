from src.apps.base_app import BaseApp
class HkserverApp(BaseApp):
    key = "hkserver"
    name = "Hkserver"
    port = 3838
    category = "none"
    description = "Dedicated server for Hollow Knight Multiplayer, allowing for cooperative play in a shared world."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  hkserver:
    image: hollowknight/hkmp:latest
    container_name: hkserver
    <<: *common-keys-apps
    ports:
      - 7777:7777/udp
"""
