---
title: Cuenca de San Francisquito - Evento Controlado LiDAR de 10 m
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Cuenca de San Francisquito - Evento Controlado LiDAR de 10 m

## Objetivo

Este ejemplo simula la tormenta del [ejemplo de 30 m](RainfallRunoff) en una cuadrícula de 10 m de la misma cuenca. Muestra cómo un terreno más detallado cambia el camino del agua y la rapidez con que sale.

## Configuración del caso

El caso `Stanford_10m_LiDAR_Website_100mmh_1h_6h` utiliza:

| Ítem | Valor |
|---|---|
| Dominio | Cuenca del San Francisquito Creek, California, EE. UU. |
| Cuadrícula | 10 m, NAD83 / California Albers (EPSG:3310) |
| Tipo de forzado | Lluvia espacialmente uniforme |
| Evento de lluvia | 100 mm/h de 15 a 75 min (100 mm) |
| Duración de la simulación | 6 h |
| Intervalo de salida de los mapas | 15 min |
| Familia de enrutamiento | Inercial local |
| Tratamiento de salida | Salida por el perímetro |
| Procesos | Infiltración activada; agua subterránea, evapotranspiración, nieve y calidad del agua desactivadas |

## Datos de entrada

Dos entradas son mapas (Figura 1):

- **Terreno.** Un DEM de terreno desnudo de 10 m del USGS 3D Elevation Program (3DEP), dominio público de EE. UU. La mayor parte es una descarga anterior del 3DEP que se guarda con el ejemplo. Su hueco de 5,9 km² en las cabeceras del oeste se rellenó el 2026-11-03 con datos del servicio 3DEPElevation a 10 m, con una transición para que el relleno se una al archivo anterior sin escalón. Se suavizaron veintiséis depresiones y picos de una celda, y el DEM se recortó a la cuenca. Las dos descargas difieren en 2,8 m RMS, sobre todo en las laderas empinadas del oeste, así que este DEM no es solo una copia más fina del de 30 m.
- **Uso y cobertura del suelo.** ESA WorldCover 2020 (v100), el mapa de 30 m del ejemplo de 30 m, leído en la cuadrícula de 10 m. CC BY 4.0. © ESA WorldCover project 2020 / Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium.

Las demás entradas son los valores uniformes del ejemplo de 30 m: una clase de suelo (la clase 8 de la tabla de suelos), una profundidad hasta la roca de 1,5 m, un LAI de 1, un albedo de 0,25 y una humedad inicial del suelo de 0,1104. Estos mapas están en la cuadrícula de 30 m. En 8.374 celdas del borde del dominio (0,5 %), que el mapa de LAI de 30 m no alcanza, el modelo usa un LAI de 0, así que allí no se intercepta la lluvia.

<p align="center">
  <img src={useBaseUrl('/img/examples/stanford-10m-inputs.es.svg')} width="680" alt="Dos mapas de la cuenca del San Francisquito Creek: terreno del DEM de 10 m del USGS 3DEP con sombreado del relieve y cobertura del suelo de ESA WorldCover con la fracción de cada clase" />
</p>

<p align="center">
  <em>Figura 1. Las dos entradas espaciales. Arriba: terreno del DEM de 10 m del USGS 3DEP. Abajo: cobertura del suelo de ESA WorldCover 2020 (mapa de 30 m), con la fracción de cada clase en el dominio. El círculo marca el lago Searsville, donde está la mayor profundidad de la simulación.</em>
</p>

## Video de la simulación

La animación siguiente muestra la simulación a 10 m. Los paneles muestran la profundidad de inundación, la velocidad, la métrica de peligro y la infiltración acumulada sobre el sombreado del DEM. La imagen fija es t = 3,0 h, el momento del caudal máximo que sale por el borde del dominio.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.mp4')} type="video/mp4" />
    Su navegador no admite la etiqueta de video.
  </video>

  <p><em>Simulación de Stanford a 10 m: profundidad de inundación, velocidad, peligro e infiltración acumulada durante seis horas.</em></p>
</div>

Cada panel usa una sola escala de colores para toda la secuencia. La escala se basa en el percentil `99` de todos los cuadros guardados.

## Resultados resumidos

La simulación guardó `25` cuadros de mapa, uno cada 15 min. El resumen de la simulación da:

