import os
import re
from src.utils.yaml_parser import get_yaml_content, get_registry_list, get_template_blocks
from src.utils.paths import get_resource_path

def run_migration():
    services_path = get_resource_path("services.yml")
    templates_path = get_resource_path("templates.yml")
    
    master_registry = get_yaml_content(services_path)
    registry_list = get_registry_list(master_registry)
    templates = get_template_blocks(templates_path)
    
    recs_map = {}
    if "RECOMMENDATIONS" in master_registry:
        for r in master_registry["RECOMMENDATIONS"]:
            recs_map[r.source] = r.recommendations
            
    conf_apps = set()
    if "CONFIGURABLE_APPS" in master_registry:
        for c in master_registry["CONFIGURABLE_APPS"]:
            conf_apps.add(c.name)
            
    widget_apps = set()
    if "SUPPORTED_WIDGETS" in master_registry:
        for w in master_registry["SUPPORTED_WIDGETS"]:
            # Handle aliases like mylar:mylar3
            name = w.name
            if ":" in name:
                name = name.split(":")[0]
            widget_apps.add(name)
            
    groups_map = {}
    if "STACK_GROUPS" in master_registry:
        for g in master_registry["STACK_GROUPS"]:
            for svc in g.services:
                groups_map[svc] = g.name
                
    os.makedirs("src/apps", exist_ok=True)
    
    for entry in registry_list:
        key = entry.key
        safe_name = key.replace("-", "_").replace(" ", "_").replace("+", "").replace("(", "").replace(")", "")
        while "__" in safe_name:
            safe_name = safe_name.replace("__", "_")
        safe_name = safe_name.strip("_")
        
        filename = f"src/apps/{safe_name}.py"
        
        template_content = templates.get(key, "")
        pydantic_model_code = ""
        config_model_ref = "None"
        
        vars_found = re.findall(r"\${([^:-}]+)(?::-(.*?))?}", template_content)
        standard_globals = {"PUID", "PGID", "TZ", "DOCKERDIR", "USERDIR", "DATADRIVE"}
        unique_vars = {}
        for var_name, default_val in vars_found:
            if var_name not in standard_globals:
                unique_vars[var_name] = default_val or ""
                
        if unique_vars:
            class_name = "".join([part.title() for part in safe_name.split("_")]) + "Config"
            pydantic_model_code = f"from pydantic import BaseModel, Field\n\nclass {class_name}(BaseModel):\n"
            for v_name, def_val in unique_vars.items():
                if def_val.isdigit():
                    pydantic_model_code += f"    {v_name}: int = Field(default={def_val}, description=\"Custom {v_name} variable\")\n"
                else:
                    pydantic_model_code += f"    {v_name}: str = Field(default=\"{def_val}\", description=\"Custom {v_name} variable\")\n"
            config_model_ref = class_name
            
        recs = recs_map.get(key, [])
        group = groups_map.get(key, "general")
        
        code = f"from src.apps.base_app import BaseApp\n"
        if pydantic_model_code:
            code += pydantic_model_code + "\n"
            
        app_class_name = "".join([part.title() for part in safe_name.split("_")]) + "App"
        
        code += f"""class {app_class_name}(BaseApp):
    key = "{key}"
    name = "{key.title()}"
    port = {entry.port or 0}
    category = "{entry.type}"
    description = "{entry.description.replace('"', '\\"')}"
    stack_group = "{group}"
    recommendations = {recs}
    is_configurable = {key in conf_apps}
    has_widget = {key in widget_apps}
    config_model = {config_model_ref}

    def get_compose_template(self) -> str:
        return \"\"\"{template_content}\"\"\"
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
            
    print("Migration finished!")

if __name__ == "__main__":
    run_migration()
