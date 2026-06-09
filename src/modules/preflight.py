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
