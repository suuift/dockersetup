from src.apps.base_app import BaseApp
class PaperlessApp(BaseApp):
    key = "paperless"
    name = "Paperless"
    port = 8010
    category = "docs"
    description = "Document management system that handles OCR and indexing to transform physical documents into a searchable online archive."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperless
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/paperless/data:/data
      - $DATADRIVE/documents:/documents
    ports:
      - 8010:8000
"""
