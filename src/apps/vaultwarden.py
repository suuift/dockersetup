from src.apps.base_app import BaseApp
class VaultwardenApp(BaseApp):
    key = "vaultwarden"
    name = "Vaultwarden"
    port = 8083
    category = "none"
    description = "Lightweight self-hosted password manager (Bitwarden compatible). Provides professional-grade security for your family's passwords."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    <<: *common-keys-apps
    environment:
      - SIGNUPS_ALLOWED=false
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/vaultwarden/data:/data
    ports:
      - 8083:80
"""
