---
title: Parámetros de configuración
---

# Parámetros de configuración

Esta página documenta todas las variables definidas en `General_Data.xlsx`.
Cada parámetro controla un aspecto específico de HydroPol2D, que incluye:
- sincronización de simulación
- estabilidad numérica
- procesos hidrológicos
- enrutamiento hidráulico
- conjuntos de datos de entrada
- control de salida

---

## Control de funcionamiento

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{time\_step\_model}$ | $\mathrm{s}$ | Paso de tiempo del modelo inicial utilizado en la simulación. |
| $\mathrm{min\_time\_step}$ | $\mathrm{s}$ | Paso de tiempo adaptativo mínimo permitido para la estabilidad numérica |
| $\mathrm{max\_time\_step}$ | $\mathrm{s}$ | Paso de tiempo adaptativo máximo permitido |
| $\mathrm{time\_step\_change}$ | $\mathrm{s}$ | Incremento utilizado para ajustar el paso de tiempo adaptativo |
| $\alpha_{\min}$ | — | Coeficiente de estabilidad mínimo tipo Courant |
| $\alpha_{\max}$ | — | Coeficiente de estabilidad máximo tipo Courant |
| $\mathrm{date\_begin}$ | — | Fecha y hora de inicio de la simulación. |
| $\mathrm{date\_end}$ | — | Fecha y hora de finalización de la simulación |

---

## Condición de límite de flujo normal

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{slope\_outlet}$ | $\mathrm{m\,m^{-1}}$ | Pendiente prescrita utilizada para estimar las condiciones normales de flujo en el límite de salida |

---

## Control del agua subterránea {#groundwater-control}

Celdas D5:E8. Los valores siguientes son los de los libros distribuidos.

| Variable | Unidades | Valor en el libro | Descripción |
|----------|----------|----------|----------|
| $\mathrm{groundwater\_courant}$ | - | 0.25 | Factor de seguridad del límite explícito del paso de tiempo del agua subterránea. En el esquema en capas, limita los subpasos del flujo lateral. |
| $\mathrm{deep\_recharge\_fraction}$ | - | 0.05 | Fracción de la recarga descendente enviada al acuífero profundo (con $\mathrm{flag\_deep\_aquifer} = 1$). |
| $\mathrm{deep\_aquifer\_tau\_days}$ | días | 180 | Tiempo de respuesta $\tau$ de los embalses lineales profundos. |

---

## Subsuelo en capas {#layered-subsurface}

Bloque D10:F28. Solo se lee cuando $\mathrm{flag\_layered\_subsurface} = 1$. Ver [Subsuelo en Capas](../theory/layered-subsurface). Una celda vacía mantiene el valor predeterminado o la alternativa indicada en la tabla.

