---
title: Cuenca de San Francisquito - Ejemplo con Lluvia Observada
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Cuenca de San Francisquito - Ejemplo con Lluvia Observada

## Objetivo

Este ejemplo describe la configuración de evento de la cuenca San Francisquito cuando el forzamiento de lluvia proviene de datos observados. El foco está en los datos necesarios para la simulación del evento y la comparación de hidrogramas.

## Configuración del caso

La simulación actual del evento utiliza:

| Ítem | Valor |
|---|---|
| Resolución de cuadrícula | 30 m |
| Profundidad de lluvia | 75 mm |
| Duración de la simulación | 48 h |
| Familia de enrutamiento | Inercial local |
| Tratamiento de salida | Salida por el perímetro |
| Observaciones de caudal en la ejecución actual | No disponibles |
| Puntos de comparación | Generados a partir de percentiles de acumulación de flujo |

La repetición actual no incluyó un archivo válido de caudal observado. Por eso, HydroPol2D generó puntos de comparación a partir de la red de drenaje. La página documenta la configuración del evento y la respuesta del modelo para la estructura actual.

## Video de simulación

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_30m_outlet020_fullperiod_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_30m_outlet020_fullperiod_panels.mp4')} type="video/mp4" />
    Su navegador no soporta la etiqueta de video.
  </video>

  <p><em>Simulación de evento en San Francisquito, 30 m: profundidad de inundación, velocidad, peligro e infiltración acumulativa.</em></p>
</div>

## Lo que muestra este ejemplo

La configuración con lluvia observada requiere:
- forzamiento de lluvia observado, idealmente interpolado a partir de múltiples medidores cuando esos datos estén disponibles;
- datos de descarga o etapa observados en el lugar de comparación;
- tratamiento explícito de las condiciones iniciales, especialmente la humedad antecedente;
- confirmación cuidadosa de que el punto de observación representa el área de drenaje modelada.

## Resultados resumidos

La simulación actual del evento produjo:

- un caudal pico de `260.57 m³/s`;
- una profundidad máxima de inundación de `0.31 m`;
- una respuesta enrutada de 48 h con mapas guardados en el mismo formato de cuatro paneles usado en el ejemplo controlado.
