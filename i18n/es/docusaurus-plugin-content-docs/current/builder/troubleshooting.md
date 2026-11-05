---
title: Solución de problemas
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Solución de problemas

## Iniciar la app {#starting}

**El navegador no se abre.** Haga clic en **Open in browser** en la ventana pequeña. La página está
en `http://127.0.0.1:8501`, o en el siguiente puerto libre.

**La ventana pequeña dice que el Case Builder se detuvo.** Nombra un archivo de registro. Envíe ese
archivo con su pregunta a Marcus N. Gomes Jr. ([marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com)).

**macOS no abre la app.** Permítala una vez en **Ajustes del Sistema › Privacidad y Seguridad**
(**System Settings › Privacy & Security**) con **Abrir igualmente** (**Open Anyway**)
([Instalación y licencia](install-and-license#mac-apple-silicon)).

## Licencia {#license}

**"This is a HydroPol2D Studio code".** Pegó su código de Studio. El Case Builder necesita su propio
código.

**La licencia venció o quedan menos de 30 días.** Escriba a Marcus para pedir un código nuevo. Para
introducirlo, borre `license.txt` de la carpeta de la licencia y vuelva a abrir el Case Builder
([Sobre su licencia](install-and-license#about-your-license)).

**El Case Builder se niega a iniciarse después de un cambio de fecha.** Ajuste correctamente la
fecha y la hora de la computadora. El Builder se niega a iniciarse cuando la fecha se atrasa más de
dos días respecto de su último uso.

## Antes de la vista previa {#before-the-preview}

**"Confirm riverbed hydraulic conductivity when river-groundwater exchange is enabled."** Abra
**Hydraulic parameters**, revise **Riverbed conductivity (m/s)** y marque **Confirm this riverbed
conductivity for the case**, o desmarque **River-groundwater exchange**.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-riverbed-confirm.png')} width="760" alt="El mensaje de listo, el botón Preview domain and cost y un cuadro de error rojo que pide confirmar la conductividad hidráulica del lecho del río cuando el intercambio río-agua subterránea está activado" />
</p>

<p align="center">
  <em>Figura 1. La vista previa se detiene hasta que se confirma la conductividad del lecho del río.</em>
</p>

**"This case cannot be prepared yet:" con una cuenta nombrada.** Configure esa cuenta
([Fuentes de datos y cuentas](data-accounts)) y luego recargue la página.

**El periodo de lluvia no está disponible.** IMERG, AORC y MSWEP tienen sus propios periodos, que la
página muestra. Elija fechas dentro de ellos, u otro producto de lluvia. AORC también necesita que
todo el dominio esté dentro de los Estados Unidos contiguos.

**No se encuentra la ciudad.** Revise cómo escribe GHSL el nombre de la ciudad y del país. Si GHSL
no tiene el límite que necesita, elija **Polygon file** e indique su propio polígono.

**"Requested … m cells are finer than the DEM's …".** El tamaño de celda no puede ser más fino que
el terreno. Use un tamaño de celda mayor, o un DEM local más fino.

**"The coarse quadtree resolution must be a power-of-two multiple of the fine resolution."** Haga
que el tamaño de celda grueso sea 2, 4, 8 o más veces el tamaño fino.

## La vista previa {#the-preview}

**El caso es demasiado grande.** Deténgase después de la vista previa. Use un tamaño de celda mayor,
una malla quadtree o un área más pequeña, o lleve la construcción y la simulación a una computadora
con más memoria. La memoria depende más de las celdas de la matriz que de las celdas activas.

**La cuenca está mal o es demasiado grande.** Elija otro **Outlet candidate**, cambie el **Snap
radius** o mueva la salida sobre el río.

## Preparar el caso {#preparing}

**Copernicus (CDS) falla o tarda mucho.** CDS pone cada solicitud en una cola, que puede tardar
minutos o más. Si falla, compruebe que `.cdsapirc` tiene la URL y el token actuales sin comillas de
más, y que aceptó las condiciones de ERA5 y ERA5-Land en el sitio web de CDS.

**IMERG devuelve 401 o 403.** Su token de Earthdata venció o no se aceptaron las condiciones de GPM.
Genere un token nuevo y compruebe los permisos del archivo.

**MSWEP no se descarga.** Ejecute `rclone lsd --drive-shared-with-me GoogleDrive:` y compruebe que
la carpeta aprobada aparece en la lista. **MSWEP rclone folder** debe apuntar a su carpeta `Hourly`
o `3hourly`. Si la carpeta aparece pero una ruta da "directory not found", llene **Shared-folder
ID** con el ID de Google Drive de la carpeta, que obtiene con:

```bash
rclone lsjson --dirs-only --drive-shared-with-me --include 'MSWEP_V316_test/' GoogleDrive:
```

**Falta un paso de tiempo de lluvia** (archivos de lluvia locales). La carpeta debe contener cada
paso de tiempo desde el inicio del calentamiento hasta el fin, con los nombres de
[Ajustes del caso](settings#rainfall-folders).

**La construcción se detuvo a medio camino.** Lea el **Process log**. Los archivos descargados se
conservan, así que **Prepare complete case** continúa desde allí después de que usted corrija la
causa.

## Verificar y ejecutar {#checking-and-running}

**La verificación previa falla.** Lea los problemas listados, o `quality_report/preflight.json`
([Verificar un caso](check-a-case)).

**"The final model-resolution D8 area differs by more than a factor of two from the preliminary
HydroSHEDS area."** Probablemente la salida se ajustó a otro río. Elija otra candidata u otro radio
de ajuste, repita la vista previa y vuelva a preparar el caso.

**La simulación de MATLAB no se inicia.** Revise **MATLAB executable**. Si la carpeta de HydroPol2D
MATLAB todavía no existe, la app la descarga con Git: instale Git, o indique una carpeta que ya
contenga HydroPol2D MATLAB.

**"HydroPol2D Python comes with HydroPol2D Studio".** La app no descarga HydroPol2D Python. Abra
`hydropol_python/case.yaml` en HydroPol2D Studio ([Ejecutar el caso](run-the-case#studio)).

**El modelo se queda sin memoria.** Use una malla más gruesa para probar, y ejecute los casos
regionales finos en una estación de trabajo o en un clúster.

**El albedo es 0,25 en todas partes.** Es lo esperado en esta versión.
