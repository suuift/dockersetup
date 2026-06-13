from src.apps.base_app import BaseApp
class ImmichApp(BaseApp):
    key = "immich"
    name = "Immich"
    port = 2283
    category = "photos"
    description = "High-performance self-hosted solution for backing up and managing your personal photo and video collections."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  immich:
    image: ghcr.io/immich-app/immich-server:release
    container_name: immich
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/immich/data:/config
      - $DATADRIVE/photos:/photos
    ports:
      - 2283:3001
"""
