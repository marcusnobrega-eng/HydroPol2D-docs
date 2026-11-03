---
title: Ejecutar desde Excel
---

# Ejecutar HydroPol2D desde Excel

En el modo Excel, todo un caso de MATLAB está en un solo libro de Excel, `HydroPol2D_Inputs.xlsx`, que contiene todos los parámetros, las tablas de clases y las series temporales. El modo bypass lee los mismos parámetros desde archivos de MATLAB en `Config/`. Ambos modos usan el mismo solucionador numérico.

## Empezar con el ejemplo probado {#start-with-the-tested-example}

El repositorio incluye un caso pequeño en V. Su libro de Excel es `Examples/VTilted_Excel/Input_Data_Sheets/HydroPol2D_Inputs.xlsx`. Se abre MATLAB en el repositorio de HydroPol2D y se ejecuta lo siguiente.

```matlab
run('Examples/VTilted_Excel/run_excel.m')
```

El lanzador lee `flag_voronoi` (pestaña Surface flow) y escribe los resultados en `Examples/VTilted_Excel/Outputs/regular` o en `Examples/VTilted_Excel/Outputs/voronoi`. Para ejecutar la malla de Voronoi preparada, se cambia `flag_voronoi` de `0` a `1` en el mismo libro de Excel. No se debe crear un segundo libro.

## El libro del caso {#the-case-workbook}

| Pestañas | Contenido |
|---|---|
| Start here | Cómo completar el libro, la leyenda de colores y un enlace a cada pestaña |
| Run control, Input maps, Soil and groundwater, Surface flow, Rain and ET, Design storm, Water quality, Risk and gauges | Todos los parámetros, uno por fila, con una nota en cada valor. Un bloque se muestra en gris mientras su interruptor vale 0. |
| Soil classes, Land use classes, Human instability, Mesh, Control structures | Las tablas de clases |
| Rain series, Rain gauges, Climate stations, Inflow hydrographs, Stage hydrographs | Las series temporales |

Las pestañas de tablas de clases y de series conservan la disposición de celdas de los libros de Excel que reemplazan, porque el modelo lee algunas de ellas por posición. Sus filas y columnas deben quedar donde están. Una hoja admite hasta 1 048 576 filas, lo que equivale a dos años de datos cada 1 min.

Los parámetros se listan en [Parámetros del libro del caso](../configuration/general_data), los interruptores en [Banderas del modelo](../configuration/flags), las tablas de clases en [Tablas de parámetros](../inputs/parameter-tables) y las series en [Forzamientos opcionales](../inputs/optional-forcing).

## Completar un caso {#fill-a-case}

1. **Start here.** Se lee la leyenda de colores. Una fila gris está desactivada, un bloque gris es avanzado (se mantienen sus valores predeterminados) y un bloque ámbar está en pausa (se mantiene en 0).
2. **Pestañas de parámetros.** Los procesos se activan o desactivan con el interruptor al inicio de cada bloque. Un asterisco rojo marca un valor obligatorio. Un valor opcional vacío mantiene su valor predeterminado, y la nota de cada valor indica cuál es.
3. **Tablas de clases.** Se da una fila por cada código de clase de los mapas de uso del suelo y de suelo. Un código válido que falta en una tabla recibe la media ponderada por área de las clases asignadas, y la decisión se escribe en `Input_Class_Code_Audit.csv`.
4. **Series.** Solo se completan las series que leen los interruptores. Las demás pueden quedar como plantillas vacías con sus encabezados.
5. **Rutas.** Las rutas de rásteres y de archivos pueden ser absolutas o relativas a la carpeta del libro de Excel.

## Malla regular o malla de Voronoi {#regular-grid-or-voronoi-mesh}

`flag_voronoi` (pestaña Surface flow, bloque Unstructured mesh) selecciona la malla.

| `flag_voronoi` | Malla |
|---|---|
| `0` | Malla ráster construida a partir del DEM y de los mapas de uso del suelo y de suelo |
| `1` | Un archivo de caso preparado, indicado en la pestaña Mesh, que hace referencia a la malla UGRID y a los archivos de superposición con rásteres creados por HydroBathyDEM |