| Resultado | Valor |
|---|---|
| Área de drenaje | `157,661 km²` |
| Lluvia aplicada | `100,00 mm` |
| Coeficiente de escorrentía | `0,40` (en las 6 h) |
| Caudal máximo que sale por el borde del dominio | `663,01 m³/s` a las 3,0 h |
| Primer pico de ese caudal | `377,13 m³/s` a los 75 min, cuando termina la lluvia |
| Profundidad máxima de inundación | `7,38 m`, en la cuenca del lago Searsville (37,411° N, 122,238° O) |
| Área que superó 1 m de profundidad en algún momento | `4,4 km²` (2,8 % del dominio) |
| Error de volumen | `-1,68 × 10⁻¹¹` de la entrada |

Como en el ejemplo de 30 m, cada celda del borde del dominio deja salir el agua (salida por el perímetro), así que el hidrograma es el caudal que sale por el borde del dominio, no solo el caudal en la desembocadura del arroyo. Los caudales son sus muestras de 15 min. El primer pico, 377,13 m³/s a los 75 min, es la escorrentía de las laderas que sale a lo largo de todo el borde. Luego el caudal baja a 123 m³/s a las 1,75 h. Después, la onda de crecida llega al tramo donde el San Francisquito Creek corre por el borde norte del dominio. El agua que desborda allí sale del modelo, y el caudal vuelve a subir hasta 663,01 m³/s a las 3,0 h. En ese momento, la mayor parte del caudal sale por el borde norte. A las 6 h el caudal es de 186,36 m³/s.

## 10 m y 30 m en las mismas seis horas

El ejemplo de 30 m dura 24 h. La tabla compara las primeras 6 h de las dos simulaciones, con las mismas muestras de 15 min y los mismos cuadros guardados:

| Resultado, primeras 6 h | 30 m | 10 m |
|---|---|---|
| Área de drenaje | 156,8 km² | 157,7 km² |
| Primer pico del caudal que sale por el borde del dominio | 402,84 m³/s a los 75 min | 377,13 m³/s a los 75 min |
| Caudal mínimo entre los dos picos | 110,1 m³/s a las 2,0 h | 123,1 m³/s a las 1,75 h |
| Caudal máximo que sale por el borde del dominio | 473,69 m³/s a las 3,5 h | 663,01 m³/s a las 3,0 h |
| Caudal a las 6 h | 144,72 m³/s | 186,36 m³/s |
| Agua que salió por el borde | 5,34 millones de m³ (34 % de la lluvia) | 6,27 millones de m³ (40 % de la lluvia) |
| Profundidad máxima en los cuadros guardados | 5,82 m | 7,38 m |
| Área con más de 1 m en algún cuadro guardado | 4,2 km² | 4,3 km² |

La tormenta y las demás entradas son las mismas, así que las diferencias vienen del terreno: la cuadrícula más fina y un DEM de otra descarga del 3DEP. En la cuadrícula de 10 m, el pico de las laderas es algo menor. El agua del arroyo que desborda hacia el borde norte llega 30 min antes, y su pico es un 40 % mayor. En seis horas sale del dominio un 17 % más de agua. La mayor profundidad está en la cuenca del lago Searsville en las dos cuadrículas, 1,56 m mayor en la de 10 m.

## Cómo ejecutarlo

El caso está en el repositorio de HydroPol2D en MATLAB, en `Examples/Stanford`. En MATLAB, desde la raíz del repositorio:

```matlab
addpath(fullfile(pwd,'Examples','Stanford'))
run_stanford_local_case('Resolution',10, ...
  'StaticFolder',fullfile('Examples','Stanford','Static_10m_LiDAR'), ...
  'SimulationMinutes',360, ...
  'RainfallTimeseriesPath',fullfile('Examples','Stanford','Forcing','Rainfall','Rainfall_Intensity_Website_100mmh_1h_24h.csv'), ...
  'RecordTimeMapsMinutes',15,'RecordTimeHydrographsMinutes',15, ...
  'OutputTag','Stanford_10m_LiDAR_Website_100mmh_1h_6h')
```

Los resultados se guardan en `Examples/Stanford/Outputs/Reruns_CurrentModel/Stanford_10m_LiDAR_Website_100mmh_1h_6h/Modeling_Results`, con los mismos archivos que el ejemplo de 30 m. La cuadrícula de 10 m tiene nueve veces más celdas que la de 30 m. La simulación tardó unas 10 h en la CPU de un portátil (Apple M4, 24 GB).
