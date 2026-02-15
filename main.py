import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from utils.file_ops import BootConfigManager
from utils.crypto import generate_password_hash
from utils.wifi_utils import get_windows_wifi_profiles

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set App User Model ID
        myappid = 'com.surya.raspberrypi.bootconfigurer.1.0' 
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

        self.title("Raspberry Pi Boot Configurer")
        self.geometry("800x600")

        # Set Icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon error: {e}")

        self.boot_manager = BootConfigManager()
        self.current_boot_path = None

        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.path_label = ctk.CTkLabel(self.header_frame, text="No Boot Folder Selected", font=("Arial", 14))
        self.path_label.pack(side="left", padx=20)

        self.select_btn = ctk.CTkButton(self.header_frame, text="Select Boot Folder", command=self.select_folder)
        self.select_btn.pack(side="right", padx=20, pady=10)

        # Dashboard Frame
        self.dashboard_frame = ctk.CTkScrollableFrame(self, label_text="Configuration Dashboard")
        self.dashboard_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.dashboard_frame.grid_columnconfigure(1, weight=1)

        # Config Items (Key, Display Name)
        self.config_items = [
            ("ssh", "SSH Enable"),
            ("wpa_supplicant", "Wi-Fi Configuration"),
            ("userconf", "User Configuration"),
            ("network_config", "Network Config (Ubuntu)")
        ]
        
        self.status_widgets = {}
        self.create_dashboard_items()
        
        self.center_window(800, 600)

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.current_boot_path = folder_selected
            self.path_label.configure(text=folder_selected)
            self.boot_manager.boot_path = folder_selected  # Update manager path
            self.refresh_dashboard()

    def create_dashboard_items(self):
        """Creates the initial dashboard rows."""
        for i, (key, name) in enumerate(self.config_items):
            # Label
            label = ctk.CTkLabel(self.dashboard_frame, text=name, font=("Arial", 16, "bold"))
            label.grid(row=i, column=0, padx=20, pady=20, sticky="w")

            # Status Indicator
            status_lbl = ctk.CTkLabel(self.dashboard_frame, text="Waiting...", text_color="gray")
            status_lbl.grid(row=i, column=1, padx=20, pady=20)

            # Action Button
            action_btn = ctk.CTkButton(self.dashboard_frame, text="Configure", state="disabled")
            action_btn.grid(row=i, column=2, padx=20, pady=20)
            
            # Store references
            self.status_widgets[key] = {
                "status_lbl": status_lbl,
                "action_btn": action_btn,
                "row": i
            }

    def refresh_dashboard(self):
        """Checks file status and updates the UI."""
        if not self.current_boot_path:
            return

        status = self.boot_manager.check_files_status()
        
        for key, exists in status.items():
            widgets = self.status_widgets.get(key)
            if not widgets:
                continue

            if exists:
                widgets["status_lbl"].configure(text="Available", text_color="green")
                widgets["action_btn"].configure(text="Edit", state="normal", fg_color="#2CC985", hover_color="#229A65")
            else:
                widgets["status_lbl"].configure(text="Missing", text_color="red")
                widgets["action_btn"].configure(text="Create", state="normal", fg_color="#3B8ED0", hover_color="#36719F")
                
            # Bind command with current key
            widgets["action_btn"].configure(command=lambda k=key: self.open_config_dialog(k))

    def open_config_dialog(self, key):
        """Opens the appropriate configuration dialog."""
        # Placeholder for now
        print(f"Opening dialog for {key}")
        if key == "ssh":
            self.open_ssh_dialog()
        elif key == "wpa_supplicant":
            self.open_wifi_dialog()
        elif key == "userconf":
            self.open_user_dialog()
        elif key == "network_config":
            self.open_network_config_dialog()

    # --- Dialog Placeholders ---
    def open_ssh_dialog(self):
        SSHDialog(self, self.boot_manager)

    def open_wifi_dialog(self):
        WiFiDialog(self, self.boot_manager)

    def open_user_dialog(self):
        UserDialog(self, self.boot_manager)

    def open_network_config_dialog(self):
        NetworkConfigDialog(self, self.boot_manager)


    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

