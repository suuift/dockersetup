import os
import sys
import platform
import shutil
import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from src.gui.base_frame import BaseFrame
from src.utils.paths import get_deploy_dir
from src.utils.logger import set_log_path, write_log

class WelcomeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Welcome Title
        lbl_title = ctk.CTkLabel(self, text="Welcome to DockerSetup", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="This wizard will help you configure, orchestrate, and deploy a complete Media and Home Server stack on your system.", justify="left", font=ctk.CTkFont(size=14))
        lbl_desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Prerequisites Panel
        prereq_box = ctk.CTkLabel(self, text="System Prerequisites Checks", font=ctk.CTkFont(size=16, weight="bold"))
        prereq_box.grid(row=2, column=0, pady=5, sticky="w")
        
        self.prereq_container = ctk.CTkFrame(self, corner_radius=8)
        self.prereq_container.grid(row=3, column=0, sticky="nsew", pady=(5, 20))
        self.prereq_container.grid_columnconfigure(0, weight=1)
        
        # Target deployment folder selector
        lbl_folder_title = ctk.CTkLabel(self, text="Deployment Directory Selection", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_folder_title.grid(row=4, column=0, pady=(10, 5), sticky="w")
        
        dir_selector_frame = ctk.CTkFrame(self, fg_color="transparent")
        dir_selector_frame.grid(row=5, column=0, sticky="ew", pady=5)
        dir_selector_frame.grid_columnconfigure(0, weight=1)
        
        # Setup initial path
        initial_deploy = get_deploy_dir()
        self.entry_deploy_path = ctk.CTkEntry(dir_selector_frame, placeholder_text="Enter deploy directory path...")
        self.entry_deploy_path.insert(0, initial_deploy)
        self.entry_deploy_path.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        btn_browse = ctk.CTkButton(dir_selector_frame, text="Browse...", width=100, command=self.controller.browse_deployment_directory)
        btn_browse.grid(row=0, column=1, sticky="e")
        
        # Next Button
        btn_next = ctk.CTkButton(self, text="Next: Select Services", width=180, height=40, command=self.validate_directory_and_proceed)
        btn_next.grid(row=6, column=0, pady=(20, 10), sticky="e")

    def run_preflight_checks(self):
        for widget in self.prereq_container.winfo_children():
            widget.destroy()
            
        os_sys = platform.system()
        lbl_os = ctk.CTkLabel(self.prereq_container, text=f"• Host Operating System: {os_sys}", font=ctk.CTkFont(size=13))
        lbl_os.grid(row=0, column=0, padx=20, pady=8, sticky="w")
        
        from src.utils.paths import get_clean_env
        docker_exists = shutil.which("docker") is not None
        docker_color = "green" if docker_exists else "red"
        docker_text = "FOUND & INSTALLED" if docker_exists else "NOT FOUND (Required)"
        lbl_docker = ctk.CTkLabel(self.prereq_container, text=f"• Docker System Check: {docker_text}", text_color=docker_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_docker.grid(row=1, column=0, padx=20, pady=8, sticky="w")
        
        compose_text = "NOT FOUND"
        compose_exists = False
        if docker_exists:
            test_proc = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True, env=get_clean_env())
            if test_proc.returncode == 0:
                compose_exists = True
                compose_text = "DOCKER COMPOSE V2 PLUG-IN INSTALLED"
        
        compose_color = "green" if compose_exists else "red"
        lbl_compose = ctk.CTkLabel(self.prereq_container, text=f"• Compose Engine Check: {compose_text}", text_color=compose_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_compose.grid(row=2, column=0, padx=20, pady=8, sticky="w")

        daemon_running = False
        if docker_exists:
            try:
                subprocess.run(
                    ["docker", "info"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                    timeout=3,
                    env=get_clean_env()
                )
                daemon_running = True
            except Exception:
                daemon_running = False

        daemon_text = "RUNNING" if daemon_running else "NOT RUNNING"
        daemon_color = "green" if daemon_running else "red"
        lbl_daemon = ctk.CTkLabel(self.prereq_container, text=f"• Docker Daemon Check: {daemon_text}", text_color=daemon_color, font=ctk.CTkFont(size=13, weight="bold"))
        lbl_daemon.grid(row=3, column=0, padx=20, pady=8, sticky="w")

    def validate_directory_and_proceed(self):
        d_dir = self.entry_deploy_path.get().strip()
        if not d_dir:
            return
            
        d_dir = os.path.normpath(d_dir)
        os.environ["DEPLOY_DIR"] = d_dir
        set_log_path(os.path.join(d_dir, "logs"))
        
        if not os.path.exists(d_dir):
            create = messagebox.askyesno("Create Directory?", f"Directory '{d_dir}' does not exist. Create it?")
            if create:
                try:
                    os.makedirs(d_dir, exist_ok=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create directory: {str(e)}")
                    return
            else:
                return
                
        metadata_file = os.path.join(d_dir, ".metadata.json")
        if os.path.exists(metadata_file):
            dialog = ctk.CTkToplevel(self.controller)
            dialog.title("Existing Deployment Detected")
            dialog.resizable(False, False)
            self.controller.center_over_parent(dialog, 500, 320)
            
            lbl_title = ctk.CTkLabel(dialog, text="Existing Deployment Found", font=ctk.CTkFont(size=18, weight="bold"))
            lbl_title.pack(pady=(20, 10))
            
            msg = f"An existing DockerSetup stack was found at:\n{d_dir}\n\nWhat would you like to do?"
            lbl_msg = ctk.CTkLabel(dialog, text=msg, wraplength=450, justify="center", font=ctk.CTkFont(size=13))
            lbl_msg.pack(pady=10)
            
            def on_modify():
                dialog.destroy()
                self.controller.build_services_checkboxes()
                self.controller.show_services_frame(from_next=True)
                
            def on_upgrade():
                dialog.destroy()
                self.controller.run_fast_upgrade(d_dir)
                
            def on_reset():
                dialog.destroy()
                self.controller.run_full_reset(d_dir)
                
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
            self.controller.show_services_frame(from_next=True)
