import os
import questionary
from src.utils.paths import get_project_root, get_resource_path
from src.utils.logger import write_log, console, write_step, safe_confirm
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list, YamlService

def select_services() -> list:
    write_step("Selecting Stack Services & Tier")
    project_root = get_project_root()
    services_path = get_resource_path("services.yml")

    metadata = get_metadata()
    if os.getenv("SKIP_SELECTION") == "true" and metadata.get("selected_services"):
        write_log("[UPGRADE] Recovered existing service selection from metadata. Skipping menu.", level="DEBUG")
        console.print("[✓] Service selections loaded from metadata", style="green")
        return metadata["selected_services"]

    master_registry = get_yaml_content(services_path)
    
    # 1. Tier selection
    choice = questionary.select(
        "Choose Stack Tier Selection Mode:",
        choices=[
            questionary.Choice("Minimal (Standard Media Stack)", value="1"),
            questionary.Choice("Advanced (Custom Selection)", value="2")
        ]
    ).ask()

    selected = []

    # 2. Add minimal services
    if "MINIMAL" in master_registry:
        write_log("Configuring MINIMAL services:", level="DEBUG")
        for svc in master_registry["MINIMAL"]:
            write_log(f" + {svc.key}", level="DEBUG")
            selected.append(svc.key)

    # 3. Custom / Advanced selections
    if choice == "2":
        categories = ["MANAGEMENT", "NETWORKING", "DATABASE", "REMOTE", "TOOLS", "GAMES"]
        for cat in categories:
            if cat in master_registry and master_registry[cat]:
                show_cat = safe_confirm(f"\nShow services in {cat}?", default=False)
                if show_cat:
                    choices = [
                        questionary.Choice(
                            title=f"{svc.key} - {svc.description}" if svc.description else svc.key,
                            value=svc.key,
                            checked=(svc.key in selected)
                        )
                        for svc in master_registry[cat]
                    ]
                    cat_selection = questionary.checkbox(
                        f"Select services in {cat}:",
                        choices=choices
                    ).ask()
                    if cat_selection:
                        for s in cat_selection:
                            if s not in selected:
                                selected.append(s)
                else:
                    write_log(f"Skipping category: {cat}", level="DEBUG")

    # 4. Dependency Mapping & Auto-Inclusion (Edge Case 11)
    db_addons = {
        "mariadb (+adminer)": "adminer",
        "postgresql (+cloudbeaver)": "cloudbeaver",
        "mongodb (+mongo-express)": "mongo-express"
    }
    for db, addon in db_addons.items():
        if db in selected and addon not in selected:
            selected.append(addon)
            write_log(f"Automatically added dependency helper application: {addon}", level="DEBUG")

    # 5. Recommendation Engine
    rec_map = {}
    if "RECOMMENDATIONS" in master_registry:
        for item in master_registry["RECOMMENDATIONS"]:
            rec_map[item.source] = item.recommendations

    suggested = []
    # Only suggest companion recommendations if custom/advanced setup mode (Tier 2) is chosen
    if choice == "2":
        for s in selected:
            if s in rec_map:
                for rec in rec_map[s]:
                    if rec not in selected and rec not in suggested and rec.strip():
                        suggested.append(rec)
    
    if suggested:
        console.print("\n--- Recommended Add-ons ---", style="yellow")
        console.print("Based on your selections, we recommend adding these services:", style="grey50")
        
        rec_choices = [
            questionary.Choice(title=f"Add {rec}?", value=rec, checked=True)
            for rec in suggested
        ]
        
        confirmed_recs = questionary.checkbox(
            "Select recommended add-ons to enable:",
            choices=rec_choices
        ).ask()
        
        if confirmed_recs:
            for rec in confirmed_recs:
                if rec not in selected:
                    selected.append(rec)
                    write_log(f"Added recommended service: {rec}", level="DEBUG")

    # Update metadata
    metadata["selected_services"] = selected
    metadata["tier"] = choice
    set_metadata(metadata)
    write_log("Selection and Tier saved to metadata.", level="DEBUG")
    console.print("[✓] Service selection saved", style="green")
    
    return selected
