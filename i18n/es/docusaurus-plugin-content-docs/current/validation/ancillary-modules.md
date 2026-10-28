---
title: Embalses, contornos, calidad del agua y riesgo
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Embalses, contornos, calidad del agua y riesgo

Estos casos validan componentes del modelo que son importantes para las aplicaciones, pero que es más fácil probar fuera de una simulación completa de cuenca. La lógica es la misma que en el resto de la suite de validación: aislar el proceso, definir claramente la referencia y separar lo que el caso demuestra de lo que no demuestra.

## Vaciado del embalse con curva de gasto {#reservoir-rating-curve-depletion}

El caso `VAL-RES-001` aísla la lógica de control del embalse mediante un embalse de área constante y una única curva de gasto en la salida. Sin aporte externo, la referencia exacta es la solución de vaciado de la EDO del almacenamiento.

| Caso | RMSE del almacenamiento (m³) | RMSE del caudal de salida (m³/s) | L2 relativo | Error del k recuperado (%) | Residuo de masa (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-RES-001` | 0,2730 | `4.96 × 10^-5` | `7.80 × 10^-6` | 0,0000 | `4.37 × 10^-13` |

El caso superó todos los umbrales. La pequeña diferencia de almacenamiento es el error de truncamiento esperado de la integración explícita respecto de la EDO exacta continua. El balance de agua en sí cierra hasta la precisión numérica.

<img src={useBaseUrl('/validation/results/ancillary/VAL_RES_001_RATING_CURVE.png')} alt="Validación de la curva de gasto del embalse" />

## Condición de contorno con hidrograma de entrada {#inflow-hydrograph-boundary-condition}

El caso `VAL-BC-INFLOW-001` impone un hidrograma triangular conocido en el contorno aguas arriba de un dominio rectangular con momento completo. La referencia es la integral exacta del hidrograma de entrada prescrito. El hidrograma aguas abajo es diagnóstico, porque no se espera una solución analítica de Saint-Venant para el dominio rugoso finito.

| Caso | Error del volumen impuesto (%) | Residuo de masa (%) | Pico en la salida (m³/s) | Desfase del pico (min) | Error de magnitud del pico (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-BC-INFLOW-001` | `3.41 × 10^-13` | `6.44 × 10^-13` | 7,3771 | 5,0 | 7,7862 |

El caso cumplió los criterios de volumen impuesto y de balance de agua. Al final de la simulación, el volumen de entrada prescrito quedó explicado por el caudal descargado en la salida más el agua que seguía almacenada.

<img src={useBaseUrl('/validation/results/ancillary/VAL_BC_INFLOW_001_HYDROGRAPH.png')} alt="Validación del contorno con hidrograma de entrada" />

## Condición de contorno con hidrograma de nivel {#stage-hydrograph-boundary-condition}

Los casos con hidrograma de nivel prescriben una profundidad sinusoidal en el contorno aguas arriba de un dominio rectangular. En cada paso, las celdas de nivel aguas arriba se restablecen al valor prescrito, el solucionador de enrutamiento seleccionado propaga la perturbación y el balance de agua registra el volumen añadido por el contorno, el volumen en la salida y el almacenamiento restante.

El error de aplicación del nivel prescrito fue nulo hasta la precisión numérica con el enrutamiento de momento completo, inercial local, autómatas celulares, cinemático y difusivo. Las amplitudes de la respuesta aguas abajo variaron según el método, lo cual es esperable porque las ecuaciones de enrutamiento no son las mismas, pero todos los errores del balance de agua se mantuvieron muy por debajo de `0.1 %`.

<div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem'}}>
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_FM_001.png')} alt="Validación del contorno de nivel con momento completo" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_LI_001.png')} alt="Validación del contorno de nivel con el modelo inercial local" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_CA_001.png')} alt="Validación del contorno de nivel con autómatas celulares" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_KIN_001.png')} alt="Validación del contorno de nivel con el modelo cinemático" />
  <img src={useBaseUrl('/validation/results/ancillary/VAL_BC_STAGE_DIFF_001.png')} alt="Validación del contorno de nivel con el modelo difusivo" />
</div>

## Lectura de rásteres de lluvia espacial {#spatial-rainfall-raster-ingestion}

