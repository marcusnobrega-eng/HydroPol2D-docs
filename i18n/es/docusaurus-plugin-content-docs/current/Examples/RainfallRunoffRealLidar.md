---
title: Cuenca de San Francisquito - Evento Controlado LiDAR de 10 m
# Hidden until the 10 m case is rerun with the current model; its numbers are from an older code.
draft: true
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Cuenca de San Francisquito - Evento Controlado LiDAR de 10 m

## Objetivo

Este ejemplo presenta la simulación de San Francisquito con LiDAR de 10 m. Muestra cómo responde el modelo cuando el terreno se representa con un DEM más detallado.

## Configuración del caso

El ejemplo de 10 m utiliza:
- un 10 m USGS o 3DEP DEM real para el dominio Stanford;
- rásteres Stanford auxiliares alineados con esa cuadrícula 10 m;
- el mismo evento de lluvia controlada utilizado en el ejemplo 30 m;
- un tratamiento de salida por el perímetro.

| Ítem | Valor |
|---|---|
| Resolución de cuadrícula | 10 m |
| Forzamiento | 100 mm/h durante 1 hora |
| Duración de la simulación | 6 h |
| Intervalo de salida del mapa | 15 min |
| Fotogramas de mapa guardados | 24 |
| Familia de enrutamiento | Inercial local |
| Tratamiento de salida | Salida por el perímetro |

## Video de simulación

La animación siguiente muestra la simulación a 10 m. Los paneles presentan la profundidad de la inundación, la velocidad, la métrica de peligro y la infiltración acumulativa.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.mp4')} type="video/mp4" />
    Su navegador no soporta la etiqueta de video.
  </video>

  <p><em>Simulación LiDAR de 10 m en San Francisquito: profundidad de inundación, velocidad, peligro e infiltración acumulativa durante seis horas.</em></p>
</div>

## Resumen de la respuesta en seis horas

El resumen siguiente se refiere a la misma simulación de seis horas mostrada en la secuencia de mapas.

| Métrica | Valor |
|---|---:|
| Resolución de cuadrícula | 10 m |
| Duración publicada | 6 h |
| Fotogramas de mapa guardados | 24 |
| Secuencia de mapas cubierta | 00:00 a 05:45 |
| Caudal pico en la ventana de seis horas | 448.06 m³/s |
| Momento del pico | 180.00 min |
| Caudal de salida a las 6 h | 115.69 m³/s |
| Profundidad máxima en los fotogramas guardados | 6.91 m |
| Velocidad máxima en los fotogramas guardados | 10.00 m/s |
| Métrica máxima de peligro en los fotogramas guardados | 25.38 m²/s |
| Infiltración acumulada máxima | 474.60 mm |

### Hidrograma y lluvia
<img src={useBaseUrl('/figures/Stanford_10m_6h_Hydrograph_Rainfall.png')} alt="Hidrograma recuperado de 10 m" />

## Lo que muestra este ejemplo

Este ejemplo destaca:

- el efecto de una representación más detallada del terreno sobre los patrones locales de inundación;
- la respuesta enrutada durante las seis primeras horas de simulación;
- las diferencias que aparecen cuando el mismo forzamiento se aplica en los dominios de 10 m y 30 m.
