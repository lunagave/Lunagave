# Publicar Luna en AUR como luna-wallpaper — pasos exactos, en orden

Versión: Luna v1.0 estable. Repo: https://github.com/lunagave/Lunagave (head c0d1fdb).
El nombre `luna` ya está ocupado en AUR por otro programa (gestor npm), verificado
con la API de AUR. `luna-wallpaper` está libre (resultcount 0). Fernando aprobó
`luna-wallpaper` el 25 nov 2026.

## Archivos en esta carpeta (~/workspace/luna/aur/)
- `PKGBUILD` — nuevo, para AUR. NO es el PKGBUILD viejo de ~/workspace/luna/
  (ese usa fuentes locales con SKIP y no sirve para AUR). No sobreescribir el
  viejo todavía: cuando luna-wallpaper esté en AUR, el PKGBUILD de AUR manda.
- `.SRCINFO` — generado a mano con el formato de `makepkg --printsrcinfo`.
  Hay que regenerarlo en Garuda con `makepkg --printsrcinfo > .SRCINFO`
  después de poner el sha256 real.
- `chaotic-aur-issue.md` — texto listo del issue para Chaotic-AUR.
  NO se puede mandar hasta que luna-wallpaper esté en AUR.

## Paso 0 — Preparar el repo (antes del tag)
1. Subir el icono a la raíz del repo como `luna.png`:
   `~/workspace/luna/flatpak/io.github.lunagave.Luna.png` (512x512).
   El PKGBUILD lo instala como icono de la app. Sin él, el build falla.
2. Verificar que el repo en main tenga la versión 1.0 estable (ya está, head 2126272).

## Paso 1 — Tag estable v1.0 en GitHub (YA HECHO el 25 nov 2026)
El tag `v1.0` ya existe en el repo lunagave/Lunagave (release "Luna v1.0",
Latest, commit `2126272e10d76c6079ba067f34eb3a2946e38860`, 11:10 CST).
El sha256 real del tarball ya está puesto en el PKGBUILD y en .SRCINFO:
`ce0d21dc99a7baa1e620c8b4e01e59d30256a80820730a6103a081b1e4ce2a92`.
Regenerar .SRCINFO en Garuda con `makepkg --printsrcinfo > .SRCINFO`
después de cualquier cambio al PKGBUILD.

⚠️ BLOQUEO: el PKGBUILD todavía NO construye del tarball v1.0 tal cual:
instala `luna.png` y 7 imágenes `media-generation-*.webp` que NO están en
el tarball v1.0 (ni en el repo). Antes de mandar a AUR hay que crear un tag
nuevo (p. ej. v1.0.1) con esos archivos, o quitarlos del package().

## Paso 2 — En Garuda: probar el build
El sha256 real ya está puesto (ver Paso 1), así que `updpkgsums` ya no hace
falta salvo que cambie el PKGBUILD o el tag.
```bash
mkdir -p ~/aur-luna && cd ~/aur-luna
cp ~/workspace/luna/aur/PKGBUILD ~/workspace/luna/aur/.SRCINFO .
makepkg -si       # construye e instala luna-wallpaper; debe terminar sin errores
makepkg --printsrcinfo > .SRCINFO   # regenera .SRCINFO con el sha256 real
```
Si `makepkg -si` falla, no seguir: el error exacto dice qué falta.

## Paso 3 — Probar en chroot limpio (lo pide Chaotic-AUR)
```bash
sudo pacman -S devtools
mkarchroot ~/chroot/root base-devel
makechrootpkg -c -r ~/chroot
```
El build debe pasar en limpio, sin depender de nada instalado a mano.

## Paso 4 — Cuenta AUR y clave SSH (lo tiene que hacer Fernando)
1. Crear cuenta en https://aur.archlinux.org/register
2. Generar clave SSH en su Garuda y registrarla en la cuenta AUR
   (Profile → SSH Public Key).
3. Clonar el repo vacío de AUR:
```bash
git clone ssh://aur@aur.archlinux.org/luna-wallpaper.git
cd luna-wallpaper
cp ~/aur-luna/PKGBUILD ~/aur-luna/.SRCINFO .
git add PKGBUILD .SRCINFO
git commit -m "Luna Wallpaper 1.0 - fondos animados en Linux"
git push
```
4. Verificar en https://aur.archlinux.org/packages/luna-wallpaper

## Paso 5 — Chaotic-AUR (solo DESPUÉS del paso 4)
Abrir un issue en https://github.com/chaotic-aur/packages/issues con la
plantilla "Request to add new package" y el texto de `chaotic-aur-issue.md`.
Antes: buscar que no exista ya un issue igual y que `luna-wallpaper` no esté
en la lista de prohibidos de Chaotic-AUR. La revisión la hacen personas
mantenedoras, sin plazo fijo: días o 1-2 semanas.

## Qué falta de Fernando
- [ ] Subir `luna.png` a la raíz del repo (o decirme que lo suba yo).
- [x] Crear el tag `v1.0` en GitHub. (HECHO el 25 nov 2026, 11:10 CST.)
- [ ] Resolver el bloqueo del Paso 1: `luna.png` y las 7 imágenes
      `media-generation-*.webp` no están en el tarball v1.0 (tag nuevo
      v1.0.1 con esos archivos, o quitarlos del PKGBUILD).
- [ ] Crear cuenta AUR y registrar su clave SSH.
- [ ] Correr `updpkgsums` + `makepkg -si` en su Garuda (esta máquina es
      Debian: no hay makepkg, no se puede generar el sha256 ni el .SRCINFO
      real aquí).
- [ ] Hacer `git push` a AUR y abrir el issue de Chaotic-AUR.
