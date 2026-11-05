---
title: Instalación y licencia
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Instalación y licencia

El Case Builder funciona con un código de licencia. Los instaladores están en la
[página de descargas](https://github.com/marcusnobrega-eng/HydroPol2D-Case-Builder-releases) pública,
en **Releases**. El código le llega por correo electrónico de Marcus N. Gomes Jr., que desarrolla
HydroPol2D.

**Contacto:** Marcus N. Gomes Jr., [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).

## 1. Solicite una licencia {#ask-for-a-license}

Escriba a Marcus indicando:

- su nombre y la dirección de correo electrónico que debe llevar la licencia (el código guarda
  ambos);
- su computadora: un Mac con Apple silicon (M1 o posterior) o Windows (64 bits).

Recibirá su código de licencia, una línea larga de texto que empieza con `HP2D1-`. Cada código
tiene un último día de validez.

## 2. Descargue {#download}

En la página de descargas, abra **Releases** y descargue el zip para su computadora.

| Computadora | Archivo | Espacio libre en disco |
|---|---|---|
| Mac con Apple silicon (M1 o posterior) | `HydroPol2D-Case-Builder-macOS-arm64.zip` | unos 600 MB, más los datos que descargue |
| Windows (64 bits) | `HydroPol2D-Case-Builder-Windows-x64.zip` | unos 600 MB, más los datos que descargue |

Las notas de la versión indican la suma de verificación SHA-256 de cada zip.

## 3. Instale {#install}

### Mac (Apple silicon) {#mac-apple-silicon}

1. Descomprima `HydroPol2D-Case-Builder-macOS-arm64.zip`.
2. Arrastre **HydroPol2D Case Builder** a la carpeta **Aplicaciones** (**Applications**).
3. Haga doble clic en él. La primera vez, macOS avisa que no puede comprobar si la app contiene
   software malicioso. Haga clic en **Done**.
4. Abra **Ajustes del Sistema › Privacidad y Seguridad** (**System Settings › Privacy &
   Security**). Desplácese hasta el mensaje sobre HydroPol2D Case Builder y haga clic en
   **Abrir igualmente** (**Open Anyway**). Confirme con su contraseña.

Los pasos 3 y 4 se hacen solo una vez. Si prefiere Terminal, este comando permite que macOS abra
la app sin el paso 4:

```bash
xattr -dr com.apple.quarantine "/Applications/HydroPol2D Case Builder.app"
```

### Windows (64 bits) {#windows-64-bit}

1. Descomprima `HydroPol2D-Case-Builder-Windows-x64.zip` en una carpeta que vaya a conservar, por
   ejemplo `Documents\HydroPol2D Case Builder`.
2. Haga doble clic en **HydroPol2D Case Builder.exe**.
3. Si Windows muestra "Windows protegió su PC", haga clic en **Más información** y luego en
   **Ejecutar de todas formas**.

## 4. Inicie y active {#activate}

Al abrir la app aparece una ventana pequeña. Esta inicia el Case Builder y, tras unos segundos, lo
abre en su navegador web. La primera vez, la página le pide su código. Pegue el código completo en
**License code** y haga clic en **Activate**.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-license.png')} width="760" alt="La página del Case Builder que pide un código de licencia, con el cuadro License code, el botón Activate y la línea de contacto" />
</p>

<p align="center">
  <em>Figura 1. La página de licencia. Pegue el código que empieza con HP2D1- y haga clic en Activate. Después, la página se abre directamente en Prepare a case.</em>
</p>

Después de la activación, una línea en la parte superior de la página muestra a quién pertenece la
licencia y su último día de validez.

## Trabajar con la app {#working-with-the-app}

- Mantenga abierta la ventana pequeña mientras trabaja. **Open in browser** vuelve a abrir la
  página si cerró su pestaña. **Quit**, o cerrar la ventana pequeña, detiene el Case Builder.
- La página está en `http://127.0.0.1:8501`, o en el siguiente puerto libre. Solo su propia
  computadora puede abrirla. El propio Case Builder funciona en su computadora, y sus casos se
  quedan allí.
- Los casos nuevos van a `Documents/HydroPol2D Case Builder/outputs` en su carpeta personal, salvo
  que elija otra carpeta en **Folders and advanced paths** (vea [Ajustes del caso](settings#folders)).
- El primer caso de una región descarga sus datos. Los casos siguientes los reutilizan desde la
  caché.

## Sobre su licencia {#about-your-license}

- Su código es personal. Funciona en cualquier computadora donde instale el Case Builder.
  Introduzca el mismo código en cada una. Por favor, no lo comparta.
- El Case Builder comprueba el código en su computadora. No necesita internet para ello.
- La página le avisa cuando quedan menos de 30 días. Para un código nuevo, escriba otra vez a
  Marcus.
- El Case Builder guarda el código en `license.txt`, en esta carpeta:
  - Mac: `~/Library/Application Support/HydroPol2D Case Builder/`
  - Windows: `%APPDATA%\HydroPol2D Case Builder\`

  Para introducir otro código, borre ese archivo y vuelva a abrir el Case Builder.
- Mantenga correcta la fecha de su computadora. El Case Builder se niega a iniciarse cuando la
  fecha se atrasa más de dos días respecto de la última vez que se usó.
- Un código de HydroPol2D Studio no abre el Case Builder. Studio trae el Case Builder integrado
  (**New model**), con el código propio de Studio.

Los términos de la licencia están en `LICENSE.txt`, junto a la app en el zip. Las partes de código
abierto de la app y sus licencias se listan en `THIRD_PARTY_NOTICES.txt`. Los conjuntos de datos
de entrada conservan sus propias licencias y condiciones.

## Desinstalar {#uninstalling}

Borre **HydroPol2D Case Builder** de Aplicaciones (Mac) o su carpeta (Windows). El Case Builder
también guarda los elementos siguientes, que puede borrar cuando ya no los necesite:

| Qué | Mac | Windows |
|---|---|---|
| Código de licencia | `~/Library/Application Support/HydroPol2D Case Builder/` | `%APPDATA%\HydroPol2D Case Builder\` |
| Datos y herramientas descargados (pueden ocupar varios GB) | `~/.cache/hydropol2d-case-builder/` | `%USERPROFILE%\.cache\hydropol2d-case-builder\` |
| Token de NASA Earthdata (si guardó uno) | `~/.config/hydropol2d-case-builder/earthdata_token` | `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token` |

HydroPol2D Studio usa la misma caché de datos, así que bórrela solo si ninguno de los dos programas
la necesita. Sus casos permanecen en las carpetas que eligió para ellos.
