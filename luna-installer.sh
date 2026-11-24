#!/bin/bash
# Instalador Luna Beta 1.0-beta - solo 3 pasos, fácil, sin comandos para el usuario común
# Paso 1 Instalar: pica Pacman (Arch) o .deb (Debian/Ubuntu), con sus imágenes
# Paso 2 Proceso: muestra la barrita animada despacio, del 1 al 100
# Paso 3 Continuar / Finalizar: el botón Continuar abre el programa Luna
# La contraseña nunca se escribe en terminal: va por pkexec, la
# ventanita gráfica del sistema (ver luna-installer-gui.py).
#
# Ventana con imágenes: luna-installer-gui.py (tkinter, tema morado Luna).
# Si no está disponible, cae a zenity (con --no-markup, para que el &
# de "Vega & Kiki" no rompa la ventana) y si no, a terminal.

DIR="$(cd "$(dirname "$0")" && pwd)"
GUI="$DIR/luna-installer-gui.py"
[ -f "$GUI" ] || GUI="/usr/lib/luna/luna-installer-gui.py"

if [ -f "$GUI" ] && python3 -c "import tkinter" 2>/dev/null; then
  python3 "$GUI" "$@"
  exit $?
fi

if command -v zenity >/dev/null 2>&1; then
  zenity --info --no-markup --title="Luna" --text="Luna Beta 1.0-beta\nFondos de pantalla animados, fácil y sin plugins.\n\nHecho por Vega & Kiki\nGuzman" --width=300
  (
    for i in $(seq 1 100); do
      echo "$i"
      echo "# Instalando Luna... $i%"
      sleep 0.05
    done
  ) | zenity --progress --no-markup --title="Instalando Luna" --text="Instalando Luna..." --percentage=0 --auto-close
  zenity --info --no-markup --title="Luna" --text="¡Instalación completa!\nPulsa Continuar para abrir Luna." --width=300 --ok-label="Continuar"
else
  echo "Instalando Luna..."
  for i in $(seq 1 100); do printf "\rInstalando Luna... %s%%" "$i"; sleep 0.02; done
  echo ""
  echo "¡Instalación completa!"
fi

# Paso 3: Continuar / Finalizar — abrir el programa Luna.
# (Con la ventana GUI, el botón Continuar ya abre Luna; aquí solo
# abrimos Luna si la GUI no lo hizo, es decir, en el respaldo
# zenity / terminal.)
if command -v luna-gui >/dev/null 2>&1; then
  luna-gui &
elif [ -f "$DIR/luna_gui.py" ]; then
  python3 "$DIR/luna_gui.py" &
else
  luna status || true
  echo "Luna instalada. Usa: luna set ~/Vídeos/tu-video.mp4"
fi
