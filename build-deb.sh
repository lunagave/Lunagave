#!/usr/bin/env bash
# Construye el .deb para Debian/Ubuntu sin necesidad de debuild
# Uso: ./build-deb.sh
set -e
VERSION="1.0-beta"
PKG="luna_${VERSION}_all"
rm -rf "$PKG" "${PKG}.deb"
mkdir -p "$PKG/DEBIAN" "$PKG/usr/bin" "$PKG/usr/share/applications" "$PKG/usr/lib/systemd/user"
chmod 755 "$PKG" "$PKG/DEBIAN" "$PKG/usr" "$PKG/usr/bin" "$PKG/usr/share" "$PKG/usr/share/applications" "$PKG/usr/lib" "$PKG/usr/lib/systemd" "$PKG/usr/lib/systemd/user"
cp luna.py "$PKG/usr/bin/luna"
chmod 755 "$PKG/usr/bin/luna"
cp luna.desktop "$PKG/usr/share/applications/"
cp luna.service "$PKG/usr/lib/systemd/user/"
cat > "$PKG/DEBIAN/control" <<EOF
Package: luna
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: mpv, python3
Maintainer: Fernando <fernando@example.com>
Description: Fondos de pantalla animados, fácil y sin plugins
 Luna pone fondos de pantalla animados en Linux sin plugins.
EOF
dpkg-deb --build "$PKG"
echo "Listo: ${PKG}.deb"
echo "Instalar: sudo dpkg -i ${PKG}.deb && sudo apt -f install"
