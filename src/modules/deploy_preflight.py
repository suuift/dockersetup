import os
import shutil
import platform
import subprocess
import socket
import re
import questionary
from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path
from src.utils.logger import write_log, console, write_step, safe_confirm
from src.utils.state import get_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list

def get_port_owner(port: int) -> str:
    """
    Query the system to identify the name/PID of the application currently binding to the specified port.
    """
    try:
        if platform.system() == "Windows":
            # Find PID using netstat
            netstat_proc = subprocess.run(
                f'netstat -ano | findstr ":{port} "',
                shell=True,
                capture_output=True,
                text=True
            )
            lines = netstat_proc.stdout.strip().splitlines()
            if lines:
                # Match last column (PID)
                match = re.search(r"(\d+)\s*$", lines[0])
                if match:
                    pid = match.group(1)
                    # Resolve process name
                    task_proc = subprocess.run(
                        f'tasklist /FI "PID eq {pid}"',
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    task_lines = task_proc.stdout.strip().splitlines()
                    if len(task_lines) >= 3:
                        parts = task_lines[3].split()
                        if parts:
                            return f"{parts[0]} (PID: {pid})"
                    return f"PID: {pid}"
        else:
            # Linux port owner checks (ss -tulpn or netstat -tulpn)
            for cmd in [["ss", "-tulpn"], ["netstat", "-tulpn"]]:
                if shutil.which(cmd[0]):
                    proc = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True
                    )
                    for line in proc.stdout.splitlines():
                        if f":{port} " in line or f":{port}\t" in line or f":{port}" in line:
                            match_pid = re.search(r"users:\(\(\"([^\"]+)\",pid=(\d+)", line)
                            if match_pid:
                                return f"{match_pid.group(1)} (PID: {match_pid.group(2)})"
                            # General parsing fallback
                            match_gen = re.search(r"(\d+)/(.*)$", line.strip().split()[-1])
                            if match_gen:
                                return f"{match_gen.group(2)} (PID: {match_gen.group(1)})"
    except Exception as e:
        write_log(f"Failed to resolve port owner for port {port}: {str(e)}", level="DEBUG")
    
    return "Unknown Process"

def run_deploy_preflight() -> bool:
    write_step("Running deployment preflight checks")

    if os.getenv("TEST_MODE") == "true":
        write_log("[TEST] Bypassing Deployment Preflight Checks", level="WARN")
        return True

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()

    if not os.path.exists(deploy_dir):
        raise FileNotFoundError(f"Target deployment directory does not exist: {deploy_dir}")

    # 1. Check disk space on target drive
    try:
        total, used, free = shutil.disk_usage(deploy_dir)
        free_gb = round(free / (1024 ** 3), 2)
        
        if free_gb < 10.0:
            write_log(f"Low disk space on target directory ({free_gb} GB free). Recommended: 10GB+", level="WARN")
        else:
            write_log(f"Sufficient disk space ({free_gb} GB free)", level="DEBUG")
    except Exception as e:
        write_log(f"Failed to check disk space: {str(e)}", level="WARN")

    # 2. Check for port conflicts based on selected services
    metadata = get_metadata()
    selected_services = metadata.get("selected_services", [])
    
    if selected_services:
        write_log("Auditing active network port mappings...", level="DEBUG")
        services_path = get_resource_path("services.yml")
        master_registry = get_yaml_content(services_path)
        registry_list = get_registry_list(master_registry)
        
        # Build mapping of selected services to default ports
        conflicts = []
        for svc in selected_services:
            reg = next((e for e in registry_list if e.key == svc), None)
            if reg and reg.port and reg.port != "0":
                port_num = int(reg.port)
                
                # Fast connection test check
                try:
                    # Attempt connection to port
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect(("127.0.0.1", port_num))
                    s.close()
                    # Connection succeeded -> Port is active/blocked
                    owner = get_port_owner(port_num)
                    conflicts.append((svc, port_num, owner))
                except OSError:
                    # Connection failed -> Port is free
                    pass

        if conflicts:
            console.print("\n[bold red][!] PORT CONFLICTS DETECTED[/bold red]")
            for svc, port_num, owner in conflicts:
                msg = f"  - Port {port_num} ({svc}) is currently blocked by process: [bold yellow]{owner}[/bold yellow]"
                console.print(msg)
                write_log(f"Conflict: Port {port_num} ({svc}) is occupied by {owner}", level="WARN")
                
            if os.getenv("DS_HEADLESS") == "true":
                write_log("Proceeding in headless/test mode despite port conflicts.", level="WARN")
            else:
                choice = safe_confirm("Would you like to proceed with the setup anyway?", default=False)
                if choice is None:
                    write_log("User aborted setup during port checks.", level="WARN")
                    sys.exit(1)
                if not choice:
                    write_log("User aborted setup due to port conflicts.", level="INFO")
                    return False
        else:
            write_log("All matching ports are open and available.", level="DEBUG")
            console.print("[✓] All matching ports are open and available", style="green")

    console.print("[✓] Deployment preflight checks completed", style="green")
    return True

