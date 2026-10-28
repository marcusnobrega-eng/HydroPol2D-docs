---
title: Módulos hidrológicos
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validación de módulos hidrológicos

Esta página documenta los casos de validación de intercepción del dosel, nieve, infiltración y evapotranspiración. Estos casos se diseñaron para responder primero una pregunta acotada: ¿cada módulo reproduce las ecuaciones previstas y la contabilidad del almacenamiento en condiciones controladas? Esa respuesta se separa luego de las preguntas posteriores sobre parámetros de campo, calibración y desempeño en la cuenca.

## Configuración común {#shared-setup}

La mayoría de los casos hidrológicos usan la cuenca sintética en V como contexto espacial común. Ese dominio proporciona un marco coherente de DEM, suelo, cobertura del suelo, IAF y agua subterránea, pero la referencia sigue proviniendo de una solución analítica o de una implementación de referencia independiente.

## Intercepción del dosel {#canopy-interception}

### Qué se probó {#what-was-tested}

El caso `VAL-CANOPY-001` aísla la rutina de almacenamiento del dosel antes de activar la infiltración, la escorrentía y el agua subterránea. La ladera izquierda usa `LAI = 0.5`, la franja del canal usa `LAI = 0` y la ladera derecha usa `LAI = 2.0`. Para la conversión de volumen se usa una celda representativa de `20 m × 20 m`.

### Referencia y método {#reference-and-method}

La rutina `interceptionModel.m` de HydroPol2D se ejecutó directamente y se comparó con una referencia independiente de depósito del dosel. El caso abarca el llenado del dosel, el throughfall una vez superada la capacidad de almacenamiento, el descenso del almacenamiento por evaporación y un bypass con `LAI = 0`.

### Resultado principal {#main-result}

HydroPol2D coincidió con la referencia independiente hasta la precisión de redondeo. Se aprobaron todas las verificaciones de benchmark, de balance de masa y de `NaN`.

| Métrica | Valor | Umbral |
|---|---:|---:|
| RMSE del almacenamiento del dosel (mm) | `1.50 × 10^-17` | `1.0 × 10^-9` |
| RMSE del throughfall (mm) | `1.31 × 10^-17` | `1.0 × 10^-9` |
| RMSE de la evaporación (mm) | `7.31 × 10^-18` | `1.0 × 10^-9` |
| Residuo de masa máximo (m³) | `2.22 × 10^-17` | `1.0 × 10^-6` |

Este caso valida las fórmulas del dosel implementadas y la contabilidad del almacenamiento en las condiciones probadas. No valida el comportamiento de la intercepción del dosel en campo, porque el caso no usa datos observados de throughfall ni de flujo de tallo.

## Módulo de nieve {#snow-module}

### Qué se probó {#what-was-tested-1}

El caso `VAL-SNOW-001` prueba la vía configurable actual de nieve. La suite incluye precipitación fría, mixta y cálida; dos clases LULC con parámetros de nieve distintos; estados iniciales nulos, solo con SWE, solo con profundidad y con el par SWE-profundidad; refinamiento del paso de tiempo; equivalencia entre la hoja de cálculo y el bypass; y una simulación acoplada de nieve y escorrentía en la cuenca en V.

### Referencia y método {#reference-and-method-1}

Las pruebas controladas usan cálculos prescritos de balance de masa para la partición lluvia-nieve, la fusión por grados-día, la conversión entre densidad y profundidad, y el almacenamiento. El caso completo en la cuenca en V usa el preprocesamiento normal de HydroPol2D y enrutamiento inercial local. Aplica 16,123.82 m³ de precipitación y verifica el balance completo del evento, que los estados de nieve sean finitos y el residuo del módulo de nieve.

### Resultado principal {#main-result-1}

Las seis verificaciones se aprobaron. La prueba del paso de tiempo dio una dispersión máxima de `1.36 × 10^-12 mm` entre las integraciones de 5, 15 y 60 minutos. El evento acoplado en la cuenca en V cerró en `5.82 × 10^-11 m³`, o `3.61 × 10^-13 %` de la precipitación del evento. El propio módulo de nieve cerró en `3.55 × 10^-16 m³`.

