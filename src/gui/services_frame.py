import tkinter as tk
import customtkinter as ctk
import webbrowser
from src.gui.base_frame import BaseFrame
from src.utils.state import get_metadata
from src.apps.loader import get_apps_list

MINIMAL_KEYS = {
    "sonarr", "radarr", "lidarr", "flaresolverr", "bazarr", "prowlarr",
    "sabnzbd", "seerr", "recyclarr", "plex", "watchtower", "docker-prune",
    "tautulli", "homepage"
}

DOC_URLS = {
    "sonarr": "https://github.com/linuxserver/docker-sonarr",
    "radarr": "https://github.com/linuxserver/docker-radarr",
    "lidarr": "https://github.com/linuxserver/docker-lidarr",
    "bazarr": "https://github.com/linuxserver/docker-bazarr",
    "prowlarr": "https://github.com/linuxserver/docker-prowlarr",
    "flaresolverr": "https://github.com/FlareSolverr/FlareSolverr",
    "qbittorrent": "https://github.com/linuxserver/docker-qbittorrent",
    "sabnzbd": "https://github.com/linuxserver/docker-sabnzbd",
    "qbittorrent-vpn": "https://github.com/binhex/arch-qbittorrentvpn",
    "seerr": "https://github.com/sct/overseerr",
    "recyclarr": "https://github.com/recyclarr/recyclarr",
    "plex": "https://github.com/linuxserver/docker-plex",
    "jellyfin": "https://github.com/linuxserver/docker-jellyfin",
    "watchtower": "https://github.com/containrrr/watchtower",
    "docker-prune": "https://hub.docker.com/r/softonic/docker-system-prune",
    "homepage": "https://github.com/gethomepage/homepage",
    "portainer": "https://github.com/portainer/portainer",
    "dockge": "https://github.com/louislam/dockge",
    "tautulli": "https://github.com/linuxserver/docker-tautulli",
    "uptime": "https://github.com/louislam/uptime-kuma",
    "tailscale": "https://github.com/tailscale/tailscale",
    "cloudflare-ddns": "https://github.com/favonia/cloudflare-ddns",
    "crowdsec": "https://github.com/crowdsecurity/crowdsec",
    "cloudbeaver": "https://github.com/dbeaver/cloudbeaver",
    "mongo-express": "https://github.com/mongo-express/mongo-express",
    "kasm": "https://github.com/linuxserver/docker-kasm",
    "cloudcmd": "https://github.com/coderaiser/cloudcmd",
    "filebrowser": "https://github.com/filebrowser/filebrowser",
    "syncthing": "https://github.com/linuxserver/docker-syncthing",
    "vaultwarden": "https://github.com/dani-garcia/vaultwarden",
    "navidrome": "https://github.com/navidrome/navidrome",
    "slskd": "https://github.com/slskd/slskd",
    "mylar": "https://github.com/linuxserver/docker-mylar3",
    "readarr": "https://github.com/linuxserver/docker-readarr",
    "hkserver": "https://github.com/hkmp-team/hkmp",
    "kopia": "https://github.com/kopia/kopia",
    "authelia": "https://github.com/authelia/authelia",
    "immich": "https://github.com/immich-app/immich",
    "audiobookshelf": "https://github.com/advplyr/audiobookshelf",
    "paperless": "https://github.com/paperless-ngx/paperless-ngx",
    "scrutiny": "https://github.com/AnalogJ/scrutiny",
    "tmodloader": "https://github.com/jacobsmile/tmodloader-docker",
    "satisfactory": "https://github.com/wolveix/satisfactory-server",
    "valheim": "https://github.com/lloesche/valheim-server-docker",
    "enshrouded": "https://github.com/mornedhels/enshrouded-docker",
    "plextraktsync": "https://github.com/Taxel/PlexTraktSync",
    "mariadb (+adminer)": "https://github.com/linuxserver/docker-mariadb",
    "postgresql (+cloudbeaver)": "https://github.com/linuxserver/docker-postgres",
    "mongodb (+mongo-express)": "https://hub.docker.com/_/mongo",
    "npm plus (+goaccess)": "https://github.com/zoeyvid/nginx-proxy-manager-plus",
}

class ServicesFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        # Initialize helper track mappings
        self.chk_buttons = {}
        self.chk_frames = {}
        self.cat_headers = {}
        self.cat_to_services = {}
        self.grid_infos = {}
        self.selected_cards = {}
        
        lbl_title = ctk.CTkLabel(self, text="Select Stack Services", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="Pick which media tools, database endpoints, and system management services you want to deploy in your stack.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 5), sticky="w")
        
        # Toggle Switch for Advanced Setup
        self.switch_advanced = ctk.CTkSwitch(
            self, 
            text="Enable Advanced Custom Setup", 
            variable=self.controller.var_advanced_mode, 
            command=self.on_advanced_switch_toggle,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.switch_advanced.grid(row=2, column=0, pady=(5, 5), sticky="w")
        
        # Search Bar for available services
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=3, column=0, sticky="ew", pady=(5, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search available services...", height=30)
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_services_checklist)
        
        # Container frame for either Minimal or Advanced layouts
        self.services_container = ctk.CTkFrame(self, fg_color="transparent")
        self.services_container.grid(row=4, column=0, sticky="nsew", pady=10)
        self.services_container.grid_columnconfigure(0, weight=1)
        self.services_container.grid_rowconfigure(0, weight=1)
        
        # Navigation
        nav_buttons = ctk.CTkFrame(self, fg_color="transparent")
        nav_buttons.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.controller.show_welcome_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Configure Credentials", width=220, command=self.check_recommendations_and_proceed)
        btn_next.grid(row=0, column=1, sticky="e")

    def build_services_checkboxes(self):
        metadata = get_metadata()
        active_selections = metadata.get("selected_services", [])
        
        # Determine initial switch state if not already set manually
        if active_selections:
            is_adv = not all(k in MINIMAL_KEYS for k in active_selections)
            if is_adv and not self.controller.var_advanced_mode.get():
                self.controller.var_advanced_mode.set(True)
        else:
            active_selections = list(MINIMAL_KEYS)

        # Ensure all services have a BooleanVar initialized
        for entry in self.controller.registry:
            if entry.key not in self.controller.chk_vars:
                is_selected = entry.key in active_selections
                self.controller.chk_vars[entry.key] = tk.BooleanVar(value=is_selected)

        # Build Minimal Frame Layout once
        if not hasattr(self, "minimal_frame_layout"):
            self.minimal_frame_layout = ctk.CTkFrame(self.services_container, fg_color="transparent")
            self.minimal_frame_layout.grid_columnconfigure(0, weight=1)
            self.minimal_frame_layout.grid_rowconfigure(0, weight=1)
            
            lbl_info = ctk.CTkLabel(self.minimal_frame_layout, text="Core Minimal Services (Enabled)", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_info.pack(anchor="w", pady=(5, 10))
            
            self.minimal_scroll = ctk.CTkScrollableFrame(self.minimal_frame_layout)
            self.minimal_scroll.pack(fill="both", expand=True)
            
            for entry in self.controller.registry:
                if entry.key in MINIMAL_KEYS:
                    self.controller.chk_vars[entry.key].set(True)
                    chk = ctk.CTkCheckBox(
                        self.minimal_scroll, 
                        text=f"{entry.name} (port {entry.port})" if entry.port and entry.port != 0 else entry.name,
                        variable=self.controller.chk_vars[entry.key], 
                        state="disabled"
                    )
                    chk.pack(anchor="w", padx=20, pady=6)
                    self.chk_buttons[entry.key] = chk

        # Build Advanced Frame Layout once
        if not hasattr(self, "advanced_frame_layout"):
            self.advanced_frame_layout = ctk.CTkFrame(self.services_container, fg_color="transparent")
            self.advanced_frame_layout.grid_columnconfigure(0, weight=3)
            self.advanced_frame_layout.grid_columnconfigure(1, weight=2)
            self.advanced_frame_layout.grid_rowconfigure(0, weight=1)
            
            # Left Pane
            left_frame = ctk.CTkFrame(self.advanced_frame_layout, fg_color="transparent")
            left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
            left_frame.grid_columnconfigure(0, weight=1)
            left_frame.grid_rowconfigure(1, weight=1)
            
            lbl_left = ctk.CTkLabel(left_frame, text="Available Services Checklist", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_left.grid(row=0, column=0, pady=(5, 10), sticky="w")
            
            self.services_scroll = ctk.CTkScrollableFrame(left_frame)
            self.services_scroll.grid(row=1, column=0, sticky="nsew")
            self.services_scroll.grid_columnconfigure(0, weight=1)
            
            # Right Pane
            right_frame = ctk.CTkFrame(self.advanced_frame_layout, fg_color="transparent")
            right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            right_frame.grid_columnconfigure(0, weight=1)
            right_frame.grid_rowconfigure(1, weight=1)
            
            lbl_right = ctk.CTkLabel(right_frame, text="Active Stack Selections", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_right.grid(row=0, column=0, pady=(5, 10), sticky="w")
            
            self.selected_scroll = ctk.CTkScrollableFrame(right_frame)
            self.selected_scroll.grid(row=1, column=0, sticky="nsew")
            
            # Resolve categories (using stack_group from plugins)
            categories = {}
            for entry in self.controller.registry:
                cat = entry.stack_group.upper() if entry.stack_group else "GENERAL"
                if cat == "NONE" or not cat:
                    cat = "UTILITIES"
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(entry)

            # Render left checkboxes in a single column
            current_row = 0
            for cat_name, entries in sorted(categories.items()):
                lbl_cat = ctk.CTkLabel(self.services_scroll, text=cat_name, font=ctk.CTkFont(size=13, weight="bold"), text_color=["#1F6AA5", "#3B8ED0"])
                lbl_cat.grid(row=current_row, column=0, pady=(12, 4), sticky="w")
                
                self.cat_headers[cat_name] = lbl_cat
                self.grid_infos[cat_name] = {
                    "row": current_row,
                    "column": 0,
                    "pady": (12, 4),
                    "sticky": "w"
                }
                current_row += 1
                
                self.cat_to_services[cat_name] = []
                for entry in entries:
                    self.cat_to_services[cat_name].append(entry.key)
                    
                    item_frame = ctk.CTkFrame(self.services_scroll, fg_color="transparent")
                    item_frame.grid(row=current_row, column=0, padx=5, pady=5, sticky="w")
                    
                    self.chk_frames[entry.key] = item_frame
                    self.grid_infos[entry.key] = {
                        "row": current_row,
                        "column": 0,
                        "padx": 5,
                        "pady": 5,
                        "sticky": "w"
                    }
                    
                    chk = ctk.CTkCheckBox(
                        item_frame, 
                        text=f"{entry.name} (port {entry.port})" if entry.port and entry.port != 0 else entry.name, 
                        variable=self.controller.chk_vars[entry.key], 
                        command=self.on_checkbox_toggle
                    )
                    chk.pack(side="left", anchor="w")
                    self.chk_buttons[entry.key] = chk
                    
                    doc_url = DOC_URLS.get(entry.key.lower())
                    if doc_url:
                        btn_link = ctk.CTkLabel(
                            item_frame, 
                            text="🌐", 
                            font=ctk.CTkFont(size=13),
                            text_color=["#1F6AA5", "#3B8ED0"],
                            cursor="hand2"
                        )
                        btn_link.pack(side="left", padx=(8, 0))
                        
                        def make_open_url_cmd(url=doc_url):
                            return lambda event: webbrowser.open(url)
                        btn_link.bind("<Button-1>", make_open_url_cmd(doc_url))
                    
                    current_row += 1

        # Toggle visibility instantly
        if not self.controller.var_advanced_mode.get():
            self.advanced_frame_layout.grid_forget()
            self.minimal_frame_layout.grid(row=0, column=0, sticky="nsew")
            
            # For minimal mode, force enable only minimal keys
            for key in self.controller.chk_vars:
                if key in MINIMAL_KEYS:
                    self.controller.chk_vars[key].set(True)
                else:
                    self.controller.chk_vars[key].set(False)
        else:
            self.minimal_frame_layout.grid_forget()
            self.advanced_frame_layout.grid(row=0, column=0, sticky="nsew")

        # Apply filtering in case the search bar already has text
        self.filter_services_checklist()
        self.on_checkbox_toggle()

    def filter_services_checklist(self, event=None):
        if not hasattr(self, "cat_to_services") or not self.cat_to_services:
            return
        query = self.search_entry.get().strip().lower() if hasattr(self, "search_entry") else ""
        
        # If in Minimal Mode
        if not self.controller.var_advanced_mode.get():
            for entry in self.controller.registry:
                if entry.key in MINIMAL_KEYS:
                    if entry.key in self.chk_buttons:
                        chk = self.chk_buttons[entry.key]
                        if not query or query in entry.key.lower() or query in entry.name.lower():
                            chk.pack(anchor="w", padx=20, pady=6)
                        else:
                            chk.pack_forget()
        else:
            # If in Advanced Mode
            for cat_name, services in self.cat_to_services.items():
                matching_services = [s for s in services if not query or query in s.lower()]
                
                # Show/hide category header
                if matching_services:
                    if cat_name in self.cat_headers:
                        self.cat_headers[cat_name].grid(**self.grid_infos[cat_name])
                else:
                    if cat_name in self.cat_headers:
                        self.cat_headers[cat_name].grid_forget()
                
                # Show/hide services
                for s in services:
                    if s in self.chk_frames:
                        if not query or query in s.lower():
                            self.chk_frames[s].grid(**self.grid_infos[s])
                        else:
                            self.chk_frames[s].grid_forget()

    def on_checkbox_toggle(self):
        self.controller.selected_services = {key for key, var in self.controller.chk_vars.items() if var.get()}
        
        # Dynamically build Selected Summary if we are in Advanced Mode and self.selected_scroll exists
        if self.controller.var_advanced_mode.get() and hasattr(self, "selected_scroll") and self.selected_scroll.winfo_exists():
            if not hasattr(self, "selected_cards"):
                self.selected_cards = {}
                
            # Remove cards for services that are no longer selected
            for key in list(self.selected_cards.keys()):
                if key not in self.controller.selected_services:
                    try:
                        self.selected_cards[key].destroy()
                    except Exception:
                        pass
                    del self.selected_cards[key]
                    
            # Add cards for new selections
            for key in sorted(self.controller.selected_services):
                if key not in self.selected_cards:
                    card = ctk.CTkFrame(self.selected_scroll, fg_color=["#E5E5E5", "#2B2B2B"], height=32, corner_radius=6)
                    
                    lbl = ctk.CTkLabel(card, text=key, font=ctk.CTkFont(size=12))
                    lbl.pack(side="left", padx=10)
                    
                    def make_delete_cmd(k=key):
                        return lambda: self.uncheck_service(k)
                    
                    btn_del = ctk.CTkButton(card, text="✕", width=20, height=20, fg_color="transparent", text_color="red", hover_color=["#FFCCCC", "#552222"], command=make_delete_cmd(key))
                    btn_del.pack(side="right", padx=10)
                    
                    self.selected_cards[key] = card
            
            # Repack in sorted order to preserve correct UI sequence
            for key in sorted(self.controller.selected_services):
                if key in self.selected_cards:
                    self.selected_cards[key].pack_forget()
                    self.selected_cards[key].pack(fill="x", padx=5, pady=3)

    def uncheck_service(self, key: str):
        if key in self.controller.chk_vars:
            self.controller.chk_vars[key].set(False)
            self.on_checkbox_toggle()

    def on_advanced_switch_toggle(self):
        is_advanced = self.controller.var_advanced_mode.get()
        if not is_advanced:
            for key in list(self.controller.chk_vars.keys()):
                if key in MINIMAL_KEYS:
                    self.controller.chk_vars[key].set(True)
                else:
                    self.controller.chk_vars[key].set(False)
                    
        if hasattr(self, "search_entry"):
            self.search_entry.delete(0, tk.END)
            self.filter_services_checklist()
            
        self.build_services_checkboxes()

    def check_recommendations_and_proceed(self):
        from src.utils.dependency_resolver import check_exclusivity_conflicts, resolve_database_dependencies
        from src.utils.port_resolver import resolve_port_conflicts
        from src.utils.paths import get_deploy_dir
        import os

        # 1. Database Dependency Resolution with User Notifications
        # Map our registry list to a dict of app key -> instance
        apps_dict = {entry.key: entry for entry in self.controller.registry}
        current_keys = [key for key, var in self.controller.chk_vars.items() if var.get()]
        
        updated_keys, db_notifs = resolve_database_dependencies(current_keys, apps_dict)
        if len(updated_keys) > len(current_keys):
            # Update check box states
            for k in updated_keys:
                if k in self.controller.chk_vars:
                    self.controller.chk_vars[k].set(True)
            self.on_checkbox_toggle()
            
            # Show dependency auto-selection info pop up
            from tkinter import messagebox
            messagebox.showinfo(
                "Database Auto-Selected",
                "\n".join(db_notifs) + "\n\nYou can manually adjust these selections if desired."
            )

        # 2. Exclusivity Group Soft Warning Pop Up
        selected_app_instances = [apps_dict[k] for k in updated_keys if k in apps_dict]
        conflicts = check_exclusivity_conflicts(selected_app_instances)
        if conflicts:
            from tkinter import messagebox
            warning_msg = "Exclusivity Warnings Found:\n\n"
            for grp, app_names in conflicts.items():
                warning_msg += f"- Exclusivity Group '{grp}': {', '.join(app_names)} are all selected.\n"
            warning_msg += "\nRunning multiple services from the same exclusivity group is not recommended. Do you want to proceed anyway?"
            
            proceed = messagebox.askyesno("Exclusivity Warning", warning_msg)
            if not proceed:
                return

        # 3. Port Conflict Check & Resolution
        deploy_dir = get_deploy_dir()
        env_path = os.path.join(deploy_dir, ".env")
        port_notifs = resolve_port_conflicts(selected_app_instances, env_path)
        if port_notifs:
            from tkinter import messagebox
            messagebox.showinfo(
                "Port Collisions Resolved",
                "Some selected apps had overlapping port requirements:\n\n" + "\n".join(port_notifs) + "\n\nThese overrides have been automatically saved to your .env file."
            )

        recommendations_map = {}
        for entry in self.controller.registry:
            if entry.recommendations:
                recommendations_map[entry.key] = entry.recommendations
                
        missing_recs = []
        for svc in self.controller.selected_services:
            if svc in recommendations_map:
                for rec in recommendations_map[svc]:
                    rec = rec.strip()
                    if rec and rec not in self.controller.selected_services and rec not in missing_recs:
                        if any(e.key == rec for e in self.controller.registry):
                            missing_recs.append(rec)
                            
        if missing_recs:
            dialog = ctk.CTkToplevel(self)
            dialog.title("Recommended companion services")
            dialog.resizable(False, False)
            
            dialog_height = min(400, 220 + 32 * len(missing_recs))
            self.controller.center_over_parent(dialog, 520, dialog_height)
            dialog.transient(self)
            dialog.grab_set()
            
            lbl_title = ctk.CTkLabel(dialog, text="Select Recommended Companion Services", font=ctk.CTkFont(size=16, weight="bold"))
            lbl_title.pack(pady=(15, 5))
            
            lbl_desc = ctk.CTkLabel(
                dialog, 
                text="The following companion services are recommended based on your selections:", 
                wraplength=480, 
                font=ctk.CTkFont(size=12)
            )
            lbl_desc.pack(pady=(0, 10))
            
            scroll_frame = ctk.CTkScrollableFrame(dialog, width=440, height=min(180, 32 * len(missing_recs)))
            scroll_frame.pack(padx=20, pady=5, fill="both", expand=True)
            
            rec_vars = {}
            for rec in missing_recs:
                var = tk.BooleanVar(value=True)
                rec_vars[rec] = var
                chk = ctk.CTkCheckBox(scroll_frame, text=rec, variable=var)
                chk.pack(anchor="w", padx=20, pady=5)
                
            btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            btn_frame.pack(pady=(10, 15))
            
            def on_confirm():
                for rec, var in rec_vars.items():
                    if var.get() and rec in self.controller.chk_vars:
                        self.controller.chk_vars[rec].set(True)
                self.on_checkbox_toggle()
                dialog.destroy()
                self.controller.show_env_frame(from_next=True)
                
            def on_skip():
                dialog.destroy()
                self.controller.show_env_frame(from_next=True)
                
            def on_back():
                dialog.destroy()
                
            btn_confirm = ctk.CTkButton(btn_frame, text="Add Selected", width=120, command=on_confirm)
            btn_confirm.grid(row=0, column=0, padx=10)
            
            btn_skip = ctk.CTkButton(btn_frame, text="Skip All", width=120, fg_color="gray", hover_color="dimgray", command=on_skip)
            btn_skip.grid(row=0, column=1, padx=10)
            
            btn_back = ctk.CTkButton(btn_frame, text="Go Back", width=120, fg_color="transparent", border_width=1, command=on_back)
            btn_back.grid(row=0, column=2, padx=10)
        else:
            self.controller.show_env_frame(from_next=True)
