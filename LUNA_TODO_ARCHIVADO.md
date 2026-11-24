# Luna — Todo archivado

Fecha: 21 nov 2026
Carpeta: `~/workspace/luna/`

## Resumen

Luna es un proyecto para poner fondos de pantalla animados, fácil y sin plugins.
Para Arch (Pacman) y Debian/Ubuntu (.deb).
Hace algo similar a Hidamari y al fondo de video de KDE, pero fácil para el usuario común.

## Archivos de resumen

- `ARCHIVO_LUNA.md` — los 3 pasos con imágenes y las funciones.
- `COMPARACION_LUNA.md` — comparación Luna vs Hidamari vs el fondo de video de KDE.

## Paso 1 — Base del proyecto

- Póster original: `../user/files/81630_0_1xuc.webp`
- Video del póster: `media-generation-luna-paso1-poster-0-bef26f93-8163-4f69-8e35-5f7f795baed1.mp4`

## Paso 2 — Diseño del instalador

- Instalando 65% con barrita: `media-generation-luna-instalando-proceso-0-f3b3df9d-f2c3-4ba1-bcb5-04792240cd4e.webp`
- Instalando 100% completado: `media-generation-luna-instalando-0-9189c024-59e0-4561-81d0-d789d24136e2.webp`
- Video del 1 al 100: `media-generation-luna-instalando-1-100-0-88194f11-e317-4a08-8d46-1dcd4d49950e.mp4`
- Video instalador termina y se abre el programa: `media-generation-luna-instalador-abre-programa-0-6256ca65-03b9-45f1-a10b-5473374cf697.mp4`

## Paso 3 — Interfaz y herramientas

- Interfaz Biblioteca con carrusel: `media-generation-luna-interfaz-biblioteca-carru-0-d4ecef1d-d3e4-4f88-ad0f-ff0eb604b6c9.webp`
- Ajustes abre otra pantalla: `media-generation-luna-interfaz-principal-sin-aj-0-28c0b2be-1eb8-4c11-b15e-bedab79e8958.webp`
- Botón Poner Imagen en el Fondo de Pantalla: `media-generation-luna-boton-poner-fondo-0-11ddadff-28ca-482e-a90a-c26fadac4ebb.webp`
- Carrusel arriba, vista previa abajo: `media-generation-luna-carrusel-arriba-vista-aba-0-3c945284-96d3-4a07-bf84-4484e9565451.webp`
- Primera interfaz de referencia: `../user/files/81463_3_hnje.webp`
- Versión con emulación, NO usar: `media-generation-luna-interfaz-emulationstation-0-8399930c-9287-4ec2-b07a-749733b8a8cb.webp`

## Funciones del programa

- Instalador fácil .deb / .pacman, sin terminal, al terminar abre Luna.
- Clic derecho en escritorio: Poner Luna como Fondo de Escritorio, Establecer Imagen como Fondo, Establecer Video como Fondo, Abrir con Luna Biblioteca.
- Automático al elegir video o imagen en la Biblioteca.
- Todos los formatos: JPG, PNG, WEBP, GIF, BMP, SVG / MP4, MKV, WEBM, MOV, AVI.
- Mejoras de video: escalado IA, nitidez, estabilización, reducción de ruido, HDR, pausa inteligente, volumen, multi-monitor.
- Archivo de funciones: `media-generation-luna-clic-derecho-fondo-automa-0-651e12c0-6c62-4cd6-8dee-7c0085df28d9.webp`

