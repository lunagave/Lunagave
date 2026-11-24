#!/bin/bash
# Luna Beta 1.0-beta — instalar Luna como un programa, sin archivos sueltos.
#
# Uso:
#   bash luna-instalar-programa.sh
#   bash luna-instalar-programa.sh https://TU-SERVIDOR/luna/luna-1.0_beta-1-any.pkg.tar.zst
#
# Lo que hace, paso a paso:
#   1. Descarga el paquete Luna (.pkg.tar.zst) a una carpeta temporal,
#      NUNCA a ~/Descargas, así no quedan archivos sueltos.
#   2. Lo instala con sudo pacman -U. Pacman pone cada archivo en su
#      lugar: el programa en /usr/bin, la ventana en /usr/bin/luna-gui,
#      la carpeta del programa en /usr/share/luna/, el icono en el menú
#      Utilidades y el clic derecho en KDE.
#   3. Borra la carpeta temporal. No queda nada suelto.
#   4. Abre el instalador con imágenes y luego la ventana de Luna.
#
# Aún no hay servidor público: cambia LUNA_PKG_URL por el enlace real
# cuando se suba el paquete. Sin ese enlace, el script lo dice claro
# y no finge que instaló nada.
set -euo pipefail

VERSION="1.0-beta"
PKG="luna-1.0_beta-1-any.pkg.tar.zst"
# TODO: poner aquí el enlace real cuando el paquete esté en el servidor.
LUNA_PKG_URL="${1:-https://TU-SERVIDOR/luna/arch/${PKG}}"

if [ -z "${LUNA_PKG_URL}" ] || [[ "$LUNA_PKG_URL" == *"TU-SERVIDOR"* ]]; then
  echo "Luna: todavía no hay enlace del paquete publicado."
  echo "Cuando el paquete esté en el servidor, corre:"
  echo "  bash luna-instalar-programa.sh https://TU-SERVIDOR/luna/arch/${PKG}"
  echo "O instala desde el repo, cuando esté publicado:"
  echo "  sudo pacman -S luna"
  exit 1
fi

TMPDIR_LUNA="$(mktemp -d /tmp/luna-instalar.XXXXXX)"
limpiar() { rm -rf "$TMPDIR_LUNA"; }
trap limpiar EXIT

echo "Luna: descargando el paquete a una carpeta temporal..."
curl -fL "$LUNA_PKG_URL" -o "$TMPDIR_LUNA/$PKG"

echo "Luna: instalando como un programa con pacman..."
sudo pacman -U --noconfirm "$TMPDIR_LUNA/$PKG"

echo "Luna: limpiando la carpeta temporal (no queda nada en Descargas)..."
limpiar
trap - EXIT

echo "Luna instalada:"
echo "  Programa:      /usr/bin/luna"
echo "  Ventana:       /usr/bin/luna-gui  (menú Utilidades > Luna)"
echo "  Carpeta:       /usr/share/luna/   (póster e imágenes de diseño)"
echo "  Instalador:    /usr/lib/luna/luna-installer.sh"
echo "  Clic derecho:  Poner con Luna (KDE)"

# Ventana del instalador, y luego la ventana de Luna.
if [ -x /usr/lib/luna/luna-installer.sh ]; then
  bash /usr/lib/luna/luna-installer.sh || true
fi
if command -v luna-gui >/dev/null 2>&1; then
  luna-gui &
fi
echo "Listo. Hecho por Vega & Kiki"
echo "Guzman"
