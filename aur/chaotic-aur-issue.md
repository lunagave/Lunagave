<!--
  Texto listo para el issue de Chaotic-AUR.
  Plantilla oficial: .github/ISSUE_TEMPLATE/01-request-new-package.yml
  en https://github.com/chaotic-aur/packages
  Título del issue: [Request] luna-wallpaper
  URL: https://github.com/chaotic-aur/packages/issues/new?template=01-request-new-package.yml
  ¡NO MANDAR hasta que luna-wallpaper esté publicado en AUR!
  Antes de mandar: buscar issues existentes de luna-wallpaper y revisar
  la lista de prohibidos de Chaotic-AUR.
-->

## Package

https://aur.archlinux.org/pkgbase/luna-wallpaper

## Purpose

Luna (luna-wallpaper) is a desktop app that sets animated wallpapers on
Linux, easy and without plugins, made for the common user. Pick an image or
a video and Luna sets it as your wallpaper, with a 3D carousel, smart pause,
multi-monitor support and volume/mute controls. It is written in Python with
tkinter, uses mpv for the wallpaper, and ships a graphical 3-step installer
for Arch (Pacman) and Debian/Ubuntu (.deb). It installs to the Start menu
(Utilities) and adds a right-click action ("Poner con Luna" / "Abrir Luna")
on images and videos.

Use cases: any Arch/Garuda user who wants a video as wallpaper without
editing config files or using plugins; similar in spirit to Hidamari and
KDE's Smart Video Wallpaper, but as a simple click-only app with an
installer. There is no equivalent package in the official Arch repos or
in Chaotic-AUR.

## License

MIT

## Submission checklist

- [x] The package is not banned.
- [x] The package is not available in Chaotic AUR or official Arch repos.
- [x] The package has not already been requested.

---
Notes for the submitter (do NOT paste these into the issue):
- AUR link must exist before submitting: https://aur.archlinux.org/packages/luna-wallpaper
- Tested in a clean chroot: YES / NO (fill in after running makechrootpkg).
- License allows redistribution: yes (MIT, LICENSE file in the repo
  https://github.com/lunagave/Lunagave).
- The name "luna" is already taken in AUR by another program (an npm
  dependency manager), which is why this package is named luna-wallpaper.
