from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class CloudflareDdnsConfig(BaseModel):
    CF_API_TOKEN: str = Field(default="", description="Cloudflare API Token", json_schema_extra={"is_secret": True})
    CF_ZONE_ID: str = Field(default="", description="Cloudflare Zone ID")
    CF_DOMAINS: str = Field(default="", description="Cloudflare Domains (comma-separated)")
    BASE_DOMAIN: str = Field(default="local.host", description="Base Domain (e.g. example.com)")

class CloudflareDdnsApp(BaseApp):
    key = "cloudflare-ddns"
    name = "Cloudflare DDNS"
    port = 0
    category = "none"
    description = "Automatically updates Cloudflare DNS records with your current public IP address to ensure your domain always points to your home network."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = CloudflareDdnsConfig

    def get_compose_template(self) -> str:
        return """  cloudflare-ddns:
    image: favonia/cloudflare-ddns:latest
    container_name: cloudflare-ddns
    <<: *common-keys-core
    environment:
      - CF_API_TOKEN=$CF_API_TOKEN
      - DOMAINS=$CF_DOMAINS
      - PROXIED=true
      - UPDATE_CRON=@every 30m
"""
