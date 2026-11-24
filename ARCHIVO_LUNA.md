# Luna — Archivo de los 3 pasos

Guardado el 21 nov 2026. Todo está en `~/workspace/luna/` para que no se pierda.

## Paso 1 — Base del proyecto

Luna es un proyecto para poner fondos de pantalla animados, fácil y sin plugins.
Para Arch (Pacman) y Debian/Ubuntu (.deb).

- Póster original: `../user/files/81630_0_1xuc.webp`
- Video del póster: `media-generation-luna-paso1-poster-0-bef26f93-8163-4f69-8e35-5f7f795baed1.mp4`

## Paso 2 — Diseño del instalador

- Pantalla instalando 65% con barrita de proceso: `media-generation-luna-instalando-proceso-0-f3b3df9d-f2c3-4ba1-bcb5-04792240cd4e.webp`
- Pantalla instalando 100% completado: `media-generation-luna-instalando-0-9189c024-59e0-4561-81d0-d789d24136e2.webp`
- Video porcentaje del 1 al 100: `media-generation-luna-instalando-1-100-0-88194f11-e317-4a08-8d46-1dcd4d49950e.mp4`
- Video instalador termina y se abre el programa: `media-generation-luna-instalador-abre-programa-0-6256ca65-03b9-45f1-a10b-5473374cf697.mp4`

Flujo confirmado: al terminar el instalador al 100%, se abre el programa Luna.

## Paso 3 — Interfaz y herramientas

Decisiones confirmadas:
- Sin emulación / sin EmulationStation.
- Biblioteca guarda fotos y videos.
- Arriba: fotos y videos en forma de carrusel.
- Abajo: vista previa con más imágenes del usuario.
- Arriba dice: Agregar Fondo & Imagen/Video.
- Iconos: Agregar Carpeta Fondo, Quitar Imagen/Video, Ajustes.
- Ajustes NO se ve en la pantalla principal: al tocar su icono se abre otra pantalla aparte, con todas las herramientas de Smart Video (detección, escalado IA, nitidez, estabilización, reducción de ruido, HDR).
- Al seleccionar una foto o video aparece el botón: Poner Imagen en el Fondo de Pantalla.

Archivos:
- Interfaz Biblioteca con carrusel: `media-generation-luna-interfaz-biblioteca-carru-0-d4ecef1d-d3e4-4f88-ad0f-ff0eb604b6c9.webp`
- Ajustes en pantalla aparte: `media-generation-luna-interfaz-principal-sin-aj-0-28c0b2be-1eb8-4c11-b15e-bedab79e8958.webp`
- Botón Poner Imagen en el Fondo de Pantalla: `media-generation-luna-boton-poner-fondo-0-11ddadff-28ca-482e-a90a-c26fadac4ebb.webp`
- Versión final, carrusel arriba y vista previa abajo: `media-generation-luna-carrusel-arriba-vista-aba-0-3c945284-96d3-4a07-bf84-4484e9565451.webp`
- Primera interfaz de referencia enviada por Fernando: `../user/files/81463_3_hnje.webp`
- Versión anterior con emulación (no usar, solo referencia): `media-generation-luna-interfaz-emulationstation-0-8399930c-9287-4ec2-b07a-749733b8a8cb.webp`

## Funciones del programa — confirmadas

- Instalador fácil para el usuario común, sin terminal: detecta .deb (Debian/Ubuntu) o .pacman (Arch/Manjaro) e instala automático.
- Al terminar el instalador se abre Luna.
- Clic derecho en el escritorio: Poner Luna como Fondo de Escritorio, Establecer Imagen como Fondo, Establecer Video como Fondo, Abrir con Luna Biblioteca.
- La imagen Luna se muestra en la Biblioteca.
- Automático: al elegir un video o una imagen, se pone como fondo de escritorio.
- Lee todos los formatos: imágenes JPG, PNG, WEBP, GIF, BMP, SVG. Videos MP4, MKV, WEBM, MOV, AVI.
- Archivo: `media-generation-luna-clic-derecho-fondo-automa-0-651e12c0-6c62-4cd6-8dee-7c0085df28d9.webp`

## Qué falta

- Paso 3 del código: instalador universal Arch y Debian/Ubuntu.
- Paso 4: paquete Arch (Pacman) y paquete .deb.
- Paso 5: README y cómo probarlo en tu PC.
