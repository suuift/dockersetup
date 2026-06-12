import os
import sys
import json
import re
import shutil
import subprocess
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from src.gui.base_frame import BaseFrame
from src.utils.paths import get_deploy_dir, get_clean_env
from src.utils.state import get_metadata
from src.utils.clipboard import copy_to_clipboard

class SummaryFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.lbl_title = ctk.CTkLabel(self, text="Setup Summary Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        self.lbl_desc = ctk.CTkLabel(self, text="Your Media and Home Server stack is successfully deployed. Use this dashboard to manage your credentials and links.", font=ctk.CTkFont(size=13))
        self.lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # Tabview layout
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=2, column=0, sticky="nsew", pady=10)
        
        self.tab_status = self.tabview.add("Service Status")
        self.tab_widgets = self.tabview.add("Widget Setup")
        self.tab_guide = self.tabview.add("Next Steps")
        
        self.btn_exit = ctk.CTkButton(self, text="Done & Exit", width=150, height=35, command=self.controller.destroy)
        self.btn_exit.grid(row=3, column=0, pady=(10, 0), sticky="e")

    def load_tabs_data(self):
        # Dynamically refresh all tabs when screen is shown
        self.build_status_tab(self.tab_status)
        self.build_widgets_tab(self.tab_widgets)
        self.build_guide_tab(self.tab_guide)

    def build_status_tab(self, tab):
        for w in tab.winfo_children():
            w.destroy()
            
        tab.grid_columnconfigure(0, weight=1)
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        scroll.grid_columnconfigure(0, weight=2)
        scroll.grid_columnconfigure(1, weight=1)
        scroll.grid_columnconfigure(2, weight=2)
        
        from src.modules.auto_configure import test_port
        metadata = get_metadata()
        selected = metadata.get("selected_services", [])
        
        container_name_mapping = {
            "npm plus (+goaccess)": "nginx-proxy-manager-plus",
            "mariadb (+adminer)": "mariadb",
            "postgresql (+cloudbeaver)": "postgresql",
            "mongodb (+mongo-express)": "mongodb",
            "qbittorrent": "qbit",
            "qbittorrent-vpn": "qbit-vpn",
        }
        
        def get_container_info(cname: str, default_p: int) -> tuple[bool, int]:
            try:
                proc = subprocess.run(
                    ["docker", "inspect", cname],
                    capture_output=True,
                    text=True,
                    env=get_clean_env()
                )
                if proc.returncode != 0:
                    return False, default_p
                data = json.loads(proc.stdout)
                if not data or not isinstance(data, list):
                    return False, default_p
                state = data[0].get("State", {})
                is_running = state.get("Running", False)
                
                host_port = default_p
                network_settings = data[0].get("NetworkSettings", {})
                ports = network_settings.get("Ports", {})
                if ports:
                    for container_port_proto, bindings in ports.items():
                        if bindings:
                            for binding in bindings:
                                binding_port = binding.get("HostPort")
                                if binding_port and binding_port.isdigit():
                                    host_port = int(binding_port)
                                    break
                            if host_port != default_p:
                                break
                return is_running, host_port
            except Exception:
                return False, default_p
                
        lbl_header_svc = ctk.CTkLabel(scroll, text="Service Name", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_svc.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        lbl_header_status = ctk.CTkLabel(scroll, text="Status", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_status.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        lbl_header_action = ctk.CTkLabel(scroll, text="Actions", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_action.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        row_idx = 1
        for entry in self.controller.registry:
            if entry.key in selected:
                default_port = int(entry.port) if entry.port and entry.port.isdigit() else 0
                cname = container_name_mapping.get(entry.key, entry.key)
                
                is_running, port = get_container_info(cname, default_port)
                
                is_non_ui = (entry.type in ["none", "db", "postgres", "mongo", "redis"]) or (entry.key in {"flaresolverr", "hkserver", "mariadb", "postgresql", "mongodb", "redis", "db", "watchtower", "docker-prune", "crowdsec", "cloudflare-ddns", "plextraktsync", "recyclarr"})
                
                is_online = False
                if port > 0 and not is_non_ui:
                    is_online = test_port("127.0.0.1", port)
                else:
                    is_online = is_running
                    
                status_text = "ONLINE" if is_online else "OFFLINE"
                status_color = "green" if is_online else "red"
                
                lbl_name = ctk.CTkLabel(scroll, text=entry.key)
                lbl_name.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
                
                lbl_stat = ctk.CTkLabel(scroll, text=status_text, text_color=status_color, font=ctk.CTkFont(weight="bold"))
                lbl_stat.grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
                
                url = f"http://localhost:{port}" if port > 0 and not is_non_ui else ""
                if entry.key == "portainer" and url:
                    url = f"https://localhost:{port}"
                elif entry.key == "plex" and url:
                    url = f"http://localhost:{port}/web"
                
                if url:
                    action_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                    action_frame.grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")
                    
                    def open_link(u=url):
                        import webbrowser
                        webbrowser.open(u)
                        
                    def copy_link(u=url):
                        if copy_to_clipboard(u):
                            messagebox.showinfo("Clipboard", f"Copied to clipboard: {u}")
                    
                    btn_link = ctk.CTkButton(action_frame, text="Open Web UI", width=100, command=open_link)
                    btn_link.pack(side="left", padx=(0, 5))
                    
                    btn_copy = ctk.CTkButton(action_frame, text="Copy Link", width=80, fg_color="gray", hover_color="dimgray", command=copy_link)
                    btn_copy.pack(side="left")
                else:
                    lbl_nolink = ctk.CTkLabel(scroll, text="No Web Interface", font=ctk.CTkFont(slant="italic"))
                    lbl_nolink.grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")
                    
                row_idx += 1

    def build_widgets_tab(self, tab):
        for w in tab.winfo_children():
            w.destroy()
            
        tab.grid_columnconfigure(0, weight=1)
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        scroll.grid_columnconfigure(1, weight=1)
        
        metadata = get_metadata()
        selected = metadata.get("selected_services", [])
        
        manual_services = []
        if "plex" in selected:
            manual_services.append(("PLEX_TOKEN", "Plex API Token", "Open Plex -> Settings -> Web Client (General) -> 'Show Advanced' -> Scroll for Token."))
        if "jellyfin" in selected:
            manual_services.append(("JELLYFIN_KEY", "Jellyfin API Key", "Open Jellyfin -> Dashboard -> API Keys -> Create key named 'Homepage'."))
        if "portainer" in selected:
            manual_services.append(("PORTAINER_KEY", "Portainer API Token", "Open Portainer -> User Settings -> Access Tokens -> Create token."))
            
        if not manual_services:
            lbl_no = ctk.CTkLabel(scroll, text="No services require manual API tokens for widget setup.", font=ctk.CTkFont(size=14, slant="italic"))
            lbl_no.pack(pady=50)
            return
            
        lbl_info = ctk.CTkLabel(scroll, text="Paste tokens below to display rich container widgets in your Homepage dashboard.", justify="left", font=ctk.CTkFont(size=12))
        lbl_info.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="w")
        
        row_idx = 1
        entries_dict = {}
        deploy_dir = get_deploy_dir()
        env_path = os.path.join(deploy_dir, ".env")
        
        current_vars = {}
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r"^([^=]+)=(.*)$", line)
                    if match:
                        current_vars[match.group(1).strip()] = match.group(2).strip()
                        
        for var_name, name, hint in manual_services:
            lbl_name = ctk.CTkLabel(scroll, text=f"{name} ({var_name}):", font=ctk.CTkFont(weight="bold"))
            lbl_name.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            
            if var_name == "PLEX_TOKEN":
                field_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                field_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                field_frame.grid_columnconfigure(0, weight=1)
                
                entry = ctk.CTkEntry(field_frame, placeholder_text=hint)
                entry.insert(0, current_vars.get(var_name, ""))
                entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
                
                def start_plex_link(ent=entry):
                    def worker():
                        from src.utils.plex_oauth import request_plex_token
                        btn_auth.configure(state="disabled", text="Linking...")
                        token = request_plex_token(is_gui=True, progress_callback=lambda msg: self.after(0, lambda: btn_auth.configure(text=msg[:12] + "...")))
                        if token:
                            self.after(0, lambda: ent.delete(0, tk.END))
                            self.after(0, lambda: ent.insert(0, token))
                            self.after(0, lambda: btn_auth.configure(state="normal", text="Linked!"))
                        else:
                            self.after(0, lambda: btn_auth.configure(state="normal", text="Auto Auth"))
                    t = threading.Thread(target=worker)
                    t.daemon = True
                    t.start()
                    
                btn_auth = ctk.CTkButton(field_frame, text="Auto Auth", width=90, command=start_plex_link)
                btn_auth.grid(row=0, column=1, sticky="e")
                entries_dict[var_name] = entry
            else:
                entry = ctk.CTkEntry(scroll, placeholder_text=hint, width=320)
                entry.insert(0, current_vars.get(var_name, ""))
                entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                entries_dict[var_name] = entry
            row_idx += 1
            
        def save_widget_keys():
            from src.utils.state import set_env_var
            saved_count = 0
            for var_name, entry in entries_dict.items():
                val = entry.get().strip()
                if val:
                    set_env_var(var_name, val, file_path=env_path)
                    saved_count += 1
                    
            if saved_count > 0:
                messagebox.showinfo("Keys Saved", f"Successfully saved {saved_count} API tokens to .env configuration! Reloading dashboard...")
                def reload_hp():
                    try:
                        hp_path = os.path.join(deploy_dir, "stacks", "maintenance")
                        if os.path.exists(hp_path):
                            subprocess.run(["docker", "compose", "up", "-d", "--remove-orphans"], cwd=hp_path, capture_output=True, env=get_clean_env())
                    except Exception:
                        pass
                t = threading.Thread(target=reload_hp)
                t.daemon = True
                t.start()
                
        btn_save = ctk.CTkButton(scroll, text="Save & Sync Tokens", command=save_widget_keys)
        btn_save.grid(row=row_idx, column=0, columnspan=2, padx=10, pady=15)

    def build_guide_tab(self, tab):
        for w in tab.winfo_children():
            w.destroy()
            
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        scroll.grid_columnconfigure(0, weight=1)
        
        # Header banner
        header_frame = ctk.CTkFrame(scroll, fg_color=["#EAEAEA", "#252525"], corner_radius=8)
        header_frame.pack(fill="x", padx=10, pady=(5, 15))
        
        lbl_congrats = ctk.CTkLabel(
            header_frame, 
            text="🎉 Stack Deployed Successfully!", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=["#1F6AA5", "#3B8ED0"]
        )
        lbl_congrats.pack(pady=(15, 5))
        
        lbl_sub = ctk.CTkLabel(
            header_frame, 
            text="Use the links below to access your services and finish setting them up.", 
            font=ctk.CTkFont(size=13)
        )
        lbl_sub.pack(pady=(0, 15))
        
        metadata = get_metadata()
        selected = metadata.get("selected_services", [])
        
        container_name_mapping = {
            "npm plus (+goaccess)": "nginx-proxy-manager-plus",
            "mariadb (+adminer)": "mariadb",
            "postgresql (+cloudbeaver)": "postgresql",
            "mongodb (+mongo-express)": "mongodb",
            "qbittorrent": "qbit",
            "qbittorrent-vpn": "qbit-vpn",
        }
        
        def get_container_info(cname: str, default_p: int) -> tuple[bool, int]:
            try:
                proc = subprocess.run(
                    ["docker", "inspect", cname],
                    capture_output=True,
                    text=True,
                    env=get_clean_env()
                )
                if proc.returncode != 0:
                    return False, default_p
                data = json.loads(proc.stdout)
                if not data or not isinstance(data, list):
                    return False, default_p
                state = data[0].get("State", {})
                is_running = state.get("Running", False)
                
                host_port = default_p
                network_settings = data[0].get("NetworkSettings", {})
                ports = network_settings.get("Ports", {})
                if ports:
                    for container_port_proto, bindings in ports.items():
                        if bindings:
                            for binding in bindings:
                                binding_port = binding.get("HostPort")
                                if binding_port and binding_port.isdigit():
                                    host_port = int(binding_port)
                                    break
                            if host_port != default_p:
                                break
                return is_running, host_port
            except Exception:
                return False, default_p
                
        # Collect UI services
        ui_services = []
        for entry in self.controller.registry:
            if entry.key in selected:
                is_non_ui = (entry.type in ["none", "db", "postgres", "mongo", "redis"]) or (entry.key in {"watchtower", "docker-prune", "crowdsec", "cloudflare-ddns", "plextraktsync", "recyclarr", "flaresolverr", "hkserver", "mariadb", "postgresql", "mongodb"})
                if not is_non_ui:
                    default_port = int(entry.port) if entry.port and entry.port.isdigit() else 0
                    if default_port > 0:
                        cname = container_name_mapping.get(entry.key, entry.key)
                        _, live_port = get_container_info(cname, default_port)
                        ui_services.append((entry.key, live_port))
                    
        # 1. Primary Dashboards & Tools
        dash_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        dash_frame.pack(fill="x", padx=10, pady=10)
        dash_frame.grid_columnconfigure(0, weight=1)
        dash_frame.grid_columnconfigure(1, weight=1)
        
        # Homepage Card
        has_homepage = "homepage" in selected
        hp_port = 3000
        if has_homepage:
            _, hp_port = get_container_info("homepage", 3000)
            
        hp_card = ctk.CTkFrame(dash_frame, fg_color=["#F2F2F2", "#2B2B2B"], border_width=1, border_color=["#D0D0D0", "#404040"], corner_radius=8)
        hp_card.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        hp_title = ctk.CTkLabel(hp_card, text="🏠 Homepage Dashboard", font=ctk.CTkFont(size=15, weight="bold"))
        hp_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        hp_desc = ctk.CTkLabel(
            hp_card, 
            text="Access your customizable landing page showing real-time status of all services.",
            justify="left", 
            wraplength=220,
            font=ctk.CTkFont(size=12)
        )
        hp_desc.pack(anchor="w", padx=15, pady=5)
        
        hp_url = f"http://localhost:{hp_port}"
        def open_hp():
            import webbrowser
            webbrowser.open(hp_url)
            
        def copy_hp():
            if copy_to_clipboard(hp_url):
                messagebox.showinfo("Clipboard", f"Copied to clipboard: {hp_url}")
            
        btn_hp_frame = ctk.CTkFrame(hp_card, fg_color="transparent")
        btn_hp_frame.pack(anchor="w", padx=15, pady=(15, 15))
        
        btn_hp = ctk.CTkButton(btn_hp_frame, text=f"Open Dashboard (Port {hp_port})", command=open_hp, state="normal" if has_homepage else "disabled", width=160)
        btn_hp.pack(side="left", padx=(0, 5))
        
        btn_hp_copy = ctk.CTkButton(btn_hp_frame, text="Copy Link", command=copy_hp, state="normal" if has_homepage else "disabled", width=80, fg_color="gray", hover_color="dimgray")
        btn_hp_copy.pack(side="left")
        
        # Dockge Card
        has_dockge = "dockge" in selected
        dg_port = 5001
        if has_dockge:
            _, dg_port = get_container_info("dockge", 5001)
            
        dg_card = ctk.CTkFrame(dash_frame, fg_color=["#F2F2F2", "#2B2B2B"], border_width=1, border_color=["#D0D0D0", "#404040"], corner_radius=8)
        dg_card.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        
        dg_title = ctk.CTkLabel(dg_card, text="🐋 Dockge Stack Manager", font=ctk.CTkFont(size=15, weight="bold"))
        dg_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        dg_desc = ctk.CTkLabel(
            dg_card, 
            text="Manage Docker Compose stacks, edit configurations, and monitor container logs.",
            justify="left", 
            wraplength=220,
            font=ctk.CTkFont(size=12)
        )
        dg_desc.pack(anchor="w", padx=15, pady=5)
        
        dg_url = f"http://localhost:{dg_port}"
        def open_dg():
            import webbrowser
            webbrowser.open(dg_url)
            
        def copy_dg():
            if copy_to_clipboard(dg_url):
                messagebox.showinfo("Clipboard", f"Copied to clipboard: {dg_url}")
            
        btn_dg_frame = ctk.CTkFrame(dg_card, fg_color="transparent")
        btn_dg_frame.pack(anchor="w", padx=15, pady=(15, 15))
        
        btn_dg = ctk.CTkButton(btn_dg_frame, text=f"Open Dockge (Port {dg_port})", command=open_dg, state="normal" if has_dockge else "disabled", width=160)
        btn_dg.pack(side="left", padx=(0, 5))
        
        btn_dg_copy = ctk.CTkButton(btn_dg_frame, text="Copy Link", command=copy_dg, state="normal" if has_dockge else "disabled", width=80, fg_color="gray", hover_color="dimgray")
        btn_dg_copy.pack(side="left")
        
        # 2. Companion Services
        ui_services_to_show = [s for s in ui_services if s[0] not in ["homepage", "dockge"]]
        if ui_services_to_show:
            comp_lbl = ctk.CTkLabel(scroll, text="Companion Web Interfaces", font=ctk.CTkFont(size=15, weight="bold"))
            comp_lbl.pack(anchor="w", padx=10, pady=(15, 5))
            
            comp_frame = ctk.CTkFrame(scroll, fg_color=["#F8F8F8", "#202020"], corner_radius=8)
            comp_frame.pack(fill="x", padx=10, pady=5)
            
            comp_frame.grid_columnconfigure((0, 1, 2), weight=1)
            
            for index, (svc_key, svc_port) in enumerate(ui_services_to_show):
                r = index // 3
                c = index % 3
                
                svc_card = ctk.CTkFrame(comp_frame, fg_color=["#EEEEEE", "#2A2A2A"], corner_radius=6)
                svc_card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
                
                lbl_svc = ctk.CTkLabel(svc_card, text=svc_key, font=ctk.CTkFont(size=13, weight="bold"))
                lbl_svc.pack(pady=(10, 5))
                
                url = f"https://localhost:{svc_port}" if svc_key == "portainer" else f"http://localhost:{svc_port}"
                if svc_key == "plex":
                    url = f"http://localhost:{svc_port}/web"
                    
                def make_open_url(u=url):
                    import webbrowser
                    return lambda: webbrowser.open(u)
                    
                def make_copy_url(u=url):
                    return lambda: copy_to_clipboard(u) and messagebox.showinfo("Clipboard", f"Copied to clipboard: {u}")
                    
                btn_svc_frame = ctk.CTkFrame(svc_card, fg_color="transparent")
                btn_svc_frame.pack(pady=(0, 10), padx=10)
                
                btn_svc = ctk.CTkButton(btn_svc_frame, text=f"Open Port {svc_port}", height=28, command=make_open_url(url), width=110)
                btn_svc.pack(side="left", padx=(0, 5))
                
                btn_svc_copy = ctk.CTkButton(btn_svc_frame, text="Copy", height=28, command=make_copy_url(url), width=50, fg_color="gray", hover_color="dimgray")
                btn_svc_copy.pack(side="left")
                
        # 3. PlexTraktSync OAuth
        if "plextraktsync" in selected:
            pts_frame = ctk.CTkFrame(scroll, fg_color=["#F0F0F0", "#1E1E1E"], corner_radius=8, border_width=1, border_color=["#D0D0D0", "#303030"])
            pts_frame.pack(fill="x", padx=10, pady=15)
            
            pts_title = ctk.CTkLabel(pts_frame, text="🔗 PlexTraktSync OAuth Authorization Guide", font=ctk.CTkFont(size=14, weight="bold"))
            pts_title.pack(anchor="w", padx=15, pady=(12, 5))
            
            pts_desc = (
                "PlexTraktSync requires initial authorization to access your Plex and Trakt.tv accounts.\n"
                "Click the button below to spawn an interactive terminal and complete the configuration."
            )
            pts_lbl = ctk.CTkLabel(pts_frame, text=pts_desc, justify="left", font=ctk.CTkFont(size=12))
            pts_lbl.pack(anchor="w", padx=15, pady=(0, 10))
            
            def authorize_pts():
                deploy_dir = get_deploy_dir()
                media_server_dir = os.path.normpath(os.path.join(deploy_dir, "stacks", "media-server"))
                if not os.path.exists(media_server_dir):
                    messagebox.showerror("Error", f"Media server stack directory not found at {media_server_dir}")
                    return
                
                try:
                    if sys.platform == "win32":
                        cmd = f'cmd.exe /k "cd /d {media_server_dir} && docker compose run --rm plextraktsync"'
                        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    elif sys.platform == "darwin":
                        cmd = f'osascript -e \'tell application "Terminal" to do script "cd {media_server_dir} && docker compose run --rm plextraktsync"\''
                        subprocess.Popen(cmd, shell=True)
                    else:
                        terminals = ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "alacritty", "kitty", "xterm"]
                        spawned = False
                        for term in terminals:
                            if shutil.which(term):
                                if term == "gnome-terminal":
                                    subprocess.Popen(["gnome-terminal", "--working-directory", media_server_dir, "--", "docker", "compose", "run", "--rm", "plextraktsync"])
                                elif term == "xfce4-terminal":
                                    subprocess.Popen(["xfce4-terminal", "--working-directory", media_server_dir, "-e", "docker compose run --rm plextraktsync"])
                                else:
                                    subprocess.Popen([term, "-e", f"sh -c 'cd {media_server_dir} && docker compose run --rm plextraktsync'"])
                                spawned = True
                                break
                        if not spawned:
                            messagebox.showerror("Error", "Could not find a supported terminal emulator (gnome-terminal, xterm, etc.) to run the auth command.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to spawn terminal: {str(e)}")
            
            btn_auth = ctk.CTkButton(pts_frame, text="Authorize PlexTraktSync", command=authorize_pts)
            btn_auth.pack(anchor="w", padx=15, pady=(0, 15))
            
        # 4. Next Steps Checklist
        checklist_lbl = ctk.CTkLabel(scroll, text="📋 Recommended Next Steps Checklist", font=ctk.CTkFont(size=15, weight="bold"))
        checklist_lbl.pack(anchor="w", padx=10, pady=(15, 5))
        
        chk_frame = ctk.CTkFrame(scroll, fg_color=["#F2F2F2", "#2B2B2B"], corner_radius=8)
        chk_frame.pack(fill="x", padx=10, pady=5)
        
        checklist_items = [
            "1. Access Dockge to confirm all compose stacks have successfully initialized and run.",
            "2. Open Prowlarr and configure your Torrent/Usenet indexers (they will sync to Sonarr/Radarr automatically).",
            "3. Verify download clients (SABnzbd or qBittorrent) are correctly linked to your PVR tools (Sonarr, Radarr, etc.).",
            "4. Map your library folders in Sonarr and Radarr, ensuring they match the mounted media path (/tv, /movies).",
            "5. Open Homepage Dashboard to view live health status widgets for all services."
        ]
        
        for item in checklist_items:
            lbl_item = ctk.CTkLabel(chk_frame, text=item, wraplength=550, justify="left", font=ctk.CTkFont(size=12))
            lbl_item.pack(anchor="w", padx=15, pady=6)
