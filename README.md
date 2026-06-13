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
