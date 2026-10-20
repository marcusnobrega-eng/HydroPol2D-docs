---
title: Validación de módulos hidrológicos
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Validación de módulos hidrológicos

Esta página describe las pruebas de la validación para intercepción de dosel, nieve, infiltración y evapotranspiración. La pregunta es directa: ¿cada módulo reproduce sus ecuaciones y su balance de almacenamiento bajo condiciones controladas? Esta evidencia se separa de la calibración y el desempeño de campo.

## Configuración común

Los casos usan la cuenca sintética en V de HydroPol2D cuando se necesita una malla espacial. Las soluciones analíticas, los cálculos independientes o los balances de masa prescritos son la referencia.

## Intercepción de dosel

`VAL-CANOPY-001` compara el almacenamiento del dosel, la evaporación y la precipitación que llega al suelo con un balance de depósito. Los errores de almacenamiento, evaporación y paso de lluvia fueron inferiores a `5.55 × 10^-17 mm`; el mayor residuo fue `2.22 × 10^-17 m³`.

## Módulo de nieve

### Qué se probó

`VAL-SNOW-001` prueba la ruta configurable de nieve. La secuencia incluye precipitación fría, mixta y cálida; dos clases LULC con parámetros distintos; estados iniciales sin ráster, con SWE, con profundidad y con ambos mapas; refinamiento de paso de tiempo; equivalencia entre hoja de cálculo y bypass; y una simulación acoplada de nieve y escorrentía en la cuenca en V.

### Método y resultados

Las pruebas controladas usan balances prescritos para la partición lluvia-nieve, la fusión por grados-día, la conversión entre densidad y profundidad, y el almacenamiento. El evento completo usa el preprocesamiento normal de HydroPol2D y enrutamiento inercial local. Aplica `16,123.82 m³` de precipitación y verifica el balance de todo el evento, los estados de nieve y el residuo interno del módulo.

Las seis pruebas pasaron. El refinamiento entre 5, 15 y 60 minutos tuvo una diferencia máxima de `1.36 × 10^-12 mm`. El evento completo cerró en `5.82 × 10^-11 m³`, o `3.61 × 10^-13 %` de la precipitación; el residuo del módulo de nieve fue `3.55 × 10^-16 m³`.

| Verificación | Resultado | Criterio |
|---|---:|---:|
| Partición y almacenamiento | 0.0 mm | exacto |
| Estados iniciales y dos clases | 0.0 error | conversión exacta y error esperado |
| Refinamiento de 5, 15 y 60 min | `1.36 × 10^-12 mm` | `< 1 × 10^-6 mm` |
| Acoplamiento nieve-escorrentía en la cuenca en V | `6.39 × 10^-15 m³` | `< 1 × 10^-6 m³` |
| Equivalencia hoja-bypass | 0.0 error | mapas de parámetros idénticos |
| Cierre del evento completo | `3.61 × 10^-13 %` | `< 0.1 %` |

<img src={useBaseUrl('/validation/results/hydrologic/snow-validation-dynamics.png')} alt="Diagnósticos de partición, almacenamiento y refinamiento temporal de nieve" />

<img src={useBaseUrl('/validation/results/hydrologic/snow-full-vtilted.png')} alt="Serie temporal de nieve y agua superficial en la cuenca en V" />

Los parámetros de nieve se leen de la fila correspondiente de la tabla de parámetros LULC. `Initial_SWE_path` e `Initial_Snow_Depth_path` son opcionales. La página del [modelo hidrológico](../theory/hydrologic-model#5-acumulación-fusión-y-sublimación-de-nieve) describe la inicialización y el fallback de códigos de clase. Estos casos verifican ecuaciones, mapeo de entradas y balance acoplado; no calibran la nieve con observaciones de campo.

## Infiltración

Los casos de infiltración verifican los regímenes sin infiltración, limitados por el suministro, limitados por la capacidad, exceso por saturación, percolación en capas, nivel freático somero y contraste espacial de suelos. El almacenamiento en capas permanece no negativo y conservativo.

## Evapotranspiración

Los casos de ET comparan la ET de referencia con cálculos independientes y verifican los límites de extracción de agua del suelo y de la superficie.

## Interpretación

Los resultados son evidencia de validación para fórmulas, almacenamiento y dinámica controlada. No son una validación observacional de cuencas.
