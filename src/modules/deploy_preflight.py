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
        
        resolved_ports = metadata.get("resolved_ports", {})
        conflicts = []
        
        for svc in selected_services:
            reg = next((e for e in registry_list if e.key == svc), None)
            if reg and reg.port and reg.port != "0":
                port_num = int(reg.port)
                
                # Check connection
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect(("127.0.0.1", port_num))
                    s.close()
                    owner = get_port_owner(port_num)
                    conflicts.append((svc, port_num, owner))
                except OSError:
                    pass

        if conflicts:
            from src.utils.state import set_metadata
            console.print("\n[bold red][!] PORT CONFLICTS DETECTED[/bold red]")
            
            for svc, port_num, owner in conflicts:
                write_log(f"Conflict: Port {port_num} ({svc}) occupied by {owner}", level="WARN")
                
                # Headless/Test mode fallback
                if os.getenv("DS_HEADLESS") == "true" and os.getenv("DS_GUI_MODE") != "true":
                    write_log(f"Headless mode bypass for {svc} on port {port_num}.", level="WARN")
                    continue
                    
                # 1. Identify container details
                try:
                    from src.utils.paths import get_clean_env
                    res = subprocess.run(
                        ["docker", "ps", "--filter", f"publish={port_num}", "--format", "{{.Names}}"],
                        capture_output=True, text=True, env=get_clean_env()
                    )
                    container_name = res.stdout.strip()
                except Exception:
                    container_name = ""
                    
                is_same_type = container_name and svc.lower() in container_name.lower()
                
                # Find alternative port
                alt_port = port_num
                while True:
                    alt_port += 1
                    try:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s2.settimeout(0.2)
                        s2.connect(("127.0.0.1", alt_port))
                        s2.close()
                    except OSError:
                        break
                
                resolved_choice = None
                
                if os.getenv("DS_GUI_MODE") == "true":
                    from tkinter import messagebox
                    if is_same_type:
                        gui_choice = messagebox.askyesnocancel(
                            "Port Conflict Detected",
                            f"Port {port_num} is occupied by an existing {svc.upper()} container ('{container_name}').\n\n"
                            f"Click YES to Stop & Replace the existing container.\n"
                            f"Click NO to Coexist (run this new instance on port {alt_port}).\n"
                            f"Click CANCEL to abort installation."
                        )
                        if gui_choice is None:
                            resolved_choice = "cancel"
                        elif gui_choice is True:
                            resolved_choice = "replace"
                        else:
                            resolved_choice = "coexist"
                    else:
                        gui_shift = messagebox.askyesno(
                            "Port Conflict",
                            f"Port {port_num} ({svc}) is occupied by process:\n{owner}\n\n"
                            f"Would you like to automatically switch '{svc}' to port {alt_port}?"
                        )
                        resolved_choice = "coexist" if gui_shift else "cancel"
                else:
                    # CLI prompt
                    if is_same_type:
                        console.print(f"\n[bold yellow][i] Port {port_num} is occupied by an existing {svc.upper()} container ('{container_name}')[/bold yellow]")
                        cli_choice = questionary.select(
                            "What would you like to do?",
                            choices=[
                                questionary.Choice("Stop & Replace the existing container", value="replace"),
                                questionary.Choice("Coexist (Run new instance on a different port)", value="coexist"),
                                questionary.Choice("Cancel installation", value="cancel")
                            ]
                        ).ask()
                        resolved_choice = cli_choice or "cancel"
                    else:
                        console.print(f"\n[bold yellow][!] Port conflict detected on port {port_num} for service '{svc}'[/bold yellow]")
                        console.print(f"Occupant: {owner}")
                        shift = safe_confirm(f"Would you like to automatically switch '{svc}' to port {alt_port}?", default=True)
                        resolved_choice = "coexist" if shift else "cancel"
                
                if resolved_choice == "cancel":
                    write_log("User aborted installation due to port conflicts.", level="INFO")
                    return False
                elif resolved_choice == "replace":
                    write_step(f"Stopping and removing conflicting container '{container_name}'...")
                    try:
                        from src.utils.paths import get_clean_env
                        subprocess.run(["docker", "stop", container_name], env=get_clean_env(), capture_output=True)
                        subprocess.run(["docker", "rm", container_name], env=get_clean_env(), capture_output=True)
                        console.print(f"[✓] Removed container '{container_name}'. Port {port_num} is now available.", style="green")
                    except Exception as e:
                        write_log(f"Failed to remove container: {str(e)}", level="ERROR")
                        # Fallback to coexist
                        resolved_choice = "coexist"
                        
                if resolved_choice == "coexist":
                    resolved_ports[svc] = alt_port
                    write_log(f"Reallocated {svc} to alternative port {alt_port}.", level="INFO")
                    console.print(f"[✓] Reallocated {svc} to port {alt_port}.", style="green")
            
            metadata["resolved_ports"] = resolved_ports
            set_metadata(metadata)
        else:
            write_log("All matching ports are open and available.", level="DEBUG")
            console.print("[✓] All matching ports are open and available", style="green")

    console.print("[✓] Deployment preflight checks completed", style="green")
    return True

