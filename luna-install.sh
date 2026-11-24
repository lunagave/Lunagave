#!/usr/bin/env bash
# Luna Beta 1.0-beta - instalador facil, como un programa
# Uso: curl -fsSL <link> | bash
# El enlace solo pide el comando. La contraseña NO se escribe en
# terminal: va por pkexec, la ventanita gráfica del sistema
# (una sola vez). Si no hay pkexec, cae a sudo y lo dice.
set -e
if command -v pkexec >/dev/null 2>&1; then
  pkexec pacman -S --needed --noconfirm zenity tk python-pillow || sudo pacman -S --needed --noconfirm zenity tk python-pillow
else
  sudo pacman -S --needed --noconfirm zenity tk python-pillow
fi
mkdir -p /tmp/luna-install
cd /tmp/luna-install
# NOTA: este enlace es el del zip luna-launcher3.zip, el último subido y aprobado.
# Cuando Fernando apruebe la subida del zip nuevo luna-1.0-beta.zip,
# actualizar esta URL al enlace nuevo de luna-1.0-beta.zip.
curl -L https://muse.ai/files/1462504743611334/3672498159581581/q9gw9plvylr6d5n7x3ghxm9p/luna-launcher3.zip -o luna-launcher3.zip
unzip -o luna-launcher3.zip
# Compilar sin instalar (makepkg sin -i no pide sudo) y luego
# instalar el paquete con pkexec (ventanita gráfica).
makepkg --noconfirm
PAQUETE=$(ls luna-*.pkg.tar.zst | sort | tail -n 1)
if command -v pkexec >/dev/null 2>&1; then
  pkexec pacman -U --noconfirm "$PAQUETE" || sudo pacman -U --noconfirm "$PAQUETE"
else
  sudo pacman -U --noconfirm "$PAQUETE"
fi
bash luna-installer.sh
cd ~
rm -rf /tmp/luna-install
echo "Luna instalada. Abrela en Utilidades o con: luna-gui"
