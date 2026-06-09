import os
import sys
import time
import subprocess
from datetime import datetime
from rich.console import Console
import questionary
from src.utils.paths import get_clean_env

console = Console()

_custom_log_path = None
_debug_logging = False

def set_log_path(path: str):
    global _custom_log_path
    _custom_log_path = os.path.abspath(path)
    os.environ["SETUP_LOG_DIR"] = _custom_log_path

def enable_debug_logging():
    global _debug_logging
    _debug_logging = True
    os.environ["DEBUG_LOGGING"] = "true"

def get_log_path() -> str:
    if os.getenv("SETUP_LOG_DIR"):
        base_path = os.getenv("SETUP_LOG_DIR")
    elif _custom_log_path:
        base_path = _custom_log_path
    else:
        # Fallback relative to this file
        base_path = os.path.join(os.path.dirname(__file__), "..", "logs")
    return os.path.abspath(os.path.join(base_path, "setup.log"))

def write_log(message: str, level: str = "INFO", clear: bool = False):
    global _debug_logging
    if os.getenv("DEBUG_LOGGING") == "true":
        _debug_logging = True

    if level == "DEBUG" and not _debug_logging:
        return

    log_path = get_log_path()
    base_path = os.path.dirname(log_path)

    if clear and os.path.exists(log_path):
        try:
            os.remove(log_path)
        except OSError:
            pass

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"

    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    # Retry write if file is locked
    for _ in range(3):
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
            break
        except OSError:
            time.sleep(0.1)

    if level != "TRACE":
        if level == "INFO":
            console.print(message, style="white")
        elif level == "WARN":
            console.print(message, style="yellow")
        elif level == "ERROR":
            console.print(message, style="bold red")
        elif level == "DEBUG":
            console.print(f"[DEBUG] {message}", style="grey50")

def write_step(message: str, level: str = "INFO"):
    write_log(f">> {message}", level=level)

def invoke_external_command(command: str, description: str = "Executing command", cwd: str = None):
    write_log(f"{description}: {command}", level="TRACE")
    prefix = "    | "
    
    # Run shell execution on all OSes to handle single command string correctly
    use_shell = True
    
    try:
        # Stream output line-by-line to prevent subprocess pipe deadlock
        process = subprocess.Popen(
            command,
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
