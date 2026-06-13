from src.apps.base_app import BaseApp
class KasmApp(BaseApp):
    key = "kasm"
    name = "Kasm"
    port = 6901
    category = "workspaces"
    description = "Containerized desktop infrastructure providing isolated, secure browser-based workspaces and remote access."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  kasm:
    image: lscr.io/linuxserver/kasm:latest
    container_name: kasm
    <<: *common-keys-core
    privileged: true
    environment:
      KASM_PORT: 6901
      <<: *default-tz-puid-pgid
    volumes:
      - $DOCKERDIR/appdata/kasm/config:/config
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 6901:6901
      - 4430:443
"""
