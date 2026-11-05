---
title: Ejecutar el caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Ejecutar el caso

Un caso que pasó la verificación se ejecuta en HydroPol2D MATLAB o en HydroPol2D Studio, según lo
que eligió en **Prepare for**. Los paneles de ejecución aparecen debajo del resultado de la
verificación, tanto después de **Prepare complete case** como en **Check a case**.

| Preparado para | Ejecútelo en | Desde |
|---|---|---|
| **HydroPol2D MATLAB** | HydroPol2D MATLAB (código abierto) | el panel **Run HydroPol2D MATLAB**, o el propio MATLAB |
| **HydroPol2D Python** | HydroPol2D Studio | **Open existing model** en Studio, con `hydropol_python/case.yaml` |
| **Python and MATLAB** | cualquiera de los dos | ambos |

## En HydroPol2D MATLAB, desde la app {#matlab-from-the-app}

Necesita MATLAB en su computadora. El panel **Run HydroPol2D MATLAB** tiene:

- **HydroPol2D MATLAB folder**: una carpeta con el código de HydroPol2D MATLAB. Una carpeta que ya
  lo contiene se usa tal como está, sin actualizarla. Si la carpeta no existe, la app descarga en
  ella HydroPol2D desde su [repositorio de GitHub](https://github.com/marcusnobrega-eng/HydroPol2D)
  (rama `main`). Esa descarga necesita [Git](https://git-scm.com).
- **MATLAB executable**: se encuentra solo cuando MATLAB está instalado en el lugar habitual. Si no,
  indique su ruta, por ejemplo `/Applications/MATLAB_R2025b.app/bin/matlab` en un Mac o
  `C:\Program Files\MATLAB\R2025b\bin\matlab.exe` en Windows.

**Run HydroPol2D MATLAB** inicia MATLAB en segundo plano. El botón solo está activo después de que
la verificación se superó. **Refresh status** actualiza la página mientras el modelo se ejecuta:

- el estado ("MATLAB is running in the background", "MATLAB simulation completed successfully",
  o el código de salida cuando se detuvo);
- una barra de progreso con la etapa y la proporción del tiempo simulado;
- **Simulated time**, **Time step**, **Elapsed** y **Estimated remaining**;
- la lluvia media y máxima, la profundidad máxima, el caudal en la salida, el almacenamiento total,
  el error de balance de masa y la profundidad media del agua subterránea;
- el **MATLAB run log**, que se abre solo cuando la simulación falla.

Cuando la simulación termina, **Results** muestra la profundidad máxima del agua superficial como
un número, un mapa y una animación, y da el nombre del GeoTIFF de profundidad máxima para un SIG.
El estado y los registros están en `model_runs/` dentro del caso, y los resultados en `Outputs/`.

## En HydroPol2D MATLAB, a mano {#matlab-by-hand}

El `run_case.m` del caso define las rutas, las fechas, la resolución, la lluvia, las condiciones de
contorno, las salidas y las opciones de ejecución del caso, y luego inicia HydroPol2D. En MATLAB:

```matlab
addpath('/path/to/CASE_DIR/hydropol_matlab')
run_case('/path/to/HydroPol2D')
```

La primera ruta es la carpeta del caso, la segunda su carpeta de HydroPol2D MATLAB. `run_case.m` no
cambia los archivos de configuración de HydroPol2D: pasa el caso al modelo en memoria, así que la
misma carpeta de HydroPol2D puede ejecutar muchos casos. Un caso en la malla nativa (una malla
quadtree, un caso Urban Area Only o tablas hidráulicas) se ejecuta con el solver de malla nativo de
HydroPol2D y escribe un archivo de resultados de malla nativa. Vea el
[flujo de trabajo de MATLAB](../getting-started/excel-workflow) para el modelo en sí.

## En HydroPol2D Studio {#studio}

1. Abra HydroPol2D Studio.
2. En **Home**, elija **Open existing model**.
3. Elija `hydropol_python/case.yaml` en la carpeta del caso.

El caso se abre en **Setup**, listo para verificarlo y ejecutarlo. Desde allí, las herramientas de
Studio trabajan sobre él, por ejemplo el drenaje urbano, los estanques de detención, la
infraestructura verde, los cruces, los resultados y la calibración. Vea la
[guía de Studio](../studio/overview).

El panel **Run HydroPol2D Python** de la app pide una carpeta que contenga HydroPol2D Python. La app
no descarga HydroPol2D Python, que viene con Studio. Sin esa carpeta, el panel lo indica y remite a
Studio.

## Dónde quedan los resultados {#results}

| Simulación | Resultados |
|---|---|
| MATLAB, malla regular | `Outputs/`, con las vistas previas de los resultados en `Outputs/PostProcessing/` |
| MATLAB, malla nativa | `Outputs/Modeling_Results/Native/unstructured_results.nc` y las vistas previas |
| Python | `Outputs/python/Modeling_Results/`: figuras, GeoTIFF estáticos y animaciones |

Los mapas guardados y su intervalo siguen **Saved outputs** ([Ajustes del caso](settings#saved-outputs)).
