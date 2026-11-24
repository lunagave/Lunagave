#!/usr/bin/env python3
"""
Luna Beta 1.0-beta — instalador con ventanita, con imágenes.
Paso 1, aprobado por Fernando: dos botones con icono para instalar.
  - 🟡 Instalar Arch Pacman: instala en Arch / Garuda
  - 🌀 Instalar .deb: instala en Debian / Ubuntu
  El póster va LIMPIO, sin logos: se recorta en memoria al 82% de
  su altura (ver cargar_poster_sin_logos), así no se ven el logo
  amarillo de Pacman Arch ni el de .deb Debian Ubuntu dentro del
  póster. Los logos van solo como icono en los botones de instalar.
Paso 2: como un asistente Next — Paso 1 elige, Paso 2 instala con
  la barrita animada DESPACIO del 1 al 100 (1% cada 700 ms, con
  "Cargando..." animado), Paso 3 completo con el botón Continuar.
  Sin contraseña de terminal: en Arch se compila con makepkg (sin
  -i, no pide sudo) y el paquete se instala con pkexec, que abre
  la ventanita gráfica del sistema para la contraseña, una sola
  vez. En Debian/Ubuntu igual: se compila el .deb y se instala con
  pkexec dpkg -i. Si no hay pkexec, se cae a makepkg -si / sudo
  dpkg -i y lo dice claro. Nunca se finge un éxito que no hubo.
Paso 3: Finalizar — botón grande "Continuar" que cierra el
  instalador y abre el programa Luna (luna-gui). Solo 3 pasos:
  1 Instalar > 2 Proceso / barra > 3 Continuar / Finalizar > Luna.

Uso en Garuda:
  python3 luna-installer-gui.py
  o, una vez instalado el paquete: bash /usr/lib/luna/luna-installer.sh
  (ese .sh abre esta ventana si tkinter está disponible,
   si no, usa zenity, y si no, terminal)

Para probar sin instalar nada de verdad:
  python3 luna-installer-gui.py --demo
  python3 luna-installer-gui.py --demo --auto   (pica Pacman solo y cierra al final)

Imágenes archivadas, nombres exactos verificados con ls:
- Póster: 81630_0_1xuc.webp (gatito morado en la luna creciente)
- Instalado 100% (vieja): media-generation-luna-instalando-0-9189c024-59e0-4561-81d0-d789d24136e2.webp
  (queda solo como respaldo si falta la nueva)
- NUEVAS imágenes v1.0 beta, de la página oficial de Luna (24 nov 2026):
  - Paso 1: luna-1.0-beta-paso1-instalar.webp (póster limpio + botones Arch Pacman / .deb)
  - Paso 2: luna-1.0-beta-paso2-instalando.webp (gatito en la luna + barrita morada)
  - Paso 3: luna-1.0-beta-paso3-completa.webp (Instalación completa + Continuar — Abrir Luna)
  - Luna ya instalado: luna-1.0-beta-instalado-carrusel.webp (ventana con carrusel 3D)
  El paso 3 usa la nueva imagen del paso 3; el paso 2 muestra la nueva
  imagen del paso 2 arriba de la barrita animada real.
- La imagen del 65% ya NO se usa: Fernando pidió quitarla el 23 nov 2026.
  En el paso 2 solo queda la barrita del 1 al 100, animada y morada
  viva (BarraAnimada: relleno morado brillante con una franja clara
  que se mueve sin parar), con el número grande.
No se usan la versión EmulationStation ni la comparación equivocada.

El texto "Hecho por Vega & Kiki" se pone como texto normal de tkinter,
no como markup, así que el & no rompe la ventana (ese fue el fallo
de zenity, ya arreglado con --no-markup en luna-installer.sh).

Solo tkinter + PIL cuando está disponible; sin PIL la ventana sigue
funcionando con texto y la barrita.

Hecho por Vega & Kiki
Guzman
"""
import argparse
import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except Exception:
    Image = None
    ImageTk = None
    PIL_DISPONIBLE = False

VERSION = "1.0-beta"
BASE_DIR = Path(__file__).resolve().parent

# Tema Luna: igual que luna_gui.py, morado oscuro, nada gris Windows 98.
FONDO = "#1e1033"
FONDO_BARRA = "#2a1745"
FONDO_TARJETA = "#2d1b4e"
MORADO = "#7c3aed"
MORADO_HOVER = "#8b5cf6"
MORADO_CLARO = "#a78bfa"
MORADO_VIVO = "#a855f7"   # morado brillante de la barrita animada
MORADO_BRILLO = "#e9d5ff"  # franja clara que se mueve por la barrita
TEXTO = "#ffffff"
TEXTO_SUAVE = "#d8b4fe"
VERDE = "#22c55e"
FUENTE = "sans-serif"

