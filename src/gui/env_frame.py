import os
import sys
import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import filedialog
import webbrowser
from src.gui.base_frame import BaseFrame
from src.utils.state import get_metadata
from src.modules.env_wizard import COMMON_ZONES, detect_timezone, new_random_password
from src.apps.loader import load_apps

class EnvFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.env_entries = {}
        
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

    def build_dynamic_env_fields(self):
        for widget in self.env_scroll.winfo_children():
            widget.destroy()
            
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
        
        # Dynamic settings fields from Pydantic config models in selected apps
        apps_dict = load_apps()
        for svc in sorted(self.controller.selected_services):
            if svc in apps_dict:
                app = apps_dict[svc]
                if app.config_model:
                    # Category section title
                    lbl_sect = ctk.CTkLabel(self.env_scroll, text=f"--- {app.name} Settings ---", font=ctk.CTkFont(size=13, weight="bold"), text_color=["#1F6AA5", "#3B8ED0"])
                    lbl_sect.grid(row=row_idx, column=0, columnspan=2, pady=(15, 5), sticky="w")
                    row_idx += 1
                    
                    for field_name, field_info in app.config_model.model_fields.items():
                        # Label
                        description = field_info.description or field_name
                        lbl_field = ctk.CTkLabel(self.env_scroll, text=f"{field_name}:", font=ctk.CTkFont(size=12, weight="bold"))
                        lbl_field.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
                        
                        extra = field_info.json_schema_extra or {}
                        is_secret = extra.get("is_secret", False) or "pass" in field_name.lower() or "key" in field_name.lower() or "token" in field_name.lower()
                        default_val = field_info.default if field_info.default is not None else ""
                        val = saved_env.get(field_name, default_val)
                        
                        # Input widget based on field type
                        field_type = field_info.annotation
                        
                        input_frame = ctk.CTkFrame(self.env_scroll, fg_color="transparent")
                        input_frame.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
                        
                        if field_type is bool:
                            var = tk.BooleanVar(value=(str(val).lower() == "true" or val is True or val == 1))
                            chk = ctk.CTkSwitch(input_frame, text=description, variable=var)
                            chk.pack(side="left", anchor="w")
                            # We store the variable in the entries dict so we can retrieve its value
                            self.env_entries[field_name] = var
                        elif is_secret:
                            entry_sec = ctk.CTkEntry(input_frame, placeholder_text=description, show="*", width=250)
                            entry_sec.insert(0, str(val))
                            entry_sec.pack(side="left", fill="x", expand=True)
                            
                            def make_toggle_sec(ent=entry_sec):
                                return lambda: ent.configure(show="" if ent.cget("show") == "*" else "*")
                            
                            btn_t = ctk.CTkButton(input_frame, text="👁", width=35, command=make_toggle_sec(entry_sec))
                            btn_t.pack(side="left", padx=(5, 0))
                            
                            self.env_entries[field_name] = entry_sec
                        else:
                            entry_std = ctk.CTkEntry(input_frame, placeholder_text=description, width=330)
                            entry_std.insert(0, str(val))
                            entry_std.pack(side="left", fill="x", expand=True)
                            
                            self.env_entries[field_name] = entry_std
                            
                        # Help link URL button if specified in the schema
                        help_url = extra.get("help_url")
                        if help_url:
                            btn_help = ctk.CTkLabel(
                                input_frame, 
                                text="❓", 
                                font=ctk.CTkFont(size=12),
                                text_color=["#1F6AA5", "#3B8ED0"],
                                cursor="hand2"
                            )
                            btn_help.pack(side="left", padx=(8, 0))
                            btn_help.bind("<Button-1>", lambda event, u=help_url: webbrowser.open(u))
                            
                        row_idx += 1
