from src.apps.base_app import BaseApp
class SyncthingApp(BaseApp):
    key = "syncthing"
    name = "Syncthing"
    port = 8384
    category = "sync"
    description = "Secure and private file synchronization program that syncs data between your devices in real time."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  syncthing:
    image: lscr.io/linuxserver/syncthing:latest
    container_name: syncthing
    <<: *common-keys-apps
    environment:
      <<: *default-tz-puid-pgid
    volumes:
      - $DOCKERDIR/appdata/syncthing/config:/config
      - $DATADRIVE/music:/data
    ports:
      - 8384:8384
      - 22000:22000/tcp
      - 22000:22000/udp
      - 21027:21027/udp
"""
