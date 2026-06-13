from src.apps.base_app import BaseApp

class SftpgoApp(BaseApp):
    key = "sftpgo"
    name = "SFTPGo"
    port = 8092
    category = "tools"
    description = "Configure secure SFTP, WebDAV, and FTP transfers with a clean administrative dashboard."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  sftpgo:
    image: drakkan/sftpgo:latest
    container_name: sftpgo
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}/data:/srv/sftpgo
      - {self.get_appdata_dir()}/config:/var/lib/sftpgo
    ports:
      - 8092:8080
      - 2022:2022
"""
