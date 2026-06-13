from src.apps.base_app import BaseApp

class CalibreWebApp(BaseApp):
    key = "calibre-web"
    name = "Calibre-Web"
    port = 8084
    category = "tools"
    description = "Clean web UI interface to browse, read, and search ebook collections."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  calibre-web:
    image: linuxserver/calibre-web:latest
    container_name: calibre-web
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 8084:8083
"""
