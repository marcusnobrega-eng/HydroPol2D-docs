---
title: Resumen matematico
---

# Resumen matematico

La seccion de teoria es la referencia principal para las ecuaciones y la estructura de los modulos de HydroPol2D. Su objetivo es describir las formulaciones implementadas sin mezclar detalles de configuracion ni narrativa de estudios de caso.

HydroPol2D acopla:

- intercepcion, evapotranspiracion, infiltracion, nieve y almacenamiento vadoso;
- recarga subterranea en capas, ascenso capilar y flujo lateral de Boussinesq;
- multiples familias de enrutamiento superficial;
- transporte de calidad del agua;
- diagnosticos opcionales de inestabilidad humana.

## Capacidades y madurez

| Capacidad | Ruta teorica principal | Estado actual |
|---|---|---|
| Nucleo hidrologico: intercepcion, ET, infiltracion, nieve, almacenamiento vadoso en capas | [Hydrologic Model](./hydrologic-model) | Predeterminado + validado |
| Recarga subterranea, programador asincrono, ascenso capilar y flujo lateral de Boussinesq | [Groundwater Model](./groundwater-model) | Predeterminado + validado |
| Subsuelo en capas de suelo sobre regolito | [Subsuelo en Capas](./layered-subsurface) | Opcional + paridad de núcleos y pruebas controladas en la cuenca en V |
| Estrés de Feddes en la absorción de agua por las raíces | [Modelo hidrológico](./hydrologic-model#35-feddes-root-water-uptake-stress) | Opcional + pruebas de consistencia |
| Acuífero profundo: embalses lineales por subcuenca y su estado inicial | [Modelo de aguas subterráneas](./groundwater-model#13-deep-aquifer) | Opcional + pruebas del estado inicial con fixtures |
| Enrutamiento local inertial | [Hydrodynamic Model](./hydrodynamic-model) | Predeterminado + validado |
| Enrutamiento full momentum | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado en benchmarks controlados |
| Enrutamientos diffusive y kinematic D4 | [Hydrodynamic Model](./hydrodynamic-model) | Opcionales + validados en benchmarks controlados |
| Cellular automata | [Hydrodynamic Model](./hydrodynamic-model) | Opcional + validado para conservacion y bookkeeping |
| Inestabilidad humana, modos `1` y `3` | [Human Instability](./human-instability) | Opcional + validada en benchmarks controlados |
| Interfaz rio-acuifero | [Groundwater Model](./groundwater-model) | Interfaz presente, todavia sin una afirmacion teorica madura independiente |

## Mapa de la teoria

### 1. Procesos hidrologicos

Las paginas hidrologicas documentan como HydroPol2D reparte la entrada atmosferica en almacenamiento en el dosel, throughfall, infiltracion, evapotranspiracion, acumulacion y derretimiento de nieve, almacenamiento vadoso, recarga y retroalimentacion del groundwater.

### 2. Acoplamiento del groundwater

La teoria del groundwater documenta la ruta actual de recarga en capas, el ascenso capilar opcional, el programador asincrono, la exfiltracion y el flujo lateral bidimensional de Boussinesq cuando el baseflow esta activo. El [subsuelo en capas](./layered-subsurface) opcional reemplaza el acuífero limitado al suelo por una columna de suelo sobre regolito, y el acuífero profundo opcional añade embalses lineales lentos por subcuenca.

### 3. Enrutamiento superficial

HydroPol2D documenta hoy cinco familias principales de enrutamiento:

- local inertial;
- full momentum;
- diffusive D4;
- kinematic D4;
- cellular automata.

Solo una formulacion principal debe estar activa por simulacion. D8 permanece como una ruta secundaria.

### 4. Inestabilidad humana

La inestabilidad humana es un diagnostico de riesgo acoplado, impulsado por las profundidades y velocidades producidas por HydroPol2D. La teoria publica actual incluye el modo `1`, basado en equilibrio de fuerzas, y el modo `3`, basado en clasificacion geometrica.

### 5. Calidad del agua

La teoria de calidad del agua documenta el buildup, el washoff, el transporte y la exportacion de constituyentes dentro de la misma estructura de enrutamiento distribuido usada para el movimiento del agua.

## Acoplamiento numerico

A nivel general, HydroPol2D avanza el sistema acoplado:

1. aplicando lluvia, inflow y forzantes meteorologicos;
2. actualizando intercepcion, nieve, evapotranspiracion, infiltracion y almacenamiento vadoso;
3. acumulando recarga e intercambio capilar para el groundwater;
4. actualizando la familia de enrutamiento activa;
5. actualizando las cargas subterraneas cuando actua el programador asincrono;
6. devolviendo exfiltracion, exceso de saturacion y diagnosticos opcionales al estado acoplado.

Esa estructura secuencial es la que conecta las paginas individuales de teoria en un solo modelo.
