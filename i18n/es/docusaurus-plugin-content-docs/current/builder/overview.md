---
title: Resumen
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# HydroPol2D Case Builder

HydroPol2D Case Builder prepara un caso de modelo completo, listo para ejecutar, a partir de datos
globales públicos. Usted elige una ciudad o una cuenca. El Builder delimita el área del modelo,
descarga y alinea los mapas, prepara la lluvia y el clima y verifica el caso antes de que usted lo
ejecute. Genera casos para HydroPol2D-MATLAB y para HydroPol2D-Python, el motor del modelo dentro
de HydroPol2D Studio.

Esta sección describe Case Builder 0.1.0, la primera versión con licencia (una versión de prueba),
para Mac con Apple silicon y para Windows (64 bits). La interfaz del Case Builder está en inglés, por lo
que los nombres de pestañas, botones, campos y mensajes aparecen aquí en inglés, tal como se ven en
pantalla.

:::info[Licencia]
Case Builder es un producto propietario. Para obtener una licencia, escriba a Marcus N. Gomes Jr.
en [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).
[Instalación y licencia](install-and-license) explica los pasos.
:::

<p align="center">
  <img src={useBaseUrl('/img/builder/case-builder-workflow.es.svg')} width="760" alt="El Case Builder desde el primer uso hasta un caso listo para ejecutar: el código de licencia, los datos públicos que descarga, los cuatro pasos Elija el área, Vista previa, Prepare y Verifique, la carpeta del caso y dónde se ejecuta el caso" />
</p>

<p align="center">
  <em>Figura 1. El recorrido por el Case Builder. Los datos públicos alimentan la vista previa y el caso completo. La carpeta del caso se ejecuta en HydroPol2D MATLAB o en HydroPol2D Studio.</em>
</p>

## Qué prepara

| Paso | Qué hace el Builder |
|---|---|
| Área del modelo | Tres formas de elegirla. **Urban Basin**: una ciudad y todas las cuencas que drenan hacia ella. **Catchment**: una salida y la cuenca aguas arriba de ella. **Urban Area Only**: el área urbanizada y una franja a su alrededor. |
| Vista previa del costo | Antes de cualquier descarga grande, muestra el área, el número de celdas de la malla, los datos que se van a descargar y el tamaño de los resultados guardados. |
| Terreno y ríos | Terreno a la resolución del modelo, acondicionado para el flujo con HydroBathyDEM, con anchos y profundidades de los ríos. |
| Mapas | Cobertura del suelo, textura del suelo, profundidad hasta la roca, agua subterránea y humedad del suelo iniciales e índice de área foliar. |
| Lluvia y clima | Un producto de lluvia por caso (IMERG, ERA5, MSWEP o AORC) y el clima de ERA5. |
| Contornos | Salidas con flujo crítico por defecto. Caudales de entrada de ríos (GloFAS) y niveles costeros (GTSM) donde corresponden. |
| Verificación | Una verificación previa de los archivos, las mallas, las fechas, las unidades y las entradas obligatorias. |
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
| Lluvia | IMERG, ERA5, MSWEP o AORC (Estados Unidos), elegido por caso |

No se necesita una cuenta de Google Earth Engine. Algunas fuentes necesitan una cuenta gratuita
propia: [Fuentes de datos y cuentas](data-accounts) las lista.

## Cómo se relaciona con Studio y MATLAB

- **En HydroPol2D Studio**, el asistente **New model** usa los pasos de preparación del Builder
  para crear un modelo a partir de un lugar en el mapa. Vea [Construir un modelo](../studio/building-a-model).
  Si tiene Studio, no necesita también el Builder.
- **El Builder independiente** agrega el conjunto completo de opciones: los tres tipos de área del
  modelo, la vista previa del costo, el informe de la verificación previa y las simulaciones en
  MATLAB.
- **Con HydroPol2D-MATLAB**, el Builder genera un caso MATLAB con un script `run_case.m` que lo
  ejecuta. Vea el [flujo de trabajo de construcción del modelo](../getting-started/model-building-workflow)
  para saber cómo trabajan juntos el Builder, los modelos y la calibración.

## Cómo se usa

- una app local que se abre en su navegador web, con las páginas **Prepare a case**, **Check a case**
  y **Python and command line**,
- una línea de comandos, para construcciones automatizadas y repetidas.

## En esta sección

1. [Instalación y licencia](install-and-license): descargar, instalar e introducir el código de licencia.
2. [Elegir el área del modelo](model-area): Urban Basin, Urban Area Only y Catchment.
3. [Ajustes del caso](settings): malla, fechas, lluvia, procesos, ríos, salidas y carpetas.
4. [Vista previa y costo](preview-and-cost): el mapa del dominio y el tamaño del caso antes de cualquier descarga.
5. [Preparar un caso](prepare-a-case): la construcción completa y lo que hay en la carpeta del caso.
6. [Fuentes de datos y cuentas](data-accounts): Copernicus, NASA Earthdata y MSWEP.
7. [Verificar un caso](check-a-case): la verificación previa.
8. [Ejecutar el caso](run-the-case): en HydroPol2D MATLAB o en HydroPol2D Studio.
9. [Línea de comandos](command-line): los mismos casos desde una terminal.
10. [Solución de problemas](troubleshooting): mensajes que puede ver y qué hacer.

## Límites actuales

- La versión 0.1.0 es una versión de prueba para Mac con Apple silicon y Windows (64 bits).
- La app no descarga HydroPol2D Python. Ejecute los casos de Python en HydroPol2D Studio.
- La lluvia de MSWEP requiere aprobación previa de GloH2O.
- La lluvia de AORC cubre solo los Estados Unidos contiguos. Los niveles costeros de GTSM terminan
  en 2024.
- El albedo es un valor único (0,25) en la versión actual.
- El drenaje pluvial, los embalses y la calibración de eventos no se agregan automáticamente.
