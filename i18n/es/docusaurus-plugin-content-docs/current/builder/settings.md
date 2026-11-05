---
title: Ajustes del caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Ajustes del caso

Debajo del área del modelo, cada pestaña de **Prepare a case** tiene los mismos grupos de ajustes,
de arriba abajo: **Grid and period**, **Forcing and model adapter**, **Simulated processes**,
**River representation** (con **Hydraulic parameters**), **Saved outputs**, **Urban boundary
conditions** (Urban Area Only), las carpetas de lluvia y **Folders and advanced paths**.

Los valores por defecto difieren entre las pestañas urbanas y la pestaña Catchment:

| Ajuste | Urban Basin y Urban Area Only | Catchment |
|---|---|---|
| Tamaño de celda | 90 m | 1.000 m |
| Área de inicio de los ríos | 5 km² | 10 km² |
| Producto de lluvia | IMERG (30 minutes) | MSWEP (3 hourly) |
| Flujo base del acuífero profundo | desactivado | activado |
| Paquete de salida | Standard | Full |
| Intervalo de mapas | 60 minutos | 180 minutos |
| Intervalo de hidrogramas | 10 minutos | 60 minutos |

Cualquier cambio de un ajuste pide una nueva [vista previa](preview-and-cost) antes de poder
preparar el caso.

## Grid and period {#grid-and-period}

| Ajuste | Qué define |
|---|---|
| **Grid type** | Solo en las pestañas urbanas. **Uniform grid** o **Quadtree grid** (ver más abajo). |
| **Cell size (m)** | El tamaño de celda del modelo. No puede ser más fino que el terreno: unos 30 m con FABDEM. |
| **Warm-up (days)** | Días simulados antes de la fecha de inicio, para que los suelos y los ríos se estabilicen. La lluvia y el clima se preparan desde el inicio del calentamiento. Por defecto, 0. |
| **River initiation area (km2)** | El área aguas arriba a partir de la cual empieza un cauce. |
| **Terrain source** | **FABDEM**, o **Local georeferenced DEM** con su **Local DEM path**. |
| **Simulation start date (UTC)**, **Start time (UTC)** | El inicio de la simulación. |
| **Simulation end date (UTC)**, **End time (UTC)** | El fin de la simulación. |

Las fechas están en UTC, desde 1979-01-01 hasta hoy. Puede escribir el año en el campo de fecha.

### Quadtree grid {#quadtree-grid}

Una malla quadtree usa celdas cuadradas de varios tamaños. La ciudad conserva las celdas finas y el
resto del dominio recibe celdas más gruesas, lo que reduce el número de celdas de una cuenca grande.

- **Fine cell size (m)**: las celdas sobre la ciudad y su franja.
- **Coarse cell size (m)**: las celdas lejos de la ciudad. Debe ser el tamaño fino multiplicado por
  2, 4, 8, etc. Por defecto, es cuatro veces el tamaño fino.
- **Fine-grid buffer (m)**: hasta dónde llegan las celdas finas alrededor de la ciudad (120 m por
  defecto).

Entre los niveles, la transición usa dos celdas por nivel, y las celdas vecinas difieren como máximo
en un factor de dos. Los ríos no cambian el tamaño de celda. Con 90 m y 360 m, por ejemplo, la
ciudad y 120 m a su alrededor tienen celdas de 90 m, sigue una banda de celdas de 180 m, y el resto
de la cuenca tiene celdas de 360 m. El modelo lee esta malla directamente con su solver de malla
nativo.

## Forcing and model adapter {#forcing}

**Rainfall product** elige una sola fuente de lluvia para todo el caso. El Builder nunca completa
un producto con otro.

| Rainfall product | Paso de tiempo | Área | Cuenta |
|---|---|---|---|
| **IMERG (30 minutes)** | 30 min | global | NASA Earthdata |
| **MSWEP (hourly)** | 1 h | global | aprobación de GloH2O y rclone |
| **MSWEP (3 hourly)** | 3 h | global | aprobación de GloH2O y rclone |
| **ERA5 (hourly)** | 1 h | global | Copernicus CDS |
| **AORC CONUS (hourly, approximately 1 km)** | 1 h | Estados Unidos contiguos | ninguna |

