# DockerSetup (Python)

A professional-grade, cross-platform Python automation suite for deploying a complete Media and Home Server stack on Windows and Linux using Docker.

## Quick Start

The fastest way to deploy DockerSetup is using the pre-compiled standalone binaries.

### Windows (PowerShell)
Run this command in an Administrative PowerShell session to download and start the setup wizard immediately:
```powershell
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/suuift/dockersetup/releases/download/v0.9.0-beta/dockersetup.exe' -OutFile 'dockersetup.exe'; .\dockersetup.exe"
```

### Linux (Shell)
Run this command in your terminal:
```bash
curl -L -o dockersetup https://github.com/suuift/dockersetup/releases/download/v0.9.0-beta/dockersetup && chmod +x dockersetup && ./dockersetup
```

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

*   **Cross-Platform Portability:** Runs seamlessly on both Windows and Linux environments.
*   **Stateless Builder Architecture:** The project root remains clean. All configurations, state files, and deployment logic are written directly to your chosen target directory.
*   **Self-Healing Updates:** Every time you launch the setup script, it checks for updates from the repository, with support for seamless binary-renaming swaps.
*   **Intelligent Migration:** Detects existing deployments and offers one-click Template Upgrades to apply the latest security and performance optimizations to your stacks without touching your data.
*   **Multi-Stack Deployment:** Automatically splits services into logical groups (Core, Media-PVR, Downloaders, etc.) for isolation and management via Dockge.
*   **Zero-Touch Authentication:** Automatically secures 11+ application web interfaces (Sonarr, Radarr, qBittorrent, etc.) using your custom management credentials.
*   **Rich Dashboards:** Generates a professional Homepage dashboard pre-configured with live data widgets for active downloads, library statistics, and service health.
*   **Advanced Stitching:** Automatically links services (e.g., Prowlarr to PVRs, FlareSolverr to Prowlarr, Seerr to Radarr) during installation.
*   **Concurrent Image Downloads:** Employs a thread pool to download service images concurrently, significantly speeding up deployment.

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
*   **Security:** CrowdSec (LAPI + NPM Integration), Vaultwarden (Bitwarden), Authelia.
*   **Networking:** Nginx Proxy Manager Plus, Tailscale VPN, Cloudflare DDNS.
*   **Media & Music:** Navidrome (Music Server), Audiobookshelf (Books/Podcasts).
*   **Management:** Portainer, Dockge, Uptime Kuma, Scrutiny (HDD Health).
*   **Productivity:** Immich (Photos), Paperless-ngx, Syncthing, CloudCmd, FileBrowser.
*   **Games:** Valheim, Satisfactory, Enshrouded, Modded Terraria.

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
