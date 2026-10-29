---
title: Forzamientos opcionales
---

# Forzamientos opcionales

HydroPol2D admite varios tipos de forzamiento meteorológico e hidrológico, además de una sola serie de lluvia. En el libro del caso de MATLAB `HydroPol2D_Inputs.xlsx`, los interruptores están en las pestañas Rain and ET, Design storm, Soil and groundwater y Surface flow. Las series temporales están en cinco pestañas de series, y las listas de archivos de mapas están en la pestaña Rain and ET.

---

## Dónde se define cada forzamiento {#where-each-forcing-is-set}

| Forzamiento | Interruptor (pestaña) | Datos |
|---|---|---|
| Serie de lluvia uniforme | `flag_rainfall` (Rain and ET), sin otra fuente de lluvia | Pestaña Rain series |
| Pluviómetros, interpolados | `flag_spatial_rainfall` (Rain and ET) | Pestaña Rain gauges |
| Mapas de lluvia | `flag_input_rainfall_map` (Rain and ET) | Lista Rainfall maps (pestaña Rain and ET) |
| Lluvia satelital | `flag_satellite_rainfall`, `flag_real_time_satellite_rainfall` (Rain and ET) | Preparada por el flujo de trabajo satelital |
| Tormenta de diseño | `flag_alternated_blocks` o `flag_huff` (Design storm) | Parámetros del hietograma y de la IDF en la misma pestaña |
| Evapotranspiración de Penman–Monteith | `flag_ETP` (Soil and groundwater), sin mapas de ET | Pestaña Climate stations |
| Mapas de evaporación y transpiración | `flag_input_ETP_map` (Rain and ET) | Listas Transpiration maps y Evaporation maps (pestaña Rain and ET) |
| Hidrogramas de entrada | `flag_inflow` (Surface flow) | Pestaña Inflow hydrographs |
| Hidrogramas de nivel | `flag_stage_hydrograph` (Surface flow) | Pestaña Stage hydrographs |

Se usa una sola fuente de lluvia a la vez. Una serie que los interruptores del caso no leen puede quedar como plantilla vacía con sus encabezados. Todos los interruptores y parámetros se listan en [Parámetros del libro del caso](../configuration/general_data).

---

## Lluvia {#rainfall}

### Serie uniforme {#uniform-series}

La pestaña Rain series contiene un pluviómetro, con la intensidad de lluvia (mm/h) en el tiempo. La lluvia se aplica de manera uniforme sobre el dominio. La pestaña se lee cuando la lluvia está activada y no se elige tormenta de diseño, mapa, lluvia satelital ni lluvia espacial.

Cada tiempo marca el inicio de un intervalo. Un valor rige hasta el tiempo siguiente; el último valor rige durante un intervalo más, y después la tasa es 0. En el ejemplo en V, 10.8 mm/h a los 0 min y 0 mm/h a los 90 min significan lluvia de 10.8 mm/h entre 0 y 90 min y ninguna lluvia entre 90 y 180 min. La misma regla se aplica a los pluviómetros, los mapas de lluvia, los mapas de evaporación y transpiración y los hidrogramas de entrada. Un hidrograma de nivel mantiene cada profundidad desde su tiempo hasta el siguiente.

:::warning[Cambiado el 2026-10-29]
Antes del 2026-10-29, MATLAB leía los tiempos de lluvia, caudal de entrada y mapas de ET como finales de intervalo, y HydroPol2D-Python los leía como inicios de intervalo. Ahora MATLAB también los lee como inicios de intervalo. La primera fila de una tabla que empieza en 0 min, como toda tabla con fechas, ahora se usa. Una tabla escrita con finales de intervalo (primer tiempo = un paso) debe adelantar cada tiempo un paso para conservar su significado. Las tormentas de diseño se reajustan automáticamente.
:::

### Pluviómetros {#rain-gauges}

La pestaña Rain gauges contiene varios pluviómetros, interpolados a cada celda por el inverso de la distancia ponderado. Se lee cuando `flag_spatial_rainfall = 1` y no se dan mapas de lluvia. Cada pluviómetro ocupa una columna, con su índice, su nombre y sus coordenadas (m, en la proyección del DEM), seguidos de su intensidad (mm/h) en cada tiempo (min) de la columna B.

### Mapas de lluvia {#rainfall-maps}

La lista Rainfall maps de la pestaña Rain and ET tiene una fila por mapa, con el tiempo en minutos desde la fecha de inicio y la ruta de un GeoTIFF en mm/h. Se lee cuando `flag_input_rainfall_map = 1` o cuando un interruptor de lluvia satelital vale 1.

---

## Tormentas de diseño {#design-storms}

La pestaña Design storm genera un hietograma sintético en lugar de leer una serie de lluvia.

| Parámetro | Clave | Unidad |
|---|---|---|
| Bloques alternados o curvas de Huff | `flag_alternated_blocks`, `flag_huff` | 0 / 1 |
| Período de retorno | `RP` | años |
| Duración de la tormenta | `Rainfall Duration` | min |
| Paso de tiempo del hietograma | `dt_design` | min |
| Coeficientes de la IDF | `K`, `a`, `b`, `c` | ver abajo |

