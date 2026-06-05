import os
import re
import hashlib
from typing import Dict, List, Any
from ruamel.yaml import YAML
from utils.logger import write_log

yaml_loader = YAML()

class YamlService:
    def __init__(self, key: str, port: str = "0", type_str: str = "none", description: str = ""):
        self.key = key
        self.port = port
        self.type = type_str
        self.description = description

class StackGroup:
    def __init__(self, name: str, services: List[str]):
        self.name = name
        self.services = services

class Recommendation:
    def __init__(self, source: str, recommendations: List[str]):
        self.source = source
        self.recommendations = recommendations

class ConfigurableApp:
    def __init__(self, name: str, alias: str):
        self.name = name
        self.alias = alias

def get_yaml_content(file_path: str) -> Dict[str, Any]:
    if not os.path.exists(file_path):
        write_log(f"YAML file not found: {file_path}", level="ERROR")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = yaml_loader.load(f)
    except Exception as e:
        write_log(f"Error loading standard YAML: {str(e)}", level="ERROR")
        return {}

    data = {}
    if not raw_data:
        return data

    for section_name, items in raw_data.items():
        data[section_name] = []
        if not items:
            continue

        for item in items:
            if not isinstance(item, str):
                continue
            parts = [p.strip() for p in item.split("|")]
            
            if section_name == "STACK_GROUPS":
                if len(parts) >= 2:
                    stack_name = parts[0]
                    services = [s.strip() for s in parts[1].split(",") if s.strip()]
                    data[section_name].append(StackGroup(stack_name, services))
            elif section_name == "RECOMMENDATIONS":
                if len(parts) >= 2:
                    source_svc = parts[0]
                    rec_svcs = [s.strip() for s in parts[1].split(",") if s.strip()]
                    data[section_name].append(Recommendation(source_svc, rec_svcs))
            elif section_name in ["CONFIGURABLE_APPS", "ARR_APPS", "SUPPORTED_WIDGETS"]:
                name = parts[0]
                alias = name
                match = re.match(r"^([^:]+):(.*)$", name)
                if match:
                    name = match.group(1).strip()
                    alias = match.group(2).strip()
                data[section_name].append(ConfigurableApp(name, alias))
            else:
                key = parts[0]
                port = "0"
                if len(parts) >= 2:
                    port = parts[1]
                type_str = "none"
                if len(parts) >= 3:
                    type_str = parts[2]
                desc = ""
                if len(parts) >= 4:
                    desc = parts[3]
                data[section_name].append(YamlService(key, port, type_str, desc))

    return data

def get_template_blocks(file_path: str) -> Dict[str, str]:
    if not os.path.exists(file_path):
        write_log(f"Template file not found: {file_path}", level="ERROR")
        return {}

    templates = {}
    current_svc = ""
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        write_log(f"Failed to read templates.yml: {str(e)}", level="ERROR")
        return {}

    for line in lines:
        # Match service_name: |
        match_svc = re.match(r"^([^:]+):\s*\|", line)
        if match_svc:
            current_svc = match_svc.group(1).strip()
            templates[current_svc] = ""
        elif line.startswith("  "):
            if current_svc:
                val = line
                if current_svc == "header":
                    val = line[2:]
                templates[current_svc] += val
        elif line.strip() and not line.startswith("  "):
            current_svc = ""

    return templates

def get_registry_list(master_registry: Dict[str, Any]) -> List[YamlService]:
    registry_list = []
    for section_name, items in master_registry.items():
        if section_name in ["STACK_GROUPS", "RECOMMENDATIONS", "CONFIGURABLE_APPS", "ARR_APPS", "SUPPORTED_WIDGETS"]:
            continue
        for item in items:
            if isinstance(item, YamlService):
                registry_list.append(item)
    return registry_list

def test_template_versions(file_path: str):
    if not os.path.exists(file_path):
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()
    except Exception:
        return

    current_service = ""
    critical_services = ["mariadb (+adminer)", "postgresql (+cloudbeaver)", "mongodb (+mongo-express)", "authelia"]

    for line in content:
        match_svc = re.match(r"^([^:]+):\s*\|", line)
        if match_svc:
            current_service = match_svc.group(1).strip()
        elif not line.strip() or not line.startswith("  "):
            if not line.strip().startswith("#"):
                current_service = ""

        if current_service and current_service in critical_services:
            match_img = re.search(r"image:\s*([^\s]+)", line)
            if match_img:
                image = match_img.group(1)
                if image.endswith(":latest") or ":" not in image:
                    write_log(
                        f"[AUDIT] Insecure tag found in critical service '{current_service}': image is using '{image}'. Consider pinning to a stable version.",
                        level="WARN"
                    )
