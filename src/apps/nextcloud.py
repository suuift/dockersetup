from src.apps.base_app import BaseApp

class NextcloudApp(BaseApp):
    key = "nextcloud"
    name = "Nextcloud"
    port = 8082
    category = "database"
    description = "Self-hosted alternative to Google Drive for managing calendars, files, and contacts."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    required_database_type = "postgres"

    def get_compose_template(self) -> str:
        return f"""  nextcloud:
    image: nextcloud:latest
    container_name: nextcloud
    <<: *common-keys-apps
    environment:
      - POSTGRES_HOST=postgresql
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${{DB_PASS}}
      - POSTGRES_DB=nextcloud
    volumes:
      - {self.get_appdata_dir()}:/var/var/html
    ports:
      - 8082:80
"""
