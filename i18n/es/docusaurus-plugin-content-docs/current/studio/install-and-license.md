---
title: Instalación y licencia
---

# Instalación y licencia

HydroPol2D Studio, el programa de escritorio de HydroPol2D-Python, funciona con un código de
licencia. Los códigos no se venden ni se descargan en este sitio: escriba a Marcus N. Gomes Jr.,
que desarrolla HydroPol2D, y él le envía el instalador y su código.

**Contacto:** Marcus N. Gomes Jr., [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).

## 1. Solicite una licencia {#ask-for-a-license}

Escriba a Marcus indicando:

- su nombre y la dirección de correo electrónico que debe llevar la licencia (el código guarda
  ambos);
- su computadora: un Mac con Apple silicon (M1 o posterior) o Windows (64 bits).

Recibirá dos cosas:

- el instalador para su computadora, un archivo `.zip`;
- su código de licencia, una línea larga de texto que empieza con `HP2D1-`. Cada código tiene un
  último día de validez.

No hay instalador para Mac con procesador Intel: JAX, la biblioteca numérica sobre la que funciona
el modelo, no publica versiones para ellos desde diciembre de 2024. Tampoco hay instalador para
Linux.

## 2. Instale {#install}

### Mac (Apple silicon) {#mac-apple-silicon}

1. Descomprima `HydroPol2D-Studio-macOS-arm64.zip`.
2. Arrastre **HydroPol2D Studio** a la carpeta **Aplicaciones** (**Applications**).
3. Haga doble clic en él. La primera vez, macOS avisa que no puede comprobar si la app contiene
   software malicioso. Cierre ese aviso.
4. Abra **Ajustes del Sistema › Privacidad y Seguridad** (**System Settings › Privacy &
   Security**), desplácese hasta el mensaje sobre HydroPol2D Studio y haga clic en **Abrir igualmente**
   (**Open Anyway**). Confirme con su contraseña.

Los pasos 3 y 4 se hacen solo una vez.

### Windows (64 bits) {#windows-64-bit}

1. Descomprima `HydroPol2D-Studio-Windows-x64.zip` en una carpeta que vaya a conservar, por ejemplo
   `Documentos\HydroPol2D Studio`.
2. Haga doble clic en **HydroPol2D Studio.exe**.
3. Si Windows muestra "Windows protegió su PC", haga clic en **Más información** y luego en
   **Ejecutar de todas formas**.

## 3. Active {#activate}

La primera vez que se abre Studio, la ventana de licencia le pide su código. Pegue el código completo
y haga clic en **Activate**. Studio muestra entonces a quién pertenece la licencia y su último día de
validez, y se abre en la pantalla Home. **Help > About HydroPol2D Studio** muestra la misma
información más adelante.

- El mismo código funciona en todas las computadoras donde instale Studio: introdúzcalo en cada una.
- Studio comprueba el código en la propia computadora y no necesita internet para ello.

## Renovar o cambiar el código {#renewing-or-changing-the-code}

- Studio le avisa cuando quedan menos de 30 días. Para un código nuevo, escriba otra vez a Marcus.
- Studio guarda el código en `license.txt`, en esta carpeta:
  - Mac: `~/Library/Application Support/HydroPol2D Studio/`
  - Windows: `%APPDATA%\HydroPol2D Studio\`

  Para introducir otro código, borre ese archivo y vuelva a abrir Studio.
- Mantenga correcta la fecha de la computadora. Studio se niega a abrirse cuando la fecha se atrasa
  más de dos días respecto de la última vez que se usó.

## Desinstalar {#uninstalling}

Borre **HydroPol2D Studio** de Aplicaciones (Mac) o su carpeta (Windows). Studio también guarda los
elementos siguientes, que puede borrar cuando ya no los necesite:

| Qué | Mac | Windows |
|---|---|---|
| Código de licencia | `~/Library/Application Support/HydroPol2D Studio/` | `%APPDATA%\HydroPol2D Studio\` |
| Informes de fallos y registro de errores | `~/Library/Logs/HydroPol2D Studio/` | `%LOCALAPPDATA%\HydroPol2D Studio\Logs\` |
| Datos y herramientas descargados (pueden ocupar varios GB) | `~/.cache/hydropol2d-case-builder/` | `%USERPROFILE%\.cache\hydropol2d-case-builder\` |
| Disposición de la ventana y modelos recientes | `~/Library/Preferences/com.hydropol2d.Studio.plist` | Registro: `HKEY_CURRENT_USER\Software\HydroPol2D\Studio` |
| Inicios de sesión de Copernicus y NASA Earthdata | Acceso a Llaveros: elementos llamados `hydropol2d:…` | Administrador de credenciales: elementos llamados `hydropol2d:…` |
| Token de NASA Earthdata (si guardó uno) | `~/.config/hydropol2d-case-builder/earthdata_token` | `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token` |

Sus modelos y resultados permanecen en las carpetas que eligió para ellos.
