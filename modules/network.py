import os
import subprocess
from utils.logger import write_log, console
from utils.paths import get_clean_env

def setup_networks() -> bool:
    console.print("\n--- Network Setup ---", style="cyan")

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
                console.print(f"[OK] Network '{net_name}' created", style="green")
            else:
                console.print(f"[OK] Network '{net_name}' already exists", style="green")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to check or create Docker network: {net_name}. Ensure Docker is running. Error: {str(e)}")

    return True
