import os
import sys
import platform
import subprocess
import shutil

def run_local_build(pyinstaller_cmd: str, data_sep: str, project_root: str):
    """
    Runs PyInstaller locally for the host OS.
    """
    cmd = [
        pyinstaller_cmd,
        "--onefile",
        "--clean",
        "--add-data", f"services.yml{data_sep}.",
        "--add-data", f"templates.yml{data_sep}.",
        "dockersetup.py"
    ]
    
    print(f"\n--- Running Local Build for {platform.system()} ---")
    print(" ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        output_name = "dockersetup.exe" if platform.system() == "Windows" else "dockersetup"
        print(f"[SUCCESS] Local build finished: dist/{output_name}")
        return True
    except Exception as e:
        print(f"[ERROR] Local build failed: {str(e)}")
        return False

def run_docker_linux_build(project_root: str):
    """
    Uses Docker to compile the Linux binary if running on a Windows host.
    """
    print("\n--- Running Docker-based Linux Build ---")
    
    # Check if Docker is installed and running
    if not shutil.which("docker"):
        print("[WARN] Docker CLI not found. Skipping Linux compilation (requires Docker on Windows).")
        return False

    try:
        # Check if Docker daemon is active
        subprocess.run(["docker", "version"], check=True, capture_output=True)
    except Exception:
        print("[WARN] Docker daemon is not running. Skipping Linux compilation.")
        return False

    # Convert Windows path to POSIX style for mounting
    abs_root = os.path.abspath(project_root)
    # Ensure Docker paths are mounted correctly
    mount_source = abs_root.replace("\\", "/")
    
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{mount_source}:/app",
        "-w", "/app",
        "python:3.10-slim",
        "sh", "-c", (
            "apt-get update && apt-get install -y binutils && "
            "pip install --no-cache-dir pyinstaller questionary rich ruamel.yaml python-dotenv requests tzlocal && "
            "pyinstaller --onefile --clean --add-data 'services.yml:.' --add-data 'templates.yml:.' dockersetup.py"
        )
    ]
    
    print("Executing Linux build inside Python Docker container (with binutils)...")
    print(" ".join(docker_cmd))
    
    try:
        subprocess.run(docker_cmd, check=True)
        print("[SUCCESS] Docker Linux build finished: dist/dockersetup (ELF binary)")
        return True
    except Exception as e:
        print(f"[ERROR] Docker Linux build failed: {str(e)}")
        return False

def main():
    print("=== Docker Setup Script: Cross-OS Build Automation ===")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # 1. Determine local OS and PyInstaller path
    host_os = platform.system()
    data_sep = ";" if host_os == "Windows" else ":"
    
    pyinstaller_cmd = "pyinstaller"
    venv_bin_dir = "Scripts" if host_os == "Windows" else "bin"
    venv_pyinstaller = os.path.join(project_root, ".venv", venv_bin_dir, "pyinstaller")
    if host_os == "Windows":
        venv_pyinstaller += ".exe"
        
    if os.path.exists(venv_pyinstaller):
        pyinstaller_cmd = venv_pyinstaller
    else:
        global_path = shutil.which("pyinstaller")
        if global_path:
            pyinstaller_cmd = global_path
        else:
            print("[ERROR] PyInstaller not found locally. Please run: pip install pyinstaller")
            sys.exit(1)

    # 2. Run local build
    local_success = run_local_build(pyinstaller_cmd, data_sep, project_root)
    
    # 3. Handle cross-compilation paths
    if host_os == "Windows":
        # On Windows host: Build Windows locally, use Docker to compile the Linux binary
        docker_success = run_docker_linux_build(project_root)
        
    else:
        # On Linux/macOS host
        print("\n--- Cross-compilation Warning ---")
        print("PyInstaller cannot natively compile Windows .exe files on a Linux host.")
        print("To compile for Windows on a Linux machine, you must run PyInstaller under Wine,")
        print("or set up a GitHub Actions workflow with matrix runners.")

    print("\n" + "="*45)
    print("BUILD SUMMARY:")
    print(f" Windows Executable (.exe): {'Check dist/dockersetup.exe' if os.path.exists('dist/dockersetup.exe') else 'Not Built'}")
    print(f" Linux Binary (ELF):        {'Check dist/dockersetup' if os.path.exists('dist/dockersetup') else 'Not Built'}")
    print("="*45)

if __name__ == "__main__":
    main()
