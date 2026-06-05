import os
import sys
import secrets
import string
import platform
import subprocess
import re
import socket
import questionary
from tzlocal import get_localzone_name
from utils.paths import get_project_root, get_deploy_dir
from utils.logger import write_log, console
from utils.state import get_metadata, save_env_vars

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

def configure_environment() -> bool:
    write_log("Starting configuration wizard...")
    
    project_root = get_project_root()
    deploy_dir = get_deploy_dir()

    # Load State
    metadata = get_metadata()
    selected_services = metadata.get("selected_services", [])

    console.print("\n--- System Configuration ---", style="yellow")

    # Timezone detection
    try:
        detected_tz = get_localzone_name()
    except Exception:
        detected_tz = "UTC"

    tz = get_validated_input("System Timezone", detected_tz)
    puid = get_validated_input("PUID (User ID)", "1000", r"^\d+$", "Must be numeric")
    pgid = get_validated_input("PGID (Group ID)", "1000", r"^\d+$", "Must be numeric")

    # Management Credentials
    http_user = get_validated_input("Management Username", "admin")
    
    if os.getenv("DS_HEADLESS") == "true":
        http_pass = new_random_password()
    else:
        http_pass = questionary.password("Management Password (leave blank to generate random):").ask()
        if not http_pass:
            http_pass = new_random_password()
            write_log("[!] Using generated password for this session.", level="WARN")

    console.print("\n--- Path Configuration ---", style="yellow")
    docker_dir = deploy_dir
    write_log(f"Docker Directory: {docker_dir}")
    default_drive_pool = "H:/Media" if platform.system() == "Windows" else resolve_path_slash(os.path.expanduser("~/media"))
    drive_pool = get_validated_input("Media folder directory", default_drive_pool)

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
                mount = questionary.confirm(f"Mount drive {drive}:\\?", default=False).ask()
                if mount:
                    drives_to_mount.append(f"{drive}:/")
        else:
            # On Linux list mount points under /mnt or /media
            for p in ["/mnt", "/media"]:
                if os.path.exists(p):
                    for d in os.listdir(p):
                        full_p = os.path.join(p, d)
                        if os.path.ismount(full_p):
                            if os.getenv("DS_HEADLESS") == "true":
                                continue
                            mount = questionary.confirm(f"Mount path {full_p}?", default=False).ask()
                            if mount:
                                drives_to_mount.append(full_p)
        
        if drives_to_mount:
            extra_mounts = ",".join(drives_to_mount)

    console.print("\n--- Service Secrets & Tokens ---", style="yellow")

    plex_claim = ""
    cf_token = ""
    cf_domains = ""
    ts_key = ""
    base_domain = "local.host"
    vpn_prov = ""
    vpn_client = ""
    vpn_user = ""
    vpn_pass = ""
    lan_net = ""

    if "plex" in selected_services:
        plex_claim = get_validated_input("Plex Claim Token (Optional, from https://www.plex.tv/claim)", "")

    if "cloudflare-ddns" in selected_services or "npm plus (+goaccess)" in selected_services:
        base_domain = get_validated_input("Base Domain (e.g., example.com)", "local.host")

    if "cloudflare-ddns" in selected_services:
        cf_token = get_multiline_input("Cloudflare API Token", "")
        cf_domains = get_validated_input("Cloudflare Domains (comma-separated)", "")

    if "tailscale" in selected_services:
        ts_key = get_multiline_input("Tailscale Auth Key (Optional)", "")

    if "qbittorrent-vpn" in selected_services:
        console.print("\n--- VPN Configuration ---", style="cyan")
        vpn_prov = get_validated_input("VPN Provider", "custom")
        vpn_client = get_validated_input("VPN Client", "wireguard")
        if os.getenv("DS_HEADLESS") == "true":
            vpn_user = ""
            vpn_pass = ""
        else:
            vpn_user = questionary.text("VPN Username:").ask() or ""
            vpn_pass = questionary.password("VPN Password:").ask() or ""
        lan_net = get_validated_input("Local Network Range", detect_lan_network())

    # Generate secure backend passwords
    write_log("Generating secure application passwords...")
    db_root_pass = new_random_password()
    db_pass = new_random_password()
    mongo_pass = new_random_password()
    kopia_pass = new_random_password()
    crowdsec_enabled = "true" if "crowdsec" in selected_services else "false"
    crowdsec_key = new_random_password() if crowdsec_enabled == "true" else ""

    # Compile environment variables
    # Sanitize environment variables quotes (Edge Case 17)
    vars_dict = {
        "TZ": tz, "PUID": puid, "PGID": pgid, "DOCKERDIR": docker_dir, "DRIVEPOOL": drive_pool,
        "EXTRA_MOUNTS": extra_mounts, "USERDIR": docker_dir, "MYSQL_ROOT_PASSWORD": db_root_pass,
        "MYSQL_USER": "mediauser", "MYSQL_PASSWORD": db_pass, "HTTP_USERNAME": http_user,
        "HTTP_PASSWORD": http_pass, "PLEX_CLAIM": plex_claim, "CF_API_TOKEN": cf_token,
        "CF_DOMAINS": cf_domains, "TS_AUTHKEY": ts_key, "BASE_DOMAIN": base_domain,
        "VPN_PROV": vpn_prov, "VPN_CLIENT": vpn_client, "VPN_USER": vpn_user, "VPN_PASS": vpn_pass,
        "LAN_NETWORK": lan_net, "DB_PASS": db_pass, "MONGO_PASS": mongo_pass,
        "KOPIA_PASSWORD": kopia_pass, "CROWDSEC_ENABLED": crowdsec_enabled, "CROWDSEC_API_KEY": crowdsec_key
    }

    env_file = os.path.join(docker_dir, ".env")
    if os.path.exists(env_file) and os.getenv("DS_HEADLESS") != "true":
        overwrite = questionary.confirm(f".env already exists in {docker_dir}. Overwrite?", default=False).ask()
        if not overwrite:
            write_log("Skipping .env creation.", level="INFO")
            return True

    write_log("Writing environment variables...")
    save_env_vars(vars_dict, file_path=env_file)

    # Restrict permissions (Edge Case 7 - Windows NTFS icacls, Linux POSIX chmod)
    if platform.system() == "Windows":
        try:
            # Query username
            import win32api
            username = win32api.GetUserName()
            # Windows icacls hardening
            subprocess.run(f'icacls "{env_file}" /inheritance:r /grant "{username}:F" /grant "*S-1-5-32-544:F"', shell=True, capture_output=True)
            write_log("Restricted permissions on .env (NTFS icacls).")
        except Exception as e:
            write_log(f"Failed to set .env permissions via icacls: {str(e)}", level="WARN")
    else:
        try:
            os.chmod(env_file, 0o600)
            write_log("Restricted permissions on .env (POSIX chmod 600).")
        except Exception as e:
            write_log(f"Failed to set .env permissions via chmod: {str(e)}", level="WARN")

    write_log(f".env file successfully synchronized in {docker_dir}")
    return True
