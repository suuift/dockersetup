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
    return get_project_root()
