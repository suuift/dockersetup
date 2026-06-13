from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class NpmPlusConfig(BaseModel):
    BASE_DOMAIN: str = Field(default="local.host", description="Base Domain (e.g. example.com)")

class NpmPlusGoaccessApp(BaseApp):
    key = "npm plus (+goaccess)"
    name = "Nginx Proxy Manager Plus"
    port = 81
    category = "proxy"
    description = "Enhanced Nginx Proxy Manager with built-in security features and GoAccess for real-time traffic analysis."
    stack_group = "core"
    recommendations = ['cloudflare-ddns', 'authelia', 'crowdsec']
    is_configurable = False
    has_widget = False
    config_model = NpmPlusConfig

    def get_compose_template(self) -> str:
        return """  npm-plus:
    <<: *common-keys-core
    container_name: nginx-proxy-manager-plus
    image: 'zoeyvid/nginx-proxy-manager-plus:latest'
    networks:
      npm_proxy:
        ipv4_address: 192.168.89.254
    ports:
      - '80:80'
      - '443:443'
      - '81:81'
    volumes:
      - $DOCKERDIR/appdata/npm/config:/config 
      - $DOCKERDIR/appdata/npm/letsencrypt:/etc/letsencrypt
      - $DOCKERDIR/appdata/npm/data:/data
    environment:
      - DISABLE_IPV6=true
      - CROWDSEC_ENABLED=$CROWDSEC_ENABLED
      - CROWDSEC_LAPI_URL=http://crowdsec:8080
      - CROWDSEC_LAPI_KEY=$CROWDSEC_API_KEY
  goaccess:
    <<: *common-keys-apps
    image: xavierh/goaccess-for-nginxproxymanager:latest
    container_name: goaccess
    ports:
      - 7880:7880
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/npm/logs:/opt/log
      - $DOCKERDIR/appdata/goaccess/config:/config
"""
