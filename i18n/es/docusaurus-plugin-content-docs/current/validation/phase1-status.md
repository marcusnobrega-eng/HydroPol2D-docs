---
title: Estado de la Fase 1
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Estado de validacion de la Fase 1

La tabla siguiente resume el estado actual de validación de los módulos de HydroPol2D. Las métricas detalladas, las figuras y las descripciones de los casos están disponibles en el <a href={useBaseUrl('/reports/validation_report.pdf')}>informe de validación de la Fase 1</a>, en la página [Resumen de validación](./overview) y en la [Validación del modelo submalla de Neal (2012)](./neal-subgrid).

| Modulo | Estado actual | Evidencia usada |
|---|---|---|
| Intercepcion del dosel | Listo para informe | Referencia independiente de almacenamiento tipo bucket y balance de masa exacto. |
| Modulo de nieve | Listo para informe | Particion lluvia-nieve, derretimiento, sublimacion y bookkeeping de SWE. |
| Infiltracion | Listo para informe en casos controlados | Pruebas analiticas y controladas con suelos en capas. |
| Evapotranspiracion | Listo para informe | Calculos independientes de ET y verificacion de limites de extraccion. |
| Groundwater y recarga | Listo para informe | Verificaciones analiticas de ascenso del nivel, equivalencia del scheduler, bookkeeping de ascenso capilar y benchmarks analiticos de ladera. |
| Hidrodinamica full momentum | Listo para informe | Benchmarks de tilted plane, V-tilted, Ritter dam-break, non-breaking wave y contornos. |
| Hidrodinamica local inertial | Listo para informe con salvedades del metodo | Pruebas de tilted plane, V-tilted, contornos de stage y conservacion. |
| Cellular automata | Listo para informe en conservacion y bookkeeping | Pruebas V-tilted, plane y contornos. |
| Enrutamientos kinematic y diffusive | Listos para informe en benchmarks controlados corregidos | Pruebas de tilted plane, conservacion en V-tilted y bookkeeping en contornos de stage. |
| Modelo submalla de Neal (2012) | Listo para informe en casos controlados de canal y desbordamiento | Referencias numéricas de malla fina para flujo dentro de las márgenes, canal compuesto permanente y transitorio, activación de las márgenes y extensión máxima de inundación. La recesión tardía permanece limitada. |
| Embalses y estructuras de control | Listo para informe | ODE analitica de agotamiento por curva de gasto y balance volumetrico exacto. |
| Contorno con hidrograma de entrada | Listo para informe | Volumen prescrito del hidrograma y bookkeeping de almacenamiento y salida. |
| Contorno con stage hydrograph | Listo para informe | Aplicacion prescrita del nivel y respuesta volumetrica. |
| Lluvia espacial en raster | Listo para informe | Pequena pila raster con lluvia exacta por celda y objetivos de volumen en el dominio. |
| Calidad del agua | Listo para informe | Washoff analitico en masa con escala conceptual inspirada en SWMM. |
| Riesgo humano e inestabilidad | Listo para informe | Referencias independientes de umbrales y clasificacion por equilibrio de fuerzas. |

## Salvedades importantes

Listo para informe significa que el modulo paso pruebas controladas de ecuaciones y dinamica de la Fase 1. No significa, por si solo, que el modulo este calibrado para un sitio de campo especifico.

Los casos con referencia numerica ayudan a ganar confianza en el comportamiento de la implementacion, pero son evidencias mas debiles que las verdades analiticas o independientes.
