from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class TailscaleConfig(BaseModel):
    TS_AUTHKEY: str = Field(
        default="", 
        description="Tailscale Auth Key",
        json_schema_extra={
            "help_url": "https://login.tailscale.com/admin/settings/keys",
            "is_secret": True
        }
    )

class TailscaleApp(BaseApp):
    key = "tailscale"
    name = "Tailscale"
    port = 0
    category = "vpn"
    description = "Zero-config VPN that creates a secure mesh network between your devices, allowing remote access without port forwarding."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = TailscaleConfig

    def get_compose_template(self) -> str:
        return """  tailscale:
    image: tailscale/tailscale:latest
    container_name: tailscale
    <<: *common-keys-core
    environment:
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_AUTHKEY=$TS_AUTHKEY
      - TS_EXTRA_ARGS=--accept-dns=true
    volumes:
      - $DOCKERDIR/appdata/tailscale:/var/lib/tailscale
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
"""
