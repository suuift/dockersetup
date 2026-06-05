import os
import platform
import re
from utils.paths import get_project_root, get_deploy_dir, resolve_path_slash
from utils.logger import write_log, console
from utils.state import get_metadata

def setup_directories() -> bool:
    console.print("\n--- Setting up directories ---", style="cyan")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    env_path = os.path.join(deploy_dir, ".env")

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
                if k in ["DOCKERDIR", "DRIVEPOOL"]:
                    v = resolve_path_slash(v)
                    # Cross-platform drive letter mapping to standard Unix mount paths
                    if platform.system() != "Windows":
                        match_drive = re.match(r"^([A-Za-z]):(.*)$", v)
                        if match_drive:
                            v = f"/mnt/{match_drive.group(1).lower()}{match_drive.group(2)}"
                env_vars[k] = v

    docker_dir = env_vars.get("DOCKERDIR")
    drive_pool = env_vars.get("DRIVEPOOL")

    if not docker_dir or not drive_pool:
        raise ValueError("DOCKERDIR or DRIVEPOOL missing in .env configurations.")

    metadata = get_metadata()
    selected = metadata.get("selected_services", [])
    if not selected:
        write_log("No service selection found in metadata. Service-specific directories will be skipped.", level="WARN")

    # Create appdata folders for selected services
    for app in selected:
        clean_app = app.lower().split(" ")[0]  # E.g. mariadb (+adminer) -> mariadb
        
        path = os.path.join(docker_dir, "appdata", clean_app, "config")
        if clean_app == "dockge":
            path = os.path.join(docker_dir, "appdata", "dockge", "data")
            
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                console.print(f"Created: {path}", style="grey50")
            except Exception as e:
                raise PermissionError(f"Failed to create directory: {path}. Ensure you have write permissions. Error: {str(e)}")

    # Create stacks directory for Dockge
    stacks_dir = os.path.join(docker_dir, "stacks")
    if not os.path.exists(stacks_dir):
        try:
            os.makedirs(stacks_dir, exist_ok=True)
            console.print(f"Created: {stacks_dir}", style="grey50")
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
        path = os.path.join(drive_pool, folder)
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                console.print(f"Created: {path}", style="grey50")
            except Exception as e:
                write_log(f"Warning: Could not create media folder {path}. It may need to be created manually. Error: {str(e)}", level="WARN")

    # Create placeholder files
    shared_path = os.path.join(docker_dir, "shared")
    os.makedirs(shared_path, exist_ok=True)
    htpasswd_path = os.path.join(shared_path, ".htpasswd")
    if not os.path.exists(htpasswd_path):
        with open(htpasswd_path, "w", encoding="utf-8") as f:
            pass

    console.print("[OK] Directory structure ready", style="green")
    return True
