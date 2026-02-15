import os
import shutil
from utils.file_ops import BootConfigManager
from utils.crypto import generate_password_hash

TEST_DIR = "dummy_boot"

def setup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)
    print(f"Created {TEST_DIR}")

def verify_ssh(mgr):
    print("Testing SSH...")
    mgr.create_ssh()
    if os.path.exists(os.path.join(TEST_DIR, "ssh")):
        print("  [PASS] SSH file created")
    else:
        print("  [FAIL] SSH file not created")
    
    mgr.remove_ssh()
    if not os.path.exists(os.path.join(TEST_DIR, "ssh")):
        print("  [PASS] SSH file removed")
    else:
        print("  [FAIL] SSH file not removed")

def verify_user(mgr):
    print("Testing User Conf...")
    user = "pi"
    pw_hash = generate_password_hash("raspberry")
    mgr.write_userconf(user, pw_hash)
    
    parsed_user, parsed_hash = mgr.parse_userconf()
    if parsed_user == user:
        print(f"  [PASS] User '{parsed_user}' parsed correctly")
    else:
        print(f"  [FAIL] User mismatch: {parsed_user}")

def verify_wifi(mgr):
    print("Testing Wi-Fi...")
    networks = [
        {"ssid": "HomeWifi", "psk": "secret123"},
        {"ssid": "GuestWifi", "psk": "guest123"}
    ]
    mgr.write_wpa_supplicant({"country": "US"}, networks)
    
    global_conf, parsed_nets = mgr.parse_wpa_supplicant()
    if len(parsed_nets) == 2:
        print("  [PASS] Correct number of networks parsed")
        if parsed_nets[0]['ssid'] == "HomeWifi":
            print("  [PASS] Network 1 SSID match")
    else:
        print(f"  [FAIL] Expected 2 networks, got {len(parsed_nets)}")

def run_tests():
    setup()
    mgr = BootConfigManager(TEST_DIR)
    
    verify_ssh(mgr)
    verify_user(mgr)
    verify_wifi(mgr)
    
    print("\nTests Completed.")

if __name__ == "__main__":
    run_tests()