Los parámetros de la pestaña Mesh deben coincidir con los metadatos guardados en el archivo UGRID. Antes de la simulación, HydroPol2D verifica el ancho de fondo, el ancho mínimo, la razón entre tamaños adyacentes, el ancho urbano, la franja de transición y la política para ríos no resueltos, de modo que un libro de Excel no pueda ejecutar sin aviso una malla distinta. Excel selecciona una malla preparada, pero no la genera ni la modifica durante una simulación. El ejecutor de Voronoi de MATLAB funciona solo en CPU.

## Ejecutar cualquier libro sin editar el lanzador {#run-any-workbook-without-editing-the-launcher}

`run_HydroPol2D.m` lee `Input_Data_Sheets/HydroPol2D_Inputs.xlsx` por defecto. Para ejecutar otro caso, se definen las rutas en MATLAB y se ejecuta el lanzador normal.

```matlab
setenv('HYDROPOL_RUN_MODE','excel')
setenv('HYDROPOL_INPUT_EXCEL_FILE','/absolute/path/to/HydroPol2D_Inputs.xlsx')
setenv('HYDROPOL_EXPORT_ROOT_DIR','/absolute/path/to/Outputs/my_run')
setenv('HYDROPOL_SKIP_POSTPROCESS','')
run('run_HydroPol2D.m')
```

Antes de la versión 1.19.0-rc2, el script principal se llamaba `HydroPol2D_V115.m`. Ese nombre todavía funciona.

Con `HYDROPOL_SKIP_POSTPROCESS` igual a `1`, se hace una simulación de diagnóstico solo del solucionador. Para la simulación completa normal, se deja vacío.

## Convertir un caso antiguo {#convert-an-older-case}

Desde `tools/workbook_builder`, en el repositorio de MATLAB, se ejecuta lo siguiente.

```bash
python build_input_workbook.py input_catalog.yaml General_Data.xlsx HydroPol2D_Inputs.xlsx
```

El constructor traslada cada valor, ruta de mapa, lista de mapas y estación, y copia las tablas de clases y las series de los libros de Excel ubicados junto al archivo de origen. El caso en V da resultados idénticos con el libro convertido y con los archivos antiguos (`Validation/Workbook/run_single_workbook_checks.m`).

## Formato anterior {#older-layout}

Los casos creados antes del 2026-10-20 usan `General_Data.xlsx`, con su hoja `Flags` y libros de Excel separados (`SOIL_parameters.xlsx`, `LULC_parameters.xlsx`, `Rainfall_Intensity_Data.xlsx` y los demás). Siguen funcionando sin cambios.

- `run_HydroPol2D.m` usa `General_Data.xlsx` cuando la carpeta de entrada no tiene `HydroPol2D_Inputs.xlsx`, o el archivo que indica `HYDROPOL_INPUT_EXCEL_FILE`.
- Cada lector toma su pestaña del libro del caso cuando el caso lo tiene y, si no, del libro de Excel anterior.
- Los libros de Excel complementarios deben estar en la misma carpeta que `General_Data.xlsx`. Las rutas relativas se resuelven desde esa carpeta.

## Configurar con archivos de MATLAB {#configure-with-matlab-files-instead}

Para estudios con scripts, ensambles o una configuración controlada línea por línea en Git, se usa el modo bypass.

1. Definir `run_mode = 'bypass'` en `run_HydroPol2D.m`.
2. Definir los controles de procesos y numéricos en `Config/input_data_bypass_script.m`.
3. Definir las rutas de rásteres y de forzamientos en `Config/input_paths_bypass.m`.
4. Ejecutar `run_HydroPol2D.m`.

El ejemplo en V tiene su propia configuración en código. Se ejecuta `addpath('Examples/VTilted_Excel')` y luego `run_code('regular')` o `run_code('voronoi')`.

El modo Excel conviene cuando un libro de Excel es el registro más práctico del proyecto. El modo bypass conviene cuando la configuración debe generarse o revisarse como código.
