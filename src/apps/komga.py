from src.apps.base_app import BaseApp

class KomgaApp(BaseApp):
    key = "komga"
    name = "Komga"
    port = 8088
    category = "tools"
    description = "Dedicated media server for comic books, manga, and CBZ files."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  komga:
    image: gotson/komga:latest
    container_name: komga
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 8088:8080
"""
