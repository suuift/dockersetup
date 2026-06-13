from src.apps.base_app import BaseApp
class CrowdsecApp(BaseApp):
    key = "crowdsec"
    name = "Crowdsec"
    port = 0
    category = "none"
    description = "Open-source and collaborative security engine that analyzes logs to detect and block malicious IPs from attacking your server."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  crowdsec:
    image: crowdsecurity/crowdsec:latest
    container_name: crowdsec
    <<: *common-keys-core
    environment:
      - GID=$PGID
      - COLLECTIONS=crowdsecurity/nginx-proxy-manager crowdsecurity/base-os crowdsecurity/sshd
    volumes:
      - $DOCKERDIR/appdata/crowdsec/config:/etc/crowdsec
      - $DOCKERDIR/appdata/crowdsec/data:/var/lib/crowdsec
      - $DOCKERDIR/appdata/npm/logs:/var/log/npm:ro
      - /var/log:/var/log:ro
    restart: unless-stopped
"""
