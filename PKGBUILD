# Maintainer: Fernando <fernando@example.com>
pkgname=luna
pkgver=1.0_beta
pkgrel=1
pkgdesc="Fondos de pantalla animados, fácil y sin plugins"
arch=('any')
url="https://example.com/luna"
license=('MIT')
depends=('mpv' 'python' 'zenity' 'tk' 'python-pillow')
optdepends=('mpvpaper: para Wayland' 'xwinwrap: para X11')
source=('luna.py' 'luna_gui.py' 'luna.desktop' 'luna-utilidades.desktop' 'luna.service' 'luna-installer.sh' 'luna-installer-gui.py' 'luna-clic-derecho.desktop' '81630_0_1xuc.webp' 'media-generation-luna-instalando-0-9189c024-59e0-4561-81d0-d789d24136e2.webp' 'media-generation-luna-interfaz-biblioteca-carru-0-d4ecef1d-d3e4-4f88-ad0f-ff0eb604b6c9.webp' 'media-generation-luna-carrusel-arriba-vista-aba-0-3c945284-96d3-4a07-bf84-4484e9565451.webp' 'media-generation-luna-boton-poner-fondo-0-11ddadff-28ca-482e-a90a-c26fadac4ebb.webp' 'media-generation-luna-interfaz-principal-sin-aj-0-28c0b2be-1eb8-4c11-b15e-bedab79e8958.webp' 'media-generation-luna-clic-derecho-fondo-automa-0-651e12c0-6c62-4cd6-8dee-7c0085df28d9.webp' 'luna-1.0-beta-paso1-instalar.webp' 'luna-1.0-beta-paso2-instalando.webp' 'luna-1.0-beta-paso3-completa.webp' 'luna-1.0-beta-instalado-carrusel.webp')
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
  # Programa: CLI + ventana GUI. Nada queda suelto en ~/Descargas:
  # pacman pone cada archivo en su lugar del sistema.
  install -Dm755 "$srcdir/luna.py" "$pkgdir/usr/bin/luna"
  install -Dm755 "$srcdir/luna_gui.py" "$pkgdir/usr/bin/luna-gui"
  # Menú Utilidades: Luna abre la ventana GUI, no el CLI.
  install -Dm644 "$srcdir/luna-utilidades.desktop" "$pkgdir/usr/share/applications/luna.desktop"
  install -Dm644 "$srcdir/luna.service" "$pkgdir/usr/lib/systemd/user/luna.service"
  # Clic derecho en KDE: "Poner con Luna" y "Abrir Luna" (abre la ventana).
  install -Dm644 "$srcdir/luna-clic-derecho.desktop" "$pkgdir/usr/share/kservices5/ServiceMenus/luna-clic-derecho.desktop"
  # Instalador con imágenes (Pacman / .deb, póster, 100%). La imagen del 65% ya no se usa.
  install -Dm755 "$srcdir/luna-installer.sh" "$pkgdir/usr/lib/luna/luna-installer.sh"
  install -Dm755 "$srcdir/luna-installer-gui.py" "$pkgdir/usr/lib/luna/luna-installer-gui.py"
  # Carpeta del programa: /usr/share/luna/ — las 7 imágenes archivadas
  # + las 4 imágenes NUEVAS v1.0 beta del instalador y de Luna ya instalado.
  for img in 81630_0_1xuc.webp media-generation-luna-instalando-0-9189c024-59e0-4561-81d0-d789d24136e2.webp media-generation-luna-interfaz-biblioteca-carru-0-d4ecef1d-d3e4-4f88-ad0f-ff0eb604b6c9.webp media-generation-luna-carrusel-arriba-vista-aba-0-3c945284-96d3-4a07-bf84-4484e9565451.webp media-generation-luna-boton-poner-fondo-0-11ddadff-28ca-482e-a90a-c26fadac4ebb.webp media-generation-luna-interfaz-principal-sin-aj-0-28c0b2be-1eb8-4c11-b15e-bedab79e8958.webp media-generation-luna-clic-derecho-fondo-automa-0-651e12c0-6c62-4cd6-8dee-7c0085df28d9.webp luna-1.0-beta-paso1-instalar.webp luna-1.0-beta-paso2-instalando.webp luna-1.0-beta-paso3-completa.webp luna-1.0-beta-instalado-carrusel.webp; do
    install -Dm644 "$srcdir/$img" "$pkgdir/usr/share/luna/$img"
  done
}
# Construir en Garuda: makepkg -si
# (esta máquina es Debian, no hay makepkg; el .pkg.tar.zst se compila en Garuda)
# Instalar el paquete ya compilado: sudo pacman -U luna-1.0_beta-1-any.pkg.tar.zst
# Instalar desde el repo, cuando esté publicado: sudo pacman -S luna
# Instalador con imágenes: bash /usr/lib/luna/luna-installer.sh
# Abrir la ventana: luna-gui  (o menú Utilidades > Luna)
