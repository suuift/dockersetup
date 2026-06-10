#!/bin/bash
# DockerSetup Native Linux Installer
# Wraps deployment folder setup and desktop integration with Zenity fallback

INSTALL_DIR="$HOME/.local/share/dockersetup"
BIN_NAME="dockersetup"
DESKTOP_FILE="$HOME/.local/share/applications/dockersetup.desktop"

# Check if display is present and zenity is installed
USE_GUI=0
if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    if command -v zenity >/dev/null 2>&1; then
        USE_GUI=1
    fi
fi

msg_info() {
    local title="$1"
    local text="$2"
    if [ $USE_GUI -eq 1 ]; then
        zenity --info --title="$title" --text="$text" --width=400
    else
        echo -e "\n=== $title ===\n$text\n"
    fi
}

msg_confirm() {
    local title="$1"
    local text="$2"
    if [ $USE_GUI -eq 1 ]; then
        zenity --question --title="$title" --text="$text" --width=400
    else
        read -p "$text (y/N): " choice
        case "$choice" in 
            [yY][eE][sS]|[yY]) return 0 ;;
            *) return 1 ;;
        esac
    fi
}

# 1. Welcome and Installation confirmation
if ! msg_confirm "DockerSetup Installer" "Do you want to install DockerSetup to your user directory ($INSTALL_DIR)?"; then
    msg_info "Cancelled" "Installation cancelled by user."
    exit 0
fi

# 2. Check if binary exists in local directory
if [ ! -f "./$BIN_NAME" ]; then
    # Try parent or dist folders
    if [ -f "./dist/$BIN_NAME" ]; then
        BIN_PATH="./dist/$BIN_NAME"
    elif [ -f "../dist/$BIN_NAME" ]; then
        BIN_PATH="../dist/$BIN_NAME"
    else
        msg_info "Error" "dockersetup binary not found in working path. Please build it first."
        exit 1
    fi
else
    BIN_PATH="./$BIN_NAME"
fi

# 3. Create install directories
mkdir -p "$INSTALL_DIR"
cp "$BIN_PATH" "$INSTALL_DIR/$BIN_NAME"
chmod +x "$INSTALL_DIR/$BIN_NAME"

# 4. Create Desktop shortcut
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=DockerSetup
Comment=Deploy Media and Home Server stacks using Docker
Exec=x-terminal-emulator -e "$INSTALL_DIR/$BIN_NAME"
Icon=utilities-terminal
Terminal=false
Categories=System;Utility;
EOF
chmod +x "$DESKTOP_FILE"

# 5. Success
msg_info "Success" "DockerSetup has been successfully installed.\n\nYou can launch it from your applications menu or run:\n$INSTALL_DIR/$BIN_NAME"
