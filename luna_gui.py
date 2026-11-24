#!/usr/bin/env python3
"""
Luna Beta 1.0-beta — ventana del programa.
Fondos de pantalla animados, fácil y sin plugins.

Estilo como el picker de Wayland Wallpaper Engine
(https://bhuwanjoshi-01.github.io/wayland-wallpaperengine/):
una barra superior con miniaturas, búsqueda, volumen, un botón
de fondo aleatorio y un enlace — pero para Luna, con tus fondos
locales, sin Steam ni Workshop.

Selector como en las fotos que mandó Fernando, pero SOLO carrusel:
- Carrusel 3D tipo cover-flow, grande y cool: la imagen del centro
  grande y de frente, las de los lados más pequeñas, inclinadas y
  más oscuras, sobre fondo negro. Es el único selector: NO hay
  cuadrícula de tarjetas, NO hay Biblioteca y NO hay Vista previa.
- Debajo del carrusel va el nombre del fondo elegido y el botón
  grande Poner Imagen en el Fondo de Pantalla.
- Teclado: flechas ← → mueven la selección, Enter confirma y pone
  el fondo, doble clic aplica, F5 refresca el carrusel,
  Ctrl+W cierra la ventana.
- Escena, web y video en el original; en Luna, imágenes y videos
  locales (JPG, PNG, WEBP, GIF, BMP, SVG / MP4, MKV, WEBM, MOV, AVI).
  NO hay función de video de YouTube ni página web como fondo:
  Hidamari es solo una comparación, Fernando dijo que no se añada.
- Sonido solo en el escritorio: el fondo suena mientras el
  escritorio tiene el foco y se silencia al cambiar a una app.
- Se detiene al trabajar: en cuanto una ventana tiene el foco, el
  video se congela y no usa CPU/GPU hasta volver al escritorio.
  Igual que `wwe config pause=fullscreen`, en Ajustes se puede
  elegir pausar solo con apps a pantalla completa o juegos.

Tema Luna: morado oscuro como el póster del gatito en la luna,
nada de gris estilo Windows 98. Botones modernos morados, grandes,
con icono + texto, con efecto al pasar el ratón, texto blanco y el
póster de bienvenida en la cabecera.

Iconos: glifos Unicode que trae el sistema (DejaVu / Noto Symbols /
Noto Color Emoji), sin descargar paquetes externos. Cada botón
principal lleva su icono: ➕ agregar, 📁 carpeta, 🗑 quitar,
⚙ ajustes, 🖼 poner fondo, 🎲 aleatorio, 🔊/🔇 sonido,
🔍 buscar, ✨ funciones, 💾 guardar, ✕ cerrar, ⏸/▶ congelar.
El icono Acerca es el gatito negro dibujado con "?" (sin emoji).

Uso en Garuda:
  python3 luna_gui.py
  o, una vez instalado el paquete: luna-gui
  o desde el menú Utilidades: Luna

Solo usa tkinter (biblioteca estándar de Python) + PIL (Pillow)
cuando está disponible; si PIL no está, la ventana sigue
funcionando con los botones de texto de antes.

Selector de archivos moderno: "Agregar Carpeta" y "Agregar Fondo"
no usan el diálogo viejo de tkinter. Primero prueban el selector
moderno del sistema — zenity (GtkFileChooser) y luego kdialog
(KDE, el de Garuda) — y solo si ninguno está instalado caen al
filedialog de tkinter. En Garuda zenity ya es dependencia de Luna.

Acerca de Luna abre su propia ventana aparte (no dentro de Ajustes):
póster de bienvenida recortado (sin la franja de abajo con los
logos de Pacman Arch y .deb Debian Ubuntu), Luna Beta 1.0-beta
y Hecho por Vega & Kiki. El póster se muestra grande y el texto
con ajuste de línea, para que nada se corte por la derecha.

Funciones de Luna (Paso 4) vive DENTRO de Acerca, como submenú
(pestaña "Funciones"), con la lista de funciones del programa
sacada de PAGINA_LUNA.md. La ventana antigua de imágenes
archivadas se quitó por completo, igual que su botón.

Hecho por Vega & Kiki
Guzman
"""
import json
import os
import random
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except Exception:
    Image = None
    ImageTk = None
    PIL_DISPONIBLE = False

VERSION = "1.0-beta"
BASE_DIR = Path(__file__).resolve().parent

# --- Tema Luna: morado del póster, fondo oscuro, nada gris viejo ---
FONDO = "#1e1033"          # morado muy oscuro, fondo principal
FONDO_BARRA = "#2a1745"    # cabecera
FONDO_TARJETA = "#2d1b4e"  # tarjetas / vista previa / carrusel
FONDO_TARJETA2 = "#3b2560" # tarjetas secundarias
MORADO = "#7c3aed"         # botón principal
MORADO_HOVER = "#8b5cf6"
MORADO_CLARO = "#a78bfa"   # acento / borde del seleccionado
AZUL_SELECCION = "#38bdf8"  # borde azul brillante de la tarjeta elegida
FONDO_COVER = "#000000"     # fondo negro del carrusel 3D, como en la foto
TEXTO = "#ffffff"
TEXTO_SUAVE = "#d8b4fe"    # lila claro para subtítulos
VERDE = "#22c55e"
BORDE = "#6d28d9"
FUENTE = "sans-serif"


def aplicar_tema(ventana):
    """Aplica el tema Luna morado/oscuro a una ventana tkinter."""
    ventana.configure(bg=FONDO)
    try:
        estilo = ttk.Style(ventana)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=FONDO)
        estilo.configure("TLabelframe", background=FONDO_TARJETA,
                         foreground=TEXTO, bordercolor=BORDE)
        estilo.configure("TLabelframe.Label", background=FONDO_TARJETA,
                         foreground=MORADO_CLARO, font=(FUENTE, 11, "bold"))
        estilo.configure("TLabel", background=FONDO, foreground=TEXTO)
        estilo.configure("TCheckbutton", background=FONDO_TARJETA,
                         foreground=TEXTO, font=(FUENTE, 11))
        estilo.map("TCheckbutton", background=[("active", FONDO_TARJETA)])
        estilo.configure("TRadiobutton", background=FONDO_TARJETA,
                         foreground=TEXTO, font=(FUENTE, 11))
        estilo.map("TRadiobutton", background=[("active", FONDO_TARJETA)])
        estilo.configure("TScale", background=FONDO, troughcolor=FONDO_TARJETA2)
        estilo.configure("Horizontal.TScrollbar", background=MORADO,
                         troughcolor=FONDO_TARJETA, arrowcolor=TEXTO)
        estilo.configure("TButton", background=MORADO, foreground=TEXTO,
                         font=(FUENTE, 11, "bold"), borderwidth=0, padding=8)
        estilo.map("TButton", background=[("active", MORADO_HOVER)])
    except Exception:
        pass


def _hover_boton(boton, normal, hover):
    """Efecto moderno al pasar el ratón: cambia el fondo del botón."""
    boton.bind("<Enter>", lambda _e: boton.config(bg=hover))
    boton.bind("<Leave>", lambda _e: boton.config(bg=normal))


def boton_morado(parent, texto, comando, grande=False):
    """Botón moderno Luna: morado, grande, con icono + texto.

    El icono ya viene dentro de `texto` (ej. "🎲 Aleatorio").
    Sin borde gris de Windows 98, con espacio y efecto hover.
    """
    boton = tk.Button(
        parent, text=texto, command=comando,
        bg=MORADO, fg=TEXTO, activebackground=MORADO_HOVER,
        activeforeground=TEXTO, relief="flat", borderwidth=0,
        padx=18, pady=12 if grande else 9,
        font=(FUENTE, 13, "bold") if grande else (FUENTE, 11, "bold"),
        cursor="hand2",
    )
    _hover_boton(boton, MORADO, MORADO_HOVER)
    return boton


def boton_claro(parent, texto, comando):
    """Botón secundario moderno: tarjeta morada oscura, icono + texto."""
    boton = tk.Button(
        parent, text=texto, command=comando,
        bg=FONDO_TARJETA2, fg=TEXTO, activebackground=MORADO,
        activeforeground=TEXTO, relief="flat", borderwidth=0,
        padx=14, pady=9, font=(FUENTE, 11, "bold"), cursor="hand2",
    )
    _hover_boton(boton, FONDO_TARJETA2, MORADO)
    return boton


