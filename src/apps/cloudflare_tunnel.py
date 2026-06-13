from src.apps.base_app import BaseApp

class CloudflareTunnelApp(BaseApp):
    key = "cloudflare-tunnel"
    name = "Cloudflare Tunnel"
    port = 0
    category = "networking"
    description = "Expose your local stack services to the public internet securely without port-forwarding."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  cloudflare-tunnel:
    image: cloudflare/cloudflared:latest
    container_name: cloudflare-tunnel
    <<: *common-keys-apps
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${{CLOUDFLARE_TUNNEL_TOKEN}}
    restart: unless-stopped
"""
