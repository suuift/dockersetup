import os
import sys
import platform
import subprocess
import shutil

def run_local_build(pyinstaller_cmd: list, data_sep: str, project_root: str):
    """
    Runs PyInstaller locally for the host OS.
    """
    import customtkinter
    customtkinter_path = os.path.dirname(customtkinter.__file__)
    cmd = pyinstaller_cmd + [
        "--onefile",
        "--clean",
        "--add-data", f"resources/services.yml{data_sep}resources",
        "--add-data", f"resources/templates.yml{data_sep}resources",
        "--add-data", f"{customtkinter_path}{data_sep}customtkinter",
        "--hidden-import", "tkinter",
        "--hidden-import", "customtkinter",
        "--hidden-import", "darkdetect",
    ]
    
    # Enable automatic Administrator elevation and set icon for Windows builds
    if platform.system() == "Windows":
        cmd.append("--uac-admin")
        if os.path.exists("resources/app.ico"):
            cmd.extend(["--icon", "resources/app.ico"])
        
    cmd.append("dockersetup.py")
    
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

def compile_inno_setup(project_root: str):
    """
    Compiles the Inno Setup script into a setup installer executable.
    """
    print("\n--- Compiling Windows Setup Installer with Inno Setup ---")
    iscc_path = shutil.which("iscc")
    if not iscc_path:
        # Check standard paths
        standard_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        if os.path.exists(standard_path):
            iscc_path = standard_path
            
    if not iscc_path:
        print("[WARN] Inno Setup compiler (ISCC.exe) not found on PATH or in standard paths. Skipping installer creation.")
        return False
        
    iss_file = os.path.join(project_root, "resources", "installer.iss")
    if not os.path.exists(iss_file):
        print(f"[ERROR] Inno Setup script not found at: {iss_file}")
        return False
        
    cmd = [iscc_path, iss_file]
    print("Executing Inno Setup compilation:")
    print(" ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("[SUCCESS] Inno Setup installer compiled: dist/dockersetupinstaller.exe")
        return True
    except Exception as e:
        print(f"[ERROR] Inno Setup compilation failed: {str(e)}")
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
            "apt-get update && apt-get install -y binutils python3-tk && "
            "pip install --no-cache-dir pyinstaller questionary rich ruamel.yaml python-dotenv requests tzlocal customtkinter darkdetect && "
            "customtkinter_path=$(python -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))') && "
            "pyinstaller --onefile --clean --add-data 'resources/services.yml:resources' --add-data 'resources/templates.yml:resources' --add-data \"$customtkinter_path:customtkinter\" --hidden-import=tkinter --hidden-import=customtkinter --hidden-import=darkdetect dockersetup.py"
        )
    ]
    
    print("Executing Linux build inside Python Docker container (with binutils)...")
    print(" ".join(docker_cmd))
    
    try:
        subprocess.run(docker_cmd, check=True)
        # Copy install.sh to dist directory
        sh_src = os.path.join(project_root, "resources", "install.sh")
        sh_dst = os.path.join(project_root, "dist", "install.sh")
        if os.path.exists(sh_src):
            shutil.copy(sh_src, sh_dst)
            print("[INFO] Copied install.sh to dist/install.sh")
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
    
    pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]

    # 2. Run local build
    local_success = run_local_build(pyinstaller_cmd, data_sep, project_root)
    
    # 3. Handle cross-compilation paths
    if host_os == "Windows":
        # Compile Inno Setup installer if local build succeeded
        if local_success:
            compile_inno_setup(project_root)
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
    print(f" Windows Executable (.exe):        {'Check dist/dockersetup.exe' if os.path.exists('dist/dockersetup.exe') else 'Not Built'}")
    print(f" Windows Setup Installer (.exe):   {'Check dist/dockersetupinstaller.exe' if os.path.exists('dist/dockersetupinstaller.exe') else 'Not Built'}")
    print(f" Linux Binary (ELF):               {'Check dist/dockersetup' if os.path.exists('dist/dockersetup') else 'Not Built'}")
    print("="*45)

if __name__ == "__main__":
    main()
