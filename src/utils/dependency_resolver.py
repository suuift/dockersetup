from typing import List, Dict, Tuple, Optional
from src.apps.base_app import BaseApp

def check_exclusivity_conflicts(selected_apps: List[BaseApp]) -> Dict[str, List[str]]:
    """
    Checks selected apps for exclusivity group overlaps.
    Returns a dictionary mapping the exclusivity group name to the list of app names causing the conflict.
    """
    groups: Dict[str, List[BaseApp]] = {}
    for app in selected_apps:
        if app.exclusivity_group:
            groups.setdefault(app.exclusivity_group, []).append(app)
            
    conflicts: Dict[str, List[str]] = {}
    for grp, apps in groups.items():
        if len(apps) > 1:
            conflicts[grp] = [app.name for app in apps]
    return conflicts

def resolve_database_dependencies(selected_keys: List[str], apps_dict: Dict[str, BaseApp]) -> Tuple[List[str], List[str]]:
    """
    Scans selected app keys, automatically adds missing required database services,
    and returns a tuple containing:
      - The updated list of selected app keys.
      - A list of notifications describing the auto-selected database mappings.
    """
    updated_keys = list(selected_keys)
    notifications = []
    
    # Check if a database engine is already selected
    has_postgres = "postgresql_cloudbeaver" in updated_keys
    has_mysql = "mariadb_adminer" in updated_keys
    
    for key in selected_keys:
        app = apps_dict.get(key)
        if not app:
            continue
            
        if app.required_database_type:
            if app.required_database_type == "postgres" and not has_postgres:
                updated_keys.append("postgresql_cloudbeaver")
                has_postgres = True
                notifications.append(
                    f"Automatically selected PostgreSQL (CloudBeaver) as a dependency for {app.name}."
                )
            elif app.required_database_type == "mysql" and not has_mysql:
                updated_keys.append("mariadb_adminer")
                has_mysql = True
                notifications.append(
                    f"Automatically selected MariaDB (Adminer) as a dependency for {app.name}."
                )
                
    return updated_keys, notifications
