---
title: Cuenca de San Francisquito - Ejemplo de Lluvia Controlada
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Cuenca de San Francisquito - Ejemplo de Lluvia Controlada

## Objetivo

Este ejemplo presenta una simulación controlada de lluvia y escorrentía para la cuenca del San Francisquito Creek, cerca de Stanford, California. Muestra cómo responde HydroPol2D, en una cuenca real, a una tormenta cuyo momento y volumen se conocen con exactitud.

## Configuración del caso

El caso `Stanford_30m_Website_100mmh_1h_24h` utiliza:

| Ítem | Valor |
|---|---|
| Dominio | Cuenca del San Francisquito Creek, California, EE. UU. |
| Cuadrícula | 30 m, NAD83 / California Albers (EPSG:3310) |
| Tipo de forzado | Lluvia espacialmente uniforme |
| Evento de lluvia | 100 mm/h de 15 a 75 min (100 mm) |
| Duración de la simulación | 24 h |
| Intervalo de salida de los mapas | 15 min |
| Familia de enrutamiento | Inercial local |
| Tratamiento de salida | Salida por el perímetro |
| Procesos | Infiltración activada; agua subterránea, evapotranspiración, nieve y calidad del agua desactivadas |

## Datos de entrada

Dos entradas son mapas (Figura 1):

- **Terreno.** El DEM de terreno desnudo del USGS 3D Elevation Program (3DEP), leído del servicio 3DEPElevation a 10 m y promediado a la cuadrícula de 30 m (descargado el 2026-11-02, dominio público de EE. UU.).
- **Uso y cobertura del suelo.** ESA WorldCover 2020 (v100), CC BY 4.0. © ESA WorldCover project 2020 / Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium. Los códigos de clase 10 a 90 de la tabla de uso del suelo son los de WorldCover.

Las demás entradas son valores uniformes definidos para el ejemplo, sin datos externos: una clase de suelo (la clase 8 de la tabla de suelos), una profundidad hasta la roca de 1,5 m, un LAI de 1, un albedo de 0,25 y una humedad inicial del suelo de 0,1104. Los demás parámetros vienen del libro de cálculo del caso Stanford que se distribuye con el modelo en MATLAB.

<p align="center">
  <img src={useBaseUrl('/img/examples/stanford-30m-inputs.es.svg')} width="680" alt="Dos mapas de la cuenca del San Francisquito Creek: terreno del USGS 3DEP con sombreado del relieve y cobertura del suelo de ESA WorldCover con la fracción de cada clase" />
</p>

<p align="center">
  <em>Figura 1. Las dos entradas espaciales en la cuadrícula de 30 m. Arriba: terreno del USGS 3DEP. Abajo: cobertura del suelo de ESA WorldCover 2020, con la fracción de cada clase en el dominio. El círculo marca el lago Searsville, donde está la mayor profundidad de la simulación.</em>
</p>

## Qué pretende mostrar este caso

Este caso destaca:

- la generación de escorrentía bajo un forzado simple y conocido;
- la interacción entre topografía, rugosidad e infiltración;
- la organización espacial de la profundidad, la velocidad, el peligro y la infiltración acumulada de la inundación;
- el comportamiento de recesión larga después de que termina el pulso de lluvia.

## Video de la simulación

La animación siguiente muestra la simulación a 30 m. Los paneles muestran la profundidad de inundación, la velocidad, la métrica de peligro y la infiltración acumulada sobre el sombreado del DEM. La imagen fija es t = 3,5 h, el momento del caudal máximo en la salida.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_30m_website_100mmh_1h_24h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_30m_website_100mmh_1h_24h_panels.mp4')} type="video/mp4" />
    Su navegador no admite la etiqueta de video.
  </video>

  <p><em>Simulación de lluvia controlada en Stanford, 30 m: profundidad de inundación, velocidad, peligro e infiltración acumulada.</em></p>
</div>

Cada panel usa una sola escala de colores para toda la secuencia. La escala se basa en el percentil `99` de todos los cuadros guardados.

## Resultados resumidos

La simulación guardó `97` cuadros de mapa, uno cada 15 min. El resumen de la simulación da:

| Resultado | Valor |
|---|---|
| Área de drenaje | `156,823 km²` |
| Lluvia aplicada | `100,00 mm` |
| Coeficiente de escorrentía | `0,47` |
| Caudal máximo en la salida | `473,69 m³/s` a las 3,5 h |
| Primer pico en la salida | `402,84 m³/s` a los 75 min, cuando termina la lluvia |
| Profundidad máxima de inundación | `5,87 m`, en la cuenca del lago Searsville (37,410° N, 122,234° O) |
| Área que superó 1 m de profundidad en algún momento | `4,3 km²` (2,7 % del dominio) |
| Error de volumen | `-6,45 × 10⁻¹²` de la entrada |

Los caudales son las muestras de 15 min del hidrograma de salida. Tiene dos picos: 402,84 m³/s a los 75 min, cuando termina la lluvia, y 473,69 m³/s a las 3,5 h. Entre ellos, el caudal baja a 110 m³/s a las 2 h y luego vuelve a subir.

## Cómo ejecutarlo

El caso está en el repositorio de HydroPol2D en MATLAB, en `Examples/Stanford`. En MATLAB, desde la raíz del repositorio:

```matlab
addpath(fullfile(pwd,'Examples','Stanford'))
run_stanford_local_case('Resolution',30,'SimulationMinutes',1440, ...
  'RainfallTimeseriesPath',fullfile('Examples','Stanford','Forcing','Rainfall','Rainfall_Intensity_Website_100mmh_1h_24h.csv'), ...
  'RecordTimeMapsMinutes',15,'RecordTimeHydrographsMinutes',15, ...
  'OutputTag','Stanford_30m_Website_100mmh_1h_24h')
```

Los resultados se guardan en `Examples/Stanford/Outputs/Reruns_CurrentModel/Stanford_30m_Website_100mmh_1h_24h/Modeling_Results`: mapas de profundidad, velocidad y peligro cada 15 min, el hidrograma de salida (`Tables_CSV/Outlet_Hydrograph_Data_Outlet.csv`) y el resumen de la simulación (`Tables_CSV/Summary_Table.csv`).

Una simulación más corta de la misma tormenta, de 3 h en lugar de 24 h, se inicia con `run('Examples/Stanford/run_excel.m')` y tarda unos 14 min en un portátil. El README del repositorio indica sus resultados esperados.
