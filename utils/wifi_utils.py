import subprocess
import re

def get_windows_wifi_profiles():
    """Retrieves saved Wi-Fi profiles and passwords from Windows using netsh."""
    profiles_data = []
    try:
        # Get list of profiles
        output = subprocess.check_output("netsh wlan show profiles", shell=True).decode("utf-8", errors="ignore")
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", output)
        
        for profile in profiles:
            profile_name = profile.strip()
            try:
                # Get password for each profile
                profile_info = subprocess.check_output(f'netsh wlan show profile name="{profile_name}" key=clear', shell=True).decode("utf-8", errors="ignore")
                password_match = re.search(r"Key Content\s*:\s*(.*)", profile_info)
                
                if password_match:
                    password = password_match.group(1).strip()
                    profiles_data.append({"ssid": profile_name, "psk": password})
            except subprocess.CalledProcessError:
                continue # Skip if cant get details for some reason
                
    except subprocess.CalledProcessError:
        return []
        
    return profiles_data
