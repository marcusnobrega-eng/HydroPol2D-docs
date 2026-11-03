---
title: Visión general
---

# HydroPol2D Case Builder

HydroPol2D Case Builder prepara un caso de modelación completo, listo para ejecutar, a partir de
datos globales públicos. Usted elige una ciudad o una cuenca. El Builder delimita el área del
modelo, descarga y alinea los mapas, prepara la lluvia y el clima y verifica el caso antes de la
simulación. Genera casos para HydroPol2D-MATLAB y para HydroPol2D-Python, el motor del modelo
dentro de HydroPol2D Studio.

:::info[Licencia]
Case Builder es un producto propietario. Para obtener una licencia, escriba a Marcus N. Gomes Jr.
en [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com). Esta página es una
visión general. La guía completa llegará con la primera versión con licencia.
:::

## Qué prepara

| Paso | Qué hace el Builder |
|---|---|
| Área del modelo | Tres formas de elegirla. **Urban Basin**: una ciudad y todas las cuencas que drenan hacia ella. **Catchment**: una salida y la cuenca aguas arriba. **Urban Area Only**: el área urbanizada y una franja a su alrededor. |
| Estimación de costo | Antes de cualquier descarga grande, muestra el área, el número de celdas y la memoria que necesita el caso. |
| Terreno y ríos | Terreno a la resolución del modelo, acondicionado para el flujo con HydroBathyDEM, con anchos y profundidades de los ríos. |
| Mapas | Cobertura del suelo, textura del suelo, profundidad hasta la roca, agua subterránea y humedad del suelo iniciales e índice de área foliar. |
| Lluvia y clima | Un producto de lluvia por caso (IMERG, ERA5 o MSWEP) y el clima de ERA5. |
| Contornos | Salidas con flujo crítico por defecto. Caudales de ríos (GloFAS) y niveles costeros (GTSM) donde corresponden. |
| Verificación | Una verificación previa de los archivos, mallas, fechas, unidades y entradas obligatorias. |
| Simulación | Genera el caso para MATLAB, Python o ambos, y puede iniciar la simulación y mostrar su avance. |

Un caso que pasa la verificación previa está completo y es coherente. Eso, por sí solo, no muestra
que el modelo sea preciso en un lugar nuevo. La calibración y la comparación con observaciones
siguen siendo necesarias.

## Fuentes de datos

| Variable | Fuente |
|---|---|
| Límite de la ciudad | GHSL Urban Centre Database R2024A |
| Cuencas y ríos | HydroBASINS v1c (nivel 12) y HydroRIVERS v1.0 |
| Terreno | FABDEM v1.2, o su propio DEM |
| Geometría de los ríos | HydroBathyDEM |
| Cobertura del suelo | ESA WorldCover |
| Textura del suelo | Clases de textura USDA de OpenLandMap |
| Profundidad hasta la roca | Shangguan et al. (2017) |
| Agua subterránea inicial | Profundidad global del nivel freático de Fan et al. |
| Humedad inicial del suelo | ERA5-Land |
| Clima | ERA5 |
| Índice de área foliar | MODIS MCD15A3H |
| Lluvia | IMERG, ERA5 o MSWEP, elegido por caso |

No se necesita una cuenta de Google Earth Engine.

## Cómo se relaciona con Studio y MATLAB

- **En HydroPol2D Studio**, el asistente **New model** usa los pasos de preparación del Builder
  para crear un modelo a partir de un lugar en el mapa. Vea [Construir un modelo](../studio/building-a-model).
- **El Builder independiente** ofrece todas las opciones: los tres tipos de área, la estimación de
  costo, el informe de la verificación previa y simulaciones en MATLAB o Python.
- **Con HydroPol2D-MATLAB**, el Builder genera un caso MATLAB con un script `run_case.m` que lo
  ejecuta. Vea el [flujo de construcción del modelo](../getting-started/model-building-workflow)
  para entender cómo trabajan juntos el Builder, los modelos y la calibración.

## Cómo se usa

- una aplicación local que se abre en el navegador, con las páginas **Prepare a case** y **Check a case**,
- una línea de comandos, para construcciones automatizadas y repetidas,
- una interfaz de Python, para notebooks y servidores.

## Límites actuales

- Probado en macOS. Linux es el sistema previsto para simulaciones grandes. Windows aún no se ha probado.
- La lluvia de MSWEP requiere aprobación previa de GloH2O.
- El albedo es un valor único (0,25) en la versión actual.
- Las redes de drenaje, los embalses y la calibración de eventos no se agregan automáticamente.
