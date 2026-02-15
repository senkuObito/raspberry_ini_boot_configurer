# Raspberry Pi Boot Configurer

A modern, user-friendly GUI tool for configuring Raspberry Pi boot files (`ssh`, `wpa_supplicant.conf`, `userconf.txt`, etc.) directly from your Windows PC. Built with Python and CustomTkinter.

![Application Icon](assets/icon.ico)

## Features

- **File Detection**: Automatically scans your SD card boot partition for existing configuration files.
- **SSH Management**: Enable or disable SSH headless access with a single toggle.
- **Wi-Fi Configuration**:
    - **Add/Edit Networks**: Manually configure SSID and Password.
    - **Import from Windows**: Automatically import saved Wi-Fi profiles from your PC.
    - **Selectable Import**: Choose exactly which networks to import from a list.
    - **Priority Management**: Reorder networks using Up/Down buttons to set connection priority.
    - **Advanced Settings**: Configure Country Code, Control Interface Dir/Group.
- **User Configuration**:
    - Set up the default user (`pi` or custom).
    - **Secure Hashing**: Passwords are hashed using SHA-512 (Linux standard) for security.
    - **Existing Configs**: Detects existing `userconf.txt` and allows password updates.
- **Network Config**: Advanced editor for Ubuntu `network-config` (YAML).
- **Modern UI**: Dark-themed, centered windows, and responsive design using CustomTkinter.

## Installation

1.  **Install Python**:
    Ensure Python 3.x is installed on your system. [Download Python](https://www.python.org/downloads/)

2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/raspberry-pi-boot-configurer.git
    cd raspberry-pi-boot-configurer
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Application**:
    ```bash
    python main.py
    ```

2.  **Select Boot Drive**:
    - Click **"Select Boot Folder"**.
    - Choose the `boot` partition of your SD card (e.g., `D:\`, `E:\`).

3.  **Configure**:
    - **SSH**: Click "Configure" next to SSH Enable and toggle the switch.
    - **Wi-Fi**: Click "Configure" next to Wi-Fi Configuration.
        - Click **Import from PC** to scan for saved networks.
        - Edit or Reorder networks as needed.
        - Click **Save Configuration** when done.
    - **User**: Set up your username and password.

## Building and Releasing

To create a standalone executable (`.exe`) for Windows:

1.  **Run the Build Script**:
    Double-click `build_exe.bat` or run it from the terminal:
    ```bash
    build_exe.bat
    ```
    This script installs `pyinstaller` and builds the executable.

2.  **Locate the Executable**:
    The generated `RaspberryPiBootConfigurer.exe` will be in the `dist/` folder.

3.  **Create a GitHub Release**:
    - Go to your GitHub repository > **Releases** > **Draft a new release**.
    - Tag the release (e.g., `v1.0.0`).
    - Upload `RaspberryPiBootConfigurer.exe` from the `dist/` folder as a binary asset.
    - Publish the release. Users can now download the `.exe` directly.

## Project Structure

- `main.py`: Entry point and GUI implementation.
- `utils/`:
    - `file_ops.py`: Handles reading/writing of boot and config files.
    - `crypto.py`: Handles password hashing.
    - `wifi_utils.py`: Logic for importing Windows Wi-Fi profiles.
    - `icon_generator.py`: Script used to generate the application icon.
- `assets/`: Contains the application icon.

## Requirements

- Python 3.x
- `customtkinter`
- `passlib`
- `Pillow`
- `PyYAML`

## License

MIT License
