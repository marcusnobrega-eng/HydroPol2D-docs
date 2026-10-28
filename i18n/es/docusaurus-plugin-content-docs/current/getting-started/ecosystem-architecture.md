---
title: Arquitectura del ecosistema
---

# Arquitectura del ecosistema

HydroPol2D usa un único paquete de malla versionado en sus implementaciones de
MATLAB y Python. Esto evita que cada solucionador reconstruya la geometría o
interprete de forma distinta las propiedades de la malla.

## Responsabilidades de los repositorios {#repository-responsibilities}

| Componente | Responsabilidad | Versión candidata |
|---|---|---|
| HydroBathyDEM | Generador de producción de mallas regulares y de Voronoi, productos de terreno, superposición conservativa de rásteres, tablas de submalla, UGRID, capas de inspección en GeoPackage y control de calidad de la malla. | `0.3.0rc1` |
| HydroPol2D-Python | Motor del modelo en Python y Studio. Valida y utiliza el paquete de malla; no regenera la geometría hidráulica de la malla. | `0.8.0rc1` |
| HydroPol2D-MATLAB | Implementación de referencia en MATLAB que utiliza de forma compatible el mismo paquete de malla. | `1.18.0-rc1` |
| HydroPolMesh | Prototipo de migración archivado. Las capacidades útiles ya validadas se están conservando en HydroBathyDEM; no es una dependencia de ejecución en producción. | prototipo |

La versión estable `v1.17.0` de MATLAB sigue siendo la referencia numérica
mientras las versiones candidatas coordinadas completan las verificaciones de
paridad y de larga duración.

## Contrato de malla compartido {#shared-mesh-contract}

El contrato de malla `1.0` exige que el paquete declare:

- la geometría de celdas y caras, la conectividad, las áreas, las longitudes y la orientación;
- índices de archivo con base cero, convertidos explícitamente a índices de MATLAB con base uno;
- `cell_cfl_width_m`, definido a partir de la separación mínima entre centros en dirección normal a una cara;
- el CRS, las unidades, la resolución de origen, la procedencia y la versión del contrato;
- pesos conservativos de superposición entre el ráster y las celdas;
- tablas de submalla compatibles a nivel de celda y de cara cuando el enrutamiento con submalla está activado.

Ambos solucionadores rechazan índices mal formados, caras de longitud cero,
áreas negativas, unidades o CRS ausentes, anchos CFL no definidos, superposición
no conservativa y tablas de submalla incompatibles. No reconstruyen de forma
silenciosa las propiedades de la malla que faltan.

## Formulaciones de submalla {#subgrid-formulations}

Las siguientes opciones resuelven representaciones distintas y no son alias
entre sí:

| Opción | Representación prevista |
|---|---|
| Canal de Neal | Canal rectangular embebido en la malla ráster estructurada; se admite con enrutamiento inercial local. |
| Submalla estructurada con tablas de consulta | Tablas de consulta de celdas y caras dependientes de la profundidad, al estilo de SFINCS, en una malla estructurada. |
| Submalla de Voronoi | Relaciones de área, perímetro mojado y capacidad de conducción en una malla de Voronoi no estructurada. |

Los nombres heredados solo se aceptan mediante la migración del caso. Las
combinaciones incompatibles deben corregirse antes de que pueda iniciarse una
simulación.

## Estado de las versiones {#release-status}

Las versiones candidatas son compilaciones de integración, no versiones
coordinadas finales. La publicación final requiere la instalación desde un clon
limpio, comparaciones entre MATLAB y Python con mallas y entradas hidrológicas
idénticas, las simulaciones de Pune de 2 h, 6 h y 12 h, y la aprobación de las
verificaciones científicas, de Studio, de lint, de tipos y de procedencia.
