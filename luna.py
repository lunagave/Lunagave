#!/usr/bin/env python3
"""
Luna v1.0 beta - fondos de pantalla animados, fácil y sin plugins.
Versión: 1.0-beta (sigue siendo Beta).
Uso:
  luna set <video.mp4|gif|webm>   # pone el fondo animado
  luna stop                       # detiene el fondo
  luna list                       # lista fondos en ~/Videos/Luna
  luna status                     # muestra si está activo
Requiere: mpv + mpvpaper (Wayland) o xwinwrap (X11).
El instalador se encarga de instalarlos según la distro.

Hecho por Vega & Kiki
Guzman
"""
import os, sys, subprocess, shutil
from pathlib import Path

VERSION = "1.0-beta"

WALLPAPERS = Path.home() / "Videos" / "Luna"
CONFIG = Path.home() / ".config" / "luna" / "current.txt"

def run(cmd, check=False):
    return subprocess.run(cmd, check=check, capture_output=True, text=True)

def is_wayland():
    return os.environ.get("XDG_SESSION_TYPE") == "wayland" or "WAYLAND_DISPLAY" in os.environ

def set_wallpaper(path):
    p = Path(path).expanduser().resolve()
    if not p.exists():
        print(f"No existe: {p}")
        return 1
    WALLPAPERS.mkdir(parents=True, exist_ok=True)
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(str(p))
    stop_wallpaper(silent=True)
    if is_wayland():
        if not shutil.which("mpvpaper"):
            print("Falta mpvpaper. Instálalo con el instalador de Luna.")
            return 1
        # mpvpaper -o "loop" <monitor> <video>
        subprocess.Popen(["mpvpaper", "-o", "loop", "*", str(p)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        if not shutil.which("xwinwrap"):
            print("Falta xwinwrap. Instálalo con el instalador de Luna.")
            return 1
        subprocess.Popen(["xwinwrap", "-g", "1920x1080", "-ni", "-s", "-st", "-sp", "-nf",
                          "--", "mpv", "--loop", "-wid", "WID", str(p)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Luna: fondo animado activado: {p.name}")
    return 0

def stop_wallpaper(silent=False):
    for name in ("mpvpaper", "xwinwrap", "mpv"):
        run(["pkill", "-f", name])
    if not silent:
        print("Luna: fondo detenido.")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    if cmd == "version":
        print(f"Luna {VERSION}")
        return 0
    if cmd == "set" and len(sys.argv) >= 3:
        return set_wallpaper(sys.argv[2])
    if cmd == "stop":
        stop_wallpaper()
        return 0
    if cmd == "list":
        WALLPAPERS.mkdir(parents=True, exist_ok=True)
        for f in sorted(WALLPAPERS.iterdir()):
            print(f.name)
        return 0
    if cmd == "status":
        r = run(["pgrep", "-af", "mpvpaper|mpv"])
        print(r.stdout.strip() or "Luna no está activa.")
        return 0
    print(__doc__)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