La intensidad sigue la relación IDF local

$$
i = \frac{K\,\mathrm{RP}^{a}}{(b + t_d)^{c}}
$$

donde $i$ es la intensidad (mm/h), $\mathrm{RP}$ el período de retorno (años) y $t_d$ la duración (min). $K$ debe ser consistente con estas unidades. $a$ y $c$ son adimensionales, y $b$ está en minutos. Se deben usar coeficientes ajustados para el sitio de estudio.

---

## Evapotranspiración {#evapotranspiration}

### Penman–Monteith a partir de estaciones climáticas {#penman-monteith-from-climate-stations}

Con `flag_ETP = 1` y sin mapas de ET, HydroPol2D calcula la evapotranspiración con Penman–Monteith a partir de datos meteorológicos diarios de una o más estaciones, interpolados a la malla por el inverso de la distancia ponderado. En la pestaña Climate stations, la fila 2 nombra el bloque de cada estación (índice, coordenadas este y norte en m), la fila 3 contiene los encabezados de sus columnas y cada fila a partir de la fila 4 corresponde a un día. Las variables típicas son la temperatura del aire, la radiación, la humedad relativa y la velocidad del viento.

### Mapas de evaporación y transpiración {#evaporation-and-transpiration-maps}

Con `flag_input_ETP_map = 1`, el modelo lee dos listas de la pestaña Rain and ET, Transpiration maps y Evaporation maps. Cada fila contiene el tiempo en días desde la fecha de inicio y la ruta de un GeoTIFF en mm/día. Ambas listas deben tener los mismos tiempos. Los flujos se aplican directamente al agua superficial y a la humedad del suelo, por lo que no se necesita forzamiento meteorológico.

:::warning[Corregido el 2026-10-20]
En `General_Data.xlsx`, las listas de lluvia, transpiración y evaporación comparten una fila de encabezado. Antes del 2026-10-20, la lista de transpiración leía la columna `Time [min]` de la lista de lluvia (sin conversión de días a minutos), y la lista de evaporación leía las rutas de transpiración. Las simulaciones con `flag_input_ETP_map = 1` hechas antes de esa fecha usaron tiempos de ET y mapas de evaporación incorrectos. Esos casos deben ejecutarse de nuevo. Ahora cada lista termina en su primera fila vacía, y sus columnas se buscan solo bajo su propio título, en ambos formatos.
:::

---

## Hidrogramas de contorno {#boundary-hydrographs}

### Hidrogramas de entrada {#inflow-hydrographs}

La pestaña Inflow hydrographs, que se lee cuando `flag_inflow = 1`, admite hasta 50 estaciones. Cada estación es un bloque de cinco columnas con el tiempo (min), el caudal (m³/s) y las coordenadas este y norte (m) de cada celda por la que entra el caudal, una celda por fila. El caudal se reparte entre esas celdas. Se deben conservar los 50 bloques, incluso los vacíos.

Los hidrogramas de entrada representan contornos aguas arriba, aportes de ríos y descargas por rotura de presa o controladas.

### Hidrogramas de nivel {#stage-hydrographs}

La pestaña Stage hydrographs, que se lee cuando `flag_stage_hydrograph = 1`, tiene la misma disposición, con el tiempo (min), la profundidad del agua (m) y las coordenadas este y norte (m) de cada celda del contorno. Todas las celdas de un contorno reciben la misma profundidad impuesta. Se deben conservar los 50 bloques, incluso los vacíos.

Los hidrogramas de nivel representan el control aguas abajo, el remanso y otras restricciones hidráulicas.

---

## Consideraciones prácticas {#practical-considerations}

- Todos los forzamientos deben usar la misma referencia de tiempo que `date_begin` y `date_end`.
- Se deben verificar las unidades de cada serie, es decir, lluvia en mm/h, mapas de ET en mm/día, caudal de entrada en m³/s y nivel en m.
- No se deben mezclar fuentes de lluvia, y se debe verificar que las estaciones y las celdas de contorno estén ubicadas en la proyección del DEM.
- Se debe usar un intervalo de forzamiento que resuelva los picos necesarios, dado el paso de tiempo del modelo.

---

## Formato anterior {#older-layout}

En los casos que usan `General_Data.xlsx`, cada serie es un libro de Excel propio en la misma carpeta, es decir, `Rainfall_Intensity_Data.xlsx` (Rain series), `Rainfall_Spatial_Input.xlsx` (Rain gauges), `ETP_input_data.xlsx` (Climate stations), `Inflow_Hydrograph.xlsx` y `Stage_Hydrograph.xlsx`. Las listas de mapas son las tablas Satellite or Radar Rainfall, Satellite transpiration y Satellite evaporation de `General_Data`. El libro del caso conserva la misma disposición de celdas, por lo que el modelo lee ambos formatos de la misma manera.
