import os
import sys
import shutil
import platform
import subprocess
import ctypes
from utils.logger import write_log, console

def is_admin() -> bool:
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0

def run_system_preflight() -> bool:
    console.print("\n--- System Preflight Checks ---", style="cyan")

    if os.getenv("TEST_MODE") == "true":
        write_log("[TEST] Bypassing System Preflight Checks", level="WARN")
        return True

    # 1. Python Version Check
    py_major, py_minor = sys.version_info.major, sys.version_info.minor
    if py_major < 3 or (py_major == 3 and py_minor < 10):
        raise RuntimeError(f"Python 3.10 or higher is required. You are running version {sys.version}.")
    console.print(f"[OK] Python version compatible ({sys.version.split()[0]})", style="green")

    # 2. Administrative Privileges
    if platform.system() == "Windows":
        if not is_admin():
            raise PermissionError(
                "Administrative privileges required. Please restart this script as Administrator."
            )
        console.print("[OK] Running as Administrator", style="green")
    else:
        console.print("[OK] Privilege checks passed", style="green")

    # 3. Docker Availability
    docker_cmd = shutil.which("docker")
    if not docker_cmd:
        raise FileNotFoundError("Docker not found. Please install Docker and ensure it is in your system PATH.")

    try:
        docker_version = subprocess.check_output(
            ["docker", "version", "--format", "{{.Server.Version}}"],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        console.print(f"[OK] Docker Engine detected (v{docker_version})", style="green")
    except Exception:
        raise RuntimeError("Docker daemon is not running or accessible. Please start Docker.")

    # 4. Docker Compose V2 Checks
    try:
        compose_proc = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True
        )
        if compose_proc.returncode != 0:
            raise RuntimeError("Docker Compose V2 not found. Please ensure compose plugin is active.")
        console.print("[OK] Docker Compose V2 active", style="green")
    except Exception:
         raise RuntimeError("Docker Compose V2 check failed. Make sure 'docker compose' is installed.")

    # 5. Security Utilities check
    if platform.system() == "Windows":
        if not shutil.which("icacls.exe"):
            write_log("icacls.exe not found. .env file permissions cannot be hardened.", level="WARN")
    
    # 6. Long Path Support (Windows Registry)
    if platform.system() == "Windows":
        console.print("Checking Long Path support...", style="white")
        import winreg
        registry_path = r"System\CurrentControlSet\Control\FileSystem"
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
            value, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
            if value != 1:
                try:
                    winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
                    console.print("[OK] Long Path support enabled in registry", style="green")
                except Exception:
                    write_log("Failed to enable Long Paths in Registry. Please enable manually if needed.", level="WARN")
            else:
                console.print("[OK] Long Path support active", style="green")
            winreg.CloseKey(key)
        except Exception as e:
            write_log(f"Failed to query/write Long Paths Registry settings: {str(e)}", level="WARN")

    return True
