import os
import sys
import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import filedialog
from src.gui.base_frame import BaseFrame
from src.utils.state import get_metadata
from src.modules.env_wizard import COMMON_ZONES, detect_timezone, new_random_password

class EnvFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        lbl_title = ctk.CTkLabel(self, text="Configure Environment Credentials", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="Provide configuration settings and API keys for the selected services. Defaults will be used if left blank.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 10), sticky="w")
        
        self.env_scroll = ctk.CTkScrollableFrame(self)
        self.env_scroll.grid(row=2, column=0, sticky="nsew", pady=10)
        self.env_scroll.grid_columnconfigure(1, weight=1)
        
        # Navigation
        nav_buttons = ctk.CTkFrame(self, fg_color="transparent")
        nav_buttons.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        nav_buttons.grid_columnconfigure(0, weight=1)
        
        btn_back = ctk.CTkButton(nav_buttons, text="Back", width=100, command=self.controller.show_services_frame)
        btn_back.grid(row=0, column=0, sticky="w")
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Deploy Stack", width=180, command=lambda: self.controller.show_deploy_frame(from_next=True))
        btn_next.grid(row=0, column=1, sticky="e")
