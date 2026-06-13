from src.apps.base_app import BaseApp
class ProwlarrApp(BaseApp):
    key = "prowlarr"
    name = "Prowlarr"
    port = 9696
    category = "indexers"
    description = "Indexer manager/proxy that integrates with your PVR apps to manage Torrent Trackers and Usenet Indexers in one place."
    stack_group = "media-pvr"
    recommendations = []
    is_configurable = True
    has_widget = True
    config_model = None

    def get_compose_template(self) -> str:
        return """  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    <<: *common-keys-apps
    volumes:
      - $DOCKERDIR/appdata/prowlarr/config:/config
    ports:
      - ${PROWLARR_PORT:-9696}:9696
    environment:
      <<: *default-tz-puid-pgid
"""

    def run_stitching(self, keys: dict, deploy_dir: str, rest_invoker) -> list:
        from src.utils.logger import write_log, write_step
        from src.utils.state import get_metadata
        import os
        results = []
        if self.key in keys:
            p_key = keys[self.key]
            env_port = os.getenv("PROWLARR_PORT")
            port = int(env_port) if (env_port and env_port.isdigit()) else self.port
            p_url = f"http://localhost:{port}/api/v1/applications?apikey={p_key}"
            prowlarr_indexers_url = f"http://localhost:{port}/api/v1/indexer?apikey={p_key}"

            metadata = get_metadata()
            selected = metadata.get("selected_services", [])

            pvr_categories = {
                "sonarr":  {"sync": [5000, 5010, 5020, 5030, 5040, 5045, 5050], "anime": [5070], "port": 8989},
                "radarr":  {"sync": [2000, 2010, 2020, 2030, 2040, 2045, 2050, 2060], "anime": [2070], "port": 7878},
                "lidarr":  {"sync": [3000, 3010, 3020, 3030, 3040], "anime": [], "port": 8686},
                "readarr": {"sync": [7000, 7010, 7020, 7030, 7040, 7050], "anime": [], "port": 8787},
                "mylar":   {"sync": [7000, 7010, 7020, 7030, 7040, 7050], "anime": [], "port": 8090},
            }

            for app, cats in pvr_categories.items():
                if app in selected and app in keys:
                    write_log(f"Stitching Prowlarr to {app}...")
                    fields = [
                        {"name": "prowlarrUrl", "value": "http://prowlarr:9696"},
                        {"name": "baseUrl",     "value": f"http://{app}:{cats['port']}"},
                        {"name": "apiKey",      "value": keys[app]},
                        {"name": "syncCategories",      "value": cats["sync"]},
                    ]
                    if cats["anime"]:
                        fields.append({"name": "animeSyncCategories", "value": cats["anime"]})

                    payload = {
                        "name": app.upper(),
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

            if "flaresolverr" in selected:
                write_log("Adding FlareSolverr proxy to Prowlarr...")
                proxy_url = f"http://localhost:{port}/api/v1/indexerproxy?apikey={p_key}"
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

            nzb_indexers = [
                {
                    "name": "Sky-Of-Usenet (Free)",
                    "implementation": "Newznab",
                    "configContract": "NewznabSettings",
                    "fields": [{"name": "baseUrl", "value": "https://skyofusenet.de"}]
                },
                {
                    "name": "NZBFinder (Free Tier)",
                    "implementation": "Newznab",
                    "configContract": "NewznabSettings",
                    "fields": [{"name": "baseUrl", "value": "https://nzbfinder.ws"}]
                },
                {
                    "name": "Tabula-Rasa (Free Tier)",
                    "implementation": "Newznab",
                    "configContract": "NewznabSettings",
                    "fields": [{"name": "baseUrl", "value": "https://www.nzb-rasa.com"}]
                }
            ]
            
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

            write_log("Auto-seeding free Usenet and torrent indexers in Prowlarr...", level="INFO")
            for indexer in indexers_to_seed:
                payload = {
                    "name": indexer["name"],
                    "enable": True,
                    "implementation": indexer["implementation"],
                    "configContract": indexer["configContract"],
                    "fields": indexer["fields"]
                }
                try:
                    rest_invoker(prowlarr_indexers_url, method="POST", json_payload=payload)
                    results.append(f"Auto-seeded indexer: {indexer['name']}")
                except Exception:
                    pass

            if os.getenv("DS_HEADLESS") != "true":
                from src.utils.logger import safe_confirm, console
                import questionary
                console.print("\n----------------------------------------------------------", style="cyan")
                console.print("             PREMIUM USENET INDEXER SETUP", style="cyan")
                console.print("----------------------------------------------------------", style="cyan")
                console.print("For automated downloading, it is highly recommended to add one premium Usenet indexer.")
                
                if safe_confirm("Would you like to configure a premium Usenet indexer now?", default=True):
                    prov = questionary.select(
                        "Select USENET Indexer to add:",
                        choices=["NZBGeek", "NinjaCentral", "AltHub", "Other Newznab"]
                    ).ask()
                    
                    if prov:
                        base_urls = {
                            "NZBGeek": "https://api.nzbgeek.info",
                            "NinjaCentral": "https://ninjacentral.co.za",
                            "AltHub": "https://althub.co.za"
                        }
                        
                        b_url = questionary.text("Enter Indexer Base URL (e.g. https://custom-index.com):").ask() if prov == "Other Newznab" else base_urls.get(prov)
                            
                        if b_url:
                            api_key = questionary.password(f"Enter your {prov} API Key:").ask()
                            if api_key and api_key.strip():
                                premium_payload = {
                                    "name": prov,
                                    "enable": True,
                                    "implementation": "Newznab",
                                    "configContract": "NewznabSettings",
                                    "fields": [
                                        {"name": "baseUrl", "value": b_url.strip()},
                                        {"name": "apiKey", "value": api_key.strip()}
                                    ]
                                }
                                try:
                                    rest_invoker(prowlarr_indexers_url, method="POST", json_payload=premium_payload)
                                    results.append(f"Successfully configured premium indexer: {prov}")
                                    console.print(f"[✓] Linked {prov} to Prowlarr", style="green")
                                except Exception as e:
                                    write_log(f"Failed to add premium indexer {prov}: {str(e)}", level="WARN")

        return results
