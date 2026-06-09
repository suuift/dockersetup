import os
import subprocess
from src.utils.logger import write_log, console, write_step
from src.utils.paths import get_clean_env

def setup_networks() -> bool:
    write_step("Configuring external Docker networks")

    if os.getenv("TEST_MODE") == "true":
        write_log("TEST_MODE enabled. Skipping live docker network configuration.", level="INFO")
        return True

    required_networks = [
        {"name": "npm_proxy", "subnet": "192.168.89.0/24"},
        {"name": "media-internal", "subnet": "192.168.90.0/24"}
    ]

    for net in required_networks:
        net_name = net["name"]
        subnet = net["subnet"]

        try:
            # Check if network exists
            proc = subprocess.run(
                ["docker", "network", "ls", "--filter", f"name=^{net_name}$", "--format", "{{.Name}}"],
                capture_output=True,
                text=True,
                check=True,
                env=get_clean_env()
            )
            exists = proc.stdout.strip()
            
            if not exists:
                write_log(f"Creating external network: {net_name} ({subnet})", level="INFO")
                subprocess.run(
                    ["docker", "network", "create", net_name, f"--subnet={subnet}"],
                    check=True,
                    env=get_clean_env()
                )
                write_log(f"Network '{net_name}' created", level="DEBUG")
            else:
                write_log(f"Network '{net_name}' already exists", level="DEBUG")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to check or create Docker network: {net_name}. Ensure Docker is running. Error: {str(e)}")

    console.print("[✓] Docker networks configured", style="green")
    return True
