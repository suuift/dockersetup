from src.apps.base_app import BaseApp
class MariadbAdminerApp(BaseApp):
    key = "mariadb (+adminer)"
    name = "Mariadb (+Adminer)"
    port = 3306
    category = "db"
    description = "Reliable open-source relational database (Low Resource). Includes Adminer for lightweight web-based management."
    stack_group = "core"
    recommendations = ['authelia']
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  mariadb:
    image: lscr.io/linuxserver/mariadb:latest
    container_name: mariadb
    <<: *common-keys-core
    networks:
      - media-internal
    environment:
      - MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
      - MYSQL_DATABASE=mediadb
      - MYSQL_USER=$MYSQL_USER
      - MYSQL_PASSWORD=$MYSQL_PASSWORD
    volumes:
      - $DOCKERDIR/appdata/mariadb/config:/config
    ports:
      - 3306:3306
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
  adminer:
    image: adminer:latest
    container_name: adminer
    <<: *common-keys-apps
    ports:
      - 8082:8080
"""
