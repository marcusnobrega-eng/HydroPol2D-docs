---
title: Verificar un caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Verificar un caso

Toda construcción termina con la verificación previa. **Check a case** la vuelve a ejecutar sobre
cualquier caso preparado, sin reconstruirlo: por ejemplo, después de mover un caso, de editar uno de
sus archivos o de prepararlo otro día.

1. Abra **Check a case**.
2. Pegue la carpeta del caso en **Prepared case directory**.
3. Haga clic en **Run preflight**.

La página dice entonces "Ready to run: all preflight checks passed." o "Not ready to run.", seguido
de la lista de problemas. Para un caso listo, los valores verificados están en un panel plegado y a
continuación aparecen los paneles de ejecución ([Ejecutar el caso](run-the-case)). El **Preflight
log** conserva los mensajes.

## Qué verifica {#what-it-checks}

| Grupo | Verificaciones |
|---|---|
| Archivos | están todos los mapas y las series que necesita el modelo elegido, y los archivos del modelo (`case.yaml`, `run_case.m` y sus entradas) están completos |
| Mallas | cada mapa tiene la malla de `DEM.tif` y cubre todas las celdas activas, y la malla está completa en los casos quadtree y Urban Area Only |
| Valores | sin valores negativos de profundidad hasta la roca, humedad del suelo, área foliar o lluvia, albedo y fracción impermeable entre 0 y 1, agua subterránea entre la superficie y la roca, y anchos y profundidades de los ríos presentes |
| Tiempo | cada paso de tiempo de lluvia desde el inicio del calentamiento hasta el fin, en una sola malla sobre todo el dominio, y clima que cubre el periodo |
| Terreno | el informe de HydroBathyDEM existe y su terreno se acepta para una simulación del modelo |
| Dominio | en un caso Catchment, la cuenca final y el primer contorno de HydroSHEDS difieren en menos de un factor de dos |
| Contornos | en Urban Area Only, cada borde exterior tiene exactamente una condición, y cada contorno activado de GloFAS o GTSM tiene datos |

El informe completo es `quality_report/preflight.json`, con `ready_to_run`, la lista de `failures` y
los valores verificados.

No ejecute un caso que no está listo. Lea los problemas, corrija las entradas (a menudo preparando
el caso de nuevo con otros ajustes) y vuelva a verificarlo. Una verificación superada dice que el
caso está completo y es coherente. No es una calibración ni una validación del modelo.

## Calibración del agua subterránea {#groundwater-calibration}

Cuando un caso Catchment se preparó con **Shallow-aquifer Ksat,h and Sy** en **Calibrate from
observed streamflow**, la página muestra **Calibrate groundwater parameters** para él. La
calibración ajusta una conductividad horizontal y un rendimiento específico del acuífero somero a
las recesiones de un hidrograma observado, luego los escribe en el caso y lo vuelve a verificar.

| Ajuste | Qué define |
|---|---|
| **Observed streamflow** | **USGS gauge** (con **USGS gauge ID**, por ejemplo 02145910) o **Local CSV** (con **Observed-discharge CSV**, columnas `date` y `observed_discharge_m3_s`) |
| **Observation start**, **Observation end** | el periodo del registro que se usa |
| **Ksat,h candidates (m/s)**, **Sy candidates** | los valores que se prueban (casos en capas: **Soil Kh multipliers** y **Regolith Kh multipliers**) |
| **Saved shallow-flow fraction** | el estado inicial se guarda cuando el flujo somero baja a esta proporción del caudal total (0,05) |
| **HydroPol2D Python folder** | una carpeta que contiene HydroPol2D Python |

**Run and apply groundwater calibration** la inicia en segundo plano, y **Refresh calibration
status** actualiza la página. El caudal observado se filtra con el método de Lyne-Hollick, las
recesiones forman una curva maestra de recesión, y un experimento de agua subterránea en una malla
regular ajusta los dos valores. Cuando termina, la página muestra "Groundwater calibration was
applied and the case passed preflight.", los valores ajustados de **Ksat,h** y **Specific yield**,
el día de recesión elegido y una figura de las recesiones observadas y calibradas. El caso no se
puede ejecutar antes de que se supere esta verificación final.

La calibración necesita HydroPol2D Python. La app no lo descarga, así que elija una carpeta que ya
lo contenga. El método se describe en
[Calibración por recesión del agua subterránea](../calibration/groundwater-recession).
