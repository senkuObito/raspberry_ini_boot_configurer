import os
import re

class BootConfigManager:
    def __init__(self, boot_path=None):
        self.boot_path = boot_path
        self.files = {
            "ssh": "ssh",
            "wpa_supplicant": "wpa_supplicant.conf",
            "userconf": "userconf.txt",
            "network_config": "network-config"
        }

    def set_boot_path(self, path):
        self.boot_path = path

    def check_files_status(self):
        """Checks if key files exist in the boot directory."""
        status = {}
        if not self.boot_path or not os.path.exists(self.boot_path):
            return {k: False for k in self.files}
        
        for key, filename in self.files.items():
            file_path = os.path.join(self.boot_path, filename)
            status[key] = os.path.exists(file_path)
        return status

    def get_file_path(self, key):
        return os.path.join(self.boot_path, self.files[key])

    # --- SSH ---
    def create_ssh(self):
        """Creates an empty ssh file."""
        with open(self.get_file_path("ssh"), 'w') as f:
            pass

    def remove_ssh(self):
        """Removes the ssh file."""
        path = self.get_file_path("ssh")
        if os.path.exists(path):
            os.remove(path)

    # --- WPA Supplicant ---
    def parse_wpa_supplicant(self):
        """Parses wpa_supplicant.conf and returns (global_config, networks)."""
        path = self.get_file_path("wpa_supplicant")
        defaults = {
            "country": "US",
            "ctrl_interface_dir": "/var/run/wpa_supplicant",
            "ctrl_interface_group": "netdev",
            "update_config": "1"
        }
        networks = []
        
        if not os.path.exists(path):
            return defaults, networks

        with open(path, 'r') as f:
            content = f.read()

        # Parse Globals
        country_match = re.search(r'^country=(.*)$', content, re.MULTILINE)
        if country_match: defaults["country"] = country_match.group(1).strip()

        ctrl_match = re.search(r'^ctrl_interface=(.*)$', content, re.MULTILINE)
        if ctrl_match:
            line = ctrl_match.group(1).strip()
            # Try to extract DIR and GROUP
            dir_match = re.search(r'DIR=(.*?)\s', line + ' ') # Add space to help regex
            group_match = re.search(r'GROUP=(.*?)$', line)
            
            if dir_match: defaults["ctrl_interface_dir"] = dir_match.group(1).strip()
            if group_match: defaults["ctrl_interface_group"] = group_match.group(1).strip()

        # Regex to find network blocks
        network_blocks = re.findall(r'network\s*=\s*{(.*?)}', content, re.DOTALL)
        
        for block in network_blocks:
            ssid_match = re.search(r'ssid\s*=\s*"(.*?)"', block)
            psk_match = re.search(r'psk\s*=\s*"(.*?)"', block)
            priority_match = re.search(r'priority\s*=\s*(\d+)', block)
            
            if ssid_match and psk_match:
                net = {
                    "ssid": ssid_match.group(1),
                    "psk": psk_match.group(1)
                }
                if priority_match:
                    net["priority"] = priority_match.group(1)
                networks.append(net)
        return defaults, networks

    def write_wpa_supplicant(self, config, networks):
        """Writes wpa_supplicant.conf with given config and networks."""
        content = f"""country={config.get('country', 'US')}
ctrl_interface=DIR={config.get('ctrl_interface_dir', '/var/run/wpa_supplicant')} GROUP={config.get('ctrl_interface_group', 'netdev')}
update_config={config.get('update_config', '1')}
"""
        for net in networks:
            priority_line = f"\n    priority={net['priority']}" if 'priority' in net else ""
            content += f"""
network={{
    ssid="{net['ssid']}"
    psk="{net['psk']}"{priority_line}
}}
"""
        with open(self.get_file_path("wpa_supplicant"), 'w', newline='\n') as f:
            f.write(content)

    # --- User Conf ---
    def parse_userconf(self):
        """Parses userconf.txt and returns (username, password_hash)."""
        path = self.get_file_path("userconf")
        if not os.path.exists(path):
            return None, None
        
        with open(path, 'r') as f:
            line = f.readline().strip()
            if ':' in line:
                parts = line.split(':')
                return parts[0], parts[1] if len(parts) > 1 else ""
        return None, None

    def write_userconf(self, username, password_hash):
        """Writes userconf.txt."""
        with open(self.get_file_path("userconf"), 'w', newline='\n') as f:
            f.write(f"{username}:{password_hash}\n")

    # --- Network Config ---
    def read_network_config(self):
        """Reads network-config content."""
        path = self.get_file_path("network_config")
        if not os.path.exists(path):
            return ""
        with open(path, 'r') as f:
            return f.read()

    def write_network_config(self, content):
        """Writes network-config content."""
        with open(self.get_file_path("network_config"), 'w', newline='\n') as f:
            f.write(content)
