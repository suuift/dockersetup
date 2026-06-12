import os
import sys
import threading
import queue
import time
import socket
import platform
import subprocess
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import tkinter.ttk as ttk

# Prevent darkdetect from executing blocking subprocess calls on Linux
if sys.platform.startswith("linux"):
    try:
        import darkdetect
        darkdetect.theme = lambda: "Dark"
    except Exception:
        pass

# Monkey-patch CTkScrollableFrame.check_if_master_is_canvas
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

# Import modular frames
from src.gui.welcome_frame import WelcomeFrame
from src.gui.services_frame import ServicesFrame
from src.gui.env_frame import EnvFrame
from src.gui.deploy_frame import DeployFrame
from src.gui.logs_frame import LogsFrame
from src.gui.summary_frame import SummaryFrame

class DockerSetupGUI(ctk.CTk):
    def get_linux_dpi_scale(self) -> float:
        try:
            tk_scale = self.tk.call('tk', 'scaling')
            detected = tk_scale / 1.33333333
            return max(detected, 1.25)
        except Exception:
            return 1.25

    def on_window_resize_event(self, event):
        if event.widget != self:
            return
        if self.resize_timer:
            self.after_cancel(self.resize_timer)
        self.resize_timer = self.after(200, self.apply_dynamic_resize_scale)

    def apply_dynamic_resize_scale(self):
        current_width = self.winfo_width()
        if abs(self.last_scaled_width - current_width) < 15:
            return
        self.last_scaled_width = current_width
        width_ratio = current_width / self.baseline_width
        base_scale = self.get_linux_dpi_scale() if sys.platform.startswith("linux") else 1.0
        new_scale = max(base_scale, min(base_scale * width_ratio, 1.8))
        ctk.set_widget_scaling(new_scale)
        self.scaling_optionmenu.set(f"{int(new_scale * 100)}%")
        self.update_idletasks()
        self.update()

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
                    if pid.value == os.getpid() or pid.value == os.getppid():
                        ctypes.windll.user32.ShowWindow(hwnd, 0) # SW_HIDE = 0
            except Exception:
                pass

        # 1. Main Window Settings
        self.title(f"DockerSetup v{VERSION} - Graphical Setup Suite")
        self.geometry("1000x650")
        self.minsize(900, 600)
        
        # Scaling variables
        self.resize_timer = None
        self.baseline_width = 1000
        self.last_scaled_width = 1000
        
        # Determine theme based on system setting
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Detect and apply platform DPI auto-scaling for Linux
        if sys.platform.startswith("linux"):
            try:
                scale = self.get_linux_dpi_scale()
                ctk.set_widget_scaling(scale)
                ctk.set_window_scaling(scale)
                self.last_scaled_width = int(1000 * scale)
                self.baseline_width = int(1000 * scale)
            except Exception:
                pass

        self.bind("<Configure>", self.on_window_resize_event)

        # Force Headless execution mode for background modules to bypass interactive questionary prompts
        os.environ["DS_HEADLESS"] = "true"
        
        # State & Logger
        self.log_queue = queue.Queue()
        from src.utils.logger import set_gui_log_callback
        set_gui_log_callback(self.log_message)
        
        self.registry = []
        self.selected_services = set()
        self.env_vars = {}
        self.chk_vars = {}
        
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
        
        self.btn_logs = ctk.CTkButton(self.sidebar_frame, text="View Logs", anchor="w", command=self.show_logs_frame)
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
        self.welcome_frame = WelcomeFrame(self.main_container, self)
        self.services_frame = ServicesFrame(self.main_container, self)
        self.env_frame = EnvFrame(self.main_container, self)
        self.deploy_frame = DeployFrame(self.main_container, self)
        self.logs_view_frame = LogsFrame(self.main_container, self)
        self.summary_view_frame = SummaryFrame(self.main_container, self)
        
        # Initialize default log path on startup
        initial_deploy = get_deploy_dir()
        log_dir = os.path.join(initial_deploy, "logs")
        set_log_path(log_dir)
        
        # Rotate setup.log on startup if it's > 0 bytes
        log_path = os.path.join(log_dir, "setup.log")
        old_log_path = os.path.join(log_dir, "setup.old.log")
        if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
            try:
                if os.path.exists(old_log_path):
                    os.remove(old_log_path)
                os.rename(log_path, old_log_path)
            except Exception:
                pass
        
        try:
            os.makedirs(log_dir, exist_ok=True)
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("")
        except Exception:
            pass
        
        # Initialize Sidebar button states
        self.update_navigation_buttons()
        
        # Launch Welcome Frame first
        self.show_welcome_frame()
        self.run_preflight_checks()
        
        # Start background queue reader for logs
        self.after(100, self.read_log_queue)

    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def change_scaling_event(self, new_scaling: str):
        try:
            scale_val = int(new_scaling.replace("%", "")) / 100
            ctk.set_widget_scaling(scale_val)
            ctk.set_window_scaling(scale_val)
            self.last_scaled_width = self.winfo_width()
            self.update_idletasks()
            self.update()
        except Exception:
            pass

    def update_navigation_buttons(self):
        self.btn_welcome.configure(state="normal")
        self.btn_services.configure(state="normal" if self.max_completed_step >= 2 else "disabled")
        self.btn_env.configure(state="normal" if self.max_completed_step >= 3 else "disabled")
        self.btn_deploy.configure(state="normal" if self.max_completed_step >= 4 else "disabled")
        if hasattr(self, "btn_logs"):
            self.btn_logs.configure(state="normal")

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
                    btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
                else:
                    btn.configure(fg_color="transparent")

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
        self.save_current_selections()
        self.update_deploy_summary()
        self.deploy_frame.grid(row=0, column=0, sticky="nsew")

    def show_logs_frame(self, from_next=False):
        self.update_navigation_buttons()
        self.select_sidebar_button(self.btn_logs)
        self.hide_all_frames()
        self.logs_view_frame.update_logs_view_content()
        self.logs_view_frame.grid(row=0, column=0, sticky="nsew")

    def show_post_deploy_summary(self):
        self.select_sidebar_button(None)
        self.hide_all_frames()
        self.summary_view_frame.load_tabs_data()
        self.summary_view_frame.grid(row=0, column=0, sticky="nsew")

    def hide_all_frames(self):
        for frame in [self.welcome_frame, self.services_frame, self.env_frame, self.deploy_frame, self.logs_view_frame, self.summary_view_frame]:
            if frame:
                frame.grid_forget()

    def run_preflight_checks(self):
        if hasattr(self, "welcome_frame"):
            self.welcome_frame.run_preflight_checks()

    def browse_deployment_directory(self):
        if hasattr(self, "welcome_frame"):
            selected_dir = filedialog.askdirectory(initialdir=self.welcome_frame.entry_deploy_path.get())
            if selected_dir:
                normalized = os.path.normpath(selected_dir)
                self.welcome_frame.entry_deploy_path.delete(0, tk.END)
                self.welcome_frame.entry_deploy_path.insert(0, normalized)
                os.environ["DEPLOY_DIR"] = normalized
                set_log_path(os.path.join(normalized, "logs"))

    def build_services_checkboxes(self):
        if hasattr(self, "services_frame"):
            self.services_frame.build_services_checkboxes()

    def build_dynamic_env_fields(self):
        if hasattr(self, "env_frame"):
            self.env_frame.build_dynamic_env_fields()

    def save_current_selections(self):
        self.selected_services = {key for key, var in self.chk_vars.items() if var.get()}
        env_dict = {}
        if hasattr(self, "env_frame") and hasattr(self.env_frame, "env_entries"):
            for key, entry in list(self.env_frame.env_entries.items()):
                try:
                    if hasattr(entry, "winfo_exists") and not entry.winfo_exists():
                        continue
                    env_dict[key] = entry.get().strip()
                except Exception:
                    pass
            
        if not env_dict.get("HTTP_PASSWORD"):
            env_dict["HTTP_PASSWORD"] = new_random_password()
            
        deploy_path = self.welcome_frame.entry_deploy_path.get().strip()
        os.environ["DEPLOY_DIR"] = deploy_path
        
        env_dict["DOCKERDIR"] = deploy_path
        env_dict["USERDIR"] = deploy_path
        
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
        
        metadata = get_metadata()
        metadata["selected_services"] = list(self.selected_services)
        metadata["env_vars"] = env_dict
        set_metadata(metadata)

    def update_deploy_summary(self):
        if hasattr(self, "deploy_frame"):
            self.deploy_frame.update_deploy_summary()

    def run_fast_upgrade(self, d_dir):
        self.show_deploy_frame(from_next=True)
        if hasattr(self, "deploy_frame"):
            self.deploy_frame.log_text.delete("1.0", tk.END)
            self.log_message("[INFO] Starting fast template upgrade...")
            self.trigger_deployment_pipeline()

    def run_full_reset(self, d_dir):
        confirm = messagebox.askyesno(
            "Permanent Wipe Warning", 
            "Are you sure you want to permanently wipe all containers, volumes, and configurations in this directory?\n\nThis action cannot be undone."
        )
        if not confirm:
            return
            
        dialog = ctk.CTkToplevel(self)
        dialog.title("Resetting System")
        dialog.resizable(False, False)
        self.center_over_parent(dialog, 400, 150)
        
        lbl_msg = ctk.CTkLabel(dialog, text="Wiping all configurations and volumes...", font=ctk.CTkFont(size=13))
        lbl_msg.pack(pady=(20, 10))
        
        prog_bar = ctk.CTkProgressBar(dialog, width=300)
        prog_bar.pack(pady=10)
        prog_bar.configure(mode="indefinite")
        prog_bar.start()
        
        def reset_worker():
            try:
                write_log("[INFO] Commencing full system reset...")
                stacks_dir = os.path.join(d_dir, "stacks")
                if os.path.exists(stacks_dir):
                    for stack in os.listdir(stacks_dir):
                        full_path = os.path.join(stacks_dir, stack)
                        if os.path.isdir(full_path):
                            compose_file = os.path.join(full_path, "docker-compose.yml")
                            if os.path.exists(compose_file):
                                write_log(f"[INFO] Tearing down stack: {stack}...")
                                subprocess.run(["docker", "compose", "down", "-v", "--remove-orphans"], cwd=full_path, capture_output=True, env=get_clean_env())
                                
                write_log("[INFO] Removing stack and configuration directories...")
                shutil.rmtree(stacks_dir, ignore_errors=True)
                shutil.rmtree(os.path.join(d_dir, "appdata"), ignore_errors=True)
                
                for file in [".metadata.json", ".env"]:
                    file_p = os.path.join(d_dir, file)
                    if os.path.exists(file_p):
                        try:
                            shutil.copy2(file_p, file_p + ".bak")
                            write_log(f"[INFO] Created backup: {file}.bak")
                            os.remove(file_p)
                        except Exception:
                            pass
                
                import src.utils.state as state
                state._metadata_cache = {}
                
                write_log("[SUCCESS] Reset complete. All containers and settings have been wiped!")
                self.after(0, lambda: [
                    dialog.destroy(),
                    messagebox.showinfo("Reset Complete", "All configurations, volumes, and containers have been wiped cleanly."),
                    self.show_welcome_frame()
                ])
            except Exception as e:
                write_log(f"[ERROR] Reset failed: {str(e)}")
                self.after(0, lambda: [
                    dialog.destroy(),
                    messagebox.showerror("Reset Failed", f"An error occurred during reset: {str(e)}")
                ])
                
        t = threading.Thread(target=reset_worker)
        t.daemon = True
        t.start()

    def log_message(self, message: str):
        self.log_queue.put(message)

    def read_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                
                show_verbose = self.deploy_frame.var_verbose.get() if hasattr(self, "deploy_frame") else False
                is_debug = "[DEBUG]" in msg or "[TRACE]" in msg or msg.startswith("[DEBUG]") or msg.startswith("[TRACE]")
                
                if (show_verbose or not is_debug) and hasattr(self, "deploy_frame"):
                    self.deploy_frame.log_text.insert(tk.END, msg + "\n")
                    self.deploy_frame.log_text.see(tk.END)
                
                if hasattr(self, "logs_view_frame") and hasattr(self.logs_view_frame, "logs_textbox"):
                    if self.logs_view_frame.logs_textbox.winfo_exists():
                        show_verbose_logs = self.logs_view_frame.chk_verbose_logs.get()
                        if show_verbose_logs or not is_debug:
                            self.logs_view_frame.logs_textbox.configure(state="normal")
                            self.logs_view_frame.logs_textbox.insert(tk.END, msg + "\n")
                            self.logs_view_frame.logs_textbox.configure(state="disabled")
                            self.logs_view_frame.logs_textbox.see(tk.END)
                            
                self.log_queue.task_done()
        except queue.Empty:
            pass
        self.after(100, self.read_log_queue)

    def trigger_deployment_pipeline(self):
        try:
            subprocess.run(
                ["docker", "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=4,
                env=get_clean_env()
            )
        except Exception:
            messagebox.showerror(
                "Docker Daemon Offline",
                "Docker daemon is not running. Please start Docker Desktop/Daemon and try again."
            )
            return

        if hasattr(self, "deploy_frame"):
            self.deploy_frame.btn_start_deploy.configure(state="disabled", text="Deploying...")
            self.deploy_frame.log_text.delete("1.0", tk.END)
        
        t = threading.Thread(target=self.deployment_worker)
        t.daemon = True
        t.start()

    def deployment_worker(self):
        deploy_dir = get_deploy_dir()
        
        if hasattr(self, "deploy_frame"):
            for key in self.deploy_frame.step_indicators:
                self.deploy_frame.update_step_status(key, "Ready", color=["#000000", "#FFFFFF"])
            self.deploy_frame.update_progress_bar(0.0)
            
            if self.deploy_frame.var_verbose.get():
                os.environ["DEBUG_LOGGING"] = "true"
            else:
                os.environ["DEBUG_LOGGING"] = "false"
            
        try:
            # 1. Preflight
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Preflight", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.1)
            self.log_message("[INFO] Starting preflight system validation checks...")
            set_log_path(os.path.join(deploy_dir, "logs"))
            run_system_preflight()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Preflight", "Completed", "green")
            
            # 2. Directories
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Dirs", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.25)
            self.log_message("[INFO] Constructing deployment folder structures...")
            
            metadata = get_metadata()
            env_vars = metadata.get("env_vars", {})
            env_path = os.path.normpath(os.path.join(deploy_dir, ".env"))
            os.makedirs(os.path.dirname(env_path), exist_ok=True)
            with open(env_path, "w", encoding="utf-8") as f:
                for k, v in env_vars.items():
                    f.write(f"{k}={v}\n")
            
            setup_directories()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Dirs", "Completed", "green")
            
            # 3. Environment Secrets and Networks
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Network", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.4)
            self.log_message("[INFO] Constructing secure Docker networks...")
            setup_networks()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Network", "Completed", "green")
            
            # 4. Compose build
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Compose", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.6)
            self.log_message("[INFO] Generating Docker Compose stacks config files...")
            build_compose_stacks()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Compose", "Completed", "green")
            
            # 5. Launch containers
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Containers", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.8)
            self.log_message("[INFO] Executing compose pulls and starting container stacks in parallel...")
            deploy_stacks()
            
            stacks_dir = os.path.join(deploy_dir, "stacks")
            if os.path.exists(stacks_dir):
                for name in os.listdir(stacks_dir):
                    fpath = os.path.join(stacks_dir, name)
                    if os.path.isdir(fpath):
                        try:
                            shutil.copy(env_path, os.path.join(fpath, ".env"))
                        except Exception:
                            pass
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Containers", "Completed", "green")
            
            # 6. Auto config
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Stitch", "Running", "#FFCC00")
                self.deploy_frame.update_progress_bar(0.9)
            self.log_message("[INFO] Commencing automated API token alignment and dashboard stitching...")
            auto_stitch_services()
            if hasattr(self, "deploy_frame"):
                self.deploy_frame.update_step_status("Stitch", "Completed", "green")
                self.deploy_frame.update_progress_bar(1.0)
            self.log_message("[SUCCESS] Setup successfully deployed!")
            
            self.after(500, self.show_post_deploy_summary)
            
        except Exception as e:
            if hasattr(self, "deploy_frame"):
                for k in ["Preflight", "Dirs", "Network", "Compose", "Containers", "Stitch"]:
                    txt = self.deploy_frame.step_indicators[k].cget("text")
                    if "⚙" in txt or "Running" in txt:
                        self.deploy_frame.update_step_status(k, "Failed", "red")
            self.log_message(f"[ERROR] Setup failed: {str(e)}")
            import traceback
            write_log(traceback.format_exc(), level="ERROR")
            err_msg = f"An error occurred during deployment:\n\n{str(e)}\n\nPlease check the logs for detailed information."
            self.after(0, lambda: messagebox.showerror("Deployment Failed", err_msg))
        finally:
            if hasattr(self, "deploy_frame"):
                self.after(0, lambda: self.deploy_frame.btn_start_deploy.configure(state="normal", text="Deploy Stack Now"))
