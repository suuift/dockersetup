import os
import sys
import tkinter as tk
import customtkinter as ctk
from src.gui.base_frame import BaseFrame
from src.utils.paths import get_deploy_dir

class DeployFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        lbl_title = ctk.CTkLabel(self, text="Orchestration & Deploy", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        # Display Summaries
        self.lbl_deploy_summary = ctk.CTkLabel(self, text="", justify="left", font=ctk.CTkFont(size=13))
        self.lbl_deploy_summary.grid(row=1, column=0, pady=(5, 5), sticky="w")
        
        # Progress Indicators Frame
        progress_control_frame = ctk.CTkFrame(self, fg_color="transparent")
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
        self.chk_verbose = ctk.CTkCheckBox(progress_control_frame, text="Enable Verbose (Debug) Logging", variable=self.var_verbose, command=self.refresh_deploy_logs)
        self.chk_verbose.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        # Deployment Button
        self.btn_start_deploy = ctk.CTkButton(self, text="Deploy Stack Now", height=45, fg_color="green", hover_color="#006400", font=ctk.CTkFont(size=15, weight="bold"), command=self.controller.trigger_deployment_pipeline)
        self.btn_start_deploy.grid(row=3, column=0, pady=10, sticky="ew")
        
        # Real-time console log
        self.log_text = tk.Text(self, wrap="word", height=12, bg="#1e1e1e", fg="#d4d4d4", font=("Courier", 11), borderwidth=0)
        self.log_text.grid(row=4, column=0, sticky="nsew", pady=(5, 10))
        
        # Navigation
        self.deploy_nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.deploy_nav_frame.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.deploy_nav_frame.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(self.deploy_nav_frame, text="Back", width=100, command=self.controller.show_env_frame)
        btn_back.grid(row=0, column=0, sticky="w")

    def update_deploy_summary(self):
        deploy_dir = get_deploy_dir()
        services_count = len(self.controller.selected_services)
        summary_text = (
            f"• Target deployment path: {deploy_dir}\n"
            f"• Selected services to deploy ({services_count}): {', '.join(sorted(self.controller.selected_services)) if self.controller.selected_services else 'None Selected'}\n"
            f"• Status: Ready to generate compose files."
        )
        self.lbl_deploy_summary.configure(text=summary_text)

    def refresh_deploy_logs(self):
        from src.utils.logger import get_log_path
        log_path = get_log_path()
        if not os.path.exists(log_path):
            self.log_text.delete("1.0", tk.END)
            return
            
        show_verbose = self.var_verbose.get()
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            lines = [f"[ERROR] Failed to read log file: {str(e)}\n"]
            
        filtered_lines = []
        for line in lines:
            if not show_verbose:
                if "[DEBUG]" in line or "[TRACE]" in line or ">>" in line:
                    continue
            filtered_lines.append(line.rstrip())
            
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "\n".join(filtered_lines) + "\n")
        self.log_text.see(tk.END)
