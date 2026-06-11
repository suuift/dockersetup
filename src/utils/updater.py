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

VERSION = "1.5.45"

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
        # os.execve is used on Unix to pass a clean environment block explicitly
        clean_env = get_clean_env()
        if sys.platform != "win32":
            os.execve(target_exe_path, [target_exe_path], clean_env)
        else:
            os.environ.clear()
            os.environ.update(clean_env)
            os.execv(target_exe_path, [target_exe_path])
        
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
