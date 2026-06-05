import os
import sys
import json
import time
import subprocess
import questionary
from concurrent.futures import ThreadPoolExecutor
from utils.paths import get_project_root, get_deploy_dir
from utils.logger import write_log, console, write_step, invoke_external_command
from utils.state import get_metadata

def test_container_conflict(stack_path: str, stack_name: str):
    compose_path = os.path.join(stack_path, "docker-compose.yml")
    if not os.path.exists(compose_path):
        return

    # Extract container_names
    container_names = []
    with open(compose_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"container_name:\s*(.*)$", line)
            if match:
                container_names.append(match.group(1).strip())

    import re
    for name in container_names:
        # Check if container exists
        exists_proc = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name=^/{name}$", "-q"],
            capture_output=True,
            text=True
        )
        exists = exists_proc.stdout.strip()
        
        if exists:
            existing_stack = ""
            try:
                inspect_proc = subprocess.run(["docker", "inspect", name], capture_output=True, text=True)
                inspect = json.loads(inspect_proc.stdout)
                if inspect and inspect[0].get("Config", {}).get("Labels"):
                    existing_stack = inspect[0]["Config"]["Labels"].get("com.docker.compose.project", "")
            except Exception:
                write_log(f"Warning: Failed to inspect container {name} for conflict resolution.", level="WARN")

            if existing_stack and existing_stack != stack_name:
                console.print(f"\n[CONFLICT] Container '{name}' already exists and is managed by stack '{existing_stack}'.", style="yellow")
                
                if os.getenv("DS_HEADLESS") == "true":
                    raise RuntimeError(f"Deployment aborted due to container name conflict: {name}")

                choice = questionary.confirm(f"Remove existing container to allow stack '{stack_name}' to start?", default=False).ask()
                if choice:
                    write_log(f"Removing conflicting container: {name}", level="INFO")
                    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
                else:
                    raise RuntimeError(f"Deployment aborted due to container name conflict: {name}")

def pull_stack_images(stack_name: str, stack_path: str) -> str:
    try:
        # Pull images for stack
        subprocess.run(
            ["docker", "compose", "-p", stack_name, "pull", "--quiet"],
            cwd=stack_path,
            check=True,
            capture_output=True
        )
        return f"SUCCESS: Pull complete for {stack_name}"
    except Exception as e:
        return f"WARN: Pull failed or timed out for {stack_name} - {str(e)}"

