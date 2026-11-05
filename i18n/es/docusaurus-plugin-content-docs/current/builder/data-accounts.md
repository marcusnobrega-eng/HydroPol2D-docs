---
title: Fuentes de datos y cuentas
---

# Fuentes de datos y cuentas

La mayoría de los datos que usa el Case Builder son descargas abiertas. Tres fuentes necesitan una
cuenta propia. Sus inicios de sesión se quedan en su computadora: el Builder los lee de sus propios
archivos o de variables de entorno, y nunca los escribe en un caso.

| Fuente | Necesaria para | Cuenta |
|---|---|---|
| Copernicus Climate Data Store (CDS) | el clima de ERA5, la humedad inicial del suelo de ERA5-Land, la lluvia de ERA5 y los contornos de GloFAS y GTSM | gratuita, necesaria para todo caso hecho en la app |
| NASA Earthdata | la lluvia de IMERG, y el área foliar cuando el servicio MODIS de ORNL no está disponible | gratuita |
| MSWEP (GloH2O) | la lluvia de MSWEP | aprobación de GloH2O, y rclone para su carpeta de Google Drive |

La lluvia de AORC (Estados Unidos) y los mapas estáticos (terreno, cuencas, cobertura del suelo,
suelos, agua subterránea) no necesitan cuenta. El área foliar viene del servicio web MODIS de ORNL,
sin cuenta. Cuando ese servicio no está disponible, el Builder la toma de NASA LP DAAC, que usa su
inicio de sesión de Earthdata.

La página verifica las cuentas antes de descargar nada. Cuando falta una, un cuadro amarillo dice
"This case cannot be prepared yet:" y la nombra, y **Prepare complete case** sigue en gris.

## Copernicus Climate Data Store {#copernicus-cds}

1. Cree una cuenta en [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/).
2. Inicie sesión y acepte las condiciones de uso de los conjuntos de datos ERA5 y ERA5-Land.
3. Copie su token de acceso personal desde la página de su perfil de CDS.
4. Cree un archivo de texto llamado `.cdsapirc` en su carpeta personal con estas dos líneas:

   ```yaml
   url: https://cds.climate.copernicus.eu/api
   key: YOUR_CDS_PERSONAL_ACCESS_TOKEN
   ```

   En un Mac el archivo es `~/.cdsapirc`, en Windows `%USERPROFILE%\.cdsapirc`. En un Mac,
   protéjalo con `chmod 600 ~/.cdsapirc`.

El token también puede venir de la variable de entorno `CDSAPI_KEY`. CDS pone cada solicitud en una
cola, así que la primera descarga de un caso puede esperar algunos minutos antes de empezar.

## NASA Earthdata {#nasa-earthdata}

1. Cree una cuenta de [NASA Earthdata Login](https://urs.earthdata.nasa.gov/) y acepte las
   condiciones de los datos GPM IMERG.
2. Genere un token en su perfil de Earthdata.
3. Guarde el token, solo en una línea, en este archivo:
   - Mac: `~/.config/hydropol2d-case-builder/earthdata_token`
   - Windows: `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token`

   En un Mac, proteja la carpeta y el archivo:

   ```bash
   mkdir -p ~/.config/hydropol2d-case-builder
   chmod 700 ~/.config/hydropol2d-case-builder
   chmod 600 ~/.config/hydropol2d-case-builder/earthdata_token
   ```

El Builder también acepta el token en la variable de entorno `EARTHDATA_TOKEN`, un archivo
`~/.netrc` con su inicio de sesión de Earthdata, o las variables `EARTHDATA_USERNAME` y
`EARTHDATA_PASSWORD`.

## MSWEP {#mswep}

MSWEP requiere aprobación previa de GloH2O.

1. Solicite acceso en la [página de MSWEP](https://www.gloh2o.org/). El correo de aprobación le da
   una carpeta compartida de Google Drive.
2. Instale [rclone](https://rclone.org) (en un Mac con Homebrew: `brew install rclone`).
3. Ejecute `rclone config` y cree un remoto llamado `GoogleDrive` del tipo `drive`. Complete la
   autorización en su navegador, y no configure la carpeta compartida como una Team Drive.
4. Compruebe que la carpeta compartida es visible:

   ```bash
   rclone lsd --drive-shared-with-me GoogleDrive:
   ```

Cuando elige **MSWEP (hourly)** o **MSWEP (3 hourly)**, la página busca la carpeta autorizada de
MSWEP en sus remotos de rclone. Cuando encuentra una, dice "Authorized MSWEP V3.16 folder found.
Automatic MSWEP download is ready." y llena **MSWEP rclone folder** y **Shared-folder ID
(optional)**. Ambos siguen visibles y puede cambiarlos. El Builder descarga solo los pasos de tiempo
del caso, los recorta al dominio y registra la fuente en `quality_report/mswep_download.json`.
Cuando una solicitud pasa del final del registro **Past**, los pasos de tiempo posteriores vienen
automáticamente de la carpeta **NRT** (casi en tiempo real).

La página advierte que MSWEP V3.16 tiene una tendencia artificial documentada en la precipitación
alrededor de 2015. Para estudios de tendencias entre 1979 y 2021, use V2.80. Los archivos NRT
recientes son preliminares y se revisan después de su primera publicación. MSWEP V3 se cita como
Wang et al. (2026), [MSWEP V3](https://arxiv.org/abs/2602.01436).

Si ya tiene la lluvia en archivos, use en su lugar **Existing rainfall directory (optional)**
([Ajustes del caso](settings#rainfall-folders)).

## Licencias de los datos {#data-licenses}

Los conjuntos de datos de entrada conservan sus propias licencias y condiciones de acceso, y usted
las sigue cuando usa sus datos. Cada caso registra cada fuente y su versión en
`quality_report/public_static_sources.json` y en su `manifest.json`.
