# Luna v1.0 beta

Fondos de pantalla animados en Linux, fácil y sin plugins.

Luna es una app para poner fondos de pantalla animados, fácil y sin plugins, para el usuario común: solo pica, no escribe comandos en la terminal.

> **Beta:** Luna v1.0 beta. Todavía es Beta, pero ya funciona bien.

## Qué hace Luna

- Pone una imagen o un video como fondo de pantalla, automáticamente.
- Carrusel 3D para elegir tu fondo.
- Clic derecho en una imagen o video: **Poner con Luna** lo pone como fondo, y **Abrir Luna** abre la ventana.
- Luna va directo al menú **Inicio > Utilidades**.
- Pausa inteligente, multi-monitor, volumen / silencio.
- Mejoras de video: escalado IA, nitidez, estabilización, reducción de ruido, HDR y desenfoque.

## Formatos

- Imágenes: JPG, PNG, WEBP, GIF, BMP y SVG.
- Videos: MP4, MKV, WEBM, MOV y AVI.

## Cómo se usa

1. Abre Luna desde **Inicio > Utilidades**.
2. Pica **Agregar Carpeta** en la barra superior y elige la carpeta donde tienes tus imágenes. Se cargan todas las imágenes y videos de esa carpeta.
3. Elige tu fondo en el carrusel 3D.
4. Pica **Poner Imagen en el Fondo de Pantalla**.

O, más fácil todavía: haz clic derecho en una imagen o video y elige **Poner con Luna**.

## Instalación en solo 3 pasos

1. **Instalar:** pica Instalar Arch Pacman o Instalar .deb. La contraseña va al instalador, no se pide en la terminal.
2. **Proceso:** barrita animada, despacio, instalando Luna.
3. **Continuar / Finalizar:** pica Continuar — Abrir Luna, y se abre el programa.

## Comandos

### Arch / Pacman

```bash
sudo pacman -S luna
```

### Debian / Ubuntu (.deb)

```bash
sudo apt install luna
```

### Chaotic-AUR — Próximamente

```bash
sudo pacman -S luna
```

Luna aún no está en Chaotic-AUR. Este comando es para cuando esté publicada ahí.

### Flatpak — Próximamente

```bash
flatpak install flathub io.github.guzmankaza.Luna
```

Luna aún no está en Flathub. Este comando es para cuando esté publicada ahí.

> Luna aún no está en AUR, Chaotic-AUR ni Flathub. Para la Beta, se instala con el comando único de Luna Launcher (makepkg), que viene en la página oficial.

## Instalación desde el código (Beta)

En Arch / Garuda:

```bash
makepkg -si
```

En Debian / Ubuntu:

```bash
./build-deb.sh
sudo dpkg -i luna_1.0_all.deb
```

## Archivos

- `luna.py` — comandos `luna set`, `luna stop`, `luna list`, `luna status`
- `luna_gui.py` — ventana de Luna
- `luna-installer-gui.py` y `luna-installer.sh` — instalador en 3 pasos
- `luna_ascii.py` — bienvenida en ASCII en la terminal
- `PKGBUILD` — paquete para Arch / Pacman
- `build-deb.sh` y `debian/` — paquete .deb para Debian / Ubuntu
- `luna.desktop` y `luna-utilidades.desktop` — menú Inicio > Utilidades
- `luna-clic-derecho.desktop` — clic derecho Poner con Luna / Abrir Luna
- `PAGINA_LUNA.md` — descripción completa del programa

---

Hecho por Vega & Kiki
Guzman
