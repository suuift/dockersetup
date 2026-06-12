import tkinter as tk
import customtkinter as ctk
import webbrowser
from src.gui.base_frame import BaseFrame
from src.utils.state import get_metadata

class ServicesFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        lbl_title = ctk.CTkLabel(self, text="Select Stack Services", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, pady=(10, 5), sticky="w")
        
        lbl_desc = ctk.CTkLabel(self, text="Pick which media tools, database endpoints, and system management services you want to deploy in your stack.", font=ctk.CTkFont(size=13))
        lbl_desc.grid(row=1, column=0, pady=(0, 5), sticky="w")
        
        # Toggle Switch for Advanced Setup
        self.switch_advanced = ctk.CTkSwitch(
            self, 
            text="Enable Advanced Custom Setup", 
            variable=self.controller.var_advanced_mode, 
            command=self.controller.on_advanced_switch_toggle,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.switch_advanced.grid(row=2, column=0, pady=(5, 5), sticky="w")
        
        # Search Bar for available services
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=3, column=0, sticky="ew", pady=(5, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search available services...", height=30)
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.controller.filter_services_checklist)
        
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
        
        btn_next = ctk.CTkButton(nav_buttons, text="Next: Configure Credentials", width=220, command=self.controller.check_recommendations_and_proceed)
        btn_next.grid(row=0, column=1, sticky="e")
