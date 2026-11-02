---
title: Resumen matemático
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Resumen matemático

La sección de teoría es la referencia principal para las ecuaciones y la estructura de los módulos de HydroPol2D. Su objetivo es describir las formulaciones implementadas sin mezclar detalles de configuración ni narrativa de estudios de caso.

HydroPol2D acopla:

- intercepción, evapotranspiración, infiltración, nieve y almacenamiento vadoso;
- recarga subterránea en capas, ascenso capilar y flujo lateral de Boussinesq;
- múltiples familias de enrutamiento superficial;
- transporte de calidad del agua;
- diagnósticos opcionales de inestabilidad humana.

## Capacidades y madurez

| Capacidad | Ruta teórica principal | Estado actual |
|---|---|---|
| Núcleo hidrológico: intercepción, ET, infiltración, almacenamiento vadoso en capas | [Hydrologic Model](./hydrologic-model) | Predeterminado + validado |
| Acumulación, fusión y sublimación de nieve | [Hydrologic Model](./hydrologic-model#5-snow-accumulation-melt-and-sublimation) | Opcional (apagado hasta que se active) + validado |
| Recarga subterránea, programador asíncrono, ascenso capilar y flujo lateral de Boussinesq | [Groundwater Model](./groundwater-model) | Predeterminado + validado |
| Subsuelo en capas de suelo sobre regolito | [Subsuelo en Capas](./layered-subsurface) | Opcional + paridad de núcleos y pruebas controladas en la cuenca en V |
| Estrés de Feddes en la absorción de agua por las raíces | [Modelo hidrológico](./hydrologic-model#35-feddes-root-water-uptake-stress) | Opcional + pruebas de consistencia |
| Acuífero profundo: embalses lineales por subcuenca y su estado inicial | [Modelo de aguas subterráneas](./groundwater-model#13-deep-aquifer) | Opcional + pruebas del estado inicial con fixtures |
| Enrutamiento local inertial | [Hydrodynamic Model](./hydrodynamic-model) | Predeterminado + validado |
| Enrutamiento full momentum | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado en benchmarks controlados |
| Enrutamientos diffusive y kinematic D4 | [Hydrodynamic Model](./hydrodynamic-model) | Opcionales + validados en benchmarks controlados |
| Cellular automata | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado para conservación y bookkeeping |
| Inestabilidad humana, modos `1` y `3` | [Human Instability](./human-instability) | Opcional + validada en benchmarks controlados |
| Intercambio río-acuífero | [Modelo de aguas subterráneas](./groundwater-model) | Implementado en Python y MATLAB + pruebas controladas de agua subterránea |

## Mapa de la teoría

### 1. Procesos hidrológicos

Las páginas hidrológicas documentan cómo HydroPol2D reparte la entrada atmosférica en almacenamiento en el dosel, throughfall, infiltración, evapotranspiración, acumulación y derretimiento de nieve, almacenamiento vadoso, recarga y retroalimentación del groundwater.

<p align="center">
  <img src={useBaseUrl('/img/theory/cell-water-budget.es.svg')} width="720" alt="Una celda del modelo vista de lado: la lluvia cae sobre el dosel de un árbol y la nieve sobre un manto de nieve; el throughfall, la fusión, la exfiltración y el exceso de saturación alimentan el agua superficial, que se infiltra en la zona vadosa y fluye hacia una celda vecina más baja; la recarga y el ascenso capilar conectan la zona vadosa con el agua subterránea, que fluye lateralmente; flechas grises devuelven vapor a la atmósfera" />
</p>

<p align="center">
  <em>Figura 1. Los almacenamientos y flujos de una celda del modelo (sin escala). Las flechas azules llevan agua líquida y las grises, vapor; solo la lluvia pasa por el dosel, y la fusión va directa al agua superficial.</em>
</p>

### 2. Acoplamiento del groundwater

La teoría del groundwater documenta la ruta actual de recarga en capas, el ascenso capilar opcional, el programador asíncrono, la exfiltración y el flujo lateral bidimensional de Boussinesq cuando el baseflow está activo. El [subsuelo en capas](./layered-subsurface) opcional reemplaza el acuífero limitado al suelo por una columna de suelo sobre regolito, y el acuífero profundo opcional añade embalses lineales lentos por subcuenca.

### 3. Enrutamiento superficial

HydroPol2D documenta hoy cinco familias principales de enrutamiento:

- local inertial;
- full momentum;
- diffusive D4;
- kinematic D4;
- cellular automata.

Solo una formulación principal debe estar activa por simulación. D8 permanece como una ruta secundaria.

### 4. Inestabilidad humana

La inestabilidad humana es un diagnóstico de riesgo acoplado, impulsado por las profundidades y velocidades producidas por HydroPol2D. La teoría pública actual incluye el modo `1`, basado en equilibrio de fuerzas, y el modo `3`, basado en clasificación geométrica.

### 5. Calidad del agua

La teoría de calidad del agua documenta el buildup, el washoff, el transporte y la exportación de constituyentes dentro de la misma estructura de enrutamiento distribuido usada para el movimiento del agua.

## Acoplamiento numérico

A nivel general, HydroPol2D avanza el sistema acoplado:

1. aplicando la lluvia y los forzantes meteorológicos;
2. actualizando intercepción, nieve, evapotranspiración, infiltración y almacenamiento vadoso;
3. acumulando recarga e intercambio capilar para el groundwater;
4. cambiando las cargas del nivel freático en cada paso del agua superficial según el intercambio neto y devolviendo la exfiltración y el exceso de saturación a la superficie; el programador del agua subterránea es siempre asíncrono, y solo el flujo lateral del agua subterránea, cuando está activo, lo espera;
5. aplicando los hidrogramas de entrada y actualizando la familia de enrutamiento activa;
6. actualizando la calidad del agua y los diagnósticos opcionales.

Esa estructura secuencial es la que conecta las páginas individuales de teoría en un solo modelo.
