from src.apps.base_app import BaseApp

class FireflyIiiApp(BaseApp):
    key = "firefly-iii"
    name = "Firefly III"
    port = 8089
    category = "tools"
    description = "Self-hosted personal finance dashboard, double-entry bookkeeper, and budget manager."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  firefly-iii:
    image: fireflyiii/core:latest
    container_name: firefly-iii
    <<: *common-keys-apps
    environment:
      - APP_KEY=SomeSecretRandomKeyOf32CharsVal
      - DB_CONNECTION=sqlite
    volumes:
      - {self.get_appdata_dir()}:/var/www/html/storage
    ports:
      - 8089:8080
"""