Antes de la vista previa, la página muestra el periodo que cubre cada fuente (por ejemplo "NASA
IMERG Final Run availability") y detiene una solicitud fuera de él. Los casos MSWEP horarios
empiezan en una hora UTC completa, y los de 3 horas a las 00, 03, 06, 09, 12, 15, 18 o 21 UTC. El
clima siempre viene de ERA5. La lluvia y el clima se quedan en sus propias mallas, y HydroPol2D las
muestrea durante la simulación: una malla del modelo de 90 m no hace que la lluvia sea de 90 m.

**Prepare for** elige los archivos de modelo que recibe el caso:

| Prepare for | El caso recibe |
|---|---|
| **HydroPol2D Python** | `hydropol_python/case.yaml` y `run_case.py`, para HydroPol2D Studio |
| **HydroPol2D MATLAB** | `hydropol_matlab/run_case.m`, para HydroPol2D MATLAB |
| **Python and MATLAB** | ambos |
| **Inputs only** | los mapas y las series, sin archivos de modelo |

## Simulated processes {#processes}

**Canopy interception**, **Infiltration**, **Groundwater** y **Evapotranspiration** están marcados
por defecto. Desmarque un proceso para dejarlo fuera. Los mapas que dependen de él quedan entonces
fuera de las salidas guardadas, y los ajustes de agua subterránea de más abajo aparecen en gris
cuando **Groundwater** está desactivado. La lluvia, el enrutamiento superficial inercial local y los
contornos de flujo crítico siempre siguen activados.

## River representation {#river-representation}

**Subgrid formulation** define cómo se representan los ríos más estrechos que una celda:

| Opción | Qué hace |
|---|---|
| **Auto** | **No subgrid** cuando las celdas más grandes coinciden con la resolución del terreno. En otro caso, **Neal channel** en mallas uniformes, y **Hydraulic tables** en mallas quadtree y en casos Urban Area Only. |
| **Neal channel** | un canal de ancho y profundidad dados dentro de cada celda de río. Solo en mallas uniformes, así que no se ofrece para mallas quadtree ni para Urban Area Only. |
| **Hydraulic tables** | tablas de almacenamiento y de capacidad de conducción calculadas a partir del terreno fino. **Hydraulic table coverage** elige **Rivers only** o **All active cells**. |
| **No subgrid** | solo el terreno de la celda. |

**All active cells** trata cada celda como un depósito de nivel horizontal. La página advierte que
esto puede distorsionar el flujo generado por la lluvia en laderas empinadas, así que elíjalo a
propósito. El terreno acondicionado por HydroBathyDEM se convierte en la superficie del modelo.
Después de la construcción, la página informa qué proporción de celdas cambió HydroBathyDEM, y el
mayor descenso y el mayor ascenso del terreno.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-river-hydraulics.png')} width="760" alt="Las casillas de Simulated processes, las opciones de River representation Auto, Neal channel, Hydraulic tables y No subgrid, y el panel Hydraulic parameters abierto con los valores de n de Manning, el intercambio río-agua subterránea, los ajustes del acuífero profundo, la fuente de parámetros del acuífero somero, la conductividad y el espesor del lecho del río, la casilla de confirmación y el ráster opcional de conductividad del lecho del río" />
</p>

<p align="center">
  <em>Figura 1. Simulated processes, River representation y el panel Hydraulic parameters abierto de un caso Urban Basin. Los ajustes del acuífero profundo aparecen en gris porque Deep-aquifer baseflow está desactivado.</em>
</p>

### Hydraulic parameters {#hydraulic-parameters}

El panel **Hydraulic parameters** está plegado por defecto.

| Ajuste | Por defecto | Qué define |
|---|---|---|
| **Channel Manning n** | 0,035 | rugosidad de los cauces |
| **Surface Manning fallback** | 0,05 | rugosidad donde la tabla de cobertura del suelo no tiene valor |
| **River-groundwater exchange** | activado | intercambio de agua entre los ríos y el agua subterránea (necesita **Groundwater**) |
| **Deep-aquifer baseflow** | activado en Catchment | un almacenamiento profundo lento por subcuenca que alimenta el flujo base (pestaña Catchment, sin tablas hidráulicas) |
| **Deep recharge fraction** | 0,05 | proporción de la recarga que va al almacenamiento profundo |
| **Deep response time (days)** | 180 | qué tan lento se vacía el almacenamiento profundo |
| **Subbasin threshold (km²)** | 100 | el tamaño de las subcuencas del acuífero profundo |
| **Deep-aquifer starting state** | Empty | **Empty**, **Baseflow on the start date** (con **Deep baseflow q0 (mm/day)**) o **Steady state from mean recharge** (con **Mean recharge (mm/year)**) |
| **Shallow-aquifer Ksat,h and Sy** | Spatial maps with class fallback | ver más abajo |
| **Riverbed conductivity (m/s)** | 1,0e-6 | conductividad del lecho del río para el intercambio |
| **Riverbed thickness (m)** | 0,50 | espesor del lecho del río |
| **Confirm this riverbed conductivity for the case** | sin marcar | debe estar marcada mientras el intercambio está activado |
| **Riverbed conductivity raster (optional)** | vacío | un mapa que reemplaza el valor único |

La conductividad del lecho del río no tiene un mapa global fiable, así que el Builder le pide que
confirme el valor. Con el intercambio activado y la casilla sin marcar, la vista previa se detiene
con "Confirm riverbed hydraulic conductivity when river-groundwater exchange is enabled."

**Shallow-aquifer Ksat,h and Sy** define la conductividad horizontal y el rendimiento específico
del acuífero somero:

- **Spatial maps with class fallback**: los mapas de agua subterránea donde tienen valores, y las
  tablas de clases en el resto.
- **Uniform effective values**: un **Uniform groundwater Ksat,h (m/s)** (por defecto 1,000e-5) y un
  **Uniform specific yield Sy** (por defecto 0,100) en todo el dominio, por ejemplo valores de una
  calibración por recesión.
- **Calibrate from observed streamflow**: pestaña Catchment, cuando el caso se prepara para Python.
  Primero se prepara el caso, y luego la calibración se ejecuta desde **Check a case**
  ([Verificar un caso](check-a-case#groundwater-calibration)).

## Saved outputs {#saved-outputs}

| Ajuste | Qué define |
|---|---|
| **Output package** | **Quick** guarda los extremos y los hidrogramas. **Standard** agrega el archivo de mapas nativo, las figuras y los videos principales. **Full** también escribe copias GeoTIFF de cada mapa guardado. |
| **Map interval (minutes)** | cada cuánto se guardan los mapas |
| **Hydrograph interval (minutes)** | cada cuánto se guardan los hidrogramas y los diagnósticos |

Las casillas de abajo eligen los mapas guardados: profundidad de inundación fuera del cauce,
velocidad en el cauce y en la llanura de inundación, intensidad de lluvia, lluvia acumulada,
infiltración acumulada, profundidad del agua subterránea, recarga acumulada del agua subterránea,
ascenso capilar acumulado, saturación de la zona de raíces, saturación de la zona de transmisión,
evaporación potencial acumulada y evapotranspiración real acumulada. Un mapa cuyo proceso está
desactivado aparece en gris. La vista previa estima el tamaño de lo que usted elige.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-saved-outputs.png')} width="760" alt="El grupo Saved outputs con Output package Standard, intervalo de mapas de 60 minutos, intervalo de hidrogramas de 10 minutos y doce mapas de salida marcados" />
</p>

<p align="center">
  <em>Figura 2. Saved outputs de un caso urbano: el paquete Standard, mapas cada hora, hidrogramas cada 10 minutos y los doce mapas.</em>
</p>

## Urban boundary conditions {#urban-boundary-conditions}

Este grupo está en la pestaña **Urban Area Only**.

| Ajuste | Qué define |
|---|---|
| **Exterior buffer (km)** | la franja alrededor de la mancha urbana (1 km por defecto) |
| **GloFAS river inflows** | caudales de entrada de ríos de GloFAS v4 donde los ríos entran en el dominio. El caudal de entrada usa el ancho de cauce del mapa de ríos del caso. |
| **GloFAS time handling** | **step** o **linear** entre valores de GloFAS |
| **Coastal water level** | **Disabled**, **GTSM total water level** o **GTSM astronomical tide** |
| **Tide time handling** | **linear** o **step** entre valores de GTSM |
| **Groundwater boundary** | **Local storage only**, **Dynamic no-flow** o **Dynamic fixed head** |
| **GTSM-to-model datum offset (m)** y **Datum confirmed** | se muestran cuando hay un nivel costero activado. GTSM se refiere al nivel medio del mar. Introduzca el desfase local respecto del datum del terreno y marque **Datum confirmed**. Cero, confirmado, indica que los dos son iguales en este lugar. |
| **Reviewed boundary overrides (optional JSON)** | un archivo de elecciones de contorno revisadas |

La marea se aplica solo a celdas exteriores bajas que WorldCover marca como agua permanente, cerca
de la costa de GTSM. GTSM da el nivel del agua, no la línea de costa. Las series de GTSM terminan
en 2024, así que las fechas posteriores necesitan **Disabled**. La construcción escribe el plan de
contornos y las series en `processed_inputs/Forcing/Boundary` y detiene la verificación si los
bordes se superponen o si un contorno activado no tiene datos.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-urban-boundaries.png')} width="760" alt="El grupo Urban boundary conditions con una franja exterior de 1 km, GloFAS river inflows sin marcar, GloFAS time handling step, coastal water level Disabled, tide time handling linear, groundwater boundary Local storage only y un campo de reemplazos vacío, con la nota de que la prioridad es marea, luego caudal de entrada de GloFAS y luego flujo crítico" />
</p>

<p align="center">
  <em>Figura 3. Urban boundary conditions con sus valores por defecto: flujo crítico en cada borde exterior.</em>
</p>

## Carpetas de lluvia {#rainfall-folders}

**Existing rainfall directory (optional)** usa archivos de lluvia que usted ya tiene en lugar de una
descarga. La carpeta debe contener cada paso de tiempo desde el inicio del calentamiento hasta el
fin de la simulación, como GeoTIFF en mm/h con nombres como estos:

```text
IMERG_30min_mmhr_YYYY_MM_DD_HH_MM.tif
AORC_1h_mmhr_YYYY_MM_DD_HH_MM.tif
ERA5_1h_mmhr_YYYY_MM_DD_HH_MM.tif
MSWEP_1h_mmhr_YYYY_MM_DD_HH_MM.tif
MSWEP_3h_mmhr_YYYY_MM_DD_HH_MM.tif
```

Para un producto MSWEP sin carpeta local, aparecen dos campos más: **MSWEP rclone folder** y
**Shared-folder ID (optional)**. Cuando rclone ya tiene acceso a la carpeta de MSWEP, la página la
encuentra y llena ambos. Vea [Fuentes de datos y cuentas](data-accounts#mswep).

## Folders and advanced paths {#folders}

El panel **Folders and advanced paths** está plegado por defecto.

| Ajuste | Qué define |
|---|---|
| **Output directory** | dónde van los casos nuevos. En la app: `Documents/HydroPol2D Case Builder/outputs` en su carpeta personal. |
| **Cache directory** | dónde se guardan los datos y las herramientas descargados (`~/.cache/hydropol2d-case-builder`), compartido por todos los casos |
| **HydroPol2D checkout (optional)** | una carpeta de HydroPol2D MATLAB, registrada con el caso |
| **Vadose and aquifer parameters** | **Class tables**, o **SoilGrids + GLHYMPS (CONUS automatic)** |
| **Groundwater Kh/Kv ratio** | la razón entre la conductividad horizontal y la vertical, usada por debajo de 2 m (100 por defecto) |
| **Subsurface scheme** | **legacy**, o **layered** (capas de suelo sobre capas de roca hasta la roca madre, para HydroPol2D Python) |
| **Rock specific yield** | solo layered: **derived_capped** (limitado por la porosidad de GLHYMPS) o **derived** |
| **Spatial soil parameter raster directory (optional)** | una carpeta de GeoTIFF de parámetros del suelo. Sus valores reemplazan las tablas de clases donde tienen datos. |

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-folders.png')} width="760" alt="El panel Folders and advanced paths abierto con el directorio de salida, el directorio de caché, un campo HydroPol2D checkout vacío, Vadose and aquifer parameters Class tables, una razón Kh/Kv de 100, el esquema de subsuelo legacy, rock specific yield derived_capped en gris y el directorio de rásteres espaciales de parámetros del suelo" />
</p>

<p align="center">
  <em>Figura 4. Folders and advanced paths. Rock specific yield aparece en gris porque el esquema de subsuelo es legacy.</em>
</p>