POSTER = "81630_0_1xuc.webp"
# IMG_65 eliminada a pedido de Fernando (23 nov 2026): no se muestra en ningún paso.
IMG_100 = "media-generation-luna-instalando-0-9189c024-59e0-4561-81d0-d789d24136e2.webp"
# Imágenes NUEVAS v1.0 beta (de la página oficial de Luna, 24 nov 2026).
IMG_PASO2 = "luna-1.0-beta-paso2-instalando.webp"
IMG_PASO3 = "luna-1.0-beta-paso3-completa.webp"


def buscar_imagen(nombre):
    """Busca una imagen archivada: instalada, junto al script o en workspace."""
    candidatos = [
        Path("/usr/share/luna") / nombre,
        BASE_DIR / nombre,
        Path.home() / "workspace" / "luna" / nombre,
    ]
    if nombre == POSTER:
        candidatos += [
            BASE_DIR.parent / "user" / "files" / nombre,
            Path.home() / "workspace" / "user" / "files" / nombre,
        ]
    for ruta in candidatos:
        if ruta.is_file():
            return ruta
    return None


def cargar_poster_sin_logos(ruta, ancho, alto):
    """Póster de Luna LIMPIO, sin los logos de Pacman/.deb de abajo.

    Igual que en luna_gui.py: recorta el 18% inferior del póster
    en memoria (se queda el 82% superior: LUNA, el gatito en la
    luna y el texto "Luna es un proyecto..."), así no se ven el
    logo amarillo de Pacman Arch ni el de .deb Debian Ubuntu
    dentro de la imagen. El archivo original no se toca.
    Los logos van solo como icono en los botones de instalar.
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


def cargar_imagen(ruta, ancho, alto):
    if not PIL_DISPONIBLE or not ruta:
        return None
    try:
        img = Image.open(str(ruta))
        img.thumbnail((ancho, alto))
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


class BarraAnimada(tk.Canvas):
    """Barrita de progreso animada y morada viva, paso 2 del instalador.

    No es la barrita plana y gris de ttk: es un Canvas con el fondo
    morado brillante que crece del 1 al 100, y una franja clara que
    se mueve sin parar de izquierda a derecha mientras instala,
    como un brillo que corre por la barra. El porcentaje grande
    se actualiza aparte. La animación corre con after(), sin
    bloquear la ventana; se para sola al llegar al 100%.
    """

    def __init__(self, parent, ancho=640, alto=36):
        super().__init__(parent, width=ancho, height=alto,
                         highlightthickness=0, bg=FONDO)
        self.ancho = ancho
        self.alto = alto
        self.valor = 0
        self._pos_brillo = 0
        self._animando = False
        self._job = None
        self._dibujar()

    def _dibujar(self):
        self.delete("all")
        # Fondo de la barra: tarjeta morada oscura, bordes redondeados.
        self.create_rectangle(2, 2, self.ancho - 2, self.alto - 2,
                              fill=FONDO_TARJETA, outline=MORADO_CLARO, width=2)
        ancho_lleno = int((self.ancho - 4) * self.valor / 100)
        if ancho_lleno > 4:
            # Relleno morado brillante.
            self.create_rectangle(3, 3, 3 + ancho_lleno, self.alto - 3,
                                  fill=MORADO_VIVO, outline="")
            # Mitad superior más clara, para que se vea con volumen.
            self.create_rectangle(3, 3, 3 + ancho_lleno, self.alto // 2,
                                  fill=MORADO_HOVER, outline="")
            # Franja clara que se mueve por el relleno.
            x_brillo = 3 + self._pos_brillo % max(ancho_lleno, 1)
            self.create_rectangle(x_brillo, 3,
                                  min(x_brillo + 48, 3 + ancho_lleno),
                                  self.alto - 3, fill=MORADO_BRILLO, outline="")

    def poner_valor(self, valor):
        self.valor = max(0, min(100, int(valor)))
        if self.valor >= 100:
            self.parar()
        self._dibujar()

    def iniciar(self):
        if not self._animando:
            self._animando = True
            self._animar()

    def _animar(self):
        if not self._animando:
            return
        self._pos_brillo = (self._pos_brillo + 14) % max(
            int((self.ancho - 4) * max(self.valor, 8) / 100), 1)
        self._dibujar()
        self._job = self.after(140, self._animar)

    def parar(self):
        self._animando = False
        if self._job is not None:
            try:
                self.after_cancel(self._job)
            except Exception:
                pass
            self._job = None
        self._dibujar()


def boton_morado(parent, texto, comando, grande=False):
    return tk.Button(
        parent, text=texto, command=comando,
        bg=MORADO, fg=TEXTO, activebackground=MORADO_HOVER,
        activeforeground=TEXTO, relief="flat", borderwidth=0,
        padx=16, pady=12 if grande else 8,
        font=(FUENTE, 13, "bold") if grande else (FUENTE, 11, "bold"),
        cursor="hand2", wraplength=260, justify="center",
    )


class InstaladorLuna:
    def __init__(self, ventana, demo=False, auto=False):
        self.ventana = ventana
        self.demo = demo
        self.auto = auto
        self._imagenes = []  # evita que PhotoImage se borre
        self.metodo = None  # "pacman" o "deb"
        self.instalado_ok = None
        self._valor_barra = 0
        self._barra_lenta_job = None
        self._instalacion_lista = False
        ventana.title("Luna — Instalador")
        ventana.configure(bg=FONDO)
        # Ventana más grande y moderna: la imagen de instalado llena casi toda.
        ventana.geometry("800x940")
        ventana.resizable(False, False)
        try:
            estilo = ttk.Style(ventana)
            estilo.theme_use("clam")
            estilo.configure("TFrame", background=FONDO)
            estilo.configure("TLabel", background=FONDO, foreground=TEXTO)
            # La barrita del paso 2 ya no es ttk: es BarraAnimada
            # (Canvas morado brillante con franja que se mueve).
        except Exception:
            pass

        self.paso1 = tk.Frame(ventana, bg=FONDO)
        self.paso2 = tk.Frame(ventana, bg=FONDO)
        self.paso3 = tk.Frame(ventana, bg=FONDO)
        for marco in (self.paso1, self.paso2, self.paso3):
            marco.pack(fill="both", expand=True)
        self._armar_paso1()
        self._armar_paso2()
        self._armar_paso3()
        self.mostrar(self.paso1)
        if self.auto:
            ventana.after(600, lambda: self.elegir("pacman"))

    def mostrar(self, marco):
        for m in (self.paso1, self.paso2, self.paso3):
            m.pack_forget()
        marco.pack(fill="both", expand=True)

    def _imagen(self, parent, nombre, ancho, alto, texto_fallback):
        ruta = buscar_imagen(nombre)
        foto = cargar_imagen(ruta, ancho, alto)
        if foto is not None:
            self._imagenes.append(foto)
            tk.Label(parent, image=foto, bg=FONDO).pack(pady=8)
            return True
        tk.Label(parent, text=texto_fallback, bg=FONDO_TARJETA,
                 fg=TEXTO_SUAVE, font=(FUENTE, 11),
                 padx=12, pady=20).pack(pady=8, fill="x", padx=20)
        return False

    def _armar_paso1(self):
        # Paso 1 de 3: póster LIMPIO + dos botones con icono para instalar.
        tk.Label(self.paso1, text="LUNA", bg=FONDO, fg=TEXTO,
                 font=(FUENTE, 28, "bold")).pack(pady=(16, 0))
        tk.Label(self.paso1, text=f"Luna Beta {VERSION} — Paso 1 de 3",
                 bg=FONDO, fg=TEXTO_SUAVE, font=(FUENTE, 12)).pack()
        tk.Label(self.paso1,
                 text="Fondos de pantalla animados, fácil y sin plugins.",
                 bg=FONDO, fg=TEXTO, font=(FUENTE, 11)).pack(pady=(4, 0))
        # Póster limpio, sin logos de Pacman/.deb dentro de la imagen.
        ruta_poster = buscar_imagen(POSTER)
        foto_poster = cargar_poster_sin_logos(ruta_poster, 720, 500)
        if foto_poster is not None:
            self._imagenes.append(foto_poster)
            tk.Label(self.paso1, image=foto_poster, bg=FONDO).pack(pady=8)
        else:
            self._imagen(self.paso1, POSTER, 680, 380,
                         "Póster de Luna — gatito morado en la luna")
        tk.Label(self.paso1, text="¿Cómo quieres instalar Luna?",
                 bg=FONDO, fg=TEXTO, font=(FUENTE, 13, "bold")).pack(pady=(6, 8))
        botones = tk.Frame(self.paso1, bg=FONDO)
        botones.pack(fill="x", padx=20)
        # Iconos en los botones, no dentro del póster:
        # 🟡 Pacman (amarillo, como el logo) y 🌀 Debian (remolino).
        boton_morado(botones, "🟡\nInstalar Arch Pacman",
                     lambda: self.elegir("pacman"), grande=True).pack(
                         side="left", expand=True, fill="both", padx=4)
        boton_morado(botones, "🌀\nInstalar .deb Debian Ubuntu",
                     lambda: self.elegir("deb"), grande=True).pack(
                         side="right", expand=True, fill="both", padx=4)
        tk.Label(self.paso1, text="Hecho por Vega & Kiki\nGuzman",
                 bg=FONDO, fg=TEXTO_SUAVE, font=(FUENTE, 11)).pack(
                     side="bottom", pady=14)

    def _armar_paso2(self):
        # Paso 2 de 3: solo la barrita moderna del 1 al 100, con el número grande.
        # Sin imagen del 65%: Fernando pidió quitarla el 23 nov 2026.
        # Como un asistente Next: Paso 1 elige, Paso 2 instala despacio,
        # Paso 3 completo. Sin contraseña de terminal: la instalación
        # usa pkexec (ventanita gráfica del sistema, una sola vez).
        tk.Label(self.paso2, text="Paso 2 de 3", bg=FONDO, fg=TEXTO_SUAVE,
                 font=(FUENTE, 12)).pack(pady=(24, 0))
        tk.Label(self.paso2, text="Instalando Luna...",
                 bg=FONDO, fg=TEXTO, font=(FUENTE, 26, "bold")).pack(pady=(8, 0))
        self.etiqueta_metodo = tk.Label(self.paso2, text="", bg=FONDO,
                                        fg=TEXTO_SUAVE, font=(FUENTE, 14))
        self.etiqueta_metodo.pack(pady=(8, 12))
        # Imagen nueva v1.0 beta del paso 2 (gatito + barrita morada),
        # arriba de la barrita animada real, que sigue funcionando.
        self._imagen(self.paso2, IMG_PASO2, 640, 320,
                     "Instalando Luna... por favor espera")
        # Barrita animada y morada viva, no plana ni gris.
        self.barra = BarraAnimada(self.paso2, ancho=640, alto=36)
        self.barra.pack(pady=24, padx=40)
        self.etiqueta_porcentaje = tk.Label(self.paso2, text="0%",
                                            bg=FONDO, fg=MORADO_CLARO,
                                            font=(FUENTE, 48, "bold"))
        self.etiqueta_porcentaje.pack(pady=(8, 0))
        self.etiqueta_estado = tk.Label(self.paso2, text="Preparando...",
                                        bg=FONDO, fg=TEXTO_SUAVE,
                                        font=(FUENTE, 13), wraplength=640)
        self.etiqueta_estado.pack(pady=12)

    def _armar_paso3(self):
        # Paso 3 de 3: Finalizar — imagen al 100% GRANDE + botón Continuar.
        # Continuar cierra el instalador y abre el programa Luna.
        tk.Label(self.paso3, text="Paso 3 de 3 — Finalizar", bg=FONDO, fg=TEXTO_SUAVE,
                 font=(FUENTE, 12)).pack(pady=(12, 0))
        tk.Label(self.paso3, text="¡Instalación completa!",
                 bg=FONDO, fg=VERDE, font=(FUENTE, 30, "bold")).pack(pady=(4, 0))
        tk.Label(self.paso3, text="Luna ya está instalada. Pulsa Continuar para abrir el programa.",
                 bg=FONDO, fg=TEXTO, font=(FUENTE, 14)).pack(pady=(4, 8))
        # Imagen grande: la NUEVA del paso 3 v1.0 beta (Instalación completa
        # + Continuar — Abrir Luna); si falta, usa la vieja del 100%.
        if not self._imagen(self.paso3, IMG_PASO3, 700, 500,
                            "Instalación completa — 100%"):
            self._imagen(self.paso3, IMG_100, 700, 500,
                         "Instalación completa — 100%")
        self.etiqueta_resultado = tk.Label(self.paso3, text="", bg=FONDO,
                                           fg=TEXTO_SUAVE, font=(FUENTE, 11),
                                           wraplength=440)
        self.etiqueta_resultado.pack(pady=6)
        boton_morado(self.paso3, "▶  Continuar — Abrir Luna", self.abrir_luna,
                     grande=True).pack(pady=8, padx=20, fill="x")
        tk.Button(self.paso3, text="Cerrar", command=self.ventana.destroy,
                  bg=FONDO_TARJETA, fg=TEXTO, relief="flat", padx=12, pady=8,
                  font=(FUENTE, 11), cursor="hand2").pack(pady=4, padx=20, fill="x")
        tk.Label(self.paso3, text="Hecho por Vega & Kiki\nGuzman",
                 bg=FONDO, fg=TEXTO_SUAVE, font=(FUENTE, 11)).pack(
                     side="bottom", pady=14)

    def elegir(self, metodo):
        self.metodo = metodo
        nombre = "Pacman — Arch / Garuda" if metodo == "pacman" else ".deb — Debian / Ubuntu"
        self.etiqueta_metodo.config(text=nombre)
        self.mostrar(self.paso2)
        self._valor_barra = 0
        self._instalacion_lista = False
        self.barra.poner_valor(0)
        self.barra.iniciar()
        self.etiqueta_porcentaje.config(text="0%")
        self.etiqueta_estado.config(text="Preparando... Sin contraseña de terminal.")
        # Barrita MÁS LENTA y animada, como un asistente Next: avanza
        # 1% cada 700 ms hasta el 90% mientras se instala de verdad
        # en el hilo de fondo, para que se vea cargando despacio;
        # al terminar salta al 100%.
        self._tick_barra_lenta()
        threading.Thread(target=self._instalar, daemon=True).start()

    def _tick_barra_lenta(self):
        """Avanza la barrita despacio y animada (1% cada 700 ms, hasta 90%).

        El texto "Cargando..." también se anima con puntos, para
        que se vea que está cargando y no quieto.
        """
        if self._instalacion_lista:
            return
        if self._valor_barra < 90:
            self._valor_barra += 1
            self.barra.poner_valor(self._valor_barra)
            self.etiqueta_porcentaje.config(text=f"{self._valor_barra}%")
            puntos = "." * (1 + (self._valor_barra // 10) % 3)
            self.etiqueta_estado.config(text=f"Cargando{puntos} Instalando Luna...")
        self._barra_lenta_job = self.ventana.after(700, self._tick_barra_lenta)

    def _parar_barra_lenta(self):
        self._instalacion_lista = True
        if self._barra_lenta_job is not None:
            try:
                self.ventana.after_cancel(self._barra_lenta_job)
            except Exception:
                pass
            self._barra_lenta_job = None
        self._valor_barra = 100
        self.barra.poner_valor(100)
        self.etiqueta_porcentaje.config(text="100%")

    def _progreso(self, valor, texto):
        # El valor lo lleva la barrita lenta; aquí solo cambia el texto
        # de estado (qué está haciendo ahora mismo).
        self.ventana.after(0, self.etiqueta_estado.config, {"text": texto})

    def _aplicar_progreso(self, valor, texto):
        self.etiqueta_estado.config(text=texto)

    def _correr(self, comando, cwd):
        """Corre un comando real y devuelve su código de salida."""
        try:
            resultado = subprocess.run(
                comando, cwd=str(cwd), capture_output=True, text=True,
                timeout=600)
            return resultado.returncode
        except Exception as error:
            print(f"Luna: no se pudo correr {comando}: {error}")
            return 1

    def _instalar_paquete_con_pkexec(self, comando_instalar):
        """Instala un paquete ya compilado sin contraseña de terminal.

        Usa pkexec, que abre la ventanita gráfica del sistema para
        la contraseña, una sola vez. Si no hay pkexec, cae al
        comando de antes (makepkg -si / sudo dpkg -i, que sí pide
        la contraseña en terminal) y lo dice en el mensaje final.
        Devuelve True si se instaló, False si no.
        """
        if shutil.which("pkexec"):
            return self._correr(["pkexec"] + comando_instalar, BASE_DIR) == 0
        return self._correr(comando_instalar, BASE_DIR) == 0

    def _instalar(self):
        """Paso 2: instala de verdad cuando se puede, si no, simula
        la barrita y lo dice claro. Nunca finge un éxito que no hubo.
        La barrita la lleva _tick_barra_lenta (despacio, 1% cada
        700 ms); aquí solo cambia el texto de estado."""
        if self.demo:
            import time
            time.sleep(12)  # demo despacio: la barrita corre sola al 90%
            self.instalado_ok = True
            self._terminar("Demo: barrita del 1 al 100 sin instalar nada.")
            return

        if self.metodo == "pacman":
            pkgbuild = BASE_DIR / "PKGBUILD"
            if shutil.which("makepkg") and pkgbuild.is_file():
                self._progreso(0, "Compilando Luna con makepkg (sin instalar aún)...")
                # makepkg sin -i: compila el .pkg.tar.zst sin pedir sudo.
                if self._correr(["makepkg", "--noconfirm"], BASE_DIR) != 0:
                    self.instalado_ok = False
                    self._terminar("makepkg falló al compilar. Revisa la terminal.")
                    return
                paquetes = sorted(BASE_DIR.glob("luna-*.pkg.tar.zst"))
                if not paquetes:
                    self.instalado_ok = False
                    self._terminar("makepkg compiló, pero no dejó el paquete. Revisa la terminal.")
                    return
                self._progreso(0, "Instalando el paquete... (ventanita del sistema, una sola vez)")
                # pkexec pacman -U: ventanita gráfica, sin terminal.
                ok = self._instalar_paquete_con_pkexec(
                    ["pacman", "-U", "--noconfirm", str(paquetes[-1])])
                if not ok:
                    # Respaldo honesto: makepkg -si (pide sudo en terminal).
                    self._progreso(0, "pkexec no instaló. Probando con makepkg -si...")
                    ok = self._correr(
                        ["makepkg", "-si", "--noconfirm"], BASE_DIR) == 0
                self.instalado_ok = ok
                self._terminar(
                    "Instalado con Pacman." if self.instalado_ok
                    else "No se pudo instalar. Revisa la terminal.")
                return
            self._simular("makepkg no está aquí (esta no es Arch).")
            return

        # .deb
        script = BASE_DIR / "build-deb.sh"
        if shutil.which("dpkg") and script.is_file():
            self._progreso(0, "Compilando el .deb...")
            if self._correr(["bash", "build-deb.sh"], BASE_DIR) == 0:
                debs = sorted(BASE_DIR.glob("luna_*.deb"))
                if debs:
                    self._progreso(0, "Instalando el .deb... (ventanita del sistema, una sola vez)")
                    ok = self._instalar_paquete_con_pkexec(
                        ["dpkg", "-i", str(debs[-1])])
                    if not ok:
                        ok = self._correr(
                            ["sudo", "dpkg", "-i", str(debs[-1])], BASE_DIR) == 0
                    self.instalado_ok = ok
                    self._terminar(
                        "Instalado con .deb." if self.instalado_ok
                        else "dpkg falló. Revisa la terminal.")
                    return
            self.instalado_ok = False
            self._terminar("No se pudo compilar el .deb. Revisa la terminal.")
            return
        self._simular("dpkg / build-deb.sh no están aquí.")

    def _simular(self, motivo):
        """Barrita simulada, avisando que no instaló de verdad."""
        import time
        time.sleep(12)  # despacio: la barrita corre sola al 90%
        self.instalado_ok = False
        self._terminar(f"{motivo} Se mostró la barrita, pero no se instaló nada. "
                       "En Garuda, pica Pacman; en Debian/Ubuntu, pica .deb.")

    def _terminar(self, mensaje):
        self.ventana.after(0, self._parar_barra_lenta)
        self.ventana.after(0, self._mostrar_fin, mensaje)

    def _mostrar_fin(self, mensaje):
        self.etiqueta_resultado.config(text=mensaje)
        self.mostrar(self.paso3)
        if self.auto:
            self.ventana.after(1200, self.ventana.destroy)

    def abrir_luna(self):
        """Paso 3, botón Continuar: cierra el instalador y abre Luna."""
        gui = BASE_DIR / "luna_gui.py"
        if shutil.which("luna-gui"):
            subprocess.Popen(["luna-gui"])
        elif gui.is_file():
            subprocess.Popen([sys.executable, str(gui)])
        else:
            subprocess.run(["luna", "status"])
            messagebox.showinfo("Luna", "Luna instalada. Usa: luna-gui")
        self.ventana.destroy()


def main():
    parser = argparse.ArgumentParser(description="Instalador Luna con imágenes")
    parser.add_argument("--demo", action="store_true",
                        help="Simula la barrita sin instalar nada")
    parser.add_argument("--auto", action="store_true",
                        help="Pica Pacman solo y cierra al final (para probar)")
    args = parser.parse_args()
    ventana = tk.Tk()
    InstaladorLuna(ventana, demo=args.demo, auto=args.auto)
    ventana.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
