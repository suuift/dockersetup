import os
import socket
from typing import List, Dict, Set
from src.apps.base_app import BaseApp

def is_port_in_use(port: int) -> bool:
    """Checks if a port is locally bound/in use by the host OS."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.bind(("127.0.0.1", port))
            return False
        except socket.error:
            return True

def resolve_port_conflicts(selected_apps: List[BaseApp], env_path: str) -> List[str]:
    """
    Scans selected apps for overlapping ports. Auto-resolves by incrementing
    and writing host environment variable overrides (e.g. KEY_PORT) to .env if in use.
    Returns a list of override notification strings.
    """
    notifications = []
    allocated_ports: Dict[int, str] = {}
    
    # 1. Gateway/Reverse Proxy services have priority and immutable ports
    immutables = {"caddy", "npm_plus_goaccess"}
    
    # Track existing .env variables to keep manually configured ports
    existing_env: Dict[str, str] = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    existing_env[k.strip()] = v.strip()

    # Place proxy services first
    sorted_apps = sorted(selected_apps, key=lambda a: 0 if a.key in immutables else 1)

    for app in sorted_apps:
        port = int(app.port)
        if port == 0:
            continue

        env_key = f"{app.key.replace('-', '_').upper()}_PORT"
        
        # Respect existing env definitions first
        if env_key in existing_env:
            try:
                port = int(existing_env[env_key])
            except ValueError:
                pass

        # Check for overlaps
        if port in allocated_ports or is_port_in_use(port):
            if app.key in immutables:
                # Proxy ports are immutable, register as allocated
                allocated_ports[port] = app.key
                continue

            # Auto-resolve: find next available port
            candidate_port = port
            while is_port_in_use(candidate_port) or candidate_port in allocated_ports:
                candidate_port += 1
                
            notifications.append(
                f"Resolved port collision for {app.name}: mapped port {port} -> {candidate_port}."
            )
            port = candidate_port
            
            # Save to env
            # (In a real run, the caller or env writer will persist this to the actual file)
            existing_env[env_key] = str(port)

        allocated_ports[port] = app.key

    # Save all resolves back to .env
    if notifications:
        lines = []
        for k, v in existing_env.items():
            lines.append(f"{k}={v}\n")
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return notifications
