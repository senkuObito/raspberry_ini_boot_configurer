@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
del *.spec

echo Building Executable...
pyinstaller --noconfirm --onefile --windowed --icon "assets/icon.ico" --name "RaspberryPiBootConfigurer" --add-data "assets/icon.ico;assets" main.py

echo Build Complete!
echo You can find the executable in the 'dist' folder.
pause
