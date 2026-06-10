import os
import re
from src.utils.logger import write_log, write_step

def run_servarr_strategy(selected, keys, registry_list, http_user, http_pass, rest_invoker, tier="1"):
    """
    Handles authentication injection and cross-linking for Servarr applications (Sonarr, Radarr, etc.)
    """
    results = []
    # Apps that support the standard v3/v1 Servarr API for auth and linking
    arr_apps = ["sonarr", "radarr", "lidarr", "readarr", "mylar", "prowlarr"]
    
    # Check if centralized identity provider / SSO is enabled
    identity_providers = ["authelia", "authentik"]
    sso_enabled = any(provider in selected for provider in identity_providers)
    
    # 1. Authentication Injection (Forms-based auth with management credentials)
    for app in arr_apps:
        if app in selected and app in keys and app != "prowlarr":
            reg_entry = next((e for e in registry_list if e.key == app), None)
            if reg_entry:
                write_step(f"Injecting Authentication for {app}...")
                # Sonarr/Radarr/Readarr use v3, Lidarr/Mylar/Prowlarr use v1
                api_version = "v1" if app in ["prowlarr", "lidarr", "mylar"] else "v3"
                api_url = f"http://localhost:{reg_entry.port}/api/{api_version}/config/host"
                api_key = keys[app]
                headers = {"X-Api-Key": api_key}
                
                try:
                    current_config = rest_invoker(api_url, method="GET", headers=headers)
                    if current_config:
                        # Set authentication method to External (Configurable via Config File Only)
                        current_config["authenticationMethod"] = "external"
                        
                        rest_invoker(api_url, method="PUT", json_payload=current_config, headers=headers)
                        results.append(f"Configured {app} with external authentication")
                except Exception as e:
                    write_log(f"Failed to inject auth for {app}: {str(e)}", level="WARN")

    # 2. Prowlarr Stitching (Linking Indexers to PVRs)
    if "prowlarr" in keys:
        p_key = keys["prowlarr"]
        p_url = f"http://localhost:9696/api/v1/applications?apikey={p_key}"
        
        # PVRs to link to Prowlarr, with their Servarr sync category sets
        pvr_categories = {
            "sonarr":  {"sync": [5000, 5010, 5020, 5030, 5040, 5045, 5050], "anime": [5070]},
            "radarr":  {"sync": [2000, 2010, 2020, 2030, 2040, 2045, 2050, 2060], "anime": [2070]},
            "lidarr":  {"sync": [3000, 3010, 3020, 3030, 3040], "anime": []},
            "readarr": {"sync": [7000, 7010, 7020, 7030, 7040, 7050], "anime": []},
            "mylar":   {"sync": [7000, 7010, 7020, 7030, 7040, 7050], "anime": []},
        }
        for app, cats in pvr_categories.items():
            if app in selected and app in keys:
                write_log(f"Stitching Prowlarr to {app}...")
                reg_entry = next((e for e in registry_list if e.key == app), None)
                if reg_entry:
                    fields = [
                        {"name": "prowlarrUrl", "value": "http://prowlarr:9696"},
                        {"name": "baseUrl",     "value": f"http://{app}:{reg_entry.port}"},
                        {"name": "apiKey",      "value": keys[app]},
                        {"name": "syncCategories",      "value": cats["sync"]},
                    ]
                    if cats["anime"]:
                        fields.append({"name": "animeSyncCategories", "value": cats["anime"]})

                    payload = {
                        "name": app.upper(),
                        "implementationName": app.capitalize(),
                        "implementation": app.capitalize(),
                        "configContract": f"{app.capitalize()}Settings",
                        "syncLevel": "fullSync",
                        "syncProfileIds": [1],
                        "fields": fields,
                        "tags": []
                    }
                    try:
                        rest_invoker(p_url, method="POST", json_payload=payload)
                        results.append(f"Linked Prowlarr to {app}")
                    except Exception as e:
                        write_log(f"Failed to link Prowlarr to {app}: {str(e)}", level="WARN")


        # 3. Flaresolverr Proxy (Anti-Cloudflare for Indexers)
        if "flaresolverr" in selected:
            write_log("Adding FlareSolverr proxy to Prowlarr...")
            proxy_url = f"http://localhost:9696/api/v1/indexerproxy?apikey={p_key}"
            proxy_payload = {
                "name": "FlareSolverr",
                "implementation": "FlareSolverr",
                "configContract": "FlareSolverrSettings",
                "fields": [
                    {"name": "host", "value": "http://flaresolverr:8191"},
                    {"name": "requestTimeout", "value": 60}
                ]
            }
            try:
                rest_invoker(proxy_url, method="POST", json_payload=proxy_payload)
                results.append("Added FlareSolverr proxy to Prowlarr")
            except Exception as e:
                write_log(f"Failed to add FlareSolverr proxy to Prowlarr: {str(e)}", level="WARN")

    # --- 3. Auto-Configure renaming, root directories, and import lists in PVRs ---
    for app in ["sonarr", "radarr", "lidarr"]:
        if app in selected and app in keys:
            reg_entry = next((e for e in registry_list if e.key == app), None)
            if reg_entry:
                api_key = keys[app]
                headers = {"X-Api-Key": api_key}
                base_url = f"http://localhost:{reg_entry.port}/api/v3"
                if app == "lidarr":
                    base_url = f"http://localhost:{reg_entry.port}/api/v1"

                # A. Enable Renaming
                try:
                    naming_url = f"{base_url}/config/naming"
                    naming_config = rest_invoker(naming_url, method="GET", headers=headers)
                    if naming_config:
                        naming_config["renameEpisodes"] = True
                        if app == "lidarr":
                            naming_config["renameTracks"] = True
                        rest_invoker(naming_url, method="PUT", json_payload=naming_config, headers=headers)
                        results.append(f"Enabled renaming rules for {app.capitalize()}")
                except Exception as e:
                    write_log(f"Failed to enable renaming for {app}: {str(e)}", level="WARN")

                # B. Add Root Directory
                try:
                    root_folder_url = f"{base_url}/rootfolder"
                    path_map = {"sonarr": "/tv", "radarr": "/movies", "lidarr": "/music"}
                    target_path = path_map[app]
                    payload = {"path": target_path}
                    rest_invoker(root_folder_url, method="POST", json_payload=payload, headers=headers)
                    results.append(f"Configured default root path '{target_path}' for {app.capitalize()}")
                except Exception as e:
                    # Ignore if root folder already exists (will throw 400 Bad Request)
                    pass

                # C. Configure Plex Watchlist and StevenLu lists (Import lists)
                plex_token = os.getenv("PLEX_TOKEN")
                if plex_token and plex_token.strip():
                    try:
                        list_url = f"{base_url}/importlist"
                        list_payload = {
                            "name": "Plex Watchlist",
                            "enableAuto": true,
                            "enabled": true,
                            "shouldMonitor": true,
                            "listType": "plex",
                            "implementation": "PlexWatchlistImport",
                            "configContract": "PlexWatchlistSettings",
                            "qualityProfileId": 1,
                            "rootFolderPath": "/tv" if app == "sonarr" else "/movies",
                            "searchOnAdd": true,
                            "fields": [
                                {"name": "plexToken", "value": plex_token.strip()},
                                {"name": "syncInterval", "value": 180} # 3 hours (180 minutes)
                            ],
                            "tags": []
                        }
                        # Radarr requires minimumAvailability field
                        if app == "radarr":
                            list_payload["minimumAvailability"] = "announced"
                        rest_invoker(list_url, method="POST", json_payload=list_payload, headers=headers)
                        results.append(f"Configured Plex Watchlist import list for {app.capitalize()}")
                    except Exception as e:
                        write_log(f"Failed to configure Plex Watchlist import list for {app}: {str(e)}", level="WARN")

                if app == "radarr":
                    # Add StevenLu List
                    try:
                        list_url = f"{base_url}/importlist"
                        stevenlu_payload = {
                            "name": "StevenLu List",
                            "enableAuto": true,
                            "enabled": true,
                            "shouldMonitor": true,
                            "listType": "popular",
                            "implementation": "StevenLuImport",
                            "configContract": "StevenLuSettings",
                            "qualityProfileId": 1,
                            "rootFolderPath": "/movies",
                            "searchOnAdd": false,
                            "minimumAvailability": "announced",
                            "fields": [
                                {"name": "baseUrl", "value": "https://api.radarr.video/v1/ma/movie/popular"}
                            ],
                            "tags": []
                        }
                        rest_invoker(list_url, method="POST", json_payload=stevenlu_payload, headers=headers)
                        results.append("Configured StevenLu Movie List for Radarr")
                    except Exception as e:
                        write_log(f"Failed to configure StevenLu list for Radarr: {str(e)}", level="WARN")

    # --- 4. Auto-Seed indexers in Prowlarr based on deployed clients ---
    if "prowlarr" in keys:
        p_key = keys["prowlarr"]
        prowlarr_indexers_url = f"http://localhost:9696/api/v1/indexer?apikey={p_key}"

        # Usenet Indexers (NZB) - Seeded for Minimal setup
        nzb_indexers = [
            {
                "name": "Sky-Of-Usenet",
                "implementation": "Newznab",
                "configContract": "NewznabSettings",
                "fields": [{"name": "baseUrl", "value": "https://skyofusenet.de"}]
            }
        ]
        
        # Torrent Indexers - Seeded if BitTorrent client is deployed
        torrent_indexers = [
            {
                "name": "1337x",
                "implementation": "Cardigann",
                "configContract": "CardigannSettings",
                "fields": [{"name": "baseUrl", "value": "https://1337x.to"}]
            },
            {
                "name": "EZTV",
                "implementation": "Cardigann",
                "configContract": "CardigannSettings",
                "fields": [{"name": "baseUrl", "value": "https://eztv.re"}]
            }
        ]

        indexers_to_seed = list(nzb_indexers)
        if "qbittorrent" in selected or "qbittorrent-vpn" in selected:
            indexers_to_seed.extend(torrent_indexers)

        for indexer in indexers_to_seed:
            payload = {
                "name": indexer["name"],
                "enable": true,
                "implementation": indexer["implementation"],
                "configContract": indexer["configContract"],
                "fields": indexer["fields"]
            }
            try:
                rest_invoker(prowlarr_indexers_url, method="POST", json_payload=payload)
                results.append(f"Auto-seeded Prowlarr indexer: {indexer['name']}")
            except Exception:
                # Ignore if indexer already exists
                pass

    return results