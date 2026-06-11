import os
import sys
import threading
import queue
import time
import socket
import platform
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path
from src.utils.logger import set_log_path, write_log
from src.utils.state import get_metadata, set_metadata
from src.utils.yaml_parser import get_yaml_content, get_registry_list
from src.utils.updater import VERSION

# Core module imports
from src.modules.preflight import run_system_preflight
from src.modules.deploy_preflight import get_port_owner
from src.modules.directories import setup_directories
from src.modules.network import setup_networks
from src.modules.compose_build import build_compose_stacks
from src.modules.deploy_start import deploy_stacks
from src.modules.auto_configure import auto_stitch_services

class DockerSetupGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Main Window Settings
        self.title(f"DockerSetup v{VERSION} - Graphical Setup Suite")
        self.geometry("1000x650")
        self.minsize(900, 600)
        
        # Determine theme based on system setting
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # State & Logger
        self.log_queue = queue.Queue()
        self.registry = []
        self.selected_services = set()
        self.env_vars = {}
        
        # Load service registry
        self.load_services_registry()
        
        # 2. Main Layout Grid (Sidebar + Main View Frame)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        # Sidebar Logo / Header
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="DockerSetup", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sub_logo = ctk.CTkLabel(self.sidebar_frame, text=f"Version {VERSION}", font=ctk.CTkFont(size=12, slant="italic"))
        self.sub_logo.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Navigation Buttons
        self.btn_welcome = ctk.CTkButton(self.sidebar_frame, text="1. Welcome", anchor="w", command=self.show_welcome_frame)
        self.btn_welcome.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_services = ctk.CTkButton(self.sidebar_frame, text="2. Services", anchor="w", command=self.show_services_frame)
        self.btn_services.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_env = ctk.CTkButton(self.sidebar_frame, text="3. Credentials", anchor="w", command=self.show_env_frame)
        self.btn_env.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_deploy = ctk.CTkButton(self.sidebar_frame, text="4. Deploy", anchor="w", command=self.show_deploy_frame)
        self.btn_deploy.grid(row=5, column=0, padx=20, pady=10, sticky="new")
        
        # Appearance Mode Selector in Sidebar bottom
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"], command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # 3. Main Display Area
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create Frame Views
        self.welcome_frame = self.create_welcome_view()
        self.services_frame = self.create_services_view()
        self.env_frame = self.create_env_view()
        self.deploy_frame = self.create_deploy_view()
        
        # Launch Welcome Frame first
        self.show_welcome_frame()
        self.run_preflight_checks()
        
        # Start background queue reader for logs
        self.after(100, self.read_log_queue)

    # Theme toggler
    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def load_services_registry(self):
        try:
            services_path = get_resource_path("services.yml")
            master_registry = get_yaml_content(services_path)
            self.registry = get_registry_list(master_registry)
        except Exception as e:
            write_log(f"GUI failed to load master registry: {str(e)}", level="ERROR")
            self.registry = []

    def select_sidebar_button(self, selected_btn):
        for btn in [self.btn_welcome, self.btn_services, self.btn_env, self.btn_deploy]:
            if btn == selected_btn:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"]) # Highlight selected
            else:
                btn.configure(fg_color="transparent")

    # ==========================================
    # VIEW SHOW/HIDE CONTROLLER
    # ==========================================
    def show_welcome_frame(self):
        self.select_sidebar_button(self.btn_welcome)
        self.hide_all_frames()
        self.welcome_frame.grid(row=0, column=0, sticky="nsew")

    def show_services_frame(self):
        self.select_sidebar_button(self.btn_services)
        self.hide_all_frames()
        self.services_frame.grid(row=0, column=0, sticky="nsew")

    def show_env_frame(self):
        self.select_sidebar_button(self.btn_env)
        self.hide_all_frames()
        # Dynamically build credentials panel based on selected checkboxes
        self.build_dynamic_env_fields()
        self.env_frame.grid(row=0, column=0, sticky="nsew")

    def show_deploy_frame(self):
        self.select_sidebar_button(self.btn_deploy)
        self.hide_all_frames()
        # Save state settings prior to showing deploy summaries
        self.save_current_selections()
        self.update_deploy_summary()
        self.deploy_frame.grid(row=0, column=0, sticky="nsew")

    def hide_all_frames(self):
        for frame in [self.welcome_frame, self.services_frame, self.env_frame, self.deploy_frame]:
            frame.grid_forget()

    # ==========================================
    # 1. WELCOME FRAME CREATION
    # ==========================================
    def create_welcome_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        
        # Welcome Title
        lbl_title = ctk.CTkLabel(frame, text="Welcome to DockerSetup", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(frame, text="This wizard will help you configure, orchestrate, and deploy a complete Media and Home Server stack on your system.", justify="left", font=ctk.CTkFont(size=14))
        lbl_desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Prerequisites Panel
        prereq_box = ctk.CTkLabel(frame, text="System Prerequisites Checks", font=ctk.CTkFont(size=16, weight="bold"))
        prereq_box.grid(row=2, column=0, pady=5, sticky="w")
        
        self.prereq_container = ctk.CTkFrame(frame, corner_radius=8)
        self.prereq_container.grid(row=3, column=0, sticky="nsew", pady=(5, 20))
        self.prereq_container.grid_columnconfigure(0, weight=1)
        
        # Target deployment folder selector
        lbl_folder_title = ctk.CTkLabel(frame, text="Deployment Directory Selection", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_folder_title.grid(row=4, column=0, pady=(10, 5), sticky="w")
        
        dir_selector_frame = ctk.CTkFrame(frame, fg_color="transparent")
        dir_selector_frame.grid(row=5, column=0, sticky="ew", pady=5)
        dir_selector_frame.grid_columnconfigure(0, weight=1)
        
        # Setup initial path
        initial_deploy = get_deploy_dir()
        self.entry_deploy_path = ctk.CTkEntry(dir_selector_frame, placeholder_text="Enter deploy directory path...")
        self.entry_deploy_path.insert(0, initial_deploy)
        self.entry_deploy_path.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        btn_browse = ctk.CTkButton(dir_selector_frame, text="Browse...", width=100, command=self.browse_deployment_directory)
        btn_browse.grid(row=0, column=1, sticky="e")
        
        # Next Button
        btn_next = ctk.CTkButton(frame, text="Next: Select Services", width=180, height=40, command=self.show_services_frame)
        btn_next.grid(row=6, column=0, pady=(20, 10), sticky="e")
        
        return frame

    def run_preflight_checks(self):
        # Displays Docker, OS and Python preflight status labels in the UI container
        for widget in self.prereq_container.winfo_children():
            widget.destroy()
            
        # 1. OS Check
        os_sys = platform.system()
        lbl_os = ctk.CTkLabel(self.prereq_container, text=f"• Host Operating System: {os_sys}", font=ctk.CTkFont(size=13))
        lbl_os.grid(row=0, column=0, padx=20, pady=8, sticky="w")
        
        # 2. Docker Check
        docker_exists = shutil.which("docker") is not None
        docker_color = "green" if docker_exists else "red"
        docker_text = "FOUND & INSTALLED" if docker_exists else "NOT FOUND (Required)"
        lbl_docker = ctk.CTkLabel(self.prereq_container, text=f"• Docker System Check: {docker_text}", text_color=docker_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_docker.grid(row=1, column=0, padx=20, pady=8, sticky="w")
        
        # 3. Docker Compose Check
        compose_text = "NOT FOUND"
        compose_exists = False
        if docker_exists:
            test_proc = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True)
            if test_proc.returncode == 0:
                compose_exists = True
                compose_text = "DOCKER COMPOSE V2 PLUG-IN INSTALLED"
        
        compose_color = "green" if compose_exists else "red"
        lbl_compose = ctk.CTkLabel(self.prereq_container, text=f"• Compose Engine Check: {compose_text}", text_color=compose_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_compose.grid(row=2, column=0, padx=20, pady=8, sticky="w")

    def browse_deployment_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.entry_deploy_path.get())
        if selected_dir:
            normalized = os.path.normpath(selected_dir)
            self.entry_deploy_path.delete(0, tk.END)
            self.entry_deploy_path.insert(0, normalized)
            os.environ["DEPLOY_DIR"] = normalized

    # ==========================================
    # 2. SERVICES FRAME CREATION
    # ==========================================
    def create_services_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        
        lbl_title = ctk.CTkLabel(frame, text="Select Stack Services", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(frame, text="Pick which media tools, database endpoints, and system management services you want to deploy in your stack.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # Scrollable container for checkboxes
        self.services_scroll = ctk.CTkScrollableFrame(frame)
        self.services_scroll.grid(row=2, column=0, sticky="nsew", pady=10)
        self.services_scroll.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.chk_vars = {}
        self.build_services_checkboxes()
        
        # Navigation
        nav_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        nav_buttons.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.show_welcome_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Configure Credentials", width=220, command=self.show_env_frame)
        btn_next.grid(row=0, column=1, sticky="e")
        
        return frame

    def build_services_checkboxes(self):
        # Categorize services based on types inside services.yml
        categories = {}
        for entry in self.registry:
            cat = entry.type.upper() if entry.type else "GENERAL"
            if cat == "NONE":
                cat = "UTILITIES"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(entry)
            
        current_row = 0
        metadata = get_metadata()
        active_selections = metadata.get("selected_services", [])
        
        # Render category headers and service checkboxes
        for cat_name, entries in sorted(categories.items()):
            lbl_cat = ctk.CTkLabel(self.services_scroll, text=cat_name, font=ctk.CTkFont(size=14, weight="bold"), text_color=["#1F6AA5", "#3B8ED0"])
            lbl_cat.grid(row=current_row, column=0, columnspan=3, pady=(15, 5), sticky="w")
            current_row += 1
            
            col_idx = 0
            for entry in entries:
                var = tk.BooleanVar(value=(entry.key in active_selections))
                self.chk_vars[entry.key] = var
                
                chk = ctk.CTkCheckBox(self.services_scroll, text=f"{entry.key} (port {entry.port})" if entry.port and entry.port != "0" else entry.key, variable=var, command=self.on_checkbox_toggle)
                chk.grid(row=current_row, column=col_idx, padx=10, pady=5, sticky="w")
                
                col_idx += 1
                if col_idx > 2:
                    col_idx = 0
                    current_row += 1
            
            if col_idx > 0:
                current_row += 1

    def on_checkbox_toggle(self):
        # Synchronize local list
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}

    # ==========================================
    # 3. CREDENTIALS / ENV VARS FRAME CREATION
    # ==========================================
    def create_env_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        
        lbl_title = ctk.CTkLabel(frame, text="Configure Environment Credentials", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(frame, text="Provide configuration settings and API keys for the selected services. Defaults will be used if left blank.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        self.env_scroll = ctk.CTkScrollableFrame(frame)
        self.env_scroll.grid(row=2, column=0, sticky="nsew", pady=10)
        self.env_scroll.grid_columnconfigure(1, weight=1)
        
        # Navigation
        nav_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        nav_buttons.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.show_services_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Deploy Stack", width=180, command=self.show_deploy_frame)
        btn_next.grid(row=0, column=1, sticky="e")
        
        return frame

    def build_dynamic_env_fields(self):
        for widget in self.env_scroll.winfo_children():
            widget.destroy()
            
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}
        self.env_entries = {}
        
        # Map out fields based on selections
        fields = [
            ("TZ", "System Timezone (e.g. America/New_York)", "America/New_York"),
            ("PUID", "Local User PID (Default: 1000)", "1000"),
            ("PGID", "Local Group GID (Default: 1000)", "1000")
        ]
        
        if "plex" in self.selected_services:
            fields.append(("PLEX_CLAIM", "Plex Claim Token (plex.tv/claim)", ""))
        if "tailscale" in self.selected_services:
            fields.append(("TS_AUTHKEY", "Tailscale Auth Key", ""))
        if "cloudflare-ddns" in self.selected_services:
            fields.append(("CF_API_TOKEN", "Cloudflare API Token", ""))
            fields.append(("CF_ZONE_ID", "Cloudflare Zone ID", ""))
            
        # Generate inputs
        row_idx = 0
        metadata = get_metadata()
        saved_env = metadata.get("env_vars", {})
        
        for key, description, default_val in fields:
            lbl = ctk.CTkLabel(self.env_scroll, text=f"{key}:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            
            val = saved_env.get(key, default_val)
            entry = ctk.CTkEntry(self.env_scroll, placeholder_text=description, width=400)
            entry.insert(0, val)
            entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
            
            self.env_entries[key] = entry
            row_idx += 1

    def save_current_selections(self):
        # Updates config metadata
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}
        
        # Read text values
        env_dict = {}
        for key, entry in self.env_entries.items():
            env_dict[key] = entry.get().strip()
            
        os.environ["DEPLOY_DIR"] = self.entry_deploy_path.get().strip()
        
        # Save to state manager
        metadata = get_metadata()
        metadata["selected_services"] = list(self.selected_services)
        metadata["env_vars"] = env_dict
        set_metadata(metadata)

    # ==========================================
    # 4. DEPLOY FRAME CREATION
    # ==========================================
    def create_deploy_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        
        lbl_title = ctk.CTkLabel(frame, text="Orchestration & Deploy", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        # Display Summaries
        self.lbl_deploy_summary = ctk.CTkLabel(frame, text="", justify="left", font=ctk.CTkFont(size=13))
        self.lbl_deploy_summary.grid(row=1, column=0, pady=(5, 10), sticky="w")
        
        # Deployment Button
        self.btn_start_deploy = ctk.CTkButton(frame, text="Deploy Stack Now", height=45, fg_color="green", hover_color="#006400", font=ctk.CTkFont(size=15, weight="bold"), command=self.trigger_deployment_pipeline)
        self.btn_start_deploy.grid(row=2, column=0, pady=10, sticky="ew")
        
        # Real-time console log
        self.log_text = tk.Text(frame, wrap="word", height=15, bg="#1e1e1e", fg="#d4d4d4", font=("Courier", 11), borderwidth=0)
        self.log_text.grid(row=3, column=0, sticky="nsew", pady=(5, 10))
        
        # Navigation
        nav_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        nav_buttons.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.show_env_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        return frame

    def update_deploy_summary(self):
        deploy_dir = get_deploy_dir()
        services_count = len(self.selected_services)
        summary_text = (
            f"• Target deployment path: {deploy_dir}\n"
            f"• Selected services to deploy ({services_count}): {', '.join(sorted(self.selected_services)) if self.selected_services else 'None Selected'}\n"
            f"• Status: Ready to generate compose files."
        )
        self.lbl_deploy_summary.configure(text=summary_text)

    # ==========================================
    # DEPLOYMENT THREAD & PIPELINE WORKER
    # ==========================================
    def log_message(self, message: str):
        self.log_queue.put(message)

    def read_log_queue(self):
        # Reads lines from background threads and writes them safely to the Tkinter text console
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, msg + "\n")
                self.log_text.see(tk.END)
                self.log_queue.task_done()
        except queue.Empty:
            pass
        self.after(100, self.read_log_queue)

    def trigger_deployment_pipeline(self):
        self.btn_start_deploy.configure(state="disabled", text="Deploying...")
        self.log_text.delete("1.0", tk.END)
        
        # Run pipeline in background worker thread to keep GUI active
        t = threading.Thread(target=self.deployment_worker)
        t.daemon = True
        t.start()

    def deployment_worker(self):
        deploy_dir = get_deploy_dir()
        
        try:
            self.log_message("[INFO] Starting deployment preflight checks...")
            # Set up logger redirect
            set_log_path(os.path.join(deploy_dir, "logs", "setup.log"))
            
            # 1. Directories setup
            self.log_message("[INFO] Setting up directories...")
            metadata = get_metadata()
            setup_directories()
            
            # 2. Write variables into target env
            self.log_message("[INFO] Writing variables to deployment environment...")
            env_vars = metadata.get("env_vars", {})
            env_path = os.path.normpath(os.path.join(deploy_dir, ".env"))
            with open(env_path, "w") as f:
                for k, v in env_vars.items():
                    f.write(f"{k}={v}\n")
                    
            # 3. Create networks
            self.log_message("[INFO] Constructing overlay network definitions...")
            setup_networks()
            
            # 4. Generate Compose stack files
            self.log_message("[INFO] Generating stack orchestration files from templates...")
            build_compose_stacks()
            
            # 5. Relaunch/Stitch logic
            self.log_message("[INFO] Executing compose starts and image downloads...")
            # We redirect standard stdout print channels to the gui log during subprocess start
            deploy_stacks()
            
            # Sync .env
            self.log_message("[INFO] Syncing environment secrets across stacks...")
            stacks_dir = os.path.join(deploy_dir, "stacks")
            if os.path.exists(stacks_dir):
                for name in os.listdir(stacks_dir):
                    fpath = os.path.join(stacks_dir, name)
                    if os.path.isdir(fpath):
                        shutil.copy(env_path, os.path.join(fpath, ".env"))
            
            # 6. Auto Config connections
            self.log_message("[INFO] Commencing auto-configure API stitching services...")
            auto_stitch_services()
            
            self.log_message("[SUCCESS] DockerSetup media stack has been successfully deployed!")
            
        except Exception as e:
            self.log_message(f"[ERROR] Deployment pipeline failed: {str(e)}")
            
        finally:
            # Re-enable button in main thread
            self.after(0, lambda: self.btn_start_deploy.configure(state="normal", text="Deploy Stack Now"))

if __name__ == "__main__":
    app = DockerSetupGUI()
    app.mainloop()
