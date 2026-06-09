import os
import sys
import shutil
import subprocess
import questionary
from rich.console import Console
from src.utils.paths import get_clean_env
from src.utils.logger import safe_confirm

console = Console()

def main():
    deploy_dir = os.getenv("DEPLOY_DIR")
    if not deploy_dir:
        console.print("[!] Error: DEPLOY_DIR environment variable is not set.", style="bold red")
        sys.exit(1)

    deploy_dir = os.path.abspath(deploy_dir)
    stacks_dir = os.path.join(deploy_dir, "stacks")

    # 1. Validation check
    metadata_path = os.path.join(deploy_dir, ".metadata.json")
    env_path = os.path.join(deploy_dir, ".env")
    
    if not os.path.exists(stacks_dir) or not (os.path.exists(metadata_path) or os.path.exists(env_path)):
        console.print(f"[!] Security Fault: '{deploy_dir}' does not appear to be a valid DockerSetup directory.", style="bold red")
        sys.exit(1)

    console.print("\n--- Uninstalling Docker Setup Stack ---", style="bold red")
    console.print(f"Target Directory: {deploy_dir}", style="grey50")
    
    # 2. Prompts
    confirm = safe_confirm(
        "Are you sure you want to completely uninstall all services and stacks?", 
        default=False
    )
    
    if not confirm:
        console.print("Uninstall cancelled.", style="yellow")
        sys.exit(0)

    remove_volumes = safe_confirm(
        "Would you like to permanently delete Docker named volumes? (This destroys database/application state not saved to host mount folders)", 
        default=False
    )

    # Backup env file for safety
    if os.path.exists(env_path):
        backup_env = env_path + ".bak"
        try:
            shutil.copy2(env_path, backup_env)
            console.print(f"[Backup] Saved backup of configurations to {backup_env}", style="green")
        except Exception as e:
            console.print(f"[!] Warning: Could not create .env backup: {str(e)}", style="yellow")

    # 3. Teardown loop
    down_args = ["docker", "compose", "down", "--remove-orphans"]
    if remove_volumes:
        down_args.append("-v")

    stacks = [s for s in os.listdir(stacks_dir) if os.path.isdir(os.path.join(stacks_dir, s))]
    failed_stacks = []

    for stack in stacks:
        full_path = os.path.join(stacks_dir, stack)
        console.print(f"\n>> Stopping stack: {stack}...", style="cyan")
        
        try:
            # Run docker compose down
            result = subprocess.run(down_args, cwd=full_path, env=get_clean_env())
            if result.returncode != 0:
                console.print(f"[!] Warning: Docker Compose down failed for stack '{stack}'.", style="bold red")
                failed_stacks.append(stack)
        except Exception as e:
            console.print(f"[!] Error running docker compose for stack '{stack}': {str(e)}", style="bold red")
            failed_stacks.append(stack)

    # 4. Handle failures
    proceed_with_cleanup = True
    if failed_stacks:
        console.print("\n[!] Warning: The following stacks failed to teardown cleanly in Docker:", style="bold red")
        for s in failed_stacks:
            console.print(f" - {s}", style="yellow")
        
        console.print("\nIf you delete the configuration files now, these containers will become orphaned and running.")
        proceed_with_cleanup = safe_confirm(
            "Force delete stack configuration folders anyway?", 
            default=False
        )

    # 5. Directory cleanup
    if proceed_with_cleanup:
        try:
            shutil.rmtree(stacks_dir, ignore_errors=True)
            console.print("[OK] Stack configuration files successfully removed.", style="green")
            
            # Clean metadata
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
                console.print("[OK] Metadata file removed.", style="green")
        except Exception as e:
            console.print(f"[!] Error during file deletion: {str(e)}", style="bold red")
    else:
        console.print("Configuration files preserved. Please resolve Docker errors and try again.", style="yellow")

if __name__ == "__main__":
    main()
