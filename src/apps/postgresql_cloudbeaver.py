from src.apps.base_app import BaseApp
class PostgresqlCloudbeaverApp(BaseApp):
    key = "postgresql (+cloudbeaver)"
    name = "Postgresql (+Cloudbeaver)"
    port = 5432
    category = "postgres"
    description = "Powerful open-source object-relational database system (High Resource). Includes CloudBeaver for professional management."
    stack_group = "core"
    recommendations = ['authelia']
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  postgresql:
    image: lscr.io/linuxserver/postgresql:latest
    container_name: postgres
    <<: *common-keys-core
    networks:
      - media-internal
    environment:
      - POSTGRES_USER=mediauser
      - POSTGRES_PASSWORD=$DB_PASS
      - POSTGRES_DB=mediadb
    volumes:
      - $DOCKERDIR/appdata/postgres/data:/var/lib/postgresql/data
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mediauser -d mediadb"]
      interval: 10s
      timeout: 5s
      retries: 5
"""
