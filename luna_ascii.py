#!/usr/bin/env python3
"""Luna en ASCII, estilo shell, en la terminal.

Al correrlo (o al pegarlo) se limpia la pantalla, se ve el
póster de Luna en ASCII, morado sobre fondo negro, y abajo
pregunta:

    ¿Quieres instalar Luna? [S/n]:

Si dices que sí, hace `sudo pacman -S luna` en la terminal
(la contraseña se pide ahí, en la terminal).
Si Luna todavía no está en ningún repo y pacman dice que no
encontró el paquete, lo dice claro y ofrece instalar con
Luna Launcher (makepkg), sin fingir que quedó instalado.
Después de instalar, abre el programa Luna.
"""
import os
import shutil
import subprocess
import sys

MORADO = "\033[95m"
RESET = "\033[0m"
VERSION = "1.0-beta"


def mostrar_poster():
    """Limpia la pantalla y muestra el póster ASCII en morado."""
    os.system("clear")
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "luna_ascii.txt")
    try:
        with open(ruta, encoding="utf-8") as f:
            arte = f.read()
    except FileNotFoundError:
        print("No se encontró luna_ascii.txt junto a este script.")
        return
    # Fondo negro, letras moradas. Solo @ # * + = - : . y espacios.
    print("\033[40m" + MORADO)
    print(arte)
    print(RESET)
    print()
    print("  Bienvenido a Luna")
    print(f"  LUNA Beta {VERSION}")
    print("  Fondos de pantalla animados, fácil y sin plugins.")
    print("  Hecho por Vega & Kiki")
    print("  Guzman")
    print()


def preguntar(texto):
    try:
        return input(texto).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return "n"


def instalar_con_pacman():
    """Intenta `sudo pacman -S luna`. Devuelve True si quedó instalado."""
    if shutil.which("pacman") is None:
        print("No hay pacman en esta computadora.")
        return False
    print()
    print("Instalando Luna con pacman...")
    print("(La contraseña se pide aquí, en la terminal.)")
    print()
    resultado = subprocess.run(["sudo", "pacman", "-S", "luna"])
    if resultado.returncode == 0:
        return True
    print()
    print("pacman no pudo instalar Luna.")
    print("Luna todavía no está en ningún repo: 'no se ha encontrado")
    print("el paquete: luna'. No quedó instalada por pacman.")
    return False


def instalar_con_launcher():
    """Respaldo: instalar con Luna Launcher (makepkg), sin fingir éxito."""
    print()
    print("¿Instalar con Luna Launcher (makepkg)? [S/n]: ", end="")
    if preguntar("") not in ("", "s", "si", "sí", "y"):
        return False
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "luna-install.sh")
    if not os.path.isfile(script):
        print()
        print("No está luna-install.sh aquí. Pide el link de Luna Launcher")
        print("para instalar con el comando único.")
        return False
    print()
    print("Instalando Luna con Luna Launcher...")
    resultado = subprocess.run(["bash", script])
    return resultado.returncode == 0


def abrir_luna():
    if shutil.which("luna-gui"):
        print()
        print("Abriendo Luna...")
        subprocess.run(["luna-gui"])
    else:
        print()
        print("Luna se instaló, pero no se encontró luna-gui para abrirla.")
        print("Prueba con: luna-gui")


def main():
    mostrar_poster()
    respuesta = preguntar("¿Quieres instalar Luna? [S/n]: ")
    if respuesta not in ("", "s", "si", "sí", "y"):
        print("No se instaló Luna.")
        return 0
    instalado = instalar_con_pacman()
    if not instalado:
        instalado = instalar_con_launcher()
    if instalado:
        print()
        print("¡Instalación completa!")
        abrir_luna()
    else:
        print()
        print("Luna no se instaló.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
