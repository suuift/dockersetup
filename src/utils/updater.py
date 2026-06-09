import os
import sys
import subprocess
import shutil
import urllib.request
import questionary
from src.utils.paths import get_project_root, get_clean_env
from src.utils.logger import write_log, console

def invoke_self_update(project_root: str) -> bool:
    # Check if running in a Git repository (Source Mode)
    if os.path.exists(os.path.join(project_root, ".git")):
        console.print("--- Checking for Git Source Updates ---", style="cyan")
        
        # Check if git command exists
        git_exists = shutil.which("git") is not None
        if not git_exists:
            write_log("Git is not installed. We need it to check for script updates.", level="WARN")
            install = questionary.confirm("Would you like to install Git now via winget/package manager?", default=False).ask()
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
                apply = questionary.confirm("Update and restart now?", default=True).ask()
                if apply:
                    console.print("Updating scripts...", style="grey50")
                    subprocess.run(["git", "pull"], cwd=project_root, env=get_clean_env())
                    return True # Needs restart
            else:
                write_log("Scripts are up to date.", level="INFO")
        except Exception as e:
            write_log(f"Failed to check for updates: {str(e)}", level="WARN")
        return False

    # Check if running as a compiled PyInstaller binary (Frozen mode)
    elif getattr(sys, "frozen", False):
        console.print("--- Checking for Compiled Binary Updates ---", style="cyan")
        # In a real scenario, we would check a GitHub releases API.
        # For this blueprint implementation, we support the rename-and-replace update logic.
        # We can implement a placeholder update check or query a mock URL.
        # Let's write the swap logic to be fully functional.
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
        with urllib.request.urlopen(download_url) as response, open(temp_download_path, 'wb') as out_file:
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
        
        write_log("Update successfully staged. Restarting binary...", level="INFO")
        
        # 4. Spawns new process and exit
        subprocess.Popen([target_exe_path], env=get_clean_env())
        sys.exit(0)
        
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
