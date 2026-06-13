from src.apps.base_app import BaseApp

class NetdataApp(BaseApp):
    key = "netdata"
    name = "Netdata"
    port = 19999
    category = "management"
    description = "Real-time system health and resource monitor tracking metrics at per-second intervals."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  netdata:
    image: netdata/netdata:latest
    container_name: netdata
    <<: *common-keys-apps
    cap_add:
      - SYS_PTRACE
    security_opt:
      - apparmor:unconfined
    volumes:
      - {self.get_appdata_dir()}/netdataconfig:/etc/netdata
      - {self.get_appdata_dir()}/netdatalib:/var/lib/netdata
      - {self.get_appdata_dir()}/netdatacache:/var/cache/netdata
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - 19999:19999
"""
