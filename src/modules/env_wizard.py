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
from src.utils.logger import write_log, console
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
    if platform.system() == "Windows":
        try:
            return get_localzone_name() or "UTC"
        except Exception:
            return "UTC"
            
    # Linux/macOS robust detection
    tz = None
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
        
    if tz and tz != "None":
        return tz
        
    try:
        val = get_localzone_name()
        if val and val != "None":
            return val
        return "UTC"
    except Exception:
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
    confirm = questionary.confirm(confirm_msg, default=True).ask()
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
    default_drive_pool = "H:/Media" if platform.system() == "Windows" else resolve_path_slash(os.path.expanduser("~/media"))
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
                mount = questionary.confirm(f"Mount drive {drive}:\\?", default=False).ask()
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
    write_log("Generating secure application passwords...", level="DEBUG")
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

    env_file = resolve_path_slash(os.path.join(docker_dir, ".env"))
    if os.path.exists(env_file) and os.getenv("DS_HEADLESS") != "true":
        overwrite = questionary.confirm(f".env already exists in {docker_dir}. Overwrite?", default=False).ask()
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