## Ventana GUI archivada 22 nov 2026
- `luna_gui.py` (19K, probado con py_compile OK) — ventana Luna Beta 0.1.0-beta, con imágenes archivadas: póster gatito morado en Acerca, 7 imágenes de diseño en "Ver diseño de Luna", carrusel arriba con miniaturas reales JPG/PNG/WEBP/GIF/BMP, vista previa abajo, botón Poner Imagen en el Fondo de Pantalla (llama a `luna set`), Ajustes en ventana aparte con Cerrar/Guardar, Próximamente, Acerca, y abajo "Hecho por Vega & Kiki". Videos y SVG siguen con texto de respaldo. Abrir con `python3 luna_gui.py`.
- `luna-installer.sh` — instalador con ventanita zenity del 1 al 100, arreglado con --no-markup por el `&` de Vega & Kiki.
- Rediseño 22 nov 2026: `luna_gui.py` ya no es gris estilo Windows 98; ahora es morado oscuro Luna (#1e1033, botones #7c3aed, texto blanco), con el póster del gatito en la cabecera. Probado con py_compile y 10 s bajo Xvfb sin errores.
- Menú Utilidades 22 nov 2026: `luna-utilidades.desktop` con Exec=luna-gui, Categories=Utility; el PKGBUILD (pkgrel=2) instala `luna_gui.py` como /usr/bin/luna-gui y ese .desktop como /usr/share/applications/luna.desktop, y añade tk y python-pillow a depends. Simulación de instalación verificada en /tmp/pkgroot. makepkg no se pudo probar aquí (VM Debian, no hay makepkg); hay que compilarlo en Garuda.

## No usar

- `media-generation-luna-comparacion-hidamari-smar-0-a38b4f06-11fa-4739-b103-9e0c9a563096.webp` — imagen generada equivocada, de estudiar en casa vs biblioteca. La comparación correcta está en `COMPARACION_LUNA.md`.

## Instalación como programa — 22 nov 2026 (noche)
- PKGBUILD pkgrel 4: instala todo en su lugar (/usr/bin/luna, /usr/bin/luna-gui, /usr/lib/luna/, /usr/share/luna/ con las 8 imágenes, menú Utilidades, clic derecho KDE, servicio). Corregido: luna_gui.py ahora busca las imágenes primero en /usr/share/luna/ (antes solo junto al script, y tras instalar no las encontraba); luna.service ahora apunta a /usr/bin/luna (antes /usr/local/bin/luna).
- `luna-instalar-programa.sh`: descarga el paquete a una carpeta temporal, instala con `sudo pacman -U`, limpia, no deja archivos sueltos en ~/Descargas. El enlace real del paquete aún no existe (falta servidor).
- `repo-arch/`: estructura del repo Pacman lista (x86_64/luna.db.tar.gz con Luna, README con las 2 formas de instalar). Falta el .pkg.tar.zst, que solo se puede compilar en Garuda con `makepkg -si` (esta máquina es Debian, no hay makepkg). Nada publicado en AUR/GitHub.

## Actualización — 24 nov 2026

### Instalador — solo 3 pasos
1. **Instalar:** el link solo pide el comando. La contraseña no se escribe en la terminal: va al instalador por `pkexec`, la ventanita gráfica del sistema, una sola vez. Si no hay pkexec, cae a `sudo` y lo dice claro. Póster limpio, sin los logos de Pacman Arch ni .deb dentro de la imagen (recortado al 82% en memoria, el archivo original no se toca), y dos botones grandes con icono: 🟡 Instalar Arch Pacman y 🌀 Instalar .deb Debian Ubuntu.
2. **Proceso / barra:** barrita animada despacio, 1% cada 700 ms hasta el 90% mientras instala de verdad, y salta al 100% al terminar. Texto animado "Cargando... Instalando Luna...". En Arch compila con `makepkg` sin `-i` (no pide sudo) y luego instala el paquete con `pkexec pacman -U`. En .deb igual, con `pkexec dpkg -i`.
3. **Continuar / Finalizar:** botón grande "▶ Continuar — Abrir Luna" que cierra el instalador y abre el programa Luna. El respaldo zenity/terminal (`luna-installer.sh`) también termina con Continuar y abre `luna-gui`.
- Al instalar, Luna queda en el **menú Utilidades** (`luna-utilidades.desktop`, `Exec=luna-gui`, `Categories=Utility;`, instalado como `/usr/share/applications/luna.desktop`).
- **Clic derecho en el escritorio:** sobre una imagen o un video, "Poner con Luna" (`luna set %f`) la pone como fondo ahí mismo; también "Abrir Biblioteca de Luna" (`luna list`). `luna-clic-derecho.desktop`, instalado por el PKGBUILD en `/usr/share/kservices5/ServiceMenus/`.
- PKGBUILD: `0.1.0_beta`, **pkgrel 5**. Corrección del 23 nov: la imagen del 65% ya no se usa ni se lista en `source` (antes `makepkg` fallaba porque la pedía y no estaba en el zip).
- `luna-install.sh`: comando único de instalación. Descarga el zip a `/tmp/luna-install`, descomprime, `makepkg`, instala con `pkexec pacman -U`, corre el instalador gráfico y limpia. Apunta a `luna-launcher3.zip` (última versión corregida).
- Límite honesto: el flujo con `pkexec` no se pudo probar en esta máquina (Debian, sin makepkg ni pkexec de Arch); en Garuda debe salir la ventanita gráfica del sistema.

### Ventana GUI — cambios del 24 nov 2026
- **Barrita del paso 2 más lenta y animada:** 1% cada 700 ms (antes 300 ms), con brillo que corre más despacio por la barra.
- **Sin "Sin carpeta":** la etiqueta de la barra superior queda vacía al inicio y solo muestra la ruta cuando se elige una carpeta con Agregar Carpeta.
- **Funciones de Luna dentro de Acerca, como submenú:** se quitó el botón aparte "✨ Funciones de Luna" de la ventana principal. Acerca ahora tiene dos pestañas arriba: 🐱 Acerca (póster grande + toda la información) y ✨ Funciones (las 14 funciones del Paso 4, de `PAGINA_LUNA.md` / `COMPARACION_LUNA.md`, sin video de YouTube ni página web como fondo).
- **Sin sonido en Ajustes:** salieron el checkbox de volumen/silencio y el deslizador de volumen de Ajustes. El sonido queda solo en la ventana principal (botón Sonido/Silencio + deslizador de la barra superior).
- **Mejoras de video activadas en Ajustes:** nueva sección "Mejoras de video" con interruptores de verdad, guardados en `~/.config/luna/ajustes.json`: mejoras de video activadas, Escalado IA, Nitidez, Estabilización, Reducción de ruido, HDR y Desenfoque (blur). Todos activados por defecto salvo blur. También se activaron Pausa inteligente por batería y por pantalla apagada, Multi-monitor e Inicio automático.
- **Póster e imágenes más grandes:** Acerca, póster de 440×660 a **560×780**, ventana de 660×880 a 720×960; cabecera de la GUI, póster de 72×72 a **120×120**; instalador paso 1, póster de 680×380 a **720×500**, ventana de 800×940.
- Se mantiene: solo carrusel 3D (sin Biblioteca, sin Vista previa, sin cuadrícula), botón 🖼 Poner Imagen en el Fondo de Pantalla, Agregar Carpeta solo en la barra superior, búsqueda, Aleatorio, Agregar Fondo, Quitar, Ajustes aparte, Acerca aparte, tema morado moderno con iconos, y al final "Hecho por Vega & Kiki / Guzman".
- Probado: `py_compile` OK en `luna_gui.py` y `luna-installer-gui.py`; ventana principal bajo Xvfb sin "Sin carpeta" ni botón Funciones suelto; instalador `--demo --auto` llega al 100% y cierra, salida 0.

### Bienvenida ASCII en la terminal — 24 nov 2026
- `luna_ascii.py` + `luna_ascii.txt`: estilo shell, en la terminal. Al pegar el comando se limpia la pantalla, se ve el póster de Luna en ASCII (solo caracteres `@ # * + = - : .`, en morado sobre fondo negro), y abajo dice "Bienvenido a Luna", "LUNA Beta 0.1.0-beta", "Fondos de pantalla animados, fácil y sin plugins" y "Hecho por Vega & Kiki / Guzman".
- Abajo pregunta: `¿Quieres instalar Luna? [S/n]:`
- Si dice que sí, hace `sudo pacman -S luna` en la terminal (la contraseña se pide ahí, en la terminal). Si pacman dice que no encontró el paquete, lo dice claro y ofrece instalar con Luna Launcher (makepkg), sin fingir que quedó instalada. Después de instalar, abre Luna con `luna-gui`. Si dice que no, muestra "No se instaló Luna." y sale.
- Probado con `n` y con `s` con un pacman falso que falla: el flujo de la pregunta funciona; no se instaló nada de verdad en esta máquina Debian.

### Guzman abajo, en todo el programa
- Abajo, en todo el programa igual: **"Hecho por Vega & Kiki / Guzman"**. En la ventana de Luna (pie y Acerca), en el instalador (pasos 1 y 3), en la terminal ASCII, en `luna.py`, en `luna-installer.sh` y `luna-instalar-programa.sh`, y en los documentos (`PAGINA_LUNA.md`, `repo-arch/README.md`).

### Estado — 24 nov 2026
- Luna sigue siendo **Beta** (0.1.0-beta), solo para nosotros por ahora. Será **Beta pública** cuando todo esté mejorado, para que la comunidad la pruebe.
- Cuando sea oficial, el orden es: **primero AUR**, después repo propio para `sudo pacman -S luna`. Después se darán las instrucciones para publicarlo en AUR, con un comando fácil de instalar para .deb y para Pacman.
- **Nada publicado en AUR/GitHub todavía.** El `.pkg.tar.zst` aún no existe: hay que compilarlo en el Garuda de Fernando con `makepkg -si` (PKGBUILD pkgrel 5), y antes de publicar hay que mostrarle primero el link donde estará alojado el código fuente.
- Fernando: usuario común en Linux, ya camino a intermedio. Instala con comandos, usa la terminal, prueba Luna y estudia el código. Luna es suya; el trabajo es ayudarlo a hacerla.
- Envío pendiente: Luna Launcher 3, mañana 25 nov 2026 a las 7, por correo a guzmankaza@gmail.com, solo con el comando.

### Archivos actuales en `~/workspace/luna/` (24 nov 2026)
- `81630_0_1xuc.webp` — póster original de Luna (gatito morado en la luna creciente), foto de bienvenida del instalador.
- `ARCHIVO_LUNA.md` — los 3 pasos con imágenes y las funciones.
- `COMPARACION_LUNA.md` — comparación Luna vs Hidamari vs el fondo de video de KDE.
- `LUNA_TODO_ARCHIVADO.md` — este archivo: todo el proyecto archivado.
- `PAGINA_LUNA.md` — descripción completa del programa para la página.
- `README.md` — resumen del proyecto.
- `PKGBUILD` — paquete Arch, 0.1.0_beta, pkgrel 5 (sin la imagen del 65%).
- `build-deb.sh` — construye el .deb de Luna.
- `debian/control`, `debian/rules` — archivos del paquete .deb.
- `install.sh` — instalador general del proyecto.
- `luna.py` — programa de fondo: comandos `set` / `stop` / `list` / `status`, pone video o imagen con mpv.
- `luna_gui.py` — ventana principal de Luna (tkinter, carrusel 3D, Ajustes, Acerca con submenú Funciones, mejoras de video).
- `luna-installer-gui.py` — instalador gráfico en 3 pasos (Instalar, proceso con barrita lenta, Continuar).
- `luna-installer.sh` — instalador con ventanita zenity (respaldo) o terminal.
- `luna-install.sh` — comando único de instalación (descarga el zip, makepkg, pkexec, instalador).
- `luna-instalar-programa.sh` — instalador limpio del paquete, sin dejar archivos sueltos en Descargas.
- `luna_ascii.py` — bienvenida ASCII en la terminal (pregunta si instalar Luna, luego `sudo pacman -S luna`).
- `luna_ascii.txt` — el póster de Luna en ASCII, para la terminal.
- `luna.desktop` — lanzador de Luna.
- `luna-utilidades.desktop` — Luna en el menú Utilidades (Exec=luna-gui).
- `luna-clic-derecho.desktop` — menú de clic derecho en KDE ("Poner con Luna", "Abrir Biblioteca de Luna").
- `luna.service` — servicio de usuario para que Luna arranque sola.
- `luna_0.1.0-beta_all.deb` — paquete .deb ya compilado (para Debian/Ubuntu, no para Garuda).
- `luna_0.1.0-beta_all/` — carpeta del paquete .deb compilado.
- `repo/` — repo Debian con el .deb, `Packages` y `Packages.gz`.
- `repo-arch/` — repo Pacman (estructura lista, falta el .pkg.tar.zst; hay un `FALTA-el-paquete.txt`).
- `media-generation-luna-*.webp` — imágenes de diseño archivadas (instalando 100%, biblioteca/carrusel, botón Poner Fondo, clic derecho, interfaz principal). La imagen del 65% ya no se usa.
- `media-generation-luna-*.mp4` — videos archivados (póster paso 1, instalando 1-100, instalador que termina y abre el programa).
- `media-generation-*.json` — datos de generación de las imágenes y videos.
- `media-generation-last-upload-handles.json` — últimos enlaces de subida.
- `.thumbnails/` — miniaturas de las imágenes generadas.

## Bloque para la página — 24 nov 2026
- `BLOCK_LUNA.md` — bloque "Bloque luna para nuestra pagina": resumen de todo para la página. Empieza con el póster ASCII en la terminal, morado sobre fondo negro, con la pregunta ¿Quieres instalar Luna? Luego qué es Luna, Beta 0.1.0-beta, instalación en 3 pasos con iconos, funciones con iconos por botón, Mejoras de video (sin el nombre Smart Video, solo sus funciones), cómo se instala, y abajo Hecho por Vega & Kiki / Guzman.
- Copia del bloque: `~/workspace/your_files/Bloque luna para nuestra pagina.md`.
- Resumen en imagen morada: `~/workspace/luna_resumen_morado.png` (póster limpio sin logos, 3 pasos, funciones, mejoras de video, terminal ASCII, Hecho por Vega & Kiki / Guzman).
- Foto terminal ASCII: `~/workspace/luna_terminal.png`.
- Foto ventana principal: `~/workspace/luna_foto.png`.
- Fotos instalador 3 pasos: `~/workspace/luna_instalador_paso1.png`, `luna_instalador_paso2.png`, `luna_instalador_paso3.png`.
