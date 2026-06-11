import os
import sys

def resolve_path_slash(path: str) -> str:
    if not path:
        return path
    
    # Replace backslashes with forward slashes for Docker compatibility
    norm = path.replace("\\", "/")
    
    # If it is a drive letter (e.g. C:), append a slash
    if len(norm) == 2 and norm[1] == ":" and norm[0].isalpha():
        norm += "/"
        
    return norm

def get_project_root() -> str:
    # Look for dockersetup.py to locate project root
    start_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = start_dir
    while current_dir:
        if os.path.exists(os.path.join(current_dir, "dockersetup.py")):
            return resolve_path_slash(current_dir)
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            break
        current_dir = parent
    
    # Fallback default
    fallback = os.path.abspath(os.path.join(start_dir, ".."))
    return resolve_path_slash(fallback)

def get_deploy_dir() -> str:
    if os.getenv("DEPLOY_DIR"):
        return resolve_path_slash(os.getenv("DEPLOY_DIR"))
    if getattr(sys, "frozen", False):
        if sys.platform == "win32":
            return "C:/docker"
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            return "/opt/docker"
        return resolve_path_slash(os.path.expanduser("~/docker"))
    return get_project_root()

def get_resource_path(filename: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundled_path = os.path.join(sys._MEIPASS, "resources", filename)
        if os.path.exists(bundled_path):
            return resolve_path_slash(bundled_path)
        return resolve_path_slash(os.path.join(sys._MEIPASS, filename))
    return resolve_path_slash(os.path.join(get_project_root(), "resources", filename))

def get_clean_env() -> dict:
    env = os.environ.copy()
    # PyInstaller overrides library paths, polluting subprocesses. Restore original if present.
    for var in ["LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH"]:
        orig_var = var + "_ORIG"
        if orig_var in env:
            env[var] = env[orig_var]
        else:
            env.pop(var, None)
    return env
