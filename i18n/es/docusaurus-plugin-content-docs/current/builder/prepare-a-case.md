---
title: Preparar un caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Preparar un caso

Después de una vista previa con los ajustes actuales, **Prepare complete case** construye el caso.
Un cuadro de estado muestra la etapa y una barra de progreso. La construcción:

1. descarga los datos que todavía no tiene: terreno, cobertura del suelo, suelos, profundidad hasta
   la roca, agua subterránea, área foliar y la lluvia y el clima del periodo (el primer caso de una
   región es el que más tarda, y los siguientes reutilizan la caché);
2. acondiciona el terreno con HydroBathyDEM, que viene con la app, para que el agua llegue a las
   salidas, y da anchos y profundidades a los cauces;
3. para un caso Catchment, delimita la cuenca final en la malla del modelo;
4. lleva cada capa a la malla del modelo y escribe las series de lluvia, clima y contorno;
5. escribe los archivos de modelo que eligió en **Prepare for**;
6. ejecuta la [verificación previa](check-a-case).

Cuando termina, el cuadro dice "Case preparation complete" y la página muestra el caso, el resultado
de la verificación y los paneles de ejecución ([Ejecutar el caso](run-the-case)). Si se detiene, el
cuadro dice "Case preparation stopped" con el error, y el **Process log** tiene los detalles. Una
construcción fallida conserva los archivos que descargó, así que el siguiente intento continúa desde
allí.

Cuánto tarda depende del tamaño del dominio, del periodo y de los servicios de datos. El caso de
San Francisquito Creek a 10 m que se muestra abajo (99 km², 987.647 celdas activas) tardó de 2 a 4
minutos, la mayor parte esperando al servicio de Copernicus, y descargó unos 10 MB.

<p align="center">
  <img src={useBaseUrl('/img/builder/stanford-terrain.jpg')} width="620" alt="Terreno sombreado de la cuenca de San Francisquito Creek en Stanford, California, en una malla de 10 m, con la red de ríos en azul y el borde de la cuenca" />
</p>

<p align="center">
  <em>Figura 1. Terreno de la cuenca de San Francisquito Creek preparado por el Case Builder en una malla de 10 m, con su red de ríos y el borde de la cuenca. El terreno es USGS 3DEP, que usted da como un DEM local o elige en la línea de comandos.</em>
</p>

<p align="center">
  <img src={useBaseUrl('/img/builder/stanford-layers.png')} width="760" alt="Tres mapas del caso de San Francisquito Creek en la misma malla de 10 m: clases de cobertura del suelo, anchos de los cauces y profundidad hasta la roca" />
</p>

<p align="center">
  <em>Figura 2. Tres capas más del mismo caso en la misma malla: la cobertura del suelo, los cauces y la profundidad hasta la roca.</em>
</p>

## Qué hay en la carpeta del caso {#case-folder}

La carpeta lleva el nombre del lugar, el tamaño de celda y la fecha de inicio, por ejemplo
`tucson_urban_only_250m_20210723`. Un caso completo tiene esta estructura general. Las carpetas
aparecen solo cuando el caso las necesita: por ejemplo, `hydropol_matlab` no existe en un caso
preparado solo para Python.

```text
CASE_DIR/
├── case.json                     la solicitud y la estimación del dominio
├── manifest.json                 cada fuente, versión y archivo del caso
├── domain.gpkg                   el dominio del modelo
├── final_domain.gpkg             Catchment: la cuenca en la malla del modelo
├── outlet_candidates.gpkg        Catchment: la salida indicada y las tres candidatas
├── preliminary_catchment.gpkg    Catchment: el primer contorno de HydroSHEDS
├── hydropol_config.json          los ajustes del modelo del caso
├── input_contract.json           la lista de entradas del modelo y sus archivos
├── figures/                      domain_preview.html y .png, otros mapas de vista previa
├── hydropol_python/              case.yaml, run_case.py y el NetCDF de lluvia
├── hydropol_matlab/              run_case.m y sus rutas de entrada
├── processed_inputs/
│   ├── Static/                   los mapas en la malla del modelo
│   └── Forcing/                  series de lluvia, clima y contorno
├── rainfall_summaries/           totales de lluvia para verificar
├── quality_report/               preflight.json y las demás verificaciones
└── Outputs/                      resultados del modelo, después de una simulación
```

### Los mapas {#maps}

Los mapas principales de `processed_inputs/Static/` son:

| Archivo | Qué contiene |
|---|---|
| `DEM.tif` | el terreno acondicionado por HydroBathyDEM, la superficie del modelo |
| `DomainMask.tif` | el dominio activo del modelo |
| `LULC.tif` | clases de cobertura del suelo de ESA WorldCover |
| `SOIL.tif` | clases de textura del suelo USDA |
| `DTB.tif` | profundidad hasta la roca |
| `GW_table.tif` | elevación inicial del agua subterránea |
| `Initial_Soil_Moisture.tif` | humedad inicial del suelo para MATLAB, en mm por encima del contenido de agua residual |
| `Initial_Soil_Moisture_Fraction.tif` | contenido volumétrico de agua inicial para Python |
| `LAI.tif` | índice de área foliar |
| `Albedo.tif` | albedo, una constante de 0,25 en esta versión |
| `RiverWidths.tif`, `RiverDepths.tif` | la geometría de los cauces |
| `D4_flow_direction.tif`, `D4_idx_facc.tif` | los mapas de enrutamiento de HydroBathyDEM |
| `FlowDirectionD8.tif`, `FlowAccumulationD8.tif` | Catchment: los mapas D8 que delimitan la cuenca |
| `BoundaryConditionMask.tif` | Catchment: las celdas de salida con profundidad crítica |

Los mapas categóricos (cobertura del suelo, clases de suelo) se remuestrean por vecino más cercano,
y los mapas continuos con una interpolación adecuada a cada fuente.

### Los informes {#reports}

`quality_report/` guarda las verificaciones de la construcción, entre ellas:

- `preflight.json`: el resultado de la verificación ([Verificar un caso](check-a-case));
- `terrain_domain_qa.json` y `hydraulic_terrain_qa.json`: el terreno, el dominio y los cambios que
  hizo HydroBathyDEM;
- `public_static_sources.json`: las fuentes de los mapas estáticos;
- `rainfall_summary.json`, `initial_soil_moisture.json` y, para MSWEP, `mswep_download.json`.

Conserve `case.json`, `manifest.json`, `quality_report/` y los archivos del modelo con cualquier
simulación publicada: registran cómo se hizo el caso.

## Antes de confiar en un caso nuevo {#before-you-trust}

Un caso que pasa la verificación está completo y es coherente, lo que todavía no dice nada sobre su
precisión. Antes de leer resultados para un lugar nuevo:

1. revise la cuenca y la red de ríos;
2. abra en un SIG los mapas de terreno, cobertura del suelo, suelo, agua subterránea y cauces;
3. compare los totales de lluvia con el producto de origen;
4. verifique las condiciones de contorno y la costa;
5. compare el caudal o la inundación simulados con observaciones independientes;
6. anote cualquier parámetro que cambie después de crear el caso.
