import platform
import subprocess
import shutil

def copy_to_clipboard(text: str) -> bool:
    """
    Copies text to the system clipboard across platforms.
    """
    if not text:
        return False
        
    system = platform.system()
    
    # 1. Tkinter clipboard fallback
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.destroy()
        return True
    except Exception:
        pass
        
    # 2. CLI fallbacks
    try:
        if system == "Windows":
            if shutil.which("clip"):
                proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
        elif system == "Linux":
            if shutil.which("xclip"):
                proc = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
            elif shutil.which("xsel"):
                proc = subprocess.Popen(["xsel", "--clipboard", "--input"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
            elif shutil.which("wl-copy"):
                proc = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
        elif system == "Darwin":
            if shutil.which("pbcopy"):
                proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
                proc.communicate(input=text)
                return True
    except Exception:
        pass
        
    return False
