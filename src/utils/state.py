import os
import json
import re
from typing import Any, Dict
from src.utils.paths import get_deploy_dir, resolve_path_slash
from src.utils.logger import write_log

# Caching variables
_metadata_cache = None
_env_cache = {}

def get_metadata_path() -> str:
    deploy_dir = get_deploy_dir()
    return resolve_path_slash(os.path.join(deploy_dir, ".metadata.json"))

def get_metadata() -> Dict[str, Any]:
    global _metadata_cache
    if _metadata_cache is not None:
        return _metadata_cache

    path = get_metadata_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                _metadata_cache = data
                return data
        except Exception:
            return {}
    return {}

def set_metadata(data: Dict[str, Any]):
    global _metadata_cache
    path = get_metadata_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        _metadata_cache = data
    except Exception as e:
        write_log(f"Failed to save .metadata.json: {str(e)}", level="ERROR")

def set_env_var(key: str, value: str, file_path: str = None):
    if not file_path:
        deploy_dir = get_deploy_dir()
        if deploy_dir:
            file_path = os.path.join(deploy_dir, ".env")
        else:
            raise ValueError("DEPLOY_DIR not set")

    # Clear cached env if exists
    if file_path in _env_cache:
        del _env_cache[file_path]

    # Handle multi-line secrets escaping
    formatted_val = value
    if "\n" in value or "\r" in value:
        formatted_val = f'"{value.replace(chr(34), chr(92) + chr(34))}"'  # Replace " with \"

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{key}={formatted_val}\n")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    found = False
    new_lines = []
    escaped_key = re.escape(key)
    
    for line in lines:
        if re.match(f"^{escaped_key}=", line):
            new_lines.append(f"{key}={formatted_val}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"{key}={formatted_val}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def save_env_vars(vars_dict: Dict[str, str], file_path: str = None):
    if not file_path:
        deploy_dir = get_deploy_dir()
        if deploy_dir:
            file_path = os.path.join(deploy_dir, ".env")
        else:
            raise ValueError("DEPLOY_DIR not set")

    if file_path in _env_cache:
        del _env_cache[file_path]

    lines = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    updated_keys = set()
    new_lines = []

    for line in lines:
        match = re.match(r"^([^=]+)=(.*)$", line)
        if match:
            k = match.group(1).strip()
            if k in vars_dict:
                val = vars_dict[k]
                if "\n" in val or "\r" in val:
                    val = f'"{val.replace(chr(34), chr(92) + chr(34))}"'
                new_lines.append(f"{k}={val}\n")
                updated_keys.add(k)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    for k, val in vars_dict.items():
        if k not in updated_keys:
            if "\n" in val or "\r" in val:
                val = f'"{val.replace(chr(34), chr(92) + chr(34))}"'
            new_lines.append(f"{k}={val}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