| Verificación | Resultado | Criterio de aceptación |
|---|---:|---:|
| Partición y almacenamiento configurables | error de 0,0 | cálculo prescrito exacto |
| Asignación de estados iniciales y de dos clases | error de 0,0 | conversión exacta y verificación del error esperado |
| Refinamiento de 5, 15 y 60 min | `1.36 × 10^-12 mm` | `< 1 × 10^-6 mm` |
| Acoplamiento nieve-escorrentía en la cuenca en V | `6.39 × 10^-15 m³` | `< 1 × 10^-6 m³` |
| Equivalencia entre la hoja de cálculo y el bypass | error de 0,0 | equivalencia exacta de los mapas de parámetros |
| Cierre del evento completo en la cuenca en V | `3.61 × 10^-13 %` | `< 0.1 %` |

<img src={useBaseUrl('/validation/results/hydrologic/snow-validation-dynamics.png')} alt="Diagnósticos de partición de la nieve, equivalente de agua de nieve, fusión, densidad y refinamiento del paso de tiempo" />

<img src={useBaseUrl('/validation/results/hydrologic/snow-full-vtilted.png')} alt="Series temporales de la profundidad de nieve y de la profundidad del agua superficial en la simulación acoplada en la cuenca en V" />

La vía probada lee los parámetros de nieve de la fila correspondiente de la tabla de parámetros LULC. `Initial_SWE_path` e `Initial_Snow_Depth_path` son opcionales. La [teoría del modelo hidrológico](../theory/hydrologic-model#5-snow-accumulation-melt-and-sublimation) define las reglas de inicialización y el fallback de códigos de clase. Estos casos validan las ecuaciones, la asignación de la configuración y la contabilidad acoplada. No calibran un manto de nieve con observaciones de campo.

## Infiltración {#infiltration}

### Qué se probó {#what-was-tested-2}

La suite de infiltración usa la cuenca en V con propiedades hidráulicas físicamente interpretables, al estilo del USDA, para suelos franco arenosos, francos y franco arcillosos. Se probaron siete regímenes:

- bypass sin infiltración;
- lluvia limitada por el suministro;
- entrada limitada por la capacidad;
- exceso por saturación con almacenamiento finito;
- percolación retardada en capas y recarga;
- exceso por saturación con agua subterránea somera;
- contraste espacial de suelos.

### Referencia y método {#reference-and-method-2}

La referencia es un programa independiente en MATLAB que evalúa la contabilidad prevista de la infiltración y del almacenamiento en capas fuera del solucionador hidrodinámico completo. Las pruebas siguen el orden implementado de arriba hacia abajo: capa cercana a la superficie, capa de la zona de raíces, capa de transmisión y recarga del agua subterránea cuando el almacenamiento vadoso está lleno y la recarga está activa.

### Resultado principal {#main-result-2}

Los siete casos independientes de infiltración se aprobaron después de restablecer las propiedades del suelo a valores físicamente coherentes basados en la textura.

| Caso | Régimen | Lluvia (mm) | Infiltración (mm) | Escorrentía (mm) | Recarga (mm) | Cierre (mm) |
|---|---|---:|---:|---:|---:|---:|
| `VAL-INFIL-VT-000` | Sin infiltración | 60,0 | 0,0 | 60,0 | 0,0 | 0,0 |
| `VAL-INFIL-VT-001` | Limitado por el suministro | 10,0 | 10,0 | 0,0 | 0,0 | 0,0 |
| `VAL-INFIL-VT-002` | Limitado por la capacidad | 120,0 | 34,157 | 85,843 | 0,0 | `1.71 × 10^-13` |
| `VAL-INFIL-VT-003` | Limitado por el almacenamiento | 180,0 | 72,5 | 107,5 | 0,0 | 0,0 |
| `VAL-INFIL-VT-004` | Percolación en capas | 384,0 | 384,0 | 0,0 | 197,614 | `1.23 × 10^-11` |
| `VAL-INFIL-VT-005` | Agua subterránea somera | 150,0 | 75,0 | 75,0 | 22,683 | `-2.84 × 10^-14` |
| `VAL-INFIL-VT-006` | Contraste espacial de suelos | 120,0 | 77,880 | 42,120 | 0,0 | `7.11 × 10^-15` |

La interpretación principal es a nivel de proceso, no solo numérica. El caso limitado por el suministro infiltró toda la lluvia aplicada. El caso limitado por la capacidad generó exceso cuando la lluvia superó la capacidad hidráulica de entrada. El caso limitado por el almacenamiento llenó el almacenamiento vadoso y luego produjo escorrentía por exceso de saturación. El caso de percolación en capas retardó la recarga en lugar de enviar el agua directamente al agua subterránea.

<img src={useBaseUrl('/validation/results/hydrologic/VTilted_Infiltration_Hydrograph_Overview.png')} alt="Resumen de los hidrogramas de infiltración en la cuenca en V" />

<p><em>Diagnósticos de infiltración en forma de hidrograma. Las líneas negras son la lluvia, las líneas azules son la escorrentía o el exceso superficial, y las líneas verdes son la recarga.</em></p>

<img src={useBaseUrl('/validation/results/hydrologic/VTilted_Infiltration_Rate_Overview.png')} alt="Resumen de las tasas de infiltración en la cuenca en V" />

<p><em>Tasas de infiltración aceptadas para los mismos casos. Las figuras se presentan en mm/h para mostrar cómo responde cada régimen a lo largo del tiempo.</em></p>

Esto valida la contabilidad de la infiltración implementada y la dinámica del suelo en capas para los regímenes de validación probados. No valida parámetros de infiltración de campo, el flujo por macroporos, el flujo preferencial ni un hidrograma calibrado de la cuenca.

## Evapotranspiración {#evapotranspiration}

### Qué se probó {#what-was-tested-3}

La suite de evapotranspiración usa la malla de la cuenca en V para probar tanto el cálculo de la ET potencial como la extracción de la ET real. Se probaron siete regímenes:

- reproducción de la fórmula de la ET potencial;
- limitación por el almacenamiento de aguas abiertas;
- extracción del suelo limitada por la demanda;
- extracción del suelo limitada por el almacenamiento;
- acceso parcial de las raíces cerca de la superficie;
- modo interno de ETP;
- enmascaramiento de celdas secas, impermeables e inválidas.

### Referencia y método {#reference-and-method-3}

El primer caso compara el cálculo de la ET de referencia de HydroPol2D con una implementación independiente de Penman-Monteith al estilo de la FAO. Los casos de extracción comparan la ET real del suelo, la evaporación de aguas abiertas, el almacenamiento final, el comportamiento del enmascaramiento y los residuos de masa con una referencia algebraica independiente.

### Resultado principal {#main-result-3}

Los siete casos se aprobaron. El caso de ET de referencia produjo valores medios idénticos de ET potencial en HydroPol2D y en la referencia independiente, `5.7669 mm/day`. En los casos de extracción, HydroPol2D coincidió en la ET del suelo, la evaporación de aguas abiertas y el almacenamiento final hasta la precisión de máquina.

| Caso | Régimen | ETP media (mm/day) | ET del suelo (suma en mm) | E superficial (suma en mm) | Residuo (m³) |
|---|---|---:|---:|---:|---:|
| `VAL-ET-VT-000` | Fórmula de la ET potencial | 5,7669 | -- | -- | 0,0 |
| `VAL-ET-VT-001` | Límite de aguas abiertas | -- | 0,0 | 27,0 | `-4.44 × 10^-14` |
| `VAL-ET-VT-002` | Limitado por la demanda del suelo | -- | 36,0 | 0,0 | `9.24 × 10^-14` |
| `VAL-ET-VT-003` | Limitado por el almacenamiento del suelo | -- | 27,0 | 0,0 | `-4.44 × 10^-14` |
| `VAL-ET-VT-004` | Acceso parcial de las raíces | -- | 45,0 | 0,0 | 0,0 |
| `VAL-ET-VT-005` | Modo interno de ETP | -- | 18,0 | 12,0 | `3.55 × 10^-15` |
| `VAL-ET-VT-006` | Máscaras y celdas secas | -- | 12,0 | 0,0 | `4.44 × 10^-15` |

<img src={useBaseUrl('/validation/results/hydrologic/VTilted_ET_Overview.png')} alt="Resumen de la validación de la evapotranspiración en la cuenca en V" />

<p><em>ET potencial, ET real del suelo, evaporación de aguas abiertas, almacenamiento antes y después de la ET, y errores absolutos de validación para los casos de ET en la cuenca en V.</em></p>

Estas pruebas validan la vía de cálculo de la fórmula de ET implementada y la contabilidad de la extracción de la ET real en regímenes controlados. No validan la ET a escala de campo, los coeficientes de cultivo ni la calibración estacional del balance de agua.
