from src.apps.base_app import BaseApp

class StirlingPdfApp(BaseApp):
    key = "stirling-pdf"
    name = "Stirling PDF"
    port = 8085
    category = "tools"
    description = "Local web-based PDF manipulation platform for merging, splitting, OCR, and editing."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  stirling-pdf:
    image: frooodle/s-pdf:latest
    container_name: stirling-pdf
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/usr/share/tessdata
    ports:
      - 8085:8080
"""
