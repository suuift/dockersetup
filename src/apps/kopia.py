from src.apps.base_app import BaseApp
class KopiaApp(BaseApp):
    key = "kopia"
    name = "Kopia"
    port = 28913
    category = "backup"
    description = "Fast and secure open-source backup tool that creates encrypted, deduplicated snapshots of your data."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  kopia:
    image: kopia/kopia:latest
    container_name: kopia
    <<: *common-keys-apps
    environment:
      <<: *default-tz-puid-pgid
      USER_UID: $PUID
      USER_GID: $PGID
    volumes:
      - $DOCKERDIR/appdata/kopia/config:/app/config
      - $DOCKERDIR/appdata/kopia/cache:/app/cache
      - $DOCKERDIR/appdata/kopia/logs:/app/logs
      - $DOCKERDIR/appdata:/source/appdata:ro
      - $DATADRIVE:/source/media:ro
    ports:
      - 51515:51515
    command: >
      server start
      --address 0.0.0.0:51515
      --server-username=$HTTP_USERNAME
      --server-password=$KOPIA_PASSWORD
      --config-file=/app/config/repository.config
      --log-dir=/app/logs
      --cache-directory=/app/cache
"""