| Variable | Unidades | Predeterminado | Descripción |
|----------|----------|----------|----------|
| $\mathrm{subsurface\_soil\_base\_depth\_m}$ | m | 2.0 | Base del suelo, es decir, fondo de las tres capas de suelo. $\mathrm{SoilBaseDepth\_path}$ tiene prioridad donde es finito. |
| $\mathrm{subsurface\_depth\_to\_bedrock\_m}$ | m | vacío | Fondo de toda la columna. Prioridad: $\mathrm{DTB\_path}$, luego este valor y luego la profundidad del suelo predeterminada (1 m cuando $\mathrm{DTB\_path}$ está vacío), con una advertencia. |
| $\mathrm{subsurface\_max\_depth\_m}$ | m | 50 | Límite de la profundidad de la columna. La base de la columna es $\min(\mathrm{DTB}, \text{cap})$. |
| $\mathrm{subsurface\_deep\_first\_thickness\_m}$ | m | 0.25 | Espesor de la primera capa de regolito por debajo de la base del suelo. |
| $\mathrm{subsurface\_deep\_growth\_ratio}$ | - | 2 | Razón de espesor entre capas de regolito consecutivas. |
| $\mathrm{subsurface\_deep\_max\_thickness\_m}$ | m | 4 | Espesor máximo de una capa de regolito. |
| $\mathrm{regolith\_theta\_s}$ | m³/m³ | 0.35 | Contenido de agua a saturación del regolito. Ráster: $\mathrm{RegolithThetaS\_path}$. |
| $\mathrm{regolith\_theta\_r}$ | m³/m³ | 0.05 | Contenido de agua residual del regolito. Ráster: $\mathrm{RegolithThetaR\_path}$. |
| $\mathrm{regolith\_alpha\_vg\_m\_inverse}$ | 1/m | 2 | $\alpha$ de van Genuchten del regolito. Ráster: $\mathrm{RegolithAlphaVG\_path}$. |
| $\mathrm{regolith\_n\_vg}$ | - | 1.5 | $n$ de van Genuchten del regolito. Ráster: $\mathrm{RegolithNVG\_path}$. |
| $\mathrm{regolith\_ksat\_v\_mm\_h}$ | mm/h | 5 | Conductividad saturada vertical del regolito. Ráster: $\mathrm{RegolithKsatV\_path}$. |
| $\mathrm{regolith\_ksat\_h\_mm\_h}$ | mm/h | vacío | Conductividad saturada horizontal del regolito. Vacío: $\mathrm{kgsat}$ de la tabla de suelos. Ráster: $\mathrm{RegolithKsatH\_path}$. |
| $\mathrm{regolith\_specific\_yield}$ | - | vacío | Rendimiento específico del regolito. Vacío: $\theta_s - \theta_{fc}$ de la curva del regolito. Ráster: $\mathrm{RegolithSpecificYield\_path}$. |
| $\mathrm{soil\_lateral\_anisotropy}$ | - | 1 | $K_h/K_v$ de las capas de suelo. |
| $\mathrm{subsurface\_drainage\_substeps}$ | - | 1 | Subpasos de la cascada de drenaje por paso del modelo. |
| $\mathrm{capillary\_field\_capacity\_head\_m}$ | m | 3.3 | Succión a capacidad de campo. Define $S_y = \theta_s - \theta_{fc}$ para todas las capas. |
| $\mathrm{groundwater\_target\_dt\_s}$ | s | 3600 | Intervalo de la actualización lateral del agua subterránea. |
| $\mathrm{groundwater\_min\_dt\_s}$ | s | 60 | Intervalo mínimo de la actualización lateral del agua subterránea. |

---

## Estrés hídrico de Feddes en las raíces {#feddes-root-water-stress}

