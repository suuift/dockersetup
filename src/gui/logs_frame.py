import os
import sys
import shutil
import subprocess
import tkinter as tk
import customtkinter as ctk
from src.gui.base_frame import BaseFrame

class LogsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        lbl_title = ctk.CTkLabel(self, text="System Installation Logs", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="View the comprehensive execution output from the background process in real-time.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        # Verbose Log Checkbox
        self.chk_verbose_logs = ctk.CTkCheckBox(
            self, 
            text="Enable Verbose (Debug) Logging", 
            command=self.update_logs_view_content,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.chk_verbose_logs.grid(row=2, column=0, pady=5, sticky="w")
        
        # Log Text Area
        self.logs_textbox = ctk.CTkTextbox(self, height=400, font=ctk.CTkFont(family="Courier", size=11))
        self.logs_textbox.grid(row=3, column=0, sticky="nsew", pady=10)
        self.logs_textbox.configure(state="disabled")
        
        # Open in Editor button
        btn_open = ctk.CTkButton(self, text="Open Log in Editor", width=180, command=self.open_log_in_editor)
        btn_open.grid(row=4, column=0, pady=(10, 0), sticky="e")

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
