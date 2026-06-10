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

# Explicit imports for strategies (required for PyInstaller tracing)
from src.modules.strategies.strategy_servarr import run_servarr_strategy
from src.modules.strategies.strategy_downloaders import run_downloaders_strategy
from src.modules.strategies.strategy_dashboards import run_dashboards_strategy
from src.modules.strategies.strategy_bazarr import run_bazarr_strategy

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
        if test_port("localhost", port):
            if not tcp_ready:
                console.print("(TCP Ready) ", end="")
                sys.stdout.flush()
                tcp_ready = True
                time.sleep(5)

            # 2. HTTP Check
            try:
                # Use Smart Verify logic for wait_for_service
                url = f"http://localhost:{port}"
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
    services_path = get_resource_path("services.yml")

    # Load Metadata
    metadata = get_metadata()
    selected = metadata.get("selected_services", [])
    if not selected:
        write_log("No selected services found in metadata. Skipping configuration.", level="WARN")
        return True

    # Load Master Registry
    master_registry = get_yaml_content(services_path)
    registry_list = get_registry_list(master_registry)

    configurable_apps = []
    if "CONFIGURABLE_APPS" in master_registry:
        configurable_apps = [a.name for a in master_registry["CONFIGURABLE_APPS"]]

    # --- 1. Service Readiness & Key Extraction ---
    keys = {}
    config_results = []

    for svc_entry in registry_list:
        svc = svc_entry.key
        try:
            port = int(svc_entry.port)
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
                        
                    # Tautulli config seeding if Plex is deployed
                    if svc == "tautulli":
                        plex_token = os.getenv("PLEX_TOKEN")
                        if plex_token and plex_token.strip():
                            config_file = os.path.join(deploy_dir, "appdata", "tautulli", "config.ini")
                            if os.path.exists(config_file):
                                try:
                                    config = configparser.ConfigParser(strict=False, empty_lines_in_values=False)
                                    config.read(config_file, encoding="utf-8")
                                    if not config.has_section("General"):
                                        config.add_section("General")
                                    config.set("General", "pms_url", "http://plex:32400")
                                    config.set("General", "pms_token", plex_token.strip())
                                    with open(config_file, "w", encoding="utf-8") as f:
                                        config.write(f)
                                    write_log("Successfully pre-seeded Tautulli config.ini with Plex token and URL.", level="INFO")
                                    config_results.append("Configured Tautulli connection to Plex")
                                except Exception as e:
                                    write_log(f"Warning: Failed to seed Tautulli config.ini: {str(e)}", level="WARN")

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
    
    # --- 3. Execute Strategies ---
    # We pass invoke_robust_rest_method to strategies to maintain the Smart Verify logic
    tier = metadata.get("tier", "1")
    
    # A. Downloaders (Auth + PVR Links)
    config_results.extend(run_downloaders_strategy(
        selected, keys, registry_list, http_user, http_pass, deploy_dir, invoke_robust_rest_method, tier
    ))

    # B. Servarr Stack (Auth + Prowlarr Links)
    config_results.extend(run_servarr_strategy(
        selected, keys, registry_list, http_user, http_pass, invoke_robust_rest_method, tier
    ))

    # C. Dashboards (Seerr Links)
    config_results.extend(run_dashboards_strategy(
        selected, keys, registry_list, invoke_robust_rest_method
    ))

    # D. Subtitles (Bazarr Links)
    config_results.extend(run_bazarr_strategy(
        selected, keys, registry_list, invoke_robust_rest_method
    ))

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
