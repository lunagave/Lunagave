# Publicar Luna en AUR como luna-wallpaper — pasos exactos, en orden

Versión: Luna v1.0.1 estable. Repo: https://github.com/lunagave/Lunagave (head a47d8b5).
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
   (HECHO: luna.png está en la raíz del repo desde el 25 nov 2026.)
2. Verificar que el repo en main tenga la versión estable (ya está, head a47d8b5).

## Paso 1 — Tag estable v1.0.1 en GitHub (YA HECHO el 25 nov 2026)
El tag `v1.0.1` ya existe en el repo lunagave/Lunagave (release "Luna v1.0.1",
Latest, commit `a47d8b5db85a9ea96ef596bf70cc54dae70a8d8c`, 15:07 CST).
El sha256 real del tarball ya está puesto en el PKGBUILD y en .SRCINFO:
`42f76411279a8333b57df7c35b3c8587eec1fffc876ddf9e40cb86e39157cb07`.
El tarball v1.0.1 ya incluye `luna.png` en la raíz y ya no trae las
imágenes viejas beta: el bloqueo anterior quedó resuelto.
Regenerar .SRCINFO en Garuda con `makepkg --printsrcinfo > .SRCINFO`
después de cualquier cambio al PKGBUILD.

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
git commit -m "Luna Wallpaper 1.0.1 - fondos animados en Linux"
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
- [x] Subir `luna.png` a la raíz del repo. (HECHO el 25 nov 2026.)
- [x] Crear el tag `v1.0` en GitHub. (HECHO el 25 nov 2026, 11:10 CST.)
- [x] Crear el tag `v1.0.1` con `luna.png` incluido y PKGBUILD corregido.
      (HECHO el 25 nov 2026, 15:07 CST; el bloqueo del Paso 1 quedó resuelto.)
- [ ] Crear cuenta AUR y registrar su clave SSH.
- [ ] Correr `updpkgsums` + `makepkg -si` en su Garuda (esta máquina es
      Debian: no hay makepkg, no se puede generar el sha256 ni el .SRCINFO
      real aquí).
- [ ] Hacer `git push` a AUR y abrir el issue de Chaotic-AUR.
