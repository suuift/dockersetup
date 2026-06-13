from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class QbittorrentVpnConfig(BaseModel):
    VPN_PROV: str = Field(default="custom", description="VPN Provider (e.g. custom, mullvad, pia)")
    VPN_CLIENT: str = Field(default="wireguard", description="VPN Client (e.g. wireguard, openvpn)")
    VPN_USER: str = Field(default="", description="VPN Username")
    VPN_PASS: str = Field(default="", description="VPN Password", json_schema_extra={"is_secret": True})
    LAN_NETWORK: str = Field(default="192.168.1.0/24", description="Local Network Range (e.g. 192.168.1.0/24)")

class QbittorrentVpnApp(BaseApp):
    key = "qbittorrent-vpn"
    name = "qBittorrent-VPN"
    port = 8081
    category = "torrents-vpn"
    description = "Advanced BitTorrent client bundled with a VPN client and an automatic killswitch to ensure all traffic is encrypted and anonymous."
    stack_group = "downloaders"
    recommendations = []
    is_configurable = False
    has_widget = True
    config_model = QbittorrentVpnConfig

    def get_compose_template(self) -> str:
        return """  qbittorrent-vpn:
    image: binhex/arch-qbittorrentvpn:latest
    container_name: qbit-vpn
    <<: *common-keys-apps
    environment:
      - VPN_ENABLED=yes
      - VPN_PROV=$VPN_PROV
      - VPN_CLIENT=$VPN_CLIENT
      - VPN_USER=$VPN_USER
      - VPN_PASS=$VPN_PASS
      - LAN_NETWORK=$LAN_NETWORK
      - NAME_SERVERS=1.1.1.1,8.8.8.8
      - STRICT_PORT_FORWARD=yes
      - ENABLE_PRIVOXY=yes
      - WEBUI_PORT=8081
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/qbit-vpn/config:/config
      - $DATADRIVE/downloads:/data
    ports:
      - ${QBITTORRENT_VPN_PORT:-8081}:8081
      - 8118:8118
      - 6881:6881
      - 6881:6881/udp
    cap_add:
      - NET_ADMIN
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        from src.utils.state import get_metadata
        import os
        import json
        import requests
        results = []
        if self.key in keys:
            metadata = get_metadata()
            selected = metadata.get("selected_services", [])
            sso_enabled = any(provider in selected for provider in ["authelia", "authentik"])
            tier = os.getenv("DEPLOY_TIER", "1")
            http_user = os.getenv("HTTP_USERNAME", "admin")
            http_pass = os.getenv("HTTP_PASSWORD", "")

            if sso_enabled:
                write_log("Skipping qBittorrent credentials injection (delegated to SSO gateway).", level="DEBUG")
                results.append("qBittorrent configured with default credentials (delegated to SSO gateway)")
            elif tier == "1":
                write_log("Skipping qBittorrent credentials injection for minimal installation.", level="DEBUG")
                results.append("qBittorrent configured with default credentials")
            else:
                qbit_port = int(os.getenv("QBITTORRENT_VPN_PORT", str(self.port)))
                write_step("Injecting Authentication for qBittorrent-VPN...")
                
                creds_to_try = [
                    {"u": http_user, "p": http_pass},
                    {"u": "admin", "p": "adminadmin"}
                ]
                
                login_success = False
                qbit_session = requests.Session()
                
                for cred in creds_to_try:
                    try:
                        payload = {"username": cred["u"], "password": cred["p"]}
                        res = qbit_session.post(
                            f"http://localhost:{qbit_port}/api/v2/auth/login",
                            data=payload,
                            timeout=5,
                            verify=False
                        )
                        if res.text.strip() == "Ok.":
                            login_success = True
                            break
                    except Exception:
                        pass
                
                if login_success:
                    try:
                        prefs = {"web_ui_username": http_user, "web_ui_password": http_pass}
                        qbit_session.post(
                            f"http://localhost:{qbit_port}/api/v2/app/setPreferences",
                            data={"json": json.dumps(prefs)},
                            timeout=5,
                            verify=False
                        )
                        results.append("Secured qBittorrent with management credentials")
                    except Exception as e:
                        write_log(f"Failed to set qBittorrent preferences: {str(e)}", level="WARN")

            pvr_apps = ["sonarr", "radarr", "lidarr"]
            for app in pvr_apps:
                if app in keys:
                    write_log(f"Linking qBittorrent-VPN to {app}...")
                    pvr_port = 7878 if app == "radarr" else (8686 if app == "lidarr" else 8989)
                    api_v = "v1" if app == "lidarr" else "v3"
                    app_url = f"http://localhost:{pvr_port}/api/{api_v}/downloadclient?apikey={keys[app]}"
                    
                    qbit_host = "qbit-vpn"
                    qbit_payload = {
                        "enable": True,
                        "priority": 1,
                        "name": self.name,
                        "implementation": "Qbittorrent",
                        "configContract": "QbittorrentSettings",
                        "fields": [
                            {"name": "host", "value": qbit_host},
                            {"name": "port", "value": 8081},
                            {"name": "username", "value": http_user if not sso_enabled and tier != "1" else "admin"},
                            {"name": "password", "value": http_pass if not sso_enabled and tier != "1" else "adminadmin"},
                            {"name": "movieCategory", "value": "movies"},
                            {"name": "tvCategory", "value": "tv"}
                        ]
                    }
                    try:
                        rest_invoker(app_url, method="POST", json_payload=qbit_payload)
                        results.append(f"Connected {self.name} to {app}")
                    except Exception as e:
                        write_log(f"Failed to connect {self.name} to {app}: {str(e)}", level="WARN")

        return results