# Iconos de los botones principales, en un solo lugar.
ICONO_AGREGAR = "➕"
ICONO_CARPETA = "📁"
ICONO_QUITAR = "🗑"
ICONO_AJUSTES = "⚙"
ICONO_ACERCA = "🐱 ?"
ICONO_PONER_FONDO = "🖼"
ICONO_ALEATORIO = "🎲"
ICONO_SONIDO = "🔊"
ICONO_SILENCIO = "🔇"
ICONO_BUSCAR = "🔍"
ICONO_FUNCIONES = "✨"
ICONO_GUARDAR = "💾"
ICONO_CERRAR = "✕"
ICONO_CONGELAR = "⏸"
ICONO_REANUDAR = "▶"


def etiqueta(parent, texto, tamano=11, negrita=False, color=TEXTO, fondo=FONDO):
    return tk.Label(parent, text=texto, bg=fondo, fg=color,
                    font=(FUENTE, tamano, "bold" if negrita else "normal"))


# Póster de bienvenida de Fernando — nombre exacto, verificado con ls.
# El póster mide 1280x1920. La franja de abajo, con los logos de
# Pacman Arch (amarillo) y .deb Debian Ubuntu, empieza cerca del
# 86% de la altura; el texto "Luna es un proyecto..." termina
# cerca del 77%. Por eso el póster se recorta en memoria al 82%
# de su altura (ver cargar_poster_sin_logos): se quita la franja
# de los logos y se conserva todo el texto del póster. El archivo
# original no se toca.
POSTER_BIENVENIDA = "81630_0_1xuc.webp"


def ruta_archivada(nombre_archivo):
    """Devuelve la ruta de una imagen archivada, o None si no existe.

    Orden: primero la carpeta del programa instalado (/usr/share/luna/,
    donde el PKGBUILD pone las 8 imágenes), luego junto al script
    (cuando se corre con python3 luna_gui.py desde workspace/luna/),
    luego el workspace. Sin esto, tras instalar con pacman la GUI
    no encontraba el póster ni las imágenes de diseño, porque el
    script vive en /usr/bin/luna-gui y las imágenes en /usr/share/luna/.
    """
    candidatos = [
        Path("/usr/share/luna") / nombre_archivo,
        BASE_DIR / nombre_archivo,
        Path.home() / "workspace" / "luna" / nombre_archivo,
    ]
    if nombre_archivo == POSTER_BIENVENIDA:
        candidatos += [
            BASE_DIR.parent / "user" / "files" / POSTER_BIENVENIDA,
            Path.home() / "workspace" / "user" / "files" / POSTER_BIENVENIDA,
        ]
    for ruta in candidatos:
        if ruta.is_file():
            return ruta
    return None


def cargar_imagen_tk(ruta, ancho, alto):
    """Carga una imagen (JPG/PNG/WEBP/GIF/BMP) como PhotoImage de tkinter."""
    if not PIL_DISPONIBLE or not ruta:
        return None
    try:
        img = Image.open(str(ruta))
        img.thumbnail((ancho, alto))
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


def miniatura_cover(ruta, ancho, alto, inclinacion=0.0, oscurecer=0.0):
    """Miniatura para el carrusel 3D (cover-flow).

    Devuelve un PhotoImage de tamaño exacto (ancho x alto), con la
    imagen centrada sobre fondo negro. Si `inclinacion` no es 0, la
    imagen se inclina (efecto 3D de las tarjetas de los lados);
    si `oscurecer` es > 0, se oscurece (las de los lados se ven más
    apagadas que la del centro). Para videos y SVG devuelve None:
    la tarjeta muestra un cuadro oscuro con 🎬.
    """
    if not PIL_DISPONIBLE or not ruta:
        return None
    try:
        from PIL import ImageEnhance
        img = Image.open(str(ruta)).convert("RGB")
        img.thumbnail((ancho, alto))
        fondo = Image.new("RGB", (ancho, alto), (0, 0, 0))
        fondo.paste(img, ((ancho - img.width) // 2, (alto - img.height) // 2))
        if inclinacion:
            fondo = fondo.transform(
                fondo.size, Image.AFFINE,
                (1, inclinacion, -inclinacion * alto / 2, 0, 1, 0),
                resample=Image.BICUBIC)
        if oscurecer > 0:
            fondo = ImageEnhance.Brightness(fondo).enhance(max(0.0, 1.0 - oscurecer))
        return ImageTk.PhotoImage(fondo)
    except Exception:
        return None


def cargar_poster_sin_logos(ruta, ancho, alto):
    """Carga el póster de Luna sin la franja de los logos de abajo.

    Recorta el 18% inferior del póster en memoria (se queda el 82%
    superior: LUNA, el gatito en la luna y el texto "Luna es un
    proyecto para usuarios para poner fondos de pantalla animados
    fácil sin plugins") y quita así los logos de Pacman Arch y de
    .deb Debian Ubuntu, sin tocar el archivo original. Devuelve un
    PhotoImage, o None si PIL no está o la imagen no carga.
    """
    if not PIL_DISPONIBLE or not ruta:
        return None
    try:
        img = Image.open(str(ruta)).convert("RGB")
        ancho_img, alto_img = img.size
        img = img.crop((0, 0, ancho_img, int(alto_img * 0.82)))
        img.thumbnail((ancho, alto))
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".svg"}
VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".mov", ".avi"}
ALL_EXTS = IMAGE_EXTS | VIDEO_EXTS

HOME = Path.home()
CONFIG_DIR = HOME / ".config" / "luna"
SETTINGS_FILE = CONFIG_DIR / "ajustes.json"
CURRENT_FILE = CONFIG_DIR / "current.txt"

# Pausa inteligente, como Wayland Wallpaper Engine:
# - "ventana": se congela en cuanto una ventana tiene el foco (al trabajar).
# - "pantalla_completa": solo se congela con apps a pantalla completa o juegos.
DEFAULT_SETTINGS = {
    "pausa_inteligente": True,
    "pausa_modo": "ventana",
    "pausa_bateria": True,
    "pausa_pantalla_apagada": True,
    "multi_monitor": True,
    "inicio_automatico": True,
    "volumen_silencio": True,  # True = silencio (solo en la ventana principal)
    "volumen": 50,
    # Mejoras de video — herramientas activas en Ajustes, no "Próximamente".
    "mejoras_video": True,
    "mejoras_video_escalado_ia": True,
    "mejoras_video_nitidez": True,
    "mejoras_video_estabilizacion": True,
    "mejoras_video_ruido": True,
    "mejoras_video_hdr": True,
    "mejoras_video_blur": False,
}


def buscar_fondos():
    """Busca imágenes y videos en Vídeos / Imágenes y sus variantes en inglés."""
    carpetas = [
        HOME / "Vídeos",
        HOME / "Imágenes",
        HOME / "Videos",
        HOME / "Pictures",
        HOME / "Videos" / "Luna",
        HOME / "Vídeos" / "Luna",
    ]
    archivos = []
    vistos = set()
    for carpeta in carpetas:
        if not carpeta.is_dir():
            continue
        for f in sorted(carpeta.iterdir()):
            if f.is_file() and f.suffix.lower() in ALL_EXTS:
                key = str(f.resolve())
                if key not in vistos:
                    vistos.add(key)
                    archivos.append(f)
    return archivos


def cargar_ajustes():
    try:
        datos = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        return {**DEFAULT_SETTINGS, **datos}
    except Exception:
        return dict(DEFAULT_SETTINGS)