def deploy_stacks() -> bool:
    write_log("Starting automated deployment...")

    project_root = get_project_root()
    deploy_dir = get_deploy_dir()
    metadata = get_metadata()
    stacks = metadata.get("generated_stacks", [])

    if not stacks:
        write_log("No generated stacks found in metadata. Skipping deployment.", level="WARN")
        return True

    stacks_dir = os.path.join(deploy_dir, "stacks")

    # 1. Start CORE stack first
    core_stack = None
    for s in stacks:
        if s.get("Name") == "core":
            core_stack = s
            break

    if core_stack:
        write_step("Initializing CORE Stack (Networking & Database)")
        path = os.path.join(stacks_dir, "core")
        if os.path.exists(path):
            test_container_conflict(path, "core")
            try:
                # Execute docker compose up (using standard streaming to prevent pipe deadlock - Edge Case 9)
                invoke_external_command(
                    "docker compose -p core up -d --quiet-pull --remove-orphans",
                    description="Starting CORE stack"
                )
            except Exception:
                raise RuntimeError("Failed to start CORE stack. Check if Docker is running and ports 80/443 are free.")
            write_log("Core stack initiated. Waiting for network baseline...")
            time.sleep(5)
        else:
            raise FileNotFoundError(f"Core stack directory missing: {path}")

    # 2. Pre-Pull Images Concurrently using ThreadPoolExecutor (Edge Case 5)
    write_step("Pre-Pulling Service Images (Concurrent)")
    pull_tasks = []
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        for stack in stacks:
            name = stack.get("Name")
            if name == "core":
                continue
            path = os.path.join(stacks_dir, name)
            if os.path.exists(path):
                write_log(f"Queuing image pull for stack: {name}", level="DEBUG")
                pull_tasks.append(executor.submit(pull_stack_images, name, path))

        # Show status spinner/dots while executing pulls
        if pull_tasks:
            console.print("    | Downloading images... ", end="", style="white")
            start_pull = time.time()
            while not all(t.done() for t in pull_tasks):
                if (time.time() - start_pull) > 600:
                    break
                console.print(".", end="")
                sys.stdout.flush()
                time.sleep(5)
            console.print("[DONE]", style="green")

            # Report any failures
            for t in pull_tasks:
                res = t.result()
                if "WARN" in res:
                    write_log(res, level="WARN")

    # 3. Start Stacks sequentially
    write_step("Initializing Service Containers (Sequenced)")
    for stack in stacks:
        name = stack.get("Name")
        if name == "core":
            continue
        path = os.path.join(stacks_dir, name)
        if os.path.exists(path):
            try:
                test_container_conflict(path, name)
            except Exception as e:
                write_log(str(e), level="ERROR")
                continue

            console.print(f"    | Starting stack: {name}... ", end="", style="white")
            try:
                invoke_external_command(
                    f"docker compose -p {name} up -d --remove-orphans",
                    description=f"Starting {name}"
                )
                
                # Verification
                exist_proc = subprocess.run(
                    ["docker", "compose", "-p", name, "ps", "-a", "-q"],
                    capture_output=True,
                    text=True
                )
                existing = exist_proc.stdout.strip()
                if not existing:
                    console.print("[FAIL]", style="red")
                    write_log(f"ERROR: Stack {name} failed to create containers.", level="ERROR")
                else:
                    console.print("[OK]", style="green")
                    write_log(f"Successfully started {name}")
            except Exception as e:
                console.print("[ERROR]", style="red")
                write_log(f"ERROR: Failed to start {name} - {str(e)}", level="ERROR")

            time.sleep(1)

    # 4. Post-Deployment Container Health Summary
    if os.getenv("TEST_MODE") != "true":
        write_step("Verifying Container Health Status")
        write_log("Waiting 5 seconds for containers to initialize before auditing health status...")
        time.sleep(5)

        try:
            all_containers_proc = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True
            )
            all_containers = [n.strip() for n in all_containers_proc.stdout.splitlines() if n.strip()]
            unhealthy_count = 0

            for c_name in all_containers:
                try:
                    inspect_proc = subprocess.run(["docker", "inspect", c_name], capture_output=True, text=True, check=True)
                    inspect = json.loads(inspect_proc.stdout)
                    if not inspect:
                        continue
                    
                    compose_proj = inspect[0].get("Config", {}).get("Labels", {}).get("com.docker.compose.project", "")
                    
                    # Verify if project matches one of our deployed stacks
                    is_managed = any(s.get("Name") == compose_proj for s in stacks)
                    
                    if is_managed:
                        health_state = "running"
                        health_info = inspect[0].get("State", {}).get("Health")
                        if health_info:
                            health_state = health_info.get("Status", "running")

                        status_style = "green"
                        if health_state == "unhealthy":
                            status_style = "bold red"
                            unhealthy_count += 1
                        elif health_state == "starting":
                            status_style = "yellow"

                        console.print(f"    | Container: {c_name.ljust(25)} Status: ", end="", style="white")
                        console.print(health_state, style=status_style)

                except Exception:
                    pass

            if unhealthy_count > 0:
                write_log(f"Deployment contains {unhealthy_count} unhealthy container(s). Please inspect logs with 'docker logs [container_name]'.", level="WARN")
            else:
                write_log("All checked container services are running or healthy.", level="INFO")

        except Exception as e:
             write_log(f"Failed to fetch health check statuses: {str(e)}", level="WARN")

    write_log("Automated deployment step finished.")
    return True