class SSHDialog(ctk.CTkToplevel):
    def __init__(self, parent, boot_manager):
        super().__init__(parent)
        self.boot_manager = boot_manager
        self.title("SSH Configuration")
        self.transient(parent)
        self.grab_set()
        self.center_window(400, 200)
        self.set_dialog_icon()
        
        self.label = ctk.CTkLabel(self, text="Enable SSH on Boot", font=("Arial", 16))
        self.label.pack(pady=20)

        self.ssh_var = ctk.BooleanVar(value=self.boot_manager.check_files_status().get('ssh', False))
        
        self.switch = ctk.CTkSwitch(self, text="Enable SSH", variable=self.ssh_var, onvalue=True, offvalue=False)
        self.switch.pack(pady=10)

        self.save_btn = ctk.CTkButton(self, text="Save", command=self.save)
        self.save_btn.pack(pady=20)

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def set_dialog_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.after(200, lambda: self.iconbitmap(icon_path))

    def save(self):
        if self.ssh_var.get():
            self.boot_manager.create_ssh()
            messagebox.showinfo("Success", "SSH Enabled!")
        else:
            self.boot_manager.remove_ssh()
            messagebox.showinfo("Success", "SSH Disabled!")
        self.master.refresh_dashboard()
        self.destroy()


class UserDialog(ctk.CTkToplevel):
    def __init__(self, parent, boot_manager):
        super().__init__(parent)
        self.boot_manager = boot_manager
        self.title("User Configuration")
        self.transient(parent)
        self.grab_set()
        self.center_window(400, 400)
        self.set_dialog_icon()

    def set_dialog_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.after(200, lambda: self.iconbitmap(icon_path))

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.current_user, self.current_hash = self.boot_manager.parse_userconf()
        self.is_new = self.current_user is None

        ctk.CTkLabel(self, text="Username:").pack(pady=(20, 5))
        self.user_entry = ctk.CTkEntry(self)
        self.user_entry.pack(pady=5)
        
        if self.current_user:
            self.user_entry.insert(0, self.current_user)
        else:
            self.user_entry.insert(0, "pi")

        ctk.CTkLabel(self, text="Password:").pack(pady=(10, 5))
        self.pass_entry = ctk.CTkEntry(self, show="*")
        self.pass_entry.pack(pady=5)
        
        # Helper text
        self.status_lbl = ctk.CTkLabel(self, text="", font=("Arial", 10), text_color="gray")
        self.status_lbl.pack(pady=2)

        if self.current_hash:
            self.pass_entry.insert(0, "********")
            self.pass_entry.configure(state="disabled") # Initially disabled to prevent accidental wipe
            self.status_lbl.configure(text="Existing password is encrypted (Hidden)")
            
            self.lock_var = ctk.BooleanVar(value=True)
            self.lock_chk = ctk.CTkCheckBox(self, text="Change Password", variable=self.lock_var, onvalue=False, offvalue=True, command=self.toggle_lock)
            self.lock_chk.pack(pady=5)
        else:
            self.status_lbl.configure(text="New user configuration")

        self.show_pw_var = ctk.BooleanVar(value=False)
        self.show_pw_chk = ctk.CTkCheckBox(self, text="Show Password", variable=self.show_pw_var, command=self.toggle_password)
        self.show_pw_chk.pack(pady=5)

        self.save_btn = ctk.CTkButton(self, text="Save User", command=self.save)
        self.save_btn.pack(pady=20)

    def toggle_lock(self):
        if not self.lock_var.get(): # User wants to change password
             self.pass_entry.configure(state="normal")
             self.pass_entry.delete(0, "end")
             self.status_lbl.configure(text="Enter new password")
        else: # Revert
             self.pass_entry.delete(0, "end")
             self.pass_entry.insert(0, "********")
             self.pass_entry.configure(state="disabled")
             self.status_lbl.configure(text="Existing password is encrypted (Hidden)")

    def toggle_password(self):
        if self.show_pw_var.get():
            self.pass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")

    def save(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if not username:
             messagebox.showerror("Error", "Username is required!")
             return

        # If locked/disabled, use existing hash
        if self.current_hash and (self.pass_entry.cget("state") == "disabled" or password == "********"):
             self.boot_manager.write_userconf(username, self.current_hash)
             messagebox.showinfo("Success", f"User updated (Password unchanged)!")
        else:
             if not password:
                 messagebox.showerror("Error", "Password is required!")
                 return
             hashed_pw = generate_password_hash(password)
             self.boot_manager.write_userconf(username, hashed_pw)
             messagebox.showinfo("Success", f"User '{username}' configured!")
        
        self.master.refresh_dashboard()
        self.destroy()


class WiFiDialog(ctk.CTkToplevel):
    def __init__(self, parent, boot_manager):
        super().__init__(parent)
        self.boot_manager = boot_manager
        self.title("Wi-Fi Configuration")
        self.transient(parent)
        self.grab_set()
        self.center_window(600, 600)
        self.set_dialog_icon()

    def set_dialog_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.after(200, lambda: self.iconbitmap(icon_path))

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.global_config, self.networks = self.boot_manager.parse_wpa_supplicant()
        
        # --- Global Configuration ---
        self.global_frame = ctk.CTkFrame(self)
        self.global_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(self.global_frame, text="Global Settings", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=2)
        
        # Country
        ctk.CTkLabel(self.global_frame, text="Country Code:").pack(side="left", padx=5)
        self.country_entry = ctk.CTkEntry(self.global_frame, width=50)
        self.country_entry.insert(0, self.global_config.get("country", "US"))
        self.country_entry.pack(side="left", padx=5)

        # Ctrl Interface Group
        ctk.CTkLabel(self.global_frame, text="Group:").pack(side="left", padx=5)
        self.group_entry = ctk.CTkEntry(self.global_frame, width=80)
        self.group_entry.insert(0, self.global_config.get("ctrl_interface_group", "netdev"))
        self.group_entry.pack(side="left", padx=5)
        
        # Ctrl Interface Dir (Full row mostly)
        self.dir_frame = ctk.CTkFrame(self)
        self.dir_frame.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(self.dir_frame, text="Ctrl Interface Dir:").pack(side="left", padx=5)
        self.dir_entry = ctk.CTkEntry(self.dir_frame, width=300)
        self.dir_entry.insert(0, self.global_config.get("ctrl_interface_dir", "/var/run/wpa_supplicant"))
        self.dir_entry.pack(side="left", padx=5)


        # --- Networks Header ---
        self.header = ctk.CTkFrame(self)
        self.header.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(self.header, text="Wi-Fi Networks", font=("Arial", 14, "bold")).pack(side="left")
        
        self.btn_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.btn_frame.pack(side="right")
        
        ctk.CTkButton(self.btn_frame, text="Import from PC", width=100, command=self.import_windows_wifi).pack(side="left", padx=5)
        ctk.CTkButton(self.btn_frame, text="+ Add", width=80, command=self.add_network_dialog).pack(side="left", padx=5)

        # Network List
        self.net_frame = ctk.CTkScrollableFrame(self)
        self.net_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.refresh_list()

        # Save Button
        self.save_btn = ctk.CTkButton(self, text="Save Configuration", command=self.save)
        self.save_btn.pack(pady=10)

    def refresh_list(self):
        for widget in self.net_frame.winfo_children():
            widget.destroy()

        # Sort by priority (descending if possible, but just listing is fine. User interprets priority)
        # However, to be helpful, let's sort purely for display? 
        # Actually user wants to change priority, so showing it is important.
        
        for i, net in enumerate(self.networks):
            f = ctk.CTkFrame(self.net_frame)
            f.pack(fill="x", pady=2)
            
            # Priority is now implicit by order (Top = Highest)
            # We can still show it if it exists in the dict, but we will overwrite it on save
            ctk.CTkLabel(f, text=f"{i+1}. SSID: {net['ssid']}").pack(side="left", padx=10)
            
            # Action Buttons
            btn_box = ctk.CTkFrame(f, fg_color="transparent")
            btn_box.pack(side="right", padx=5)
            
            # Reorder Buttons
            if i > 0:
                ctk.CTkButton(btn_box, text="⬆", width=30, command=lambda idx=i: self.move_up(idx)).pack(side="left", padx=2)
            if i < len(self.networks) - 1:
                ctk.CTkButton(btn_box, text="⬇", width=30, command=lambda idx=i: self.move_down(idx)).pack(side="left", padx=2)

            ctk.CTkButton(btn_box, text="Edit", width=60, command=lambda n=net: self.edit_network_dialog(n)).pack(side="left", padx=2)
            ctk.CTkButton(btn_box, text="X", width=30, fg_color="red", command=lambda n=net: self.remove_network(n)).pack(side="left", padx=2)

    def move_up(self, index):
        if index > 0:
            self.networks[index], self.networks[index-1] = self.networks[index-1], self.networks[index]
            self.refresh_list()

    def move_down(self, index):
        if index < len(self.networks) - 1:
            self.networks[index], self.networks[index+1] = self.networks[index+1], self.networks[index]
            self.refresh_list()

    def remove_network(self, network):
        self.networks.remove(network)
        self.refresh_list()

    def import_windows_wifi(self):
        profiles = get_windows_wifi_profiles()
        if not profiles:
            messagebox.showinfo("Import", "No saved Wi-Fi profiles found or could not retrieve passwords.")
            return

        existing_ssids = {n['ssid'] for n in self.networks}
        new_profiles = [p for p in profiles if p['ssid'] not in existing_ssids]

        if not new_profiles:
            messagebox.showinfo("Import", "All Windows Wi-Fi profiles are already in the list.")
            return

        self.open_import_dialog(new_profiles)

    def open_import_dialog(self, profiles):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Networks")
        dialog.transient(self)
        dialog.grab_set()

        # Set Icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            dialog.after(200, lambda: dialog.iconbitmap(icon_path))

        # Center Window Helper
        def center_window(width, height):
            dialog.update_idletasks()
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            dialog.geometry(f"{width}x{height}+{x}+{y}")
        center_window(350, 400)

        ctk.CTkLabel(dialog, text="Select Networks to Import:", font=("Arial", 14, "bold")).pack(pady=10)

        scroll = ctk.CTkScrollableFrame(dialog)
        scroll.pack(fill="both", expand=True, padx=10, pady=5)

        checkboxes = []
        for p in profiles:
            var = ctk.BooleanVar(value=True)
            chk = ctk.CTkCheckBox(scroll, text=p['ssid'], variable=var)
            chk.pack(anchor="w", pady=2, padx=5)
            checkboxes.append((p, var))

        def import_selected():
            count = 0
            for profile, var in checkboxes:
                if var.get():
                    self.networks.append(profile)
                    count += 1
            if count > 0:
                self.refresh_list()
                dialog.destroy()
                messagebox.showinfo("Import", f"Imported {count} networks.")
            else:
                 dialog.destroy()

        ctk.CTkButton(dialog, text="Import Selected", command=import_selected).pack(pady=10)

    def edit_network_dialog(self, network=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Network" if network else "Add Network")
        dialog.transient(self)
        dialog.grab_set()
        
        # Set Icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            dialog.after(200, lambda: dialog.iconbitmap(icon_path))
        
        def center_window(width, height): # Local helper for this inner dialog (or use mixin next time)
            dialog.update_idletasks()
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            dialog.geometry(f"{width}x{height}+{x}+{y}")
        center_window(350, 250)

        ctk.CTkLabel(dialog, text="SSID:").pack(pady=5)
        ssid_entry = ctk.CTkEntry(dialog)
        ssid_entry.pack(pady=5)
        if network: ssid_entry.insert(0, network['ssid'])
        
        ctk.CTkLabel(dialog, text="Password:").pack(pady=5)
        psk_entry = ctk.CTkEntry(dialog, show="*") 
        psk_entry.pack(pady=5)
        if network: psk_entry.insert(0, network['psk'])

        # Show Password toggle
        def toggle_pw():
            if show_pw_var.get(): psk_entry.configure(show="")
            else: psk_entry.configure(show="*")
            
        show_pw_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(dialog, text="Show Password", variable=show_pw_var, command=toggle_pw).pack(pady=5)

        def save_current():
            ssid = ssid_entry.get()
            psk = psk_entry.get()
            
            if ssid and psk:
                net_data = {"ssid": ssid, "psk": psk}
                
                if network: 
                    network.update(net_data)
                else:
                    self.networks.append(net_data)
                self.refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "SSID and Password required")

        ctk.CTkButton(dialog, text="Save", command=save_current).pack(pady=10)

    def add_network_dialog(self):
        self.edit_network_dialog(None)

    def save(self):
        # Update global config from fields
        self.global_config["country"] = self.country_entry.get()
        self.global_config["ctrl_interface_dir"] = self.dir_entry.get()
        self.global_config["ctrl_interface_group"] = self.group_entry.get()
        
        # Update Priorities based on list order
        # Top of list = Highest Priority (e.g. 100, 99, 98...)
        base_priority = 100
        for i, net in enumerate(self.networks):
            net["priority"] = str(base_priority - i)

        self.boot_manager.write_wpa_supplicant(self.global_config, self.networks)
        messagebox.showinfo("Success", "Wi-Fi Configuration Saved!")
        self.master.refresh_dashboard()
        self.destroy()


class NetworkConfigDialog(ctk.CTkToplevel):
    def __init__(self, parent, boot_manager):
        super().__init__(parent)
        self.boot_manager = boot_manager
        self.title("Network Config Editor")
        self.transient(parent)
        self.grab_set()
        self.center_window(600, 500)
        self.set_dialog_icon()

    def set_dialog_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.after(200, lambda: self.iconbitmap(icon_path))

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(self, text="Edit network-config (YAML)", font=("Arial", 14)).pack(pady=10)

        self.text_area = ctk.CTkTextbox(self, width=550, height=350)
        self.text_area.pack(pady=10)

        content = self.boot_manager.read_network_config()
        self.text_area.insert("0.0", content)

        self.save_btn = ctk.CTkButton(self, text="Save Config", command=self.save)
        self.save_btn.pack(pady=10)

    def save(self):
        content = self.text_area.get("0.0", "end-1c")
        self.boot_manager.write_network_config(content)
        messagebox.showinfo("Success", "Network Config Saved!")
        self.master.refresh_dashboard()
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()
