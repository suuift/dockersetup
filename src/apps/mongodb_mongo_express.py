from src.apps.base_app import BaseApp
class MongodbMongoExpressApp(BaseApp):
    key = "mongodb (+mongo-express)"
    name = "Mongodb (+Mongo-Express)"
    port = 27017
    category = "mongo"
    description = "High-performance NoSQL document database. Includes Mongo-Express for an easy-to-use web interface."
    stack_group = "core"
    recommendations = ['authelia']
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  mongodb:
    image: mongo:latest
    container_name: mongodb
    <<: *common-keys-core
    networks:
      - media-internal
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASS
    volumes:
      - $DOCKERDIR/appdata/mongodb/data:/data/db
    ports:
      - 27017:27017
"""
