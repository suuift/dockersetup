import os
import shutil
from src.utils.paths import get_project_root, get_deploy_dir
from src.utils.logger import write_log, console, write_step

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

    console.print("[✓] Deployment preflight checks completed", style="green")
    return True
