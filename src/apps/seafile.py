from src.apps.base_app import BaseApp

class SeafileApp(BaseApp):
    key = "seafile"
    name = "Seafile"
    port = 8083
    category = "database"
    description = "Ultra-fast, high-performance C-based file synchronization service."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  seafile:
    image: seafileltd/seafile-mc:latest
    container_name: seafile
    <<: *common-keys-apps
    environment:
      - DB_HOST=mariadb
      - DB_ROOT_PASSWD=${{MYSQL_ROOT_PASSWORD}}
      - TIME_ZONE=${{TZ}}
    volumes:
      - {self.get_appdata_dir()}:/shared
    ports:
      - 8083:80
"""
