import os
import sys

# Prevent darkdetect from executing blocking subprocess calls on Linux
if sys.platform.startswith("linux"):
    try:
        import darkdetect
        darkdetect.theme = lambda: "Dark"
    except Exception:
        pass

import threading
import queue
import time
import socket
import platform
import subprocess
import shutil
import re
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

# Monkey-patch CTkScrollableFrame.check_if_master_is_canvas to prevent AttributeError: 'str' object has no attribute 'master'
try:
    original_check = ctk.CTkScrollableFrame.check_if_master_is_canvas
    def patched_check(self, widget):
        if isinstance(widget, str):
            try:
                widget = self.nametowidget(widget)
            except Exception:
                return False
        try:
            return original_check(self, widget)
        except Exception:
            return False
    ctk.CTkScrollableFrame.check_if_master_is_canvas = patched_check
except Exception:
    pass

from src.utils.paths import get_project_root, get_deploy_dir, get_resource_path, get_clean_env
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
from src.modules.env_wizard import COMMON_ZONES, detect_timezone, new_random_password
import tkinter.ttk as ttk

class DockerSetupGUI(ctk.CTk):
    def get_linux_dpi_scale(self) -> float:
        try:
            tk_scale = self.tk.call('tk', 'scaling')
            return tk_scale / 1.33333333
        except Exception:
            return 1.0

    def __init__(self):
        super().__init__()

        # Hide terminal console window at startup on Windows only if we own the console process
        if sys.platform == "win32":
            try:
                import ctypes
                hwnd = ctypes.windll.kernel32.GetConsoleWindow()
                if hwnd != 0:
                    pid = ctypes.wintypes.DWORD()
                    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if pid.value == os.getpid():
                        ctypes.windll.user32.ShowWindow(hwnd, 0) # SW_HIDE = 0
            except Exception:
                pass

        # 1. Main Window Settings
        self.title(f"DockerSetup v{VERSION} - Graphical Setup Suite")
        self.geometry("1000x650")
        self.minsize(900, 600)
        
        # Determine theme based on system setting
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Detect and apply platform DPI auto-scaling for Linux
        if sys.platform.startswith("linux"):
            try:
                scale = self.get_linux_dpi_scale()
                ctk.set_widget_scaling(scale)
                ctk.set_window_scaling(scale)
            except Exception:
                pass

        # Force Headless execution mode for background modules to bypass interactive questionary prompts
        os.environ["DS_HEADLESS"] = "true"
        
        # State & Logger
        self.log_queue = queue.Queue()
        from src.utils.logger import set_gui_log_callback
        set_gui_log_callback(self.log_message)
        
        self.registry = []
        self.selected_services = set()
        self.env_vars = {}
        
        # Navigation Locks State
        self.max_completed_step = 1

        # Load service registry
        self.load_services_registry()
        
        # 2. Main Layout Grid (Sidebar + Main View Frame)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
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
        
        self.btn_logs = ctk.CTkButton(self.sidebar_frame, text="5. View Logs", anchor="w", command=self.show_logs_frame)
        self.btn_logs.grid(row=6, column=0, padx=20, pady=10, sticky="new")
        
        # Appearance Mode Selector in Sidebar bottom
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"], command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 5), sticky="ew")
        
        # UI Scaling Selector
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(5, 0), sticky="w")
        self.scaling_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["80%", "90%", "100%", "110%", "120%", "150%", "180%", "200%"],
            command=self.change_scaling_event
        )
        self.scaling_optionmenu.grid(row=10, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # Sync scaling menu selection with active scale
        try:
            current_scale_pct = f"{int(ctk.get_widget_scaling() * 100)}%"
            self.scaling_optionmenu.set(current_scale_pct)
        except Exception:
            self.scaling_optionmenu.set("100%")
        
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
        self.logs_view_frame = self.create_logs_view()
        
        # Initialize default log path on startup
        initial_deploy = get_deploy_dir()
        set_log_path(os.path.join(initial_deploy, "logs"))
        
        # Initialize Sidebar button states
        self.update_navigation_buttons()
        
        # Launch Welcome Frame first
        self.show_welcome_frame()
        self.run_preflight_checks()
        
        # Start background queue reader for logs
        self.after(100, self.read_log_queue)

    # Theme toggler
    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    # UI scaling handler
    def change_scaling_event(self, new_scaling: str):
        try:
            scale_val = int(new_scaling.replace("%", "")) / 100
            ctk.set_widget_scaling(scale_val)
            ctk.set_window_scaling(scale_val)
        except Exception:
            pass

    # Sidebar state manager
    def update_navigation_buttons(self):
        self.btn_welcome.configure(state="normal")
        self.btn_services.configure(state="normal" if self.max_completed_step >= 2 else "disabled")
        self.btn_env.configure(state="normal" if self.max_completed_step >= 3 else "disabled")
        self.btn_deploy.configure(state="normal" if self.max_completed_step >= 4 else "disabled")
        if hasattr(self, "btn_logs"):
            self.btn_logs.configure(state="normal" if self.max_completed_step >= 5 else "disabled")

    # Generic window centering helper
    def center_over_parent(self, dialog, width: int, height: int):
        self.update_idletasks()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()
        parent_x = self.winfo_x()
        parent_y = self.winfo_y()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        dialog.transient(self)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        dialog.deiconify()
        dialog.update_idletasks()
        try:
            dialog.grab_set()
        except Exception:
            pass

    def load_services_registry(self):
        try:
            services_path = get_resource_path("services.yml")
            self.master_registry = get_yaml_content(services_path)
            self.registry = get_registry_list(self.master_registry)
        except Exception as e:
            write_log(f"GUI failed to load master registry: {str(e)}", level="ERROR")
            self.registry = []
            self.master_registry = {}

    def select_sidebar_button(self, selected_btn):
        for btn in [self.btn_welcome, self.btn_services, self.btn_env, self.btn_deploy, getattr(self, "btn_logs", None)]:
            if btn:
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

    def show_services_frame(self, from_next=False):
        if from_next:
            self.max_completed_step = max(self.max_completed_step, 2)
        if self.max_completed_step < 2:
            return
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_services)
        self.hide_all_frames()
        self.services_frame.grid(row=0, column=0, sticky="nsew")

    def show_env_frame(self, from_next=False):
        if from_next:
            self.max_completed_step = max(self.max_completed_step, 3)
        if self.max_completed_step < 3:
            return
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_env)
        self.hide_all_frames()
        # Dynamically build credentials panel based on selected checkboxes
        self.build_dynamic_env_fields()
        self.env_frame.grid(row=0, column=0, sticky="nsew")

    def show_deploy_frame(self, from_next=False):
        if from_next:
            self.max_completed_step = max(self.max_completed_step, 4)
        if self.max_completed_step < 4:
            return
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_deploy)
        self.hide_all_frames()
        # Save state settings prior to showing deploy summaries
        self.save_current_selections()
        self.update_deploy_summary()
        self.deploy_frame.grid(row=0, column=0, sticky="nsew")

    def show_logs_frame(self, from_next=False):
        if from_next:
            self.max_completed_step = max(self.max_completed_step, 5)
        if self.max_completed_step < 5:
            return
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_logs)
        self.hide_all_frames()
        self.update_logs_view_content()
        self.logs_view_frame.grid(row=0, column=0, sticky="nsew")

    def hide_all_frames(self):
        for frame in [self.welcome_frame, self.services_frame, self.env_frame, self.deploy_frame, getattr(self, "logs_view_frame", None), getattr(self, "summary_view_frame", None)]:
            if frame:
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
        btn_next = ctk.CTkButton(frame, text="Next: Select Services", width=180, height=40, command=self.validate_directory_and_proceed)
        btn_next.grid(row=6, column=0, pady=(20, 10), sticky="e")
        
        return frame

    def validate_directory_and_proceed(self):
        d_dir = self.entry_deploy_path.get().strip()
        if not d_dir:
            return
            
        d_dir = os.path.normpath(d_dir)
        os.environ["DEPLOY_DIR"] = d_dir
        set_log_path(os.path.join(d_dir, "logs"))
        
        # 1. Handle directory creation
        if not os.path.exists(d_dir):
            from tkinter import messagebox
            create = messagebox.askyesno("Create Directory?", f"Directory '{d_dir}' does not exist. Create it?")
            if create:
                try:
                    os.makedirs(d_dir, exist_ok=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create directory: {str(e)}")
                    return
            else:
                return
                
        # 2. Check for existing deployment
        metadata_file = os.path.join(d_dir, ".metadata.json")
        if os.path.exists(metadata_file):
            # Show existing deployment menu
            dialog = ctk.CTkToplevel(self)
            dialog.title("Existing Deployment Detected")
            dialog.resizable(False, False)
            self.center_over_parent(dialog, 500, 320)
            
            lbl_title = ctk.CTkLabel(dialog, text="Existing Deployment Found", font=ctk.CTkFont(size=18, weight="bold"))
            lbl_title.pack(pady=(20, 10))
            
            msg = (
                f"An existing DockerSetup stack was found at:\n{d_dir}\n\n"
                f"What would you like to do?"
            )
            lbl_msg = ctk.CTkLabel(dialog, text=msg, wraplength=450, justify="center", font=ctk.CTkFont(size=13))
            lbl_msg.pack(pady=10)
            
            def on_modify():
                dialog.destroy()
                # Reload metadata so checkbox selections are loaded properly
                self.build_services_checkboxes()
                self.show_services_frame(from_next=True)
                
            def on_upgrade():
                dialog.destroy()
                self.run_fast_upgrade(d_dir)
                
            def on_reset():
                dialog.destroy()
                self.run_full_reset(d_dir)
                
            def on_cancel():
                dialog.destroy()
                
            btn_modify = ctk.CTkButton(dialog, text="Modify Selections (Re-run Wizard)", width=320, command=on_modify)
            btn_modify.pack(pady=5)
            
            btn_upgrade = ctk.CTkButton(dialog, text="Fast Upgrade (Apply Template Updates)", width=320, command=on_upgrade)
            btn_upgrade.pack(pady=5)
            
            btn_reset = ctk.CTkButton(dialog, text="Full Reset (Wipe All Configs & Volumes)", fg_color="red", hover_color="#8B0000", width=320, command=on_reset)
            btn_reset.pack(pady=5)
            
            btn_cancel = ctk.CTkButton(dialog, text="Change Directory / Cancel", fg_color="transparent", border_width=1, width=320, command=on_cancel)
            btn_cancel.pack(pady=(5, 20))
        else:
            # New deployment, proceed to selections
            self.show_services_frame(from_next=True)

    def run_fast_upgrade(self, d_dir):
        # We can switch directly to the deploy frame, populate it, and trigger the deployment pipeline
        self.show_deploy_frame(from_next=True)
        self.log_text.delete("1.0", tk.END)
        self.log_message("[INFO] Starting fast template upgrade...")
        self.trigger_deployment_pipeline()
        
    def run_full_reset(self, d_dir):
        from tkinter import messagebox
        confirm = messagebox.askyesno(
            "Permanent Wipe Warning", 
            "Are you sure you want to permanently wipe all containers, volumes, and configurations in this directory?\n\nThis action cannot be undone."
        )
        if not confirm:
            return
            
        # Run reset in background showing the log console
        self.show_deploy_frame(from_next=True)
        self.log_text.delete("1.0", tk.END)
        self.btn_start_deploy.configure(state="disabled")
        
        def reset_worker():
            try:
                self.log_message("[INFO] Commencing full system reset...")
                stacks_dir = os.path.join(d_dir, "stacks")
                if os.path.exists(stacks_dir):
                    for stack in os.listdir(stacks_dir):
                        full_path = os.path.join(stacks_dir, stack)
                        if os.path.isdir(full_path):
                            compose_file = os.path.join(full_path, "docker-compose.yml")
                            if os.path.exists(compose_file):
                                self.log_message(f"[INFO] Tearing down stack: {stack}...")
                                subprocess.run(["docker", "compose", "down", "-v", "--remove-orphans"], cwd=full_path, capture_output=True, env=get_clean_env())
                                
                self.log_message("[INFO] Removing stack and configuration directories...")
                shutil.rmtree(stacks_dir, ignore_errors=True)
                shutil.rmtree(os.path.join(d_dir, "appdata"), ignore_errors=True)
                
                # Back up metadata and env files
                for file in [".metadata.json", ".env"]:
                    file_p = os.path.join(d_dir, file)
                    if os.path.exists(file_p):
                        try:
                            shutil.copy2(file_p, file_p + ".bak")
                            self.log_message(f"[INFO] Created backup: {file}.bak")
                            os.remove(file_p)
                        except Exception:
                            pass
                
                # Clear state
                import src.utils.state as state
                state._metadata_cache = {}
                
                self.log_message("[SUCCESS] Reset complete. All containers and settings have been wiped!")
                messagebox.showinfo("Reset Complete", "All configurations, volumes, and containers have been wiped cleanly.")
                
                # Relaunch Welcome
                self.after(0, lambda: self.show_welcome_frame())
            except Exception as e:
                self.log_message(f"[ERROR] Reset failed: {str(e)}")
            finally:
                self.after(0, lambda: self.btn_start_deploy.configure(state="normal"))
                
        t = threading.Thread(target=reset_worker)
        t.daemon = True
        t.start()

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
            set_log_path(os.path.join(normalized, "logs"))

    # ==========================================
    # 2. SERVICES FRAME CREATION
    # ==========================================
    def create_services_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        
        lbl_title = ctk.CTkLabel(frame, text="Select Stack Services", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(frame, text="Pick which media tools, database endpoints, and system management services you want to deploy in your stack.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 5), sticky="w")
        
        # Toggle Switch for Advanced Setup
        self.var_advanced_mode = tk.BooleanVar(value=False)
        self.switch_advanced = ctk.CTkSwitch(
            frame, 
            text="Enable Advanced Custom Setup", 
            variable=self.var_advanced_mode, 
            command=self.on_advanced_switch_toggle,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.switch_advanced.grid(row=2, column=0, pady=(5, 5), sticky="w")
        
        # Container frame for either Minimal or Advanced layouts
        self.services_container = ctk.CTkFrame(frame, fg_color="transparent")
        self.services_container.grid(row=3, column=0, sticky="nsew", pady=10)
        self.services_container.grid_columnconfigure(0, weight=1)
        self.services_container.grid_rowconfigure(0, weight=1)
        
        self.chk_vars = {}
        self.chk_buttons = {}
        self.build_services_checkboxes()
        
        # Navigation
        nav_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        nav_buttons.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.show_welcome_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Configure Credentials", width=220, command=self.check_recommendations_and_proceed)
        btn_next.grid(row=0, column=1, sticky="e")
        
        return frame

    def on_advanced_switch_toggle(self):
        is_advanced = self.var_advanced_mode.get()
        minimal_keys = []
        if hasattr(self, "master_registry") and "MINIMAL" in self.master_registry:
            minimal_keys = [svc.key for svc in self.master_registry["MINIMAL"]]
            
        # If toggling back to minimal, reset selections to minimal keys
        if not is_advanced:
            for key in list(self.chk_vars.keys()):
                if key in minimal_keys:
                    self.chk_vars[key].set(True)
                else:
                    self.chk_vars[key].set(False)
                    
        self.build_services_checkboxes()

    def build_services_checkboxes(self):
        # Clear container
        for widget in self.services_container.winfo_children():
            try:
                widget.destroy()
            except Exception:
                pass
                
        # Resolve categories
        categories = {}
        for entry in self.registry:
            cat = entry.type.upper() if entry.type else "GENERAL"
            if cat == "NONE":
                cat = "UTILITIES"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(entry)
            
        metadata = get_metadata()
        active_selections = metadata.get("selected_services", [])
        
        # Resolve minimal keys
        minimal_keys = []
        if hasattr(self, "master_registry") and "MINIMAL" in self.master_registry:
            minimal_keys = [svc.key for svc in self.master_registry["MINIMAL"]]
            
        # Determine initial switch state if not already set manually
        if active_selections:
            is_adv = not all(k in minimal_keys for k in active_selections)
            if is_adv and not self.var_advanced_mode.get():
                self.var_advanced_mode.set(True)
        else:
            active_selections = minimal_keys

        # Ensure all services have a BooleanVar initialized
        for entry in self.registry:
            if entry.key not in self.chk_vars:
                is_selected = entry.key in active_selections
                self.chk_vars[entry.key] = tk.BooleanVar(value=is_selected)

        # 1. MINIMAL MODE
        if not self.var_advanced_mode.get():
            self.services_container.grid_columnconfigure(0, weight=1)
            self.services_container.grid_columnconfigure(1, weight=0)
            
            lbl_info = ctk.CTkLabel(self.services_container, text="Core Minimal Services (Enabled)", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_info.pack(anchor="w", pady=(5, 10))
            
            self.minimal_scroll = ctk.CTkScrollableFrame(self.services_container)
            self.minimal_scroll.pack(fill="both", expand=True)
            
            for entry in self.registry:
                if entry.key in minimal_keys:
                    self.chk_vars[entry.key].set(True)
                    chk = ctk.CTkCheckBox(
                        self.minimal_scroll, 
                        text=f"{entry.key} (port {entry.port})" if entry.port and entry.port != "0" else entry.key,
                        variable=self.chk_vars[entry.key], 
                        state="disabled"
                    )
                    chk.pack(anchor="w", padx=20, pady=6)
                    self.chk_buttons[entry.key] = chk
            self.on_checkbox_toggle()
            
        # 2. ADVANCED MODE (DUAL-PANE LAYOUT)
        else:
            self.services_container.grid_columnconfigure(0, weight=3)
            self.services_container.grid_columnconfigure(1, weight=2)
            
            # Left Pane
            left_frame = ctk.CTkFrame(self.services_container, fg_color="transparent")
            left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
            left_frame.grid_columnconfigure(0, weight=1)
            left_frame.grid_rowconfigure(1, weight=1)
            
            lbl_left = ctk.CTkLabel(left_frame, text="Available Services Checklist", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_left.grid(row=0, column=0, pady=(5, 10), sticky="w")
            
            self.services_scroll = ctk.CTkScrollableFrame(left_frame)
            self.services_scroll.grid(row=1, column=0, sticky="nsew")
            self.services_scroll.grid_columnconfigure(0, weight=1)
            
            # Right Pane
            right_frame = ctk.CTkFrame(self.services_container, fg_color="transparent")
            right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            right_frame.grid_columnconfigure(0, weight=1)
            right_frame.grid_rowconfigure(1, weight=1)
            
            lbl_right = ctk.CTkLabel(right_frame, text="Active Stack Selections", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_right.grid(row=0, column=0, pady=(5, 10), sticky="w")
            
            self.selected_scroll = ctk.CTkScrollableFrame(right_frame)
            self.selected_scroll.grid(row=1, column=0, sticky="nsew")
            
            # Render left checkboxes in a single column to prevent horizontal truncation
            current_row = 0
            for cat_name, entries in sorted(categories.items()):
                lbl_cat = ctk.CTkLabel(self.services_scroll, text=cat_name, font=ctk.CTkFont(size=13, weight="bold"), text_color=["#1F6AA5", "#3B8ED0"])
                lbl_cat.grid(row=current_row, column=0, pady=(12, 4), sticky="w")
                current_row += 1
                
                for entry in entries:
                    chk = ctk.CTkCheckBox(
                        self.services_scroll, 
                        text=f"{entry.key} (port {entry.port})" if entry.port and entry.port != "0" else entry.key, 
                        variable=self.chk_vars[entry.key], 
                        command=self.on_checkbox_toggle
                    )
                    chk.grid(row=current_row, column=0, padx=5, pady=5, sticky="w")
                    self.chk_buttons[entry.key] = chk
                    current_row += 1
            self.on_checkbox_toggle()

    def uncheck_service(self, key: str):
        if key in self.chk_vars:
            self.chk_vars[key].set(False)
            self.on_checkbox_toggle()

    def check_recommendations_and_proceed(self):
        recommendations_map = {}
        if hasattr(self, "master_registry") and "RECOMMENDATIONS" in self.master_registry:
            for item in self.master_registry["RECOMMENDATIONS"]:
                recommendations_map[item.source] = item.recommendations
                
        missing_recs = []
        for svc in self.selected_services:
            if svc in recommendations_map:
                for rec in recommendations_map[svc]:
                    rec = rec.strip()
                    if rec and rec not in self.selected_services and rec not in missing_recs:
                        if any(e.key == rec for e in self.registry):
                            missing_recs.append(rec)
                            
        if missing_recs:
            dialog = ctk.CTkToplevel(self)
            dialog.title("Complete Your Stack Add-ons")
            dialog.resizable(False, False)
            self.center_over_parent(dialog, 500, 250)
            
            lbl_title = ctk.CTkLabel(dialog, text="Complete Your Stack?", font=ctk.CTkFont(size=18, weight="bold"))
            lbl_title.pack(pady=(20, 10))
            
            msg = (
                f"Based on your selections, we recommend adding the following companion services:\n\n"
                f"{', '.join(missing_recs)}\n\n"
                f"Would you like to automatically enable these recommended services?"
            )
            lbl_msg = ctk.CTkLabel(dialog, text=msg, wraplength=450, justify="center", font=ctk.CTkFont(size=13))
            lbl_msg.pack(pady=10)
            
            btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            btn_frame.pack(pady=(20, 10))
            
            def on_yes():
                for rec in missing_recs:
                    if rec in self.chk_vars:
                        self.chk_vars[rec].set(True)
                self.on_checkbox_toggle()
                dialog.destroy()
                self.show_env_frame(from_next=True)
                
            def on_no():
                dialog.destroy()
                self.show_env_frame(from_next=True)
                
            def on_cancel():
                dialog.destroy()
                
            btn_yes = ctk.CTkButton(btn_frame, text="Yes, Enable All", width=120, command=on_yes)
            btn_yes.grid(row=0, column=0, padx=10)
            
            btn_no = ctk.CTkButton(btn_frame, text="No, Skip", width=120, fg_color="gray", hover_color="dimgray", command=on_no)
            btn_no.grid(row=0, column=1, padx=10)
            
            btn_cancel = ctk.CTkButton(btn_frame, text="Go Back", width=120, fg_color="transparent", border_width=1, command=on_cancel)
            btn_cancel.grid(row=0, column=2, padx=10)
            
        else:
            self.show_env_frame(from_next=True)

    def on_checkbox_toggle(self):
        # Synchronize local list
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}
        
        # Dynamically build Selected Summary if we are in Advanced Mode and self.selected_scroll exists
        if self.var_advanced_mode.get() and hasattr(self, "selected_scroll") and self.selected_scroll.winfo_exists():
            for widget in self.selected_scroll.winfo_children():
                try:
                    widget.destroy()
                except Exception:
                    pass
            
            for key in sorted(self.selected_services):
                card = ctk.CTkFrame(self.selected_scroll, fg_color=["#E5E5E5", "#2B2B2B"], height=32, corner_radius=6)
                card.pack(fill="x", padx=5, pady=3)
                
                lbl = ctk.CTkLabel(card, text=key, font=ctk.CTkFont(size=12))
                lbl.pack(side="left", padx=10)
                
                def make_delete_cmd(k=key):
                    return lambda: self.uncheck_service(k)
                
                btn_del = ctk.CTkButton(card, text="✕", width=20, height=20, fg_color="transparent", text_color="red", hover_color=["#FFCCCC", "#552222"], command=make_delete_cmd(key))
                btn_del.pack(side="right", padx=10)

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
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Deploy Stack", width=180, command=lambda: self.show_deploy_frame(from_next=True))
        btn_next.grid(row=0, column=1, sticky="e")
        
        return frame

    def build_dynamic_env_fields(self):
        for widget in self.env_scroll.winfo_children():
            widget.destroy()
            
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}
        self.env_entries = {}
        
        metadata = get_metadata()
        saved_env = metadata.get("env_vars", {})
        
        import platform
        detected_tz = detect_timezone()
        default_tz = saved_env.get("TZ", detected_tz)
        default_puid = saved_env.get("PUID", os.environ.get("SUDO_UID", "1000"))
        default_pgid = saved_env.get("PGID", os.environ.get("SUDO_GID", "1000"))
        default_media = saved_env.get("DATADRIVE", "D:/Media" if platform.system() == "Windows" else os.path.expanduser("~/media"))
        
        row_idx = 0
        
        def add_standard_row(key, description, default_val):
            nonlocal row_idx
            lbl = ctk.CTkLabel(self.env_scroll, text=f"{key}:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            
            val = saved_env.get(key, default_val)
            entry = ctk.CTkEntry(self.env_scroll, placeholder_text=description, width=400)
            entry.insert(0, val)
            entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
            
            self.env_entries[key] = entry
            row_idx += 1
            
        # Timezone Combobox
        lbl_tz = ctk.CTkLabel(self.env_scroll, text="TZ (Timezone):", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_tz.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        
        cb_tz = ttk.Combobox(self.env_scroll, values=COMMON_ZONES, width=37, state="readonly")
        cb_tz.set(default_tz)
        cb_tz.grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        self.env_entries["TZ"] = cb_tz
        row_idx += 1
        
        # PUID & PGID
        add_standard_row("PUID", "Local User PID (Default: 1000)", default_puid)
        add_standard_row("PGID", "Local Group GID (Default: 1000)", default_pgid)
        
        # HTTP_USERNAME & HTTP_PASSWORD
        add_standard_row("HTTP_USERNAME", "Management Username (Default: admin)", "admin")
        
        lbl_pass = ctk.CTkLabel(self.env_scroll, text="HTTP_PASSWORD:", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_pass.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        
        pass_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
        pass_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        
        entry_pass = ctk.CTkEntry(pass_frame, placeholder_text="Management Password (leave blank to generate)", show="*", width=250)
        entry_pass.insert(0, saved_env.get("HTTP_PASSWORD", ""))
        entry_pass.grid(row=0, column=0, sticky="ew")
        
        def toggle_pass():
            if entry_pass.cget("show") == "*":
                entry_pass.configure(show="")
                btn_toggle.configure(text="Hide")
            else:
                entry_pass.configure(show="*")
                btn_toggle.configure(text="Show")
                
        btn_toggle = ctk.CTkButton(pass_frame, text="Show", width=60, command=toggle_pass)
        btn_toggle.grid(row=0, column=1, padx=(10, 0))
        
        def generate_rand():
            entry_pass.delete(0, tk.END)
            entry_pass.insert(0, new_random_password())
            
        btn_random = ctk.CTkButton(pass_frame, text="Random", width=70, command=generate_rand)
        btn_random.grid(row=0, column=2, padx=(10, 0))
        
        self.env_entries["HTTP_PASSWORD"] = entry_pass
        row_idx += 1
        
        # DATADRIVE (Media folder directory) with Browse button
        lbl_media = ctk.CTkLabel(self.env_scroll, text="DATADRIVE (Media Folder):", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_media.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        
        media_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
        media_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        
        entry_media = ctk.CTkEntry(media_frame, placeholder_text="Media folder directory path", width=330)
        entry_media.insert(0, default_media)
        entry_media.grid(row=0, column=0, sticky="ew")
        
        def browse_media():
            folder = filedialog.askdirectory(initialdir=entry_media.get())
            if folder:
                entry_media.delete(0, tk.END)
                entry_media.insert(0, os.path.normpath(folder))
                
        btn_browse = ctk.CTkButton(media_frame, text="Browse...", width=60, command=browse_media)
        btn_browse.grid(row=0, column=1, padx=(10, 0))
        
        self.env_entries["DATADRIVE"] = entry_media
        row_idx += 1
        
        if "plex" in self.selected_services:
            lbl_plex = ctk.CTkLabel(self.env_scroll, text="PLEX_CLAIM:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl_plex.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            
            plex_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
            plex_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
            
            val = saved_env.get("PLEX_CLAIM", "")
            entry_plex = ctk.CTkEntry(plex_frame, placeholder_text="Plex Claim Token (plex.tv/claim)", width=250)
            entry_plex.insert(0, val)
            entry_plex.grid(row=0, column=0, sticky="ew")
            
            def open_plex_claim():
                import webbrowser
                try:
                    webbrowser.open("https://plex.tv/claim")
                except Exception:
                    pass
                    
            btn_plex = ctk.CTkButton(plex_frame, text="Get Token", width=70, command=open_plex_claim)
            btn_plex.grid(row=0, column=1, padx=(10, 0))
            
            self.env_entries["PLEX_CLAIM"] = entry_plex
            row_idx += 1
            
        if "tailscale" in self.selected_services:
            add_standard_row("TS_AUTHKEY", "Tailscale Auth Key", "")
            
        if "cloudflare-ddns" in self.selected_services:
            add_standard_row("CF_API_TOKEN", "Cloudflare API Token", "")
            add_standard_row("CF_ZONE_ID", "Cloudflare Zone ID", "")
            add_standard_row("CF_DOMAINS", "Cloudflare Domains (comma-separated)", "")
            
        if "cloudflare-ddns" in self.selected_services or "npm plus (+goaccess)" in self.selected_services:
            add_standard_row("BASE_DOMAIN", "Base Domain (e.g. example.com)", "local.host")
            
        if "qbittorrent-vpn" in self.selected_services:
            add_standard_row("VPN_PROV", "VPN Provider (e.g. custom, mullvad, pia)", "custom")
            add_standard_row("VPN_CLIENT", "VPN Client (e.g. wireguard, openvpn)", "wireguard")
            add_standard_row("VPN_USER", "VPN Username (leave blank if not required)", "")
            
            lbl_vpn_pass = ctk.CTkLabel(self.env_scroll, text="VPN_PASS:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl_vpn_pass.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            
            vpn_pass_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
            vpn_pass_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
            
            entry_vpn_pass = ctk.CTkEntry(vpn_pass_frame, placeholder_text="VPN Password", show="*", width=330)
            entry_vpn_pass.insert(0, saved_env.get("VPN_PASS", ""))
            entry_vpn_pass.grid(row=0, column=0, sticky="ew")
            
            def toggle_vpn_pass():
                if entry_vpn_pass.cget("show") == "*":
                    entry_vpn_pass.configure(show="")
                    btn_vpn_toggle.configure(text="Hide")
                else:
                    entry_vpn_pass.configure(show="*")
                    btn_vpn_toggle.configure(text="Show")
                    
            btn_vpn_toggle = ctk.CTkButton(vpn_pass_frame, text="Show", width=60, command=toggle_vpn_pass)
            btn_vpn_toggle.grid(row=0, column=1, padx=(10, 0))
            
            self.env_entries["VPN_PASS"] = entry_vpn_pass
            row_idx += 1
            
            from src.modules.env_wizard import detect_lan_network
            add_standard_row("LAN_NETWORK", "Local Network Range (e.g. 192.168.1.0/24)", detect_lan_network())

    def save_current_selections(self):
        # Updates config metadata
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}
        
        # Read text values safely
        env_dict = {}
        if hasattr(self, "env_entries") and self.env_entries:
            for key, entry in list(self.env_entries.items()):
                try:
                    if hasattr(entry, "winfo_exists") and not entry.winfo_exists():
                        continue
                    env_dict[key] = entry.get().strip()
                except Exception:
                    pass
            
        # Ensure HTTP_PASSWORD is not empty (auto-generate if blank)
        if not env_dict.get("HTTP_PASSWORD"):
            env_dict["HTTP_PASSWORD"] = new_random_password()
            
        os.environ["DEPLOY_DIR"] = self.entry_deploy_path.get().strip()
        
        env_dict["DOCKERDIR"] = self.entry_deploy_path.get().strip()
        env_dict["USERDIR"] = self.entry_deploy_path.get().strip()
        
        # Generate secure backend database & Kopia passwords (CLI Parity)
        for key in ["MYSQL_ROOT_PASSWORD", "MYSQL_USER", "MYSQL_PASSWORD", "DB_PASS", "MONGO_PASS", "KOPIA_PASSWORD", "CROWDSEC_API_KEY"]:
            metadata = get_metadata()
            saved_env = metadata.get("env_vars", {})
            
            if key not in env_dict or not env_dict[key]:
                if saved_env.get(key):
                    env_dict[key] = saved_env.get(key)
                elif key == "MYSQL_USER":
                    env_dict[key] = "mediauser"
                elif key == "CROWDSEC_API_KEY":
                    env_dict[key] = new_random_password() if "crowdsec" in self.selected_services else ""
                else:
                    env_dict[key] = new_random_password()
                    
        env_dict["CROWDSEC_ENABLED"] = "true" if "crowdsec" in self.selected_services else "false"
        
        # Save to state manager
        metadata = get_metadata()
        metadata["selected_services"] = list(self.selected_services)
        metadata["env_vars"] = env_dict
        set_metadata(metadata)

    # ==========================================
    # 4. DEPLOY FRAME CREATION
    # ==========================================
    # ==========================================
    # 4. DEPLOY FRAME CREATION
    # ==========================================
    def create_deploy_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        
        lbl_title = ctk.CTkLabel(frame, text="Orchestration & Deploy", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        # Display Summaries
        self.lbl_deploy_summary = ctk.CTkLabel(frame, text="", justify="left", font=ctk.CTkFont(size=13))
        self.lbl_deploy_summary.grid(row=1, column=0, pady=(5, 5), sticky="w")
        
        # Progress Indicators Frame
        progress_control_frame = ctk.CTkFrame(frame, fg_color="transparent")
        progress_control_frame.grid(row=2, column=0, sticky="ew", pady=5)
        progress_control_frame.grid_columnconfigure(0, weight=1)
        
        # Steps Indicator
        self.steps_frame = ctk.CTkFrame(progress_control_frame, corner_radius=8)
        self.steps_frame.grid(row=0, column=0, sticky="ew", pady=5)
        self.steps_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.step_indicators = {}
        steps_list = [
            ("Preflight", "Preflight"),
            ("Dirs", "Directories"),
            ("Network", "Networks"),
            ("Compose", "Compose"),
            ("Containers", "Containers"),
            ("Stitch", "Stitching")
        ]
        
        for idx, (key, name) in enumerate(steps_list):
            lbl_step = ctk.CTkLabel(self.steps_frame, text=f"• {name}: Ready", font=ctk.CTkFont(size=11))
            lbl_step.grid(row=0, column=idx, padx=5, pady=8, sticky="ew")
            self.step_indicators[key] = lbl_step
            
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(progress_control_frame)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        self.progress_bar.set(0.0)
        
        # Verbose Toggle
        self.var_verbose = tk.BooleanVar(value=False)
        self.chk_verbose = ctk.CTkCheckBox(progress_control_frame, text="Enable Verbose (Debug) Logging", variable=self.var_verbose)
        self.chk_verbose.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        # Deployment Button
        self.btn_start_deploy = ctk.CTkButton(frame, text="Deploy Stack Now", height=45, fg_color="green", hover_color="#006400", font=ctk.CTkFont(size=15, weight="bold"), command=self.trigger_deployment_pipeline)
        self.btn_start_deploy.grid(row=3, column=0, pady=10, sticky="ew")
        
        # Real-time console log
        self.log_text = tk.Text(frame, wrap="word", height=12, bg="#1e1e1e", fg="#d4d4d4", font=("Courier", 11), borderwidth=0)
        self.log_text.grid(row=4, column=0, sticky="nsew", pady=(5, 10))
        
        # Navigation
        self.deploy_nav_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.deploy_nav_frame.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.deploy_nav_frame.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(self.deploy_nav_frame, text="Back", width=100, command=self.show_env_frame)
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
                
                # Check verbose setting for deploy tab
                show_verbose = self.var_verbose.get() if hasattr(self, "var_verbose") else False
                is_debug = "[DEBUG]" in msg or "[TRACE]" in msg or msg.startswith("[DEBUG]") or msg.startswith("[TRACE]")
                
                if show_verbose or not is_debug:
                    self.log_text.insert(tk.END, msg + "\n")
                    self.log_text.see(tk.END)
                
                if hasattr(self, "logs_textbox") and self.logs_textbox.winfo_exists():
                    show_verbose_logs = self.chk_verbose_logs.get()
                    if show_verbose_logs or not is_debug:
                        self.logs_textbox.configure(state="normal")
                        self.logs_textbox.insert(tk.END, msg + "\n")
                        self.logs_textbox.configure(state="disabled")
                        self.logs_textbox.see(tk.END)
                        
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

    def update_step_status(self, key: str, status: str, color: str = None):
        def run():
            if key in self.step_indicators:
                steps_names = {
                    "Preflight": "Preflight",
                    "Dirs": "Directories",
                    "Network": "Networks",
                    "Compose": "Compose",
                    "Containers": "Containers",
                    "Stitch": "Stitching"
                }
                name = steps_names.get(key, key)
                symbol = "•"
                if status == "Running":
                    symbol = "⚙"
                elif status == "Completed":
                    symbol = "✓"
                elif status == "Failed":
                    symbol = "✗"
                
                text = f"{symbol} {name}: {status}"
                self.step_indicators[key].configure(text=text)
                if color:
                    self.step_indicators[key].configure(text_color=color)
        self.after(0, run)

    def update_progress_bar(self, value: float):
        self.after(0, lambda: self.progress_bar.set(value))

    def deployment_worker(self):
        deploy_dir = get_deploy_dir()
        
        # Reset step indicators and progress bar
        for key in self.step_indicators:
            self.update_step_status(key, "Ready", color=["#000000", "#FFFFFF"])
        self.update_progress_bar(0.0)
        
        # Check verbose setting
        if self.var_verbose.get():
            os.environ["DEBUG_LOGGING"] = "true"
        else:
            os.environ["DEBUG_LOGGING"] = "false"
            
        try:
            # 1. Preflight
            self.update_step_status("Preflight", "Running", "#FFCC00")
            self.update_progress_bar(0.1)
            self.log_message("[INFO] Starting preflight system validation checks...")
            set_log_path(os.path.join(deploy_dir, "logs"))
            run_system_preflight()
            self.update_step_status("Preflight", "Completed", "green")
            
            # 2. Directories
            self.update_step_status("Dirs", "Running", "#FFCC00")
            self.update_progress_bar(0.25)
            self.log_message("[INFO] Constructing deployment folder structures...")
            
            # Write environment variables first so that setup_directories() can read them correctly
            metadata = get_metadata()
            env_vars = metadata.get("env_vars", {})
            env_path = os.path.normpath(os.path.join(deploy_dir, ".env"))
            os.makedirs(os.path.dirname(env_path), exist_ok=True)
            with open(env_path, "w", encoding="utf-8") as f:
                for k, v in env_vars.items():
                    f.write(f"{k}={v}\n")
            
            setup_directories()
            self.update_step_status("Dirs", "Completed", "green")
            
            # 3. Environment Secrets and Networks
            self.update_step_status("Network", "Running", "#FFCC00")
            self.update_progress_bar(0.4)
            self.log_message("[INFO] Constructing secure Docker networks...")
            setup_networks()
            self.update_step_status("Network", "Completed", "green")
            
            # 4. Compose build
            self.update_step_status("Compose", "Running", "#FFCC00")
            self.update_progress_bar(0.6)
            self.log_message("[INFO] Generating Docker Compose stacks config files...")
            build_compose_stacks()
            self.update_step_status("Compose", "Completed", "green")
            
            # 5. Launch containers
            self.update_step_status("Containers", "Running", "#FFCC00")
            self.update_progress_bar(0.8)
            self.log_message("[INFO] Executing compose pulls and starting container stacks in parallel...")
            deploy_stacks()
            
            # Sync .env
            stacks_dir = os.path.join(deploy_dir, "stacks")
            if os.path.exists(stacks_dir):
                for name in os.listdir(stacks_dir):
                    fpath = os.path.join(stacks_dir, name)
                    if os.path.isdir(fpath):
                        try:
                            shutil.copy(env_path, os.path.join(fpath, ".env"))
                        except Exception:
                            pass
            self.update_step_status("Containers", "Completed", "green")
            
            # 6. Auto config
            self.update_step_status("Stitch", "Running", "#FFCC00")
            self.update_progress_bar(0.9)
            self.log_message("[INFO] Commencing automated API token alignment and dashboard stitching...")
            auto_stitch_services()
            self.update_step_status("Stitch", "Completed", "green")
            
            self.update_progress_bar(1.0)
            self.log_message("[SUCCESS] Setup successfully deployed!")
            
            # Load the Post-Deployment dashboard directly upon successful run!
            self.after(500, self.show_post_deploy_summary)
            
        except Exception as e:
            for k in ["Preflight", "Dirs", "Network", "Compose", "Containers", "Stitch"]:
                txt = self.step_indicators[k].cget("text")
                if "⚙" in txt or "Running" in txt:
                    self.update_step_status(k, "Failed", "red")
            self.log_message(f"[ERROR] Setup failed: {str(e)}")
            import traceback
            write_log(traceback.format_exc(), level="ERROR")
        finally:
            self.after(0, lambda: self.btn_start_deploy.configure(state="normal", text="Deploy Stack Now"))

    def show_post_deploy_summary(self):
        self.select_sidebar_button(None)
        self.hide_all_frames()
        
        if hasattr(self, "summary_view_frame"):
            self.summary_view_frame.destroy()
            
        self.summary_view_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.summary_view_frame.grid(row=0, column=0, sticky="nsew")
        self.summary_view_frame.grid_columnconfigure(0, weight=1)
        self.summary_view_frame.grid_rowconfigure(2, weight=1)
        
        lbl_title = ctk.CTkLabel(self.summary_view_frame, text="Setup Summary Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self.summary_view_frame, text="Your Media and Home Server stack is successfully deployed. Use this dashboard to manage your credentials and links.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # Tabview layout
        tabview = ctk.CTkTabview(self.summary_view_frame)
        tabview.grid(row=2, column=0, sticky="nsew", pady=10)
        
        tab_status = tabview.add("Service Status")
        tab_widgets = tabview.add("Widget Setup")
        tab_guide = tabview.add("Next Steps")
        
        self.build_status_tab(tab_status)
        self.build_widgets_tab(tab_widgets)
        self.build_guide_tab(tab_guide)
        
        btn_exit = ctk.CTkButton(self.summary_view_frame, text="Done & Exit", width=150, height=35, command=self.destroy)
        btn_exit.grid(row=3, column=0, pady=(10, 0), sticky="e")

    def build_status_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        scroll.grid_columnconfigure((0, 1, 2), weight=1)
        
        from src.modules.auto_configure import test_port
        metadata = get_metadata()
        selected = metadata.get("selected_services", [])
        
        lbl_header_svc = ctk.CTkLabel(scroll, text="Service Name", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_svc.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        lbl_header_status = ctk.CTkLabel(scroll, text="Status", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_status.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        lbl_header_action = ctk.CTkLabel(scroll, text="Action", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_action.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        row_idx = 1
        for entry in self.registry:
            if entry.key in selected:
                port = int(entry.port) if entry.port and entry.port.isdigit() else 0
                is_online = False
                if port > 0:
                    is_online = test_port("localhost", port)
                    
                status_text = "ONLINE" if is_online else "OFFLINE"
                status_color = "green" if is_online else "red"
                
                lbl_name = ctk.CTkLabel(scroll, text=entry.key)
                lbl_name.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
                
                lbl_stat = ctk.CTkLabel(scroll, text=status_text, text_color=status_color, font=ctk.CTkFont(weight="bold"))
                lbl_stat.grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
                
                non_ui_services = {"flaresolverr", "hkserver", "mariadb", "postgresql", "mongodb", "redis", "db"}
                url = f"http://localhost:{port}" if port > 0 and entry.key not in non_ui_services else ""
                
                def open_link(u=url):
                    if u:
                        import webbrowser
                        webbrowser.open(u)
                        
                if url:
                    btn_link = ctk.CTkButton(scroll, text="Open Web UI", width=100, command=open_link)
                    btn_link.grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")
                else:
                    lbl_nolink = ctk.CTkLabel(scroll, text="No Web Interface", font=ctk.CTkFont(slant="italic"))
                    lbl_nolink.grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")
                    
                row_idx += 1

    def build_widgets_tab(self, tab):
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
                from tkinter import messagebox
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
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        guide_text = (
            "Congratulations! Your media server stack is fully operational.\n\n"
            "GETTING STARTED GUIDE:\n"
            "1. Access Homepage Dashboard: Open http://localhost:8080 in your browser to view your stack.\n"
            "2. Access Docker Manager (Dockge): Open http://localhost:5001 to monitor container stacks and logs.\n"
            "3. Prowlarr Indexers: Open Prowlarr to verify indexers. They automatically synchronize to Radarr and Sonarr.\n"
            "4. SABnzbd / qBittorrent: Verify downloads folder configuration paths match the mounted root volumes (/downloads).\n\n"
            "CLEANUP WARNING:\n"
            "If you de-selected any services during this run, their container instances have been stopped and deleted cleanly. "
            "However, to protect your data, their persistent files remain in the appdata/ and stacks/ directory. "
            "You can manually delete them to reclaim disk space if you do not plan to use them again."
        )
        
        lbl_guide = ctk.CTkLabel(scroll, text=guide_text, justify="left", wraplength=550, font=ctk.CTkFont(size=12))
        lbl_guide.pack(padx=10, pady=10)

    def create_logs_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        
        lbl_title = ctk.CTkLabel(frame, text="System Installation Logs", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(frame, text="View the comprehensive execution output from the background process in real-time.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # Verbose Log Checkbox
        self.chk_verbose_logs = ctk.CTkCheckBox(
            frame, 
            text="Enable Verbose (Debug) Logging", 
            command=self.update_logs_view_content,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.chk_verbose_logs.grid(row=2, column=0, pady=5, sticky="w")
        
        # Log Text Area
        self.logs_textbox = ctk.CTkTextbox(frame, height=400, font=ctk.CTkFont(family="Courier", size=11))
        self.logs_textbox.grid(row=3, column=0, sticky="nsew", pady=10)
        self.logs_textbox.configure(state="disabled")
        
        # Open in Editor button
        btn_open = ctk.CTkButton(frame, text="Open Log in Editor", width=180, command=self.open_log_in_editor)
        btn_open.grid(row=4, column=0, pady=(10, 0), sticky="e")
        
        return frame

    def update_logs_view_content(self):
        if not hasattr(self, "logs_textbox"):
            return
        from src.utils.logger import get_log_path
        log_path = get_log_path()
        if os.path.exists(log_path) and os.path.isdir(log_path):
            try:
                shutil.rmtree(log_path)
            except OSError:
                pass
        if not os.path.exists(log_path):
            self.logs_textbox.configure(state="normal")
            self.logs_textbox.delete("1.0", tk.END)
            self.logs_textbox.insert(tk.END, "[INFO] No log files generated yet.")
            self.logs_textbox.configure(state="disabled")
            return
            
        show_verbose = self.chk_verbose_logs.get()
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            lines = [f"[ERROR] Failed to read log file: {str(e)}\n"]
            
        filtered_lines = []
        for line in lines:
            if not show_verbose:
                if "[DEBUG]" in line or "[TRACE]" in line:
                    continue
            filtered_lines.append(line)
            
        self.logs_textbox.configure(state="normal")
        self.logs_textbox.delete("1.0", tk.END)
        self.logs_textbox.insert(tk.END, "".join(filtered_lines))
        self.logs_textbox.configure(state="disabled")
        self.logs_textbox.see(tk.END)

    def open_log_in_editor(self):
        from src.utils.logger import get_log_path
        log_path = get_log_path()
        if not os.path.exists(log_path):
            from tkinter import messagebox
            messagebox.showwarning("Log Not Found", "No log file has been created yet.")
            return
        try:
            if sys.platform == "win32":
                os.startfile(log_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", log_path])
            else:
                subprocess.Popen(["xdg-open", log_path])
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to open log file: {str(e)}")

if __name__ == "__main__":
    app = DockerSetupGUI()
    app.mainloop()
