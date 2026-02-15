# Raspberry Pi Boot Configurer

A modern, user-friendly GUI tool for configuring Raspberry Pi boot files (`ssh`, `wpa_supplicant.conf`, `userconf.txt`, etc.) directly from your Windows PC.

![Application Icon](assets/icon.ico)

## 📥 Download & Run

**No installation required!**

1.  **Download**: Go to the [Releases Page](../../releases) and download the latest `RaspberryPiBootConfigurer.exe`.
2.  **Run**: Double-click the downloaded `.exe` file.
3.  **Enjoy**: The application will launch immediately.

*> **Note**: Windows Defender might verify the file since it's a new application. Click "Run anyway" if prompted.*

---

## ✨ Features

### 📂 Automatic File Detection
Automatically scans your SD card's `boot` partition for existing configuration files.

### 🔐 SSH Management
Enable or disable headless SSH access with a single toggle. No more creating empty files manually!

### 📶 Wi-Fi Configuration
- **Import from PC**: Automatically scan and import your saved Windows Wi-Fi profiles.
- **Select Networks**: Choose exactly which networks to add from a checklist.
- **Priority Management**: Reorder networks (Up/Down) to set connection priority.
- **Advanced Settings**: Configure Country Code and Ctrl Interface details.

### 👤 User Configuration
- **Secure Setup**: Set up your default user (e.g., `pi`) with a secure password.
- **Linux Standard**: Passwords are hashed using **SHA-512**, ensuring compatibility and security.

### 🛠️ Network Config (Advanced)
A built-in editor for Ubuntu's `network-config` (YAML) for advanced static IP setups.

---

## 🏗️ For Developers (Build from Source)

If you want to modify the code or build it yourself:

### Requirements
- Python 3.x
- `customtkinter`
- `passlib`
- `Pillow`
- `PyYAML`
- `pyinstaller` (for building exe)

### Installation
1.  Clone the repo:
    ```bash
    git clone https://github.com/yourusername/raspberry-pi-boot-configurer.git
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    python main.py
    ```

### Building the Executable
You can build the `.exe` using the included script or GitHub Actions.

**Option 1: Local Build**
Run `build_exe.bat` in the terminal. The output will be in `dist/`.

**Option 2: GitHub Actions**
Fork the repo and push changes. Go to "Actions" to download the build artifact, or create a Release to have it automatically attached.

## License
MIT License
