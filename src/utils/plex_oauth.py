import requests
import time
import webbrowser
import platform
from src.utils.logger import write_log, console, write_step

CLIENT_ID = "DockerSetup-MediaStack-Orchestration-Client"

def request_plex_token(is_gui=False, progress_callback=None) -> str:
    """
    Implements Plex PIN flow authentication.
    Returns the authToken string if successful, or None.
    """
    headers = {
        "Accept": "application/json",
        "X-Plex-Client-Identifier": CLIENT_ID,
        "X-Plex-Product": "DockerSetup",
        "X-Plex-Version": "1.0",
        "X-Plex-Device": platform.node() or "HomeServer"
    }

    try:
        # 1. Request a PIN code from Plex API
        res = requests.post("https://plex.tv/api/v2/pins", headers=headers, timeout=10)
        res.raise_for_status()
        pin_data = res.json()
        
        pin_id = pin_data.get("id")
        code = pin_data.get("code")
        
        if not pin_id or not code:
            write_log("Failed to get PIN ID or Code from Plex API", level="ERROR")
            return None
            
        auth_url = f"https://app.plex.tv/auth#?clientID={CLIENT_ID}&code={code}&context%5Bdevice%5D%5Bproduct%5D=DockerSetup"
        
        console.print("\n==========================================", style="cyan")
        console.print("             PLEX AUTHENTICATION", style="cyan")
        console.print("==========================================", style="cyan")
        console.print(f"1. Open your browser and sign in to Plex.")
        console.print(f"2. Go to: [link={auth_url}]{auth_url}[/link]", style="yellow")
        console.print(f"3. Or enter this code on https://plex.tv/link : [bold green]{code}[/bold green]\n")
        console.print("Waiting for authentication approval...", style="grey50")
        
        # Try to open browser automatically
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass
            
        # 2. Poll Plex API for the token
        timeout = 180
        start_time = time.time()
        poll_interval = 5
        
        while (time.time() - start_time) < timeout:
            if progress_callback:
                progress_callback(f"Waiting for Plex link: {code} ({int(timeout - (time.time() - start_time))}s remaining)")
                
            poll_res = requests.get(f"https://plex.tv/api/v2/pins/{pin_id}", headers=headers, timeout=10)
            if poll_res.status_code == 200:
                poll_data = poll_res.json()
                auth_token = poll_data.get("authToken")
                if auth_token:
                    console.print("[✓] Plex Account Linked Successfully!", style="green")
                    write_log("Successfully retrieved Plex authToken via PIN link flow.", level="INFO")
                    return auth_token
                    
            time.sleep(poll_interval)
            
        console.print("[!] Plex Auth Link Timeout.", style="red")
        write_log("Plex auth link flow timed out.", level="WARN")
        return None
        
    except Exception as e:
        write_log(f"Plex OAuth link API error: {str(e)}", level="ERROR")
        return None
