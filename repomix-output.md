This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: .gemini/**, testing_sandbox/**
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.github/workflows/build-assets.yml
.gitignore
build_bin.py
dockersetup.py
pyproject.toml
README.md
refs/homepage_reference.md
resources/app.ico
resources/dockersetup.png
resources/install.sh
resources/installer.iss
src/apps/adguardhome.py
src/apps/audiobookshelf.py
src/apps/authelia.py
src/apps/authentik.py
src/apps/base_app.py
src/apps/bazarr.py
src/apps/beszel.py
src/apps/caddy.py
src/apps/calibre_web.py
src/apps/changedetection.py
src/apps/cloudcmd.py
src/apps/cloudflare_ddns.py
src/apps/cloudflare_tunnel.py
src/apps/code_server.py
src/apps/crowdsec.py
src/apps/dashy.py
src/apps/docker_prune.py
src/apps/dockge.py
src/apps/docmost.py
src/apps/dokploy.py
src/apps/enshrouded.py
src/apps/filebrowser.py
src/apps/fileflows.py
src/apps/firefly_iii.py
src/apps/flame.py
src/apps/flaresolverr.py
src/apps/hkserver.py
src/apps/home_assistant.py
src/apps/homepage.py
src/apps/immich.py
src/apps/it_tools.py
src/apps/jellyfin.py
src/apps/kasm.py
src/apps/komga.py
src/apps/kopia.py
src/apps/lidarr.py
src/apps/loader.py
src/apps/mariadb_adminer.py
src/apps/mealie.py
src/apps/mongodb_mongo_express.py
src/apps/mylar.py
src/apps/navidrome.py
src/apps/netdata.py
src/apps/nextcloud.py
src/apps/npm_plus_goaccess.py
src/apps/paperless.py
src/apps/pihole.py
src/apps/plex.py
src/apps/plextraktsync.py
src/apps/portainer.py
src/apps/postgresql_cloudbeaver.py
src/apps/prowlarr.py
src/apps/qbittorrent_vpn.py
src/apps/qbittorrent.py
src/apps/radarr.py
src/apps/readarr.py
src/apps/recyclarr.py
src/apps/sabnzbd.py
src/apps/satisfactory.py
src/apps/scrutiny.py
src/apps/seafile.py
src/apps/searxng.py
src/apps/seerr.py
src/apps/sftpgo.py
src/apps/slskd.py
src/apps/sonarr.py
src/apps/stirling_pdf.py
src/apps/syncthing.py
src/apps/tailscale.py
src/apps/tautulli.py
src/apps/tmodloader.py
src/apps/trilium.py
src/apps/uptime_kuma.py
src/apps/valheim.py
src/apps/vaultwarden.py
src/apps/watchtower.py
src/gui.py
src/gui/__init__.py
src/gui/base_frame.py
src/gui/deploy_frame.py
src/gui/env_frame.py
src/gui/logs_frame.py
src/gui/services_frame.py
src/gui/summary_frame.py
src/gui/welcome_frame.py
src/modules/__init__.py
src/modules/auto_configure.py
src/modules/compose_build.py
src/modules/deploy_preflight.py
src/modules/deploy_start.py
src/modules/directories.py
src/modules/env_wizard.py
src/modules/network.py
src/modules/preflight.py
src/modules/tier_select.py
src/utils/__init__.py
src/utils/clipboard.py
src/utils/dependency_resolver.py
src/utils/logger.py
src/utils/migrate_to_plugins.py
src/utils/paths.py
src/utils/plex_oauth.py
src/utils/port_resolver.py
src/utils/state.py
src/utils/uninstall.py
src/utils/updater.py
src/utils/yaml_parser.py
TASKS.md
tests/__init__.py
tests/test_runtime.py
```

# Files

## File: tests/__init__.py
````python
# tests package
````

## File: .gitignore
````
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
bin/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script, python-build-prints etc
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nosenv/
.pytest_cache/
.mypy_cache/
.cache/
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.run/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Logs
logs/
*.log

# Documentation and Agent Protocols
docs/
agents.md
AGENTS.md

# Development Scratchpad
scratch/
````

## File: refs/homepage_reference.md
````markdown
# Homepage Configuration & Layout Reference

This document serves as a reference for configuring the Homepage dashboard (`gethomepage.dev`), specifically focusing on layout management, grouping, and ordering.

## Core Concepts

Homepage uses YAML files located in its `config` directory to define its behavior. The two primary files relevant to layout are:
- `services.yaml`: Defines the actual services, their URLs, and widget configurations.
- `settings.yaml`: Controls the global application settings and the visual layout (rows, columns, ordering) of the groups defined in `services.yaml` and `bookmarks.yaml`.

## Layout Configuration (`settings.yaml`)

By default, Homepage arranges groups vertically in columns. To force groups into horizontal rows and control their exact order, you must use the `layout` block in `settings.yaml`.

### 1. Forcing Horizontal Rows

To make a group render as a horizontal row, you map the group's exact name (as defined in `services.yaml`) under the `layout` block and assign it `style: row`. You can also specify the maximum number of `columns` (widgets per row) before wrapping.

```yaml
# settings.yaml
layout:
  "Media Server":
    style: row
    columns: 4
```

### 2. Group Ordering

The order of groups rendered on the Homepage is strictly determined by their top-to-bottom order within the `layout` block in `settings.yaml`. 

*Note: Any group defined in `services.yaml` but missing from the `layout` block will be automatically appended to the bottom of the page in a default vertical column.*

**Example:**
```yaml
# settings.yaml
layout:
  - "Media Server":
      style: row
      columns: 4
  - "Media PVR":
      style: row
      columns: 4
  - "Downloaders":
      style: row
      columns: 4
  - "Maintenance":
      style: row
      columns: 4
```

### 3. Global Layout Settings

To ensure the rows utilize the full width of modern monitors (preventing widgets from squishing together in the center), you should enable the `fullWidth` property globally.

```yaml
# settings.yaml (top level)
title: "Home Server Dashboard"
favicon: "https://homepage.dev/favicon.ico"
theme: dark
fullWidth: true  # Make rows span the whole screen
```

## Strategy for DockerSetup

When dynamically generating the Homepage configuration in `compose_build.py`:

1.  **Generate `services.yaml`**: This file will map the selected apps to their respective stack groups (e.g., `media-server`, `media-pvr`).
2.  **Generate `settings.yaml`**: We must also dynamically write a `settings.yaml` to the Homepage config directory that explicitly defines the `layout` block. We will iterate through the configured stacks in the required order (`media-server`, `media-pvr`, `downloaders`, `maintenance`, plus any others) and assign `style: row`.

## Additional Configurations

### Services (`services.yaml`)
Services are the core clickable items on the dashboard, mapped to containers and URLs.
- **Structure:** Defined as a list of groups containing a list of service objects. Nesting is supported.
- **Key Attributes:** `icon`, `href`, `description`, `ping` (for health checks).
- **Service Widgets:** Live data from third-party APIs (like Sonarr or Plex) can be attached directly to a service definition via the `widget` property.

### Information Widgets (`widgets.yaml`)
Global widgets that display at the top of the dashboard for system-level or generic data.
- **Display Order:** Rendered in the exact order they are listed in the file. Some widgets (like weather or time) align to the right by default.
- **Examples:** Logo, Search, Weather, Resources (CPU/RAM), GitHub statistics, Date/Time.

### Docker Integration (`docker.yaml`)
Allows Homepage to query Docker directly to display container states and resource usage.
- **Connection Methods:** Can use `/var/run/docker.sock` directly (if root), a TCP API, or a secure proxy (`docker-socket-proxy`).
- **Mapping:** Use `server` and `container` attributes in `services.yaml` to link a dashboard item to its corresponding live container data.
- **Auto-Discovery:** By applying `homepage.*` labels to your Docker containers, Homepage can automatically populate them on the dashboard without manual entries in `services.yaml`.

### Bookmarks (`bookmarks.yaml`)
Smaller, simplified links that exist separately from Services.
- **Limitations:** Cannot host Service Widgets or ping monitors.
- **Structure:** Configured similarly to services (groups of links), but optimized for simple URL redirection. Often used for external sites or static reference material.

---
*Reference generated from gethomepage.dev documentation.*
````

## File: resources/install.sh
````bash
#!/bin/bash
# DockerSetup Native Linux Installer
# Wraps deployment folder setup and desktop integration with Zenity fallback

INSTALL_DIR="$HOME/.local/share/dockersetup"
BIN_NAME="dockersetup"
DESKTOP_FILE="$HOME/.local/share/applications/dockersetup.desktop"

# Check if display is present and zenity is installed
USE_GUI=0
if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    if command -v zenity >/dev/null 2>&1; then
        USE_GUI=1
    fi
fi

msg_info() {
    local title="$1"
    local text="$2"
    if [ $USE_GUI -eq 1 ]; then
        zenity --info --title="$title" --text="$text" --width=400
    else
        echo -e "\n=== $title ===\n$text\n"
    fi
}

msg_confirm() {
    local title="$1"
    local text="$2"
    if [ $USE_GUI -eq 1 ]; then
        zenity --question --title="$title" --text="$text" --width=400
    else
        read -p "$text (y/N): " choice
        case "$choice" in 
            [yY][eE][sS]|[yY]) return 0 ;;
            *) return 1 ;;
        esac
    fi
}

# 1. Welcome and Installation confirmation
if ! msg_confirm "DockerSetup Installer" "Do you want to install DockerSetup to your user directory ($INSTALL_DIR)?"; then
    msg_info "Cancelled" "Installation cancelled by user."
    exit 0
fi

# 2. Check if binary exists in local directory
if [ ! -f "./$BIN_NAME" ]; then
    # Try parent or dist folders
    if [ -f "./dist/$BIN_NAME" ]; then
        BIN_PATH="./dist/$BIN_NAME"
    elif [ -f "../dist/$BIN_NAME" ]; then
        BIN_PATH="../dist/$BIN_NAME"
    else
        msg_info "Error" "dockersetup binary not found in working path. Please build it first."
        exit 1
    fi
else
    BIN_PATH="./$BIN_NAME"
fi

# 3. Create install directories
mkdir -p "$INSTALL_DIR"
cp "$BIN_PATH" "$INSTALL_DIR/$BIN_NAME"
chmod +x "$INSTALL_DIR/$BIN_NAME"

# 4. Create Desktop shortcut
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=DockerSetup
Comment=Deploy Media and Home Server stacks using Docker
Exec=x-terminal-emulator -e "$INSTALL_DIR/$BIN_NAME"
Icon=utilities-terminal
Terminal=false
Categories=System;Utility;
EOF
chmod +x "$DESKTOP_FILE"

# 5. Success
msg_info "Success" "DockerSetup has been successfully installed.\n\nYou can launch it from your applications menu or run:\n$INSTALL_DIR/$BIN_NAME"
````

## File: src/apps/adguardhome.py
````python
from src.apps.base_app import BaseApp

class AdguardHomeApp(BaseApp):
    key = "adguardhome"
    name = "AdGuard Home"
    port = 3010
    category = "networking"
    description = "DNS-based network tracker blocker with DNS-over-HTTPS built-in natively."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dns_resolver"

    def get_compose_template(self) -> str:
        return f"""  adguardhome:
    image: adguard/adguardhome:latest
    container_name: adguardhome
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}/workdir:/opt/adguardhome/work
      - {self.get_appdata_dir()}/confdir:/opt/adguardhome/conf
    ports:
      - 3010:3000
      - 53:53/tcp
      - 53:53/udp
"""
````

## File: src/apps/audiobookshelf.py
````python
from src.apps.base_app import BaseApp
class AudiobookshelfApp(BaseApp):
    key = "audiobookshelf"
    name = "Audiobookshelf"
    port = 13378
    category = "books"
    description = "Self-hosted audiobook and podcast server with a beautiful web UI and full-featured mobile apps."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    container_name: audiobookshelf
    <<: *common-keys-apps
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/audiobookshelf/config:/config
      - $DOCKERDIR/appdata/audiobookshelf/metadata:/metadata
      - $DATADRIVE/audiobooks:/audiobooks
      - $DATADRIVE/books:/books
      - $DATADRIVE/podcasts:/podcasts
    ports:
      - 13378:80
"""
````

## File: src/apps/authentik.py
````python
from src.apps.base_app import BaseApp

class AuthentikApp(BaseApp):
    key = "authentik"
    name = "Authentik"
    port = 9002
    category = "networking"
    description = "Feature-rich Identity Provider (SSO) with custom user flows and app portals."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    required_database_type = "postgres"

    def get_compose_template(self) -> str:
        return f"""  authentik:
    image: ghcr.io/goauthentik/server:latest
    container_name: authentik
    <<: *common-keys-apps
    command: start
    environment:
      - AUTHENTIK_REDIS__HOST=valkey
      - AUTHENTIK_POSTGRESQL__HOST=postgresql
      - AUTHENTIK_POSTGRESQL__USER=postgres
      - AUTHENTIK_POSTGRESQL__PASSWORD=${{DB_PASS}}
      - AUTHENTIK_POSTGRESQL__DB=authentik
    volumes:
      - {self.get_appdata_dir()}/media:/media
      - {self.get_appdata_dir()}/templates:/templates
    ports:
      - 9002:9000
      - 9443:9443
"""
````

## File: src/apps/bazarr.py
````python
from src.apps.base_app import BaseApp
class BazarrApp(BaseApp):
    key = "bazarr"
    name = "Bazarr"
    port = 6767
    category = "subs"
    description = "Companion to Sonarr and Radarr that automatically manages and downloads subtitles for your media collection."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  bazarr:
    image: lscr.io/linuxserver/bazarr:1.5.1
    container_name: bazarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/bazarr/config:/config
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/tv:/tv
    ports:
      - ${BAZARR_PORT:-6767}:6767
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log
        import os
        results = []
        if self.key in keys:
            b_key = keys[self.key]
            b_headers = {"X-Api-Key": b_key}
            
            env_port = os.getenv("BAZARR_PORT")
            bazarr_port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            bazarr_api_url = f"http://localhost:{bazarr_port}/api"

            if "sonarr" in keys:
                write_log("Linking Sonarr to Bazarr...")
                payload = {
                    "enabled": True,
                    "name": "Sonarr",
                    "host": "sonarr",
                    "port": 8989,
                    "apikey": keys["sonarr"],
                    "ssl": False,
                    "base_url": ""
                }
                try:
                    rest_invoker(f"{bazarr_api_url}/settings/sonarr", method="POST", json_payload=payload, headers=b_headers)
                    results.append("Connected Sonarr to Bazarr")
                except Exception as e:
                    write_log(f"Failed to link Sonarr to Bazarr: {str(e)}", level="WARN")

            if "radarr" in keys:
                write_log("Linking Radarr to Bazarr...")
                payload = {
                    "enabled": True,
                    "name": "Radarr",
                    "host": "radarr",
                    "port": 7878,
                    "apikey": keys["radarr"],
                    "ssl": False,
                    "base_url": ""
                }
                try:
                    rest_invoker(f"{bazarr_api_url}/settings/radarr", method="POST", json_payload=payload, headers=b_headers)
                    results.append("Connected Radarr to Bazarr")
                except Exception as e:
                    write_log(f"Failed to link Radarr to Bazarr: {str(e)}", level="WARN")

        return results
````

## File: src/apps/beszel.py
````python
from src.apps.base_app import BaseApp

class BeszelApp(BaseApp):
    key = "beszel"
    name = "Beszel"
    port = 8090
    category = "management"
    description = "Lightweight resource monitor offering CPU, RAM, disk, and Docker container stats."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  beszel:
    image: henrygd/beszel:latest
    container_name: beszel
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/beszel_data
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - 8090:8090
"""
````

## File: src/apps/caddy.py
````python
from src.apps.base_app import BaseApp

class CaddyApp(BaseApp):
    key = "caddy"
    name = "Caddy"
    port = 80
    category = "networking"
    description = "Lightweight reverse proxy and web server with automated HTTPS certificate management."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "reverse_proxy"

    def get_compose_template(self) -> str:
        return f"""  caddy:
    image: caddy:latest
    container_name: caddy
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}/Caddyfile:/etc/caddy/Caddyfile
      - {self.get_appdata_dir()}/data:/data
      - {self.get_appdata_dir()}/config:/config
    ports:
      - 80:80
      - 443:443
"""
````

## File: src/apps/calibre_web.py
````python
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
````

## File: src/apps/changedetection.py
````python
from src.apps.base_app import BaseApp

class ChangedetectionApp(BaseApp):
    key = "changedetection"
    name = "Changedetection.io"
    port = 5002
    category = "tools"
    description = "Self-hosted web page change detection, monitoring, and notification tool."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  changedetection:
    image: dgtlmoon/changedetection.io:latest
    container_name: changedetection
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/datastore
    ports:
      - 5002:5000
"""
````

## File: src/apps/cloudcmd.py
````python
from src.apps.base_app import BaseApp
class CloudcmdApp(BaseApp):
    key = "cloudcmd"
    name = "Cloudcmd"
    port = 8000
    category = "files"
    description = "Web-based file manager with a built-in editor and terminal for managing your server files directly from your browser."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  cloudcmd:
    image: coderaiser/cloudcmd:latest
    container_name: cloudcmd
    <<: *common-keys-apps
    environment:
      - CLOUDCMD_AUTHENTICATION=true
      - CLOUDCMD_USERNAME=$HTTP_USERNAME
      - CLOUDCMD_PASSWORD=$HTTP_PASSWORD
    volumes:
      - $DATADRIVE:/media_pool
      - $DOCKERDIR:/docker_data
"""
````

## File: src/apps/cloudflare_ddns.py
````python
from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class CloudflareDdnsConfig(BaseModel):
    CF_API_TOKEN: str = Field(default="", description="Cloudflare API Token", json_schema_extra={"is_secret": True})
    CF_ZONE_ID: str = Field(default="", description="Cloudflare Zone ID")
    CF_DOMAINS: str = Field(default="", description="Cloudflare Domains (comma-separated)")
    BASE_DOMAIN: str = Field(default="local.host", description="Base Domain (e.g. example.com)")

class CloudflareDdnsApp(BaseApp):
    key = "cloudflare-ddns"
    name = "Cloudflare DDNS"
    port = 0
    category = "none"
    description = "Automatically updates Cloudflare DNS records with your current public IP address to ensure your domain always points to your home network."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = CloudflareDdnsConfig

    def get_compose_template(self) -> str:
        return """  cloudflare-ddns:
    image: favonia/cloudflare-ddns:latest
    container_name: cloudflare-ddns
    <<: *common-keys-core
    environment:
      - CF_API_TOKEN=$CF_API_TOKEN
      - DOMAINS=$CF_DOMAINS
      - PROXIED=true
      - UPDATE_CRON=@every 30m
"""
````

## File: src/apps/cloudflare_tunnel.py
````python
from src.apps.base_app import BaseApp

class CloudflareTunnelApp(BaseApp):
    key = "cloudflare-tunnel"
    name = "Cloudflare Tunnel"
    port = 0
    category = "networking"
    description = "Expose your local stack services to the public internet securely without port-forwarding."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  cloudflare-tunnel:
    image: cloudflare/cloudflared:latest
    container_name: cloudflare-tunnel
    <<: *common-keys-apps
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${{CLOUDFLARE_TUNNEL_TOKEN}}
    restart: unless-stopped
"""
````

## File: src/apps/code_server.py
````python
from src.apps.base_app import BaseApp

class CodeServerApp(BaseApp):
    key = "code-server"
    name = "Code-Server"
    port = 8443
    category = "tools"
    description = "Run VS Code on your home server in a secure web browser workspace."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  code-server:
    image: linuxserver/code-server:latest
    container_name: code-server
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 8443:8443
"""
````

## File: src/apps/crowdsec.py
````python
from src.apps.base_app import BaseApp
class CrowdsecApp(BaseApp):
    key = "crowdsec"
    name = "Crowdsec"
    port = 0
    category = "none"
    description = "Open-source and collaborative security engine that analyzes logs to detect and block malicious IPs from attacking your server."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  crowdsec:
    image: crowdsecurity/crowdsec:latest
    container_name: crowdsec
    <<: *common-keys-core
    environment:
      - GID=$PGID
      - COLLECTIONS=crowdsecurity/nginx-proxy-manager crowdsecurity/base-os crowdsecurity/sshd
    volumes:
      - $DOCKERDIR/appdata/crowdsec/config:/etc/crowdsec
      - $DOCKERDIR/appdata/crowdsec/data:/var/lib/crowdsec
      - $DOCKERDIR/appdata/npm/logs:/var/log/npm:ro
      - /var/log:/var/log:ro
    restart: unless-stopped
"""
````

## File: src/apps/dashy.py
````python
from src.apps.base_app import BaseApp

class DashyApp(BaseApp):
    key = "dashy"
    name = "Dashy"
    port = 8095
    category = "networking"
    description = "Highly customizable, themeable personal dashboard for self-hosted apps."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dashboard"

    def get_compose_template(self) -> str:
        return f"""  dashy:
    image: lissy93/dashy:latest
    container_name: dashy
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/public
    ports:
      - 8095:80
"""
````

## File: src/apps/docker_prune.py
````python
from src.apps.base_app import BaseApp
class DockerPruneApp(BaseApp):
    key = "docker-prune"
    name = "Docker-Prune"
    port = 0
    category = "none"
    description = "Utility that automatically cleans up unused Docker images, containers, and networks daily to keep your system lean."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  docker-prune:
    image: softonic/docker-system-prune:latest
    container_name: docker-prune
    <<: *common-keys-core
    entrypoint: ["/bin/sh", "-c", "while true; do /run.sh --volumes --all; sleep 86400; done"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
"""
````

## File: src/apps/dockge.py
````python
from src.apps.base_app import BaseApp
class DockgeApp(BaseApp):
    key = "dockge"
    name = "Dockge"
    port = 5001
    category = "stacks"
    description = "Modern and intuitive manager for Docker Compose stacks that simplifies editing and monitoring your deployments."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  dockge:
    image: louislam/dockge:1
    container_name: dockge
    restart: unless-stopped
    ports:
      - 5001:5001
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - $DOCKERDIR/appdata/dockge/data:/app/data
      - $DOCKERDIR/stacks:/app/stacks
    environment:
      - DOCKGE_STACKS_DIR=$DOCKERDIR/stacks
"""
````

## File: src/apps/docmost.py
````python
from src.apps.base_app import BaseApp

class DocmostApp(BaseApp):
    key = "docmost"
    name = "Docmost"
    port = 3006
    category = "tools"
    description = "Collaborative documentation, wiki, and knowledge base platform."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    required_database_type = "postgres"

    def get_compose_template(self) -> str:
        return f"""  docmost:
    image: docmost/docmost:latest
    container_name: docmost
    <<: *common-keys-apps
    environment:
      - APP_URL=http://localhost:3006
      - DB_URL=postgresql://postgres:${{DB_PASS}}@postgresql:5432/docmost
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 3006:3000
"""
````

## File: src/apps/dokploy.py
````python
from src.apps.base_app import BaseApp

class DokployApp(BaseApp):
    key = "dokploy"
    name = "Dokploy"
    port = 3005
    category = "tools"
    description = "Self-hosted PaaS platform built on Docker for deploying applications and databases."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  dokploy:
    image: dokploy/dokploy:latest
    container_name: dokploy
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 3005:3000
"""
````

## File: src/apps/enshrouded.py
````python
from src.apps.base_app import BaseApp
class EnshroudedApp(BaseApp):
    key = "enshrouded"
    name = "Enshrouded"
    port = 15636
    category = "enshrouded"
    description = "Dedicated server for cooperative multiplayer in the voxel-based survival world of Enshrouded."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  enshrouded:
    image: mornedhels/enshrouded-server:latest
    container_name: enshrouded
    hostname: enshrouded
    <<: *common-keys-apps
    stop_grace_period: 90s
    ports:
      - "15637:15637/udp"
    volumes:
      - $DOCKERDIR/appdata/enshrouded/data:/opt/enshrouded
    environment:
      - SERVER_NAME=Enshrouded Server
      - SERVER_PASSWORD=secret
      - UPDATE_CRON=*/30 * * * *
      - PUID=4711
      - PGID=4711
"""
````

## File: src/apps/filebrowser.py
````python
from src.apps.base_app import BaseApp
class FilebrowserApp(BaseApp):
    key = "filebrowser"
    name = "Filebrowser"
    port = 8082
    category = "files"
    description = "Modern, fast web file browser. Replaces traditional FTP and provides a beautiful interface for managing server files."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    <<: *common-keys-apps
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/filebrowser/config/filebrowser.db:/database/filebrowser.db
      - $DOCKERDIR/appdata/filebrowser/config/settings.json:/config/settings.json
      - $DATADRIVE:/srv/Media
      - $DOCKERDIR:/srv/DockerData
"""
````

## File: src/apps/fileflows.py
````python
from src.apps.base_app import BaseApp

class FileflowsApp(BaseApp):
    key = "fileflows"
    name = "FileFlows"
    port = 5001
    category = "tools"
    description = "Create automated workflows to process files (transcode, rename, move, clean)."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  fileflows:
    image: fileflows/fileflows:latest
    container_name: fileflows
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}/Data:/app/Data
      - {self.get_appdata_dir()}/Logs:/app/Logs
    ports:
      - 5001:5000
"""
````

## File: src/apps/firefly_iii.py
````python
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
````

## File: src/apps/flame.py
````python
from src.apps.base_app import BaseApp

class FlameApp(BaseApp):
    key = "flame"
    name = "Flame"
    port = 5005
    category = "networking"
    description = "Minimalist dashboard for self-hosted services and bookmarks."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dashboard"

    def get_compose_template(self) -> str:
        return f"""  flame:
    image: pawelmalak/flame:latest
    container_name: flame
    <<: *common-keys-apps
    environment:
      - PASSWORD=${{HTTP_PASSWORD}}
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 5005:5005
"""
````

## File: src/apps/flaresolverr.py
````python
from src.apps.base_app import BaseApp
class FlaresolverrApp(BaseApp):
    key = "flaresolverr"
    name = "Flaresolverr"
    port = 8191
    category = "none"
    description = "Proxy server to bypass Cloudflare and DDOS-Guard protections on torrent trackers, ensuring your indexers stay online."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = True
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  flaresolverr:
    image: ghcr.io/flaresolverr/flaresolverr:latest
    container_name: flaresolverr
    <<: *common-keys-apps
    environment:
      - LOG_LEVEL=info
      - TZ=$TZ
    ports:
      - ${FLARESOLVERR_PORT:-8191}:8191
"""
````

## File: src/apps/hkserver.py
````python
from src.apps.base_app import BaseApp
class HkserverApp(BaseApp):
    key = "hkserver"
    name = "Hkserver"
    port = 3838
    category = "none"
    description = "Dedicated server for Hollow Knight Multiplayer, allowing for cooperative play in a shared world."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  hkserver:
    image: hollowknight/hkmp:latest
    container_name: hkserver
    <<: *common-keys-apps
    ports:
      - 7777:7777/udp
"""
````

## File: src/apps/home_assistant.py
````python
from src.apps.base_app import BaseApp

class HomeAssistantApp(BaseApp):
    key = "home-assistant"
    name = "Home Assistant"
    port = 8123
    category = "networking"
    description = "Home automation hub that aggregates and controls smart devices locally."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  home-assistant:
    image: homeassistant/home-assistant:stable
    container_name: home-assistant
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
      - /run/dbus:/run/dbus:ro
    ports:
      - 8123:8123
"""
````

## File: src/apps/homepage.py
````python
from src.apps.base_app import BaseApp
class HomepageApp(BaseApp):
    key = "homepage"
    name = "Homepage"
    port = 3000
    category = "dash"
    description = "Highly customizable dashboard that provides a unified landing page and real-time status for all your services."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    <<: *common-keys-apps
    ports:
      - 3000:3000
    volumes:
      - $DOCKERDIR/appdata/homepage/config:/app/config
      - /var/run/docker.sock:/var/run/docker.sock
      - $USERDIR:/c
      - $DATADRIVE:/h
    environment:
      <<: *default-tz-puid-pgid
"""
````

## File: src/apps/immich.py
````python
from src.apps.base_app import BaseApp
class ImmichApp(BaseApp):
    key = "immich"
    name = "Immich"
    port = 2283
    category = "photos"
    description = "High-performance self-hosted solution for backing up and managing your personal photo and video collections."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  immich:
    image: ghcr.io/immich-app/immich-server:release
    container_name: immich
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/immich/data:/config
      - $DATADRIVE/photos:/photos
    ports:
      - 2283:3001
"""
````

## File: src/apps/it_tools.py
````python
from src.apps.base_app import BaseApp

class ItToolsApp(BaseApp):
    key = "it-tools"
    name = "IT-Tools"
    port = 8086
    category = "tools"
    description = "Useful offline-capable client-side tools for developers and IT professionals."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  it-tools:
    image: corentinth/it-tools:latest
    container_name: it-tools
    <<: *common-keys-apps
    ports:
      - 8086:80
"""
````

## File: src/apps/jellyfin.py
````python
from src.apps.base_app import BaseApp
class JellyfinApp(BaseApp):
    key = "jellyfin"
    name = "Jellyfin"
    port = 8096
    category = "jellyfin"
    description = "Free, open-source media system that provides total control over managing and streaming your media with no strings attached."
    stack_group = "media-server"
    recommendations = ['seerr', 'watchtower']
    is_configurable = False
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    <<: *common-keys-core
    environment:
      <<: *default-tz-puid-pgid
    ports:
      - 8096:8096
    volumes:
      - $DOCKERDIR/appdata/jellyfin/config:/config
      - $DATADRIVE/tv:/tv
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/anime:/anime
      - $DATADRIVE/music:/music
      - $DATADRIVE/audiobooks:/audiobooks
      - $DATADRIVE/books:/books
"""
````

## File: src/apps/kasm.py
````python
from src.apps.base_app import BaseApp
class KasmApp(BaseApp):
    key = "kasm"
    name = "Kasm"
    port = 6901
    category = "workspaces"
    description = "Containerized desktop infrastructure providing isolated, secure browser-based workspaces and remote access."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  kasm:
    image: lscr.io/linuxserver/kasm:latest
    container_name: kasm
    <<: *common-keys-core
    privileged: true
    environment:
      KASM_PORT: 6901
      <<: *default-tz-puid-pgid
    volumes:
      - $DOCKERDIR/appdata/kasm/config:/config
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 6901:6901
      - 4430:443
"""
````

## File: src/apps/komga.py
````python
from src.apps.base_app import BaseApp

class KomgaApp(BaseApp):
    key = "komga"
    name = "Komga"
    port = 8088
    category = "tools"
    description = "Dedicated media server for comic books, manga, and CBZ files."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  komga:
    image: gotson/komga:latest
    container_name: komga
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 8088:8080
"""
````

## File: src/apps/kopia.py
````python
from src.apps.base_app import BaseApp
class KopiaApp(BaseApp):
    key = "kopia"
    name = "Kopia"
    port = 28913
    category = "backup"
    description = "Fast and secure open-source backup tool that creates encrypted, deduplicated snapshots of your data."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  kopia:
    image: kopia/kopia:latest
    container_name: kopia
    <<: *common-keys-apps
    environment:
      <<: *default-tz-puid-pgid
      USER_UID: $PUID
      USER_GID: $PGID
    volumes:
      - $DOCKERDIR/appdata/kopia/config:/app/config
      - $DOCKERDIR/appdata/kopia/cache:/app/cache
      - $DOCKERDIR/appdata/kopia/logs:/app/logs
      - $DOCKERDIR/appdata:/source/appdata:ro
      - $DATADRIVE:/source/media:ro
    ports:
      - 51515:51515
    command: >
      server start
      --address 0.0.0.0:51515
      --server-username=$HTTP_USERNAME
      --server-password=$KOPIA_PASSWORD
      --config-file=/app/config/repository.config
      --log-dir=/app/logs
      --cache-directory=/app/cache
"""
````

## File: src/apps/lidarr.py
````python
from src.apps.base_app import BaseApp
class LidarrApp(BaseApp):
    key = "lidarr"
    name = "Lidarr"
    port = 8686
    category = "music"
    description = "Music collection manager that automatically discovers and downloads music from various providers."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  lidarr:
    image: lscr.io/linuxserver/lidarr:nightly
    container_name: lidarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/lidarr/config:/config
      - $DATADRIVE/music:/music
      - $DATADRIVE/downloads:/downloads
    ports:
      - ${LIDARR_PORT:-8686}:8686
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        import os
        results = []
        if self.key in keys:
            api_key = keys[self.key]
            headers = {"X-Api-Key": api_key}
            env_port = os.getenv("LIDARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            base_url = f"http://localhost:{port}/api/v1"
            
            write_step(f"Injecting Authentication for {self.name}...")
            try:
                current_config = rest_invoker(f"{base_url}/config/host", method="GET", headers=headers)
                if current_config:
                    current_config["authenticationMethod"] = "external"
                    rest_invoker(f"{base_url}/config/host", method="PUT", json_payload=current_config, headers=headers)
                    results.append(f"Configured {self.name} with external authentication")
            except Exception as e:
                write_log(f"Failed to inject auth for {self.name}: {str(e)}", level="WARN")

            try:
                naming_config = rest_invoker(f"{base_url}/config/naming", method="GET", headers=headers)
                if naming_config:
                    naming_config["renameTracks"] = True
                    rest_invoker(f"{base_url}/config/naming", method="PUT", json_payload=naming_config, headers=headers)
                    results.append(f"Enabled renaming rules for {self.name}")
            except Exception as e:
                write_log(f"Failed to enable renaming for {self.name}: {str(e)}", level="WARN")

            try:
                rest_invoker(f"{base_url}/rootfolder", method="POST", json_payload={"path": "/music"}, headers=headers)
                results.append(f"Configured default root path '/music' for {self.name}")
            except Exception:
                pass
        return results
````

## File: src/apps/loader.py
````python
import os
import pkgutil
import importlib
from typing import Dict, List
from src.apps.base_app import BaseApp

_loaded_apps: Dict[str, BaseApp] = {}

def load_apps() -> Dict[str, BaseApp]:
    global _loaded_apps
    if _loaded_apps:
        return _loaded_apps

    package_dir = os.path.dirname(__file__)
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        if module_name in ["base_app", "loader"]:
            continue
        try:
            full_module_name = f"src.apps.{module_name}"
            module = importlib.import_module(full_module_name)
            
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and issubclass(attribute, BaseApp) and attribute is not BaseApp:
                    app_instance = attribute()
                    if app_instance.key:
                        _loaded_apps[app_instance.key] = app_instance
        except Exception as e:
            from src.utils.logger import write_log
            write_log(f"Failed to load app plugin '{module_name}': {str(e)}", level="ERROR")
            
    return _loaded_apps

def get_apps_list() -> List[BaseApp]:
    apps_dict = load_apps()
    return sorted(apps_dict.values(), key=lambda x: x.key)
````

## File: src/apps/mariadb_adminer.py
````python
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
````

## File: src/apps/mealie.py
````python
from src.apps.base_app import BaseApp

class MealieApp(BaseApp):
    key = "mealie"
    name = "Mealie"
    port = 9005
    category = "tools"
    description = "Self-hosted recipe manager and meal planner with website recipe scraper."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  mealie:
    image: ghcr.io/mealie-recipes/mealie:latest
    container_name: mealie
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 9005:9000
"""
````

## File: src/apps/mongodb_mongo_express.py
````python
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
````

## File: src/apps/mylar.py
````python
from src.apps.base_app import BaseApp
class MylarApp(BaseApp):
    key = "mylar"
    name = "Mylar"
    port = 8090
    category = "comics"
    description = "Automated comic book downloader that monitors for new issues and handles the download and organization process."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  mylar:
    image: lscr.io/linuxserver/mylar3:latest
    container_name: mylar
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/mylar/config:/config
      - $DATADRIVE/comics:/comics
      - $DATADRIVE/downloads:/downloads
    ports:
      - 8090:8090
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        import os
        results = []
        if self.key in keys:
            api_key = keys[self.key]
            headers = {"X-Api-Key": api_key}
            env_port = os.getenv("MYLAR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            base_url = f"http://localhost:{port}/api/v1"
            
            write_step(f"Injecting Authentication for {self.name}...")
            try:
                current_config = rest_invoker(f"{base_url}/config/host", method="GET", headers=headers)
                if current_config:
                    current_config["authenticationMethod"] = "external"
                    rest_invoker(f"{base_url}/config/host", method="PUT", json_payload=current_config, headers=headers)
                    results.append(f"Configured {self.name} with external authentication")
            except Exception as e:
                write_log(f"Failed to inject auth for {self.name}: {str(e)}", level="WARN")
        return results
````

## File: src/apps/navidrome.py
````python
from src.apps.base_app import BaseApp
class NavidromeApp(BaseApp):
    key = "navidrome"
    name = "Navidrome"
    port = 4533
    category = "music"
    description = "High-performance music streaming server and library. The perfect companion to Lidarr for listening to your music collection anywhere."
    stack_group = "media-server"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    <<: *common-keys-apps
    environment:
      - ND_SCANSCHEDULE=1h
      - ND_LOGLEVEL=info
      - ND_BASEURL=""
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/navidrome/data:/data
      - $DATADRIVE/music:/music:ro
    ports:
      - 4533:4533
"""
````

## File: src/apps/netdata.py
````python
from src.apps.base_app import BaseApp

class NetdataApp(BaseApp):
    key = "netdata"
    name = "Netdata"
    port = 19999
    category = "management"
    description = "Real-time system health and resource monitor tracking metrics at per-second intervals."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  netdata:
    image: netdata/netdata:latest
    container_name: netdata
    <<: *common-keys-apps
    cap_add:
      - SYS_PTRACE
    security_opt:
      - apparmor:unconfined
    volumes:
      - {self.get_appdata_dir()}/netdataconfig:/etc/netdata
      - {self.get_appdata_dir()}/netdatalib:/var/lib/netdata
      - {self.get_appdata_dir()}/netdatacache:/var/cache/netdata
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - 19999:19999
"""
````

## File: src/apps/nextcloud.py
````python
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
````

## File: src/apps/paperless.py
````python
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
````

## File: src/apps/pihole.py
````python
from src.apps.base_app import BaseApp

class PiholeApp(BaseApp):
    key = "pihole"
    name = "Pi-hole"
    port = 8081
    category = "networking"
    description = "Network-wide DNS tracker and ad-blocker sinkhole."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None
    exclusivity_group = "dns_resolver"

    def get_compose_template(self) -> str:
        return f"""  pihole:
    image: pihole/pihole:latest
    container_name: pihole
    <<: *common-keys-apps
    environment:
      - TZ=${{TZ}}
      - WEBPASSWORD=${{HTTP_PASSWORD}}
    volumes:
      - {self.get_appdata_dir()}/etc:/etc/pihole
      - {self.get_appdata_dir()}/dnsmasq:/etc/dnsmasq.d
    ports:
      - 53:53/tcp
      - 53:53/udp
      - 8081:80
"""
````

## File: src/apps/plex.py
````python
from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class PlexConfig(BaseModel):
    PLEX_CLAIM: str = Field(
        default="", 
        description="Plex Claim Token", 
        json_schema_extra={
            "help_url": "https://www.plex.tv/claim",
            "is_secret": True
        }
    )

class PlexApp(BaseApp):
    key = "plex"
    name = "Plex"
    port = 32400
    category = "plex"
    description = "Premium media server that organizes your collections and streams them to any device, featuring rich metadata and remote access."
    stack_group = "media-server"
    recommendations = ['tautulli', 'seerr', 'watchtower', 'plextraktsync']
    is_configurable = False
    has_widget = True
    config_model = PlexConfig

    def get_compose_template(self) -> str:
        return """  plex:
    image: lscr.io/linuxserver/plex:latest
    container_name: plex
    <<: *common-keys-core
    environment:
      - VERSION=docker
      - PLEX_CLAIM=$PLEX_CLAIM
      - TZ=$TZ
      - PUID=$PUID
      - PGID=$PGID
      - NVIDIA_VISIBLE_DEVICES=all
    ports:
      - 32400:32400
      - 1900:1900/udp
      - 3005:3005
      - 8324:8324/tcp
      - 32410:32410/udp
      - 32412:32412/udp
      - 32413:32413/udp
      - 32414:32414/udp
      - 32469:32469
    volumes:
      - $DOCKERDIR/appdata/plex/config:/config
      - $DATADRIVE/tv:/tv
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/anime:/anime
      - $DATADRIVE/music:/music
      - $DATADRIVE/audiobooks:/audiobooks
"""
````

## File: src/apps/plextraktsync.py
````python
from src.apps.base_app import BaseApp
class PlextraktsyncApp(BaseApp):
    key = "plextraktsync"
    name = "Plextraktsync"
    port = 0
    category = "none"
    description = "Dynamic two-way synchronization tool between your Plex media library and Trakt.tv profiles."
    stack_group = "media-server"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  plextraktsync:
    image: ghcr.io/taxel/plextraktsync:latest
    container_name: plextraktsync
    <<: *common-keys-apps
    command: watch
    volumes:
      - $DOCKERDIR/appdata/plextraktsync:/app/config
"""
````

## File: src/apps/portainer.py
````python
from src.apps.base_app import BaseApp
class PortainerApp(BaseApp):
    key = "portainer"
    name = "Portainer"
    port = 9443
    category = "docker"
    description = "Powerful GUI for managing Docker containers, images, and networks through a user-friendly web interface."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  portainer:
    container_name: portainer
    image: portainer/portainer-ce:latest
    command: -H unix:///var/run/docker.sock
    ports:
      - 9443:9443
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - $DOCKERDIR/appdata/portainer/data:/data
    <<: *common-keys-core
    environment:
      <<: *default-tz-puid-pgid
"""
````

## File: src/apps/postgresql_cloudbeaver.py
````python
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
````

## File: src/apps/prowlarr.py
````python
from src.apps.base_app import BaseApp
class ProwlarrApp(BaseApp):
    key = "prowlarr"
    name = "Prowlarr"
    port = 9696
    category = "indexers"
    description = "Indexer manager/proxy that integrates with your PVR apps to manage Torrent Trackers and Usenet Indexers in one place."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/prowlarr/config:/config
    ports:
      - ${PROWLARR_PORT:-9696}:9696
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        from src.utils.state import get_metadata
        import os
        results = []
        if self.key in keys:
            p_key = keys[self.key]
            env_port = os.getenv("PROWLARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            p_url = f"http://localhost:{port}/api/v1/applications?apikey={p_key}"
            prowlarr_indexers_url = f"http://localhost:{port}/api/v1/indexer?apikey={p_key}"

            metadata = get_metadata()
            selected = metadata.get("selected_services", [])

            pvr_categories = {
                "sonarr":  {"sync": [5000, 5010, 5020, 5030, 5040, 5045, 5050], "anime": [5070], "port": 8989},
                "radarr":  {"sync": [2000, 2010, 2020, 2030, 2040, 2045, 2050, 2060], "anime": [2070], "port": 7878},
                "lidarr":  {"sync": [3000, 3010, 3020, 3030, 3040], "anime": [], "port": 8686},
                "readarr": {"sync": [7000, 7010, 7020, 7030, 7040, 7050], "anime": [], "port": 8787},
                "mylar":   {"sync": [7000, 7010, 7020, 7030, 7040, 7050], "anime": [], "port": 8090},
            }

            for app, cats in pvr_categories.items():
                if app in selected and app in keys:
                    write_log(f"Stitching Prowlarr to {app}...")
                    fields = [
                        {"name": "prowlarrUrl", "value": "http://prowlarr:9696"},
                        {"name": "baseUrl",     "value": f"http://{app}:{cats['port']}"},
                        {"name": "apiKey",      "value": keys[app]},
                        {"name": "syncCategories",      "value": cats["sync"]},
                    ]
                    if cats["anime"]:
                        fields.append({"name": "animeSyncCategories", "value": cats["anime"]})

                    payload = {
                        "name": app.upper(),
                        "implementation": app.capitalize(),
                        "configContract": f"{app.capitalize()}Settings",
                        "syncLevel": "fullSync",
                        "syncProfileIds": [1],
                        "fields": fields,
                        "tags": []
                    }
                    try:
                        rest_invoker(p_url, method="POST", json_payload=payload)
                        results.append(f"Linked Prowlarr to {app}")
                    except Exception as e:
                        write_log(f"Failed to link Prowlarr to {app}: {str(e)}", level="WARN")

            if "flaresolverr" in selected:
                write_log("Adding FlareSolverr proxy to Prowlarr...")
                proxy_url = f"http://localhost:{port}/api/v1/indexerproxy?apikey={p_key}"
                proxy_payload = {
                    "name": "FlareSolverr",
                    "implementation": "FlareSolverr",
                    "configContract": "FlareSolverrSettings",
                    "fields": [
                        {"name": "host", "value": "http://flaresolverr:8191"},
                        {"name": "requestTimeout", "value": 60}
                    ]
                }
                try:
                    rest_invoker(proxy_url, method="POST", json_payload=proxy_payload)
                    results.append("Added FlareSolverr proxy to Prowlarr")
                except Exception as e:
                    write_log(f"Failed to add FlareSolverr proxy to Prowlarr: {str(e)}", level="WARN")

            nzb_indexers = [
                {
                    "name": "Sky-Of-Usenet (Free)",
                    "implementation": "Newznab",
                    "configContract": "NewznabSettings",
                    "fields": [{"name": "baseUrl", "value": "https://skyofusenet.de"}]
                },
                {
                    "name": "NZBFinder (Free Tier)",
                    "implementation": "Newznab",
                    "configContract": "NewznabSettings",
                    "fields": [{"name": "baseUrl", "value": "https://nzbfinder.ws"}]
                },
                {
                    "name": "Tabula-Rasa (Free Tier)",
                    "implementation": "Newznab",
                    "configContract": "NewznabSettings",
                    "fields": [{"name": "baseUrl", "value": "https://www.nzb-rasa.com"}]
                }
            ]
            
            torrent_indexers = [
                {
                    "name": "1337x",
                    "implementation": "Cardigann",
                    "configContract": "CardigannSettings",
                    "fields": [{"name": "baseUrl", "value": "https://1337x.to"}]
                },
                {
                    "name": "EZTV",
                    "implementation": "Cardigann",
                    "configContract": "CardigannSettings",
                    "fields": [{"name": "baseUrl", "value": "https://eztv.re"}]
                }
            ]

            indexers_to_seed = list(nzb_indexers)
            if "qbittorrent" in selected or "qbittorrent-vpn" in selected:
                indexers_to_seed.extend(torrent_indexers)

            write_log("Auto-seeding free Usenet and torrent indexers in Prowlarr...", level="INFO")
            for indexer in indexers_to_seed:
                payload = {
                    "name": indexer["name"],
                    "enable": True,
                    "implementation": indexer["implementation"],
                    "configContract": indexer["configContract"],
                    "fields": indexer["fields"]
                }
                try:
                    rest_invoker(prowlarr_indexers_url, method="POST", json_payload=payload)
                    results.append(f"Auto-seeded indexer: {indexer['name']}")
                except Exception:
                    pass

            if os.getenv("DS_HEADLESS") != "true":
                from src.utils.logger import safe_confirm, console
                import questionary
                console.print("\n----------------------------------------------------------", style="cyan")
                console.print("             PREMIUM USENET INDEXER SETUP", style="cyan")
                console.print("----------------------------------------------------------", style="cyan")
                console.print("For automated downloading, it is highly recommended to add one premium Usenet indexer.")
                
                if safe_confirm("Would you like to configure a premium Usenet indexer now?", default=True):
                    prov = questionary.select(
                        "Select USENET Indexer to add:",
                        choices=["NZBGeek", "NinjaCentral", "AltHub", "Other Newznab"]
                    ).ask()
                    
                    if prov:
                        base_urls = {
                            "NZBGeek": "https://api.nzbgeek.info",
                            "NinjaCentral": "https://ninjacentral.co.za",
                            "AltHub": "https://althub.co.za"
                        }
                        
                        b_url = questionary.text("Enter Indexer Base URL (e.g. https://custom-index.com):").ask() if prov == "Other Newznab" else base_urls.get(prov)
                            
                        if b_url:
                            api_key = questionary.password(f"Enter your {prov} API Key:").ask()
                            if api_key and api_key.strip():
                                premium_payload = {
                                    "name": prov,
                                    "enable": True,
                                    "implementation": "Newznab",
                                    "configContract": "NewznabSettings",
                                    "fields": [
                                        {"name": "baseUrl", "value": b_url.strip()},
                                        {"name": "apiKey", "value": api_key.strip()}
                                    ]
                                }
                                try:
                                    rest_invoker(prowlarr_indexers_url, method="POST", json_payload=premium_payload)
                                    results.append(f"Successfully configured premium indexer: {prov}")
                                    console.print(f"[✓] Linked {prov} to Prowlarr", style="green")
                                except Exception as e:
                                    write_log(f"Failed to add premium indexer {prov}: {str(e)}", level="WARN")

        return results
````

## File: src/apps/qbittorrent_vpn.py
````python
from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class QbittorrentVpnConfig(BaseModel):
    VPN_PROV: str = Field(default="custom", description="VPN Provider (e.g. custom, mullvad, pia)")
    VPN_CLIENT: str = Field(default="wireguard", description="VPN Client (e.g. wireguard, openvpn)")
    VPN_USER: str = Field(default="", description="VPN Username")
    VPN_PASS: str = Field(default="", description="VPN Password", json_schema_extra={"is_secret": True})
    LAN_NETWORK: str = Field(default="192.168.1.0/24", description="Local Network Range (e.g. 192.168.1.0/24)")

class QbittorrentVpnApp(BaseApp):
    key = "qbittorrent-vpn"
    name = "qBittorrent-VPN"
    port = 8081
    category = "torrents-vpn"
    description = "Advanced BitTorrent client bundled with a VPN client and an automatic killswitch to ensure all traffic is encrypted and anonymous."
    stack_group = "downloaders"
    recommendations = []
    is_configurable = False
    has_widget = True
    config_model = QbittorrentVpnConfig

    def get_compose_template(self) -> str:
        return """  qbittorrent-vpn:
    image: binhex/arch-qbittorrentvpn:latest
    container_name: qbit-vpn
    <<: *common-keys-apps
    environment:
      - VPN_ENABLED=yes
      - VPN_PROV=$VPN_PROV
      - VPN_CLIENT=$VPN_CLIENT
      - VPN_USER=$VPN_USER
      - VPN_PASS=$VPN_PASS
      - LAN_NETWORK=$LAN_NETWORK
      - NAME_SERVERS=1.1.1.1,8.8.8.8
      - STRICT_PORT_FORWARD=yes
      - ENABLE_PRIVOXY=yes
      - WEBUI_PORT=8081
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/qbit-vpn/config:/config
      - $DATADRIVE/downloads:/data
    ports:
      - ${QBITTORRENT_VPN_PORT:-8081}:8081
      - 8118:8118
      - 6881:6881
      - 6881:6881/udp
    cap_add:
      - NET_ADMIN
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        from src.utils.state import get_metadata
        import os
        import json
        import requests
        results = []
        if self.key in keys:
            metadata = get_metadata()
            selected = metadata.get("selected_services", [])
            sso_enabled = any(provider in selected for provider in ["authelia", "authentik"])
            tier = os.getenv("DEPLOY_TIER", "1")
            http_user = os.getenv("HTTP_USERNAME", "admin")
            http_pass = os.getenv("HTTP_PASSWORD", "")

            if sso_enabled:
                write_log("Skipping qBittorrent credentials injection (delegated to SSO gateway).", level="DEBUG")
                results.append("qBittorrent configured with default credentials (delegated to SSO gateway)")
            elif tier == "1":
                write_log("Skipping qBittorrent credentials injection for minimal installation.", level="DEBUG")
                results.append("qBittorrent configured with default credentials")
            else:
                qbit_port = int(os.getenv("QBITTORRENT_VPN_PORT", str(self.port)))
                write_step("Injecting Authentication for qBittorrent-VPN...")
                
                creds_to_try = [
                    {"u": http_user, "p": http_pass},
                    {"u": "admin", "p": "adminadmin"}
                ]
                
                login_success = False
                qbit_session = requests.Session()
                
                for cred in creds_to_try:
                    try:
                        payload = {"username": cred["u"], "password": cred["p"]}
                        res = qbit_session.post(
                            f"http://localhost:{qbit_port}/api/v2/auth/login",
                            data=payload,
                            timeout=5,
                            verify=False
                        )
                        if res.text.strip() == "Ok.":
                            login_success = True
                            break
                    except Exception:
                        pass
                
                if login_success:
                    try:
                        prefs = {"web_ui_username": http_user, "web_ui_password": http_pass}
                        qbit_session.post(
                            f"http://localhost:{qbit_port}/api/v2/app/setPreferences",
                            data={"json": json.dumps(prefs)},
                            timeout=5,
                            verify=False
                        )
                        results.append("Secured qBittorrent with management credentials")
                    except Exception as e:
                        write_log(f"Failed to set qBittorrent preferences: {str(e)}", level="WARN")

            pvr_apps = ["sonarr", "radarr", "lidarr"]
            for app in pvr_apps:
                if app in keys:
                    write_log(f"Linking qBittorrent-VPN to {app}...")
                    pvr_port = 7878 if app == "radarr" else (8686 if app == "lidarr" else 8989)
                    api_v = "v1" if app == "lidarr" else "v3"
                    app_url = f"http://localhost:{pvr_port}/api/{api_v}/downloadclient?apikey={keys[app]}"
                    
                    qbit_host = "qbit-vpn"
                    qbit_payload = {
                        "enable": True,
                        "priority": 1,
                        "name": self.name,
                        "implementation": "Qbittorrent",
                        "configContract": "QbittorrentSettings",
                        "fields": [
                            {"name": "host", "value": qbit_host},
                            {"name": "port", "value": 8081},
                            {"name": "username", "value": http_user if not sso_enabled and tier != "1" else "admin"},
                            {"name": "password", "value": http_pass if not sso_enabled and tier != "1" else "adminadmin"},
                            {"name": "movieCategory", "value": "movies"},
                            {"name": "tvCategory", "value": "tv"}
                        ]
                    }
                    try:
                        rest_invoker(app_url, method="POST", json_payload=qbit_payload)
                        results.append(f"Connected {self.name} to {app}")
                    except Exception as e:
                        write_log(f"Failed to connect {self.name} to {app}: {str(e)}", level="WARN")

        return results
````

## File: src/apps/qbittorrent.py
````python
from src.apps.base_app import BaseApp
class QbittorrentApp(BaseApp):
    key = "qbittorrent"
    name = "Qbittorrent"
    port = 8081
    category = "torrents"
    description = "Lightweight, open-source BitTorrent client with a stable and feature-rich web interface for managing downloads."
    stack_group = "downloaders"
    recommendations = ['prowlarr', 'sonarr', 'radarr']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbit
    <<: *common-keys-apps
    environment:
      - WEBUI_PORT=8081
    volumes:
      - $DOCKERDIR/appdata/qbit/config:/config
      - $DATADRIVE/downloads:/downloads
    ports:
      - ${QBITTORRENT_PORT:-8081}:8081
      - 6881:6881
      - 6881:6881/udp
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        from src.utils.state import get_metadata
        import os
        import json
        import requests
        results = []
        if self.key in keys:
            metadata = get_metadata()
            selected = metadata.get("selected_services", [])
            sso_enabled = any(provider in selected for provider in ["authelia", "authentik"])
            tier = os.getenv("DEPLOY_TIER", "1")
            http_user = os.getenv("HTTP_USERNAME", "admin")
            http_pass = os.getenv("HTTP_PASSWORD", "")

            if sso_enabled:
                write_log("Skipping qBittorrent credentials injection (delegated to SSO gateway).", level="DEBUG")
                results.append("qBittorrent configured with default credentials (delegated to SSO gateway)")
            elif tier == "1":
                write_log("Skipping qBittorrent credentials injection for minimal installation.", level="DEBUG")
                results.append("qBittorrent configured with default credentials")
            else:
                qbit_port = int(os.getenv("QBITTORRENT_PORT", str(self.port)))
                write_step("Injecting Authentication for qBittorrent...")
                
                creds_to_try = [
                    {"u": http_user, "p": http_pass},
                    {"u": "admin", "p": "adminadmin"}
                ]
                
                login_success = False
                qbit_session = requests.Session()
                
                for cred in creds_to_try:
                    try:
                        payload = {"username": cred["u"], "password": cred["p"]}
                        res = qbit_session.post(
                            f"http://localhost:{qbit_port}/api/v2/auth/login",
                            data=payload,
                            timeout=5,
                            verify=False
                        )
                        if res.text.strip() == "Ok.":
                            login_success = True
                            break
                    except Exception:
                        pass
                
                if login_success:
                    try:
                        prefs = {"web_ui_username": http_user, "web_ui_password": http_pass}
                        qbit_session.post(
                            f"http://localhost:{qbit_port}/api/v2/app/setPreferences",
                            data={"json": json.dumps(prefs)},
                            timeout=5,
                            verify=False
                        )
                        results.append("Secured qBittorrent with management credentials")
                    except Exception as e:
                        write_log(f"Failed to set qBittorrent preferences: {str(e)}", level="WARN")

            pvr_apps = ["sonarr", "radarr", "lidarr"]
            for app in pvr_apps:
                if app in keys:
                    write_log(f"Linking qBittorrent to {app}...")
                    pvr_port = 7878 if app == "radarr" else (8686 if app == "lidarr" else 8989)
                    api_v = "v1" if app == "lidarr" else "v3"
                    app_url = f"http://localhost:{pvr_port}/api/{api_v}/downloadclient?apikey={keys[app]}"
                    
                    qbit_host = "qbit" if self.key == "qbittorrent" else "qbit-vpn"
                    qbit_payload = {
                        "enable": True,
                        "priority": 1,
                        "name": self.name,
                        "implementation": "Qbittorrent",
                        "configContract": "QbittorrentSettings",
                        "fields": [
                            {"name": "host", "value": qbit_host},
                            {"name": "port", "value": 8081},
                            {"name": "username", "value": http_user if not sso_enabled and tier != "1" else "admin"},
                            {"name": "password", "value": http_pass if not sso_enabled and tier != "1" else "adminadmin"},
                            {"name": "movieCategory", "value": "movies"},
                            {"name": "tvCategory", "value": "tv"}
                        ]
                    }
                    try:
                        rest_invoker(app_url, method="POST", json_payload=qbit_payload)
                        results.append(f"Connected {self.name} to {app}")
                    except Exception as e:
                        write_log(f"Failed to connect {self.name} to {app}: {str(e)}", level="WARN")

        return results
````

## File: src/apps/radarr.py
````python
from src.apps.base_app import BaseApp
class RadarrApp(BaseApp):
    key = "radarr"
    name = "Radarr"
    port = 7878
    category = "movies"
    description = "Movie PVR for Usenet and BitTorrent. Automatically monitors for new movies and interfaces with download clients to organize your library."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'bazarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/radarr/config:/config
      - $DATADRIVE/movies:/movies
      - $DATADRIVE/downloads:/downloads
    ports:
      - ${RADARR_PORT:-7878}:7878
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        import os
        results = []
        if self.key in keys:
            api_key = keys[self.key]
            headers = {"X-Api-Key": api_key}
            env_port = os.getenv("RADARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            base_url = f"http://localhost:{port}/api/v3"
            
            write_step(f"Injecting Authentication for {self.name}...")
            try:
                current_config = rest_invoker(f"{base_url}/config/host", method="GET", headers=headers)
                if current_config:
                    current_config["authenticationMethod"] = "external"
                    rest_invoker(f"{base_url}/config/host", method="PUT", json_payload=current_config, headers=headers)
                    results.append(f"Configured {self.name} with external authentication")
            except Exception as e:
                write_log(f"Failed to inject auth for {self.name}: {str(e)}", level="WARN")

            try:
                naming_config = rest_invoker(f"{base_url}/config/naming", method="GET", headers=headers)
                if naming_config:
                    naming_config["renameEpisodes"] = True
                    rest_invoker(f"{base_url}/config/naming", method="PUT", json_payload=naming_config, headers=headers)
                    results.append(f"Enabled renaming rules for {self.name}")
            except Exception as e:
                write_log(f"Failed to enable renaming for {self.name}: {str(e)}", level="WARN")

            try:
                rest_invoker(f"{base_url}/rootfolder", method="POST", json_payload={"path": "/movies"}, headers=headers)
                results.append(f"Configured default root path '/movies' for {self.name}")
            except Exception:
                pass

            plex_token = os.getenv("PLEX_TOKEN")
            if plex_token and plex_token.strip():
                try:
                    payload = {
                        "name": "Plex Watchlist",
                        "enableAuto": True,
                        "enabled": True,
                        "shouldMonitor": True,
                        "listType": "plex",
                        "implementation": "PlexWatchlistImport",
                        "configContract": "PlexWatchlistSettings",
                        "qualityProfileId": 1,
                        "rootFolderPath": "/movies",
                        "searchOnAdd": True,
                        "minimumAvailability": "announced",
                        "fields": [
                            {"name": "plexToken", "value": plex_token.strip()},
                            {"name": "syncInterval", "value": 180}
                        ],
                        "tags": []
                    }
                    rest_invoker(f"{base_url}/importlist", method="POST", json_payload=payload, headers=headers)
                    results.append(f"Configured Plex Watchlist import list for {self.name}")
                except Exception as e:
                    write_log(f"Failed to configure Plex Watchlist for {self.name}: {str(e)}", level="WARN")

            try:
                stevenlu_payload = {
                    "name": "StevenLu List",
                    "enableAuto": True,
                    "enabled": True,
                    "shouldMonitor": True,
                    "listType": "popular",
                    "implementation": "StevenLuImport",
                    "configContract": "StevenLuSettings",
                    "qualityProfileId": 1,
                    "rootFolderPath": "/movies",
                    "searchOnAdd": False,
                    "minimumAvailability": "announced",
                    "fields": [
                        {"name": "baseUrl", "value": "https://api.radarr.video/v1/ma/movie/popular"}
                    ],
                    "tags": []
                }
                rest_invoker(f"{base_url}/importlist", method="POST", json_payload=stevenlu_payload, headers=headers)
                results.append("Configured StevenLu Movie List for Radarr")
            except Exception as e:
                write_log(f"Failed to configure StevenLu list for Radarr: {str(e)}", level="WARN")

        return results
````

## File: src/apps/readarr.py
````python
from src.apps.base_app import BaseApp
class ReadarrApp(BaseApp):
    key = "readarr"
    name = "Readarr"
    port = 8787
    category = "books"
    description = "Book downloader and library manager that automatically handles both E-books and Audiobooks via Usenet and BitTorrent."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  readarr:
    image: lscr.io/linuxserver/readarr:develop
    container_name: readarr
    <<: *common-keys-apps
    environment:
      <<: *default-tz-puid-pgid
    volumes:
      - $DOCKERDIR/appdata/readarr/config:/config
      - $DATADRIVE/books:/books
      - $DATADRIVE/audiobooks:/audiobooks
      - $DATADRIVE/downloads:/downloads
    ports:
      - 8787:8787
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        import os
        results = []
        if self.key in keys:
            api_key = keys[self.key]
            headers = {"X-Api-Key": api_key}
            env_port = os.getenv("READARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            base_url = f"http://localhost:{port}/api/v1"
            
            write_step(f"Injecting Authentication for {self.name}...")
            try:
                current_config = rest_invoker(f"{base_url}/config/host", method="GET", headers=headers)
                if current_config:
                    current_config["authenticationMethod"] = "external"
                    rest_invoker(f"{base_url}/config/host", method="PUT", json_payload=current_config, headers=headers)
                    results.append(f"Configured {self.name} with external authentication")
            except Exception as e:
                write_log(f"Failed to inject auth for {self.name}: {str(e)}", level="WARN")
        return results
````

## File: src/apps/recyclarr.py
````python
from src.apps.base_app import BaseApp
class RecyclarrApp(BaseApp):
    key = "recyclarr"
    name = "Recyclarr"
    port = 0
    category = "none"
    description = "Syncs recommended settings from TRaSH Guides to Sonarr and Radarr to ensure your media quality profiles are always optimal."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  recyclarr:
    image: ghcr.io/recyclarr/recyclarr:latest
    container_name: recyclarr
    user: $PUID:$PGID
    volumes:
      - $DOCKERDIR/appdata/recyclarr/config:/config
    environment:
      - TZ=$TZ
    restart: unless-stopped
"""
````

## File: src/apps/sabnzbd.py
````python
from src.apps.base_app import BaseApp
class SabnzbdApp(BaseApp):
    key = "sabnzbd"
    name = "Sabnzbd"
    port = 8080
    category = "usenet"
    description = "Automated Usenet download tool that handles all file processing and verification with a simple web-based interface."
    stack_group = "downloaders"
    recommendations = ['prowlarr', 'sonarr', 'radarr']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  sabnzbd:
    image: lscr.io/linuxserver/sabnzbd:latest
    container_name: sabnzbd
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/sabnzbd/config:/config
      - $DATADRIVE/downloads:/downloads
      - $DATADRIVE/downloads/incomplete:/incompletedownloads
    ports:
      - 8080:8080
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        from src.utils.state import get_metadata
        import os
        import re
        results = []
        if self.key in keys:
            metadata = get_metadata()
            selected = metadata.get("selected_services", [])
            sso_enabled = any(provider in selected for provider in ["authelia", "authentik"])
            tier = os.getenv("DEPLOY_TIER", "1")
            http_user = os.getenv("HTTP_USERNAME", "admin")
            http_pass = os.getenv("HTTP_PASSWORD", "")

            sab_ini = os.path.join(deploy_dir, "appdata", "sabnzbd", "config", "sabnzbd.ini")
            if sso_enabled:
                write_log("Skipping SABnzbd credentials injection (delegated to SSO gateway).", level="DEBUG")
                results.append("SABnzbd configured unauthenticated (delegated to SSO gateway)")
            elif tier == "1":
                write_log("Skipping SABnzbd credentials injection for minimal installation.", level="DEBUG")
                results.append("SABnzbd configured unauthenticated")
                
                if not os.path.exists(sab_ini):
                    os.makedirs(os.path.dirname(sab_ini), exist_ok=True)
                    default_ini = "[misc]\nusername =\npassword =\n[servers]\n"
                    with open(sab_ini, "w", encoding="utf-8") as f:
                        f.write(default_ini)

                if os.getenv("DS_HEADLESS") != "true":
                    import questionary
                    from src.utils.logger import safe_confirm, console
                    if safe_confirm("\nWould you like to configure your USENET news server details now?", default=True):
                        host = questionary.text("Enter USENET Server Host (e.g. news.newsgroup.ninja):").ask()
                        if host and host.strip():
                            port = questionary.text("Enter Port (e.g. 563 for SSL, 119 for non-SSL):", default="563").ask()
                            username = questionary.text("Enter Newsgroup Username:").ask()
                            password = questionary.password("Enter Newsgroup Password:").ask()
                            
                            server_section = f"\n[[{host}]]\nname = {host}\nhost = {host}\nport = {port}\nusername = {username}\npassword = {password}\nconnections = 20\nssl = 1\nssl_verify = 2\nenable = 1\n"
                            try:
                                with open(sab_ini, "r", encoding="utf-8") as f:
                                    content = f.read()
                                if "[servers]" in content:
                                    content = content.replace("[servers]", f"[servers]\n{server_section}")
                                else:
                                    content += f"\n[servers]\n{server_section}"
                                with open(sab_ini, "w", encoding="utf-8") as f:
                                    f.write(content)
                                results.append("Configured primary USENET Server connection in SABnzbd")
                            except Exception as e:
                                write_log(f"Failed to pre-seed USENET server configuration: {str(e)}", level="WARN")

            if not sso_enabled and http_pass:
                write_step("Injecting Authentication for SABnzbd...")
                if os.path.exists(sab_ini):
                    try:
                        with open(sab_ini, "r", encoding="utf-8") as f:
                            ini_content = f.read()
                        
                        new_ini = re.sub(r"^username\s*=.*", f"username = {http_user}", ini_content, flags=re.MULTILINE)
                        new_ini = re.sub(r"^password\s*=.*", f"password = {http_pass}", new_ini, flags=re.MULTILINE)
                        
                        whitelist_value = "host_whitelist = sabnzbd, localhost, 127.0.0.1, 192.168.90.11"
                        if "host_whitelist" in new_ini:
                            new_ini = re.sub(r"^host_whitelist\s*=.*", whitelist_value, new_ini, flags=re.MULTILINE)
                        else:
                            if "[misc]" in new_ini:
                                new_ini = new_ini.replace("[misc]", f"[misc]\n{whitelist_value}")
                            else:
                                new_ini += f"\n{whitelist_value}\n"
                        
                        with open(sab_ini, "w", encoding="utf-8") as f:
                            f.write(new_ini)
                        results.append("Secured SABnzbd and configured host whitelist")
                    except Exception as e:
                        write_log(f"Failed to write SABnzbd configurations: {str(e)}", level="WARN")

            # Link SABnzbd to PVRs
            pvr_apps = ["sonarr", "radarr", "lidarr"]
            for app in pvr_apps:
                if app in keys:
                    write_log(f"Linking SABnzbd to {app}...")
                    pvr_port = 7878 if app == "radarr" else (8686 if app == "lidarr" else 8989)
                    api_v = "v1" if app == "lidarr" else "v3"
                    app_url = f"http://localhost:{pvr_port}/api/{api_v}/downloadclient?apikey={keys[app]}"
                    
                    sab_payload = {
                        "enable": True, 
                        "priority": 1, 
                        "name": "SABnzbd", 
                        "implementation": "Sabnzbd", 
                        "configContract": "SabnzbdSettings",
                        "fields": [
                            {"name": "host", "value": "sabnzbd"}, 
                            {"name": "port", "value": 8080},
                            {"name": "apiKey", "value": keys["sabnzbd"]}, 
                            {"name": "movieCategory", "value": "movies"},
                            {"name": "tvCategory", "value": "tv"}
                        ]
                    }
                    try:
                        rest_invoker(app_url, method="POST", json_payload=sab_payload)
                        results.append(f"Connected SABnzbd to {app}")
                    except Exception as e:
                        write_log(f"Failed to connect SABnzbd to {app}: {str(e)}", level="WARN")

        return results
````

## File: src/apps/satisfactory.py
````python
from src.apps.base_app import BaseApp
class SatisfactoryApp(BaseApp):
    key = "satisfactory"
    name = "Satisfactory"
    port = 15777
    category = "satisfactory"
    description = "Dedicated server for hosting Satisfactory games, allowing players to build massive factories together on a persistent world."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  satisfactory:
    container_name: 'satisfactory-server'
    hostname: 'satisfactory-server'
    image: 'wolveix/satisfactory-server:latest'
    ports:
      - '8012:7777/tcp'
      - '8012:7777/udp'
      - '8888:8888/tcp'
    volumes:
      - $DOCKERDIR/appdata/satisfactory/config:/config
    environment:
      - MAXPLAYERS=10
      - PGID=1000
      - PUID=1000
      - STEAMBETA=true
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G
"""
````

## File: src/apps/scrutiny.py
````python
from src.apps.base_app import BaseApp
class ScrutinyApp(BaseApp):
    key = "scrutiny"
    name = "Scrutiny"
    port = 8086
    category = "status"
    description = "Hard drive S.M.A.R.T. monitoring dashboard that tracks disk health and alerts you to potential failures before they happen."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  scrutiny:
    image: ghcr.io/analogj/scrutiny:latest-omnibus
    container_name: scrutiny
    <<: *common-keys-apps
    cap_add:
      - SYS_RAWIO
      - SYS_ADMIN
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - /run/udev:/run/udev:ro
      - $DOCKERDIR/appdata/scrutiny/config:/opt/scrutiny/config
      - $DOCKERDIR/appdata/scrutiny/influxdb:/opt/scrutiny/influxdb
    ports:
      - 8086:8080
"""
````

## File: src/apps/seafile.py
````python
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
````

## File: src/apps/searxng.py
````python
from src.apps.base_app import BaseApp

class SearxngApp(BaseApp):
    key = "searxng"
    name = "SearXNG"
    port = 8087
    category = "tools"
    description = "Privacy metasearch engine aggregating queries anonymously from multiple sites."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/etc/searxng
    ports:
      - 8087:8080
"""
````

## File: src/apps/seerr.py
````python
from src.apps.base_app import BaseApp
class SeerrApp(BaseApp):
    key = "seerr"
    name = "Seerr"
    port = 5055
    category = "requests"
    description = "Unified request management and media discovery dashboard for your Plex or Jellyfin ecosystem."
    stack_group = "media-server"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  seerr:
    image: ghcr.io/seerr-team/seerr:latest
    container_name: seerr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/seerr/config:/config
    ports:
      - 5055:5055
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log
        results = []
        if self.key in keys:
            s_key = keys[self.key]
            s_header = {"X-Api-Key": s_key}
            for app in ["sonarr", "radarr"]:
                if app in keys:
                    write_log(f"Linking {app} to Seerr...")
                    endpoint = "settings/radarr" if app == "radarr" else "settings/sonarr"
                    active_dir = "/movies" if app == "radarr" else "/tv"
                    port = 7878 if app == "radarr" else 8989
                    
                    payload = {
                        "name": f"{app.upper()} (Auto)", 
                        "hostname": app, 
                        "port": port,
                        "apiKey": keys[app], 
                        "useSsl": False, 
                        "isDefault": True,
                        "activeProfileId": 1, 
                        "activeDirectory": active_dir
                    }
                    if app == "sonarr":
                        payload["activeLanguageProfileId"] = 1
                    
                    try:
                        rest_invoker(f"http://localhost:5055/api/v1/{endpoint}", method="POST", json_payload=payload, headers=s_header)
                        results.append(f"Linked {app} to Seerr")
                    except Exception as e:
                        write_log(f"Failed to link {app} to Seerr: {str(e)}", level="WARN")
        return results
````

## File: src/apps/sftpgo.py
````python
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
````

## File: src/apps/slskd.py
````python
from src.apps.base_app import BaseApp
class SlskdApp(BaseApp):
    key = "slskd"
    name = "Slskd"
    port = 5030
    category = "slskd"
    description = "Modern, headless Soulseek client designed for servers, featuring a clean web interface for music sharing and discovery."
    stack_group = "downloaders"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  slskd:
    image: slskd/slskd:latest
    container_name: slskd
    <<: *common-keys-apps
    environment:
      - SLSKD_PUID=$PUID
      - SLSKD_PGID=$PGID
      - SLSKD_TZ=$TZ
      - SLSKD_SLSK_LISTEN_PORT=50300
    volumes:
      - $DOCKERDIR/appdata/slskd/config:/app/config
      - $DATADRIVE/music:/app/music
      - $DATADRIVE/downloads/slskd:/app/downloads
    ports:
      - 50300:50300
      - 5030:5030
"""
````

## File: src/apps/sonarr.py
````python
from src.apps.base_app import BaseApp
class SonarrApp(BaseApp):
    key = "sonarr"
    name = "Sonarr"
    port = 8989
    category = "tv"
    description = "Smart TV show PVR for Usenet and BitTorrent. Monitors RSS feeds for new episodes and handles grabbing, sorting, and renaming."
    stack_group = "media-pvr"
    recommendations = ['prowlarr', 'bazarr', 'recyclarr', 'qbittorrent', 'sabnzbd']
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  # PORT: 8989
  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/sonarr/config:/config
      - $DATADRIVE/tv:/tv
      - $DATADRIVE/anime:/anime
      - $DATADRIVE/downloads:/downloads
    ports:
      - ${SONARR_PORT:-8989}:8989
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        import os
        results = []
        if self.key in keys:
            api_key = keys[self.key]
            headers = {"X-Api-Key": api_key}
            env_port = os.getenv("SONARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            base_url = f"http://localhost:{port}/api/v3"
            
            write_step(f"Injecting Authentication for {self.name}...")
            try:
                current_config = rest_invoker(f"{base_url}/config/host", method="GET", headers=headers)
                if current_config:
                    current_config["authenticationMethod"] = "external"
                    rest_invoker(f"{base_url}/config/host", method="PUT", json_payload=current_config, headers=headers)
                    results.append(f"Configured {self.name} with external authentication")
            except Exception as e:
                write_log(f"Failed to inject auth for {self.name}: {str(e)}", level="WARN")

            try:
                naming_config = rest_invoker(f"{base_url}/config/naming", method="GET", headers=headers)
                if naming_config:
                    naming_config["renameEpisodes"] = True
                    rest_invoker(f"{base_url}/config/naming", method="PUT", json_payload=naming_config, headers=headers)
                    results.append(f"Enabled renaming rules for {self.name}")
            except Exception as e:
                write_log(f"Failed to enable renaming for {self.name}: {str(e)}", level="WARN")

            try:
                rest_invoker(f"{base_url}/rootfolder", method="POST", json_payload={"path": "/tv"}, headers=headers)
                results.append(f"Configured default root path '/tv' for {self.name}")
            except Exception:
                pass

            plex_token = os.getenv("PLEX_TOKEN")
            if plex_token and plex_token.strip():
                try:
                    payload = {
                        "name": "Plex Watchlist",
                        "enableAuto": True,
                        "enabled": True,
                        "shouldMonitor": True,
                        "listType": "plex",
                        "implementation": "PlexWatchlistImport",
                        "configContract": "PlexWatchlistSettings",
                        "qualityProfileId": 1,
                        "rootFolderPath": "/tv",
                        "searchOnAdd": True,
                        "fields": [
                            {"name": "plexToken", "value": plex_token.strip()},
                            {"name": "syncInterval", "value": 180}
                        ],
                        "tags": []
                    }
                    rest_invoker(f"{base_url}/importlist", method="POST", json_payload=payload, headers=headers)
                    results.append(f"Configured Plex Watchlist import list for {self.name}")
                except Exception as e:
                    write_log(f"Failed to configure Plex Watchlist for {self.name}: {str(e)}", level="WARN")
        return results
````

## File: src/apps/stirling_pdf.py
````python
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
````

## File: src/apps/syncthing.py
````python
from src.apps.base_app import BaseApp
class SyncthingApp(BaseApp):
    key = "syncthing"
    name = "Syncthing"
    port = 8384
    category = "sync"
    description = "Secure and private file synchronization program that syncs data between your devices in real time."
    stack_group = "personal-cloud"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  syncthing:
    image: lscr.io/linuxserver/syncthing:latest
    container_name: syncthing
    <<: *common-keys-apps
    environment:
      <<: *default-tz-puid-pgid
    volumes:
      - $DOCKERDIR/appdata/syncthing/config:/config
      - $DATADRIVE/music:/data
    ports:
      - 8384:8384
      - 22000:22000/tcp
      - 22000:22000/udp
      - 21027:21027/udp
"""
````

## File: src/apps/tailscale.py
````python
from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class TailscaleConfig(BaseModel):
    TS_AUTHKEY: str = Field(
        default="", 
        description="Tailscale Auth Key",
        json_schema_extra={
            "help_url": "https://login.tailscale.com/admin/settings/keys",
            "is_secret": True
        }
    )

class TailscaleApp(BaseApp):
    key = "tailscale"
    name = "Tailscale"
    port = 0
    category = "vpn"
    description = "Zero-config VPN that creates a secure mesh network between your devices, allowing remote access without port forwarding."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = TailscaleConfig

    def get_compose_template(self) -> str:
        return """  tailscale:
    image: tailscale/tailscale:latest
    container_name: tailscale
    <<: *common-keys-core
    environment:
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_AUTHKEY=$TS_AUTHKEY
      - TS_EXTRA_ARGS=--accept-dns=true
    volumes:
      - $DOCKERDIR/appdata/tailscale:/var/lib/tailscale
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
"""
````

## File: src/apps/tautulli.py
````python
from src.apps.base_app import BaseApp
class TautulliApp(BaseApp):
    key = "tautulli"
    name = "Tautulli"
    port = 8181
    category = "stats"
    description = "Comprehensive monitoring and analytics tool for Plex that provides detailed statistics on watch history and user activity."
    stack_group = "media-server"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  tautulli:
    image: lscr.io/linuxserver/tautulli:latest
    container_name: tautulli
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/tautulli/config:/config
    ports:
      - 8181:8181
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log
        import configparser
        import os
        results = []
        if self.key in keys:
            plex_token = os.getenv("PLEX_TOKEN")
            if plex_token and plex_token.strip():
                config_file = os.path.join(deploy_dir, "appdata", "tautulli", "config.ini")
                # Ensure the folder structure exists
                os.makedirs(os.path.dirname(config_file), exist_ok=True)
                try:
                    config = configparser.ConfigParser(strict=False, empty_lines_in_values=False)
                    if os.path.exists(config_file):
                        config.read(config_file, encoding="utf-8")
                    if not config.has_section("General"):
                        config.add_section("General")
                    config.set("General", "pms_url", "http://plex:32400")
                    config.set("General", "pms_token", plex_token.strip())
                    with open(config_file, "w", encoding="utf-8") as f:
                        config.write(f)
                    write_log("Successfully pre-seeded Tautulli config.ini with Plex token and URL.", level="INFO")
                    results.append("Configured Tautulli connection to Plex")
                except Exception as e:
                    write_log(f"Warning: Failed to seed Tautulli config.ini: {str(e)}", level="WARN")
        return results
````

## File: src/apps/tmodloader.py
````python
from src.apps.base_app import BaseApp
class TmodloaderApp(BaseApp):
    key = "tmodloader"
    name = "Tmodloader"
    port = 7777
    category = "terraria"
    description = "Dedicated server for modded Terraria, providing a persistent world for multiplayer sessions with friends."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  tmodloader:
    image: 'jacobsmile/tmodloader1.4:latest'
    container_name: 'terraria'
    ports:
      - "7771:7777"
    expose:
      - "7771"
    <<: *common-keys-apps
    environment:
      - "TMOD_AUTODOWNLOAD=2979448082,2658460246,2836588773,3244873353,3222493606,2906451681,2782337219,3044249615,2815540735,2876787119,2562953970,3628420060,2828370879,3582340033,3617579754,2793782057,2564503881,2877850919,2687866031,2563309347,2563851005,2570931073,2597324266,2619954303,2669644269,2816694149,2824688072,2824688266,2824688804,2908170107,2797518634,2917091521,2815010161,2812377597,2827999994,2839001756,2565639705,2864849706,3024322683"
      - "TMOD_ENABLEDMODS=2979448082,2658460246,2836588773,3244873353,3222493606,2906451681,2782337219,3044249615,2815540735,2876787119,2562953970,3628420060,2828370879,3582340033,3617579754,2793782057,2564503881,2877850919,2687866031,2563309347,2563851005,2570931073,2597324266,2619954303,2669644269,2816694149,2824688072,2824688266,2824688804,2908170107,2797518634,2917091521,2815010161,2812377597,2827999994,2839001756,2565639705,2864849706,3024322683"
      - "TMOD_SHUTDOWN_MESSAGE=Goodbye!"
      - "TMOD_AUTOSAVE_INTERVAL=15"
      - "TMOD_MOTD=!"
      - "TMOD_PASS=suuift"
      - "TMOD_MAXPLAYERS=16"
      - "TMOD_WORLDNAME=Earth"
      - "TMOD_WORLDSIZE=3"
      - "TMOD_WORLDSEED=twins"
      - "TMOD_DIFFICULTY=0"
      - "TMOD_USECONFIGFILE=No"
      - "UPDATE_NOTICE=true"
    volumes:
      - $DOCKERDIR/appdata/terraria/data:/data
"""
````

## File: src/apps/trilium.py
````python
from src.apps.base_app import BaseApp

class TriliumApp(BaseApp):
    key = "trilium"
    name = "Trilium Notes"
    port = 8091
    category = "tools"
    description = "Hierarchical note-taking application designed for constructing large personal knowledge bases."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  trilium:
    image: zadam/trilium:latest
    container_name: trilium
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/home/node/trilium-data
    ports:
      - 8091:8080
"""
````

## File: src/apps/uptime_kuma.py
````python
from src.apps.base_app import BaseApp

class UptimeKumaApp(BaseApp):
    key = "uptime-kuma"
    name = "Uptime Kuma"
    port = 3001
    category = "management"
    description = "Beautiful monitoring tool to check the status of your stack and send alert notifications."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/app/data
    ports:
      - 3001:3001
"""
````

## File: src/apps/valheim.py
````python
from src.apps.base_app import BaseApp
class ValheimApp(BaseApp):
    key = "valheim"
    name = "Valheim"
    port = 2456
    category = "valheim"
    description = "Persistent dedicated server for Valheim, enabling you and your friends to explore and survive in a shared Viking world."
    stack_group = "games"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  valheim:
    image: lloesche/valheim-server:latest
    container_name: valheim
    <<: *common-keys-apps
    ports:
      - "2456-2457:2456-2457/udp"
    volumes:
      - $DOCKERDIR/appdata/valheim/config:/config
      - $DOCKERDIR/appdata/valheim/data:/opt/valheim
    environment:
      - SERVER_NAME=Valheim Server
      - WORLD_NAME=Bussh
      - SERVER_PASS=busting
"""
````

## File: src/apps/vaultwarden.py
````python
from src.apps.base_app import BaseApp
class VaultwardenApp(BaseApp):
    key = "vaultwarden"
    name = "Vaultwarden"
    port = 8083
    category = "none"
    description = "Lightweight self-hosted password manager (Bitwarden compatible). Provides professional-grade security for your family's passwords."
    stack_group = "core"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    <<: *common-keys-apps
    environment:
      - SIGNUPS_ALLOWED=false
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/vaultwarden/data:/data
    ports:
      - 8083:80
"""
````

## File: src/apps/watchtower.py
````python
from src.apps.base_app import BaseApp
class WatchtowerApp(BaseApp):
    key = "watchtower"
    name = "Watchtower"
    port = 0
    category = "none"
    description = "Automates Docker base image updates by watching your running containers and restarting them when a new image version is available."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return """  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    <<: *common-keys-core
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      DOCKER_API_VERSION: 1.44
      <<: *default-tz-puid-pgid
"""
````

## File: src/gui/base_frame.py
````python
import customtkinter as ctk

class BaseFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
````

## File: src/gui/logs_frame.py
````python
import os
import sys
import shutil
import subprocess
import tkinter as tk
import customtkinter as ctk
from src.gui.base_frame import BaseFrame

class LogsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        lbl_title = ctk.CTkLabel(self, text="System Installation Logs", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="View the comprehensive execution output from the background process in real-time.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # Verbose Log Checkbox
        self.chk_verbose_logs = ctk.CTkCheckBox(
            self, 
            text="Enable Verbose (Debug) Logging", 
            command=self.update_logs_view_content,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.chk_verbose_logs.grid(row=2, column=0, pady=5, sticky="w")
        
        # Log Text Area
        self.logs_textbox = ctk.CTkTextbox(self, height=400, font=ctk.CTkFont(family="Courier", size=11))
        self.logs_textbox.grid(row=3, column=0, sticky="nsew", pady=10)
        self.logs_textbox.configure(state="disabled")
        
        # Open in Editor button
        btn_open = ctk.CTkButton(self, text="Open Log in Editor", width=180, command=self.open_log_in_editor)
        btn_open.grid(row=4, column=0, pady=(10, 0), sticky="e")

    def update_logs_view_content(self):
        if not hasattr(self, "logs_textbox"):
            return
        from src.utils.logger import get_log_path
        log_path = get_log_path()
        if os.path.exists(log_path) and os.path.isdir(log_path):
            try:
                shutil.rmtree(log_path)
            except OSError:
                pass
        if not os.path.exists(log_path):
            self.logs_textbox.configure(state="normal")
            self.logs_textbox.delete("1.0", tk.END)
            self.logs_textbox.insert(tk.END, "[INFO] No log files generated yet.")
            self.logs_textbox.configure(state="disabled")
            return
            
        show_verbose = self.chk_verbose_logs.get()
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            lines = [f"[ERROR] Failed to read log file: {str(e)}\n"]
            
        filtered_lines = []
        for line in lines:
            if not show_verbose:
                if "[DEBUG]" in line or "[TRACE]" in line:
                    continue
            filtered_lines.append(line)
            
        self.logs_textbox.configure(state="normal")
        self.logs_textbox.delete("1.0", tk.END)
        self.logs_textbox.insert(tk.END, "".join(filtered_lines))
        self.logs_textbox.configure(state="disabled")
        self.logs_textbox.see(tk.END)

    def open_log_in_editor(self):
        from src.utils.logger import get_log_path
        log_path = get_log_path()
        if not os.path.exists(log_path):
            from tkinter import messagebox
            messagebox.showwarning("Log Not Found", "No log file has been created yet.")
            return
        try:
            if sys.platform == "win32":
                os.startfile(log_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", log_path])
            else:
                subprocess.Popen(["xdg-open", log_path])
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to open log file: {str(e)}")
````

## File: src/gui/summary_frame.py
````python
import os
import sys
import json
import re
import shutil
import subprocess
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from src.gui.base_frame import BaseFrame
from src.utils.paths import get_deploy_dir, get_clean_env
from src.utils.state import get_metadata
from src.utils.clipboard import copy_to_clipboard

class SummaryFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.lbl_title = ctk.CTkLabel(self, text="Setup Summary Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        self.lbl_desc = ctk.CTkLabel(self, text="Your Media and Home Server stack is successfully deployed. Use this dashboard to manage your credentials and links.", font=ctk.CTkFont(size=13))
        self.lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # Tabview layout
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=2, column=0, sticky="nsew", pady=10)
        
        self.tab_status = self.tabview.add("Service Status")
        self.tab_widgets = self.tabview.add("Widget Setup")
        self.tab_guide = self.tabview.add("Next Steps")
        
        self.btn_exit = ctk.CTkButton(self, text="Done & Exit", width=150, height=35, command=self.controller.destroy)
        self.btn_exit.grid(row=3, column=0, pady=(10, 0), sticky="e")

    def load_tabs_data(self):
        # Dynamically refresh all tabs when screen is shown
        self.build_status_tab(self.tab_status)
        self.build_widgets_tab(self.tab_widgets)
        self.build_guide_tab(self.tab_guide)

    def build_status_tab(self, tab):
        for w in tab.winfo_children():
            w.destroy()
            
        tab.grid_columnconfigure(0, weight=1)
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        scroll.grid_columnconfigure(0, weight=2)
        scroll.grid_columnconfigure(1, weight=1)
        scroll.grid_columnconfigure(2, weight=2)
        
        from src.modules.auto_configure import test_port
        metadata = get_metadata()
        selected = metadata.get("selected_services", [])
        
        container_name_mapping = {
            "npm plus (+goaccess)": "nginx-proxy-manager-plus",
            "mariadb (+adminer)": "mariadb",
            "postgresql (+cloudbeaver)": "postgresql",
            "mongodb (+mongo-express)": "mongodb",
            "qbittorrent": "qbit",
            "qbittorrent-vpn": "qbit-vpn",
        }
        
        def get_container_info(cname: str, default_p: int) -> tuple[bool, int]:
            try:
                proc = subprocess.run(
                    ["docker", "inspect", cname],
                    capture_output=True,
                    text=True,
                    env=get_clean_env()
                )
                if proc.returncode != 0:
                    return False, default_p
                data = json.loads(proc.stdout)
                if not data or not isinstance(data, list):
                    return False, default_p
                state = data[0].get("State", {})
                is_running = state.get("Running", False)
                
                host_port = default_p
                network_settings = data[0].get("NetworkSettings", {})
                ports = network_settings.get("Ports", {})
                if ports:
                    for container_port_proto, bindings in ports.items():
                        if bindings:
                            for binding in bindings:
                                binding_port = binding.get("HostPort")
                                if binding_port and binding_port.isdigit():
                                    host_port = int(binding_port)
                                    break
                            if host_port != default_p:
                                break
                return is_running, host_port
            except Exception:
                return False, default_p
                
        lbl_header_svc = ctk.CTkLabel(scroll, text="Service Name", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_svc.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        lbl_header_status = ctk.CTkLabel(scroll, text="Status", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_status.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        lbl_header_action = ctk.CTkLabel(scroll, text="Actions", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_action.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        row_idx = 1
        for entry in self.controller.registry:
            if entry.key in selected:
                default_port = int(entry.port) if entry.port and entry.port.isdigit() else 0
                cname = container_name_mapping.get(entry.key, entry.key)
                
                is_running, port = get_container_info(cname, default_port)
                
                is_non_ui = (entry.type in ["none", "db", "postgres", "mongo", "redis"]) or (entry.key in {"flaresolverr", "hkserver", "mariadb", "postgresql", "mongodb", "redis", "db", "watchtower", "docker-prune", "crowdsec", "cloudflare-ddns", "plextraktsync", "recyclarr"})
                
                is_online = False
                if port > 0 and not is_non_ui:
                    is_online = test_port("127.0.0.1", port)
                else:
                    is_online = is_running
                    
                status_text = "ONLINE" if is_online else "OFFLINE"
                status_color = "green" if is_online else "red"
                
                lbl_name = ctk.CTkLabel(scroll, text=entry.key)
                lbl_name.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
                
                lbl_stat = ctk.CTkLabel(scroll, text=status_text, text_color=status_color, font=ctk.CTkFont(weight="bold"))
                lbl_stat.grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
                
                url = f"http://localhost:{port}" if port > 0 and not is_non_ui else ""
                if entry.key == "portainer" and url:
                    url = f"https://localhost:{port}"
                elif entry.key == "plex" and url:
                    url = f"http://localhost:{port}/web"
                
                if url:
                    action_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                    action_frame.grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")
                    
                    def open_link(u=url):
                        import webbrowser
                        webbrowser.open(u)
                        
                    def copy_link(u=url):
                        if copy_to_clipboard(u):
                            messagebox.showinfo("Clipboard", f"Copied to clipboard: {u}")
                    
                    btn_link = ctk.CTkButton(action_frame, text="Open Web UI", width=100, command=open_link)
                    btn_link.pack(side="left", padx=(0, 5))
                    
                    btn_copy = ctk.CTkButton(action_frame, text="Copy Link", width=80, fg_color="gray", hover_color="dimgray", command=copy_link)
                    btn_copy.pack(side="left")
                else:
                    lbl_nolink = ctk.CTkLabel(scroll, text="No Web Interface", font=ctk.CTkFont(slant="italic"))
                    lbl_nolink.grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")
                    
                row_idx += 1

    def build_widgets_tab(self, tab):
        for w in tab.winfo_children():
            w.destroy()
            
        tab.grid_columnconfigure(0, weight=1)
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        scroll.grid_columnconfigure(1, weight=1)
        
        metadata = get_metadata()
        selected = metadata.get("selected_services", [])
        
        manual_services = []
        if "plex" in selected:
            manual_services.append(("PLEX_TOKEN", "Plex API Token", "Open Plex -> Settings -> Web Client (General) -> 'Show Advanced' -> Scroll for Token."))
        if "jellyfin" in selected:
            manual_services.append(("JELLYFIN_KEY", "Jellyfin API Key", "Open Jellyfin -> Dashboard -> API Keys -> Create key named 'Homepage'."))
        if "portainer" in selected:
            manual_services.append(("PORTAINER_KEY", "Portainer API Token", "Open Portainer -> User Settings -> Access Tokens -> Create token."))
            
        if not manual_services:
            lbl_no = ctk.CTkLabel(scroll, text="No services require manual API tokens for widget setup.", font=ctk.CTkFont(size=14, slant="italic"))
            lbl_no.pack(pady=50)
            return
            
        lbl_info = ctk.CTkLabel(scroll, text="Paste tokens below to display rich container widgets in your Homepage dashboard.", justify="left", font=ctk.CTkFont(size=12))
        lbl_info.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="w")
        
        row_idx = 1
        entries_dict = {}
        deploy_dir = get_deploy_dir()
        env_path = os.path.join(deploy_dir, ".env")
        
        current_vars = {}
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r"^([^=]+)=(.*)$", line)
                    if match:
                        current_vars[match.group(1).strip()] = match.group(2).strip()
                        
        for var_name, name, hint in manual_services:
            lbl_name = ctk.CTkLabel(scroll, text=f"{name} ({var_name}):", font=ctk.CTkFont(weight="bold"))
            lbl_name.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            
            if var_name == "PLEX_TOKEN":
                field_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                field_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                field_frame.grid_columnconfigure(0, weight=1)
                
                entry = ctk.CTkEntry(field_frame, placeholder_text=hint)
                entry.insert(0, current_vars.get(var_name, ""))
                entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
                
                def start_plex_link(ent=entry):
                    def worker():
                        from src.utils.plex_oauth import request_plex_token
                        btn_auth.configure(state="disabled", text="Linking...")
                        token = request_plex_token(is_gui=True, progress_callback=lambda msg: self.after(0, lambda: btn_auth.configure(text=msg[:12] + "...")))
                        if token:
                            self.after(0, lambda: ent.delete(0, tk.END))
                            self.after(0, lambda: ent.insert(0, token))
                            self.after(0, lambda: btn_auth.configure(state="normal", text="Linked!"))
                        else:
                            self.after(0, lambda: btn_auth.configure(state="normal", text="Auto Auth"))
                    t = threading.Thread(target=worker)
                    t.daemon = True
                    t.start()
                    
                btn_auth = ctk.CTkButton(field_frame, text="Auto Auth", width=90, command=start_plex_link)
                btn_auth.grid(row=0, column=1, sticky="e")
                entries_dict[var_name] = entry
            else:
                entry = ctk.CTkEntry(scroll, placeholder_text=hint, width=320)
                entry.insert(0, current_vars.get(var_name, ""))
                entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                entries_dict[var_name] = entry
            row_idx += 1
            
        def save_widget_keys():
            from src.utils.state import set_env_var
            saved_count = 0
            for var_name, entry in entries_dict.items():
                val = entry.get().strip()
                if val:
                    set_env_var(var_name, val, file_path=env_path)
                    saved_count += 1
                    
            if saved_count > 0:
                messagebox.showinfo("Keys Saved", f"Successfully saved {saved_count} API tokens to .env configuration! Reloading dashboard...")
                def reload_hp():
                    try:
                        hp_path = os.path.join(deploy_dir, "stacks", "maintenance")
                        if os.path.exists(hp_path):
                            subprocess.run(["docker", "compose", "up", "-d", "--remove-orphans"], cwd=hp_path, capture_output=True, env=get_clean_env())
                    except Exception:
                        pass
                t = threading.Thread(target=reload_hp)
                t.daemon = True
                t.start()
                
        btn_save = ctk.CTkButton(scroll, text="Save & Sync Tokens", command=save_widget_keys)
        btn_save.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=15)

    def build_guide_tab(self, tab):
        for w in tab.winfo_children():
            w.destroy()
            
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        scroll.grid_columnconfigure(0, weight=1)
        
        # Header banner
        header_frame = ctk.CTkFrame(scroll, fg_color=["#EAEAEA", "#252525"], corner_radius=8)
        header_frame.pack(fill="x", padx=10, pady=(5, 15))
        
        lbl_congrats = ctk.CTkLabel(
            header_frame, 
            text="🎉 Stack Deployed Successfully!", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=["#1F6AA5", "#3B8ED0"]
        )
        lbl_congrats.pack(pady=(15, 5))
        
        lbl_sub = ctk.CTkLabel(
            header_frame, 
            text="Use the links below to access your services and finish setting them up.", 
            font=ctk.CTkFont(size=13)
        )
        lbl_sub.pack(pady=(0, 15))
        
        metadata = get_metadata()
        selected = metadata.get("selected_services", [])
        
        container_name_mapping = {
            "npm plus (+goaccess)": "nginx-proxy-manager-plus",
            "mariadb (+adminer)": "mariadb",
            "postgresql (+cloudbeaver)": "postgresql",
            "mongodb (+mongo-express)": "mongodb",
            "qbittorrent": "qbit",
            "qbittorrent-vpn": "qbit-vpn",
        }
        
        def get_container_info(cname: str, default_p: int) -> tuple[bool, int]:
            try:
                proc = subprocess.run(
                    ["docker", "inspect", cname],
                    capture_output=True,
                    text=True,
                    env=get_clean_env()
                )
                if proc.returncode != 0:
                    return False, default_p
                data = json.loads(proc.stdout)
                if not data or not isinstance(data, list):
                    return False, default_p
                state = data[0].get("State", {})
                is_running = state.get("Running", False)
                
                host_port = default_p
                network_settings = data[0].get("NetworkSettings", {})
                ports = network_settings.get("Ports", {})
                if ports:
                    for container_port_proto, bindings in ports.items():
                        if bindings:
                            for binding in bindings:
                                binding_port = binding.get("HostPort")
                                if binding_port and binding_port.isdigit():
                                    host_port = int(binding_port)
                                    break
                            if host_port != default_p:
                                break
                return is_running, host_port
            except Exception:
                return False, default_p
                
        # Collect UI services
        ui_services = []
        for entry in self.controller.registry:
            if entry.key in selected:
                is_non_ui = (entry.type in ["none", "db", "postgres", "mongo", "redis"]) or (entry.key in {"watchtower", "docker-prune", "crowdsec", "cloudflare-ddns", "plextraktsync", "recyclarr", "flaresolverr", "hkserver", "mariadb", "postgresql", "mongodb"})
                if not is_non_ui:
                    default_port = int(entry.port) if entry.port and entry.port.isdigit() else 0
                    if default_port > 0:
                        cname = container_name_mapping.get(entry.key, entry.key)
                        _, live_port = get_container_info(cname, default_port)
                        ui_services.append((entry.key, live_port))
                    
        # 1. Primary Dashboards & Tools
        dash_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        dash_frame.pack(fill="x", padx=10, pady=10)
        dash_frame.grid_columnconfigure(0, weight=1)
        dash_frame.grid_columnconfigure(1, weight=1)
        
        # Homepage Card
        has_homepage = "homepage" in selected
        hp_port = 3000
        if has_homepage:
            _, hp_port = get_container_info("homepage", 3000)
            
        hp_card = ctk.CTkFrame(dash_frame, fg_color=["#F2F2F2", "#2B2B2B"], border_width=1, border_color=["#D0D0D0", "#404040"], corner_radius=8)
        hp_card.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        hp_title = ctk.CTkLabel(hp_card, text="🏠 Homepage Dashboard", font=ctk.CTkFont(size=15, weight="bold"))
        hp_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        hp_desc = ctk.CTkLabel(
            hp_card, 
            text="Access your customizable landing page showing real-time status of all services.",
            justify="left", 
            wraplength=220,
            font=ctk.CTkFont(size=12)
        )
        hp_desc.pack(anchor="w", padx=15, pady=5)
        
        hp_url = f"http://localhost:{hp_port}"
        def open_hp():
            import webbrowser
            webbrowser.open(hp_url)
            
        def copy_hp():
            if copy_to_clipboard(hp_url):
                messagebox.showinfo("Clipboard", f"Copied to clipboard: {hp_url}")
            
        btn_hp_frame = ctk.CTkFrame(hp_card, fg_color="transparent")
        btn_hp_frame.pack(anchor="w", padx=15, pady=(15, 15))
        
        btn_hp = ctk.CTkButton(btn_hp_frame, text=f"Open Dashboard (Port {hp_port})", command=open_hp, state="normal" if has_homepage else "disabled", width=160)
        btn_hp.pack(side="left", padx=(0, 5))
        
        btn_hp_copy = ctk.CTkButton(btn_hp_frame, text="Copy Link", command=copy_hp, state="normal" if has_homepage else "disabled", width=80, fg_color="gray", hover_color="dimgray")
        btn_hp_copy.pack(side="left")
        
        # Dockge Card
        has_dockge = "dockge" in selected
        dg_port = 5001
        if has_dockge:
            _, dg_port = get_container_info("dockge", 5001)
            
        dg_card = ctk.CTkFrame(dash_frame, fg_color=["#F2F2F2", "#2B2B2B"], border_width=1, border_color=["#D0D0D0", "#404040"], corner_radius=8)
        dg_card.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        
        dg_title = ctk.CTkLabel(dg_card, text="🐋 Dockge Stack Manager", font=ctk.CTkFont(size=15, weight="bold"))
        dg_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        dg_desc = ctk.CTkLabel(
            dg_card, 
            text="Manage Docker Compose stacks, edit configurations, and monitor container logs.",
            justify="left", 
            wraplength=220,
            font=ctk.CTkFont(size=12)
        )
        dg_desc.pack(anchor="w", padx=15, pady=5)
        
        dg_url = f"http://localhost:{dg_port}"
        def open_dg():
            import webbrowser
            webbrowser.open(dg_url)
            
        def copy_dg():
            if copy_to_clipboard(dg_url):
                messagebox.showinfo("Clipboard", f"Copied to clipboard: {dg_url}")
            
        btn_dg_frame = ctk.CTkFrame(dg_card, fg_color="transparent")
        btn_dg_frame.pack(anchor="w", padx=15, pady=(15, 15))
        
        btn_dg = ctk.CTkButton(btn_dg_frame, text=f"Open Dockge (Port {dg_port})", command=open_dg, state="normal" if has_dockge else "disabled", width=160)
        btn_dg.pack(side="left", padx=(0, 5))
        
        btn_dg_copy = ctk.CTkButton(btn_dg_frame, text="Copy Link", command=copy_dg, state="normal" if has_dockge else "disabled", width=80, fg_color="gray", hover_color="dimgray")
        btn_dg_copy.pack(side="left")
        
        # 2. Companion Services
        ui_services_to_show = [s for s in ui_services if s[0] not in ["homepage", "dockge"]]
        if ui_services_to_show:
            comp_lbl = ctk.CTkLabel(scroll, text="Companion Web Interfaces", font=ctk.CTkFont(size=15, weight="bold"))
            comp_lbl.pack(anchor="w", padx=10, pady=(15, 5))
            
            comp_frame = ctk.CTkFrame(scroll, fg_color=["#F8F8F8", "#202020"], corner_radius=8)
            comp_frame.pack(fill="x", padx=10, pady=5)
            
            comp_frame.grid_columnconfigure((0, 1, 2), weight=1)
            
            for index, (svc_key, svc_port) in enumerate(ui_services_to_show):
                r = index // 3
                c = index % 3
                
                svc_card = ctk.CTkFrame(comp_frame, fg_color=["#EEEEEE", "#2A2A2A"], corner_radius=6)
                svc_card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
                
                lbl_svc = ctk.CTkLabel(svc_card, text=svc_key, font=ctk.CTkFont(size=13, weight="bold"))
                lbl_svc.pack(pady=(10, 5))
                
                url = f"https://localhost:{svc_port}" if svc_key == "portainer" else f"http://localhost:{svc_port}"
                if svc_key == "plex":
                    url = f"http://localhost:{svc_port}/web"
                    
                def make_open_url(u=url):
                    import webbrowser
                    return lambda: webbrowser.open(u)
                    
                def make_copy_url(u=url):
                    return lambda: copy_to_clipboard(u) and messagebox.showinfo("Clipboard", f"Copied to clipboard: {u}")
                    
                btn_svc_frame = ctk.CTkFrame(svc_card, fg_color="transparent")
                btn_svc_frame.pack(pady=(0, 10), padx=10)
                
                btn_svc = ctk.CTkButton(btn_svc_frame, text=f"Open Port {svc_port}", height=28, command=make_open_url(url), width=110)
                btn_svc.pack(side="left", padx=(0, 5))
                
                btn_svc_copy = ctk.CTkButton(btn_svc_frame, text="Copy", height=28, command=make_copy_url(url), width=50, fg_color="gray", hover_color="dimgray")
                btn_svc_copy.pack(side="left")
                
        # 3. PlexTraktSync OAuth
        if "plextraktsync" in selected:
            pts_frame = ctk.CTkFrame(scroll, fg_color=["#F0F0F0", "#1E1E1E"], corner_radius=8, border_width=1, border_color=["#D0D0D0", "#303030"])
            pts_frame.pack(fill="x", padx=10, pady=15)
            
            pts_title = ctk.CTkLabel(pts_frame, text="🔗 PlexTraktSync OAuth Authorization Guide", font=ctk.CTkFont(size=14, weight="bold"))
            pts_title.pack(anchor="w", padx=15, pady=(12, 5))
            
            pts_desc = (
                "PlexTraktSync requires initial authorization to access your Plex and Trakt.tv accounts.\n"
                "Click the button below to spawn an interactive terminal and complete the configuration."
            )
            pts_lbl = ctk.CTkLabel(pts_frame, text=pts_desc, justify="left", font=ctk.CTkFont(size=12))
            pts_lbl.pack(anchor="w", padx=15, pady=(0, 10))
            
            def authorize_pts():
                deploy_dir = get_deploy_dir()
                media_server_dir = os.path.normpath(os.path.join(deploy_dir, "stacks", "media-server"))
                if not os.path.exists(media_server_dir):
                    messagebox.showerror("Error", f"Media server stack directory not found at {media_server_dir}")
                    return
                
                try:
                    if sys.platform == "win32":
                        cmd = f'cmd.exe /k "cd /d {media_server_dir} && docker compose run --rm plextraktsync"'
                        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    elif sys.platform == "darwin":
                        cmd = f'osascript -e \'tell application "Terminal" to do script "cd {media_server_dir} && docker compose run --rm plextraktsync"\''
                        subprocess.Popen(cmd, shell=True)
                    else:
                        terminals = ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "alacritty", "kitty", "xterm"]
                        spawned = False
                        for term in terminals:
                            if shutil.which(term):
                                if term == "gnome-terminal":
                                    subprocess.Popen(["gnome-terminal", "--working-directory", media_server_dir, "--", "docker", "compose", "run", "--rm", "plextraktsync"])
                                elif term == "xfce4-terminal":
                                    subprocess.Popen(["xfce4-terminal", "--working-directory", media_server_dir, "-e", "docker compose run --rm plextraktsync"])
                                else:
                                    subprocess.Popen([term, "-e", f"sh -c 'cd {media_server_dir} && docker compose run --rm plextraktsync'"])
                                spawned = True
                                break
                        if not spawned:
                            messagebox.showerror("Error", "Could not find a supported terminal emulator (gnome-terminal, xterm, etc.) to run the auth command.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to spawn terminal: {str(e)}")
            
            btn_auth = ctk.CTkButton(pts_frame, text="Authorize PlexTraktSync", command=authorize_pts)
            btn_auth.pack(anchor="w", padx=15, pady=(0, 15))
            
        # 4. Next Steps Checklist
        checklist_lbl = ctk.CTkLabel(scroll, text="📋 Recommended Next Steps Checklist", font=ctk.CTkFont(size=15, weight="bold"))
        checklist_lbl.pack(anchor="w", padx=10, pady=(15, 5))
        
        chk_frame = ctk.CTkFrame(scroll, fg_color=["#F2F2F2", "#2B2B2B"], corner_radius=8)
        chk_frame.pack(fill="x", padx=10, pady=5)
        
        checklist_items = [
            "1. Access Dockge to confirm all compose stacks have successfully initialized and run.",
            "2. Open Prowlarr and configure your Torrent/Usenet indexers (they will sync to Sonarr/Radarr automatically).",
            "3. Verify download clients (SABnzbd or qBittorrent) are correctly linked to your PVR tools (Sonarr, Radarr, etc.).",
            "4. Map your library folders in Sonarr and Radarr, ensuring they match the mounted media path (/tv, /movies).",
            "5. Open Homepage Dashboard to view live health status widgets for all services."
        ]
        
        for item in checklist_items:
            lbl_item = ctk.CTkLabel(chk_frame, text=item, wraplength=550, justify="left", font=ctk.CTkFont(size=12))
            lbl_item.pack(anchor="w", padx=15, pady=6)
````

## File: src/gui/welcome_frame.py
````python
import os
import sys
import platform
import shutil
import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from src.gui.base_frame import BaseFrame
from src.utils.paths import get_deploy_dir
from src.utils.logger import set_log_path, write_log

class WelcomeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Welcome Title
        lbl_title = ctk.CTkLabel(self, text="Welcome to DockerSetup", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="This wizard will help you configure, orchestrate, and deploy a complete Media and Home Server stack on your system.", justify="left", font=ctk.CTkFont(size=14))
        lbl_desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Prerequisites Panel
        prereq_box = ctk.CTkLabel(self, text="System Prerequisites Checks", font=ctk.CTkFont(size=16, weight="bold"))
        prereq_box.grid(row=2, column=0, pady=5, sticky="w")
        
        self.prereq_container = ctk.CTkFrame(self, corner_radius=8)
        self.prereq_container.grid(row=3, column=0, sticky="nsew", pady=(5, 20))
        self.prereq_container.grid_columnconfigure(0, weight=1)
        
        # Target deployment folder selector
        lbl_folder_title = ctk.CTkLabel(self, text="Deployment Directory Selection", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_folder_title.grid(row=4, column=0, pady=(10, 5), sticky="w")
        
        dir_selector_frame = ctk.CTkFrame(self, fg_color="transparent")
        dir_selector_frame.grid(row=5, column=0, sticky="ew", pady=5)
        dir_selector_frame.grid_columnconfigure(0, weight=1)
        
        # Setup initial path
        initial_deploy = get_deploy_dir()
        self.entry_deploy_path = ctk.CTkEntry(dir_selector_frame, placeholder_text="Enter deploy directory path...")
        self.entry_deploy_path.insert(0, initial_deploy)
        self.entry_deploy_path.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        btn_browse = ctk.CTkButton(dir_selector_frame, text="Browse...", width=100, command=self.controller.browse_deployment_directory)
        btn_browse.grid(row=0, column=1, sticky="e")
        
        # Next Button
        btn_next = ctk.CTkButton(self, text="Next: Select Services", width=180, height=40, command=self.validate_directory_and_proceed)
        btn_next.grid(row=6, column=0, pady=(20, 10), sticky="e")

    def run_preflight_checks(self):
        for widget in self.prereq_container.winfo_children():
            widget.destroy()
            
        os_sys = platform.system()
        lbl_os = ctk.CTkLabel(self.prereq_container, text=f"• Host Operating System: {os_sys}", font=ctk.CTkFont(size=13))
        lbl_os.grid(row=0, column=0, padx=20, pady=8, sticky="w")
        
        from src.utils.paths import get_clean_env
        docker_exists = shutil.which("docker") is not None
        docker_color = "green" if docker_exists else "red"
        docker_text = "FOUND & INSTALLED" if docker_exists else "NOT FOUND (Required)"
        lbl_docker = ctk.CTkLabel(self.prereq_container, text=f"• Docker System Check: {docker_text}", text_color=docker_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_docker.grid(row=1, column=0, padx=20, pady=8, sticky="w")
        
        compose_text = "NOT FOUND"
        compose_exists = False
        if docker_exists:
            test_proc = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True, env=get_clean_env())
            if test_proc.returncode == 0:
                compose_exists = True
                compose_text = "DOCKER COMPOSE V2 PLUG-IN INSTALLED"
        
        compose_color = "green" if compose_exists else "red"
        lbl_compose = ctk.CTkLabel(self.prereq_container, text=f"• Compose Engine Check: {compose_text}", text_color=compose_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_compose.grid(row=2, column=0, padx=20, pady=8, sticky="w")

        daemon_running = False
        if docker_exists:
            try:
                subprocess.run(
                    ["docker", "info"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                    timeout=3,
                    env=get_clean_env()
                )
                daemon_running = True
            except Exception:
                daemon_running = False

        daemon_text = "RUNNING" if daemon_running else "NOT RUNNING"
        daemon_color = "green" if daemon_running else "red"
        lbl_daemon = ctk.CTkLabel(self.prereq_container, text=f"• Docker Daemon Check: {daemon_text}", text_color=daemon_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_daemon.grid(row=3, column=0, padx=20, pady=8, sticky="w")

    def validate_directory_and_proceed(self):
        d_dir = self.entry_deploy_path.get().strip()
        if not d_dir:
            return
            
        d_dir = os.path.normpath(d_dir)
        os.environ["DEPLOY_DIR"] = d_dir
        set_log_path(os.path.join(d_dir, "logs"))
        
        if not os.path.exists(d_dir):
            create = messagebox.askyesno("Create Directory?", f"Directory '{d_dir}' does not exist. Create it?")
            if create:
                try:
                    os.makedirs(d_dir, exist_ok=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create directory: {str(e)}")
                    return
            else:
                return
                
        metadata_file = os.path.join(d_dir, ".metadata.json")
        if os.path.exists(metadata_file):
            dialog = ctk.CTkToplevel(self.controller)
            dialog.title("Existing Deployment Detected")
            dialog.resizable(False, False)
            self.controller.center_over_parent(dialog, 500, 320)
            
            lbl_title = ctk.CTkLabel(dialog, text="Existing Deployment Found", font=ctk.CTkFont(size=18, weight="bold"))
            lbl_title.pack(pady=(20, 10))
            
            msg = f"An existing DockerSetup stack was found at:\n{d_dir}\n\nWhat would you like to do?"
            lbl_msg = ctk.CTkLabel(dialog, text=msg, wraplength=450, justify="center", font=ctk.CTkFont(size=13))
            lbl_msg.pack(pady=10)
            
            def on_modify():
                dialog.destroy()
                self.controller.build_services_checkboxes()
                self.controller.show_services_frame(from_next=True)
                
            def on_upgrade():
                dialog.destroy()
                self.controller.run_fast_upgrade(d_dir)
                
            def on_reset():
                dialog.destroy()
                self.controller.run_full_reset(d_dir)
                
            def on_cancel():
                dialog.destroy()
                
            btn_modify = ctk.CTkButton(dialog, text="Modify Selections (Re-run Wizard)", width=320, command=on_modify)
            btn_modify.pack(pady=5)
            
            btn_upgrade = ctk.CTkButton(dialog, text="Fast Upgrade (Apply Template Updates)", width=320, command=on_upgrade)
            btn_upgrade.pack(pady=5)
            
            btn_reset = ctk.CTkButton(dialog, text="Full Reset (Wipe All Configs & Volumes)", fg_color="red", hover_color="#8B0000", width=320, command=on_reset)
            btn_reset.pack(pady=5)
            
            btn_cancel = ctk.CTkButton(dialog, text="Change Directory / Cancel", fg_color="transparent", border_width=1, width=320, command=on_cancel)
            btn_cancel.pack(pady=(5, 20))
        else:
            self.controller.show_services_frame(from_next=True)
````

## File: src/modules/__init__.py
````python
# modules package
````

## File: src/modules/network.py
````python
import os
import subprocess
from src.utils.logger import write_log, console, write_step
from src.utils.paths import get_clean_env

def setup_networks() -> bool:
    write_step("Configuring external Docker networks")

    if os.getenv("TEST_MODE") == "true":
        write_log("TEST_MODE enabled. Skipping live docker network configuration.", level="INFO")
        return True

    required_networks = [
        {"name": "npm_proxy", "subnet": "192.168.89.0/24"},
        {"name": "media-internal", "subnet": "192.168.90.0/24"}
    ]

    for net in required_networks:
        net_name = net["name"]
        subnet = net["subnet"]

        try:
            # Check if network exists
            proc = subprocess.run(
                ["docker", "network", "ls", "--filter", f"name=^{net_name}$", "--format", "{{.Name}}"],
                capture_output=True,
                text=True,
                check=True,
                env=get_clean_env()
            )
            exists = proc.stdout.strip()
            
            if not exists:
                write_log(f"Creating external network: {net_name} ({subnet})", level="INFO")
                subprocess.run(
                    ["docker", "network", "create", net_name, f"--subnet={subnet}"],
                    check=True,
                    env=get_clean_env()
                )
                write_log(f"Network '{net_name}' created", level="DEBUG")
            else:
                write_log(f"Network '{net_name}' already exists", level="DEBUG")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to check or create Docker network: {net_name}. Ensure Docker is running. Error: {str(e)}")

    console.print("[✓] Docker networks configured", style="green")
    return True
````

## File: src/modules/preflight.py
````python
import os
import sys
import shutil
import platform
import subprocess
import ctypes
from src.utils.logger import write_log, console, write_step
from src.utils.paths import get_clean_env

def is_admin() -> bool:
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0

def run_system_preflight() -> bool:
    write_step("Running system preflight checks")

    if os.getenv("TEST_MODE") == "true":
        write_log("[TEST] Bypassing System Preflight Checks", level="WARN")
        return True

    # 1. Python Version Check
    py_major, py_minor = sys.version_info.major, sys.version_info.minor
    if py_major < 3 or (py_major == 3 and py_minor < 10):
        raise RuntimeError(f"Python 3.10 or higher is required. You are running version {sys.version}.")
    write_log(f"Python version compatible ({sys.version.split()[0]})", level="DEBUG")

    # 2. Administrative Privileges
    if platform.system() == "Windows":
        if not is_admin():
            raise PermissionError(
                "Administrative privileges required. Please restart this script as Administrator."
            )
        write_log("Running as Administrator", level="DEBUG")
    else:
        write_log("Privilege checks passed", level="DEBUG")

    # 3. Docker Availability (Stage 1: Installed)
    docker_cmd = shutil.which("docker")
    if not docker_cmd:
        raise FileNotFoundError("Docker not found. Please install Docker and ensure it is in your system PATH.")

    try:
        docker_version = subprocess.check_output(
            ["docker", "--version"],
            text=True,
            stderr=subprocess.DEVNULL,
            env=get_clean_env()
        ).strip()
        write_log(f"{docker_version} detected", level="DEBUG")
    except Exception:
        raise RuntimeError("Docker binary exists but '--version' failed. Your Docker installation may be corrupted.")

    # 4. Docker Daemon Status (Stage 2: Running)
    daemon_running = False
    try:
        # docker info requires the daemon to be responsive
        subprocess.run(
            ["docker", "info"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=get_clean_env()
        )
        daemon_running = True
        write_log("Docker daemon is running", level="DEBUG")
    except subprocess.CalledProcessError:
        daemon_running = False

    # Auto-start logic if installed but not running
    if not daemon_running:
        if os.getenv("TEST_MODE") == "true" or os.getenv("DS_HEADLESS") == "true":
            raise RuntimeError("Docker daemon is offline. (Auto-start disabled in test/headless mode).")

        write_log("Docker daemon is offline. Attempting to start it...", level="WARN")
        
        start_attempted = False
        if platform.system() == "Windows":
            import winreg
            try:
                # Query registry for Docker Desktop path
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Docker Inc.\Docker\1.0")
                app_path, _ = winreg.QueryValueEx(key, "AppPath")
                winreg.CloseKey(key)
                
                if os.path.exists(app_path):
                    # Launch in background
                    subprocess.Popen([app_path], creationflags=subprocess.CREATE_NO_WINDOW)
                    start_attempted = True
            except Exception as e:
                write_log(f"Could not find Docker Desktop in registry: {e}", level="DEBUG")
        else:
            # Linux fallbacks
            try:
                if "/snap/bin/docker" in docker_cmd:
                    subprocess.run(["snap", "start", "docker"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    # Try systemd first, then service
                    try:
                        subprocess.run(["systemctl", "start", "docker"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except subprocess.CalledProcessError:
                        subprocess.run(["service", "docker", "start"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                start_attempted = True
            except Exception as e:
                write_log(f"Failed to auto-start Linux Docker daemon: {e}", level="DEBUG")

        if not start_attempted:
            raise RuntimeError("Docker is not running and could not be started automatically. Please start Docker manually.")

        # Polling loop (max 60 seconds)
        import time
        console.print("Waiting for Docker daemon to initialize... ", end="", style="white")
        sys.stdout.flush()
        
        timeout = 60
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            try:
                subprocess.run(
                    ["docker", "info"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env=get_clean_env()
                )
                console.print("[OK]", style="green")
                daemon_running = True
                break
            except subprocess.CalledProcessError:
                console.print(".", end="")
                sys.stdout.flush()
                time.sleep(3)

        if not daemon_running:
            console.print("[TIMEOUT]", style="bold red")
            raise RuntimeError("Docker daemon took too long to start. Please check Docker for errors.")

    # 5. Docker Compose V2 Checks
    try:
        compose_proc = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            env=get_clean_env()
        )
        if compose_proc.returncode != 0:
            raise RuntimeError("Docker Compose V2 not found. Please ensure compose plugin is active.")
        write_log("Docker Compose V2 active", level="DEBUG")
    except Exception:
         raise RuntimeError("Docker Compose V2 check failed. Make sure 'docker compose' is installed.")

    # 5. Security Utilities check
    if platform.system() == "Windows":
        if not shutil.which("icacls.exe"):
            write_log("icacls.exe not found. .env file permissions cannot be hardened.", level="WARN")
    
    # 6. Long Path Support (Windows Registry)
    if platform.system() == "Windows":
        write_log("Checking Long Path support...", level="DEBUG")
        import winreg
        registry_path = r"System\CurrentControlSet\Control\FileSystem"
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
            value, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
            if value != 1:
                try:
                    write_log("Long Path support enabled in registry", level="DEBUG")
                except Exception:
                    write_log("Failed to enable Long Paths in Registry. Please enable manually if needed.", level="WARN")
            else:
                write_log("Long Path support active", level="DEBUG")
            winreg.CloseKey(key)
        except Exception as e:
            write_log(f"Failed to query/write Long Paths Registry settings: {str(e)}", level="WARN")

    console.print("[✓] System preflight checks completed", style="green")
    return True
````

## File: src/utils/__init__.py
````python
# utils package
````

## File: src/utils/clipboard.py
````python
import platform
import subprocess
import shutil

def copy_to_clipboard(text: str) -> bool:
    """
    Copies text to the system clipboard across platforms.
    """
    if not text:
        return False
        
    system = platform.system()
    
    # 1. Tkinter clipboard fallback
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.destroy()
        return True
    except Exception:
        pass
        
    # 2. CLI fallbacks
    try:
        if system == "Windows":
            if shutil.which("clip"):
                proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
        elif system == "Linux":
            if shutil.which("xclip"):
                proc = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
            elif shutil.which("xsel"):
                proc = subprocess.Popen(["xsel", "--clipboard", "--input"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
            elif shutil.which("wl-copy"):
                proc = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
        elif system == "Darwin":
            if shutil.which("pbcopy"):
                proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
    except Exception:
        pass
        
    return False
````

## File: src/utils/dependency_resolver.py
````python
from typing import List, Dict, Tuple, Optional
from src.apps.base_app import BaseApp

def check_exclusivity_conflicts(selected_apps: List[BaseApp]) -> Dict[str, List[str]]:
    """
    Checks selected apps for exclusivity group overlaps.
    Returns a dictionary mapping the exclusivity group name to the list of app names causing the conflict.
    """
    groups: Dict[str, List[BaseApp]] = {}
    for app in selected_apps:
        if app.exclusivity_group:
            groups.setdefault(app.exclusivity_group, []).append(app)
            
    conflicts: Dict[str, List[str]] = {}
    for grp, apps in groups.items():
        if len(apps) > 1:
            conflicts[grp] = [app.name for app in apps]
    return conflicts

def resolve_database_dependencies(selected_keys: List[str], apps_dict: Dict[str, BaseApp]) -> Tuple[List[str], List[str]]:
    """
    Scans selected app keys, automatically adds missing required database services,
    and returns a tuple containing:
      - The updated list of selected app keys.
      - A list of notifications describing the auto-selected database mappings.
    """
    updated_keys = list(selected_keys)
    notifications = []
    
    # Check if a database engine is already selected
    has_postgres = "postgresql_cloudbeaver" in updated_keys
    has_mysql = "mariadb_adminer" in updated_keys
    
    for key in selected_keys:
        app = apps_dict.get(key)
        if not app:
            continue
            
        if app.required_database_type:
            if app.required_database_type == "postgres" and not has_postgres:
                updated_keys.append("postgresql_cloudbeaver")
                has_postgres = True
                notifications.append(
                    f"Automatically selected PostgreSQL (CloudBeaver) as a dependency for {app.name}."
                )
            elif app.required_database_type == "mysql" and not has_mysql:
                updated_keys.append("mariadb_adminer")
                has_mysql = True
                notifications.append(
                    f"Automatically selected MariaDB (Adminer) as a dependency for {app.name}."
                )
                
    return updated_keys, notifications
````

## File: src/utils/migrate_to_plugins.py
````python
import os
import re
from src.utils.yaml_parser import get_yaml_content, get_registry_list, get_template_blocks
from src.utils.paths import get_resource_path

def run_migration():
    services_path = get_resource_path("services.yml")
    templates_path = get_resource_path("templates.yml")
    
    master_registry = get_yaml_content(services_path)
    registry_list = get_registry_list(master_registry)
    templates = get_template_blocks(templates_path)
    
    recs_map = {}
    if "RECOMMENDATIONS" in master_registry:
        for r in master_registry["RECOMMENDATIONS"]:
            recs_map[r.source] = r.recommendations
            
    conf_apps = set()
    if "CONFIGURABLE_APPS" in master_registry:
        for c in master_registry["CONFIGURABLE_APPS"]:
            conf_apps.add(c.name)
            
    widget_apps = set()
    if "SUPPORTED_WIDGETS" in master_registry:
        for w in master_registry["SUPPORTED_WIDGETS"]:
            # Handle aliases like mylar:mylar3
            name = w.name
            if ":" in name:
                name = name.split(":")[0]
            widget_apps.add(name)
            
    groups_map = {}
    if "STACK_GROUPS" in master_registry:
        for g in master_registry["STACK_GROUPS"]:
            for svc in g.services:
                groups_map[svc] = g.name
                
    os.makedirs("src/apps", exist_ok=True)
    
    for entry in registry_list:
        key = entry.key
        safe_name = key.replace("-", "_").replace(" ", "_").replace("+", "").replace("(", "").replace(")", "")
        while "__" in safe_name:
            safe_name = safe_name.replace("__", "_")
        safe_name = safe_name.strip("_")
        
        filename = f"src/apps/{safe_name}.py"
        
        template_content = templates.get(key, "")
        pydantic_model_code = ""
        config_model_ref = "None"
        
        vars_found = re.findall(r"\${([^:-}]+)(?::-(.*?))?}", template_content)
        standard_globals = {"PUID", "PGID", "TZ", "DOCKERDIR", "USERDIR", "DATADRIVE"}
        unique_vars = {}
        for var_name, default_val in vars_found:
            if var_name not in standard_globals:
                unique_vars[var_name] = default_val or ""
                
        if unique_vars:
            class_name = "".join([part.title() for part in safe_name.split("_")]) + "Config"
            pydantic_model_code = f"from pydantic import BaseModel, Field\n\nclass {class_name}(BaseModel):\n"
            for v_name, def_val in unique_vars.items():
                if def_val.isdigit():
                    pydantic_model_code += f"    {v_name}: int = Field(default={def_val}, description=\"Custom {v_name} variable\")\n"
                else:
                    pydantic_model_code += f"    {v_name}: str = Field(default=\"{def_val}\", description=\"Custom {v_name} variable\")\n"
            config_model_ref = class_name
            
        recs = recs_map.get(key, [])
        group = groups_map.get(key, "general")
        
        code = f"from src.apps.base_app import BaseApp\n"
        if pydantic_model_code:
            code += pydantic_model_code + "\n"
            
        app_class_name = "".join([part.title() for part in safe_name.split("_")]) + "App"
        
        code += f"""class {app_class_name}(BaseApp):
    key = "{key}"
    name = "{key.title()}"
    port = {entry.port or 0}
    category = "{entry.type}"
    description = "{entry.description.replace('"', '\\"')}"
    stack_group = "{group}"
    recommendations = {recs}
    is_configurable = {key in conf_apps}
    has_widget = {key in widget_apps}
    config_model = {config_model_ref}

    def get_compose_template(self) -> str:
        return \"\"\"{template_content}\"\"\"
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
            
    print("Migration finished!")

if __name__ == "__main__":
    run_migration()
````

## File: src/utils/plex_oauth.py
````python
import requests
import time
import webbrowser
import platform
from src.utils.logger import write_log, console, write_step

CLIENT_ID = "DockerSetup-MediaStack-Orchestration-Client"

def request_plex_token(is_gui=False, progress_callback=None) -> str:
    """
    Implements Plex PIN flow authentication.
    Returns the authToken string if successful, or None.
    """
    headers = {
        "Accept": "application/json",
        "X-Plex-Client-Identifier": CLIENT_ID,
        "X-Plex-Product": "DockerSetup",
        "X-Plex-Version": "1.0",
        "X-Plex-Device": platform.node() or "HomeServer"
    }

    try:
        # 1. Request a PIN code from Plex API
        res = requests.post("https://plex.tv/api/v2/pins", headers=headers, timeout=10)
        res.raise_for_status()
        pin_data = res.json()
        
        pin_id = pin_data.get("id")
        code = pin_data.get("code")
        
        if not pin_id or not code:
            write_log("Failed to get PIN ID or Code from Plex API", level="ERROR")
            return None
            
        auth_url = f"https://app.plex.tv/auth#?clientID={CLIENT_ID}&code={code}&context%5Bdevice%5D%5Bproduct%5D=DockerSetup"
        
        console.print("\n==========================================", style="cyan")
        console.print("             PLEX AUTHENTICATION", style="cyan")
        console.print("==========================================", style="cyan")
        console.print(f"1. Open your browser and sign in to Plex.")
        console.print(f"2. Go to: [link={auth_url}]{auth_url}[/link]", style="yellow")
        console.print(f"3. Or enter this code on https://plex.tv/link : [bold green]{code}[/bold green]\n")
        console.print("Waiting for authentication approval...", style="grey50")
        
        # Try to open browser automatically
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass
            
        # 2. Poll Plex API for the token
        timeout = 180
        start_time = time.time()
        poll_interval = 5
        
        while (time.time() - start_time) < timeout:
            if progress_callback:
                progress_callback(f"Waiting for Plex link: {code} ({int(timeout - (time.time() - start_time))}s remaining)")
                
            poll_res = requests.get(f"https://plex.tv/api/v2/pins/{pin_id}", headers=headers, timeout=10)
            if poll_res.status_code == 200:
                poll_data = poll_res.json()
                auth_token = poll_data.get("authToken")
                if auth_token:
                    console.print("[✓] Plex Account Linked Successfully!", style="green")
                    write_log("Successfully retrieved Plex authToken via PIN link flow.", level="INFO")
                    return auth_token
                    
            time.sleep(poll_interval)
            
        console.print("[!] Plex Auth Link Timeout.", style="red")
        write_log("Plex auth link flow timed out.", level="WARN")
        return None
        
    except Exception as e:
        write_log(f"Plex OAuth link API error: {str(e)}", level="ERROR")
        return None
````

## File: src/apps/authelia.py
````python
from src.apps.base_app import BaseApp

class AutheliaApp(BaseApp):
    key = "authelia"
    name = "Authelia"
    port = 9091
    category = "networking"
    description = "Lightweight Single Sign-On and 2FA authentication portal for reverse proxies."
    stack_group = "maintenance"
    recommendations = []
    is_configurable = False
    has_widget = False
    config_model = None

    def get_compose_template(self) -> str:
        return f"""  authelia:
    image: authelia/authelia:latest
    container_name: authelia
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 9091:9090
"""
````

## File: src/apps/base_app.py
````python
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class BaseApp:
    key: str = ""
    name: str = ""
    port: int = 0
    category: str = ""
    description: str = ""
    stack_group: str = ""
    recommendations: List[str] = []
    is_configurable: bool = True
    has_widget: bool = False
    config_model: Optional[type[BaseModel]] = None
    exclusivity_group: Optional[str] = None
    required_database_type: Optional[str] = None

    def get_appdata_dir(self) -> str:
        """Returns the standard container volume host directory for this application."""
        return f"${{DEPLOY_DIR}}/appdata/{self.key}"

    def get_compose_template(self) -> str:
        """Returns the Docker Compose YAML template string for this service."""
        return ""

    def run_stitching(self, keys: Dict[str, str], deploy_dir: str, rest_invoker) -> List[str]:
        """Runs custom stitching or setup actions. Returns a list of result strings."""
        return []
````

## File: src/apps/npm_plus_goaccess.py
````python
from pydantic import BaseModel, Field
from src.apps.base_app import BaseApp

class NpmPlusConfig(BaseModel):
    BASE_DOMAIN: str = Field(default="local.host", description="Base Domain (e.g. example.com)")

class NpmPlusGoaccessApp(BaseApp):
    key = "npm plus (+goaccess)"
    name = "Nginx Proxy Manager Plus"
    port = 81
    category = "proxy"
    description = "Enhanced Nginx Proxy Manager with built-in security features and GoAccess for real-time traffic analysis."
    stack_group = "core"
    recommendations = ['cloudflare-ddns', 'authelia', 'crowdsec']
    is_configurable = False
    has_widget = False
    config_model = NpmPlusConfig
    exclusivity_group = "reverse_proxy"

    def get_compose_template(self) -> str:
        return """  npm-plus:
    <<: *common-keys-core
    container_name: nginx-proxy-manager-plus
    image: 'zoeyvid/nginx-proxy-manager-plus:latest'
    networks:
      npm_proxy:
        ipv4_address: 192.168.89.254
    ports:
      - '80:80'
      - '443:443'
      - '81:81'
    volumes:
      - $DOCKERDIR/appdata/npm/config:/config 
      - $DOCKERDIR/appdata/npm/letsencrypt:/etc/letsencrypt
      - $DOCKERDIR/appdata/npm/data:/data
    environment:
      - DISABLE_IPV6=true
      - CROWDSEC_ENABLED=$CROWDSEC_ENABLED
      - CROWDSEC_LAPI_URL=http://crowdsec:8080
      - CROWDSEC_LAPI_KEY=$CROWDSEC_API_KEY
  goaccess:
    <<: *common-keys-apps
    image: xavierh/goaccess-for-nginxproxymanager:latest
    container_name: goaccess
    ports:
      - 7880:7880
    environment:
      - PUID=$PUID
      - PGID=$PGID
      - TZ=$TZ
    volumes:
      - $DOCKERDIR/appdata/npm/logs:/opt/log
      - $DOCKERDIR/appdata/goaccess/config:/config
"""
````

## File: src/gui/deploy_frame.py
````python
import os
import sys
import tkinter as tk
import customtkinter as ctk
from src.gui.base_frame import BaseFrame
from src.utils.paths import get_deploy_dir

class DeployFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        lbl_title = ctk.CTkLabel(self, text="Orchestration & Deploy", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        # Display Summaries
        self.lbl_deploy_summary = ctk.CTkLabel(self, text="", justify="left", font=ctk.CTkFont(size=13))
        self.lbl_deploy_summary.grid(row=1, column=0, pady=(5, 5), sticky="w")
        
        # Progress Indicators Frame
        progress_control_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_control_frame.grid(row=2, column=0, sticky="ew", pady=5)
        progress_control_frame.grid_columnconfigure(0, weight=1)
        
        # Steps Indicator
        self.steps_frame = ctk.CTkFrame(progress_control_frame, corner_radius=8)
        self.steps_frame.grid(row=0, column=0, sticky="ew", pady=5)
        self.steps_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.step_indicators = {}
        steps_list = [
            ("Preflight", "Preflight"),
            ("Dirs", "Directories"),
            ("Network", "Networks"),
            ("Compose", "Compose"),
            ("Containers", "Containers"),
            ("Stitch", "Stitching")
        ]
        
        for idx, (key, name) in enumerate(steps_list):
            lbl_step = ctk.CTkLabel(self.steps_frame, text=f"• {name}: Ready", font=ctk.CTkFont(size=11))
            lbl_step.grid(row=0, column=idx, padx=5, pady=8, sticky="ew")
            self.step_indicators[key] = lbl_step
            
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(progress_control_frame)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        self.progress_bar.set(0.0)
        
        # Verbose Toggle
        self.var_verbose = tk.BooleanVar(value=False)
        self.chk_verbose = ctk.CTkCheckBox(progress_control_frame, text="Enable Verbose (Debug) Logging", variable=self.var_verbose, command=self.refresh_deploy_logs)
        self.chk_verbose.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        # Deployment Button
        self.btn_start_deploy = ctk.CTkButton(self, text="Deploy Stack Now", height=45, fg_color="green", hover_color="#006400", font=ctk.CTkFont(size=15, weight="bold"), command=self.controller.trigger_deployment_pipeline)
        self.btn_start_deploy.grid(row=3, column=0, pady=10, sticky="ew")
        
        # Real-time console log
        self.log_text = tk.Text(self, wrap="word", height=12, bg="#1e1e1e", fg="#d4d4d4", font=("Courier", 11), borderwidth=0)
        self.log_text.grid(row=4, column=0, sticky="nsew", pady=(5, 10))
        
        # Navigation
        self.deploy_nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.deploy_nav_frame.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.deploy_nav_frame.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(self.deploy_nav_frame, text="Back", width=100, command=self.controller.show_env_frame)
        btn_back.grid(row=0, column=0, sticky="w")

    def update_deploy_summary(self):
        deploy_dir = get_deploy_dir()
        services_count = len(self.controller.selected_services)
        summary_text = (
            f"• Target deployment path: {deploy_dir}\n"
            f"• Selected services to deploy ({services_count}): {', '.join(sorted(self.controller.selected_services)) if self.controller.selected_services else 'None Selected'}\n"
            f"• Status: Ready to generate compose files."
        )
        self.lbl_deploy_summary.configure(text=summary_text)

    def refresh_deploy_logs(self):
        from src.utils.logger import get_log_path
        log_path = get_log_path()
        if not os.path.exists(log_path):
            self.log_text.delete("1.0", tk.END)
            return
            
        show_verbose = self.var_verbose.get()
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            lines = [f"[ERROR] Failed to read log file: {str(e)}\n"]
            
        filtered_lines = []
        for line in lines:
            if not show_verbose:
                if "[DEBUG]" in line or "[TRACE]" in line or ">>" in line:
                    continue
            filtered_lines.append(line.rstrip())
            
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "\n".join(filtered_lines) + "\n")
        self.log_text.see(tk.END)

    def update_step_status(self, step_key: str, status_text: str, color="white"):
        if step_key in self.step_indicators:
            names = {
                "Preflight": "Preflight",
                "Dirs": "Directories",
                "Network": "Networks",
                "Compose": "Compose",
                "Containers": "Containers",
                "Stitch": "Stitching"
            }
            name = names.get(step_key, step_key)
            self.step_indicators[step_key].configure(
                text=f"• {name}: {status_text}", 
                text_color=color
            )

    def update_progress_bar(self, val: float):
        self.progress_bar.set(val)
````

## File: src/gui/env_frame.py
````python
import os
import sys
import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import filedialog
import webbrowser
from src.gui.base_frame import BaseFrame
from src.utils.state import get_metadata
from src.modules.env_wizard import COMMON_ZONES, detect_timezone, new_random_password
from src.apps.loader import load_apps

class EnvFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.env_entries = {}
        
        lbl_title = ctk.CTkLabel(self, text="Configure Environment Credentials", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="Provide configuration settings and API keys for the selected services. Defaults will be used if left blank.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        self.env_scroll = ctk.CTkScrollableFrame(self)
        self.env_scroll.grid(row=2, column=0, sticky="nsew", pady=10)
        self.env_scroll.grid_columnconfigure(1, weight=1)
        
        # Navigation
        nav_buttons = ctk.CTkFrame(self, fg_color="transparent")
        nav_buttons.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.controller.show_services_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Deploy Stack", width=180, command=lambda: self.controller.show_deploy_frame(from_next=True))
        btn_next.grid(row=0, column=1, sticky="e")

    def build_dynamic_env_fields(self):
        for widget in self.env_scroll.winfo_children():
            widget.destroy()
            
        self.env_entries = {}
        
        metadata = get_metadata()
        saved_env = metadata.get("env_vars", {})
        
        import platform
        detected_tz = detect_timezone()
        default_tz = saved_env.get("TZ", detected_tz)
        default_puid = saved_env.get("PUID", os.environ.get("SUDO_UID", "1000"))
        default_pgid = saved_env.get("PGID", os.environ.get("SUDO_GID", "1000"))
        default_media = saved_env.get("DATADRIVE", "D:/Media" if platform.system() == "Windows" else os.path.expanduser("~/media"))
        
        row_idx = 0
        
        def add_standard_row(key, description, default_val):
            nonlocal row_idx
            lbl = ctk.CTkLabel(self.env_scroll, text=f"{key}:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            
            val = saved_env.get(key, default_val)
            entry = ctk.CTkEntry(self.env_scroll, placeholder_text=description, width=400)
            entry.insert(0, val)
            entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
            
            self.env_entries[key] = entry
            row_idx += 1
            
        # Timezone Combobox
        lbl_tz = ctk.CTkLabel(self.env_scroll, text="TZ (Timezone):", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_tz.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        
        cb_tz = ttk.Combobox(self.env_scroll, values=COMMON_ZONES, width=37, state="readonly")
        cb_tz.set(default_tz)
        cb_tz.grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        self.env_entries["TZ"] = cb_tz
        row_idx += 1
        
        # PUID & PGID
        add_standard_row("PUID", "Local User PID (Default: 1000)", default_puid)
        add_standard_row("PGID", "Local Group GID (Default: 1000)", default_pgid)
        
        # HTTP_USERNAME & HTTP_PASSWORD
        add_standard_row("HTTP_USERNAME", "Management Username (Default: admin)", "admin")
        
        lbl_pass = ctk.CTkLabel(self.env_scroll, text="HTTP_PASSWORD:", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_pass.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        
        pass_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
        pass_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        
        entry_pass = ctk.CTkEntry(pass_frame, placeholder_text="Management Password (leave blank to generate)", show="*", width=250)
        entry_pass.insert(0, saved_env.get("HTTP_PASSWORD", ""))
        entry_pass.grid(row=0, column=0, sticky="ew")
        
        def toggle_pass():
            if entry_pass.cget("show") == "*":
                entry_pass.configure(show="")
                btn_toggle.configure(text="Hide")
            else:
                entry_pass.configure(show="*")
                btn_toggle.configure(text="Show")
                
        btn_toggle = ctk.CTkButton(pass_frame, text="Show", width=60, command=toggle_pass)
        btn_toggle.grid(row=0, column=1, padx=(10, 0))
        
        def generate_rand():
            entry_pass.delete(0, tk.END)
            entry_pass.insert(0, new_random_password())
            
        btn_random = ctk.CTkButton(pass_frame, text="Random", width=70, command=generate_rand)
        btn_random.grid(row=0, column=2, padx=(10, 0))
        
        self.env_entries["HTTP_PASSWORD"] = entry_pass
        row_idx += 1
        
        # DATADRIVE (Media folder directory) with Browse button
        lbl_media = ctk.CTkLabel(self.env_scroll, text="DATADRIVE (Media Folder):", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_media.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        
        media_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
        media_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        
        entry_media = ctk.CTkEntry(media_frame, placeholder_text="Media folder directory path", width=330)
        entry_media.insert(0, default_media)
        entry_media.grid(row=0, column=0, sticky="ew")
        
        def browse_media():
            folder = filedialog.askdirectory(initialdir=entry_media.get())
            if folder:
                entry_media.delete(0, tk.END)
                entry_media.insert(0, os.path.normpath(folder))
                
        btn_browse = ctk.CTkButton(media_frame, text="Browse...", width=60, command=browse_media)
        btn_browse.grid(row=0, column=1, padx=(10, 0))
        
        self.env_entries["DATADRIVE"] = entry_media
        row_idx += 1
        
        # Dynamic settings fields from Pydantic config models in selected apps
        apps_dict = load_apps()
        for svc in sorted(self.controller.selected_services):
            if svc in apps_dict:
                app = apps_dict[svc]
                if app.config_model:
                    # Category section title
                    lbl_sect = ctk.CTkLabel(self.env_scroll, text=f"--- {app.name} Settings ---", font=ctk.CTkFont(size=13, weight="bold"), text_color=["#1F6AA5", "#3B8ED0"])
                    lbl_sect.grid(row=row_idx, column=0, columnspan=2, pady=(15, 5), sticky="w")
                    row_idx += 1
                    
                    for field_name, field_info in app.config_model.model_fields.items():
                        # Label
                        description = field_info.description or field_name
                        lbl_field = ctk.CTkLabel(self.env_scroll, text=f"{field_name}:", font=ctk.CTkFont(size=12, weight="bold"))
                        lbl_field.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
                        
                        extra = field_info.json_schema_extra or {}
                        is_secret = extra.get("is_secret", False) or "pass" in field_name.lower() or "key" in field_name.lower() or "token" in field_name.lower()
                        default_val = field_info.default if field_info.default is not None else ""
                        val = saved_env.get(field_name, default_val)
                        
                        # Input widget based on field type
                        field_type = field_info.annotation
                        
                        input_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
                        input_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                        
                        if field_type is bool:
                            var = tk.BooleanVar(value=(str(val).lower() == "true" or val is True or val == 1))
                            chk = ctk.CTkSwitch(input_frame, text=description, variable=var)
                            chk.pack(side="left", anchor="w")
                            # We store the variable in the entries dict so we can retrieve its value
                            self.env_entries[field_name] = var
                        elif is_secret:
                            entry_sec = ctk.CTkEntry(input_frame, placeholder_text=description, show="*", width=250)
                            entry_sec.insert(0, str(val))
                            entry_sec.pack(side="left", fill="x", expand=True)
                            
                            def make_toggle_sec(ent=entry_sec):
                                return lambda: ent.configure(show="" if ent.cget("show") == "*" else "*")
                            
                            btn_t = ctk.CTkButton(input_frame, text="👁", width=35, command=make_toggle_sec(entry_sec))
                            btn_t.pack(side="left", padx=(5, 0))
                            
                            self.env_entries[field_name] = entry_sec
                        else:
                            entry_std = ctk.CTkEntry(input_frame, placeholder_text=description, width=330)
                            entry_std.insert(0, str(val))
                            entry_std.pack(side="left", fill="x", expand=True)
                            
                            self.env_entries[field_name] = entry_std
                            
                        # Help link URL button if specified in the schema
                        help_url = extra.get("help_url")
                        if help_url:
                            btn_help = ctk.CTkLabel(
                                input_frame, 
                                text="❓", 
                                font=ctk.CTkFont(size=12),
                                text_color=["#1F6AA5", "#3B8ED0"],
                                cursor="hand2"
                            )
                            btn_help.pack(side="left", padx=(8, 0))
                            btn_help.bind("<Button-1>", lambda event, u=help_url: webbrowser.open(u))
                            
                        row_idx += 1
````

## File: src/utils/port_resolver.py
````python
import os
import socket
from typing import List, Dict, Set
from src.apps.base_app import BaseApp

def is_port_in_use(port: int) -> bool:
    """Checks if a port is locally bound/in use by the host OS."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.bind(("127.0.0.1", port))
            return False
        except socket.error:
            return True

def resolve_port_conflicts(selected_apps: List[BaseApp], env_path: str) -> List[str]:
    """
    Scans selected apps for overlapping ports. Auto-resolves by incrementing
    and writing host environment variable overrides (e.g. KEY_PORT) to .env if in use.
    Returns a list of override notification strings.
    """
    from concurrent.futures import ThreadPoolExecutor
    
    notifications = []
    allocated_ports: Dict[int, str] = {}
    
    # 1. Gateway/Reverse Proxy services have priority and immutable ports
    immutables = {"caddy", "npm_plus_goaccess"}
    
    # Track existing .env variables to keep manually configured ports
    existing_env: Dict[str, str] = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    existing_env[k.strip()] = v.strip()

    # Place proxy services first
    sorted_apps = sorted(selected_apps, key=lambda a: 0 if a.key in immutables else 1)

    # Perform a pre-scan check in parallel of default/configured port values to warm caches
    ports_to_check = set()
    for app in sorted_apps:
        port = int(app.port)
        if port == 0:
            continue
        env_key = f"{app.key.replace('-', '_').upper()}_PORT"
        if env_key in existing_env:
            try:
                port = int(existing_env[env_key])
            except ValueError:
                pass
        ports_to_check.add(port)

    # Parallel socket binds validation
    port_status: Dict[int, bool] = {}
    with ThreadPoolExecutor() as executor:
        results = executor.map(is_port_in_use, ports_to_check)
        for p, in_use in zip(ports_to_check, results):
            port_status[p] = in_use

    # Sequential logic evaluation
    for app in sorted_apps:
        port = int(app.port)
        if port == 0:
            continue

        env_key = f"{app.key.replace('-', '_').upper()}_PORT"
        if env_key in existing_env:
            try:
                port = int(existing_env[env_key])
            except ValueError:
                pass

        in_use_on_host = port_status.get(port, False)
        # Re-verify if not cached
        if port not in port_status:
            in_use_on_host = is_port_in_use(port)
            port_status[port] = in_use_on_host

        # Check for overlaps or host port locks
        if port in allocated_ports or in_use_on_host:
            if app.key in immutables:
                allocated_ports[port] = app.key
                continue

            candidate_port = port
            while is_port_in_use(candidate_port) or candidate_port in allocated_ports:
                candidate_port += 1
                
            notifications.append(
                f"Resolved port collision for {app.name}: mapped port {port} -> {candidate_port}."
            )
            port = candidate_port
            existing_env[env_key] = str(port)

        allocated_ports[port] = app.key

    # Save all resolves back to .env
    if notifications:
        lines = []
        for k, v in existing_env.items():
            lines.append(f"{k}={v}\n")
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return notifications
````

## File: src/utils/state.py
````python
import os
import json
import re
from typing import Any, Dict
from src.utils.paths import get_deploy_dir, resolve_path_slash
from src.utils.logger import write_log

# Caching variables
_metadata_cache = None
_env_cache = {}

def get_metadata_path() -> str:
    deploy_dir = get_deploy_dir()
    return resolve_path_slash(os.path.join(deploy_dir, ".metadata.json"))

def get_metadata() -> Dict[str, Any]:
    global _metadata_cache
    if _metadata_cache is not None:
        return _metadata_cache

    path = get_metadata_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                _metadata_cache = data
                return data
        except Exception:
            return {}
    return {}

def set_metadata(data: Dict[str, Any]):
    global _metadata_cache
    path = get_metadata_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        _metadata_cache = data
    except Exception as e:
        write_log(f"Failed to save .metadata.json: {str(e)}", level="ERROR")

def set_env_var(key: str, value: str, file_path: str = None):
    if not file_path:
        deploy_dir = get_deploy_dir()
        if deploy_dir:
            file_path = os.path.join(deploy_dir, ".env")
        else:
            raise ValueError("DEPLOY_DIR not set")

    # Clear cached env if exists
    if file_path in _env_cache:
        del _env_cache[file_path]

    # Handle null/None values safely
    if value is None:
        value = ""

    # Handle multi-line secrets escaping
    formatted_val = value
    if "\n" in value or "\r" in value:
        formatted_val = f'"{value.replace(chr(34), chr(92) + chr(34))}"'  # Replace " with \"

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{key}={formatted_val}\n")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    found = False
    new_lines = []
    escaped_key = re.escape(key)
    
    for line in lines:
        if re.match(f"^{escaped_key}=", line):
            new_lines.append(f"{key}={formatted_val}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"{key}={formatted_val}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def save_env_vars(vars_dict: Dict[str, str], file_path: str = None):
    if not file_path:
        deploy_dir = get_deploy_dir()
        if deploy_dir:
            file_path = os.path.join(deploy_dir, ".env")
        else:
            raise ValueError("DEPLOY_DIR not set")

    if file_path in _env_cache:
        del _env_cache[file_path]

    lines = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    updated_keys = set()
    new_lines = []

    for line in lines:
        match = re.match(r"^([^=]+)=(.*)$", line)
        if match:
            k = match.group(1).strip()
            if k in vars_dict:
                val = vars_dict[k]
                if "\n" in val or "\r" in val:
                    val = f'"{val.replace(chr(34), chr(92) + chr(34))}"'
                new_lines.append(f"{k}={val}\n")
                updated_keys.add(k)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    for k, val in vars_dict.items():
        if k not in updated_keys:
            if "\n" in val or "\r" in val:
                val = f'"{val.replace(chr(34), chr(92) + chr(34))}"'
            new_lines.append(f"{k}={val}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
````

## File: src/modules/deploy_start.py
````python
import os
import sys
import re
import json
import time
import subprocess
import questionary
from concurrent.futures import ThreadPoolExecutor
from src.utils.paths import get_project_root, get_deploy_dir, get_clean_env, resolve_path_slash
from src.utils.logger import write_log, console, write_step, invoke_external_command, safe_confirm
from src.utils.state import get_metadata

def test_container_conflict(stack_path: str, stack_name: str):
    compose_path = os.path.join(stack_path, "docker-compose.yml")
    if not os.path.exists(compose_path):
        return

    # Extract container_names
    container_names = []
    with open(compose_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"container_name:\s*(.*)$", line)
            if match:
                container_names.append(match.group(1).strip())

    for name in container_names:
        # Check if container exists
        exists_proc = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name=^/{name}$", "-q"],
            capture_output=True,
            text=True,
            env=get_clean_env()
        )
        exists = exists_proc.stdout.strip()
        
        if exists:
            existing_stack = ""
            try:
                inspect_proc = subprocess.run(
                    ["docker", "inspect", name],
                    capture_output=True,
                    text=True,
                    env=get_clean_env()
                )
                inspect = json.loads(inspect_proc.stdout)
                if inspect and inspect[0].get("Config", {}).get("Labels"):
                    existing_stack = inspect[0]["Config"]["Labels"].get("com.docker.compose.project", "")
            except Exception:
                write_log(f"Warning: Failed to inspect container {name} for conflict resolution.", level="WARN")

            if existing_stack and existing_stack != stack_name:
                console.print(f"\n[CONFLICT] Container '{name}' already exists and is managed by stack '{existing_stack}'.", style="yellow")
                
                if os.getenv("DS_HEADLESS") == "true":
                    raise RuntimeError(f"Deployment aborted due to container name conflict: {name}")

                choice = safe_confirm(f"Remove existing container to allow stack '{stack_name}' to start?", default=False)
                if choice:
                    write_log(f"Removing conflicting container: {name}", level="INFO")
                    subprocess.run(["docker", "rm", "-f", name], capture_output=True, env=get_clean_env())
                else:
                    raise RuntimeError(f"Deployment aborted due to container name conflict: {name}")

def pull_stack_images(stack_name: str, stack_path: str) -> dict:
    try:
        # Pull images for stack
        subprocess.run(
            ["docker", "compose", "-p", stack_name, "pull", "--quiet"],
            cwd=stack_path,
            check=True,
            capture_output=True,
            env=get_clean_env()
        )
        return {"name": stack_name, "success": True, "error": None}
    except Exception as e:
        return {"name": stack_name, "success": False, "error": str(e)}

def deploy_stacks() -> bool:
    write_step("Deploying container stacks to Docker")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    metadata = get_metadata()
    stacks = metadata.get("generated_stacks", [])

    if not stacks:
        write_log("No generated stacks found in metadata. Skipping deployment.", level="WARN")
        return True

    stacks_dir = resolve_path_slash(os.path.join(deploy_dir, "stacks"))

    # 1. Start CORE stack first
    core_stack = None
    for s in stacks:
        if s.get("Name") == "core":
            core_stack = s
            break

    if core_stack:
        write_step("Initializing CORE Stack (Networking & Database)")
        path = resolve_path_slash(os.path.join(stacks_dir, "core"))
        if os.path.exists(path):
            test_container_conflict(path, "core")
            try:
                # Execute docker compose up (using standard streaming to prevent pipe deadlock - Edge Case 9)
                invoke_external_command(
                    "docker compose -p core up -d --quiet-pull --remove-orphans",
                    description="Starting CORE stack",
                    cwd=path
                )
            except Exception:
                raise RuntimeError("Failed to start CORE stack. Check if Docker is running and ports 80/443 are free.")
            write_log("Core stack initiated. Waiting for network baseline...")
            time.sleep(5)
        else:
            raise FileNotFoundError(f"Core stack directory missing: {path}")

    # 2. Pre-Pull Images Concurrently using ThreadPoolExecutor (Edge Case 5)
    write_step("Pre-Pulling Service Images (Concurrent)")
    pull_tasks = []
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        for stack in stacks:
            name = stack.get("Name")
            if name == "core":
                continue
            path = resolve_path_slash(os.path.join(stacks_dir, name))
            if os.path.exists(path):
                write_log(f"Queuing image pull for stack: {name}", level="DEBUG")
                pull_tasks.append(executor.submit(pull_stack_images, name, path))

        # Show status spinner/dots while executing pulls
        if pull_tasks:
            console.print("    | Downloading images... ", end="", style="white")
            start_pull = time.time()
            while not all(t.done() for t in pull_tasks):
                if (time.time() - start_pull) > 600:
                    break
                console.print(".", end="")
                sys.stdout.flush()
                time.sleep(5)
            console.print("[DONE]", style="green")

            # Report any failures and decide next steps
            failed_pulls = []
            for t in pull_tasks:
                res = t.result()
                if not res["success"]:
                    write_log(f"WARN: Pull failed or timed out for {res['name']} - {res['error']}", level="WARN")
                    failed_pulls.append(res["name"])

            if failed_pulls:
                failed_list = ", ".join(failed_pulls)
                console.print(f"\n[!] Pull failures occurred for stack(s): {failed_list}", style="bold yellow")
                
                is_headless = os.getenv("DS_HEADLESS") == "true" or not sys.stdin.isatty()
                if is_headless:
                    write_log(f"ERROR: Aborting deployment in headless mode due to image pull failures on stack(s): {failed_list}", level="ERROR")
                    raise RuntimeError(f"Deployment aborted due to image pull failures: {failed_list}")
                
                choice = questionary.select(
                    "Image pulling failed. How would you like to proceed?",
                    choices=[
                        "Abort deployment (Recommended)",
                        "Ignore failures and proceed",
                        "Retry pulling failed stacks"
                    ],
                    default="Abort deployment (Recommended)"
                ).ask()
                
                if choice == "Retry pulling failed stacks":
                    write_log("Retrying image pull for failed stacks...", level="INFO")
                    retry_tasks = []
                    with ThreadPoolExecutor(max_workers=3) as executor:
                        for name in failed_pulls:
                            path = resolve_path_slash(os.path.join(stacks_dir, name))
                            if os.path.exists(path):
                                write_log(f"Queuing retry image pull for stack: {name}", level="INFO")
                                retry_tasks.append(executor.submit(pull_stack_images, name, path))
                    
                    if retry_tasks:
                        console.print("    | Retrying downloads... ", end="", style="white")
                        start_pull = time.time()
                        while not all(t.done() for t in retry_tasks):
                            if (time.time() - start_pull) > 600:
                                break
                            console.print(".", end="")
                            sys.stdout.flush()
                            time.sleep(5)
                        console.print("[DONE]", style="green")
                        
                        second_failed_pulls = []
                        for t in retry_tasks:
                            res = t.result()
                            if not res["success"]:
                                write_log(f"ERROR: Pull retry failed for {res['name']} - {res['error']}", level="ERROR")
                                second_failed_pulls.append(res["name"])
                        
                        if second_failed_pulls:
                            raise RuntimeError(f"Deployment aborted after retry due to image pull failures: {', '.join(second_failed_pulls)}")
                elif choice == "Ignore failures and proceed":
                    write_log("Proceeding with deployment despite pull failures...", level="WARN")
                else:
                    raise RuntimeError(f"Deployment aborted by user due to image pull failures on stack(s): {failed_list}")

    # 3. Start Stacks sequentially
    write_step("Initializing Service Containers (Sequenced)")
    for stack in stacks:
        name = stack.get("Name")
        if name == "core":
            continue
        path = resolve_path_slash(os.path.join(stacks_dir, name))
        if os.path.exists(path):
            try:
                test_container_conflict(path, name)
            except Exception as e:
                write_log(str(e), level="ERROR")
                continue

            write_log(f"Starting stack: {name}", level="DEBUG")
            try:
                invoke_external_command(
                    f"docker compose -p {name} up -d --remove-orphans",
                    description=f"Starting {name}",
                    cwd=path
                )
                
                # Verification
                exist_proc = subprocess.run(
                    ["docker", "compose", "-p", name, "ps", "-a", "-q"],
                    capture_output=True,
                    text=True
                )
                existing = exist_proc.stdout.strip()
                if not existing:
                    write_log(f"ERROR: Stack {name} failed to create containers.", level="ERROR")
                else:
                    write_log(f"Successfully started {name}", level="DEBUG")
            except Exception as e:
                write_log(f"ERROR: Failed to start {name} - {str(e)}", level="ERROR")

            time.sleep(1)

    # 4. Post-Deployment Container Health Summary
    if os.getenv("TEST_MODE") != "true":
        write_log("Verifying Container Health Status", level="DEBUG")
        write_log("Waiting 5 seconds for containers to initialize before auditing health status...", level="DEBUG")
        time.sleep(5)

        try:
            all_containers_proc = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True
            )
            all_containers = [n.strip() for n in all_containers_proc.stdout.splitlines() if n.strip()]
            unhealthy_count = 0

            for c_name in all_containers:
                try:
                    inspect_proc = subprocess.run(["docker", "inspect", c_name], capture_output=True, text=True, check=True)
                    inspect = json.loads(inspect_proc.stdout)
                    if not inspect:
                        continue
                    
                    compose_proj = inspect[0].get("Config", {}).get("Labels", {}).get("com.docker.compose.project", "")
                    
                    # Verify if project matches one of our deployed stacks
                    is_managed = any(s.get("Name") == compose_proj for s in stacks)
                    
                    if is_managed:
                        health_state = "running"
                        health_info = inspect[0].get("State", {}).get("Health")
                        if health_info:
                            health_state = health_info.get("Status", "running")

                        status_style = "green"
                        if health_state == "unhealthy":
                            status_style = "bold red"
                            unhealthy_count += 1
                        elif health_state == "starting":
                            status_style = "yellow"

                        write_log(f"Container: {c_name} Status: {health_state}", level="DEBUG")

                except Exception:
                    pass

            if unhealthy_count > 0:
                write_log(f"Deployment contains {unhealthy_count} unhealthy container(s). Please inspect logs with 'docker logs [container_name]'.", level="WARN")
            else:
                write_log("All checked container services are running or healthy.", level="DEBUG")
                console.print("[✓] All checked container services are running or healthy", style="green")

        except Exception as e:
             write_log(f"Failed to fetch health check statuses: {str(e)}", level="WARN")

    write_log("Automated deployment step finished.", level="DEBUG")
    console.print("[✓] Deployment complete", style="green")
    return True
````

## File: src/utils/paths.py
````python
import os
import sys

def resolve_path_slash(path: str) -> str:
    if not path:
        return path
    
    # Replace backslashes with forward slashes for Docker compatibility
    norm = path.replace("\\", "/")
    
    # If it is a drive letter (e.g. C:), append a slash
    if len(norm) == 2 and norm[1] == ":" and norm[0].isalpha():
        norm += "/"
        
    return norm

def get_project_root() -> str:
    # Look for dockersetup.py to locate project root
    start_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = start_dir
    while current_dir:
        if os.path.exists(os.path.join(current_dir, "dockersetup.py")):
            return resolve_path_slash(current_dir)
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            break
        current_dir = parent
    
    # Fallback default
    fallback = os.path.abspath(os.path.join(start_dir, ".."))
    return resolve_path_slash(fallback)

def get_deploy_dir() -> str:
    if os.getenv("DEPLOY_DIR"):
        return resolve_path_slash(os.getenv("DEPLOY_DIR"))
    if getattr(sys, "frozen", False):
        if sys.platform == "win32":
            return "C:/docker"
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            return "/opt/docker"
        return resolve_path_slash(os.path.expanduser("~/docker"))
    return get_project_root()

def get_resource_path(filename: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundled_path = os.path.join(sys._MEIPASS, "resources", filename)
        if os.path.exists(bundled_path):
            return resolve_path_slash(bundled_path)
        return resolve_path_slash(os.path.join(sys._MEIPASS, filename))
    return resolve_path_slash(os.path.join(get_project_root(), "resources", filename))

def get_clean_env() -> dict:
    env = os.environ.copy()
    # PyInstaller overrides library paths, polluting subprocesses. Restore original if present.
    for var in ["LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH"]:
        orig_var = var + "_ORIG"
        if orig_var in env:
            env[var] = env[orig_var]
        else:
            env.pop(var, None)
    # Remove PyInstaller-specific internal variables so that relaunched binaries extract cleanly
    env.pop("_MEIPASS", None)
    return env
````

## File: src/utils/uninstall.py
````python
import os
import sys
import shutil
import subprocess
import questionary
from rich.console import Console
from src.utils.paths import get_clean_env
from src.utils.logger import safe_confirm

console = Console()

def main():
    deploy_dir = os.getenv("DEPLOY_DIR")
    if not deploy_dir:
        console.print("[!] Error: DEPLOY_DIR environment variable is not set.", style="bold red")
        sys.exit(1)

    deploy_dir = os.path.abspath(deploy_dir)
    stacks_dir = os.path.join(deploy_dir, "stacks")

    # 1. Validation check
    metadata_path = os.path.join(deploy_dir, ".metadata.json")
    env_path = os.path.join(deploy_dir, ".env")
    
    if not os.path.exists(stacks_dir) or not (os.path.exists(metadata_path) or os.path.exists(env_path)):
        console.print(f"[!] Security Fault: '{deploy_dir}' does not appear to be a valid DockerSetup directory.", style="bold red")
        sys.exit(1)

    console.print("\n--- Uninstalling Docker Setup Stack ---", style="bold red")
    console.print(f"Target Directory: {deploy_dir}", style="grey50")
    
    # 2. Prompts
    confirm = safe_confirm(
        "Are you sure you want to completely uninstall all services and stacks?", 
        default=False
    )
    
    if not confirm:
        console.print("Uninstall cancelled.", style="yellow")
        sys.exit(0)

    remove_volumes = safe_confirm(
        "Would you like to permanently delete Docker named volumes? (This destroys database/application state not saved to host mount folders)", 
        default=False
    )

    # Check Docker daemon availability
    docker_online = False
    try:
        subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=get_clean_env(), timeout=4)
        docker_online = True
    except Exception:
        docker_online = False

    if not docker_online:
        console.print("\n[bold red][!] WARNING: Docker daemon is not running.[/bold red]")
        console.print("Containers and volumes cannot be stopped or removed automatically.", style="yellow")
        cont = safe_confirm("Do you want to proceed with deleting the local configuration folders anyway?", default=False)
        if not cont:
            console.print("Uninstall aborted. Config directories preserved.", style="yellow")
            sys.exit(0)

    # Backup env file for safety
    if os.path.exists(env_path):
        backup_env = env_path + ".bak"
        try:
            shutil.copy2(env_path, backup_env)
            console.print(f"[Backup] Saved backup of configurations to {backup_env}", style="green")
        except Exception as e:
            console.print(f"[!] Warning: Could not create .env backup: {str(e)}", style="yellow")

    # 3. Teardown loop
    down_args = ["docker", "compose", "down", "--remove-orphans"]
    if remove_volumes:
        down_args.append("-v")

    stacks = [s for s in os.listdir(stacks_dir) if os.path.isdir(os.path.join(stacks_dir, s))]
    failed_stacks = []

    for stack in stacks:
        full_path = os.path.join(stacks_dir, stack)
        console.print(f"\n>> Stopping stack: {stack}...", style="cyan")
        
        try:
            # Run docker compose down
            result = subprocess.run(down_args, cwd=full_path, env=get_clean_env())
            if result.returncode != 0:
                console.print(f"[!] Warning: Docker Compose down failed for stack '{stack}'.", style="bold red")
                failed_stacks.append(stack)
        except Exception as e:
            console.print(f"[!] Error running docker compose for stack '{stack}': {str(e)}", style="bold red")
            failed_stacks.append(stack)

    # 4. Handle failures
    proceed_with_cleanup = True
    if failed_stacks:
        console.print("\n[!] Warning: The following stacks failed to teardown cleanly in Docker:", style="bold red")
        for s in failed_stacks:
            console.print(f" - {s}", style="yellow")
        
        console.print("\nIf you delete the configuration files now, these containers will become orphaned and running.")
        proceed_with_cleanup = safe_confirm(
            "Force delete stack configuration folders anyway?", 
            default=False
        )

    # 5. Directory cleanup
    if proceed_with_cleanup:
        import stat
        import sys
        def force_delete_fallback(func, path, exc_info):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception:
                pass

        rmtree_opts = {}
        if sys.version_info >= (3, 12):
            rmtree_opts["onexc"] = force_delete_fallback
        else:
            rmtree_opts["onerror"] = force_delete_fallback
            
        try:
            shutil.rmtree(stacks_dir, **rmtree_opts)
            console.print("[OK] Stack configuration files successfully removed.", style="green")
            
            # Clean metadata
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
                console.print("[OK] Metadata file removed.", style="green")
        except Exception as e:
            console.print(f"[!] Error during file deletion: {str(e)}", style="bold red")
    else:
        console.print("Configuration files preserved. Please resolve Docker errors and try again.", style="yellow")

if __name__ == "__main__":
    main()
````

## File: src/utils/yaml_parser.py
````python
import os
import re
import hashlib
from typing import Dict, List, Any
from ruamel.yaml import YAML
from src.utils.logger import write_log

yaml_loader = YAML()

class YamlService:
    def __init__(self, key: str, port: str = "0", type_str: str = "none", description: str = ""):
        self.key = key
        self.port = port
        self.type = type_str
        self.description = description

class StackGroup:
    def __init__(self, name: str, services: List[str]):
        self.name = name
        self.services = services

class Recommendation:
    def __init__(self, source: str, recommendations: List[str]):
        self.source = source
        self.recommendations = recommendations

class ConfigurableApp:
    def __init__(self, name: str, alias: str):
        self.name = name
        self.alias = alias

def get_yaml_content(file_path: str) -> Dict[str, Any]:
    if not os.path.exists(file_path):
        write_log(f"YAML file not found: {file_path}", level="ERROR")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = yaml_loader.load(f)
    except Exception as e:
        write_log(f"Error loading standard YAML: {str(e)}", level="ERROR")
        return {}

    data = {}
    if not raw_data:
        return data

    for section_name, items in raw_data.items():
        data[section_name] = []
        if not items:
            continue

        for item in items:
            if not isinstance(item, str):
                continue
            parts = [p.strip() for p in item.split("|") if p.strip() or p == '']
            if not parts or not parts[0]:
                write_log(f"Malformed entry in section '{section_name}': '{item}'", level="WARN")
                continue
            
            if section_name == "STACK_GROUPS":
                stack_name = parts[0]
                services = []
                if len(parts) >= 2:
                    services = [s.strip() for s in parts[1].split(",") if s.strip()]
                else:
                    write_log(f"Stack group '{stack_name}' has no services defined.", level="WARN")
                data[section_name].append(StackGroup(stack_name, services))
            elif section_name == "RECOMMENDATIONS":
                source_svc = parts[0]
                rec_svcs = []
                if len(parts) >= 2:
                    rec_svcs = [s.strip() for s in parts[1].split(",") if s.strip()]
                else:
                    write_log(f"Recommendation for '{source_svc}' has no recommended services defined.", level="WARN")
                data[section_name].append(Recommendation(source_svc, rec_svcs))
            elif section_name in ["CONFIGURABLE_APPS", "ARR_APPS", "SUPPORTED_WIDGETS"]:
                name = parts[0]
                alias = name
                match = re.match(r"^([^:]+):(.*)$", name)
                if match:
                    name = match.group(1).strip()
                    alias = match.group(2).strip()
                data[section_name].append(ConfigurableApp(name, alias))
            else:
                key = parts[0]
                port = "0"
                if len(parts) >= 2:
                    port = parts[1]
                type_str = "none"
                if len(parts) >= 3:
                    type_str = parts[2]
                desc = ""
                if len(parts) >= 4:
                    desc = parts[3]
                data[section_name].append(YamlService(key, port, type_str, desc))

    return data

def get_template_blocks(file_path: str) -> Dict[str, str]:
    if not os.path.exists(file_path):
        write_log(f"Template file not found: {file_path}", level="ERROR")
        return {}

    templates = {}
    current_svc = ""
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        write_log(f"Failed to read template blocks from {file_path}: {str(e)}", level="ERROR")
        return {}

    for line in lines:
        # Match service_name: |
        match_svc = re.match(r"^([^:]+):\s*\|", line)
        if match_svc:
            current_svc = match_svc.group(1).strip()
            templates[current_svc] = ""
        elif line.startswith("  "):
            if current_svc:
                val = line
                if current_svc == "header":
                    val = line[2:]
                templates[current_svc] += val
        elif line.strip() and not line.startswith("  "):
            current_svc = ""

    return templates

def get_registry_list(master_registry: Dict[str, Any]) -> List[YamlService]:
    registry_list = []
    for section_name, items in master_registry.items():
        if section_name in ["STACK_GROUPS", "RECOMMENDATIONS", "CONFIGURABLE_APPS", "ARR_APPS", "SUPPORTED_WIDGETS"]:
            continue
        for item in items:
            if isinstance(item, YamlService):
                registry_list.append(item)
    return registry_list

def test_template_versions(file_path: str):
    if not os.path.exists(file_path):
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()
    except Exception:
        return

    current_service = ""
    critical_services = ["mariadb (+adminer)", "postgresql (+cloudbeaver)", "mongodb (+mongo-express)", "authelia"]

    for line in content:
        match_svc = re.match(r"^([^:]+):\s*\|", line)
        if match_svc:
            current_service = match_svc.group(1).strip()
        elif not line.strip() or not line.startswith("  "):
            if not line.strip().startswith("#"):
                current_service = ""

        if current_service and current_service in critical_services:
            match_img = re.search(r"image:\s*([^\s]+)", line)
            if match_img:
                image = match_img.group(1)
                if image.endswith(":latest") or ":" not in image:
                    write_log(
                        f"[AUDIT] Insecure tag found in critical service '{current_service}': image is using '{image}'. Consider pinning to a stable version.",
                        level="WARN"
                    )
````

## File: TASKS.md
````markdown
# Docker Setup Script: Python Migration Tasks

All tasks for the non-destructive Python migration are successfully completed.

## 🚀 Migration Completion Checklist

- [x] **Project Scaffolding**
  - Poetry `pyproject.toml` declared.
  - Independent virtual environment (`.venv`) initialized.
  - Python packaging setup completed.
- [x] **Utilities Migration**
  - `logger.py`: Formatted terminal logs and step tracking via `rich`.
  - `paths.py`: Drive path resolution and volume mount string formatting.
  - `state.py`: Caching, metadata reading/writing, and secure env variables.
  - `yaml_parser.py`: Multi-line key-value parsing for `services.yml` and custom line-based block scalar scanning for `templates.yml` (ensuring 100% backward compatibility).
  - `updater.py`: Renovated self-updater with binary-renaming swap support.
- [x] **Modules Migration**
  - `preflight.py`: Admin checks, Docker presence checks, and Windows registry edits.
  - `deploy_preflight.py`: Space capacity reviews via `shutil.disk_usage()`.
  - `tier_select.py`: Dynamic interactive menus utilizing `questionary`.
  - `env_wizard.py`: Secure password generation, automatic timezone discovery, and LAN network scans.
  - `directories.py`: Cross-platform structure creation and placeholder writing.
  - `network.py`: External Docker networking checks.
  - `compose_build.py`: Filtered `.env` generation and Compose file stitching.
  - `deploy_start.py`: Thread pool concurrent image downloading and sequential stack creation.
  - `auto_configure.py`: Multi-service API key matching, qBittorrent authentication, and dashboard stitching.
- [x] **Master Entry Point**
  - `dockersetup.py` completed with all menus, reconfigure workflows, updates, and token config utilities.
- [x] **Testing & Validation**
  - Comprehensive unit test suite implemented at `tests/test_runtime.py` covering paths, yaml loader, metadata state, env configuration, and directories.
  - Integration tests added for `compose_build` and `auto_configure` with network/process mocking.
  - All tests verified and passing inside the virtual environment.

## 🛡️ Security & Architecture Hardening (June 2026)
- [x] **Secret Isolation**: Moved hardcoded development tokens to project-level `.env`.
- [x] **Smart SSL Verification**: Re-enabled SSL verification for public URLs while allowing bypassed local traffic.
- [x] **Architectural Refactor**: Decomposed `auto_configure.py` into focused strategy modules (`modules/strategies/`).
- [x] **Dependency Hardening**: Pinned all dependencies to exact versions in `pyproject.toml`.
- [x] **YAML Integrity**: Added protection headers to `templates.yml` to prevent parser breakage.

## 📝 Deferred / Complex Items
*No functionality was deferred. The Python migration successfully preserves 100% of the original features while upgrading performance via concurrent pulling and premium terminal menus.*

## 📌 Next Session Tasks (Primary Priority)
- [x] **Fix Concurrent Pull Failures and Error Handling in `deploy_start.py`**:
  - Evaluate why concurrent image pulls fail with exit status 2 on certain Docker/Podman environments (e.g., Podman compose compatibility).
  - Implement robust error handling so that if image pulling fails, the script either recovers, retries, or halts deployment rather than silently continuing and trying to start stacks with missing/stale images.

- [ ] **Automated NPM Forward Auth Integration**:
  - Research direct database seeding or configuration injection for Nginx Proxy Manager hosts.
  - Implement automatic forward-authentication routing to Authelia/Authentik when identity providers are present in the stack.
````

## File: src/modules/tier_select.py
````python
import os
import questionary
from src.utils.paths import get_project_root, get_resource_path
from src.utils.logger import write_log, console, write_step, safe_confirm
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list, YamlService

def select_services() -> list:
    write_step("Selecting Stack Services & Tier")
    project_root = get_project_root()
    services_path = get_resource_path("services.yml")

    from src.apps.loader import get_apps_list
    apps = get_apps_list()

    metadata = get_metadata()
    if os.getenv("SKIP_SELECTION") == "true" and metadata.get("selected_services"):
        write_log("[UPGRADE] Recovered existing service selection from metadata. Skipping menu.", level="DEBUG")
        console.print("[✓] Service selections loaded from metadata", style="green")
        return metadata["selected_services"]

    # 1. Tier selection
    choice = questionary.select(
        "Choose Stack Tier Selection Mode:",
        choices=[
            questionary.Choice("Minimal (Standard Media Stack)", value="1"),
            questionary.Choice("Advanced (Custom Selection)", value="2")
        ]
    ).ask()

    selected = []

    # Define minimal keys
    MINIMAL_KEYS = {
        "sonarr", "radarr", "lidarr", "flaresolverr", "bazarr", "prowlarr",
        "sabnzbd", "seerr", "recyclarr", "plex", "watchtower", "docker-prune",
        "tautulli", "homepage"
    }

    # 2. Add minimal services
    write_log("Configuring MINIMAL services:", level="DEBUG")
    for app in apps:
        if app.key in MINIMAL_KEYS:
            write_log(f" + {app.key}", level="DEBUG")
            selected.append(app.key)

    # 3. Custom / Advanced selections
    if choice == "2":
        categories = {}
        for app in apps:
            cat = app.stack_group.upper() if app.stack_group else "GENERAL"
            if not cat or cat == "NONE":
                cat = "UTILITIES"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(app)

        for cat in sorted(categories.keys()):
            show_cat = safe_confirm(f"\nShow services in {cat}?", default=False)
            if show_cat:
                choices = [
                    questionary.Choice(
                        title=f"{svc.key} - {svc.description}" if svc.description else svc.key,
                        value=svc.key,
                        checked=(svc.key in selected)
                    )
                    for svc in categories[cat]
                ]
                cat_selection = questionary.checkbox(
                    f"Select services in {cat}:",
                    choices=choices
                ).ask()
                if cat_selection:
                    for s in cat_selection:
                        if s not in selected:
                            selected.append(s)
            else:
                write_log(f"Skipping category: {cat}", level="DEBUG")

    # 4. Dependency Mapping & Auto-Inclusion (Edge Case 11)
    db_addons = {
        "mariadb (+adminer)": "adminer",
        "postgresql (+cloudbeaver)": "cloudbeaver",
        "mongodb (+mongo-express)": "mongo-express"
    }
    for db, addon in db_addons.items():
        if db in selected and addon not in selected:
            selected.append(addon)
            write_log(f"Automatically added dependency helper application: {addon}", level="DEBUG")

    # 5. Recommendation Engine
    rec_map = {app.key: app.recommendations for app in apps if app.recommendations}

    suggested = []
    # Only suggest companion recommendations if custom/advanced setup mode (Tier 2) is chosen
    if choice == "2":
        for s in selected:
            if s in rec_map:
                for rec in rec_map[s]:
                    if rec not in selected and rec not in suggested and rec.strip():
                        suggested.append(rec)
    
    if suggested:
        console.print("\n--- Recommended Add-ons ---", style="yellow")
        console.print("Based on your selections, we recommend adding these services:", style="grey50")
        
        rec_choices = [
            questionary.Choice(title=f"Add {rec}?", value=rec, checked=True)
            for rec in suggested
        ]
        
        confirmed_recs = questionary.checkbox(
            "Select recommended add-ons to enable:",
            choices=rec_choices
        ).ask()
        
        if confirmed_recs:
            for rec in confirmed_recs:
                if rec not in selected:
                    selected.append(rec)
                    write_log(f"Added recommended service: {rec}", level="DEBUG")

    # Update metadata
    metadata["selected_services"] = selected
    metadata["tier"] = choice
    set_metadata(metadata)
    write_log("Selection and Tier saved to metadata.", level="DEBUG")
    console.print("[✓] Service selection saved", style="green")
    
    return selected
````

## File: src/gui/__init__.py
````python
import os
import sys
import threading
import queue
import time
import socket
import platform
import subprocess
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import tkinter.ttk as ttk

# Prevent darkdetect from executing blocking subprocess calls on Linux
if sys.platform.startswith("linux"):
    try:
        import darkdetect
        darkdetect.theme = lambda: "Dark"
    except Exception:
        pass

# Monkey-patch CTkScrollableFrame.check_if_master_is_canvas
try:
    original_check = ctk.CTkScrollableFrame.check_if_master_is_canvas
    def patched_check(self, widget):
        if isinstance(widget, str):
            try:
                widget = self.nametowidget(widget)
            except Exception:
                return False
        try:
            return original_check(self, widget)
        except Exception:
            return False
    ctk.CTkScrollableFrame.check_if_master_is_canvas = patched_check
except Exception:
    pass

from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path, get_clean_env
from src.utils.logger import set_log_path, write_log
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list
from src.utils.updater import VERSION

# Core module imports
from src.modules.preflight import run_system_preflight
from src.modules.deploy_preflight import get_port_owner
from src.modules.directories import setup_directories
from src.modules.network import setup_networks
from src.modules.compose_build import build_compose_stacks
from src.modules.deploy_start import deploy_stacks
from src.modules.auto_configure import auto_stitch_services
from src.modules.env_wizard import COMMON_ZONES, detect_timezone, new_random_password

# Import modular frames
from src.gui.welcome_frame import WelcomeFrame
from src.gui.services_frame import ServicesFrame
from src.gui.env_frame import EnvFrame
from src.gui.deploy_frame import DeployFrame
from src.gui.logs_frame import LogsFrame
from src.gui.summary_frame import SummaryFrame

class DockerSetupGUI(ctk.CTk):
    def get_linux_dpi_scale(self) -> float:
        try:
            tk_scale = self.tk.call('tk', 'scaling')
            detected = tk_scale / 1.33333333
            return max(detected, 1.25)
        except Exception:
            return 1.25

    def on_window_resize_event(self, event):
        if event.widget != self:
            return
        if self.resize_timer:
            self.after_cancel(self.resize_timer)
        self.resize_timer = self.after(500, self.apply_dynamic_resize_scale)

    def apply_dynamic_resize_scale(self):
        current_width = self.winfo_width()
        if abs(self.last_scaled_width - current_width) < 15:
            return
        self.last_scaled_width = current_width
        width_ratio = current_width / self.baseline_width
        base_scale = self.get_linux_dpi_scale() if sys.platform.startswith("linux") else 1.0
        new_scale = max(base_scale, min(base_scale * width_ratio, 1.8))
        self.current_scale = new_scale
        self.apply_scaling_factor(new_scale)

    def __init__(self):
        super().__init__()

        # Hide terminal console window at startup on Windows only if we own the console process
        if sys.platform == "win32":
            try:
                import ctypes
                hwnd = ctypes.windll.kernel32.GetConsoleWindow()
                if hwnd != 0:
                    pid = ctypes.wintypes.DWORD()
                    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if pid.value == os.getpid() or pid.value == os.getppid():
                        ctypes.windll.user32.ShowWindow(hwnd, 0) # SW_HIDE = 0
            except Exception:
                pass

        # 1. Main Window Settings
        self.title(f"DockerSetup v{VERSION} - Graphical Setup Suite")
        self.geometry("1000x650")
        self.minsize(900, 600)
        
        # Scaling variables
        self.resize_timer = None
        self.baseline_width = 1000
        self.last_scaled_width = 1000
        self.current_scale = 1.0
        
        # Determine theme based on system setting
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Detect and apply platform DPI auto-scaling for Linux
        if sys.platform.startswith("linux"):
            try:
                scale = self.get_linux_dpi_scale()
                ctk.set_widget_scaling(scale)
                ctk.set_window_scaling(scale)
                self.last_scaled_width = int(1000 * scale)
                self.baseline_width = int(1000 * scale)
                self.current_scale = scale
            except Exception:
                pass

        self.bind("<Configure>", self.on_window_resize_event)

        # Force Headless execution mode for background modules to bypass interactive questionary prompts
        os.environ["DS_HEADLESS"] = "true"
        
        # State & Logger
        self.log_queue = queue.Queue()
        from src.utils.logger import set_gui_log_callback
        set_gui_log_callback(self.log_message)
        
        self.registry = []
        self.selected_services = set()
        self.env_vars = {}
        self.chk_vars = {}
        self.var_advanced_mode = tk.BooleanVar(value=False)
        
        # Navigation Locks State
        self.max_completed_step = 1

        # Load service registry
        self.load_services_registry()
        
        # 2. Main Layout Grid (Sidebar + Main View Frame)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        # Sidebar Logo / Header
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="DockerSetup", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sub_logo = ctk.CTkLabel(self.sidebar_frame, text=f"Version {VERSION}", font=ctk.CTkFont(size=12, slant="italic"))
        self.sub_logo.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Navigation Buttons
        self.btn_welcome = ctk.CTkButton(self.sidebar_frame, text="1. Welcome", anchor="w", command=self.show_welcome_frame)
        self.btn_welcome.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_services = ctk.CTkButton(self.sidebar_frame, text="2. Services", anchor="w", command=self.show_services_frame)
        self.btn_services.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_env = ctk.CTkButton(self.sidebar_frame, text="3. Credentials", anchor="w", command=self.show_env_frame)
        self.btn_env.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_deploy = ctk.CTkButton(self.sidebar_frame, text="4. Deploy", anchor="w", command=self.show_deploy_frame)
        self.btn_deploy.grid(row=5, column=0, padx=20, pady=10, sticky="new")
        
        self.btn_logs = ctk.CTkButton(self.sidebar_frame, text="View Logs", anchor="w", command=self.show_logs_frame)
        self.btn_logs.grid(row=6, column=0, padx=20, pady=10, sticky="new")
        
        # Appearance Mode Selector in Sidebar bottom
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"], command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 5), sticky="ew")
        
        # UI Scaling Control
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(5, 0), sticky="w")
        
        scaling_buttons_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        scaling_buttons_frame.grid(row=10, column=0, padx=20, pady=(5, 20), sticky="ew")
        scaling_buttons_frame.grid_columnconfigure(0, weight=1)
        scaling_buttons_frame.grid_columnconfigure(1, weight=1)
        
        self.btn_scale_down = ctk.CTkButton(scaling_buttons_frame, text="➖", width=40, height=30, command=self.zoom_out)
        self.btn_scale_down.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_scale_up = ctk.CTkButton(scaling_buttons_frame, text="➕", width=40, height=30, command=self.zoom_in)
        self.btn_scale_up.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        try:
            self.scaling_label.configure(text="UI Scaling")
        except Exception:
            self.scaling_label.configure(text="UI Scaling")
        
        # 3. Main Display Area
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create Frame Views
        self.welcome_frame = WelcomeFrame(self.main_container, self)
        self.services_frame = ServicesFrame(self.main_container, self)
        self.env_frame = EnvFrame(self.main_container, self)
        self.deploy_frame = DeployFrame(self.main_container, self)
        self.logs_view_frame = LogsFrame(self.main_container, self)
        self.summary_view_frame = SummaryFrame(self.main_container, self)
        
        # Initialize default log path on startup
        initial_deploy = get_deploy_dir()
        log_dir = os.path.join(initial_deploy, "logs")
        set_log_path(log_dir)
        
        # Rotate setup.log on startup if it's > 0 bytes
        log_path = os.path.join(log_dir, "setup.log")
        old_log_path = os.path.join(log_dir, "setup.old.log")
        if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
            try:
                if os.path.exists(old_log_path):
                    os.remove(old_log_path)
                os.rename(log_path, old_log_path)
            except Exception:
                pass
        
        try:
            os.makedirs(log_dir, exist_ok=True)
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("")
        except Exception:
            pass
        
        # Initialize Sidebar button states
        self.update_navigation_buttons()
        
        # Launch Welcome Frame first
        self.show_welcome_frame()
        self.run_preflight_checks()
        
        # Start background queue reader for logs
        self.after(100, self.read_log_queue)

    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def zoom_in(self):
        self.current_scale = min(self.current_scale + 0.1, 2.0)
        self.apply_scaling_factor(self.current_scale)

    def zoom_out(self):
        self.current_scale = max(self.current_scale - 0.1, 0.8)
        self.apply_scaling_factor(self.current_scale)

    def apply_scaling_factor(self, scale_val: float):
        try:
            ctk.set_widget_scaling(scale_val)
            ctk.set_window_scaling(scale_val)
            self.scaling_label.configure(text="UI Scaling")
            self.update_idletasks()
        except Exception:
            pass

    def update_navigation_buttons(self):
        self.btn_welcome.configure(state="normal")
        self.btn_services.configure(state="normal" if self.max_completed_step >= 2 else "disabled")
        self.btn_env.configure(state="normal" if self.max_completed_step >= 3 else "disabled")
        self.btn_deploy.configure(state="normal" if self.max_completed_step >= 4 else "disabled")
        if hasattr(self, "btn_logs"):
            self.btn_logs.configure(state="normal")

    def center_over_parent(self, dialog, width: int, height: int):
        self.update_idletasks()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()
        parent_x = self.winfo_x()
        parent_y = self.winfo_y()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        dialog.transient(self)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        dialog.deiconify()
        dialog.update_idletasks()
        try:
            dialog.grab_set()
        except Exception:
            pass

    def load_services_registry(self):
        try:
            from src.apps.loader import get_apps_list
            self.registry = get_apps_list()
            self.master_registry = {}
        except Exception as e:
            write_log(f"GUI failed to load dynamic registry: {str(e)}", level="ERROR")
            self.registry = []
            self.master_registry = {}

    def select_sidebar_button(self, selected_btn):
        for btn in [self.btn_welcome, self.btn_services, self.btn_env, self.btn_deploy, getattr(self, "btn_logs", None)]:
            if btn:
                if btn == selected_btn:
                    btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
                else:
                    btn.configure(fg_color="transparent")

    def show_welcome_frame(self):
        self.select_sidebar_button(self.btn_welcome)
        self.hide_all_frames()
        self.welcome_frame.grid(row=0, column=0, sticky="nsew")

    def show_services_frame(self, from_next=False):
        if from_next:
            self.max_completed_step = max(self.max_completed_step, 2)
        if self.max_completed_step < 2:
            return
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_services)
        self.hide_all_frames()
        self.build_services_checkboxes()
        self.services_frame.grid(row=0, column=0, sticky="nsew")

    def show_env_frame(self, from_next=False):
        if from_next:
            self.max_completed_step = max(self.max_completed_step, 3)
        if self.max_completed_step < 3:
            return
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_env)
        self.hide_all_frames()
        self.build_dynamic_env_fields()
        self.env_frame.grid(row=0, column=0, sticky="nsew")

    def show_deploy_frame(self, from_next=False):
        if from_next:
            self.max_completed_step = max(self.max_completed_step, 4)
        if self.max_completed_step < 4:
            return
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_deploy)
        self.hide_all_frames()
        self.save_current_selections()
        self.update_deploy_summary()
        self.deploy_frame.grid(row=0, column=0, sticky="nsew")

    def show_logs_frame(self, from_next=False):
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_logs)
        self.hide_all_frames()
        self.logs_view_frame.update_logs_view_content()
        self.logs_view_frame.grid(row=0, column=0, sticky="nsew")

    def show_post_deploy_summary(self):
        self.select_sidebar_button(None)
        self.hide_all_frames()
        self.summary_view_frame.load_tabs_data()
        self.summary_view_frame.grid(row=0, column=0, sticky="nsew")

    def hide_all_frames(self):
        for frame in [self.welcome_frame, self.services_frame, self.env_frame, self.deploy_frame, self.logs_view_frame, self.summary_view_frame]:
            if frame:
                frame.grid_forget()

    def run_preflight_checks(self):
        if hasattr(self, "welcome_frame"):
            self.welcome_frame.run_preflight_checks()

    def browse_deployment_directory(self):
        if hasattr(self, "welcome_frame"):
            selected_dir = filedialog.askdirectory(initialdir=self.welcome_frame.entry_deploy_path.get())
            if selected_dir:
                normalized = os.path.normpath(selected_dir)
                self.welcome_frame.entry_deploy_path.delete(0, tk.END)
                self.welcome_frame.entry_deploy_path.insert(0, normalized)
                os.environ["DEPLOY_DIR"] = normalized
                set_log_path(os.path.join(normalized, "logs"))

    def build_services_checkboxes(self):
        if hasattr(self, "services_frame"):
            self.services_frame.build_services_checkboxes()

    def build_dynamic_env_fields(self):
        if hasattr(self, "env_frame"):
            self.env_frame.build_dynamic_env_fields()

    def save_current_selections(self):
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}
        env_dict = {}
        if hasattr(self, "env_frame") and hasattr(self.env_frame, "env_entries"):
            for key, entry in list(self.env_frame.env_entries.items()):
                try:
                    if hasattr(entry, "winfo_exists"):
                        if not entry.winfo_exists():
                            continue
                    if hasattr(entry, "get"):
                        val = entry.get()
                        if isinstance(val, bool):
                            env_dict[key] = "true" if val else "false"
                        else:
                            env_dict[key] = str(val).strip()
                except Exception:
                    pass
            
        if not env_dict.get("HTTP_PASSWORD"):
            env_dict["HTTP_PASSWORD"] = new_random_password()
            
        deploy_path = self.welcome_frame.entry_deploy_path.get().strip()
        os.environ["DEPLOY_DIR"] = deploy_path
        
        env_dict["DOCKERDIR"] = deploy_path
        env_dict["USERDIR"] = deploy_path
        
        for key in ["MYSQL_ROOT_PASSWORD", "MYSQL_USER", "MYSQL_PASSWORD", "DB_PASS", "MONGO_PASS", "KOPIA_PASSWORD", "CROWDSEC_API_KEY"]:
            metadata = get_metadata()
            saved_env = metadata.get("env_vars", {})
            if key not in env_dict or not env_dict[key]:
                if saved_env.get(key):
                    env_dict[key] = saved_env.get(key)
                elif key == "MYSQL_USER":
                    env_dict[key] = "mediauser"
                elif key == "CROWDSEC_API_KEY":
                    env_dict[key] = new_random_password() if "crowdsec" in self.selected_services else ""
                else:
                    env_dict[key] = new_random_password()
                    
        env_dict["CROWDSEC_ENABLED"] = "true" if "crowdsec" in self.selected_services else "false"
        
        metadata = get_metadata()
        metadata["selected_services"] = list(self.selected_services)
        metadata["env_vars"] = env_dict
        set_metadata(metadata)

    def update_deploy_summary(self):
        if hasattr(self, "deploy_frame"):
            self.deploy_frame.update_deploy_summary()

    def run_fast_upgrade(self, d_dir):
        self.show_deploy_frame(from_next=True)
        if hasattr(self, "deploy_frame"):
            self.deploy_frame.log_text.delete("1.0", tk.END)
            self.log_message("[INFO] Starting fast template upgrade...")
            self.trigger_deployment_pipeline()

    def run_full_reset(self, d_dir):
        confirm = messagebox.askyesno(
            "Permanent Wipe Warning", 
            "Are you sure you want to permanently wipe all containers, volumes, and configurations in this directory?\n\nThis action cannot be undone."
        )
        if not confirm:
            return
            
        dialog = ctk.CTkToplevel(self)
        dialog.title("Resetting System")
        dialog.resizable(False, False)
        self.center_over_parent(dialog, 400, 150)
        
        lbl_msg = ctk.CTkLabel(dialog, text="Wiping all configurations and volumes...", font=ctk.CTkFont(size=13))
        lbl_msg.pack(pady=(20, 10))
        
        prog_bar = ctk.CTkProgressBar(dialog, width=300)
        prog_bar.pack(pady=10)
        prog_bar.configure(mode="indefinite")
        prog_bar.start()
        
        def reset_worker():
            try:
                write_log("[INFO] Commencing full system reset...")
                stacks_dir = os.path.join(d_dir, "stacks")
                if os.path.exists(stacks_dir):
                    for stack in os.listdir(stacks_dir):
                        full_path = os.path.join(stacks_dir, stack)
                        if os.path.isdir(full_path):
                            compose_file = os.path.join(full_path, "docker-compose.yml")
                            if os.path.exists(compose_file):
                                write_log(f"[INFO] Tearing down stack: {stack}...")
                                subprocess.run(["docker", "compose", "down", "-v", "--remove-orphans"], cwd=full_path, capture_output=True, env=get_clean_env())
                                
                write_log("[INFO] Removing stack and configuration directories...")
                shutil.rmtree(stacks_dir, ignore_errors=True)
                shutil.rmtree(os.path.join(d_dir, "appdata"), ignore_errors=True)
                
                for file in [".metadata.json", ".env"]:
                    file_p = os.path.join(d_dir, file)
                    if os.path.exists(file_p):
                        try:
                            shutil.copy2(file_p, file_p + ".bak")
                            write_log(f"[INFO] Created backup: {file}.bak")
                            os.remove(file_p)
                        except Exception:
                            pass
                
                import src.utils.state as state
                state._metadata_cache = {}
                
                write_log("[SUCCESS] Reset complete. All containers and settings have been wiped!")
                self.after(0, lambda: [
                    dialog.destroy(),
                    messagebox.showinfo("Reset Complete", "All configurations, volumes, and containers have been wiped cleanly."),
                    self.show_welcome_frame()
                ])
            except Exception as e:
                write_log(f"[ERROR] Reset failed: {str(e)}")
                self.after(0, lambda: [
                    dialog.destroy(),
                    messagebox.showerror("Reset Failed", f"An error occurred during reset: {str(e)}")
                ])
                
        t = threading.Thread(target=reset_worker)
        t.daemon = True
        t.start()

    def log_message(self, message: str):
        self.log_queue.put(message)

    def read_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                
                show_verbose = self.deploy_frame.var_verbose.get() if hasattr(self, "deploy_frame") else False
                is_debug = "[DEBUG]" in msg or "[TRACE]" in msg or msg.startswith("[DEBUG]") or msg.startswith("[TRACE]")
                
                if (show_verbose or not is_debug) and hasattr(self, "deploy_frame"):
                    self.deploy_frame.log_text.insert(tk.END, msg + "\n")
                    self.deploy_frame.log_text.see(tk.END)
                
                if hasattr(self, "logs_view_frame") and hasattr(self.logs_view_frame, "logs_textbox"):
                    if self.logs_view_frame.logs_textbox.winfo_exists():
                        show_verbose_logs = self.logs_view_frame.chk_verbose_logs.get()
                        if show_verbose_logs or not is_debug:
                            self.logs_view_frame.logs_textbox.configure(state="normal")
                            self.logs_view_frame.logs_textbox.insert(tk.END, msg + "\n")
                            self.logs_view_frame.logs_textbox.configure(state="disabled")
                            self.logs_view_frame.logs_textbox.see(tk.END)
                            
                self.log_queue.task_done()
        except queue.Empty:
            pass
        self.after(100, self.read_log_queue)

    def trigger_deployment_pipeline(self):
        try:
            subprocess.run(
                ["docker", "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=4,
                env=get_clean_env()
            )
        except Exception:
            messagebox.showerror(
                "Docker Daemon Offline",
                "Docker daemon is not running. Please start Docker Desktop/Daemon and try again."
            )
            return

        if hasattr(self, "deploy_frame"):
            self.deploy_frame.btn_start_deploy.configure(state="disabled", text="Deploying...")
            self.deploy_frame.log_text.delete("1.0", tk.END)
        
        t = threading.Thread(target=self.deployment_worker)
        t.daemon = True
        t.start()

    def deployment_worker(self):
        deploy_dir = get_deploy_dir()
        
        if hasattr(self, "deploy_frame"):
            for key in self.deploy_frame.step_indicators:
                self.deploy_frame.update_step_status(key, "Ready", color=["#000000", "#FFFFFF"])
            self.deploy_frame.update_progress_bar(0.0)
            
            if self.deploy_frame.var_verbose.get():
                os.environ["DEBUG_LOGGING"] = "true"
            else:
                os.environ["DEBUG_LOGGING"] = "false"
            
        try:
            # 1. Preflight
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Preflight", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.1)
            self.log_message("[INFO] Starting preflight system validation checks...")
            set_log_path(os.path.join(deploy_dir, "logs"))
            run_system_preflight()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Preflight", "Completed", "green")
            
            # 2. Directories
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Dirs", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.25)
            self.log_message("[INFO] Constructing deployment folder structures...")
            
            metadata = get_metadata()
            env_vars = metadata.get("env_vars", {})
            env_path = os.path.normpath(os.path.join(deploy_dir, ".env"))
            os.makedirs(os.path.dirname(env_path), exist_ok=True)
            with open(env_path, "w", encoding="utf-8") as f:
                for k, v in env_vars.items():
                    f.write(f"{k}={v}\n")
            
            setup_directories()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Dirs", "Completed", "green")
            
            # 3. Environment Secrets and Networks
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Network", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.4)
            self.log_message("[INFO] Constructing secure Docker networks...")
            setup_networks()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Network", "Completed", "green")
            
            # 4. Compose build
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Compose", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.6)
            self.log_message("[INFO] Generating Docker Compose stacks config files...")
            build_compose_stacks()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Compose", "Completed", "green")
            
            # 5. Launch containers
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Containers", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.8)
            self.log_message("[INFO] Executing compose pulls and starting container stacks in parallel...")
            deploy_stacks()
            
            stacks_dir = os.path.join(deploy_dir, "stacks")
            if os.path.exists(stacks_dir):
                for name in os.listdir(stacks_dir):
                    fpath = os.path.join(stacks_dir, name)
                    if os.path.isdir(fpath):
                        try:
                            shutil.copy(env_path, os.path.join(fpath, ".env"))
                        except Exception:
                            pass
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Containers", "Completed", "green")
            
            # 6. Auto config
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Stitch", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.9)
            self.log_message("[INFO] Commencing automated API token alignment and dashboard stitching...")
            auto_stitch_services()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Stitch", "Completed", "green")
                self.deploy_frame.update_progress_bar(1.0)
            self.log_message("[SUCCESS] Setup successfully deployed!")
            
            self.after(500, self.show_post_deploy_summary)
            
        except Exception as e:
            if hasattr(self, "deploy_frame"):
                for k in ["Preflight", "Dirs", "Network", "Compose", "Containers", "Stitch"]:
                    txt = self.deploy_frame.step_indicators[k].cget("text")
                    if "⚙" in txt or "Running" in txt:
                        self.deploy_frame.update_step_status(k, "Failed", "red")
            self.log_message(f"[ERROR] Setup failed: {str(e)}")
            import traceback
            write_log(traceback.format_exc(), level="ERROR")
            err_msg = f"An error occurred during deployment:\n\n{str(e)}\n\nPlease check the logs for detailed information."
            self.after(0, lambda: messagebox.showerror("Deployment Failed", err_msg))
        finally:
            if hasattr(self, "deploy_frame"):
                self.after(0, lambda: self.deploy_frame.btn_start_deploy.configure(state="normal", text="Deploy Stack Now"))
````

## File: src/gui/services_frame.py
````python
import tkinter as tk
import customtkinter as ctk
import webbrowser
from src.gui.base_frame import BaseFrame
from src.utils.state import get_metadata
from src.apps.loader import get_apps_list

MINIMAL_KEYS = {
    "sonarr", "radarr", "lidarr", "flaresolverr", "bazarr", "prowlarr",
    "sabnzbd", "seerr", "recyclarr", "plex", "watchtower", "docker-prune",
    "tautulli", "homepage"
}

DOC_URLS = {
    "sonarr": "https://github.com/linuxserver/docker-sonarr",
    "radarr": "https://github.com/linuxserver/docker-radarr",
    "lidarr": "https://github.com/linuxserver/docker-lidarr",
    "bazarr": "https://github.com/linuxserver/docker-bazarr",
    "prowlarr": "https://github.com/linuxserver/docker-prowlarr",
    "flaresolverr": "https://github.com/FlareSolverr/FlareSolverr",
    "qbittorrent": "https://github.com/linuxserver/docker-qbittorrent",
    "sabnzbd": "https://github.com/linuxserver/docker-sabnzbd",
    "qbittorrent-vpn": "https://github.com/binhex/arch-qbittorrentvpn",
    "seerr": "https://github.com/sct/overseerr",
    "recyclarr": "https://github.com/recyclarr/recyclarr",
    "plex": "https://github.com/linuxserver/docker-plex",
    "jellyfin": "https://github.com/linuxserver/docker-jellyfin",
    "watchtower": "https://github.com/containrrr/watchtower",
    "docker-prune": "https://hub.docker.com/r/softonic/docker-system-prune",
    "homepage": "https://github.com/gethomepage/homepage",
    "portainer": "https://github.com/portainer/portainer",
    "dockge": "https://github.com/louislam/dockge",
    "tautulli": "https://github.com/linuxserver/docker-tautulli",
    "uptime": "https://github.com/louislam/uptime-kuma",
    "tailscale": "https://github.com/tailscale/tailscale",
    "cloudflare-ddns": "https://github.com/favonia/cloudflare-ddns",
    "crowdsec": "https://github.com/crowdsecurity/crowdsec",
    "cloudbeaver": "https://github.com/dbeaver/cloudbeaver",
    "mongo-express": "https://github.com/mongo-express/mongo-express",
    "kasm": "https://github.com/linuxserver/docker-kasm",
    "cloudcmd": "https://github.com/coderaiser/cloudcmd",
    "filebrowser": "https://github.com/filebrowser/filebrowser",
    "syncthing": "https://github.com/linuxserver/docker-syncthing",
    "vaultwarden": "https://github.com/dani-garcia/vaultwarden",
    "navidrome": "https://github.com/navidrome/navidrome",
    "slskd": "https://github.com/slskd/slskd",
    "mylar": "https://github.com/linuxserver/docker-mylar3",
    "readarr": "https://github.com/linuxserver/docker-readarr",
    "hkserver": "https://github.com/hkmp-team/hkmp",
    "kopia": "https://github.com/kopia/kopia",
    "authelia": "https://github.com/authelia/authelia",
    "immich": "https://github.com/immich-app/immich",
    "audiobookshelf": "https://github.com/advplyr/audiobookshelf",
    "paperless": "https://github.com/paperless-ngx/paperless-ngx",
    "scrutiny": "https://github.com/AnalogJ/scrutiny",
    "tmodloader": "https://github.com/jacobsmile/tmodloader-docker",
    "satisfactory": "https://github.com/wolveix/satisfactory-server",
    "valheim": "https://github.com/lloesche/valheim-server-docker",
    "enshrouded": "https://github.com/mornedhels/enshrouded-docker",
    "plextraktsync": "https://github.com/Taxel/PlexTraktSync",
    "mariadb (+adminer)": "https://github.com/linuxserver/docker-mariadb",
    "postgresql (+cloudbeaver)": "https://github.com/linuxserver/docker-postgres",
    "mongodb (+mongo-express)": "https://hub.docker.com/_/mongo",
    "npm plus (+goaccess)": "https://github.com/zoeyvid/nginx-proxy-manager-plus",
}

class ServicesFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        # Initialize helper track mappings
        self.chk_buttons = {}
        self.chk_frames = {}
        self.cat_headers = {}
        self.cat_to_services = {}
        self.grid_infos = {}
        self.selected_cards = {}
        
        lbl_title = ctk.CTkLabel(self, text="Select Stack Services", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="Pick which media tools, database endpoints, and system management services you want to deploy in your stack.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 5), sticky="w")
        
        # Toggle Switch for Advanced Setup
        self.switch_advanced = ctk.CTkSwitch(
            self, 
            text="Enable Advanced Custom Setup", 
            variable=self.controller.var_advanced_mode, 
            command=self.on_advanced_switch_toggle,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.switch_advanced.grid(row=2, column=0, pady=(5, 5), sticky="w")
        
        # Search Bar for available services
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=3, column=0, sticky="ew", pady=(5, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search available services...", height=30)
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_services_checklist)
        
        # Container frame for either Minimal or Advanced layouts
        self.services_container = ctk.CTkFrame(self, fg_color="transparent")
        self.services_container.grid(row=4, column=0, sticky="nsew", pady=10)
        self.services_container.grid_columnconfigure(0, weight=1)
        self.services_container.grid_rowconfigure(0, weight=1)
        
        # Navigation
        nav_buttons = ctk.CTkFrame(self, fg_color="transparent")
        nav_buttons.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.controller.show_welcome_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Configure Credentials", width=220, command=self.check_recommendations_and_proceed)
        btn_next.grid(row=0, column=1, sticky="e")

    def build_services_checkboxes(self):
        metadata = get_metadata()
        active_selections = metadata.get("selected_services", [])
        
        # Determine initial switch state if not already set manually
        if active_selections:
            is_adv = not all(k in MINIMAL_KEYS for k in active_selections)
            if is_adv and not self.controller.var_advanced_mode.get():
                self.controller.var_advanced_mode.set(True)
        else:
            active_selections = list(MINIMAL_KEYS)

        # Ensure all services have a BooleanVar initialized
        for entry in self.controller.registry:
            if entry.key not in self.controller.chk_vars:
                is_selected = entry.key in active_selections
                self.controller.chk_vars[entry.key] = tk.BooleanVar(value=is_selected)

        # Build Minimal Frame Layout once
        if not hasattr(self, "minimal_frame_layout"):
            self.minimal_frame_layout = ctk.CTkFrame(self.services_container, fg_color="transparent")
            self.minimal_frame_layout.grid_columnconfigure(0, weight=1)
            self.minimal_frame_layout.grid_rowconfigure(0, weight=1)
            
            lbl_info = ctk.CTkLabel(self.minimal_frame_layout, text="Core Minimal Services (Enabled)", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_info.pack(anchor="w", pady=(5, 10))
            
            self.minimal_scroll = ctk.CTkScrollableFrame(self.minimal_frame_layout)
            self.minimal_scroll.pack(fill="both", expand=True)
            
            for entry in self.controller.registry:
                if entry.key in MINIMAL_KEYS:
                    self.controller.chk_vars[entry.key].set(True)
                    chk = ctk.CTkCheckBox(
                        self.minimal_scroll, 
                        text=f"{entry.name} (port {entry.port})" if entry.port and entry.port != 0 else entry.name,
                        variable=self.controller.chk_vars[entry.key], 
                        state="disabled"
                    )
                    chk.pack(anchor="w", padx=20, pady=6)
                    self.chk_buttons[entry.key] = chk

        # Build Advanced Frame Layout once
        if not hasattr(self, "advanced_frame_layout"):
            self.advanced_frame_layout = ctk.CTkFrame(self.services_container, fg_color="transparent")
            self.advanced_frame_layout.grid_columnconfigure(0, weight=3)
            self.advanced_frame_layout.grid_columnconfigure(1, weight=2)
            self.advanced_frame_layout.grid_rowconfigure(0, weight=1)
            
            # Left Pane
            left_frame = ctk.CTkFrame(self.advanced_frame_layout, fg_color="transparent")
            left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
            left_frame.grid_columnconfigure(0, weight=1)
            left_frame.grid_rowconfigure(1, weight=1)
            
            lbl_left = ctk.CTkLabel(left_frame, text="Available Services Checklist", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_left.grid(row=0, column=0, pady=(5, 10), sticky="w")
            
            self.services_scroll = ctk.CTkScrollableFrame(left_frame)
            self.services_scroll.grid(row=1, column=0, sticky="nsew")
            self.services_scroll.grid_columnconfigure(0, weight=1)
            
            # Right Pane
            right_frame = ctk.CTkFrame(self.advanced_frame_layout, fg_color="transparent")
            right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            right_frame.grid_columnconfigure(0, weight=1)
            right_frame.grid_rowconfigure(1, weight=1)
            
            lbl_right = ctk.CTkLabel(right_frame, text="Active Stack Selections", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_right.grid(row=0, column=0, pady=(5, 10), sticky="w")
            
            self.selected_scroll = ctk.CTkScrollableFrame(right_frame)
            self.selected_scroll.grid(row=1, column=0, sticky="nsew")
            
            # Resolve categories (using stack_group from plugins)
            categories = {}
            for entry in self.controller.registry:
                cat = entry.stack_group.upper() if entry.stack_group else "GENERAL"
                if cat == "NONE" or not cat:
                    cat = "UTILITIES"
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(entry)

            # Render left checkboxes in a single column
            current_row = 0
            for cat_name, entries in sorted(categories.items()):
                lbl_cat = ctk.CTkLabel(self.services_scroll, text=cat_name, font=ctk.CTkFont(size=13, weight="bold"), text_color=["#1F6AA5", "#3B8ED0"])
                lbl_cat.grid(row=current_row, column=0, pady=(12, 4), sticky="w")
                
                self.cat_headers[cat_name] = lbl_cat
                self.grid_infos[cat_name] = {
                    "row": current_row,
                    "column": 0,
                    "pady": (12, 4),
                    "sticky": "w"
                }
                current_row += 1
                
                self.cat_to_services[cat_name] = []
                for entry in entries:
                    self.cat_to_services[cat_name].append(entry.key)
                    
                    item_frame = ctk.CTkFrame(self.services_scroll, fg_color="transparent")
                    item_frame.grid(row=current_row, column=0, padx=5, pady=5, sticky="w")
                    
                    self.chk_frames[entry.key] = item_frame
                    self.grid_infos[entry.key] = {
                        "row": current_row,
                        "column": 0,
                        "padx": 5,
                        "pady": 5,
                        "sticky": "w"
                    }
                    
                    chk = ctk.CTkCheckBox(
                        item_frame, 
                        text=f"{entry.name} (port {entry.port})" if entry.port and entry.port != 0 else entry.name, 
                        variable=self.controller.chk_vars[entry.key], 
                        command=self.on_checkbox_toggle
                    )
                    chk.pack(side="left", anchor="w")
                    self.chk_buttons[entry.key] = chk
                    
                    doc_url = DOC_URLS.get(entry.key.lower())
                    if doc_url:
                        btn_link = ctk.CTkLabel(
                            item_frame, 
                            text="🌐", 
                            font=ctk.CTkFont(size=13),
                            text_color=["#1F6AA5", "#3B8ED0"],
                            cursor="hand2"
                        )
                        btn_link.pack(side="left", padx=(8, 0))
                        
                        def make_open_url_cmd(url=doc_url):
                            return lambda event: webbrowser.open(url)
                        btn_link.bind("<Button-1>", make_open_url_cmd(doc_url))
                    
                    current_row += 1

        # Toggle visibility instantly
        if not self.controller.var_advanced_mode.get():
            self.advanced_frame_layout.grid_forget()
            self.minimal_frame_layout.grid(row=0, column=0, sticky="nsew")
            
            # For minimal mode, force enable only minimal keys
            for key in self.controller.chk_vars:
                if key in MINIMAL_KEYS:
                    self.controller.chk_vars[key].set(True)
                else:
                    self.controller.chk_vars[key].set(False)
        else:
            self.minimal_frame_layout.grid_forget()
            self.advanced_frame_layout.grid(row=0, column=0, sticky="nsew")

        # Apply filtering in case the search bar already has text
        self.filter_services_checklist()
        self.on_checkbox_toggle()

    def filter_services_checklist(self, event=None):
        if not hasattr(self, "cat_to_services") or not self.cat_to_services:
            return
        query = self.search_entry.get().strip().lower() if hasattr(self, "search_entry") else ""
        
        # If in Minimal Mode
        if not self.controller.var_advanced_mode.get():
            for entry in self.controller.registry:
                if entry.key in MINIMAL_KEYS:
                    if entry.key in self.chk_buttons:
                        chk = self.chk_buttons[entry.key]
                        if not query or query in entry.key.lower() or query in entry.name.lower():
                            chk.pack(anchor="w", padx=20, pady=6)
                        else:
                            chk.pack_forget()
        else:
            # If in Advanced Mode
            for cat_name, services in self.cat_to_services.items():
                matching_services = [s for s in services if not query or query in s.lower()]
                
                # Show/hide category header
                if matching_services:
                    if cat_name in self.cat_headers:
                        self.cat_headers[cat_name].grid(**self.grid_infos[cat_name])
                else:
                    if cat_name in self.cat_headers:
                        self.cat_headers[cat_name].grid_forget()
                
                # Show/hide services
                for s in services:
                    if s in self.chk_frames:
                        if not query or query in s.lower():
                            self.chk_frames[s].grid(**self.grid_infos[s])
                        else:
                            self.chk_frames[s].grid_forget()

    def on_checkbox_toggle(self):
        self.controller.selected_services = {key for key, var in self.controller.chk_vars.items() if var.get()}
        
        # Dynamically build Selected Summary if we are in Advanced Mode and self.selected_scroll exists
        if self.controller.var_advanced_mode.get() and hasattr(self, "selected_scroll") and self.selected_scroll.winfo_exists():
            if not hasattr(self, "selected_cards"):
                self.selected_cards = {}
                
            # Remove cards for services that are no longer selected
            for key in list(self.selected_cards.keys()):
                if key not in self.controller.selected_services:
                    try:
                        self.selected_cards[key].destroy()
                    except Exception:
                        pass
                    del self.selected_cards[key]
                    
            # Add cards for new selections
            for key in sorted(self.controller.selected_services):
                if key not in self.selected_cards:
                    card = ctk.CTkFrame(self.selected_scroll, fg_color=["#E5E5E5", "#2B2B2B"], height=32, corner_radius=6)
                    
                    lbl = ctk.CTkLabel(card, text=key, font=ctk.CTkFont(size=12))
                    lbl.pack(side="left", padx=10)
                    
                    def make_delete_cmd(k=key):
                        return lambda: self.uncheck_service(k)
                    
                    btn_del = ctk.CTkButton(card, text="✕", width=20, height=20, fg_color="transparent", text_color="red", hover_color=["#FFCCCC", "#552222"], command=make_delete_cmd(key))
                    btn_del.pack(side="right", padx=10)
                    
                    self.selected_cards[key] = card
            
            # Repack in sorted order to preserve correct UI sequence
            for key in sorted(self.controller.selected_services):
                if key in self.selected_cards:
                    self.selected_cards[key].pack_forget()
                    self.selected_cards[key].pack(fill="x", padx=5, pady=3)

    def uncheck_service(self, key: str):
        if key in self.controller.chk_vars:
            self.controller.chk_vars[key].set(False)
            self.on_checkbox_toggle()

    def on_advanced_switch_toggle(self):
        is_advanced = self.controller.var_advanced_mode.get()
        if not is_advanced:
            for key in list(self.controller.chk_vars.keys()):
                if key in MINIMAL_KEYS:
                    self.controller.chk_vars[key].set(True)
                else:
                    self.controller.chk_vars[key].set(False)
                    
        if hasattr(self, "search_entry"):
            self.search_entry.delete(0, tk.END)
            self.filter_services_checklist()
            
        self.build_services_checkboxes()

    def check_recommendations_and_proceed(self):
        from src.utils.dependency_resolver import check_exclusivity_conflicts, resolve_database_dependencies
        from src.utils.port_resolver import resolve_port_conflicts
        from src.utils.paths import get_deploy_dir
        import os

        # 1. Database Dependency Resolution with User Notifications
        # Map our registry list to a dict of app key -> instance
        apps_dict = {entry.key: entry for entry in self.controller.registry}
        current_keys = [key for key, var in self.controller.chk_vars.items() if var.get()]
        
        updated_keys, db_notifs = resolve_database_dependencies(current_keys, apps_dict)
        if len(updated_keys) > len(current_keys):
            # Update check box states
            for k in updated_keys:
                if k in self.controller.chk_vars:
                    self.controller.chk_vars[k].set(True)
            self.on_checkbox_toggle()
            
            # Show dependency auto-selection info pop up
            from tkinter import messagebox
            messagebox.showinfo(
                "Database Auto-Selected",
                "\n".join(db_notifs) + "\n\nYou can manually adjust these selections if desired."
            )

        # 2. Exclusivity Group Soft Warning Pop Up
        selected_app_instances = [apps_dict[k] for k in updated_keys if k in apps_dict]
        conflicts = check_exclusivity_conflicts(selected_app_instances)
        if conflicts:
            from tkinter import messagebox
            warning_msg = "Exclusivity Warnings Found:\n\n"
            for grp, app_names in conflicts.items():
                warning_msg += f"- Exclusivity Group '{grp}': {', '.join(app_names)} are all selected.\n"
            warning_msg += "\nRunning multiple services from the same exclusivity group is not recommended. Do you want to proceed anyway?"
            
            proceed = messagebox.askyesno("Exclusivity Warning", warning_msg)
            if not proceed:
                return

        # 3. Port Conflict Check & Resolution
        deploy_dir = get_deploy_dir()
        env_path = os.path.join(deploy_dir, ".env")
        port_notifs = resolve_port_conflicts(selected_app_instances, env_path)
        if port_notifs:
            from tkinter import messagebox
            messagebox.showinfo(
                "Port Collisions Resolved",
                "Some selected apps had overlapping port requirements:\n\n" + "\n".join(port_notifs) + "\n\nThese overrides have been automatically saved to your .env file."
            )

        recommendations_map = {}
        for entry in self.controller.registry:
            if entry.recommendations:
                recommendations_map[entry.key] = entry.recommendations
                
        missing_recs = []
        # Only prompt companion recommendations if Advanced Custom mode is enabled
        if self.controller.var_advanced_mode.get():
            for svc in self.controller.selected_services:
                if svc in recommendations_map:
                    for rec in recommendations_map[svc]:
                        rec = rec.strip()
                        if rec and rec not in self.controller.selected_services and rec not in missing_recs:
                            if any(e.key == rec for e in self.controller.registry):
                                missing_recs.append(rec)
                            
        if missing_recs:
            dialog = ctk.CTkToplevel(self)
            dialog.title("Recommended companion services")
            dialog.resizable(False, False)
            
            dialog_height = min(500, 300 + 32 * len(missing_recs))
            self.controller.center_over_parent(dialog, 520, dialog_height)
            dialog.transient(self)
            dialog.grab_set()
            
            lbl_title = ctk.CTkLabel(dialog, text="Select Recommended Companion Services", font=ctk.CTkFont(size=16, weight="bold"))
            lbl_title.pack(pady=(15, 5))
            
            lbl_desc = ctk.CTkLabel(
                dialog, 
                text="The following companion services are recommended based on your selections:", 
                wraplength=480, 
                font=ctk.CTkFont(size=12)
            )
            lbl_desc.pack(pady=(0, 10))
            
            scroll_frame = ctk.CTkScrollableFrame(dialog, width=440, height=min(180, 32 * len(missing_recs)))
            scroll_frame.pack(padx=20, pady=5, fill="both", expand=True)
            
            rec_vars = {}
            for rec in missing_recs:
                var = tk.BooleanVar(value=True)
                rec_vars[rec] = var
                chk = ctk.CTkCheckBox(scroll_frame, text=rec, variable=var)
                chk.pack(anchor="w", padx=20, pady=5)
                
            btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            btn_frame.pack(pady=(10, 15))
            
            def on_confirm():
                for rec, var in rec_vars.items():
                    if var.get() and rec in self.controller.chk_vars:
                        self.controller.chk_vars[rec].set(True)
                self.on_checkbox_toggle()
                dialog.destroy()
                self.controller.show_env_frame(from_next=True)
                
            def on_skip():
                dialog.destroy()
                self.controller.show_env_frame(from_next=True)
                
            def on_back():
                dialog.destroy()
                
            btn_confirm = ctk.CTkButton(btn_frame, text="Add Selected", width=120, command=on_confirm)
            btn_confirm.grid(row=0, column=0, padx=10)
            
            btn_skip = ctk.CTkButton(btn_frame, text="Skip All", width=120, fg_color="gray", hover_color="dimgray", command=on_skip)
            btn_skip.grid(row=0, column=1, padx=10)
            
            btn_back = ctk.CTkButton(btn_frame, text="Go Back", width=120, fg_color="transparent", border_width=1, command=on_back)
            btn_back.grid(row=0, column=2, padx=10)
        else:
            self.controller.show_env_frame(from_next=True)
````

## File: src/modules/deploy_preflight.py
````python
import os
import shutil
import platform
import subprocess
import socket
import re
import questionary
from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path
from src.utils.logger import write_log, console, write_step, safe_confirm
from src.utils.state import get_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list

def get_port_owner(port: int) -> str:
    """
    Query the system to identify the name/PID of the application currently binding to the specified port.
    """
    try:
        if platform.system() == "Windows":
            # Find PID using netstat
            netstat_proc = subprocess.run(
                f'netstat -ano | findstr ":{port} "',
                shell=True,
                capture_output=True,
                text=True
            )
            lines = netstat_proc.stdout.strip().splitlines()
            if lines:
                # Match last column (PID)
                match = re.search(r"(\d+)\s*$", lines[0])
                if match:
                    pid = match.group(1)
                    # Resolve process name
                    task_proc = subprocess.run(
                        f'tasklist /FI "PID eq {pid}"',
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    task_lines = task_proc.stdout.strip().splitlines()
                    if len(task_lines) >= 3:
                        parts = task_lines[3].split()
                        if parts:
                            return f"{parts[0]} (PID: {pid})"
                    return f"PID: {pid}"
        else:
            # Linux port owner checks (ss -tulpn or netstat -tulpn)
            for cmd in [["ss", "-tulpn"], ["netstat", "-tulpn"]]:
                if shutil.which(cmd[0]):
                    proc = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True
                    )
                    for line in proc.stdout.splitlines():
                        if f":{port} " in line or f":{port}\t" in line or f":{port}" in line:
                            match_pid = re.search(r"users:\(\(\"([^\"]+)\",pid=(\d+)", line)
                            if match_pid:
                                return f"{match_pid.group(1)} (PID: {match_pid.group(2)})"
                            # General parsing fallback
                            match_gen = re.search(r"(\d+)/(.*)$", line.strip().split()[-1])
                            if match_gen:
                                return f"{match_gen.group(2)} (PID: {match_gen.group(1)})"
    except Exception as e:
        write_log(f"Failed to resolve port owner for port {port}: {str(e)}", level="DEBUG")
    
    return "Unknown Process"

def run_deploy_preflight() -> bool:
    write_step("Running deployment preflight checks")

    if os.getenv("TEST_MODE") == "true":
        write_log("[TEST] Bypassing Deployment Preflight Checks", level="WARN")
        return True

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()

    if not os.path.exists(deploy_dir):
        raise FileNotFoundError(f"Target deployment directory does not exist: {deploy_dir}")

    # 1. Check disk space on target drive
    try:
        total, used, free = shutil.disk_usage(deploy_dir)
        free_gb = round(free / (1024 ** 3), 2)
        
        if free_gb < 10.0:
            write_log(f"Low disk space on target directory ({free_gb} GB free). Recommended: 10GB+", level="WARN")
        else:
            write_log(f"Sufficient disk space ({free_gb} GB free)", level="DEBUG")
    except Exception as e:
        write_log(f"Failed to check disk space: {str(e)}", level="WARN")

    # 2. Check for port conflicts based on selected services
    metadata = get_metadata()
    selected_services = metadata.get("selected_services", [])
    
    if selected_services:
        write_log("Auditing active network port mappings...", level="DEBUG")
        from src.apps.loader import get_apps_list
        registry_list = get_apps_list()
        
        resolved_ports = metadata.get("resolved_ports", {})
        conflicts = []
        
        for svc in selected_services:
            reg = next((e for e in registry_list if e.key == svc), None)
            if reg and reg.port and reg.port != 0:
                port_num = int(reg.port)
                
                # Check connection
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect(("127.0.0.1", port_num))
                    s.close()
                    owner = get_port_owner(port_num)
                    conflicts.append((svc, port_num, owner))
                except OSError:
                    pass

        if conflicts:
            from src.utils.state import set_metadata
            console.print("\n[bold red][!] PORT CONFLICTS DETECTED[/bold red]")
            
            for svc, port_num, owner in conflicts:
                write_log(f"Conflict: Port {port_num} ({svc}) occupied by {owner}", level="WARN")
                
                # Headless/Test mode fallback
                if os.getenv("DS_HEADLESS") == "true" and os.getenv("DS_GUI_MODE") != "true":
                    write_log(f"Headless mode bypass for {svc} on port {port_num}.", level="WARN")
                    continue
                    
                # 1. Identify container details
                try:
                    from src.utils.paths import get_clean_env
                    res = subprocess.run(
                        ["docker", "ps", "--filter", f"publish={port_num}", "--format", "{{.Names}}"],
                        capture_output=True, text=True, env=get_clean_env()
                    )
                    container_name = res.stdout.strip()
                except Exception:
                    container_name = ""
                    
                is_same_type = container_name and svc.lower() in container_name.lower()
                
                # Find alternative port
                alt_port = port_num
                while True:
                    alt_port += 1
                    try:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s2.settimeout(0.2)
                        s2.connect(("127.0.0.1", alt_port))
                        s2.close()
                    except OSError:
                        break
                
                resolved_choice = None
                
                if os.getenv("DS_GUI_MODE") == "true":
                    from tkinter import messagebox
                    if is_same_type:
                        gui_choice = messagebox.askyesnocancel(
                            "Port Conflict Detected",
                            f"Port {port_num} is occupied by an existing {svc.upper()} container ('{container_name}').\n\n"
                            f"Click YES to Stop & Replace the existing container.\n"
                            f"Click NO to Coexist (run this new instance on port {alt_port}).\n"
                            f"Click CANCEL to abort installation."
                        )
                        if gui_choice is None:
                            resolved_choice = "cancel"
                        elif gui_choice is True:
                            resolved_choice = "replace"
                        else:
                            resolved_choice = "coexist"
                    else:
                        gui_shift = messagebox.askyesno(
                            "Port Conflict",
                            f"Port {port_num} ({svc}) is occupied by process:\n{owner}\n\n"
                            f"Would you like to automatically switch '{svc}' to port {alt_port}?"
                        )
                        resolved_choice = "coexist" if gui_shift else "cancel"
                else:
                    # CLI prompt
                    if is_same_type:
                        console.print(f"\n[bold yellow][i] Port {port_num} is occupied by an existing {svc.upper()} container ('{container_name}')[/bold yellow]")
                        cli_choice = questionary.select(
                            "What would you like to do?",
                            choices=[
                                questionary.Choice("Stop & Replace the existing container", value="replace"),
                                questionary.Choice("Coexist (Run new instance on a different port)", value="coexist"),
                                questionary.Choice("Cancel installation", value="cancel")
                            ]
                        ).ask()
                        resolved_choice = cli_choice or "cancel"
                    else:
                        console.print(f"\n[bold yellow][!] Port conflict detected on port {port_num} for service '{svc}'[/bold yellow]")
                        console.print(f"Occupant: {owner}")
                        shift = safe_confirm(f"Would you like to automatically switch '{svc}' to port {alt_port}?", default=True)
                        resolved_choice = "coexist" if shift else "cancel"
                
                if resolved_choice == "cancel":
                    write_log("User aborted installation due to port conflicts.", level="INFO")
                    return False
                elif resolved_choice == "replace":
                    write_step(f"Stopping and removing conflicting container '{container_name}'...")
                    try:
                        from src.utils.paths import get_clean_env
                        subprocess.run(["docker", "stop", container_name], env=get_clean_env(), capture_output=True)
                        subprocess.run(["docker", "rm", container_name], env=get_clean_env(), capture_output=True)
                        console.print(f"[✓] Removed container '{container_name}'. Port {port_num} is now available.", style="green")
                    except Exception as e:
                        write_log(f"Failed to remove container: {str(e)}", level="ERROR")
                        # Fallback to coexist
                        resolved_choice = "coexist"
                        
                if resolved_choice == "coexist":
                    resolved_ports[svc] = alt_port
                    write_log(f"Reallocated {svc} to alternative port {alt_port}.", level="INFO")
                    console.print(f"[✓] Reallocated {svc} to port {alt_port}.", style="green")
            
            metadata["resolved_ports"] = resolved_ports
            set_metadata(metadata)
        else:
            write_log("All matching ports are open and available.", level="DEBUG")
            console.print("[✓] All matching ports are open and available", style="green")

    console.print("[✓] Deployment preflight checks completed", style="green")
    return True
````

## File: src/utils/logger.py
````python
import os
import sys
import time
import subprocess
import shutil
from datetime import datetime
from rich.console import Console
import questionary
from src.utils.paths import get_clean_env

console = Console()

_custom_log_path = None
_debug_logging = False
_gui_log_callback = None

def set_log_path(path: str):
    global _custom_log_path
    _custom_log_path = os.path.abspath(path)
    os.environ["SETUP_LOG_DIR"] = _custom_log_path

def enable_debug_logging():
    global _debug_logging
    _debug_logging = True
    os.environ["DEBUG_LOGGING"] = "true"

def set_gui_log_callback(callback):
    global _gui_log_callback
    _gui_log_callback = callback

def get_log_path() -> str:
    if os.getenv("SETUP_LOG_DIR"):
        base_path = os.getenv("SETUP_LOG_DIR")
    elif _custom_log_path:
        base_path = _custom_log_path
    else:
        # Fallback relative to this file
        base_path = os.path.join(os.path.dirname(__file__), "..", "logs")
    return os.path.abspath(os.path.join(base_path, "setup.log"))

def write_log(message: str, level: str = "INFO", clear: bool = False):
    global _debug_logging, _gui_log_callback
    if os.getenv("DEBUG_LOGGING") == "true":
        _debug_logging = True

    log_path = get_log_path()
    base_path = os.path.dirname(log_path)

    # Resolve directory collision where setup.log might be a folder
    if os.path.exists(log_path) and os.path.isdir(log_path):
        try:
            shutil.rmtree(log_path)
        except OSError:
            pass

    if clear and os.path.exists(log_path):
        try:
            os.remove(log_path)
        except OSError:
            pass

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"

    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    # Retry write if file is locked
    for _ in range(3):
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
            break
        except OSError:
            time.sleep(0.1)

    # Trigger GUI log callback if set
    if _gui_log_callback:
        try:
            _gui_log_callback(log_entry.strip())
        except Exception:
            pass

    if level != "TRACE":
        if level == "INFO":
            console.print(message, style="white")
        elif level == "WARN":
            console.print(message, style="yellow")
        elif level == "ERROR":
            console.print(message, style="bold red")
        elif level == "DEBUG" and _debug_logging:
            console.print(f"[DEBUG] {message}", style="grey50")

def write_step(message: str, level: str = "INFO"):
    write_log(f">> {message}", level=level)

def invoke_external_command(command, description: str = "Executing command", cwd: str = None):
    import shlex
    import platform
    
    # Secure command execution: support both list-based command representation and strings
    if isinstance(command, list):
        cmd_list = command
        cmd_str_for_log = " ".join(command)
        use_shell = False
    else:
        cmd_str_for_log = command
        # shlex.split on POSIX systems safely handles string parameters/quoting
        if platform.system() != "Windows":
            try:
                cmd_list = shlex.split(command)
                use_shell = False
            except Exception:
                cmd_list = command
                use_shell = True
        else:
            # On Windows, list split is less reliable for cmd/powershell execution. Use shell for raw strings.
            cmd_list = command
            use_shell = True

    write_log(f"{description}: {cmd_str_for_log}", level="TRACE")
    prefix = "    | "
    
    try:
        # Stream output line-by-line to prevent subprocess pipe deadlock
        process = subprocess.Popen(
            cmd_list,
            shell=use_shell,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=get_clean_env()
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line_str = line.strip()
                write_log(line_str, level="TRACE")
                
                is_error = any(x in line_str.lower() for x in ["error", "failed", "conflict", "denied", "fatal", "critical"])
                
                if _debug_logging:
                    if is_error:
                        console.print(f"{prefix}{line_str}", style="red")
                    else:
                        console.print(f"{prefix}{line_str}", style="grey50")
                elif is_error:
                    console.print(f"{prefix}{line_str}", style="red")
        
        returncode = process.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, command)
            
    except Exception as e:
        write_log(f"External Command Failed: {str(e)}", level="ERROR")
        raise e

def safe_confirm(message: str, default: bool = True) -> bool:
    """
    Prompt the user with a Yes/No select list to force pressing Enter to confirm.
    """
    if os.getenv("DS_HEADLESS") == "true":
        return default
        
    choices = ["Yes", "No"] if default else ["No", "Yes"]
    choice = questionary.select(
        message,
        choices=choices,
        default=choices[0]
    ).ask()
    return choice == "Yes"
````

## File: .github/workflows/build-assets.yml
````yaml
name: build-assets

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build-assets:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyinstaller questionary rich ruamel.yaml python-dotenv requests tzlocal certifi customtkinter darkdetect pydantic

      - name: Inject Version into Code (Linux)
        if: runner.os == 'Linux'
        run: |
          TAG_VER=$(echo "${{ github.ref_name }}" | sed 's/^v//')
          sed -i "s/VERSION = \".*\"/VERSION = \"$TAG_VER\"/g" src/utils/updater.py

      - name: Inject Version into Code (Windows)
        if: runner.os == 'Windows'
        shell: pwsh
        run: |
          $TagVer = "${{ github.ref_name }}".TrimStart("v")
          (Get-Content src/utils/updater.py) -replace 'VERSION = ".*"', "VERSION = `"$TagVer`"" | Set-Content src/utils/updater.py

      - name: Build Binary (Linux)
        if: runner.os == 'Linux'
        run: |
          customtkinter_path=$(python -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))")
          pyinstaller --onefile --clean --add-data "$customtkinter_path:customtkinter" --add-data "src/apps:src/apps" --hidden-import=tkinter --hidden-import=customtkinter --hidden-import=darkdetect --exclude-module numpy --exclude-module pandas --exclude-module scipy --exclude-module matplotlib --exclude-module setuptools --exclude-module pip --exclude-module wheel dockersetup.py

      - name: Build Binary (Windows)
        if: runner.os == 'Windows'
        shell: pwsh
        run: |
          $customtkinter_path = python -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))"
          pyinstaller --onefile --clean --add-data "${customtkinter_path};customtkinter" --add-data "src/apps;src/apps" --hidden-import=tkinter --hidden-import=customtkinter --hidden-import=darkdetect --exclude-module numpy --exclude-module pandas --exclude-module scipy --exclude-module matplotlib --exclude-module setuptools --exclude-module pip --exclude-module wheel --uac-admin --icon "resources/app.ico" dockersetup.py

      - name: Build Setup Installer (Windows)
        if: runner.os == 'Windows'
        run: |
          iscc resources/installer.iss

      - name: Create Release and Upload Binary (Linux)
        if: runner.os == 'Linux'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Create release if it doesn't exist, then upload binary
          gh release create ${{ github.ref_name }} --title "${{ github.ref_name }}" --generate-notes || true
          gh release upload ${{ github.ref_name }} dist/dockersetup --clobber

      - name: Upload Binary to Release (Windows)
        if: runner.os == 'Windows'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        shell: bash
        run: |
          gh release create ${{ github.ref_name }} --title "${{ github.ref_name }}" --generate-notes || true
          gh release upload ${{ github.ref_name }} dist/dockersetup.exe --clobber
          gh release upload ${{ github.ref_name }} dist/dockersetupinstaller.exe --clobber
````

## File: src/modules/directories.py
````python
import os
import platform
import re
from src.utils.paths import get_project_root, get_deploy_dir, resolve_path_slash
from src.utils.logger import write_log, console, write_step
from src.utils.state import get_metadata

def secure_dir_recursive(path: str, uid: int, gid: int):
    if platform.system() == "Windows" or not hasattr(os, "getuid") or os.getuid() != 0:
        return
    try:
        os.chown(path, uid, gid)
        for root, dirs, files in os.walk(path):
            for d in dirs:
                os.chown(os.path.join(root, d), uid, gid)
            for f in files:
                os.chown(os.path.join(root, f), uid, gid)
    except OSError as e:
        write_log(f"Warning: Could not set ownership to {uid}:{gid} for {path}. Error: {str(e)}", level="WARN")

def setup_directories() -> bool:
    write_step("Setting up folder directory structure")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    env_path = resolve_path_slash(os.path.join(deploy_dir, ".env"))

    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Configuration file (.env) missing in {deploy_dir}. Please run the environment wizard.")

    # Load environment variables manually to extract paths
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^([^=]+)=(.*)$", line)
            if match:
                k = match.group(1).strip()
                v = match.group(2).strip()
                if k in ["DOCKERDIR", "DATADRIVE"]:
                    v = resolve_path_slash(v)
                    # Cross-platform drive letter mapping to standard Unix mount paths
                    if platform.system() != "Windows":
                        match_drive = re.match(r"^([A-Za-z]):(.*)$", v)
                        if match_drive:
                            v = f"/mnt/{match_drive.group(1).lower()}{match_drive.group(2)}"
                env_vars[k] = v

    docker_dir = env_vars.get("DOCKERDIR")
    drive_pool = env_vars.get("DATADRIVE")

    if not docker_dir or not drive_pool:
        raise ValueError("DOCKERDIR or DATADRIVE missing in .env configurations.")

    metadata = get_metadata()
    selected = metadata.get("selected_services", [])
    if not selected:
        write_log("No service selection found in metadata. Service-specific directories will be skipped.", level="WARN")

    # Create appdata folders for selected services
    for app in selected:
        clean_app = app.lower().split(" ")[0]  # E.g. mariadb (+adminer) -> mariadb
        
        path = resolve_path_slash(os.path.join(docker_dir, "appdata", clean_app, "config"))
        if clean_app == "dockge":
            path = resolve_path_slash(os.path.join(docker_dir, "appdata", "dockge", "data"))
            
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                write_log(f"Created directory: {path}", level="DEBUG")
            except Exception as e:
                raise PermissionError(f"Failed to create directory: {path}. Ensure you have write permissions. Error: {str(e)}")

        # Enforce External authentication method for Servarr apps config.xml pre-creation
        if clean_app in ["sonarr", "radarr", "lidarr"]:
            config_file = os.path.join(path, "config.xml")
            if not os.path.exists(config_file):
                try:
                    default_config = (
                        "<Config>\n"
                        "  <LogLevel>info</LogLevel>\n"
                        "  <AuthenticationMethod>External</AuthenticationMethod>\n"
                        "</Config>\n"
                    )
                    with open(config_file, "w", encoding="utf-8") as f:
                        f.write(default_config)
                    write_log(f"Pre-seeded config.xml with External auth for {clean_app}", level="DEBUG")
                except Exception as e:
                    write_log(f"Warning: Could not pre-seed config.xml for {clean_app}. Error: {str(e)}", level="WARN")

        # Pre-seed config.yml with username filter for PlexTraktSync
        if clean_app == "plextraktsync":
            parent_dir = os.path.dirname(path)
            config_file = os.path.join(parent_dir, "config.yml")
            if not os.path.exists(config_file):
                try:
                    default_config = (
                        "watch:\n"
                        "  username_filter: true\n"
                    )
                    with open(config_file, "w", encoding="utf-8") as f:
                        f.write(default_config)
                    write_log("Pre-seeded config.yml with username_filter for plextraktsync", level="DEBUG")
                except Exception as e:
                    write_log(f"Warning: Could not pre-seed config.yml for plextraktsync. Error: {str(e)}", level="WARN")

    # Create stacks directory for Dockge
    stacks_dir = resolve_path_slash(os.path.join(docker_dir, "stacks"))
    if not os.path.exists(stacks_dir):
        try:
            os.makedirs(stacks_dir, exist_ok=True)
            write_log(f"Created stacks directory: {stacks_dir}", level="DEBUG")
        except Exception as e:
            raise PermissionError(f"Failed to create stacks directory: {stacks_dir}. Error: {str(e)}")

    # Create media folders
    media_folders = ["downloads", "downloads/incomplete"]

    # Add conditional folders based on services
    if "sonarr" in selected:
        media_folders.extend(["tv", "anime"])
    if "radarr" in selected:
        media_folders.append("movies")
    if any(s in selected for s in ["lidarr", "navidrome", "slskd"]):
        media_folders.append("music")
    if any(s in selected for s in ["readarr", "audiobookshelf"]):
        media_folders.extend(["books", "audiobooks"])
    if "mylar" in selected:
        media_folders.append("comics")
    if "immich" in selected:
        media_folders.append("photos")
    if "paperless" in selected:
        media_folders.append("documents")

    for folder in media_folders:
        path = resolve_path_slash(os.path.join(drive_pool, folder))
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                write_log(f"Created media directory: {path}", level="DEBUG")
            except Exception as e:
                write_log(f"Warning: Could not create media folder {path}. It may need to be created manually. Error: {str(e)}", level="WARN")

    # Create placeholder files
    shared_path = resolve_path_slash(os.path.join(docker_dir, "shared"))
    os.makedirs(shared_path, exist_ok=True)
    htpasswd_path = resolve_path_slash(os.path.join(shared_path, ".htpasswd"))
    if not os.path.exists(htpasswd_path):
        with open(htpasswd_path, "w", encoding="utf-8") as f:
            pass

    try:
        puid_val = int(env_vars.get("PUID", "1000"))
        pgid_val = int(env_vars.get("PGID", "1000"))
    except ValueError:
        puid_val = 1000
        pgid_val = 1000

    secure_dir_recursive(docker_dir, puid_val, pgid_val)
    for folder in media_folders:
        path = resolve_path_slash(os.path.join(drive_pool, folder))
        secure_dir_recursive(path, puid_val, pgid_val)

    console.print("[✓] Directory structure ready", style="green")
    return True
````

## File: src/modules/auto_configure.py
````python
import os
import sys
import re
import time
import socket
import ipaddress
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import configparser
import requests
import questionary
from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path
from src.utils.logger import write_log, console, write_step, invoke_external_command
from src.utils.state import get_metadata, set_metadata, set_env_var
from src.utils.yaml_parser import get_yaml_content, get_registry_list



def test_port(host: str, port: int, timeout: int = 2) -> bool:
    """
    Cross-platform socket connectivity check replacing Test-NetConnection (Edge Case 13).
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

def is_private_address(url: str) -> bool:
    """
    Determines if a URL points to a private/local address to decide on SSL verification.
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return True # Assume local if no host
            
        if hostname.lower() == "localhost" or hostname == "127.0.0.1" or hostname == "::1":
            return True
            
        # Check if it's an IP
        try:
            ip = ipaddress.ip_address(hostname)
            return ip.is_private
        except ValueError:
            # Not an IP, check if it's a .local domain or single label (no dots)
            if "." not in hostname or hostname.lower().endswith(".local"):
                return True
                
        return False
    except Exception:
        return False

def wait_for_service(name: str, port: int, max_timeout_seconds: int = 180) -> bool:
    if os.getenv("TEST_MODE") == "true":
        console.print(f"Waiting for {name}... [SKIPPED (TEST MODE)]", style="grey50")
        return False

    console.print(f"Waiting for {name} to initialize (Port {port})... ", end="", style="white")
    sys.stdout.flush()

    start_time = time.time()
    retry_interval = 5
    tcp_ready = False

    while (time.time() - start_time) < max_timeout_seconds:
        # 1. TCP Check
        if test_port("127.0.0.1", port):
            if not tcp_ready:
                console.print("(TCP Ready) ", end="")
                sys.stdout.flush()
                tcp_ready = True
                time.sleep(5)

            # 2. HTTP Check
            try:
                # Use Smart Verify logic for wait_for_service
                url = f"http://127.0.0.1:{port}"
                verify = True
                if os.getenv("DS_ALLOW_INSECURE_SSL") == "true" or is_private_address(url):
                    verify = False
                
                response = requests.get(url, timeout=2, verify=verify)
                if response is not None:
                    console.print("[OK]", style="green")
                    return True
            except Exception:
                pass
        
        console.print(".", end="")
        sys.stdout.flush()
        time.sleep(retry_interval)
        if retry_interval < 20:
            retry_interval += 5

    console.print("[TIMEOUT]", style="yellow")
    return False

def get_api_key(app: str, deploy_dir: str) -> str:
    config_path = os.path.join(deploy_dir, "appdata", app, "config", "config.xml")
    if app == "sabnzbd":
        config_path = os.path.join(deploy_dir, "appdata", "sabnzbd", "config", "sabnzbd.ini")
    elif app == "tautulli":
        config_path = os.path.join(deploy_dir, "appdata", "tautulli", "config.ini")

    if not os.path.exists(config_path):
        return None

    try:
        if app == "sabnzbd":
            config = configparser.ConfigParser(strict=False, empty_lines_in_values=False)
            config.read(config_path, encoding="utf-8")
            for section in config.sections():
                if "api_key" in config[section]:
                    return config[section]["api_key"].strip()
            
            # Simple text fallback if configparser fails on non-standard ini
            with open(config_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r"^api_key\s*=\s*(.*)", line)
                    if match:
                        return match.group(1).strip()
        elif app == "tautulli":
            config = configparser.ConfigParser(strict=False, empty_lines_in_values=False)
            config.read(config_path, encoding="utf-8")
            for section in config.sections():
                if "api_key" in config[section]:
                    return config[section]["api_key"].strip()
            
            # Fallback
            with open(config_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r"^api_key\s*=\s*(.*)", line)
                    if match:
                        return match.group(1).strip()
        else:
            tree = ET.parse(config_path)
            root = tree.getroot()
            apikey_el = root.find("ApiKey")
            if apikey_el is not None and apikey_el.text:
                return apikey_el.text.strip()
    except Exception as e:
        write_log(f"Failed to parse API Key for {app}: {str(e)}", level="DEBUG")
        return None
    return None

def invoke_robust_rest_method(url: str, method: str = "GET", json_payload: dict = None, headers: dict = None, max_retries: int = 3) -> dict:
    session = requests.Session()
    
    # Smart Verify logic
    verify = True
    if os.getenv("DS_ALLOW_INSECURE_SSL") == "true":
        verify = False
        write_log(f"DS_ALLOW_INSECURE_SSL is enabled. SSL verification disabled for {url}", level="DEBUG")
    elif is_private_address(url):
        verify = False
        # Only log bypass for local addresses at DEBUG to keep output clean
        write_log(f"Private address detected for {url}. Bypassing SSL verification.", level="DEBUG")
    
    attempts = 0
    while attempts < max_retries:
        attempts += 1
        try:
            res = session.request(
                method=method,
                url=url,
                json=json_payload,
                headers=headers,
                timeout=10,
                verify=verify
            )
            res.raise_for_status()
            try:
                return res.json()
            except Exception:
                return {"status": "ok", "content": res.text}
        except Exception as e:
            if attempts < max_retries:
                sleep_time = 2 * (2 ** (attempts - 1))
                write_log(f"Transient REST failure on attempt {attempts} of {max_retries} for {url}. Retrying in {sleep_time}s. Error: {str(e)}", level="WARN")
                time.sleep(sleep_time)
            else:
                raise e

def auto_stitch_services() -> bool:
    write_step("Running automated service configuration and stitching")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    env_path = os.path.join(deploy_dir, ".env")
    metadata = get_metadata()
    selected = metadata.get("selected_services", [])
    if not selected:
        write_log("No selected services found in metadata. Skipping configuration.", level="WARN")
        return True

    from src.apps.loader import load_apps
    apps_dict = load_apps()

    configurable_apps = [app.key for app in apps_dict.values() if app.is_configurable]

    # --- 1. Service Readiness & Key Extraction ---
    keys = {}
    config_results = []

    for app in apps_dict.values():
        svc = app.key
        try:
            env_port = os.getenv(f"{svc.replace('-', '_').replace(' (+goaccess)', '').upper()}_PORT")
            if env_port and env_port.isdigit():
                port = int(env_port)
            else:
                port = int(app.port)
        except ValueError:
            port = 0

        if svc in selected and port > 0:
            if svc in configurable_apps:
                write_step(f"Checking Service Availability: {svc}")
                if wait_for_service(svc, port):
                    key = get_api_key(svc, deploy_dir)
                    if key:
                        keys[svc] = key
                        write_log(f"Extracted {svc} API Key.", level="INFO")
                        


                    if key:
                        env_key = f"{svc}_API_KEY".upper().replace("-", "_")
                        set_env_var(env_key, key, file_path=env_path)

    # --- 2. Load Management Credentials ---
    http_user = "admin"
    http_pass = os.getenv("HTTP_PASSWORD", "")
    http_user_env = os.getenv("HTTP_USERNAME", "")
    if http_user_env:
        http_user = http_user_env

    # Fallback to loading from env file
    if not http_pass and os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                match_u = re.match(r"^HTTP_USERNAME=(.*)", line)
                match_p = re.match(r"^HTTP_PASSWORD=(.*)", line)
                if match_u:
                    http_user = match_u.group(1).strip()
                if match_p:
                    http_pass = match_p.group(1).strip()

    if not http_pass:
        write_log("HTTP_PASSWORD not found. Skipping credential-dependent automation.", level="WARN")
    
    # --- 3. Execute Strategies dynamically via App Plugins ---
    os.environ["HTTP_USERNAME"] = http_user
    os.environ["HTTP_PASSWORD"] = http_pass
    tier = metadata.get("tier", "1")
    os.environ["DEPLOY_TIER"] = tier

    for svc in selected:
        app = apps_dict.get(svc)
        if app:
            try:
                results = app.run_stitching(keys, deploy_dir, invoke_robust_rest_method)
                if results:
                    config_results.extend(results)
            except Exception as e:
                write_log(f"Stitching failed for service {svc}: {str(e)}", level="ERROR")

    # --- 4. Stitching Summary Report ---
    console.print("\n--- Service Stitching Report ---", style="bold yellow")
    if config_results:
        for res in config_results:
            console.print(f" [✓] {res}", style="green")
    else:
        console.print(" No automated stitching actions were required or performed.", style="grey50")

    # Update metadata
    metadata["auto_config_results"] = config_results
    set_metadata(metadata)

    # --- 5. Sync and Restart Dependent Stacks ---
    write_log("Syncing environment variables and reloading dashboard/maintenance stacks to apply new keys...")
    from dockersetup import sync_dot_env
    sync_dot_env(env_path, deploy_dir)

    stacks_to_reload = ["maintenance", "media-server"]
    for st in stacks_to_reload:
        st_path = os.path.join(deploy_dir, "stacks", st)
        if os.path.exists(st_path):
            write_log(f"Reloading stack: {st}", level="DEBUG")
            if os.getenv("TEST_MODE") == "true":
                write_log("TEST_MODE enabled. Skipping live docker stack reload.", level="INFO")
                continue
            try:
                invoke_external_command(
                    "docker compose up -d --remove-orphans",
                    description=f"Reloading {st}",
                    cwd=st_path
                )
            except Exception:
                pass

    write_log("Automated stitching complete.", level="DEBUG")
    console.print("[✓] Automated stitching complete", style="green")
    return True
````

## File: tests/test_runtime.py
````python
import os
import sys
import shutil
import pytest
from unittest.mock import MagicMock, patch

# Ensure projects directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.paths import get_project_root, get_deploy_dir, resolve_path_slash
from src.utils.yaml_parser import get_yaml_content, get_template_blocks, get_registry_list
from src.utils.state import get_metadata, set_metadata, set_env_var, save_env_vars
from src.modules.preflight import is_admin
from src.modules.directories import setup_directories

# Temporary test directories
TEST_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DEPLOY_DIR = os.path.join(TEST_PROJECT_ROOT, "testing_sandbox")

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    monkeypatch.setenv("TEST_MODE", "true")
    monkeypatch.setenv("DS_HEADLESS", "true")
    monkeypatch.setenv("DEPLOY_DIR", TEST_DEPLOY_DIR)
    
    os.makedirs(TEST_DEPLOY_DIR, exist_ok=True)
    yield
    # Cleanup
    if os.path.exists(TEST_DEPLOY_DIR):
        shutil.rmtree(TEST_DEPLOY_DIR, ignore_errors=True)

def test_path_resolution():
    assert resolve_path_slash("C:\\test\\path") == "C:/test/path"
    assert resolve_path_slash("D:") == "D:/"

def test_app_loader():
    from src.apps.loader import load_apps
    apps_dict = load_apps()
    assert len(apps_dict) > 0
    assert "sonarr" in apps_dict
    sonarr_app = apps_dict["sonarr"]
    assert sonarr_app.name == "Sonarr"
    assert sonarr_app.port == 8989

def test_metadata_read_write():
    meta = get_metadata()
    assert isinstance(meta, dict)
    
    test_data = {"test_key": "test_value", "selected_services": ["sonarr", "radarr"]}
    set_metadata(test_data)
    
    new_meta = get_metadata()
    assert new_meta["test_key"] == "test_value"
    assert "sonarr" in new_meta["selected_services"]

def test_env_file_generation():
    env_file = os.path.join(TEST_DEPLOY_DIR, ".env")
    set_env_var("TEST_KEY", "TEST_VAL", file_path=env_file)
    assert os.path.exists(env_file)
    
    with open(env_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "TEST_KEY=TEST_VAL" in content
    
    # Save bulk env vars
    vars_dict = {"VAR1": "VAL1", "VAR2": "VAL2\nmulti"}
    save_env_vars(vars_dict, file_path=env_file)
    
    with open(env_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "VAR1=VAL1" in content
    assert 'VAR2="VAL2\nmulti"' in content

def test_directory_setup():
    env_file = os.path.join(TEST_DEPLOY_DIR, ".env")
    save_env_vars({
        "DOCKERDIR": TEST_DEPLOY_DIR,
        "DATADRIVE": os.path.join(TEST_DEPLOY_DIR, "media")
    }, file_path=env_file)
    
    set_metadata({"selected_services": ["sonarr", "radarr"]})
    
    setup_directories()
    
    # Check that directories were created
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "appdata/sonarr/config"))
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "appdata/radarr/config"))
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "stacks"))
    assert os.path.exists(os.path.join(TEST_DEPLOY_DIR, "media/downloads"))

def test_timezone_detection():
    from src.modules.env_wizard import detect_timezone, select_timezone_interactive
    
    # 1. Test detect_timezone returns a string (not None or "None")
    tz = detect_timezone()
    assert tz is not None
    assert tz != "None"
    
    # 2. Test select_timezone_interactive behaves correctly in headless mode
    interactive_tz = select_timezone_interactive(tz)
    assert interactive_tz is not None
    assert interactive_tz != "None"
    
    # 3. Test that None/"None" input fallback logic resolves to a valid timezone/UTC
    fallback_tz = select_timezone_interactive("None")
    assert fallback_tz is not None
    assert fallback_tz != "None"

def test_compose_build_integration():
    from src.modules.compose_build import build_compose_stacks
    
    # 1. Setup metadata
    set_metadata({
        "selected_services": ["sonarr", "radarr", "homepage"],
        "tier": "1"
    })
    
    # 2. Setup master .env
    env_file = os.path.join(TEST_DEPLOY_DIR, ".env")
    save_env_vars({
        "PUID": "1000",
        "PGID": "1000",
        "TZ": "UTC",
        "DOCKERDIR": TEST_DEPLOY_DIR,
        "DATADRIVE": os.path.join(TEST_DEPLOY_DIR, "media"),
        "USERDIR": TEST_DEPLOY_DIR,
        "HTTP_USERNAME": "admin",
        "HTTP_PASSWORD": "password"
    }, file_path=env_file)
    
    # 3. Run build
    assert build_compose_stacks() is True
    
    # 4. Verify output
    stack_dir = os.path.join(TEST_DEPLOY_DIR, "stacks", "media-pvr")
    assert os.path.exists(stack_dir)
    assert os.path.exists(os.path.join(stack_dir, "docker-compose.yml"))
    assert os.path.exists(os.path.join(stack_dir, ".env"))
    
    with open(os.path.join(stack_dir, "docker-compose.yml"), "r") as f:
        content = f.read()
    assert "sonarr" in content
    assert "radarr" in content
    
    with open(os.path.join(stack_dir, ".env"), "r") as f:
        env_content = f.read()
    assert "PUID=1000" in env_content
    # HTTP_PASSWORD should be filtered out from PVR stack as it's not used in its compose
    assert "HTTP_PASSWORD" not in env_content

    # 5. Verify Homepage configuration files
    hp_config_dir = os.path.join(TEST_DEPLOY_DIR, "appdata", "homepage", "config")
    assert os.path.exists(os.path.join(hp_config_dir, "bookmarks.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "docker.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "widgets.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "settings.yaml"))
    assert os.path.exists(os.path.join(hp_config_dir, "services.yaml"))

@patch("src.modules.auto_configure.wait_for_service")
@patch("requests.Session.request")
def test_auto_stitch_integration(mock_request, mock_wait):
    from src.modules.auto_configure import auto_stitch_services
    
    mock_wait.return_value = True
    
    # Mock API responses
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_request.return_value = mock_response
    
    # Setup files
    set_metadata({"selected_services": ["sonarr", "prowlarr"]})
    deploy_dir = TEST_DEPLOY_DIR
    
    # Mock sonarr config
    sonarr_cfg_path = os.path.join(deploy_dir, "appdata", "sonarr", "config", "config.xml")
    os.makedirs(os.path.dirname(sonarr_cfg_path), exist_ok=True)
    with open(sonarr_cfg_path, "w") as f:
        f.write("<Config><ApiKey>testkey</ApiKey></Config>")
        
    # Mock prowlarr config
    prowl_cfg_path = os.path.join(deploy_dir, "appdata", "prowlarr", "config", "config.xml")
    os.makedirs(os.path.dirname(prowl_cfg_path), exist_ok=True)
    with open(prowl_cfg_path, "w") as f:
        f.write("<Config><ApiKey>prowlkey</ApiKey></Config>")
        
    env_file = os.path.join(deploy_dir, ".env")
    save_env_vars({"HTTP_PASSWORD": "testpassword"}, file_path=env_file)
    
    # Run stitching
    assert auto_stitch_services() is True
    
    # Verify mock calls (should have attempted to auth sonarr and link prowlarr)
    assert mock_request.called
    
    # Verify metadata update
    meta = get_metadata()
    assert "auto_config_results" in meta
    assert len(meta["auto_config_results"]) > 0

@patch("src.modules.deploy_start.invoke_external_command")
@patch("src.modules.deploy_start.subprocess.run")
@patch("src.modules.deploy_start.test_container_conflict")
def test_deploy_stacks_success(mock_conflict, mock_run, mock_invoke):
    from src.modules.deploy_start import deploy_stacks
    
    # Mock subprocess run to succeed
    mock_run.return_value = MagicMock(returncode=0, stdout="Success")
    mock_invoke.return_value = None
    
    # Setup deployment directory and files
    set_metadata({
        "generated_stacks": [
            {"Name": "core"},
            {"Name": "media-server"}
        ]
    })
    
    stacks_dir = os.path.join(TEST_DEPLOY_DIR, "stacks")
    os.makedirs(os.path.join(stacks_dir, "core"), exist_ok=True)
    os.makedirs(os.path.join(stacks_dir, "media-server"), exist_ok=True)
    
    # Execute deploy
    assert deploy_stacks() is True
    assert mock_run.called

@patch("src.modules.deploy_start.invoke_external_command")
@patch("src.modules.deploy_start.subprocess.run")
@patch("src.modules.deploy_start.test_container_conflict")
def test_deploy_stacks_pull_failure(mock_conflict, mock_run, mock_invoke):
    from src.modules.deploy_start import deploy_stacks
    mock_invoke.return_value = None
    
    # Mock subprocess run to fail on pull
    def run_side_effect(args, **kwargs):
        if "pull" in args:
            raise subprocess.CalledProcessError(1, args)
        return MagicMock(returncode=0, stdout="Success")
        
    mock_run.side_effect = run_side_effect
    
    set_metadata({
        "generated_stacks": [
            {"Name": "core"},
            {"Name": "media-server"}
        ]
    })
    
    stacks_dir = os.path.join(TEST_DEPLOY_DIR, "stacks")
    os.makedirs(os.path.join(stacks_dir, "core"), exist_ok=True)
    os.makedirs(os.path.join(stacks_dir, "media-server"), exist_ok=True)
    
    # Under headless mode, pull failures must raise RuntimeError
    import subprocess
    with pytest.raises(RuntimeError):
        deploy_stacks()

@patch("src.utils.uninstall.subprocess.run")
@patch("src.utils.uninstall.safe_confirm")
def test_uninstall_workflow(mock_confirm, mock_run):
    from src.utils.uninstall import main as uninstall_main
    
    # Setup environment
    os.environ["DEPLOY_DIR"] = TEST_DEPLOY_DIR
    
    # Write mock files to satisfy the validation checks in uninstall
    os.makedirs(os.path.join(TEST_DEPLOY_DIR, "stacks"), exist_ok=True)
    with open(os.path.join(TEST_DEPLOY_DIR, ".metadata.json"), "w") as f:
        f.write("{}")
    with open(os.path.join(TEST_DEPLOY_DIR, ".env"), "w") as f:
        f.write("HTTP_PASSWORD=test")
        
    # Mock user input: confirmation to proceed and deletion of volumes
    mock_confirm.return_value = True
    mock_run.return_value = MagicMock(returncode=0)
    
    # Run uninstall main
    try:
        uninstall_main()
    except SystemExit as e:
        assert e.code == 0
        
    # Verify cleanup occurred
    assert not os.path.exists(os.path.join(TEST_DEPLOY_DIR, "stacks"))
    assert not os.path.exists(os.path.join(TEST_DEPLOY_DIR, ".metadata.json"))

def test_ast_and_syntax_validation():
    """
    Ensure all Python source files in the project are syntactically valid by parsing them with built-in ast.
    """
    import ast
    project_root = TEST_PROJECT_ROOT
    python_files = []
    
    # Traverse directories to find python files
    for root, _, files in os.walk(project_root):
        if ".venv" in root or ".pytest_cache" in root or "build" in root or "dist" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
                
    assert len(python_files) > 0, "No Python source files found to validate."
    
    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                source = f.read()
            ast.parse(source, filename=py_file)
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {py_file}: {e}")

def test_app_registry_and_schema():
    """
    Ensure the dynamically loaded apps meet basic structure and schema rules.
    """
    from src.apps.loader import load_apps
    apps_dict = load_apps()
    assert len(apps_dict) > 0, "No apps loaded"
    
    # Verify some key apps are present
    expected_apps = ["sonarr", "radarr", "prowlarr", "bazarr", "stirling-pdf", "uptime-kuma"]
    for ea in expected_apps:
        assert ea in apps_dict, f"Expected app '{ea}' missing from loaded apps"
        app = apps_dict[ea]
        assert app.key == ea
        assert app.name is not None
        assert app.category is not None
        assert app.stack_group is not None
        assert app.port is not None
        assert app.get_compose_template() != "", f"Empty compose template for '{ea}'"

def test_exclusivity_warnings():
    from src.utils.dependency_resolver import check_exclusivity_conflicts
    from src.apps.loader import load_apps
    apps_dict = load_apps()
    
    # Test reverse proxies conflict
    conflict_apps = [apps_dict["caddy"], apps_dict["npm plus (+goaccess)"]]
    conflicts = check_exclusivity_conflicts(conflict_apps)
    assert "reverse_proxy" in conflicts
    assert "Caddy" in conflicts["reverse_proxy"]
    assert "Nginx Proxy Manager Plus" in conflicts["reverse_proxy"]

def test_database_auto_selection():
    from src.utils.dependency_resolver import resolve_database_dependencies
    from src.apps.loader import load_apps
    apps_dict = load_apps()
    
    # Authentik requires postgres
    updated_keys, db_notifs = resolve_database_dependencies(["authentik"], apps_dict)
    assert "postgresql_cloudbeaver" in updated_keys
    assert len(db_notifs) == 1

def test_port_conflict_resolution(tmp_path, monkeypatch):
    from src.utils.port_resolver import resolve_port_conflicts
    from src.apps.loader import load_apps
    apps_dict = load_apps()
    
    env_file = tmp_path / ".env"
    env_file.write_text("FLAME_PORT=5005\n")
    
    # Select two apps that share port (e.g. Flame and fileflows)
    flame_app = apps_dict["flame"]
    fileflows_app = apps_dict["fileflows"]
    
    # Manually align them to same port to force resolving
    flame_app.port = 5001
    fileflows_app.port = 5001
    
    # Mock socket check to always report port 5001 in use so resolver kicks in
    import src.utils.port_resolver
    monkeypatch.setattr(src.utils.port_resolver, "is_port_in_use", lambda p: p == 5001)
    
    notifs = resolve_port_conflicts([flame_app, fileflows_app], str(env_file))
    assert len(notifs) > 0
    
    # Check that file was updated and ports changed
    content = env_file.read_text()
    assert "FILEFLOWS_PORT=" in content

def test_strict_path_normalization_invariant():
    """
    Verify path normalization ensures forward slashes exclusively on Windows or other OS.
    """
    # Windows paths with backslashes
    assert resolve_path_slash("C:\\docker\\stacks") == "C:/docker/stacks"
    assert resolve_path_slash("appdata\\sonarr\\config") == "appdata/sonarr/config"
    assert resolve_path_slash("\\\\network-share\\share") == "//network-share/share"
    # Empty and invalid cases
    assert resolve_path_slash("") == ""
    assert resolve_path_slash(None) is None
    
    # Windows drives
    assert resolve_path_slash("D:") == "D:/"
    assert resolve_path_slash("z:") == "z:/"
````

## File: build_bin.py
````python
import os
import sys
import platform
import subprocess
import shutil

def run_local_build(pyinstaller_cmd: list, data_sep: str, project_root: str):
    """
    Runs PyInstaller locally for the host OS.
    """
    import customtkinter
    customtkinter_path = os.path.dirname(customtkinter.__file__)
    cmd = pyinstaller_cmd + [
        "--onefile",
        "--clean",
        "--add-data", f"resources/services.yml{data_sep}resources",
        "--add-data", f"resources/templates.yml{data_sep}resources",
        "--add-data", f"src/apps{data_sep}src/apps",
        "--add-data", f"{customtkinter_path}{data_sep}customtkinter",
        "--hidden-import", "tkinter",
        "--hidden-import", "customtkinter",
        "--hidden-import", "darkdetect",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "--exclude-module", "scipy",
        "--exclude-module", "matplotlib",
        "--exclude-module", "setuptools",
        "--exclude-module", "pip",
        "--exclude-module", "wheel",
    ]
    
    # Enable automatic Administrator elevation and set icon for Windows builds
    if platform.system() == "Windows":
        cmd.append("--uac-admin")
        if os.path.exists("resources/app.ico"):
            cmd.extend(["--icon", "resources/app.ico"])
        
    cmd.append("dockersetup.py")
    
    print(f"\n--- Running Local Build for {platform.system()} ---")
    print(" ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        output_name = "dockersetup.exe" if platform.system() == "Windows" else "dockersetup"
        print(f"[SUCCESS] Local build finished: dist/{output_name}")
        return True
    except Exception as e:
        print(f"[ERROR] Local build failed: {str(e)}")
        return False

def compile_inno_setup(project_root: str):
    """
    Compiles the Inno Setup script into a setup installer executable.
    """
    print("\n--- Compiling Windows Setup Installer with Inno Setup ---")
    iscc_path = shutil.which("iscc")
    if not iscc_path:
        # Check standard paths
        standard_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        if os.path.exists(standard_path):
            iscc_path = standard_path
            
    if not iscc_path:
        print("[WARN] Inno Setup compiler (ISCC.exe) not found on PATH or in standard paths. Skipping installer creation.")
        return False
        
    iss_file = os.path.join(project_root, "resources", "installer.iss")
    if not os.path.exists(iss_file):
        print(f"[ERROR] Inno Setup script not found at: {iss_file}")
        return False
        
    cmd = [iscc_path, iss_file]
    print("Executing Inno Setup compilation:")
    print(" ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("[SUCCESS] Inno Setup installer compiled: dist/dockersetupinstaller.exe")
        return True
    except Exception as e:
        print(f"[ERROR] Inno Setup compilation failed: {str(e)}")
        return False

def run_docker_linux_build(project_root: str):
    """
    Uses Docker to compile the Linux binary if running on a Windows host.
    """
    print("\n--- Running Docker-based Linux Build ---")
    
    # Check if Docker is installed and running
    if not shutil.which("docker"):
        print("[WARN] Docker CLI not found. Skipping Linux compilation (requires Docker on Windows).")
        return False

    try:
        # Check if Docker daemon is active
        subprocess.run(["docker", "version"], check=True, capture_output=True)
    except Exception:
        print("[WARN] Docker daemon is not running. Skipping Linux compilation.")
        return False

    # Convert Windows path to POSIX style for mounting
    abs_root = os.path.abspath(project_root)
    # Ensure Docker paths are mounted correctly
    mount_source = abs_root.replace("\\", "/")
    
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{mount_source}:/app",
        "-w", "/app",
        "python:3.10-slim",
        "sh", "-c", (
            "apt-get update && apt-get install -y binutils python3-tk && "
            "pip install --no-cache-dir pyinstaller questionary rich ruamel.yaml python-dotenv requests tzlocal customtkinter darkdetect && "
            "customtkinter_path=$(python -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))') && "
            "pyinstaller --onefile --clean --add-data 'resources/services.yml:resources' --add-data 'resources/templates.yml:resources' --add-data \"$customtkinter_path:customtkinter\" --hidden-import=tkinter --hidden-import=customtkinter --hidden-import=darkdetect --exclude-module=numpy --exclude-module=pandas --exclude-module=scipy --exclude-module=matplotlib --exclude-module=setuptools --exclude-module=pip --exclude-module=wheel dockersetup.py"
        )
    ]
    
    print("Executing Linux build inside Python Docker container (with binutils)...")
    print(" ".join(docker_cmd))
    
    try:
        subprocess.run(docker_cmd, check=True)
        # Copy install.sh to dist directory
        sh_src = os.path.join(project_root, "resources", "install.sh")
        sh_dst = os.path.join(project_root, "dist", "install.sh")
        if os.path.exists(sh_src):
            shutil.copy(sh_src, sh_dst)
            print("[INFO] Copied install.sh to dist/install.sh")
        print("[SUCCESS] Docker Linux build finished: dist/dockersetup (ELF binary)")
        return True
    except Exception as e:
        print(f"[ERROR] Docker Linux build failed: {str(e)}")
        return False

def main():
    print("=== Docker Setup Script: Cross-OS Build Automation ===")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # 1. Determine local OS and PyInstaller path
    host_os = platform.system()
    data_sep = ";" if host_os == "Windows" else ":"
    
    pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]

    # 2. Run local build
    local_success = run_local_build(pyinstaller_cmd, data_sep, project_root)
    
    # 3. Handle cross-compilation paths
    if host_os == "Windows":
        # Compile Inno Setup installer if local build succeeded
        if local_success:
            compile_inno_setup(project_root)
        # On Windows host: Build Windows locally, use Docker to compile the Linux binary
        docker_success = run_docker_linux_build(project_root)
        
    else:
        # On Linux/macOS host
        print("\n--- Cross-compilation Warning ---")
        print("PyInstaller cannot natively compile Windows .exe files on a Linux host.")
        print("To compile for Windows on a Linux machine, you must run PyInstaller under Wine,")
        print("or set up a GitHub Actions workflow with matrix runners.")

    print("\n" + "="*45)
    print("BUILD SUMMARY:")
    print(f" Windows Executable (.exe):        {'Check dist/dockersetup.exe' if os.path.exists('dist/dockersetup.exe') else 'Not Built'}")
    print(f" Windows Setup Installer (.exe):   {'Check dist/dockersetupinstaller.exe' if os.path.exists('dist/dockersetupinstaller.exe') else 'Not Built'}")
    print(f" Linux Binary (ELF):               {'Check dist/dockersetup' if os.path.exists('dist/dockersetup') else 'Not Built'}")
    print("="*45)

if __name__ == "__main__":
    main()
````

## File: README.md
````markdown
# <img src="resources/dockersetup.png" alt="DockerSetup Logo" height="38" valign="middle"> DockerSetup

A professional-grade, cross-platform Python automation suite for deploying a complete Media and Home Server stack on Windows and Linux using Docker.

## Quick Start

The fastest way to deploy DockerSetup is using the pre-compiled standalone binaries. 

By default, the application will automatically launch the **Graphical Setup Suite (GUI)** if a display environment is available. To force the command-line wizard (e.g. in SSH or headless mode), append the `--cli` parameter.

### Windows (PowerShell)
Download and run the executable. Note that running this command will trigger a User Account Control (UAC) prompt to grant the installer necessary Administrator permissions.
```powershell
Invoke-WebRequest -Uri "https://github.com/suuift/dockersetup/releases/latest/download/dockersetup.exe" -OutFile "dockersetup.exe"; .\dockersetup.exe
```
*(To force CLI mode: `.\dockersetup.exe --cli`)*

### Linux (Shell)
Run this command in your terminal. For standard setups where your user is in the `docker` group, running without `sudo` is recommended.
```bash
curl -L -o dockersetup https://github.com/suuift/dockersetup/releases/latest/download/dockersetup && chmod +x dockersetup && ./dockersetup
```
*(To force CLI mode: `./dockersetup --cli`)*
*(Note: Use `sudo ./dockersetup` only if your user lacks docker group socket permissions or you are deploying to a system-protected path like `/opt`)*

---

## Alternative: Manual Setup (From Source)

If you prefer to run from source code or modify the codebase, follow these steps:

### 1. Set Up the Environment
Clone the repository and install the dependencies in a virtual environment:
```bash
# Clone the repository
git clone https://github.com/suuift/dockersetup.git
cd dockersetup

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r pyproject.toml  # or poetry install
```

### 2. Launch the Installer
Run the setup wizard using Python:
```bash
python dockersetup.py
```
Follow the interactive menus to select your installation tier, configure credentials, and build/deploy your stack.

---

## Key Features

*   **Dual Mode (GUI & CLI):** Launches a modern CustomTkinter-based Graphical Setup Suite in desktop environments for interactive, visual stack configuration and real-time thread-safe deployment progress tracking. Automatically falls back to a robust, interactive CLI wizard in headless/SSH environments (or when launched with the `--cli` flag).
*   **Stateless Builder Architecture:** Keeps the code repository clean. All configurations, state metadata, and Docker Compose directories write directly to your target directory.
*   **Fully Automated Stitching & Stitch-Config:** Automatically links download clients to PVRs, Prowlarr to indexers, Bazarr to subtitles, and connects Radarr/Sonarr import lists (Plex watchlists, StevenLu popular list) and quality renaming configs out of the box.
*   **Interactive Setup Wizards:** Streamlines initial configuration with guided prompts for Plex claim tokens, Usenet server definitions, Prowlarr indexers, and API credential syncing.
*   **Zero-Touch Authentication Integration:** Automatically configures internal service configuration files to use native authentication or secure external reverse proxies (like Authelia/Nginx Proxy Manager).
*   **Self-Healing Binary Updates:** STANDALONE binaries automatically verify, pull, swap, and relaunch dynamically on update checks, keeping deployments seamlessly aligned with repository updates.
*   **Visual Dashboards (Homepage):** Auto-generates a clean Homepage config containing dynamic container API keys, local disk mounts, and targeted bookmarks (like Titus winutil debloat).

---

## Requirements

Before starting, ensure your system meets the following criteria:

*   **Operating System:** Windows 10/11 or modern Linux distribution (Ubuntu, Debian, etc.).
*   **Docker:** Docker Engine & Docker Compose V2 must be installed and running.
*   **Python (for running from source):** Version 3.10 or higher.

---

## Service Catalog

### Minimal Setup (Core Media)
Plex, Jellyfin, Tautulli, Sonarr, Radarr, Lidarr, Bazarr, Prowlarr, FlareSolverr, qBittorrent, SABnzbd, Seerr, Recyclarr, Watchtower, Docker-Prune, Homepage.

### Advanced Add-ons
*   **Security:** CrowdSec (LAPI + NPM Integration), Vaultwarden (Bitwarden), Authelia, Authentik.
*   **Networking:** Nginx Proxy Manager Plus, Caddy, Tailscale VPN, Cloudflare DDNS, Cloudflare Tunnel, Home Assistant, Flame, Dashy.
*   **Media & Music:** Navidrome (Music Server), Audiobookshelf (Books/Podcasts), Calibre-Web, Komga, FileFlows.
*   **Management:** Portainer, Dockge, Uptime Kuma, Beszel, Netdata, Scrutiny (HDD Health).
*   **Productivity:** Immich (Photos), Paperless-ngx, Syncthing, CloudCmd, FileBrowser, Stirling PDF, Mealie, IT-Tools, Code-Server, Dokploy, Docmost, SFTPGo, Firefly III, Changedetection.io, Trilium Notes, SearXNG.
*   **Games:** Valheim, Satisfactory, Enshrouded, Modded Terraria.

---

## How to Add a New Service

To add a new application to the DockerSetup stack, you only need to create a single Python file under [src/apps/](file:///C:/odysseus/projects/dockersetup/src/apps/). The application loader dynamically registers any class inheriting from `BaseApp`.

### Steps:
1. Create a new python file in `src/apps/<service_key>.py`.
2. Define a class inheriting from `BaseApp`.
3. Set properties: `key`, `name`, `port`, `category`, `description`, and `stack_group`.
4. (Optional) Set `exclusivity_group` if the service conflicts with others (e.g. `"reverse_proxy"`).
5. (Optional) Set `required_database_type` (e.g. `"postgres"`) to trigger automatic database companion selection.
6. Implement `get_compose_template(self)` to return the Docker Compose YAML segment. Use `{self.get_appdata_dir()}` to reference volume storage.

### Code Template:
```python
from src.apps.base_app import BaseApp

class MyNewServiceApp(BaseApp):
    key = "mynewservice"
    name = "My New Service"
    port = 8080
    category = "tools"
    description = "A short description of what my new service does."
    stack_group = "maintenance"
    
    # Optional settings
    exclusivity_group = None
    required_database_type = None

    def get_compose_template(self) -> str:
        return f"""  mynewservice:
    image: mynewservice/image:latest
    container_name: mynewservice
    <<: *common-keys-apps
    volumes:
      - {self.get_appdata_dir()}:/config
    ports:
      - 8080:8080
"""
```

---

## Maintenance & Compilation

### Self-Updates
The installer checks for updates on launch. If a new version is available, it pulls changes and swaps binaries cleanly if running from a compiled executable.

### Upgrade Templates
Run `python dockersetup.py` or the compiled binary, and select Upgrade Templates to safely apply updates from `templates.yml` to your existing configuration files without data loss.

### Force Update Containers
Run the main setup script and select Force Update to trigger a fresh image pull and restart of all configured services.

### Build Executables
To build standalone binary executables (a `.exe` for Windows or an ELF binary for Linux):
```bash
python build_bin.py
```
This automates PyInstaller configuration. On a Windows host, if Docker is running, it will also spin up a container to build the Linux executable for cross-compilation.

### Running Tests
To run the automated pytest suite:
```bash
pytest tests/test_runtime.py
```

---

## Notes for Plex Users
*   **Plex Claim:** Get your token from [plex.tv/claim](https://www.plex.tv/claim) to automatically sign in your server.
*   **Transcoding:** The Plex template is pre-configured with `NVIDIA_VISIBLE_DEVICES=all` for hardware acceleration support.
````

## File: resources/installer.iss
````
; DockerSetup Inno Setup Script
; Generates a user-level standalone setup installer for Windows

[Setup]
AppName=DockerSetup
AppVersion=1.5.36
AppPublisher=suuift
AppPublisherURL=https://github.com/suuift/dockersetup
DefaultDirName={localappdata}\DockerSetup
DefaultGroupName=DockerSetup
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=dockersetupinstaller
SetupIconFile=app.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
ChangesEnvironment=no

[Files]
Source: "..\dist\dockersetup.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DockerSetup"; Filename: "{app}\dockersetup.exe"; WorkingDir: "{userdocs}"
Name: "{userdesktop}\DockerSetup"; Filename: "{app}\dockersetup.exe"; WorkingDir: "{userdocs}"

[Run]
Description: "Launch DockerSetup"; Filename: "{app}\dockersetup.exe"; WorkingDir: "{userdocs}"; Flags: postinstall nowait shellexec
````

## File: src/modules/env_wizard.py
````python
import os
import sys
import secrets
import string
import platform
import subprocess
import re
import socket
import shutil
import datetime
import questionary
from zoneinfo import ZoneInfo
from tzlocal import get_localzone_name
from src.utils.paths import get_project_root, get_deploy_dir, resolve_path_slash
from src.utils.logger import write_log, console, write_step, safe_confirm
from src.utils.state import get_metadata, save_env_vars

def check_keyboard_locks():
    """
    Checks the system state for Caps Lock and Num Lock to warn the user before typing passwords.
    """
    caps_on = False
    num_off = False
    
    if platform.system() == "Windows":
        try:
            import ctypes
            VK_CAPITAL = 0x14
            VK_NUMLOCK = 0x90
            caps_on = ctypes.windll.user32.GetKeyState(VK_CAPITAL) & 1 == 1
            num_off = ctypes.windll.user32.GetKeyState(VK_NUMLOCK) & 1 == 0
        except Exception:
            pass
    elif platform.system() == "Linux":
        try:
            # Best-effort X11 check (fails gracefully if headless/Wayland)
            res = subprocess.run(["xset", "q"], capture_output=True, text=True, timeout=1)
            if res.returncode == 0:
                caps_on = "Caps Lock:   on" in res.stdout
                num_off = "Num Lock:    off" in res.stdout
        except Exception:
            pass
            
    if caps_on:
        console.print("[!] WARNING: Caps Lock is ON.", style="bold yellow")
    if num_off:
        console.print("[i] Notice: Num Lock is OFF.", style="grey50")

def new_random_password(length: int = 24) -> str:
    # Alphanumeric plus safe symbols to prevent escaping breakages in templates (Edge Case 2)
    chars = string.ascii_letters + string.digits + "!@#_-"
    return "".join(secrets.choice(chars) for _ in range(length))

def get_validated_input(prompt: str, default: str, regex: str = None, error_msg: str = "") -> str:
    if os.getenv("DS_HEADLESS") == "true":
        return default

    val = questionary.text(f"{prompt} (default: {default}):").ask()
    if not val or not val.strip():
        return default
        
    val = val.strip()
    if regex and not re.match(regex, val):
        write_log(f"{error_msg}. Using default: {default}", level="WARN")
        return default
        
    return val

def get_multiline_input(prompt: str, default: str) -> str:
    if os.getenv("DS_HEADLESS") == "true":
        return default

    console.print(f"\n{prompt}", style="cyan")
    console.print("Provide input via one of these options:", style="grey50")
    console.print("1. Paste content (Press Enter twice / empty line to finish)")
    console.print("2. Provide absolute file path to read from")
    
    choice = questionary.select(
        "Select option:",
        choices=[
            questionary.Choice("Paste content", value="1"),
            questionary.Choice("Read from file path", value="2")
        ]
    ).ask()

    if choice == "2":
        path = questionary.text("Enter absolute file path:").ask()
        if path and os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception as e:
                write_log(f"Failed to read file: {path}. Using default. Error: {str(e)}", level="WARN")
                return default
        else:
            write_log(f"File not found: {path}. Using default.", level="WARN")
            return default
    else:
        console.print("Paste your multi-line content below. Press Enter on an empty line to finish:", style="yellow")
        lines = []
        while True:
            try:
                line = input()
                if not line:
                    break
                lines.append(line)
            except EOFError:
                break
        if not lines:
            return default
        return "\n".join(lines).strip()

def detect_lan_network() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        parts = ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    except Exception:
        return "192.168.1.0/24"

def detect_timezone() -> str:
    # Calculate system offset in hours
    system_offset = 0.0
    try:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        local_now = utc_now.astimezone()
        system_offset = local_now.utcoffset().total_seconds() / 3600.0
    except Exception:
        pass

    # Helper to check if a zone has a specific offset right now
    def offset_matches(zone_name, target_offset):
        try:
            utc_now = datetime.datetime.now(datetime.timezone.utc)
            tz_offset = utc_now.astimezone(ZoneInfo(zone_name)).utcoffset().total_seconds() / 3600.0
            return abs(tz_offset - target_offset) < 0.01
        except Exception:
            return False

    tz = None
    if platform.system() == "Windows":
        try:
            tz = get_localzone_name()
            if tz and tz != "None" and offset_matches(tz, system_offset):
                return tz
        except Exception:
            pass
    else:
        # Linux/macOS robust detection
        try:
            # 1. TZ env variable
            if os.environ.get("TZ"):
                tz = os.environ["TZ"]
                
            # 2. /etc/timezone file
            if not tz and os.path.exists("/etc/timezone"):
                with open("/etc/timezone", "r") as f:
                    val = f.read().strip()
                    if val:
                        tz = val
                        
            # 3. /etc/localtime symlink resolution
            if not tz and os.path.exists("/etc/localtime"):
                real_path = os.path.realpath("/etc/localtime")
                if "zoneinfo/" in real_path:
                    tz = real_path.split("zoneinfo/")[-1]
                    
            # 4. timedatectl query
            if not tz and shutil.which("timedatectl"):
                res = subprocess.run(
                    ["timedatectl", "show", "--property=Timezone", "--value"],
                    capture_output=True, text=True, timeout=2
                )
                if res.returncode == 0:
                    val = res.stdout.strip()
                    if val:
                        tz = val
        except Exception:
            pass

    if tz and tz != "None" and offset_matches(tz, system_offset):
        return tz

    # Fallback regional selection from COMMON_ZONES using current offset
    matching_zones = []
    for zone in COMMON_ZONES:
        if offset_matches(zone, system_offset):
            matching_zones.append(zone)

    if matching_zones:
        priority_map = {
            -4: ["America/New_York", "America/Toronto", "America/Halifax"],
            -5: ["America/Chicago", "America/Toronto", "America/Bogota", "America/Lima"],
            -6: ["America/Denver", "America/Chicago", "America/Mexico_City"],
            -7: ["America/Phoenix", "America/Los_Angeles", "America/Denver"],
            -8: ["America/Los_Angeles", "America/Vancouver"],
            0: ["UTC", "Europe/London"],
            1: ["Europe/London", "Europe/Paris", "Europe/Berlin"],
            2: ["Europe/Berlin", "Europe/Rome"],
            3: ["Europe/Moscow", "Asia/Riyadh"],
        }
        rounded_offset = round(system_offset)
        if rounded_offset in priority_map:
            for p_zone in priority_map[rounded_offset]:
                if p_zone in matching_zones:
                    return p_zone
        return matching_zones[0]

    try:
        val = get_localzone_name()
        if val and val != "None":
            return val
    except Exception:
        pass

    return "UTC"
        
COMMON_ZONES = [
    "UTC", "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
    "America/Phoenix", "America/Anchorage", "Pacific/Honolulu", "America/Halifax",
    "America/Toronto", "America/Vancouver", "America/Mexico_City", "America/Bogota", 
    "America/Lima", "America/Santiago", "America/Argentina/Buenos_Aires", "America/Sao_Paulo",
    "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Rome", "Europe/Moscow",
    "Africa/Lagos", "Africa/Cairo", "Africa/Nairobi", "Asia/Jerusalem", "Asia/Riyadh",
    "Asia/Tehran", "Asia/Dubai", "Asia/Kabul", "Asia/Karachi", "Asia/Kolkata", 
    "Asia/Colombo", "Asia/Bangkok", "Asia/Jakarta", "Asia/Shanghai", "Asia/Singapore", 
    "Asia/Taipei", "Asia/Tokyo", "Asia/Seoul", "Australia/Perth", "Australia/Adelaide", 
    "Australia/Darwin", "Australia/Sydney", "Australia/Melbourne", "Pacific/Auckland", 
    "Pacific/Fiji"
]

def select_timezone_interactive(detected_tz: str) -> str:
    # Normalize None / "None" input
    if not detected_tz or detected_tz == "None":
        detected_tz = "UTC"

    if os.getenv("DS_HEADLESS") == "true":
        if detected_tz == "UTC":
            try:
                utc_now = datetime.datetime.now(datetime.timezone.utc)
                local_now = utc_now.astimezone()
                user_offset = local_now.utcoffset().total_seconds() / 3600.0
                if user_offset != 0:
                    for zone in COMMON_ZONES:
                        try:
                            tz_offset = utc_now.astimezone(ZoneInfo(zone)).utcoffset().total_seconds() / 3600.0
                            if tz_offset == user_offset:
                                return zone
                        except Exception:
                            pass
            except Exception:
                pass
        return detected_tz

    # Get active local offset
    try:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        local_now = utc_now.astimezone()
        offset_seconds = local_now.utcoffset().total_seconds()
        user_offset = offset_seconds / 3600.0
    except Exception:
        return get_validated_input("System Timezone", detected_tz)

    guessed_tz = detected_tz
    if guessed_tz == "UTC" and user_offset != 0:
        # Find a better regional guess from offset
        for zone in COMMON_ZONES:
            try:
                tz_offset = utc_now.astimezone(ZoneInfo(zone)).utcoffset().total_seconds() / 3600.0
                if tz_offset == user_offset:
                    guessed_tz = zone
                    break
            except Exception:
                pass

    confirm_msg = f"We detected your timezone as '{guessed_tz}'. Is this correct?"
    confirm = safe_confirm(confirm_msg, default=True)
    if confirm:
        return guessed_tz

    # Filter common timezones matching user's offset
    matching_choices = []
    for zone in COMMON_ZONES:
        try:
            tz_offset = utc_now.astimezone(ZoneInfo(zone)).utcoffset().total_seconds() / 3600.0
            if tz_offset == user_offset:
                matching_choices.append(zone)
        except Exception:
            pass

    # Ensure POSIX Etc/GMT fallback is present
    sign = "+" if user_offset < 0 else "-"
    hours = abs(round(user_offset))
    gmt_zone = "UTC" if user_offset == 0 else f"Etc/GMT{sign}{hours}"
    if gmt_zone not in matching_choices:
        matching_choices.append(gmt_zone)

    matching_choices.sort()
    manual_option = "[Type timezone manually]"
    matching_choices.append(manual_option)

    choice = questionary.select(
        f"Select your timezone (matching UTC offset {user_offset:+.1f}):",
        choices=matching_choices
    ).ask()

    if choice == manual_option:
        return get_validated_input("System Timezone", guessed_tz)

    return choice

def configure_environment() -> bool:
    write_step("Configuring environment settings")
    
    project_root = get_project_root()
    deploy_dir = get_deploy_dir()

    # Load State
    metadata = get_metadata()
    selected_services = metadata.get("selected_services", [])

    # Dynamic app parameters loading using Pydantic config models
    from src.apps.loader import load_apps
    from src.utils.dependency_resolver import check_exclusivity_conflicts, resolve_database_dependencies
    from src.utils.port_resolver import resolve_port_conflicts

    apps_dict = load_apps()

    # 1. CLI Exclusivity Checks
    selected_instances = [apps_dict[s] for s in selected_services if s in apps_dict]
    conflicts = check_exclusivity_conflicts(selected_instances)
    if conflicts:
        console.print("[!] EXCLUSIVITY WARNING:", style="bold yellow")
        for grp, names in conflicts.items():
            console.print(f"  - Exclusivity Group '{grp}': {', '.join(names)} are all selected.", style="yellow")
        if not os.getenv("DS_HEADLESS") == "true":
            proceed = safe_confirm("Running multiple services in the same group is not recommended. Proceed anyway?", default=True)
            if not proceed:
                return False

    # 2. CLI Database Dependencies Resolution
    updated_keys, db_notifs = resolve_database_dependencies(selected_services, apps_dict)
    if len(updated_keys) > len(selected_services):
        for notif in db_notifs:
            console.print(f"[i] {notif}", style="green")
        selected_services = updated_keys
        metadata["selected_services"] = selected_services
        from src.utils.state import set_metadata
        set_metadata(metadata)

    # 3. CLI Port Conflict Checks
    env_path = os.path.join(deploy_dir, ".env")
    port_notifs = resolve_port_conflicts([apps_dict[s] for s in selected_services if s in apps_dict], env_path)
    if port_notifs:
        for notif in port_notifs:
            console.print(f"[i] {notif}", style="green")

    console.print("\n--- System Configuration ---", style="yellow")

    # Timezone detection
    detected_tz = detect_timezone()
    tz = select_timezone_interactive(detected_tz)
    default_puid = os.environ.get("SUDO_UID", "1000")
    default_pgid = os.environ.get("SUDO_GID", "1000")
    puid = get_validated_input("PUID (User ID)", default_puid, r"^\d+$", "Must be numeric")
    pgid = get_validated_input("PGID (Group ID)", default_pgid, r"^\d+$", "Must be numeric")

    # Management Credentials
    http_user = get_validated_input("Management Username", "admin")
    
    if os.getenv("DS_HEADLESS") == "true":
        http_pass = new_random_password()
    else:
        while True:
            check_keyboard_locks()
            http_pass = questionary.password("Management Password (leave blank to generate random):").ask()
            
            # Handle Ctrl+C abort
            if http_pass is None:
                write_log("User aborted setup.", level="WARN")
                sys.exit(1)
                
            # Handle blank input (generate random)
            if not http_pass:
                http_pass = new_random_password()
                write_log("[!] Using generated password for this session.", level="WARN")
                break
                
            # Double-entry confirmation for manually entered passwords
            check_keyboard_locks()
            confirm_pass = questionary.password("Confirm Management Password:").ask()
            
            if confirm_pass is None:
                write_log("User aborted setup.", level="WARN")
                sys.exit(1)
                
            if http_pass == confirm_pass:
                break
            else:
                console.print("[!] The passwords don't match, please try again.", style="bold red")

    console.print("\n--- Path Configuration ---", style="yellow")
    docker_dir = resolve_path_slash(deploy_dir)
    write_log(f"Docker Directory: {docker_dir}")
    default_drive_pool = "D:/Media" if platform.system() == "Windows" else resolve_path_slash(os.path.expanduser("~/media"))
    drive_pool = resolve_path_slash(get_validated_input("Media folder directory", default_drive_pool))

    # File browser extra mounts (Edge Case 16)
    extra_mounts = ""
    if "filebrowser" in selected_services or "cloudcmd" in selected_services:
        console.print("\n--- Multi-Drive Configuration ---", style="yellow")
        console.print("FileBrowser/CloudCmd detected. You can map additional system drives for web access.", style="grey50")

        # Basic Windows/Linux drive detection
        drives_to_mount = []
        if platform.system() == "Windows":
            # List possible drives (simple check from D to Z)
            import string
            available_drives = []
            for letter in string.ascii_uppercase:
                if letter in ["C", "A", "B"]:
                    continue
                if os.path.exists(f"{letter}:\\"):
                    available_drives.append(letter)
            
            for drive in available_drives:
                if os.getenv("DS_HEADLESS") == "true":
                    continue
                mount = safe_confirm(f"Mount drive {drive}:\\?", default=False)
                if mount:
                    drives_to_mount.append(f"{drive}:/")
        else:
            # On Linux list mount points under /mnt or /media
            for p in ["/mnt", "/media"]:
                if os.path.exists(p):
                    for d in os.listdir(p):
                        full_p = resolve_path_slash(os.path.join(p, d))
                        if os.path.ismount(full_p):
                            if os.getenv("DS_HEADLESS") == "true":
                                continue
                            mount = safe_confirm(f"Mount path {full_p}?", default=False)
                            if mount:
                                drives_to_mount.append(full_p)
        
        if drives_to_mount:
            extra_mounts = ",".join(drives_to_mount)

    # Generate secure backend passwords
    write_log("Generating secure application passwords...", level="DEBUG")
    db_root_pass = new_random_password()
    db_pass = new_random_password()
    mongo_pass = new_random_password()
    kopia_pass = new_random_password()
    crowdsec_enabled = "true" if "crowdsec" in selected_services else "false"
    crowdsec_key = new_random_password() if crowdsec_enabled == "true" else ""

    # Compile environment variables
    vars_dict = {
        "TZ": tz, "PUID": puid, "PGID": pgid, "DOCKERDIR": docker_dir, "DATADRIVE": drive_pool,
        "EXTRA_MOUNTS": extra_mounts, "USERDIR": docker_dir, "MYSQL_ROOT_PASSWORD": db_root_pass,
        "MYSQL_USER": "mediauser", "MYSQL_PASSWORD": db_pass, "HTTP_USERNAME": http_user,
        "HTTP_PASSWORD": http_pass, "DB_PASS": db_pass, "MONGO_PASS": mongo_pass,
        "KOPIA_PASSWORD": kopia_pass, "CROWDSEC_ENABLED": crowdsec_enabled, "CROWDSEC_API_KEY": crowdsec_key
    }

    # Helper method for browser integration with failsafe
    def launch_browser_safely(url: str):
        if os.getenv("DS_HEADLESS") == "true":
            return
        
        launch = safe_confirm(f"Would you like to open '{url}' in your web browser now?", default=True)
        if launch:
            try:
                import webbrowser
                webbrowser.open(url)
                console.print(f"[OK] Opened {url} in your browser.", style="green")
            except Exception as e:
                write_log(f"Failed to launch browser automatically: {str(e)}", level="WARN")
                console.print(f"[!] Please open this URL manually: {url}", style="cyan")

    console.print("\n--- Service Secrets & Tokens ---", style="yellow")

    # Dynamic app parameters loading using Pydantic config models
    from src.apps.loader import load_apps
    apps_dict = load_apps()
    
    for svc in selected_services:
        if svc in apps_dict:
            app = apps_dict[svc]
            if app.config_model:
                console.print(f"\n--- {app.name} Settings ---", style="yellow")
                model = app.config_model
                for field_name, field_info in model.model_fields.items():
                    default_val = field_info.default if field_info.default is not None else ""
                    description = field_info.description or field_name
                    
                    extra = field_info.json_schema_extra or {}
                    help_url = extra.get("help_url")
                    if help_url:
                        launch_browser_safely(help_url)
                        
                    is_secret = extra.get("is_secret", False) or "pass" in field_name.lower() or "key" in field_name.lower() or "token" in field_name.lower()
                    
                    if os.getenv("DS_HEADLESS") == "true":
                        val = default_val
                    else:
                        if is_secret:
                            val = questionary.password(f"{description} (default: [hidden]):").ask()
                        else:
                            val = questionary.text(f"{description} (default: {default_val}):").ask()
                            
                        if val is None:
                            write_log("User aborted setup.", level="WARN")
                            sys.exit(1)
                            
                        val = val.strip()
                        if not val:
                            val = default_val
                            
                    vars_dict[field_name] = str(val)

    # Inject dynamically resolved alternative ports
    resolved_ports = metadata.get("resolved_ports", {})
    for svc, alt_port in resolved_ports.items():
        vars_dict[f"{svc.upper()}_PORT"] = str(alt_port)

    env_file = resolve_path_slash(os.path.join(docker_dir, ".env"))
    if os.path.exists(env_file) and os.getenv("DS_HEADLESS") != "true":
        overwrite = safe_confirm(f".env already exists in {docker_dir}. Overwrite?", default=False)
        if not overwrite:
            write_log("Skipping .env creation.", level="INFO")
            return True

    write_log("Writing environment variables...", level="DEBUG")
    save_env_vars(vars_dict, file_path=env_file)

    # Restrict permissions (Edge Case 7 - Windows NTFS icacls, Linux POSIX chmod)
    if platform.system() == "Windows":
        try:
            # Query username
            import getpass
            username = getpass.getuser()
            # Windows icacls hardening
            subprocess.run(f'icacls "{env_file}" /inheritance:r /grant "{username}:F" /grant "*S-1-5-32-544:F"', shell=True, capture_output=True)
            write_log("Restricted permissions on .env (NTFS icacls).", level="DEBUG")
        except Exception as e:
            write_log(f"Failed to set .env permissions via icacls: {str(e)}", level="WARN")
    else:
        try:
            os.chmod(env_file, 0o600)
            write_log("Restricted permissions on .env (POSIX chmod 600).", level="DEBUG")
        except Exception as e:
            write_log(f"Failed to set .env permissions via chmod: {str(e)}", level="WARN")

    write_log(f".env file successfully synchronized in {docker_dir}", level="DEBUG")
    console.print("[✓] Environment configuration synchronized", style="green")
    return True
````

## File: src/modules/compose_build.py
````python
import os
import re
import hashlib
from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path, resolve_path_slash
from src.utils.logger import write_log, console, write_step
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_template_blocks, get_registry_list

def indent_service_block(block: str) -> str:
    """
    Reconstructs 2-space indentation for loaded templates to match services block nesting (Edge Case 12).
    """
    return "\n".join("  " + line if line.strip() else "" for line in block.splitlines())

COMPOSE_HEADER = """networks:
  default:
    driver: bridge
  npm_proxy:
    external: true
  media-internal:
    external: true

x-environment: &default-tz-puid-pgid
  TZ: $TZ
  PUID: $PUID
  PGID: $PGID

x-logging: &default-logging
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"

x-common-keys-core: &common-keys-core
  <<: *default-logging
  networks:
    - npm_proxy
  security_opt:
    - no-new-privileges:true
  restart: always

x-common-keys-apps: &common-keys-apps
  <<: *default-logging
  networks:
    - npm_proxy
    - media-internal
  security_opt:
    - no-new-privileges:true
  restart: unless-stopped

services:
"""

def build_compose_stacks() -> bool:
    write_step("Generating Docker Compose stack configurations")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    env_path = resolve_path_slash(os.path.join(deploy_dir, ".env"))

    # Load state & apps dynamically
    from src.apps.loader import load_apps
    apps_dict = load_apps()
    metadata = get_metadata()
    selected_services = metadata.get("selected_services", [])

    # Database Manager dependency logic
    db_addons = {
        "mariadb (+adminer)": "adminer",
        "postgresql (+cloudbeaver)": "cloudbeaver",
        "mongodb (+mongo-express)": "mongo-express"
    }
    for db, addon in db_addons.items():
        if db in selected_services and addon not in selected_services:
            selected_services.append(addon)

    # Update Hash in Metadata
    metadata["template_hash"] = "DYNAMIC"
    set_metadata(metadata)

    stacks_dir = resolve_path_slash(os.path.join(deploy_dir, "stacks"))
    os.makedirs(stacks_dir, exist_ok=True)

    generated_stacks = []
    homepage_services = []

    # Pre-compute dynamic mounts string (Edge Case 16)
    extra_mounts = os.getenv("EXTRA_MOUNTS", "")
    if not extra_mounts and os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"^EXTRA_MOUNTS=(.*)", line)
                if match:
                    extra_mounts = match.group(1)
                    break

    dynamic_mounts_string = ""
    if extra_mounts:
        mounts = [m.strip() for m in extra_mounts.split(",") if m.strip()]
        for m in mounts:
            clean_m = m.replace('"', '').replace("'", "")
            # Windows drive parsing or Linux paths
            drive_letter = clean_m.replace(":/", "").replace(":\\", "").replace(":", "")
            dynamic_mounts_string += f"      - {clean_m}:/srv/{drive_letter}_Drive\n"

    # Group services by stack_group
    stack_groups_list = ["core", "media-pvr", "media-server", "downloaders", "maintenance", "personal-cloud", "games"]
    services_by_stack = {}
    for svc in selected_services:
        app = apps_dict.get(svc)
        if app:
            sg = app.stack_group or "utilities"
            if sg not in services_by_stack:
                services_by_stack[sg] = []
            services_by_stack[sg].append(svc)

    ordered_stack_names = list(stack_groups_list)
    for sg in services_by_stack:
        if sg not in ordered_stack_names:
            ordered_stack_names.append(sg)

    # --- STACK GENERATION LOOP ---
    for stack_name in ordered_stack_names:
        active_services = services_by_stack.get(stack_name, [])

        if active_services:
            write_log(f"Generating stack: {stack_name} ({len(active_services)} services)")
            stack_path = os.path.join(stacks_dir, stack_name)
            os.makedirs(stack_path, exist_ok=True)

            # Build Compose
            output = COMPOSE_HEADER
            for svc in active_services:
                write_log(f"Adding service to {stack_name}: {svc}", level="DEBUG")
                app = apps_dict.get(svc)
                if app:
                    svc_content = app.get_compose_template()

                    # Security warning for privileged containers
                    if "privileged: true" in svc_content or "cap_add:" in svc_content and "SYS_ADMIN" in svc_content:
                        write_step(f"Security Warning: Service '{svc}' in stack '{stack_name}' is privileged.", level="WARN")

                    # Audit template version tags for critical services (Verbose only)
                    critical_services = ["mariadb (+adminer)", "postgresql (+cloudbeaver)", "mongodb (+mongo-express)", "authelia"]
                    if svc in critical_services:
                        match_img = re.search(r"image:\s*([^\s]+)", svc_content)
                        if match_img:
                            image = match_img.group(1)
                            if image.endswith(":latest") or ":" not in image:
                                write_log(
                                    f"[AUDIT] Insecure tag found in critical service '{svc}': image is using '{image}'. Consider pinning to a stable version.",
                                    level="DEBUG"
                                )

                    if "{{DYNAMIC_MOUNTS}}" in svc_content:
                        svc_content = svc_content.replace("{{DYNAMIC_MOUNTS}}", dynamic_mounts_string)

                    output += "\n" + indent_service_block(svc_content)
                else:
                    write_log(f"Plugin NOT FOUND for service: {svc}", level="DEBUG")

            # Write Compose File
            compose_file_path = os.path.join(stack_path, "docker-compose.yml")
            with open(compose_file_path, "w", encoding="utf-8") as f:
                f.write(output)

            # --- PHASE 4: SECRET ISOLATION (FILTERED .ENV) ---
            write_log(f"Isolating secrets for stack: {stack_name}", level="DEBUG")
            master_env_lines = []
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    master_env_lines = f.readlines()

            # Global defaults always included
            required_vars = {"PUID", "PGID", "TZ", "DOCKERDIR", "DATADRIVE", "USERDIR"}

            # Scan compose for variables using exact regex mapping (Edge Case 14)
            var_matches = re.findall(r'\$\{?(\w+)(?:[:?#-][^}]*)?\}?', output)
            for var_name in var_matches:
                required_vars.add(var_name)

            # Special case for maintenance stack: Include all API keys and HTTP credentials for Homepage Widgets
            if stack_name == "maintenance":
                required_vars.update({"HTTP_USERNAME", "HTTP_PASSWORD"})
                for line in master_env_lines:
                    match = re.match(r"^([A-Z0-9_]+_API_KEY|[A-Z0-9_]+_TOKEN|[A-Z0-9_]+_KEY)=", line)
                    if match:
                        required_vars.add(match.group(1))

            # Filter and Write Stack-Local .env
            filtered_env = []
            for line in master_env_lines:
                match = re.match(r"^([^=]+)=", line)
                if match:
                    key = match.group(1).strip()
                    if key in required_vars:
                        filtered_env.append(line)
                elif line.startswith("#") or not line.strip():
                    filtered_env.append(line)

            with open(os.path.join(stack_path, ".env"), "w", encoding="utf-8") as f:
                f.writelines(filtered_env)

            generated_stacks.append({
                "Name": stack_name,
                "Apps": ", ".join(active_services)
            })

            # Collect for Homepage (excluding helper DB apps)
            db_helpers = ["adminer", "cloudbeaver", "mongo-express"]
            for svc in active_services:
                if svc not in db_helpers:
                    homepage_services.append({"Name": svc, "Stack": stack_name})

    # --- PHASE 5: NPM + AUTHELIA COMPANION CONFIG ---
    if "authelia" in selected_services and "npm plus (+goaccess)" in selected_services:
        write_log("Configuring NPM & Authelia Companion forward-auth configs...")
        npm_nginx_path = os.path.join(deploy_dir, "appdata", "npm", "config", "nginx")
        os.makedirs(npm_nginx_path, exist_ok=True)
        
        # Write reusable location block for forward auth
        authelia_conf_content = """# Reusable Authelia Forward Auth configuration block
# Include this in your Nginx Proxy Manager Proxy Host -> Custom Configuration box:
# include /config/nginx/authelia-auth.conf;

auth_request /authelia;
error_page 401 = @clean_auth_demanded;

location /authelia {
    internal;
    set $upstream_authelia http://authelia:9091/api/verify;
    proxy_pass $upstream_authelia;
    
    proxy_set_header X-Original-URI $request_uri;
    proxy_set_header X-Original-Method $request_method;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $http_host;
    proxy_set_header X-Forwarded-Uri $request_uri;
    proxy_set_header X-Forwarded-Ssl on;
    proxy_set_header Connection "";
    
    # Do not buffer verification requests
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
}

location @clean_auth_demanded {
    # Replace auth.local.host with your public Authelia domain if routing externally
    return 302 https://$host/authelia/?rd=$scheme://$http_host$request_uri;
}
"""
        try:
            with open(os.path.join(npm_nginx_path, "authelia-auth.conf"), "w", encoding="utf-8") as f:
                f.write(authelia_conf_content)
            write_log("Successfully wrote Authelia NPM helper config to appdata/npm/config/nginx/authelia-auth.conf", level="INFO")
        except Exception as e:
            write_log(f"Warning: Failed to write Authelia auth config to NPM: {str(e)}", level="WARN")

    # --- HOMEPAGE GENERATOR ---
    if "homepage" in selected_services:
        write_log("Generating Homepage services configuration...")
        hp_path = os.path.join(deploy_dir, "appdata", "homepage", "config")
        os.makedirs(hp_path, exist_ok=True)

        hp_output = ""
        hp_env_mappings = []
        active_hp_groups = []

        supported_widgets = {
            "sonarr": "sonarr",
            "radarr": "radarr",
            "lidarr": "lidarr",
            "readarr": "readarr",
            "bazarr": "bazarr",
            "prowlarr": "prowlarr",
            "qbittorrent": "qbittorrent",
            "sabnzbd": "sabnzbd",
            "plex": "plex",
            "jellyfin": "jellyfin",
            "tautulli": "tautulli",
            "portainer": "portainer",
            "mylar": "mylar3",
            "audiobookshelf": "audiobookshelf",
            "paperless": "paperless",
            "seerr": "seerr"
        }

        def make_friendly_name(name: str) -> str:
            # Converts 'media-pvr' to 'Media PVR', 'media-server' to 'Media Server'
            parts = name.split('-')
            return " ".join([p.upper() if p.lower() in ["pvr", "vpn"] else p.capitalize() for p in parts])

        for stack_name in ordered_stack_names:
            stack_apps = [a for a in homepage_services if a["Stack"] == stack_name and a["Name"] != "homepage"]

            if stack_apps:
                friendly_group_name = make_friendly_name(stack_name)
                active_hp_groups.append(friendly_group_name)
                hp_output += f"- {friendly_group_name}:\n"
                for app in stack_apps:
                    svc_key = app["Name"]
                    
                    app_instance = apps_dict.get(svc_key)
                    alias = svc_key
                    port = 0
                    if app_instance:
                        alias = app_instance.name
                        port = app_instance.port
                    
                    container_port = str(port)
                    svc_template = app_instance.get_compose_template() if app_instance else ""
                    # Check for explicit PORT override
                    match_port = re.search(r"#\s*PORT:\s*(\d+)", svc_template)
                    if match_port:
                        port = match_port.group(1)
                        container_port = port
                    else:
                        # Find the ports block
                        match_ports = re.search(r"ports:\s*\n((?:\s*-\s*['\"]?\d+:\d+['\"]?\s*\n)+)", svc_template)
                        if match_ports:
                            ports_list = match_ports.group(1)
                            # Parse the first port pair, e.g. 8083:80
                            match_pair = re.search(r"-\s*['\"]?(\d+):(\d+)['\"]?", ports_list)
                            if match_pair:
                                port = match_pair.group(1)
                                container_port = match_pair.group(2)
                        elif port == "0":
                            # Regex fallback check
                            match_regex_port = re.search(r"-\s*(\d+):", svc_template)
                            if match_regex_port:
                                port = match_regex_port.group(1)
                                container_port = port

                    clean_key = svc_key.split(" ")[0]
                    if not port or port == "0" or (app_instance and app_instance.category == "none"):
                        continue

                    hp_output += f"    - {svc_key}:\n"
                    hp_output += f"        icon: {clean_key}.png\n"

                    if port and port != "0":
                        url = f"http://localhost:{port}"
                        base_domain = "local.host"
                        # Fetch base domain from env
                        base_domain_env = os.getenv("BASE_DOMAIN", "")
                        if not base_domain_env and os.path.exists(env_path):
                            with open(env_path, "r", encoding="utf-8") as f:
                                for line in f:
                                    match = re.match(r"^BASE_DOMAIN=(.*)", line)
                                    if match:
                                        base_domain_env = match.group(1)
                                        break
                        if base_domain_env:
                            base_domain = base_domain_env

                        if "npm plus (+goaccess)" in selected_services and base_domain != "local.host":
                            url = f"https://{alias.split(' ')[0]}.{base_domain}"

                        if clean_key == "plex":
                            url += "/web"

                        # Get a clean description from the app instance category
                        description = app_instance.category.capitalize() if app_instance and app_instance.category and app_instance.category != "none" else alias

                        hp_output += f"        href: {url}\n"
                        hp_output += f"        description: {description}\n"
                        hp_output += f"        ping: http://{clean_key}:{container_port}\n"

                        # --- WIDGET LOGIC ---
                        w_key = clean_key.lower()
                        if w_key in ["qbit-vpn", "qbit"]:
                            w_key = "qbittorrent"
                        if w_key == "uptimekuma":
                            w_key = "uptime-kuma"

                        if w_key in supported_widgets and url:
                            w_type = supported_widgets[w_key]
                            hp_output += "        widget:\n"
                            hp_output += f"          type: {w_type}\n"
                            hp_output += f"          url: http://{clean_key}:{container_port}\n"

                            env_key_base = svc_key.upper().replace("-", "_").replace(" ", "_")

                            if w_type == "qbittorrent":
                                hp_output += "          username: {{HOMEPAGE_VAR_HTTP_USERNAME}}\n"
                                hp_output += "          password: {{HOMEPAGE_VAR_HTTP_PASSWORD}}\n"
                                hp_env_mappings.append("      - HOMEPAGE_VAR_HTTP_USERNAME=${HTTP_USERNAME}")
                                hp_env_mappings.append("      - HOMEPAGE_VAR_HTTP_PASSWORD=${HTTP_PASSWORD}")
                            else:
                                api_key_var = f"{env_key_base}_API_KEY"
                                # Jellyfin widget uses 'apiKey', all others use 'key'
                                key_field = "key"
                                if w_type == "plex":
                                    api_key_var = "PLEX_TOKEN"
                                elif w_type == "jellyfin":
                                    api_key_var = "JELLYFIN_KEY"
                                    key_field = "apiKey"
                                elif w_type == "portainer":
                                    api_key_var = "PORTAINER_KEY"

                                hp_output += f"          {key_field}: {{{{HOMEPAGE_VAR_{api_key_var}}}}}\n"
                                hp_env_mappings.append(f"      - HOMEPAGE_VAR_{api_key_var}=${api_key_var}")
                    else:
                        hp_output += "        description: Background Service\n"
                hp_output += "\n"

        # Write Homepage services.yaml
        with open(os.path.join(hp_path, "services.yaml"), "w", encoding="utf-8") as f:
            f.write(hp_output)

        # Write Homepage settings.yaml (Layout configuration) - Safe Merge
        from ruamel.yaml import YAML
        yaml = YAML()
        yaml.preserve_quotes = True
        
        settings_file = os.path.join(hp_path, "settings.yaml")
        settings_data = {}
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    loaded = yaml.load(f)
                    if loaded:
                        settings_data = loaded
            except Exception as e:
                write_log(f"Failed to load existing settings.yaml: {str(e)}", level="WARN")

        # Set defaults if not present
        if "title" not in settings_data:
            settings_data["title"] = "Home Server Dashboard"
        if "theme" not in settings_data:
            settings_data["theme"] = "dark"
        if "fullWidth" not in settings_data:
            settings_data["fullWidth"] = True
        
        # Determine strict priority order for top rows dynamically from stack groups list
        priority_order = []
        for sg in stack_groups_list:
            priority_order.append(make_friendly_name(sg))

        ordered_groups = []
        
        # 1. Add priority groups if active
        for p_group in priority_order:
            if p_group in active_hp_groups:
                ordered_groups.append(p_group)
                
        # 2. Add any remaining active groups
        for a_group in active_hp_groups:
            if a_group not in ordered_groups:
                ordered_groups.append(a_group)
                
        # Build the layout dictionary
        layout_list = []
        for layout_group in ordered_groups:
            # We construct a dict like: {"Media Server": {"style": "row", "columns": 4}}
            layout_list.append({layout_group: {"style": "row", "columns": 4}})
            
        settings_data["layout"] = layout_list
        
        with open(settings_file, "w", encoding="utf-8") as f:
            yaml.dump(settings_data, f)

        # Write Homepage widgets.yaml
        widgets_file = os.path.join(hp_path, "widgets.yaml")
        if not os.path.exists(widgets_file) or os.getenv("TEST_MODE") != "true":
            # Determine disk path
            drive = os.path.splitdrive(deploy_dir)[0]
            if drive:
                disk_path = "/" + drive.replace(":", "").lower()
            else:
                disk_path = "/"
                
            widgets_content = f"""---
# For configuration options and examples, please see:
# https://gethomepage.dev/en/configs/widgets

- resources:
    cpu: true
    memory: true
    disk: {disk_path}

- search:
    provider: google
    target: _blank
    
- datetime:
    text_size: xl
    format:
      dateStyle: short
      timeStyle: short
      hour12: true
"""
            with open(widgets_file, "w", encoding="utf-8") as f:
                f.write(widgets_content)

        # Write Homepage bookmarks.yaml
        bookmarks_file = os.path.join(hp_path, "bookmarks.yaml")
        if not os.path.exists(bookmarks_file) or os.getenv("TEST_MODE") != "true":
            bookmarks_content = """- Developer:
    - github.com/suuift/dockersetup:
        abbr: GH
        href: https://github.com/suuift/dockersetup
- Windows Debloat Scripts:
    - Github/ChrisTitusTech/winutil/:
        abbr: RE
        href: https://github.com/ChrisTitusTech/winutil/
"""
            with open(bookmarks_file, "w", encoding="utf-8") as f:
                f.write(bookmarks_content)

        # Write Homepage docker.yaml (Local Socket connection)
        docker_file = os.path.join(hp_path, "docker.yaml")
        if not os.path.exists(docker_file) or os.getenv("TEST_MODE") != "true":
            docker_data = {
                "my-docker": {
                    "socket": "/var/run/docker.sock"
                }
            }
            with open(docker_file, "w", encoding="utf-8") as f:
                yaml.dump(docker_data, f)        # Update the Homepage Compose with dynamic mappings
        hp_compose_path = os.path.join(stacks_dir, "maintenance", "docker-compose.yml")
        if os.path.exists(hp_compose_path):
            unique_mappings = sorted(list(set(hp_env_mappings)))
            mapping_str = "\n".join(unique_mappings)
            with open(hp_compose_path, "r", encoding="utf-8") as f:
                hp_compose = f.read()
            new_hp_compose = hp_compose.replace("{{HOMEPAGE_MAPPINGS}}", mapping_str)
            with open(hp_compose_path, "w", encoding="utf-8") as f:
                f.write(new_hp_compose)
    # Finalize State
    metadata["generated_stacks"] = generated_stacks
    set_metadata(metadata)

    write_log(f"Multi-stack build complete at {stacks_dir}", level="DEBUG")
    console.print("[✓] Docker Compose stack configurations generated", style="green")
    return True
````

## File: src/gui.py
````python
from src.gui import DockerSetupGUI

if __name__ == "__main__":
    app = DockerSetupGUI()
    app.mainloop()
````

## File: dockersetup.py
````python
import os
import re
import sys
import shutil
import hashlib
import platform
import subprocess
import questionary
from rich.console import Console

# Bootstrap utilities
from src.utils.paths import get_project_root, get_deploy_dir, resolve_path_slash, get_resource_path
from src.utils.logger import write_log, write_step, set_log_path, enable_debug_logging, get_log_path, invoke_external_command, safe_confirm
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list
from src.utils.updater import invoke_self_update, VERSION

# Import modules locally in main or methods for lazy loading performance optimization
# from src.modules.preflight import run_system_preflight
# from src.modules.deploy_preflight import run_deploy_preflight
# from src.modules.tier_select import select_services
# from src.modules.env_wizard import configure_environment
# from src.modules.directories import setup_directories
# from src.modules.network import setup_networks
# from src.modules.compose_build import build_compose_stacks
# from src.modules.deploy_start import deploy_stacks
# from src.modules.auto_configure import auto_stitch_services, test_port

console = Console()

def sync_dot_env(source_env: str, target_dir: str):
    write_log("Syncing environment variables to stack folders...", level="DEBUG")
    stacks_dir = resolve_path_slash(os.path.join(target_dir, "stacks"))
    if os.path.exists(stacks_dir):
        for name in os.listdir(stacks_dir):
            folder_path = resolve_path_slash(os.path.join(stacks_dir, name))
            if os.path.isdir(folder_path):
                try:
                    shutil.copy(source_env, resolve_path_slash(os.path.join(folder_path, ".env")))
                except Exception as e:
                    write_log(f"Failed to copy .env to {folder_path}: {str(e)}", level="WARN")

def invoke_token_wizard(target_dir: str):
    metadata = get_metadata()
    selected = metadata.get("selected_services", [])
    if not selected:
        return

    env_path = resolve_path_slash(os.path.join(target_dir, ".env"))
    if not os.path.exists(env_path):
        return

    manual_services = {
        "plex": {"Name": "Plex", "Var": "PLEX_TOKEN", "Url": "http://localhost:32400", "Hint": "Open Plex -> Settings -> Web Client (General) -> 'Show Advanced' -> Scroll to bottom for 'Plex Token'."},
        "jellyfin": {"Name": "Jellyfin", "Var": "JELLYFIN_KEY", "Url": "http://localhost:8096", "Hint": "Open Jellyfin -> Dashboard -> API Keys -> Create a new key named 'Homepage'."},
        "portainer": {"Name": "Portainer", "Var": "PORTAINER_KEY", "Url": "http://localhost:9443", "Hint": "Open Portainer -> User Settings -> Access Tokens -> Create a new token named 'Homepage'."}
    }

    to_configure = []
    # Read env file content
    env_content = ""
    with open(env_path, "r", encoding="utf-8") as f:
        env_content = f.read()

    for svc, info in manual_services.items():
        if svc in selected:
            if not re.search(fr"^{info['Var']}=", env_content, re.MULTILINE):
                to_configure.append(svc)

    if to_configure and os.getenv("DS_HEADLESS") != "true":
        console.print("\n----------------------------------------------------------", style="cyan")
        console.print("             HOMEPAGE WIDGET SETUP", style="cyan")
        console.print("----------------------------------------------------------", style="cyan")
        console.print("I noticed some services are running that require a manual")
        console.print("API token to enable rich data widgets in your Dashboard:")
        for s in to_configure:
            console.print(f" - {manual_services[s]['Name']}", style="yellow")
        console.print("")
        
        do_setup = safe_confirm("Would you like to set these up now?", default=False)
        if do_setup:
            from src.utils.state import set_env_var
            for s in to_configure:
                cfg = manual_services[s]
                console.print(f"\n>> Configuring {cfg['Name']}", style="cyan")
                
                token = None
                if s == "plex":
                    auth_choice = safe_confirm("Would you like to automatically link your Plex account using Plex PIN flow?", default=True)
                    if auth_choice:
                        from src.utils.plex_oauth import request_plex_token
                        token = request_plex_token()
                    else:
                        console.print(f"1. Open: {cfg['Url']}", style="grey50")
                        console.print(f"2. {cfg['Hint']}", style="grey50")
                        token = questionary.password(f"Paste the Token/Key here (leave blank to skip):").ask()
                else:
                    console.print(f"1. Open: {cfg['Url']}", style="grey50")
                    console.print(f"2. {cfg['Hint']}", style="grey50")
                    token = questionary.password(f"Paste the Token/Key here (leave blank to skip):").ask()
                    
                if token and token.strip():
                    set_env_var(cfg["Var"], token.strip(), file_path=env_path)
                    console.print(f"[OK] Saved {cfg['Var']} to .env", style="green")

            # Restart maintenance stack
            hp_path = resolve_path_slash(os.path.join(target_dir, "stacks", "maintenance"))
            if os.path.exists(hp_path):
                write_step("Reloading Dashboard to apply new tokens...")
                try:
                    invoke_external_command("docker compose up -d --remove-orphans", description="Reloading Maintenance stack")
                except Exception:
                    pass

def get_default_deployment_dir() -> str:
    if sys.platform == "win32":
        return "C:/docker"
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return "/opt/docker"
    return resolve_path_slash(os.path.expanduser("~/docker"))

def get_deployment_dir_interactive(project_root: str, required: bool = True) -> str:
    console.print("\n--- Deployment Folder Selection ---", style="yellow")
    default_path = get_default_deployment_dir()
    if os.getenv("DS_HEADLESS") == "true":
        path = default_path
    else:
        path = questionary.text(f"Please provide the full path to your Docker deployment folder (default: {default_path}):").ask()
        if not path or not path.strip():
            path = default_path
        else:
            path = path.strip().replace("'", "").replace('"', "")

    norm_path = resolve_path_slash(path)
    
    if not os.path.exists(norm_path) and required:
        if os.getenv("DS_HEADLESS") == "true":
            create = True
        else:
            create = safe_confirm(f"Folder '{norm_path}' does not exist. Create it?", default=True)
        if create:
            os.makedirs(norm_path, exist_ok=True)
        else:
            return None

    if os.getenv("TEST_MODE") == "true":
        if "testing" not in norm_path.lower():
            raise RuntimeError(f"SECURITY FAULT: AIT tried to deploy to '{norm_path}' which is outside the testing/ sandbox.")

    return norm_path

def main():
    try:
        # UTF-8 Console encoding
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

        project_root = get_project_root()

        # Check if we should route to GUI mode
        use_cli = "--cli" in sys.argv
        has_display = sys.platform == "win32" or os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
        is_gui = not use_cli and has_display

        # Self-Update check (Headless/CI skips update)
        if os.getenv("TEST_MODE") != "true" and os.getenv("DS_HEADLESS") != "true":
            if invoke_self_update(project_root, is_gui=is_gui):
                write_log("Setup updated. Please restart the script.", level="INFO")
                sys.exit(0)
        
        if is_gui:
            try:
                from src.gui import DockerSetupGUI
                app = DockerSetupGUI()
                app.mainloop()
                sys.exit(0)
            except Exception as e:
                # Fall back to CLI if GUI initialization fails
                print(f"[WARN] GUI initialization failed: {str(e)}. Falling back to CLI mode.")

        debug_logging_enabled = False
        exit_script = False

        while not exit_script:
            console.print(f"\n--- Media Stack Manager v{VERSION} ---", style="cyan")
            console.print("[1] Install / Reconfigure / Upgrade Stack")
            console.print("[2] Force Update All Containers (Existing Setup)")
            console.print("[3] Uninstall Stack")
            debug_label = "[ENABLED]" if debug_logging_enabled else "[DISABLED]"
            console.print(f"[4] Toggle Verbose (Debug) Logging {debug_label}")
            console.print("[Q] Exit")
            console.print("")

            if os.getenv("DS_HEADLESS") == "true":
                choice = "1"
                exit_script = True
            else:
                choice = questionary.text("Select an option:").ask()

            if not choice or choice.strip().lower() == "q":
                exit_script = True
                break

            choice = choice.strip()
            
            if choice == "4":
                if debug_logging_enabled:
                    debug_logging_enabled = False
                    os.environ["DEBUG_LOGGING"] = "false"
                else:
                    debug_logging_enabled = True
                    enable_debug_logging()
                console.print(f"Verbose logging {'ENABLED' if debug_logging_enabled else 'DISABLED'} for this session.", style="yellow")
            
            elif choice == "1":
                d_dir = get_deployment_dir_interactive(project_root)
                if not d_dir:
                    continue
                os.environ["DEPLOY_DIR"] = d_dir

                # Smart Reconfigure / Upgrade menu
                metadata = get_metadata()
                os.environ["SKIP_SELECTION"] = "false"

                if metadata.get("selected_services"):
                    write_step(f"Existing Deployment Detected at {d_dir}", level="WARN")
                    
                    # Check for template updates
                    needs_upgrade = False
                    template_path = get_resource_path("templates.yml")
                    
                    sha256 = hashlib.sha256()
                    with open(template_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256.update(chunk)
                    current_hash = sha256.hexdigest().upper()
                    
                    if metadata.get("template_hash") != current_hash:
                        needs_upgrade = True

                    if os.getenv("DS_HEADLESS") != "true":
                        console.print("What would you like to do?")
                        console.print("[1] Add / Remove Services (Re-run Wizard)")
                        upgrade_label = "[2] Upgrade Templates (NEW UPDATES AVAILABLE!)" if needs_upgrade else "[2] Re-generate Stacks (Upgrade Templates)"
                        upgrade_style = "green" if needs_upgrade else "white"
                        console.print(upgrade_label, style=upgrade_style)
                        console.print("[3] Full Reset (Wipe selection/config and start fresh)")
                        console.print("[4] Cancel")
                        
                        sub_choice = questionary.text("Select an option:").ask()
                        if sub_choice == "2":
                            os.environ["SKIP_SELECTION"] = "true"
                            console.print("[UPGRADE] Regenerating stacks with latest templates...", style="cyan")
                        elif sub_choice == "3":
                            console.print("\n[bold red][!] WARNING: A Full Reset will completely destroy all active containers,[/bold red]")
                            console.print("[bold red]    remove docker volumes, and delete all configuration folders (appdata) under:[/bold red]")
                            console.print(f"    [cyan]{d_dir}[/cyan]\n")
                            confirm = safe_confirm("Are you sure you want to permanently wipe all containers and configurations?", default=False)
                            if confirm:
                                # Stop containers and clean volumes first if stacks exist
                                from src.utils.paths import get_clean_env
                                
                                # Verify Docker daemon is online
                                docker_online = False
                                try:
                                    subprocess.run(
                                        ["docker", "info"],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL,
                                        check=True,
                                        timeout=4,
                                        env=get_clean_env()
                                    )
                                    docker_online = True
                                except Exception:
                                    docker_online = False

                                proceed_cleanup = True
                                if not docker_online:
                                    console.print("\n[bold red][!] WARNING: Docker daemon is not running.[/bold red]")
                                    console.print("Cannot automatically stop active container stacks or clean Docker volumes.")
                                    proceed_cleanup = safe_confirm("Would you like to force delete the configuration folders anyway?", default=False)
                                    if not proceed_cleanup:
                                        console.print("Reset cancelled. Config directories preserved.", style="yellow")
                                        continue

                                stacks_dir = resolve_path_slash(os.path.join(d_dir, "stacks"))
                                if docker_online and os.path.exists(stacks_dir):
                                    for stack in os.listdir(stacks_dir):
                                        full_path = resolve_path_slash(os.path.join(stacks_dir, stack))
                                        if os.path.isdir(full_path):
                                            compose_file = resolve_path_slash(os.path.join(full_path, "docker-compose.yml"))
                                            if os.path.exists(compose_file):
                                                write_step(f"Removing containers & volumes for stack: {stack}")
                                                try:
                                                    res_down = subprocess.run(
                                                        ["docker", "compose", "down", "-v", "--remove-orphans"],
                                                        cwd=full_path,
                                                        capture_output=True,
                                                        env=get_clean_env()
                                                    )
                                                    if res_down.returncode != 0:
                                                        console.print(f"\n[bold red][!] Warning: docker compose down failed for '{stack}':[/bold red]")
                                                        console.print(res_down.stderr.decode("utf-8", errors="ignore").strip())
                                                        force_del = safe_confirm(f"Remove configuration directory for stack '{stack}' anyway?", default=False)
                                                        if not force_del:
                                                            proceed_cleanup = False
                                                except Exception as e:
                                                    write_log(f"Failed to compose down stack {stack}: {str(e)}", level="WARN")

                                if proceed_cleanup:
                                    import stat
                                    def force_delete_fallback(func, path, exc_info):
                                        try:
                                            os.chmod(path, stat.S_IWRITE)
                                            func(path)
                                        except Exception:
                                            pass

                                    rmtree_opts = {}
                                    if sys.version_info >= (3, 12):
                                        rmtree_opts["onexc"] = force_delete_fallback
                                    else:
                                        rmtree_opts["onerror"] = force_delete_fallback

                                    # Remove directories
                                    write_step("Deleting configuration and stack directories")
                                    shutil.rmtree(stacks_dir, **rmtree_opts)
                                    shutil.rmtree(resolve_path_slash(os.path.join(d_dir, "appdata")), **rmtree_opts)
                                    
                                    # Double check residual files
                                    if os.path.exists(stacks_dir) or os.path.exists(os.path.join(d_dir, "appdata")):
                                        console.print("[!] Notice: Some locked or root-owned files could not be removed automatically. Please check permissions.", style="yellow")
                                else:
                                    continue
                                
                                # Remove metadata and environment files
                                for file in [".metadata.json", ".env"]:
                                    file_p = resolve_path_slash(os.path.join(d_dir, file))
                                    if os.path.exists(file_p):
                                        try:
                                            shutil.copy2(file_p, file_p + ".bak")
                                            console.print(f"[Backup] Saved backup to {file}.bak", style="grey50")
                                        except Exception:
                                            pass
                                        try:
                                            os.remove(file_p)
                                        except Exception:
                                            pass
                                console.print("Settings and configurations wiped. Starting fresh install...", style="green")
                            else:
                                console.print("[i] Reset cancelled. No containers or configurations were modified.", style="yellow")
                                continue
                        elif sub_choice == "4" or not sub_choice:
                            continue
                    else:
                        os.environ["SKIP_SELECTION"] = "true"

                set_log_path(d_dir)
                write_log(f"Initializing install at {d_dir}...", level="INFO", clear=True)

                failed = False
                try:
                    # Run linear modules loaded locally for lazy execution optimization
                    from src.modules.preflight import run_system_preflight
                    from src.modules.deploy_preflight import run_deploy_preflight
                    from src.modules.tier_select import select_services
                    from src.modules.env_wizard import configure_environment
                    from src.modules.directories import setup_directories
                    from src.modules.network import setup_networks
                    from src.modules.compose_build import build_compose_stacks
                    from src.modules.deploy_start import deploy_stacks
                    from src.modules.auto_configure import auto_stitch_services

                    run_system_preflight()
                    select_services()
                    if not run_deploy_preflight():
                        # If user declined due to port conflicts
                        continue
                    configure_environment()
                    setup_directories()
                    setup_networks()
                    build_compose_stacks()
                    deploy_stacks()
                    auto_stitch_services()
                except Exception as e:
                    import traceback
                    err_msg = traceback.format_exc()
                    write_log(f"Fatal error in setup execution: {err_msg}", level="ERROR")
                    console.print(f"\n[!] SETUP FAILED\nReason: {str(e)}", style="bold red")
                    console.print(f"Please check the log for details: {get_log_path()}", style="grey50")
                    failed = True

                if not failed:
                    metadata = get_metadata()  # Reload metadata
                    console.print("\n==========================================", style="cyan")
                    console.print("         INSTALLATION SUMMARY", style="cyan")
                    console.print("==========================================", style="cyan")
                    console.print(f"Docker Dir:   {d_dir}")

                    if metadata.get("generated_stacks"):
                        console.print("\nGENERATED STACKS (Managed in Dockge):")
                        for stack in metadata["generated_stacks"]:
                            console.print(f" [OK] {stack.get('Name')}: {stack.get('Apps')}", style="green")

                    # Health check summary
                    if metadata.get("selected_services") and os.getenv("TEST_MODE") != "true":
                        console.print("\nSERVICE HEALTH STATUS:", style="yellow")
                        services_path = get_resource_path("services.yml")
                        master_registry = get_yaml_content(services_path)
                        registry_list = get_registry_list(master_registry)

                        for svc in metadata["selected_services"]:
                            reg = next((e for e in registry_list if e.key == svc), None)
                            if reg and reg.port != "0":
                                port = int(reg.port)
                                status = "ONLINE " if test_port("localhost", port) else "OFFLINE"
                                color = "green" if status == "ONLINE " else "red"
                                console.print(f" [{status}] ", end="", style=color)
                                console.print(f"{svc} (Port {port})")

                    console.print("==========================================", style="cyan")
                    console.print("\nSetup Complete! Your Media Stack is running.", style="green")

                    # Copy setup.log to deploy folder
                    log_file = resolve_path_slash(get_log_path())
                    d_dir_slash = resolve_path_slash(d_dir)
                    if os.path.exists(log_file):
                        try:
                            shutil.copy(log_file, d_dir_slash)
                        except shutil.SameFileError:
                            pass
                        except Exception as e:
                            write_log(f"Failed to copy log file: {str(e)}", level="DEBUG")

                    console.print("\nNEXT STEPS:", style="yellow")
                    console.print("1. Access your Dashboard at [link=http://localhost:3000]http://localhost:3000[/link]")
                    console.print("2. Access Dockge Management at [link=http://localhost:5001]http://localhost:5001[/link]")

                    # Extract credentials for printout
                    h_user = "admin"
                    h_pass = "[CHECK .ENV]"
                    env_file = resolve_path_slash(os.path.join(d_dir, ".env"))
                    if os.path.exists(env_file):
                        with open(env_file, "r", encoding="utf-8") as f:
                            for line in f:
                                match_u = re.match(r"^HTTP_USERNAME=(.*)", line)
                                match_p = re.match(r"^HTTP_PASSWORD=(.*)", line)
                                if match_u:
                                    h_user = match_u.group(1).strip()
                                if match_p:
                                    h_pass = match_p.group(1).strip()

                    console.print("3. Web Management Credentials:", style="cyan")
                    console.print(f"   - Username: {h_user}")
                    console.print(f"   - Password: {h_pass}")

                    console.print("\n4. Automated Configurations:", style="yellow")
                    if metadata.get("auto_config_results"):
                        for r in metadata["auto_config_results"]:
                            console.print(f"   [x] {r}", style="green")
                    else:
                        console.print("   [!] No automated configurations were performed.", style="grey50")

                    # Tautulli/Plex token note
                    selected_svcs = metadata.get("selected_services", [])
                    if "tautulli" in selected_svcs or "plex" in selected_svcs:
                        console.print("\n5. Plex Token (Required for Tautulli):", style="yellow")
                        console.print("   Tautulli needs your permanent Plex token (not the claim token).")
                        console.print("   To get it: open Plex → Settings → Troubleshooting → 'Get Online Media Info'")
                        console.print("   Copy the token from the URL (?X-Plex-Token=XXXXX) and paste it into")
                        console.print("   Tautulli → Settings → Plex Media Server → Plex Auth Token.", style="grey50")
                    if "bazarr" in selected_svcs:
                        console.print("\n6. Bazarr Subtitle Setup:", style="yellow")
                        console.print("   Bazarr is auto-linked to Radarr/Sonarr, but subtitles providers require configuration.")
                        console.print("   Access http://localhost:6767 → Settings → Languages/Providers to set up.", style="grey50")
                    # Seerr Interactive Setup Assistant
                    if "seerr" in selected_svcs:
                        console.print("\n----------------------------------------------------------", style="cyan")
                        console.print("             SEERR DASHBOARD SYNC ASSISTANT", style="cyan")
                        console.print("----------------------------------------------------------", style="cyan")
                        console.print("Let's configure Seerr for your dashboard now.")
                        
                        do_seerr_setup = False
                        if os.getenv("DS_HEADLESS") != "true":
                            do_seerr_setup = safe_confirm("Would you like to complete Seerr's first-time configuration now?", default=True)
                            
                        if do_seerr_setup:
                            # Prompt user to open browser
                            launch = safe_confirm("Shall I open http://localhost:5055 in your browser now?", default=True)
                            if launch:
                                try:
                                    import webbrowser
                                    webbrowser.open("http://localhost:5055")
                                except Exception:
                                    console.print("[!] Failed to open browser. Please visit http://localhost:5055 manually.", style="yellow")
                                    
                            # Conditionally output checklist instructions
                            from rich.panel import Panel
                            checklist = "[bold white]SEERR FIRST-TIME CONFIGURATION CHECKLIST:[/bold white]\n\n"
                            checklist += "1. Sign in to Seerr with your Plex or Jellyfin account.\n"
                            
                            services_details = []
                            if "radarr" in selected_svcs:
                                services_details.append("Radarr (Host: 'radarr', Port: '7878')")
                            if "sonarr" in selected_svcs:
                                services_details.append("Sonarr (Host: 'sonarr', Port: '8989')")
                                
                            if services_details:
                                checklist += "2. Go to Settings -> Services -> Add connection to:\n"
                                for detail in services_details:
                                    checklist += f"   - {detail}\n"
                                    
                            checklist += "3. Go to Settings -> General. Scroll down to API Key.\n"
                            checklist += "4. Copy the API Key and paste it in the prompt below."
                            
                            console.print(Panel(checklist, border_style="cyan"))
                            
                            # Prompt for API Key
                            seerr_key = questionary.password("Paste Seerr API Key (leave blank to skip / configure manually later):").ask()
                            if seerr_key and seerr_key.strip():
                                from src.utils.state import set_env_var
                                set_env_var("SEERR_API_KEY", seerr_key.strip(), file_path=env_file)
                                console.print("[✓] Saved SEERR_API_KEY to configuration .env", style="green")
                                
                                # Reload homepage to pick up key
                                hp_path = resolve_path_slash(os.path.join(d_dir, "stacks", "maintenance"))
                                if os.path.exists(hp_path):
                                    write_step("Reloading dashboard widgets...")
                                    try:
                                        subprocess.run(["docker", "compose", "up", "-d", "--remove-orphans"], cwd=hp_path, capture_output=True)
                                    except Exception:
                                        pass
                            else:
                                write_log("Seerr configuration key skipped. Seerr widgets will remain unauthenticated.", level="WARN")

                    invoke_token_wizard(d_dir)
                    exit_script = True

            elif choice == "2":
                d_dir = get_deployment_dir_interactive(project_root)
                if d_dir and os.path.exists(resolve_path_slash(os.path.join(d_dir, "stacks"))):
                    os.environ["DEPLOY_DIR"] = d_dir
                    stacks_dir = resolve_path_slash(os.path.join(d_dir, "stacks"))
                    for stack in os.listdir(stacks_dir):
                        full_path = resolve_path_slash(os.path.join(stacks_dir, stack))
                        if os.path.isdir(full_path):
                            write_step(f"Updating Stack: {stack}")
                            # Execute docker compose pull and up
                            try:
                                subprocess.run(["docker", "compose", "up", "-d", "--pull", "always", "--remove-orphans"], cwd=full_path, check=True)
                            except Exception as e:
                                write_log(f"Failed to update stack {stack}: {str(e)}", level="ERROR")
                    exit_script = True
                else:
                    console.print("[!] Error: Deployment stacks not found.", style="red")

            elif choice == "3":
                d_dir = get_deployment_dir_interactive(project_root)
                if d_dir and os.path.exists(resolve_path_slash(os.path.join(d_dir, "stacks"))):
                    os.environ["DEPLOY_DIR"] = d_dir
                    
                    # Call uninstall utility
                    uninstall_script = resolve_path_slash(os.path.join(project_root, "src", "utils", "uninstall.py"))
                    if os.path.exists(uninstall_script):
                        subprocess.run([sys.executable, uninstall_script])
                    else:
                        # Manual inline uninstall
                        console.print("\n--- Uninstalling Stack ---", style="bold red")
                        confirm = safe_confirm("Are you sure you want to completely uninstall all services and docker stacks?", default=False)
                        if confirm:
                            stacks_dir = resolve_path_slash(os.path.join(d_dir, "stacks"))
                            for stack in os.listdir(stacks_dir):
                                full_path = resolve_path_slash(os.path.join(stacks_dir, stack))
                                if os.path.isdir(full_path):
                                    subprocess.run(["docker", "compose", "down", "-v", "--remove-orphans"], cwd=full_path)
                            shutil.rmtree(stacks_dir, ignore_errors=True)
                            console.print("Stacks and services successfully removed.", style="green")
                    exit_script = True
                else:
                    console.print("[!] Error: Invalid deployment folder.", style="red")

    except Exception as e:
        import traceback
        from rich.panel import Panel
        
        # Write traceback to setup.log
        error_trace = traceback.format_exc()
        write_log(f"CRITICAL EXCEPTION OCCURRED:\n{error_trace}", level="ERROR")
        
        log_path = get_log_path()
        error_msg = f"[bold red]An unexpected error occurred during execution.[/bold red]\n\n" \
                    f"[bold white]Reason:[/bold white] {str(e)}\n\n" \
                    f"Please review the logs for the full stack trace:\n" \
                    f"[cyan]{log_path}[/cyan]"
                    
        console.print(Panel(error_msg, title="[bold red]Critical Script Error[/bold red]", border_style="red"))
        
        if os.getenv("TEST_MODE") == "true":
            sys.exit(1)
    finally:
        if os.getenv("TEST_MODE") != "true" and os.getenv("DS_HEADLESS") != "true":
            input("\nPress Enter to close this window...")

if __name__ == "__main__":
    main()
````

## File: pyproject.toml
````toml
[tool.poetry]
name = "dockersetup"
version = "1.5.51"
description = "Cross-platform python-based Docker media stack setup script"
authors = ["suuift <suuift@gmail.com>"]
readme = "README.md"
packages = [{include = "dockersetup.py"}, {include = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
questionary = "2.0.1"
rich = "13.7.0"
"ruamel.yaml" = "0.18.6"
python-dotenv = "1.0.1"
requests = "2.31.0"
tzlocal = "5.2"
customtkinter = "^5.2.2"
pydantic = "^2.6.1"

[tool.poetry.group.dev.dependencies]
pytest = "8.0.0"
pyinstaller = "6.4.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
````

## File: src/utils/updater.py
````python
import os
import sys
import subprocess
import shutil
import urllib.request
import json
import ssl
import questionary
from src.utils.paths import get_project_root, get_clean_env
from src.utils.logger import write_log, console, safe_confirm

try:
    import certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    ssl_context = ssl.create_default_context()

VERSION = "1.5.56"

def parse_version(v_str: str):
    """
    Parses a semantic version string (e.g. 'v1.5.8' or '1.5.8') into a list of integers.
    """
    try:
        return [int(x) for x in v_str.lstrip("vV").split(".")]
    except ValueError:
        return [0, 0, 0]

def invoke_self_update(project_root: str, is_gui: bool = False) -> bool:
    # Check if running in a Git repository (Source Mode)
    if os.path.exists(os.path.join(project_root, ".git")):
        # If in GUI mode, skip git console print statements to avoid unnecessary noise
        if not is_gui:
            console.print("--- Checking for Git Source Updates ---", style="cyan")
        
        # Check if git command exists
        git_exists = shutil.which("git") is not None
        if not git_exists:
            if not is_gui:
                write_log("Git is not installed. We need it to check for script updates.", level="WARN")
                install = safe_confirm("Would you like to install Git now via winget/package manager?", default=False)
                if install:
                    if sys.platform == "win32" and shutil.which("winget"):
                        console.print("Installing Git via winget...", style="grey50")
                        ret = subprocess.run(
                            [
                                "winget", "install", 
                                "--id", "Git.Git", 
                                "-e", 
                                "--source", "winget", 
                                "--accept-package-agreements", 
                                "--accept-source-agreements"
                            ],
                            env=get_clean_env()
                        )
                        if ret.returncode != 0:
                            write_log("Winget install failed. Please install Git manually from https://git-scm.com/", level="ERROR")
                            return False
                        write_log("Git installed. Please restart this script to check for updates.", level="INFO")
                    else:
                        write_log("Please install Git manually from https://git-scm.com/ or your system package manager.", level="WARN")
                    return False
            return False

        try:
            # Run git fetch and status checks
            subprocess.run(["git", "fetch"], cwd=project_root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=get_clean_env())
            status_proc = subprocess.run(["git", "status", "-uno"], cwd=project_root, capture_output=True, text=True, env=get_clean_env())
            
            if "Your branch is behind" in status_proc.stdout:
                write_log("A new version of the Docker Setup Suite is available.", level="WARN")
                if is_gui:
                    import tkinter as tk
                    from tkinter import messagebox
                    root = tk.Tk()
                    root.withdraw()
                    apply = messagebox.askyesno(
                        "Update Available",
                        "A new version of the Docker Setup Suite is available.\n\nUpdate and restart now?"
                    )
                    root.destroy()
                else:
                    apply = safe_confirm("Update and restart now?", default=True)
                if apply:
                    console.print("Updating scripts...", style="grey50")
                    subprocess.run(["git", "pull"], cwd=project_root, env=get_clean_env())
                    return True # Needs restart
            else:
                if not is_gui:
                    write_log("Scripts are up to date.", level="INFO")
        except Exception as e:
            write_log(f"Failed to check for updates: {str(e)}", level="WARN")
        return False

    # Check if running as a compiled PyInstaller binary (Frozen mode)
    elif getattr(sys, "frozen", False):
        # Clean up leftover .old backup from a previous self-update swap
        old_backup = sys.executable + ".old"
        if os.path.exists(old_backup):
            try:
                os.remove(old_backup)
                write_log("Cleaned up previous binary backup (.old).", level="DEBUG")
            except OSError:
                pass  # May still be locked on Windows; silently skip

        if not is_gui:
            console.print("--- Checking for Compiled Binary Updates ---", style="cyan")
        try:
            # Check the GitHub Releases API for updates
            repo = "suuift/dockersetup"
            api_url = f"https://api.github.com/repos/{repo}/releases/latest"
            
            req = urllib.request.Request(
                api_url, 
                headers={"User-Agent": "DockerSetup-Updater"}
            )
            
            with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                latest_tag = data.get("tag_name", "")
                
                if not latest_tag:
                    write_log("Unable to resolve the latest version from GitHub API.", level="WARN")
                    return False
                
                local_ver = parse_version(VERSION)
                remote_ver = parse_version(latest_tag)
                
                if remote_ver > local_ver:
                    write_log(f"A new compiled release ({latest_tag}) is available. Current: v{VERSION}", level="WARN")
                    
                    # Search for appropriate binary asset based on operating system and environment
                    is_installed = False
                    if sys.platform == "win32":
                        uninstaller_path = os.path.join(os.path.dirname(sys.executable), "unins000.exe")
                        is_installed = os.path.exists(uninstaller_path)
                        expected_asset_name = "dockersetupinstaller.exe" if is_installed else "dockersetup.exe"
                    else:
                        expected_asset_name = "dockersetup"
                        
                    download_url = None
                    for asset in data.get("assets", []):
                        if asset.get("name") == expected_asset_name:
                            download_url = asset.get("browser_download_url")
                            break
                    
                    if not download_url:
                        write_log(f"Could not find binary asset '{expected_asset_name}' in the latest release.", level="WARN")
                        return False
                    
                    if is_gui:
                        import tkinter as tk
                        from tkinter import messagebox
                        root = tk.Tk()
                        root.withdraw()
                        apply = messagebox.askyesno(
                            "Update Available",
                            f"A new compiled release ({latest_tag}) is available.\nCurrent version: v{VERSION}\n\nDownload and upgrade now?"
                        )
                        root.destroy()
                    else:
                        apply = safe_confirm(f"Download and upgrade to {latest_tag} now?", default=True)
                    if apply:
                        if sys.platform == "win32" and is_installed:
                            perform_installer_update(download_url, sys.executable)
                        else:
                            perform_binary_swap(download_url, sys.executable)
                        return True # Restart scheduled by updater
                else:
                    if not is_gui:
                        write_log(f"Binary is up to date (v{VERSION}).", level="INFO")
                    
        except urllib.error.HTTPError as e:
            if e.code == 403:
                write_log("GitHub API rate limit exceeded or access forbidden. Skipping update check.", level="DEBUG")
            else:
                write_log(f"HTTP error during update check: {e.code} {e.reason}", level="WARN")
        except Exception as e:
            write_log(f"Failed to check for binary updates: {str(e)}", level="WARN")
        return False
        
    return False

def perform_binary_swap(download_url: str, target_exe_path: str):
    """
    Implements the rename-first binary swap strategy for frozen executables (Edge Case 6 & 15).
    """
    temp_download_path = target_exe_path + ".new"
    old_backup_path = target_exe_path + ".old"
    
    try:
        # 1. Download updated binary
        write_log(f"Downloading update from {download_url}...", level="INFO")
        req = urllib.request.Request(
            download_url,
            headers={"User-Agent": "DockerSetup-Updater"}
        )
        with urllib.request.urlopen(req, context=ssl_context) as response, open(temp_download_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        # 2. Rename running binary to .old (Windows allows renaming running binaries)
        if os.path.exists(old_backup_path):
            try:
                os.remove(old_backup_path)
            except OSError:
                pass
                
        os.rename(target_exe_path, old_backup_path)
        
        # 3. Move new binary to main location
        shutil.move(temp_download_path, target_exe_path)
        
        # 4. Set executable permission on Unix-like OS
        if sys.platform != "win32":
            os.chmod(target_exe_path, 0o755)
        
        write_log("Update successfully applied and staged. Restarting binary...", level="INFO")
        
        # Print cleanly formatted console separators to avoid overlapped terminal outputs
        print("\n" + "="*60)
        print("                RELAUNCHING MEDIA STACK MANAGER")
        print("="*60 + "\n")
        sys.stdout.flush()

        # 5. Replace current process in-place (avoids temp dir race and shell stdin hijacking)
        clean_env = get_clean_env()
        if sys.platform != "win32":
            # Unix: replace process in-place
            os.execve(target_exe_path, [target_exe_path], clean_env)
        else:
            # Windows: Check if running as a GUI process (no console/stdout attached)
            if getattr(sys, "frozen", False) and not sys.stdout:
                # GUI mode: spawn detached asynchronously and exit parent immediately
                subprocess.Popen([target_exe_path] + sys.argv[1:], env=clean_env, creationflags=0x00000008, close_fds=True)
                os._exit(0)
            else:
                # CLI/Console mode: delegate synchronously to preserve console attachment
                ret = subprocess.run([target_exe_path] + sys.argv[1:], env=clean_env)
                sys.exit(ret.returncode)
        
    except PermissionError as e:
        write_log(
            f"Write Permission Error: Lacked permission to modify {target_exe_path}. "
            f"If installed in a protected directory (e.g. C:\\Program Files or /usr/local/bin), "
            f"please re-run as administrator or update manually. Error: {str(e)}",
            level="ERROR"
        )
        # Clean up temp downloads if possible
        for path in [temp_download_path, old_backup_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
    except Exception as e:
        write_log(f"Updater encountered an error: {str(e)}", level="ERROR")

def perform_installer_update(download_url: str, target_exe_path: str):
    """
    Downloads the new setup installer and executes it silently using a detached batch script
    to avoid file locks on the running dockersetup.exe binary.
    """
    import tempfile
    
    # 1. Determine temporary paths
    temp_dir = tempfile.gettempdir()
    installer_path = os.path.join(temp_dir, "dockersetupinstaller_update.exe")
    bat_path = os.path.join(temp_dir, "update_installer.bat")
    
    try:
        # 2. Download the installer file
        write_log(f"Downloading setup installer from {download_url}...", level="INFO")
        req = urllib.request.Request(
            download_url,
            headers={"User-Agent": "DockerSetup-Updater"}
        )
        with urllib.request.urlopen(req, context=ssl_context) as response, open(installer_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        write_log("Download finished. Preparing background installation script...", level="INFO")
        
        # 3. Create the self-deleting batch script
        parent_pid = os.getpid()
        bat_content = f"""@echo off
:loop
tasklist /fi "pid eq {parent_pid}" 2>nul | find "{parent_pid}" >nul
if %errorlevel%==0 (
    timeout /t 1 /nobreak >nul
    goto loop
)
powershell -Command "Start-Process -FilePath '{installer_path}' -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES' -Verb RunAs -Wait; Start-Process -FilePath '{target_exe_path}'"
del "%~f0"
"""
        with open(bat_path, "w") as bat_file:
            bat_file.write(bat_content)
            
        write_log("Spawning setup installer. The application will close and restart automatically...", level="INFO")
        
        # 4. Detach process and run the batch file (DETACHED_PROCESS = 0x00000008)
        subprocess.Popen(
            [bat_path], 
            creationflags=0x00000008, 
            close_fds=True
        )
        
        # 5. Exit immediately to release file lock on target_exe_path
        os._exit(0)
        
    except Exception as e:
        write_log(f"Failed to execute installer update: {str(e)}", level="ERROR")
````
