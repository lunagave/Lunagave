#!/usr/bin/env bash
# Luna - instalador universal desde cero
# Detecta Arch (pacman) o Debian/Ubuntu (.deb / apt) e instala Luna.
# Uso: sudo ./install.sh   |   ./install.sh --user
set -e
APP="luna"
VERSION="1.0-beta"

detect_distro() {
  if [ -f /etc/os-release ]; then . /etc/os-release; echo "$ID"; else echo "unknown"; fi
}

install_deps_arch() {
  echo "[Luna] Arch detectado, instalando con pacman..."
  sudo pacman -Sy --noconfirm mpv python python-pip xwinwrap 2>/dev/null || sudo pacman -Sy --noconfirm mpv python
  # mpvpaper está en AUR; si yay/paru existe, úsalo, si no, avisa
  if command -v yay >/dev/null 2>&1; then yay -S --noconfirm mpvpaper
  elif command -v paru >/dev/null 2>&1; then paru -S --noconfirm mpvpaper
  else echo "[Luna] mpvpaper no está en repos oficiales. Instala un AUR helper (yay/paru) o usa: yay -S mpvpaper"
  fi
}

install_deps_debian() {
  echo "[Luna] Debian/Ubuntu detectado, instalando con apt..."
  sudo apt update
  sudo apt install -y mpv python3 python3-pip xwinwrap 2>/dev/null || sudo apt install -y mpv python3
  echo "[Luna] Para Wayland, instala mpvpaper manualmente: https://github.com/GhostNaN/mpvpaper"
}

install_files() {
  echo "[Luna] Copiando archivos..."
  sudo install -Dm755 luna.py /usr/local/bin/luna
  sudo install -Dm644 luna.desktop /usr/share/applications/luna.desktop
  sudo install -Dm644 luna.service /usr/lib/systemd/user/luna.service 2>/dev/null || sudo install -Dm644 luna.service /etc/systemd/user/luna.service
  mkdir -p "$HOME/Videos/Luna" "$HOME/.config/luna"
  echo "[Luna] Listo. Prueba: luna set ~/Videos/Luna/tu-video.mp4"
  echo "[Luna] Para autostart: systemctl --user enable --now luna"
}

DISTRO=$(detect_distro)
case "$DISTRO" in
  arch|manjaro|endeavouros) install_deps_arch ;;
  debian|ubuntu|linuxmint|pop) install_deps_debian ;;
  *) echo "Distro no detectada ($DISTRO). Instala mpv y python3 manualmente y sigue con install_files." ;;
esac
install_files