def guardar_ajustes(ajustes):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.write_text(
            json.dumps(ajustes, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return True
    except Exception as exc:
        messagebox.showerror("Luna", f"No se pudieron guardar los Ajustes:\n{exc}")
        return False


def llamar_luna(*args):
    """Llama a `luna ...`; si no está instalado, usa luna.py de esta carpeta."""
    if subprocess.run(["which", "luna"], capture_output=True).returncode == 0:
        return subprocess.run(["luna", *args], capture_output=True, text=True)
    aqui = Path(__file__).resolve().parent / "luna.py"
    return subprocess.run(
        [sys.executable, str(aqui), *args], capture_output=True, text=True
    )


# --- Selector de archivos moderno (no el diálogo viejo de tkinter) ---
# Orden: 1) zenity --file-selection (GtkFileChooser, moderno),
# 2) kdialog (selector nativo de KDE, el de Garuda),
# 3) filedialog de tkinter, solo como respaldo si no hay ninguno.
# En Garuda zenity ya es dependencia de Luna (PKGBUILD), así que
# normalmente se abre el selector moderno del sistema.

def _hay_comando(nombre):
    """True si el comando existe en el PATH."""
    return subprocess.run(
        ["which", nombre], capture_output=True
    ).returncode == 0


def _salida_selector(resultado):
    """Devuelve la ruta elegida en un selector, o None si se canceló."""
    if resultado is None or resultado.returncode != 0:
        return None
    ruta = (resultado.stdout or "").strip()
    if not ruta:
        return None
    # zenity --multiple separa con "\n"; aquí solo se toma la primera.
    ruta = ruta.splitlines()[0].strip()
    return ruta or None


def elegir_carpeta_moderna(titulo="Elige una carpeta con fondos"):
    """Abre el selector moderno del sistema para elegir una carpeta.

    Devuelve la ruta como str, o None si se canceló / no se eligió nada.
    """
    # 1) zenity: el selector moderno de GTK.
    if _hay_comando("zenity"):
        resultado = subprocess.run(
            ["zenity", "--file-selection", "--directory",
             "--title", titulo],
            capture_output=True, text=True)
        ruta = _salida_selector(resultado)
        if ruta and Path(ruta).is_dir():
            return ruta
        if ruta is None:
            return None
    # 2) kdialog: el selector nativo de KDE (Garuda).
    if _hay_comando("kdialog"):
        resultado = subprocess.run(
            ["kdialog", "--getexistingdirectory", ".",
             "--title", titulo],
            capture_output=True, text=True)
        ruta = _salida_selector(resultado)
        if ruta and Path(ruta).is_dir():
            return ruta
        if ruta is None:
            return None
    # 3) Respaldo: el diálogo viejo de tkinter, solo si no hay otro.
    return filedialog.askdirectory(title=titulo) or None


def elegir_archivo_moderno(titulo="Elige una imagen o un video"):
    """Abre el selector moderno del sistema para elegir un fondo.

    Devuelve la ruta como str, o None si se canceló / no se eligió nada.
    """
    filtro_imagenes = "Imágenes | *.jpg *.jpeg *.png *.webp *.gif *.bmp *.svg"
    filtro_videos = "Videos | *.mp4 *.mkv *.webm *.mov *.avi"
    # 1) zenity: el selector moderno de GTK.
    if _hay_comando("zenity"):
        resultado = subprocess.run(
            ["zenity", "--file-selection",
             "--file-filter", filtro_imagenes,
             "--file-filter", filtro_videos,
             "--title", titulo],
            capture_output=True, text=True)
        ruta = _salida_selector(resultado)
        if ruta and Path(ruta).is_file():
            return ruta
        if ruta is None:
            return None
    # 2) kdialog: el selector nativo de KDE (Garuda).
    if _hay_comando("kdialog"):
        resultado = subprocess.run(
            ["kdialog", "--getopenfilename", ".",
             "*.jpg *.jpeg *.png *.webp *.gif *.bmp *.svg *.mp4 *.mkv *.webm *.mov *.avi | Imágenes y videos",
             "--title", titulo],
            capture_output=True, text=True)
        ruta = _salida_selector(resultado)
        if ruta and Path(ruta).is_file():
            return ruta
        if ruta is None:
            return None
    # 3) Respaldo: el diálogo viejo de tkinter, solo si no hay otro.
    ruta = filedialog.askopenfilename(
        title=titulo,
        filetypes=[
            ("Imágenes y videos", "*.jpg *.jpeg *.png *.webp *.gif *.bmp *.svg *.mp4 *.mkv *.webm *.mov *.avi"),
            ("Imágenes", "*.jpg *.jpeg *.png *.webp *.gif *.bmp *.svg"),
            ("Videos", "*.mp4 *.mkv *.webm *.mov *.avi"),
            ("Todos los archivos", "*.*"),
        ])
    return ruta or None


def fondo_en_uso():
    """Ruta del fondo actual (la escribe `luna set`), o None."""
    try:
        ruta = CURRENT_FILE.read_text(encoding="utf-8").strip()
        return Path(ruta) if ruta else None
    except Exception:
        return None


def _hay_proceso_fondo():
    """True si mpvpaper o xwinwrap/mpv del fondo está corriendo."""
    r = subprocess.run(["pgrep", "-f", "mpvpaper|xwinwrap"],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def congelar_fondo():
    """Congela el video del fondo (SIGSTOP): no usa CPU/GPU hasta reanudar.

    Como Wayland Wallpaper Engine: al trabajar, el fondo se queda
    quieto en el mismo cuadro y sigue desde ahí al volver al escritorio.
    """
    if not _hay_proceso_fondo():
        return False
    subprocess.run(["pkill", "-STOP", "-f", "mpvpaper"],
                   capture_output=True)
    subprocess.run(["pkill", "-STOP", "-f", "xwinwrap"],
                   capture_output=True)
    subprocess.run(["pkill", "-STOP", "-f", "mpv"],
                   capture_output=True)
    return True


def reanudar_fondo():
    """Reanuda el video del fondo (SIGCONT) desde el mismo cuadro."""
    if not _hay_proceso_fondo():
        return False
    subprocess.run(["pkill", "-CONT", "-f", "mpvpaper"],
                   capture_output=True)
    subprocess.run(["pkill", "-CONT", "-f", "xwinwrap"],
                   capture_output=True)
    subprocess.run(["pkill", "-CONT", "-f", "mpv"],
                   capture_output=True)
    return True


class VentanaAjustes(tk.Toplevel):
    """Ajustes en ventana aparte, no amontonados en la pantalla principal.

    SIN sonido: Fernando pidió quitar el sonido de Ajustes — el
    volumen/silencio queda solo en la ventana principal (botón
    Sonido/Silencio + deslizador de la barra superior).
    Mejoras de video: TODAS las herramientas activas, con interruptores
    de verdad que se guardan en ~/.config/luna/ajustes.json:
    escalado IA, nitidez, estabilización, reducción de ruido, HDR
    y desenfoque (blur).
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajustes — Luna")
        self.geometry("540x780")
        self.resizable(False, False)
        aplicar_tema(self)
        self.ajustes = cargar_ajustes()

        etiqueta(self, "Ajustes", 16, True).pack(pady=(14, 4))
        etiqueta(self, "Mejoras de video — herramientas activas", 11,
                 color=TEXTO_SUAVE).pack(pady=(0, 10))

        # --- Mejoras de video: todas las herramientas, activas ---
        marco_sv = tk.LabelFrame(self, text="Mejoras de video",
                                 padx=12, pady=8, bg=FONDO_TARJETA, fg=MORADO_CLARO,
                                 font=(FUENTE, 11, "bold"))
        marco_sv.pack(fill="x", padx=20, pady=6)
        self.var_sv = tk.BooleanVar(value=self.ajustes.get("mejoras_video", True))
        tk.Checkbutton(
            marco_sv, text="🎬 Mejoras de video activadas", variable=self.var_sv,
            bg=FONDO_TARJETA, fg=TEXTO, selectcolor=MORADO,
            activebackground=FONDO_TARJETA, activeforeground=TEXTO,
            font=(FUENTE, 12, "bold"),
        ).pack(anchor="w", padx=4, pady=2)
        self.vars_sv = {}
        for clave, texto in [
            ("mejoras_video_escalado_ia", "⬆ Escalado IA (mejora la calidad del video)"),
            ("mejoras_video_nitidez", "✦ Nitidez"),
            ("mejoras_video_estabilizacion", "◎ Estabilización de video"),
            ("mejoras_video_ruido", "〰 Reducción de ruido"),
            ("mejoras_video_hdr", "☀ HDR (más luz y color)"),
            ("mejoras_video_blur", "◐ Desenfoque (blur) de fondo"),
        ]:
            var = tk.BooleanVar(value=self.ajustes.get(clave, True))
            self.vars_sv[clave] = var
            tk.Checkbutton(
                marco_sv, text=texto, variable=var, bg=FONDO_TARJETA, fg=TEXTO,
                selectcolor=MORADO, activebackground=FONDO_TARJETA,
                activeforeground=TEXTO, font=(FUENTE, 11),
            ).pack(anchor="w", padx=20, pady=2)

        # --- Pausa inteligente ---
        self.var_pausa = tk.BooleanVar(value=self.ajustes["pausa_inteligente"])
        self.var_multi = tk.BooleanVar(value=self.ajustes["multi_monitor"])
        self.var_inicio = tk.BooleanVar(value=self.ajustes.get("inicio_automatico", True))
        for texto, var in [
            ("⏸ Pausa inteligente (congela el video al trabajar)", self.var_pausa),
            ("🖥 Multi-monitor (mismo fondo en todas las pantallas)", self.var_multi),
            ("▶ Inicio automático (Luna se abre sola al encender)", self.var_inicio),
        ]:
            tk.Checkbutton(
                self, text=texto, variable=var, bg=FONDO_TARJETA, fg=TEXTO,
                selectcolor=MORADO, activebackground=FONDO_TARJETA,
                activeforeground=TEXTO, font=(FUENTE, 11),
            ).pack(anchor="w", padx=20, pady=4)

        # Pausa inteligente: como `wwe config pause=fullscreen`.
        marco_pausa = tk.LabelFrame(self, text="Pausa inteligente — ¿cuándo se congela?",
                                    padx=12, pady=8, bg=FONDO_TARJETA, fg=MORADO_CLARO,
                                    font=(FUENTE, 11, "bold"))
        marco_pausa.pack(fill="x", padx=20, pady=10)
        self.var_modo = tk.StringVar(value=self.ajustes.get("pausa_modo", "ventana"))
        tk.Radiobutton(
            marco_pausa, text="Al trabajar: en cuanto una ventana tiene el foco",
            variable=self.var_modo, value="ventana", bg=FONDO_TARJETA, fg=TEXTO,
            selectcolor=MORADO, activebackground=FONDO_TARJETA,
            activeforeground=TEXTO, font=(FUENTE, 11),
        ).pack(anchor="w")
        tk.Radiobutton(
            marco_pausa, text="Solo a pantalla completa o jugando",
            variable=self.var_modo, value="pantalla_completa", bg=FONDO_TARJETA, fg=TEXTO,
            selectcolor=MORADO, activebackground=FONDO_TARJETA,
            activeforeground=TEXTO, font=(FUENTE, 11),
        ).pack(anchor="w")
        self.var_bateria = tk.BooleanVar(value=self.ajustes.get("pausa_bateria", True))
        self.var_pantalla = tk.BooleanVar(value=self.ajustes.get("pausa_pantalla_apagada", True))
        for texto, var in [
            ("🔋 También al estar con batería baja", self.var_bateria),
            ("🌙 También cuando se apaga la pantalla", self.var_pantalla),
        ]:
            tk.Checkbutton(
                marco_pausa, text=texto, variable=var, bg=FONDO_TARJETA, fg=TEXTO,
                selectcolor=MORADO, activebackground=FONDO_TARJETA,
                activeforeground=TEXTO, font=(FUENTE, 11),
            ).pack(anchor="w", padx=4, pady=2)
        etiqueta(marco_pausa, "Congelado no usa CPU ni GPU. Al volver al escritorio\n"
                 "sigue desde el mismo cuadro.",
                 10, color=TEXTO_SUAVE, fondo=FONDO_TARJETA).pack(anchor="w", pady=(6, 0))

        # Próximamente / Se acerca
        marco_prox = tk.LabelFrame(self, text="Próximamente / Se acerca",
                                   padx=12, pady=8, bg=FONDO_TARJETA, fg=MORADO_CLARO,
                                   font=(FUENTE, 11, "bold"))
        marco_prox.pack(fill="x", padx=20, pady=14)
        etiqueta(marco_prox, "• Carrusel con favoritos\n• Fondos por hora del día\n• Más formatos y efectos",
                 11, fondo=FONDO_TARJETA).pack(anchor="w")

        # Acerca ya NO va dentro de Ajustes: tiene su propia ventana
        # aparte, que se abre desde el icono Acerca de la ventana principal.
        botones = tk.Frame(self, bg=FONDO)
        botones.pack(pady=16)
        boton_morado(botones, f"{ICONO_GUARDAR} Guardar Cambios", self.guardar).pack(side="left", padx=8)
        boton_claro(botones, f"{ICONO_CERRAR} Cerrar", self.destroy).pack(side="left", padx=8)

    def guardar(self):
        # Se parte de los ajustes guardados, para no borrar el
        # volumen/silencio (que vive solo en la ventana principal).
        nuevos = cargar_ajustes()
        nuevos.update({
            "mejoras_video": self.var_sv.get(),
            "pausa_inteligente": self.var_pausa.get(),
            "pausa_modo": self.var_modo.get(),
            "pausa_bateria": self.var_bateria.get(),
            "pausa_pantalla_apagada": self.var_pantalla.get(),
            "multi_monitor": self.var_multi.get(),
            "inicio_automatico": self.var_inicio.get(),
        })
        for clave, var in self.vars_sv.items():
            nuevos[clave] = var.get()
        if guardar_ajustes(nuevos):
            self.ajustes = nuevos
            messagebox.showinfo("Luna", "Cambios guardados. Mejoras de video activas.")
            self.destroy()


class VentanaAcerca(tk.Toplevel):
    """Acerca de Luna en su propia ventana aparte, no dentro de Ajustes.

    Con submenú de dos páginas (pestañas arriba):
    - "Acerca": el póster completo y GRANDE, sin la franja de los
      logos de Pacman/.deb, y toda la información de Luna.
    - "Funciones": las funciones de Luna, Paso 4 (antes era un
      botón aparte en la ventana principal; ahora vive aquí dentro).
    Todo el texto va con ajuste de línea (wraplength) y la ventana
    tiene barra de desplazamiento, para que nada se corte.
    """

    def __init__(self, parent, pagina="acerca"):
        super().__init__(parent)
        self.title("Acerca de Luna")
        self.geometry("720x960")
        self.minsize(600, 640)
        aplicar_tema(self)

        # Submenú arriba: dos pestañas, Acerca y Funciones.
        barra_paginas = tk.Frame(self, bg=FONDO_BARRA, padx=8, pady=8)
        barra_paginas.pack(fill="x")
        self.boton_pag_acerca = boton_morado(
            barra_paginas, "🐱 Acerca", lambda: self.mostrar_pagina("acerca"))
        self.boton_pag_acerca.pack(side="left", padx=4)
        self.boton_pag_funciones = boton_claro(
            barra_paginas, "✨ Funciones", lambda: self.mostrar_pagina("funciones"))
        self.boton_pag_funciones.pack(side="left", padx=4)
        boton_claro(barra_paginas, f"{ICONO_CERRAR} Cerrar",
                    self.destroy).pack(side="right", padx=4)

        self.pagina_acerca = tk.Frame(self, bg=FONDO)
        self.pagina_funciones = tk.Frame(self, bg=FONDO)
        self._armar_pagina_acerca()
        self._armar_pagina_funciones()
        self.mostrar_pagina(pagina)

    def mostrar_pagina(self, pagina):
        self.pagina_funciones.pack_forget()
        self.pagina_acerca.pack_forget()
        if pagina == "funciones":
            self.pagina_funciones.pack(fill="both", expand=True)
            self.boton_pag_funciones.config(bg=MORADO)
            self.boton_pag_acerca.config(bg=FONDO_TARJETA2)
        else:
            self.pagina_acerca.pack(fill="both", expand=True)
            self.boton_pag_acerca.config(bg=MORADO)
            self.boton_pag_funciones.config(bg=FONDO_TARJETA2)

    def _marco_scroll(self, parent):
        """Marco con desplazamiento vertical, para contenido largo."""
        lienzo = tk.Canvas(parent, highlightthickness=0, bg=FONDO)
        barra_scroll = tk.Scrollbar(parent, orient="vertical", command=lienzo.yview)
        lienzo.configure(yscrollcommand=barra_scroll.set)
        lienzo.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")
        contenido = tk.Frame(lienzo, bg=FONDO)
        lienzo.create_window((0, 0), window=contenido, anchor="nw")
        contenido.bind(
            "<Configure>", lambda e: lienzo.configure(scrollregion=lienzo.bbox("all"))
        )
        lienzo.bind("<MouseWheel>", lambda e: lienzo.yview_scroll(-1 if e.delta > 0 else 1, "units"))
        lienzo.bind("<Button-4>", lambda e: lienzo.yview_scroll(-1, "units"))
        lienzo.bind("<Button-5>", lambda e: lienzo.yview_scroll(1, "units"))
        return contenido

    def _armar_pagina_acerca(self):
        contenido = self._marco_scroll(self.pagina_acerca)

        def texto(texto_, tamano=12, negrita=False, color=TEXTO):
            lbl = tk.Label(contenido, text=texto_, bg=FONDO, fg=color,
                           font=(FUENTE, tamano, "bold" if negrita else "normal"),
                           wraplength=620, justify="center")
            lbl.pack(pady=(4, 4), padx=20, fill="x")
            return lbl

        texto("Acerca de Luna", 20, True)

        # Póster GRANDE, sin logos: recortado al 82% en memoria.
        self._poster = cargar_poster_sin_logos(
            ruta_archivada(POSTER_BIENVENIDA), 560, 780
        )
        if self._poster is not None:
            tk.Label(contenido, image=self._poster, bg=FONDO).pack(pady=10)
        else:
            lienzo_gato = tk.Canvas(contenido, width=160, height=160,
                                    highlightthickness=0, bg=FONDO)
            lienzo_gato.pack(pady=8)
            lienzo_gato.create_polygon(36, 56, 56, 12, 76, 52, fill="black")
            lienzo_gato.create_polygon(124, 56, 104, 12, 84, 52, fill="black")
            lienzo_gato.create_oval(28, 40, 132, 136, fill="black")
            lienzo_gato.create_oval(56, 76, 68, 88, fill="white")
            lienzo_gato.create_oval(92, 76, 104, 88, fill="white")
            lienzo_gato.create_text(80, 116, text="?", fill="white",
                                    font=(FUENTE, 28, "bold"))

        texto("Luna Beta 1.0-beta", 16, True)
        texto("Qué es Luna", 13, True, MORADO_CLARO)
        texto("Luna es un proyecto para poner fondos de pantalla animados, "
              "fácil y sin plugins, para el usuario común en Linux. "
              "Pones un video o una foto como fondo de tu escritorio, "
              "sin terminal y sin complicarte.")
        texto("Cómo se usa", 13, True, MORADO_CLARO)
        texto("• Clic derecho en tu foto o video, le das a Luna, y Luna "
              "la pone automática en el programa y en el escritorio, "
              "tanto foto como video.\n"
              "• O abres Luna, eliges una foto o video del carrusel 3D, "
              "y picas el botón grande "
              "Poner Imagen en el Fondo de Pantalla.")
        texto("Instalación — solo 3 pasos", 13, True, MORADO_CLARO)
        texto("1. Picas Pacman para Arch, o .deb para Debian / Ubuntu.\n"
              "2. Se ve el proceso instalando, con la barrita del 1 al 100.\n"
              "3. Al terminar, se abre el programa Luna.")
        texto("Hecho por Vega & Kiki", 12, True, TEXTO_SUAVE)
        texto("Guzman", 11, True, TEXTO_SUAVE)
        boton_claro(contenido, f"{ICONO_CERRAR} Cerrar", self.destroy).pack(pady=14)

    def _armar_pagina_funciones(self):
        """Página Funciones — Paso 4, dentro de Acerca como submenú.

        La lista sale de PAGINA_LUNA.md y COMPARACION_LUNA.md, sin
        inventar funciones nuevas. No incluye video de YouTube ni
        página web como fondo.
        """
        contenido = self._marco_scroll(self.pagina_funciones)
        tk.Label(contenido, text="Funciones de Luna — Paso 4", bg=FONDO,
                 fg=TEXTO, font=(FUENTE, 16, "bold"),
                 wraplength=620, justify="center").pack(pady=(14, 4), padx=20)
        tk.Label(contenido, text="Luna Beta 1.0-beta — fácil y sin plugins",
                 bg=FONDO, fg=TEXTO_SUAVE, font=(FUENTE, 11),
                 wraplength=620, justify="center").pack(pady=(0, 10), padx=20)
        for titulo, detalle in FUNCIONES_LUNA:
            marco = tk.Frame(contenido, bg=FONDO_TARJETA, padx=12, pady=8)
            marco.pack(fill="x", padx=20, pady=4)
            tk.Label(marco, text=f"✓ {titulo}", bg=FONDO_TARJETA, fg=TEXTO,
                     font=(FUENTE, 12, "bold"), wraplength=560,
                     justify="left", anchor="w").pack(fill="x")
            tk.Label(marco, text=detalle, bg=FONDO_TARJETA, fg=TEXTO_SUAVE,
                     font=(FUENTE, 11), wraplength=560,
                     justify="left", anchor="w").pack(fill="x")
        tk.Label(contenido, text="No incluye video de YouTube ni página web "
                 "como fondo.", bg=FONDO, fg=TEXTO_SUAVE,
                 font=(FUENTE, 11), wraplength=620, justify="center").pack(pady=(10, 4), padx=20)
        tk.Label(contenido, text="Hecho por Vega & Kiki\nGuzman", bg=FONDO,
                 fg=TEXTO_SUAVE, font=(FUENTE, 11)).pack(pady=(0, 4))
        boton_claro(contenido, f"{ICONO_CERRAR} Cerrar", self.destroy).pack(pady=12)


def dibujar_gatito_acerca(lienzo, cx, cy, escala=1.0):
    """Dibuja el gatito negro con '?' en un Canvas, centrado en (cx, cy)."""
    s = escala
    lienzo.create_polygon(cx - 22 * s, cy - 12 * s, cx - 12 * s, cy - 34 * s,
                          cx - 2 * s, cy - 14 * s, fill="black")
    lienzo.create_polygon(cx + 22 * s, cy - 12 * s, cx + 12 * s, cy - 34 * s,
                          cx + 2 * s, cy - 14 * s, fill="black")
    lienzo.create_oval(cx - 26 * s, cy - 20 * s, cx + 26 * s, cy + 28 * s, fill="black")
    lienzo.create_oval(cx - 12 * s, cy - 2 * s, cx - 6 * s, cy + 4 * s, fill="white")
    lienzo.create_oval(cx + 6 * s, cy - 2 * s, cx + 12 * s, cy + 4 * s, fill="white")
    lienzo.create_text(cx, cy + 18 * s, text="?", fill="white",
                       font=(FUENTE, int(14 * s), "bold"))


FUNCIONES_LUNA = [
    ("Video como fondo de pantalla", "Pones un video como fondo de tu escritorio y se mueve."),
    ("Imagen como fondo de pantalla", "Pones una foto como fondo de tu escritorio."),
    ("Instalador fácil .deb / Pacman", "Detecta solo tu sistema y al terminar abre Luna. Solo 3 pasos."),
    ("Carrusel 3D", "Solo el carrusel 3D, grande y cool, con tus fotos y videos."),
    ("Clic derecho en escritorio", "Poner con Luna, Establecer Imagen como Fondo, Establecer Video como Fondo, Abrir Luna."),
    ("Botón Poner en el Fondo", "Al elegir un fondo, picas el botón grande Poner Imagen en el Fondo de Pantalla."),
    ("Poner fondo automático", "Al elegir un video o una imagen, Luna la pone automática en el programa y en el escritorio."),
    ("Todos los formatos", "Imágenes JPG, PNG, WEBP, GIF, BMP y SVG. Videos MP4, MKV, WEBM, MOV y AVI."),
    ("Pausa inteligente", "Congela el video al maximizar, a pantalla completa, según la ventana, la batería y si se apaga la pantalla. Congelado no usa CPU ni GPU."),
    ("Volumen y silencio", "Sonido solo en el escritorio: se silencia al cambiar a una app."),
    ("Multi-monitor", "El mismo fondo en todas las pantallas."),
    ("Inicio automático", "Luna se abre sola al encender tu computadora."),
    ("Mejoras de video", "Escalado IA, nitidez, estabilización, reducción de ruido, HDR y desenfoque."),
    ("Sin terminal", "Para el usuario común: solo picas, no escribes comandos."),
]


class LunaGUI(tk.Tk):
    """Ventana principal de Luna, como el picker de Wayland Wallpaper Engine.

    Barra superior: búsqueda, volumen/silencio, Aleatorio, Agregar
    Carpeta (solo aquí va ese botón, y aquí se muestra la carpeta
    elegida) y el botón "Funciones de Luna" (Paso 4). Debajo, SOLO
    el carrusel 3D, grande y cool, con el nombre del fondo elegido
    y el botón Poner en el Fondo. Sin Biblioteca, sin cuadrícula
    y sin Vista previa.
    """

    def __init__(self):
        super().__init__()
        self.title(f"Luna Beta {VERSION}")
        self.geometry("900x880")
        self.minsize(720, 640)
        aplicar_tema(self)
        self.ajustes = cargar_ajustes()
        self.fondos = buscar_fondos()
        self.carpeta_actual = None  # carpeta elegida con Agregar Carpeta
        self.busqueda = ""
        self.seleccionado = None
        self.congelado = False
        self.imagenes_cache = []  # evita que PhotoImage se borre
        self._poster_cabecera = None

        # Cabecera Luna: póster del gatito + LUNA en morado oscuro
        barra = tk.Frame(self, bg=FONDO_BARRA, padx=12, pady=10)
        barra.pack(fill="x")
        self._poster_cabecera = cargar_poster_sin_logos(ruta_archivada(POSTER_BIENVENIDA), 120, 120)
        if self._poster_cabecera is not None:
            tk.Label(barra, image=self._poster_cabecera, bg=FONDO_BARRA).pack(side="left", padx=(0, 10))
        etiqueta(barra, "LUNA", 22, True, fondo=FONDO_BARRA).pack(side="left")
        etiqueta(barra, "  Beta 1.0-beta", 11, color=TEXTO_SUAVE, fondo=FONDO_BARRA).pack(side="left", pady=(8, 0))
        # Estado del fondo, como en la página de referencia: reproduciendo / congelado.
        self.etiqueta_pausa = tk.Label(barra, text="▶ Reproduciendo", bg=FONDO_BARRA,
                                       fg=VERDE, font=(FUENTE, 11, "bold"))
        self.etiqueta_pausa.pack(side="right", pady=(8, 0))

        # --- Barra del picker (como la de Wayland Wallpaper Engine) ---
        picker = tk.Frame(self, bg=FONDO, padx=12, pady=8)
        picker.pack(fill="x")
        etiqueta(picker, f"{ICONO_BUSCAR} Buscar:", 11, True).pack(side="left", padx=(0, 4))
        self.entrada_busqueda = tk.Entry(
            picker, bg=FONDO_TARJETA2, fg=TEXTO, insertbackground=TEXTO,
            relief="flat", font=(FUENTE, 11), width=22,
        )
        self.entrada_busqueda.pack(side="left", padx=2)
        self.entrada_busqueda.bind("<KeyRelease>", self._al_escribir_busqueda)
        boton_claro(picker, f"{ICONO_CERRAR} Limpiar", self._limpiar_busqueda).pack(side="left", padx=2)
        # Volumen / silencio: sonido solo en el escritorio.
        self.boton_volumen = boton_claro(
            picker, f"{ICONO_SILENCIO} Silencio" if self.ajustes["volumen_silencio"] else f"{ICONO_SONIDO} Sonido",
            self._cambiar_silencio)
        self.boton_volumen.pack(side="left", padx=8)
        self.var_volumen = tk.IntVar(value=self.ajustes["volumen"])
        # En Luna no hay barrita de progreso: el único deslizador es
        # el de volumen, y su carril ahora es morado vivo, no gris.
        tk.Scale(picker, from_=0, to=100, orient="horizontal",
                 variable=self.var_volumen, length=110, showvalue=False,
                 bg=FONDO, fg=TEXTO, troughcolor=MORADO,
                 activebackground=MORADO_CLARO,
                 highlightthickness=0, command=lambda _v: self._al_cambiar_volumen(),
                 ).pack(side="left", padx=2)
        # Aleatorio: como el botón de fondo aleatorio del picker.
        boton_morado(picker, f"{ICONO_ALEATORIO} Aleatorio", self.poner_aleatorio).pack(side="left", padx=8)
        # Agregar Carpeta va SOLO en esta barra superior, no en otra
        # parte. Aquí mismo se muestra la carpeta elegida.
        boton_claro(picker, f"{ICONO_CARPETA} Agregar Carpeta", self.agregar_carpeta).pack(side="left", padx=2)
        # Etiqueta vacía al inicio: solo muestra la ruta cuando
        # se elige una carpeta con Agregar Carpeta.
        self.etiqueta_carpeta = etiqueta(picker, "", 10, color=TEXTO_SUAVE)
        self.etiqueta_carpeta.pack(side="left", padx=6)
        # Paso 4: Funciones de Luna ya NO es botón aparte: vive
        # dentro de Acerca, como submenú (pestaña "Funciones").
        # Pausa manual: congela / reanuda el video del fondo.
        self.boton_pausa = boton_claro(picker, f"{ICONO_CONGELAR} Congelar", self._cambiar_pausa_manual)
        self.boton_pausa.pack(side="right", padx=2)

        # Barra de acciones
        acciones = tk.Frame(self, bg=FONDO, padx=12, pady=6)
        acciones.pack(fill="x")
        etiqueta(acciones, f"{ICONO_AGREGAR} Agregar Fondo & Imagen/Video", 14, True).pack(side="left")
        self._crear_icono_acerca(acciones).pack(side="right", padx=6)
        boton_morado(acciones, f"{ICONO_AJUSTES} Ajustes", self.abrir_ajustes).pack(side="right", padx=4)
        boton_claro(acciones, f"{ICONO_QUITAR} Quitar Imagen/Video", self.quitar_seleccionado).pack(side="right", padx=4)
        boton_claro(acciones, f"{ICONO_AGREGAR} Agregar Fondo", self.agregar_fondo).pack(side="right", padx=4)

        # --- Barra "Wallpapers", como en la foto de referencia ---
        # Título a la izquierda, ayuda de teclado en el centro y
        # fecha/hora a la derecha, igual que en la captura.
        from datetime import datetime as _dt
        barra_wall = tk.Frame(self, bg=FONDO_TARJETA, padx=12, pady=6)
        barra_wall.pack(fill="x", padx=12, pady=(6, 0))
        etiqueta(barra_wall, "Wallpapers", 13, True, fondo=FONDO_TARJETA).pack(side="left")
        etiqueta(barra_wall,
                 "← →: mover   Enter: confirmar   Clic: elegir   Doble clic: aplicar   F5: refrescar   Ctrl+W: cerrar",
                 10, color=TEXTO_SUAVE, fondo=FONDO_TARJETA).pack(side="left", padx=16)
        etiqueta(barra_wall, _dt.now().strftime("%d %b %Y - %I:%M %p").upper(),
                 11, True, color=TEXTO_SUAVE, fondo=FONDO_TARJETA).pack(side="right")

        # SOLO carrusel 3D, grande y cool: la imagen del centro grande
        # y de frente; las de los lados más pequeñas, inclinadas y
        # oscuras, sobre fondo negro. Sin Biblioteca, sin cuadrícula
        # y sin Vista previa: Fernando pidió quitarlas.
        marco_biblio = tk.Frame(self, bg=FONDO)
        marco_biblio.pack(fill="x", padx=12, pady=(6, 0))
        etiqueta(marco_biblio, "🎠 Carrusel 3D", 12, True).pack(side="left")
        self.etiqueta_conteo = etiqueta(marco_biblio, "", 11, color=TEXTO_SUAVE)
        self.etiqueta_conteo.pack(side="right")
        marco_cover = tk.Frame(self, bg=FONDO_COVER, padx=6, pady=10)
        marco_cover.pack(fill="both", expand=True, padx=12, pady=6)
        boton_claro(marco_cover, "‹", lambda: self._mover_seleccion(-1)).pack(side="left", padx=2)
        self.carrusel = tk.Frame(marco_cover, bg=FONDO_COVER)
        self.carrusel.pack(side="left", fill="both", expand=True)
        boton_claro(marco_cover, "›", lambda: self._mover_seleccion(1)).pack(side="right", padx=2)
        self._cover_cache = []

        # Nombre del fondo elegido, debajo del carrusel.
        self.etiqueta_seleccionado = tk.Label(
            self, text="Elige un fondo en el carrusel.",
            font=(FUENTE, 12, "bold"), bg=FONDO, fg=TEXTO,
            wraplength=700, justify="center",
        )
        self.etiqueta_seleccionado.pack(pady=(4, 2))
        self.etiqueta_ruta = tk.Label(
            self, text="", font=(FUENTE, 10), bg=FONDO, fg=TEXTO_SUAVE,
            wraplength=700, justify="center",
        )
        self.etiqueta_ruta.pack(pady=(0, 4))

        # Botón principal morado, grande, con icono
        boton_morado(self, f"{ICONO_PONER_FONDO} Poner Imagen en el Fondo de Pantalla",
                     self.poner_fondo, grande=True).pack(pady=10)
        self.etiqueta_estado = tk.Label(self, text="", fg=VERDE, bg=FONDO,
                                        font=(FUENTE, 12, "bold"))
        self.etiqueta_estado.pack()

        # Pie, al final de todo
        etiqueta(self, "Hecho por Vega & Kiki\nGuzman", 10, color=TEXTO_SUAVE).pack(
            side="bottom", pady=8
        )

        self.refrescar_todo()
        if self.fondos:
            self.seleccionar(self.fondos[0])
        # Teclado del selector, como en la foto: flechas mueven,
        # Enter confirma y pone el fondo, F5 refresca, Ctrl+W cierra.
        # Si el foco está en la caja de búsqueda, las flechas y Enter
        # son de la caja, no del selector.
        self.bind_all("<Left>", lambda e: self._mover_seleccion(-1))
        self.bind_all("<Right>", lambda e: self._mover_seleccion(1))
        self.bind_all("<Return>", lambda e: self._enter_selector())
        self.bind_all("<F5>", lambda e: self._refrescar_biblioteca())
        self.bind_all("<Control-w>", lambda e: self.destroy())
        self.bind_all("<Control-W>", lambda e: self.destroy())
        # Vigila la pausa inteligente cada 3 segundos (ver _vigilar_pausa).
        self.after(3000, self._vigilar_pausa)

    def _en_caja_busqueda(self):
        try:
            return self.focus_get() is self.entrada_busqueda
        except Exception:
            return False

    def _mover_seleccion(self, delta):
        """Flechas ← →: mueve la selección en el carrusel."""
        if self._en_caja_busqueda():
            return
        filtrados = self._fondos_filtrados()
        if not filtrados:
            return
        try:
            i = filtrados.index(self.seleccionado)
        except ValueError:
            i = 0 if delta > 0 else len(filtrados) - 1
            self.seleccionar(filtrados[i])
            return
        self.seleccionar(filtrados[(i + delta) % len(filtrados)])

    def _enter_selector(self):
        """Enter: confirma y pone el fondo elegido."""
        if self._en_caja_busqueda():
            return
        self.poner_fondo()

    def _refrescar_biblioteca(self):
        """F5: vuelve a buscar los fondos en el disco y refresca el carrusel.

        Se añaden los de Vídeos/Imágenes y se conservan los que el
        usuario agregó a mano con Agregar Carpeta/Fondo, si el
        archivo sigue existiendo.
        """
        actual = self.seleccionado
        vistos = set()
        nuevos = []
        for f in buscar_fondos() + list(self.fondos):
            key = str(f.resolve()) if f.exists() else None
            if key and key not in vistos:
                vistos.add(key)
                nuevos.append(f)
        self.fondos = nuevos
        if actual and actual in self.fondos:
            self.seleccionar(actual)
        else:
            self.refrescar_todo()
            if self.fondos:
                self.seleccionar(self.fondos[0])
        self.etiqueta_estado.config(text="Carrusel actualizado.")

    # --- Picker: búsqueda, volumen, aleatorio, pausa ---

    def _fondos_filtrados(self):
        if not self.busqueda.strip():
            return list(self.fondos)
        texto = self.busqueda.strip().lower()
        return [f for f in self.fondos if texto in f.name.lower()]

    def _al_escribir_busqueda(self, _evento=None):
        self.busqueda = self.entrada_busqueda.get()
        self.refrescar_todo()

    def _limpiar_busqueda(self):
        self.entrada_busqueda.delete(0, "end")
        self.busqueda = ""
        self.refrescar_todo()

    def _cambiar_silencio(self):
        self.ajustes["volumen_silencio"] = not self.ajustes["volumen_silencio"]
        self.boton_volumen.config(
            text=f"{ICONO_SILENCIO} Silencio" if self.ajustes["volumen_silencio"] else f"{ICONO_SONIDO} Sonido")
        guardar_ajustes(self.ajustes)
        estado = "en silencio" if self.ajustes["volumen_silencio"] else "con sonido"
        self.etiqueta_estado.config(text=f"Volumen: fondo {estado}.")

    def _al_cambiar_volumen(self):
        self.ajustes["volumen"] = self.var_volumen.get()
        if self.ajustes["volumen"] > 0 and self.ajustes["volumen_silencio"]:
            self.ajustes["volumen_silencio"] = False
            self.boton_volumen.config(text=f"{ICONO_SONIDO} Sonido")
        guardar_ajustes(self.ajustes)

    def poner_aleatorio(self):
        """Botón Aleatorio del picker: elige un fondo al azar y lo pone."""
        candidatos = self._fondos_filtrados()
        if not candidatos:
            messagebox.showinfo("Luna", "No hay fondos para elegir al azar.")
            return
        elegido = random.choice(candidatos)
        self.seleccionar(elegido)
        self.poner_fondo()

    def _cambiar_pausa_manual(self):
        if self.congelado:
            if reanudar_fondo():
                self.congelado = False
                self.etiqueta_pausa.config(text="▶ Reproduciendo", fg=VERDE)
                self.boton_pausa.config(text=f"{ICONO_CONGELAR} Congelar")
                self.etiqueta_estado.config(text="Fondo reanudado desde el mismo cuadro.")
            else:
                messagebox.showinfo("Luna", "No hay ningún fondo de video corriendo para reanudar.")
        else:
            if congelar_fondo():
                self.congelado = True
                self.etiqueta_pausa.config(text="⏸ Congelado — estás trabajando", fg=MORADO_CLARO)
                self.boton_pausa.config(text=f"{ICONO_REANUDAR} Reanudar")
                self.etiqueta_estado.config(text="Fondo congelado: no usa CPU ni GPU.")
            else:
                messagebox.showinfo("Luna", "No hay ningún fondo de video corriendo para congelar.")

    def _vigilar_pausa(self):
        """Pausa inteligente automática, como en Wayland Wallpaper Engine.

        Modo "ventana": si hay una ventana activa que no es Luna ni el
        escritorio, congela el fondo; al volver al escritorio, reanuda.
        Modo "pantalla_completa": solo congela si hay una ventana a
        pantalla completa (juego o app). Necesita xdotool; si no está
        instalado, la pausa queda en manual y no se hace nada sola.
        """
        try:
            if self.ajustes.get("pausa_inteligente") and _hay_proceso_fondo():
                modo = self.ajustes.get("pausa_modo", "ventana")
                trabajando = False
                if modo == "pantalla_completa":
                    r = subprocess.run(
                        ["xdotool", "search", "--onlyvisible", "--fullscreen", ""],
                        capture_output=True, text=True)
                    trabajando = bool(r.stdout.strip())
                else:
                    r = subprocess.run(
                        ["xdotool", "getactivewindow", "getwindowname"],
                        capture_output=True, text=True)
                    nombre = (r.stdout or "").strip()
                    trabajando = bool(nombre) and "Luna" not in nombre
                if trabajando and not self.congelado:
                    if congelar_fondo():
                        self.congelado = True
                        self.etiqueta_pausa.config(text="⏸ Congelado — estás trabajando", fg=MORADO_CLARO)
                        self.boton_pausa.config(text=f"{ICONO_REANUDAR} Reanudar")
                elif not trabajando and self.congelado:
                    if reanudar_fondo():
                        self.congelado = False
                        self.etiqueta_pausa.config(text="▶ Reproduciendo", fg=VERDE)
                        self.boton_pausa.config(text=f"{ICONO_CONGELAR} Congelar")
        except Exception:
            pass
        finally:
            self.after(3000, self._vigilar_pausa)

    # --- Carrusel 3D, solo él ---

    def refrescar_todo(self):
        self.refrescar_carrusel()

    def refrescar_carrusel(self):
        """Carrusel 3D tipo cover-flow, grande y cool, como en la foto.

        Muestra hasta 7 fondos alrededor del elegido: el del centro
        grande y de frente (340x230), los de los lados cada vez más
        pequeños, inclinados y oscuros. Clic en cualquiera lo elige.
        """
        for hijo in self.carrusel.winfo_children():
            hijo.destroy()
        self._cover_cache = []
        filtrados = self._fondos_filtrados()
        self.etiqueta_conteo.config(text=f"{len(filtrados)} de {len(self.fondos)} fondos")
        if not filtrados:
            etiqueta(
                self.carrusel,
                "No hay fondos con esa búsqueda.\nUsa 'Agregar Carpeta Fondo'.",
                11, fondo=FONDO_COVER,
            ).pack(padx=10, pady=20)
            return
        try:
            centro = filtrados.index(self.seleccionado)
        except ValueError:
            centro = 0
        # (distancia, ancho, alto, inclinación, oscurecer)
        niveles = [(0, 340, 230, 0.0, 0.0),
                   (1, 260, 175, 0.25, 0.25),
                   (2, 190, 130, 0.45, 0.45),
                   (3, 140, 95, 0.6, 0.6)]
        for i in range(centro - 3, centro + 4):
            if i < 0 or i >= len(filtrados):
                continue
            f = filtrados[i]
            distancia = abs(i - centro)
            lado = -1 if i < centro else (1 if i > centro else 0)
            _d, ancho, alto, incl, osc = niveles[distancia]
            es_video = f.suffix.lower() in VIDEO_EXTS
            mini = None
            if not es_video:
                mini = miniatura_cover(f, ancho, alto,
                                       inclinacion=incl * lado,
                                       oscurecer=osc)
            if mini is not None:
                self._cover_cache.append(mini)
                boton = tk.Button(
                    self.carrusel, image=mini, bg=FONDO_COVER,
                    activebackground=FONDO_COVER, relief="flat",
                    borderwidth=0, highlightthickness=3 if distancia == 0 else 0,
                    highlightbackground=AZUL_SELECCION,
                    command=lambda r=f: self.seleccionar(r))
            else:
                texto = ("🎬 VIDEO\n" if es_video else "🖼 IMAGEN\n") + f.name[:18]
                boton = tk.Button(
                    self.carrusel, text=texto, width=ancho // 10, height=alto // 22,
                    bg="#111111", fg=TEXTO, activebackground=MORADO,
                    relief="flat", borderwidth=0,
                    highlightthickness=3 if distancia == 0 else 0,
                    highlightbackground=AZUL_SELECCION,
                    font=(FUENTE, 10, "bold"),
                    command=lambda r=f: self.seleccionar(r))
            boton.pack(side="left", padx=3, pady=4)

    def _boton_fondo(self, parent, ruta, mini, texto, ancho, alto, seleccionado):
        if mini is not None:
            self.imagenes_cache.append(mini)
            return tk.Button(
                parent, image=mini, text=texto, compound="top",
                width=ancho, height=alto, bg=FONDO_TARJETA2, fg=TEXTO,
                activebackground=MORADO, relief="flat", borderwidth=0,
                highlightthickness=3 if seleccionado else 0,
                highlightbackground=MORADO_CLARO,
                command=lambda r=ruta: self.seleccionar(r),
            )
        return tk.Button(
            parent, text=texto, width=14, height=4,
            bg=FONDO_TARJETA2, fg=TEXTO, activebackground=MORADO,
            relief="flat", borderwidth=0,
            highlightthickness=3 if seleccionado else 0,
            highlightbackground=MORADO_CLARO,
            command=lambda r=ruta: self.seleccionar(r),
        )

    def seleccionar(self, ruta):
        self.seleccionado = ruta
        tipo = "Video" if ruta.suffix.lower() in VIDEO_EXTS else "Imagen"
        en_uso = fondo_en_uso()
        marca = " ★ En uso" if en_uso and Path(en_uso) == ruta else ""
        self.etiqueta_seleccionado.config(text=f"{tipo}: {ruta.name}{marca}")
        self.etiqueta_ruta.config(text=str(ruta))
        self.refrescar_todo()

    def agregar_fondo(self):
        """Agrega una imagen o un video con el selector moderno del sistema."""
        ruta = elegir_archivo_moderno("Elige una imagen o un video")
        if not ruta:
            return
        f = Path(ruta)
        if f.suffix.lower() not in ALL_EXTS:
            messagebox.showinfo("Luna", "Ese archivo no es una imagen ni un video compatible.")
            return
        if f in self.fondos:
            self.seleccionar(f)
            return
        self.fondos.append(f)
        self.refrescar_todo()
        self.seleccionar(f)

    def agregar_carpeta(self):
        """Agrega una carpeta con el selector moderno del sistema.

        Fernando aclara: para buscar la imagen, el usuario selecciona
        su carpeta, y se cargan todas sus imágenes de donde las tenga
        guardadas. Por eso esto vale para CUALQUIER carpeta del
        usuario — no solo ~/Vídeos o ~/Imágenes — y carga TODAS las
        imágenes y videos que haya dentro, también en sus subcarpetas:
        JPG, PNG, WEBP, GIF, BMP, SVG y MP4, MKV, WEBM, MOV, AVI.
        Al elegirla, todas aparecen en el carrusel. La carpeta
        elegida se muestra solo en la barra superior (una sola
        carpeta a la vez), no en otra parte de la ventana.
        """
        carpeta = elegir_carpeta_moderna("Elige una carpeta con fondos")
        if not carpeta:
            return
        carpeta = Path(carpeta)
        if not carpeta.is_dir():
            messagebox.showinfo("Luna", "Esa carpeta no existe.")
            return
        # La carpeta elegida se muestra solo en la barra superior.
        self.carpeta_actual = carpeta
        self.etiqueta_carpeta.config(text=f"📁 {carpeta}")
        ya = {str(f.resolve()) for f in self.fondos}
        nuevos = []
        total_en_carpeta = 0
        # rglob: también las imágenes guardadas en subcarpetas.
        for f in sorted(carpeta.rglob("*")):
            if f.is_file() and f.suffix.lower() in ALL_EXTS:
                total_en_carpeta += 1
                key = str(f.resolve())
                if key not in ya:
                    ya.add(key)
                    nuevos.append(f)
        if not nuevos:
            if total_en_carpeta:
                messagebox.showinfo(
                    "Luna",
                    f"Todos los fondos de esa carpeta ya estaban en el carrusel ({total_en_carpeta}).")
            else:
                messagebox.showinfo(
                    "Luna",
                    "Esa carpeta no tiene imágenes ni videos compatibles.\n"
                    "Formatos: JPG, PNG, WEBP, GIF, BMP, SVG y "
                    "MP4, MKV, WEBM, MOV, AVI.")
            return
        self.fondos.extend(nuevos)
        self.carpeta_actual = carpeta
        self.etiqueta_carpeta.config(text=f"📁 {carpeta}")
        self.refrescar_todo()
        self.seleccionar(nuevos[0])
        self.etiqueta_estado.config(
            text=f"Se cargaron {len(nuevos)} fondos de {carpeta.name}."
        )

    def quitar_seleccionado(self):
        if not self.seleccionado:
            messagebox.showinfo("Luna", "Primero elige un fondo en el carrusel.")
            return
        nombre = self.seleccionado.name
        self.fondos.remove(self.seleccionado)
        self.seleccionado = None
        self.refrescar_todo()
        self.etiqueta_seleccionado.config(text="Fondo quitado de la lista.")
        self.etiqueta_ruta.config(text="")
        self.etiqueta_estado.config(text=f"Se quitó {nombre} de la lista (el archivo no se borró).")

    def _crear_icono_acerca(self, parent):
        """Icono Acerca: gatito negro dibujado con '?' y texto 'Acerca', clicable.

        Es un icono dibujado (no emoji): al pasar el ratón se ilumina
        en morado, como los demás botones modernos.
        """
        marco = tk.Frame(parent, bg=FONDO, cursor="hand2")
        lienzo = tk.Canvas(marco, width=52, height=52, highlightthickness=0, bg=FONDO)
        lienzo.pack()
        dibujar_gatito_acerca(lienzo, 26, 28, escala=0.9)
        etiqueta_acerca = tk.Label(marco, text="🐱 Acerca", bg=FONDO, fg=TEXTO,
                                   font=(FUENTE, 10, "bold"))
        etiqueta_acerca.pack()
        for widget in (marco, lienzo, etiqueta_acerca):
            widget.bind("<Button-1>", lambda e: self.abrir_acerca())
            widget.bind("<Enter>", lambda _e: marco.config(bg=FONDO_TARJETA2))
            widget.bind("<Leave>", lambda _e: marco.config(bg=FONDO))
        return marco

    def abrir_acerca(self):
        VentanaAcerca(self)

    def abrir_ajustes(self):
        VentanaAjustes(self)
        # Al volver de Ajustes, recarga volumen y pausa por si cambiaron.
        self.ajustes = cargar_ajustes()
        self.var_volumen.set(self.ajustes["volumen"])
        self.boton_volumen.config(
            text=f"{ICONO_SILENCIO} Silencio" if self.ajustes["volumen_silencio"] else f"{ICONO_SONIDO} Sonido")

    def poner_fondo(self):
        if not self.seleccionado:
            messagebox.showinfo("Luna", "Primero elige un fondo en el carrusel.")
            return
        resultado = llamar_luna("set", str(self.seleccionado))
        salida = (resultado.stdout or "") + (resultado.stderr or "")
        if resultado.returncode == 0:
            self.congelado = False
            self.etiqueta_pausa.config(text="▶ Reproduciendo", fg=VERDE)
            self.boton_pausa.config(text=f"{ICONO_CONGELAR} Congelar")
            self.etiqueta_estado.config(
                text=f"¡Listo! Fondo puesto: {self.seleccionado.name}"
            )
            self.refrescar_todo()
        else:
            messagebox.showerror("Luna", f"No se pudo poner el fondo:\n{salida.strip() or 'Error desconocido.'}")


def main():
    app = LunaGUI()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
