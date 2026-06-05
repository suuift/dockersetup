import os
import sys
import re
import time
import socket
import xml.etree.ElementTree as ET
import configparser
import requests
import questionary
from utils.paths import get_project_root, get_deploy_dir
from utils.logger import write_log, console, write_step, invoke_external_command
from utils.state import get_metadata, set_metadata, set_env_var
from utils.yaml_parser import get_yaml_content, get_registry_list

def test_port(host: str, port: int, timeout: int = 2) -> bool:
    """
    Cross-platform socket connectivity check replacing Test-NetConnection (Edge Case 13).
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
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
                response = requests.get(f"http://localhost:{port}", timeout=2, verify=False)
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
    # verify=False for self-signed certificates (Edge Case 1)
    
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
                verify=False
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
    write_log("Initializing automated service stitching...")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    env_path = os.path.join(deploy_dir, ".env")
    services_path = os.path.join(project_root, "services.yml")

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
    arr_apps = []
    if "CONFIGURABLE_APPS" in master_registry:
        configurable_apps = [a.name for a in master_registry["CONFIGURABLE_APPS"]]
    if "ARR_APPS" in master_registry:
        arr_apps = [a.name for a in master_registry["ARR_APPS"]]

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
                        
                        env_key = f"{svc}_API_KEY".upper().replace("-", "_")
                        set_env_var(env_key, key, file_path=env_path)

    # --- 2. Service Stitching & Auth Automation ---
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
        write_log("HTTP_PASSWORD not found in env vars or .env file. Skipping authentication injection.", level="WARN")
        return True

    # A. *arr Authentication Injection
    for app in arr_apps:
        if app in selected and app in keys:
            # Find registry entry
            reg_entry = next((e for e in registry_list if e.key == app), None)
            if reg_entry:
                write_step(f"Injecting Authentication for {app}...")
                api_url = f"http://localhost:{reg_entry.port}/api/v3/config/host"
                api_key = keys[app]
                headers = {"X-Api-Key": api_key}
                
                try:
                    current_config = invoke_robust_rest_method(api_url, method="GET", headers=headers)
                    if current_config:
                        current_config["authenticationMethod"] = "forms"
                        current_config["username"] = http_user
                        current_config["password"] = http_pass
                        
                        invoke_robust_rest_method(api_url, method="PUT", json_payload=current_config, headers=headers)
                        config_results.append(f"Secured {app} with management credentials")
                except Exception as e:
                    write_log(f"Failed to inject auth for {app}: {str(e)}", level="WARN")

    # B. SABnzbd Config Injection
    if "sabnzbd" in selected and "sabnzbd" in keys:
        write_step("Injecting Authentication for SABnzbd...")
        sab_ini = os.path.join(deploy_dir, "appdata/sabnzbd/config/sabnzbd.ini")
        if os.path.exists(sab_ini):
            try:
                with open(sab_ini, "r", encoding="utf-8") as f:
                    ini_content = f.read()
                
                new_ini = re.sub(r"^username\s*=.*", lambda m: f"username = {http_user}", ini_content, flags=re.MULTILINE)
                new_ini = re.sub(r"^password\s*=.*", lambda m: f"password = {http_pass}", new_ini, flags=re.MULTILINE)
                
                with open(sab_ini, "w", encoding="utf-8") as f:
                    f.write(new_ini)
                config_results.append("Secured SABnzbd with management credentials")
            except Exception as e:
                write_log(f"Failed to write SABnzbd auth configurations: {str(e)}", level="WARN")

    # C. qBittorrent API Handshake
    if "qbittorrent" in selected or "qbittorrent-vpn" in selected:
        qbit_port = 8081
        if wait_for_service("qbittorrent", qbit_port, max_timeout_seconds=30):
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
                        timeout=5
                    )
                    if res.text.strip() == "Ok.":
                        login_success = True
                        break
                except Exception:
                    pass
            
            if login_success:
                try:
                    import json
                    prefs = {"web_ui_username": http_user, "web_ui_password": http_pass}
                    qbit_session.post(
                        f"http://localhost:{qbit_port}/api/v2/app/setPreferences",
                        data={"json": json.dumps(prefs)},
                        timeout=5
                    )
                    config_results.append("Secured qBittorrent with management credentials")
                except Exception as e:
                    write_log(f"Failed to set qBittorrent preferences: {str(e)}", level="WARN")

    # D. Prowlarr -> PVRs
    if "prowlarr" in keys:
        p_key = keys["prowlarr"]
        p_url = f"http://localhost:9696/api/v1/applications?apikey={p_key}"
        for app in ["sonarr", "radarr", "lidarr"]:
            if app in selected and app in keys:
                write_log(f"Stitching Prowlarr to {app}...")
                reg_entry = next((e for e in registry_list if e.key == app), None)
                if reg_entry:
                    payload = {
                        "name": app.upper(),
                        "configContract": "ServarrSettings",
                        "implementation": "Servarr",
                        "fields": [
                            {"name": "prowlarrUrl", "value": "http://prowlarr:9696"},
                            {"name": "baseUrl", "value": f"http://{app}:{reg_entry.port}"},
                            {"name": "apiKey", "value": keys[app]},
                            {"name": "syncLevel", "value": "fullSync"}
                        ]
                    }
                    try:
                        invoke_robust_rest_method(p_url, method="POST", json_payload=payload)
                        config_results.append(f"Linked Prowlarr to {app}")
                    except Exception as e:
                        write_log(f"Failed to link Prowlarr to {app}: {str(e)}", level="WARN")

        # Flaresolverr Proxy
        if "flaresolverr" in selected:
            write_log("Adding FlareSolverr proxy to Prowlarr...")
            proxy_url = f"http://localhost:9696/api/v1/proxies?apikey={p_key}"
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
                invoke_robust_rest_method(proxy_url, method="POST", json_payload=proxy_payload)
                config_results.append("Added FlareSolverr proxy to Prowlarr")
            except Exception as e:
                write_log(f"Failed to add FlareSolverr proxy to Prowlarr: {str(e)}", level="WARN")

    # E. Downloaders -> PVRs
    pvr_apps = ["sonarr", "radarr", "lidarr"]
    for app in pvr_apps:
        if app in selected and app in keys:
            reg_entry = next((e for e in registry_list if e.key == app), None)
            if reg_entry:
                app_url = f"http://localhost:{reg_entry.port}/api/v3/downloadclient?apikey={keys[app]}"
                
                # SABnzbd
                if "sabnzbd" in selected and "sabnzbd" in keys:
                    write_log(f"Linking SABnzbd to {app}...")
                    sab_payload = {
                        "enable": True, "priority": 1, "name": "SABnzbd", "implementation": "Sabnzbd", "configContract": "SabnzbdSettings",
                        "fields": [
                            {"name": "host", "value": "sabnzbd"}, {"name": "port", "value": 8080},
                            {"name": "apiKey", "value": keys["sabnzbd"]}, {"name": "movieCategory", "value": "movies"},
                            {"name": "tvCategory", "value": "tv"}
                        ]
                    }
                    try:
                        invoke_robust_rest_method(app_url, method="POST", json_payload=sab_payload)
                        config_results.append(f"Connected SABnzbd to {app}")
                    except Exception as e:
                        write_log(f"Failed to connect SABnzbd to {app}: {str(e)}", level="WARN")

    # F. PVRs -> Seerr
    if "seerr" in selected and "seerr" in keys:
        s_key = keys["seerr"]
        s_header = {"X-Api-Key": s_key}
        for app in ["sonarr", "radarr"]:
            if app in selected and app in keys:
                write_log(f"Linking {app} to Seerr...")
                reg_entry = next((e for e in registry_list if e.key == app), None)
                if reg_entry:
                    endpoint = "settings/radarr" if app == "radarr" else "settings/sonarr"
                    active_dir = "/movies" if app == "radarr" else "/tv"
                    payload = {
                        "name": f"{app.upper()} (Auto)", "hostname": app, "port": int(reg_entry.port),
                        "apiKey": keys[app], "useSsl": False, "isDefault": True,
                        "activeProfileId": 1, "activeDirectory": active_dir
                    }
                    if app == "sonarr":
                        payload["activeLanguageProfileId"] = 1
                    
                    try:
                        invoke_robust_rest_method(f"http://localhost:5055/api/v1/{endpoint}", method="POST", json_payload=payload, headers=s_header)
                        config_results.append(f"Linked {app} to Seerr")
                    except Exception as e:
                        write_log(f"Failed to link {app} to Seerr: {str(e)}", level="WARN")

    # Save results
    metadata["auto_config_results"] = config_results
    set_metadata(metadata)

    # --- 3. Restart Dependent Stacks ---
    write_log("Reloading dashboard and maintenance stacks to apply new keys...")
    stacks_to_reload = ["maintenance", "media-server"]
    for st in stacks_to_reload:
        st_path = os.path.join(deploy_dir, "stacks", st)
        if os.path.exists(st_path):
            console.print(f"Reloading stack: {st}", style="cyan")
            if os.getenv("TEST_MODE") == "true":
                write_log("TEST_MODE enabled. Skipping live docker stack reload.", level="INFO")
                continue
            try:
                invoke_external_command(
                    "docker compose up -d --remove-orphans",
                    description=f"Reloading {st}"
                )
            except Exception:
                pass

    write_log("Automated stitching complete.")
    return True