El caso `VAL-RAIN-MAP-001` valida la lectura de rásteres, la acumulación temporal, la conversión de unidades y la contabilidad del volumen por celda antes de acoplar los mapas de lluvia al enrutamiento, la infiltración o la ET.

| Caso | RMSE por celda (m) | Error máximo por celda (m) | Volumen total (m³) | Error de volumen (%) | Error máximo por paso (%) |
|---|---:|---:|---:|---:|---:|
| `VAL-RAIN-MAP-001` | 0 | 0 | 75,3333 | 0 | 0 |

El caso se aprobó de forma exacta. Las láminas acumuladas leídas del ráster coincidieron con la referencia prescrita por celda, y el volumen de cada paso coincidió con la integral analítica.

<img src={useBaseUrl('/validation/results/ancillary/VAL_RAIN_MAP_001_TOTALS.png')} alt="Validación de los rásteres de lluvia espacial" />

## Calidad del agua {#water-quality}

El caso de calidad del agua valida la vía actual de acumulación y lavado basada en masa de HydroPol2D antes de intentar cualquier calibración con polutogramas de campo. La escala de los parámetros sigue la acumulación y el lavado de sólidos suspendidos totales al estilo de SWMM, pero la referencia es un balance de masa analítico y no una simulación numérica de SWMM.

Se usaron tres verificaciones deterministas:

- inicialización de la acumulación en tiempo seco;
- lavado exponencial en una sola celda;
- transferencia y exportación conservativas entre dos celdas.

| Caso | RMSE de masa (kg) | Error de exportación (%) | Residuo de masa (kg) | Número de masas negativas |
|---|---:|---:|---:|---:|
| Acumulación en tiempo seco | 0 | 0 | 0 | 0 |
| Lavado en una sola celda | `4.998 × 10^-7` | `2.483 × 10^-4` | 0 | 0 |
| Transferencia entre dos celdas | `6.272 × 10^-8` | `3.722 × 10^-5` | 0 | 0 |

La validación también reveló un artefacto de implementación: la rutina original de lavado redondeaba la masa de contaminante restante a seis decimales en cada subpaso, lo que generaba un error de masa artificial en las pruebas analíticas. Esa cuantización se eliminó, y las métricas del código actual que se muestran arriba corresponden a la implementación corregida.

<img src={useBaseUrl('/validation/results/ancillary/VAL_WQ_001_SINGLE_CELL.png')} alt="Validación de la calidad del agua en una sola celda" />

<img src={useBaseUrl('/validation/results/ancillary/VAL_WQ_001_TWO_CELL.png')} alt="Validación de la calidad del agua en dos celdas" />

## Riesgo e inestabilidad humana {#human-risk-and-instability}

El caso de riesgo humano valida el álgebra implementada y la lógica de clasificación, no la predicción de la seguridad pública a escala de campo. Se probaron dos vías activas de HydroPol2D:

- el índice simple de inestabilidad que se usa cuando `flag_human_instability = 1`;
- el clasificador detallado de equilibrio de fuerzas que se usa cuando `flag_human_instability = 3`.

| Caso | RMSE | Error máximo | Exactitud (%) | Errores en los límites | Número de NaN |
|---|---:|---:|---:|---:|---:|
| Índice simple de inestabilidad | 0 | 0 | 100 | 0 | 0 |
| Clasificador de deslizamiento/vuelco/ahogamiento | 0 | 0 | 100 | 0 | 0 |

La cuadrícula de casos del clasificador detallado recorrió todas las clases de salida implementadas y coincidió exactamente con la referencia independiente.

<img src={useBaseUrl('/validation/results/ancillary/VAL_HR_001_SIMPLE_INSTABILITY.png')} alt="Validación del índice simple de inestabilidad humana" />

<img src={useBaseUrl('/validation/results/ancillary/VAL_HR_001_FORCE_BALANCE.png')} alt="Validación del riesgo humano con el equilibrio de fuerzas detallado" />

## Qué respaldan estos casos {#what-these-cases-support}

Estos casos complementarios respaldan las implementaciones actuales del vaciado de embalses, el tratamiento de los contornos de entrada y de nivel, la lectura de rásteres de lluvia, la contabilidad de la calidad del agua basada en masa y la clasificación del riesgo humano en condiciones controladas.

No sustituyen la calibración de campo, la verificación de los forzamientos específicos de cada sitio ni las pruebas de desempeño con observaciones.
