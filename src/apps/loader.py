import os
import pkgutil
import importlib
from typing import Dict, List
from src.apps.base_app import BaseApp

_loaded_apps: Dict[str, BaseApp] = {}

def load_apps() -> Dict[str, BaseApp]:
    global _loaded_apps
    if _loaded_apps:
        return _loaded_apps

    package_dir = os.path.dirname(__file__)
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        if module_name in ["base_app", "loader"]:
            continue
        try:
            full_module_name = f"src.apps.{module_name}"
            module = importlib.import_module(full_module_name)
            
            for attribute_name in dir(module):
                try:
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, BaseApp) and attribute is not BaseApp:
                        app_instance = attribute()
                        if app_instance.key:
                            _loaded_apps[app_instance.key] = app_instance
                except Exception as ex:
                    from src.utils.logger import write_log
                    write_log(f"Failed to load class '{attribute_name}' in '{module_name}': {str(ex)}", level="ERROR")
        except Exception as e:
            from src.utils.logger import write_log
            write_log(f"Failed to load app plugin '{module_name}': {str(e)}", level="ERROR")
            
    return _loaded_apps

def get_apps_list() -> List[BaseApp]:
    apps_dict = load_apps()
    return sorted(apps_dict.values(), key=lambda x: x.key)
