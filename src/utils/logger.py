import os
import sys
import time
import subprocess
import shutil
from datetime import datetime
from rich.console import Console
import questionary
from src.utils.paths import get_clean_env

console = Console()

import logging

_logger = logging.getLogger("dockersetup")
_logger.setLevel(logging.DEBUG)

_custom_log_path = None
_debug_logging = False
_gui_log_callback = None
_file_handler = None

class GuiLogHandler(logging.Handler):
    def emit(self, record):
        global _gui_log_callback
        if _gui_log_callback:
            try:
                msg = self.format(record)
                _gui_log_callback(msg)
            except Exception:
                pass

def configure_logging():
    global _file_handler, _custom_log_path
    
    # Remove existing handlers to avoid duplicates
    for handler in list(_logger.handlers):
        _logger.removeHandler(handler)
        
    log_path = get_log_path()
    base_path = os.path.dirname(log_path)
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
        
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    try:
        # Resolve directory collision where setup.log might be a folder
        if os.path.exists(log_path) and os.path.isdir(log_path):
            try:
                shutil.rmtree(log_path)
            except OSError:
                pass
        _file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
        _file_handler.setFormatter(formatter)
        _logger.addHandler(_file_handler)
    except OSError:
        pass
        
    gui_handler = GuiLogHandler()
    gui_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    _logger.addHandler(gui_handler)

def set_log_path(path: str):
    global _custom_log_path
    _custom_log_path = os.path.abspath(path)
    os.environ["SETUP_LOG_DIR"] = _custom_log_path
    configure_logging()

def enable_debug_logging():
    global _debug_logging
    _debug_logging = True
    os.environ["DEBUG_LOGGING"] = "true"

def set_gui_log_callback(callback):
    global _gui_log_callback
    _gui_log_callback = callback
    configure_logging()

def get_log_path() -> str:
    if os.getenv("SETUP_LOG_DIR"):
        base_path = os.getenv("SETUP_LOG_DIR")
    elif _custom_log_path:
        base_path = _custom_log_path
    else:
        base_path = os.path.join(os.path.dirname(__file__), "..", "logs")
    return os.path.abspath(os.path.join(base_path, "setup.log"))

def write_log(message: str, level: str = "INFO", clear: bool = False):
    global _debug_logging, _file_handler
    if os.getenv("DEBUG_LOGGING") == "true":
        _debug_logging = True

    log_path = get_log_path()
    
    if clear and os.path.exists(log_path):
        if _file_handler:
            _logger.removeHandler(_file_handler)
            _file_handler.close()
            _file_handler = None
        try:
            if os.path.isdir(log_path):
                shutil.rmtree(log_path)
            else:
                os.remove(log_path)
        except OSError:
            pass
            
    if not _logger.handlers:
        configure_logging()
    elif _file_handler and os.path.abspath(_file_handler.baseFilename) != os.path.abspath(log_path):
        configure_logging()
        
    log_level = logging.INFO
    if level == "DEBUG":
        log_level = logging.DEBUG
    elif level == "WARN":
        log_level = logging.WARNING
    elif level == "ERROR":
        log_level = logging.ERROR
    elif level == "TRACE":
        log_level = logging.DEBUG
        
    _logger.log(log_level, message)

    if level != "TRACE":
        if level == "INFO":
            console.print(message, style="white")
        elif level == "WARN":
            console.print(message, style="yellow")
        elif level == "ERROR":
            console.print(message, style="bold red")
        elif level == "DEBUG" and _debug_logging:
            console.print(f"[DEBUG] {message}", style="grey50")

def write_step(message: str, level: str = "INFO"):
    write_log(f">> {message}", level=level)

def invoke_external_command(command, description: str = "Executing command", cwd: str = None):
    import shlex
    import platform
    
    # Secure command execution: support both list-based command representation and strings
    if isinstance(command, list):
        cmd_list = command
        cmd_str_for_log = " ".join(command)
        use_shell = False
    else:
        cmd_str_for_log = command
        # shlex.split on POSIX systems safely handles string parameters/quoting
        if platform.system() != "Windows":
            try:
                cmd_list = shlex.split(command)
                use_shell = False
            except Exception:
                cmd_list = command
                use_shell = True
        else:
            # On Windows, list split is less reliable for cmd/powershell execution. Use shell for raw strings.
            cmd_list = command
            use_shell = True

    write_log(f"{description}: {cmd_str_for_log}", level="TRACE")
    prefix = "    | "
    
    try:
        # Stream output line-by-line to prevent subprocess pipe deadlock
        process = subprocess.Popen(
            cmd_list,
            shell=use_shell,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=get_clean_env()
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line_str = line.strip()
                write_log(line_str, level="TRACE")
                
                is_error = any(x in line_str.lower() for x in ["error", "failed", "conflict", "denied", "fatal", "critical"])
                
                if _debug_logging:
                    if is_error:
                        console.print(f"{prefix}{line_str}", style="red")
                    else:
                        console.print(f"{prefix}{line_str}", style="grey50")
                elif is_error:
                    console.print(f"{prefix}{line_str}", style="red")
        
        returncode = process.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, command)
            
    except Exception as e:
        write_log(f"External Command Failed: {str(e)}", level="ERROR")
        raise e

def safe_confirm(message: str, default: bool = True) -> bool:
    """
    Prompt the user with a Yes/No select list to force pressing Enter to confirm.
    """
    if os.getenv("DS_HEADLESS") == "true":
        return default
        
    choices = ["Yes", "No"] if default else ["No", "Yes"]
    choice = questionary.select(
        message,
        choices=choices,
        default=choices[0]
    ).ask()
    return choice == "Yes"