Bloque D30:F36. Solo se lee cuando $\mathrm{flag\_feddes} = 1$. Ver [Modelo hidrológico, sección 3.5](../theory/hydrologic-model#35-feddes-root-water-uptake-stress). Las cargas deben cumplir $0 \ge h_1 > h_2 \ge h_3 > h_4$.

| Variable | Unidades | Predeterminado | Descripción |
|----------|----------|----------|----------|
| $\mathrm{feddes\_h1\_m}$ | m | −0.1 | Más húmedo que este valor: sin absorción (anaerobiosis). |
| $\mathrm{feddes\_h2\_m}$ | m | −0.25 | Inicio de la absorción sin estrés. |
| $\mathrm{feddes\_h3\_m}$ | m | −4.0 | Fin de la absorción sin estrés. |
| $\mathrm{feddes\_h3\_low\_m}$ | m | vacío: $h_3$ | $h_3$ con una transpiración potencial de 1 mm/día o menos. |
| $\mathrm{feddes\_h3\_high\_m}$ | m | vacío: $h_3$ | $h_3$ con una transpiración potencial de 5 mm/día o más. |
| $\mathrm{feddes\_h4\_m}$ | m | −80 | Punto de marchitez: sin absorción. |

---

## Estado inicial del acuífero profundo {#deep-aquifer-initial-state}

Bloque D38:F40. Solo se lee cuando $\mathrm{flag\_deep\_aquifer} = 1$. Se debe indicar como máximo un valor, o un archivo en $\mathrm{DeepAquiferInitialState\_path}$ (T29). Si no se indica ninguno, los embalses parten vacíos. Ver [Modelo de aguas subterráneas, sección 13](../theory/groundwater-model#13-deep-aquifer).

| Variable | Unidades | Predeterminado | Descripción |
|----------|----------|----------|----------|
| $\mathrm{deep\_aquifer\_initial\_baseflow\_mm\_day}$ | mm/día | vacío | Flujo base profundo por unidad de área $q_0$ en la fecha de inicio. Cada subcuenca parte de $S_0 = q_0 A \tau$. |
| $\mathrm{deep\_aquifer\_mean\_recharge\_mm\_year}$ | mm/año | vacío | Recarga media de largo plazo $\bar{R}$. Los embalses parten en estado estacionario, $q_0 = f_d \bar{R}$. |

---

## Multiplicadores de la conductividad lateral {#lateral-conductivity-multipliers}

Bloque D42:F44. Solo se lee con el subsuelo en capas. El rendimiento específico no se escala, porque proviene de las curvas de retención. La [calibración por recesión del agua subterránea](../calibration/groundwater-recession) ajusta ambos factores. El Case Builder pasa los valores ajustados a MATLAB mediante `HYDROPOL_SOIL_LATERAL_CONDUCTIVITY_MULTIPLIER` y `HYDROPOL_REGOLITH_LATERAL_CONDUCTIVITY_MULTIPLIER`, que tienen prioridad sobre estas celdas.

| Variable | Unidades | Predeterminado | Descripción |
|----------|----------|----------|----------|
| $\mathrm{soil\_lateral\_conductivity\_multiplier}$ | - | 1 | Factor sobre la conductividad horizontal de las tres capas de suelo ($K_{sat}$ del suelo × anisotropía). |
| $\mathrm{regolith\_lateral\_conductivity\_multiplier}$ | - | 1 | Factor sobre la conductividad horizontal de las capas de regolito. |

---

## Control de mapas y parcelas

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{record\_time\_maps}$ | $\mathrm{min}$ | Intervalo de tiempo para guardar resultados ráster |
| $\mathrm{record\_time\_hydrographs}$ | $\mathrm{min}$ | Intervalo de tiempo para guardar las salidas del hidrograma |
| $\mathrm{Pol\_min}$ | $\mathrm{mg\,L^{-1}}$ | Umbral mínimo de concentración de contaminantes para visualización |
| $\mathrm{depth\_wse}$ | $\mathrm{m}$ | Profundidad umbral utilizada para definir resultados de elevación de la superficie del agua |
| $\mathrm{flag\_wse}$ | — | Bandera para activar salidas de elevación de la superficie del agua en lugar de profundidad |
| $\mathrm{record\_time\_spatial\_rainfall}$ | $\mathrm{min}$ | Intervalo de tiempo para exportar mapas espaciales de lluvia |
| $\mathrm{time\_save\_ETP}$ | $\mathrm{min}$ | Intervalo de tiempo para guardar las salidas de evapotranspiración |
| $\mathrm{record\_time\_spatial\_ETP}$ | $\mathrm{min}$ | Intervalo de tiempo para exportar campos ETP espaciales |

---

## Parámetros de geometría del río
Si se activa `flag_reduce_dem`, la elevación de las celdas del río se reduce para tener en cuenta la batimetría del río. Luego se requiere un conjunto de 4 parámetros para describir el ancho y la profundidad del flujo. Estos parámetros son válidos para convertir el área de acumulación de flujo [$\mathrm{km^2}$] en profundidad de flujo [$\mathrm{m}$] y ancho [$\mathrm{m}$].| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\alpha_1$ | — | Coeficiente empírico que controla el escalado de la geometría del canal. |
| $\alfa_2$ | — | Coeficiente secundario para relaciones de geometría hidráulica. |
| $\beta_1$ | — | Ancho de control de exponente o comportamiento de escalado hidráulico |
| $\beta_2$ | — | Exponente secundario para relaciones de escala hidráulica. |
| $n$ | $\mathrm{s\,m^{-1/3}}$ | Coeficiente de rugosidad de Manning para canal y flujo superficial. |

---

## Entradas de calidad del agua

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{ADD}$ | $\mathrm{days}$ | Días secos anteriores utilizados en el modelado de acumulación de contaminantes |
| $\mathrm{min\_Bt}$ | $\mathrm{g\,m^{-2}}$ | Umbral mínimo de acumulación de contaminantes |
| $\mathrm{Bmin}$ | $\mathrm{g\,m^{-2}}$ | Masa contaminante mínima permitida |
| $\mathrm{Bmax}$ | $\mathrm{g\,m^{-2}}$ | Capacidad máxima de acumulación de contaminantes |

---

## DEM Procesamiento y controles de terreno

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{min\_area}$ | $\mathrm{km^2}$ | Umbral mínimo del área de drenaje para la iniciación del canal. |
| $\tau$ | — | Parámetro de suavizado que controla la intensidad del filtrado DEM |
| $\mathrm{K\_value}$ | — | Control de parámetros, procesamiento del terreno o escalado hidráulico. |
| $\mathrm{sl}$ | $\mathrm{m\,m^{-1}}$ | Umbral de pendiente mínima utilizado en el acondicionamiento DEM |
| $\mathrm{resolution\_resample}$ | $\mathrm{m}$ | Resolución objetivo para el remuestreo DEM |
| $\mathrm{slope\_DTM}$ | $\%$ | Umbral de pendiente utilizado para corrección o filtrado del terreno |

---

## Rutas de archivos y datos de entrada

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{DEM\_path}$ | — | Ruta al modelo digital de elevación |
| $\mathrm{LULC\_path}$ | — | Ruta al ráster de uso y cobertura del suelo |
| $\mathrm{SOIL\_path}$ | — | Ruta al ráster de clasificación del suelo |
| $\mathrm{Warmup\_Depth\_path}$ | — | Camino hacia la condición inicial de profundidad del agua de calentamiento |
| $\mathrm{Initial\_Buildup\_path}$ | — | Ruta hacia el mapa inicial de acumulación de contaminantes |
| $\mathrm{Initial\_Soil\_Moisture\_path}$ | — | Camino hacia la condición inicial de humedad del suelo. |
| $\mathrm{Initial\_SWE\_path}$ | — | Ruta opcional al SWE inicial en milímetros |
| $\mathrm{Initial\_Snow\_Depth\_path}$ | — | Ruta opcional a la profundidad física inicial de nieve en milímetros |
| $\mathrm{Albedo\_path}$ | — | Camino a la trama de albedo |
| $\mathrm{LAI\_path}$ | — | Ruta al ráster de índice de área foliar |
| $\mathrm{RiverWidths\_path}$ | — | Ruta al ráster de ancho del río |
| $\mathrm{RiverDepths\_path}$ | — | Trama de ruta a la profundidad del río |
| $\mathrm{DTB\_path}$ | — | Ruta al ráster de profundidad al lecho rocoso. En el subsuelo en capas, fondo de toda la columna |
| $\mathrm{SoilBaseDepth\_path}$ | - | Ráster opcional de profundidad de la base del suelo (m), subsuelo en capas (T21) |
| $\mathrm{RegolithThetaS\_path}$ | - | Ráster opcional de $\theta_s$ del regolito (T22) |
| $\mathrm{RegolithThetaR\_path}$ | - | Ráster opcional de $\theta_r$ del regolito (T23) |
| $\mathrm{RegolithAlphaVG\_path}$ | - | Ráster opcional de $\alpha$ de van Genuchten del regolito (T24) |
| $\mathrm{RegolithNVG\_path}$ | - | Ráster opcional de $n$ de van Genuchten del regolito (T25) |
| $\mathrm{RegolithKsatV\_path}$ | - | Ráster opcional de $K_{sat}$ vertical del regolito, mm/h (T26) |
| $\mathrm{RegolithKsatH\_path}$ | - | Ráster opcional de $K_{sat}$ horizontal del regolito, mm/h (T27) |
| $\mathrm{RegolithSpecificYield\_path}$ | - | Ráster opcional de rendimiento específico del regolito (T28) |
| $\mathrm{DeepAquiferSubbasins\_path}$ | - | Ráster de subcuencas del acuífero profundo, que indica qué celdas alimentan cada embalse (T19) |
| $\mathrm{DeepAquiferChannelWeight\_path}$ | - | Ráster de pesos del canal, que indica dónde descarga cada embalse profundo (T20) |
| $\mathrm{DeepAquiferInitialState\_path}$ | - | JSON opcional del estado inicial del acuífero profundo, escrito por la calibración del Case Builder (T29) |
| $\mathrm{B1\_path}$ | — | Ruta al ráster de parámetros relacionados con contaminantes |
| $\mathrm{B2\_path}$ | — | Ruta al ráster de parámetros relacionados con contaminantes |
| $\mathrm{W1\_path}$ | — | Ruta hacia el ráster de parámetros de eliminación de contaminantes |
| $\mathrm{W2\_path}$ | — | Ruta hacia el ráster de parámetros de eliminación de contaminantes |

---

## Parámetros de inestabilidad humana

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mu$ | — | Coeficiente de fricción entre el cuerpo humano y el suelo. |
| $C_d$ | — | Coeficiente de arrastre para el cuerpo humano en flujo. |
| $\rho_{\mathrm{person}}$ | $\mathrm{kg\,m^{-3}}$ | Densidad del cuerpo humano. |
| $\mathrm{weight\_person}$ | $\mathrm{kg}$ | Peso humano promedio |
| $\mathrm{height\_person}$ | $\mathrm{m}$ | Altura humana promedio |
| $\mathrm{width1\_person}$ | $\mathrm{m}$ | Ancho frontal característico |
| $\mathrm{width2\_person}$ | $\mathrm{m}$ | Parámetro de ancho secundario |
| $\rho_{\mathrm{water}}$ | $\mathrm{kg\,m^{-3}}$ | densidad del agua |
| $g$ | $\mathrm{m\,s^{-2}}$ | aceleración gravitacional |

---

## Puntos de observación

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{Gauge}$ | — | Identificador de calibre |
| $\mathrm{Easting}$ | $\mathrm{m}$ | Coordenada este |
| $\mathrm{Northing}$ | $\mathrm{m}$ | Coordenada norte |
| $\mathrm{Label\ Name}$ | — | Etiqueta de salida para series temporales |

---

## Parámetros de tormenta de diseño

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{RP}$ | $\mathrm{years}$ | Período de retorno de la tormenta de diseño. |
| $\mathrm{Rainfall\ Duration}$ | $\mathrm{min}$ | Duración total de la tormenta |
| $K$ | — | Coeficiente intensidad-duración-frecuencia |
| $a$ | — | Parámetro de curva IDF |
| $b$ | — | Parámetro de curva IDF |
| $c$ | — | Parámetro de curva IDF |
| $\mathrm{dt\_design}$ | $\mathrm{min}$ | Resolución temporal de la tormenta sintética. |

---

## Precipitación por satélite o radar

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{min}$ | Paso de tiempo del ráster de lluvia |
| $\mathrm{Raster\ Directory}$ | — | Ruta a archivos ráster de lluvia |

---

## Transpiración satelital

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Índice de tiempo para datos de transpiración. |
| $\mathrm{Raster\ Directory}$ | — | Camino a los rásteres de transpiración |

---

## Evaporación satelital

| Variable | Unidades | Descripción |
|----------|------|-------------|
| $\mathrm{Time}$ | $\mathrm{day}$ | Índice de tiempo para datos de evaporación. |
| $\mathrm{Raster\ Directory}$ | — | Camino a los rásteres de evaporación |

---

## Convenciones del libro para los bloques de agua subterránea {#workbook-conventions-for-the-groundwater-blocks}

- Cada celda de entrada de los libros `General_Data` distribuidos tiene un comentario que la explica.
- Los nuevos bloques usan celdas de entrada blancas con bordes laterales.
- En el modo bypass, las mismas claves son campos de `InputData_Bypass.flags` (parámetros del esquema en capas y de Feddes) y de `InputData_Bypass.general` (estado inicial del acuífero profundo).
- Las variables de entorno `HYDROPOL_SUBSURFACE_SCHEME`, `HYDROPOL_ENABLE_FEDDES`, `HYDROPOL_<NAME>` para cualquier clave anterior, `HYDROPOL_DEEP_INITIAL_BASEFLOW_MM_DAY`, `HYDROPOL_DEEP_MEAN_RECHARGE_MM_YEAR` y `HYDROPOL_DEEP_INITIAL_STATE_PATH` tienen prioridad sobre el libro. El Case Builder las usa.
- Cada columna de `SOIL_parameters.xlsx` también tiene una nota, incluida la forma en que el subsuelo en capas trata `Sy` (se ignora), `kgsat` (alternativa para $K_h$ del regolito) y `DTB (m)` (no se lee).

## Decisiones pendientes {#open-decisions}

Estas preguntas están pendientes. Para cada una se indica el comportamiento actual.

| Pregunta | Comportamiento actual |
|---|---|
| ¿Debe `DTB_path` ser obligatorio en el modo Excel cuando el subsuelo en capas está activo? | No es obligatorio. Sin él, el fondo de la columna pasa a `subsurface_depth_to_bedrock_m` y luego a la profundidad del suelo predeterminada, con una advertencia. |
| ¿Qué ocurre con la columna `DTB (m)` de `SOIL_parameters.xlsx`? | No se lee. La profundidad del suelo proviene de `DTB_path`, o es 1 m cuando está vacío. |
| ¿Se pueden indicar rásteres de propiedades del suelo en el modo Excel? | El libro no tiene celdas para los rásteres de propiedades del suelo (`ThetaS_path`, `KsatNearSurface_path`, …), que el código lee de `InputPaths`. Solo los rásteres de base del suelo y del regolito (T21:T28) tienen celdas en Excel. |

---

## Notas

Las descripciones proporcionadas aquí representan la función funcional de cada parámetro dentro de HydroPol2D.
Las definiciones finales deben perfeccionarse en función de:
- comentarios de hoja de cálculo
- estrategia de calibración
- contexto de aplicación

Esta tabla sirve como referencia central para la configuración del modelo.
