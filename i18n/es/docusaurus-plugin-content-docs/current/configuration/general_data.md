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
| $\mathrm{topo\_path}$ | — | Ruta al directorio TopoToolbox |
| $\mathrm{PHTOKEN0XYZ\_path}$ | — | Camino hacia el modelo de elevación digital |
| $\mathrm{PHTOKEN0XYZ\_path}$ | — | Ruta al ráster de uso del suelo/cobertura del suelo |
| $\mathrm{SOIL\_path}$ | — | Ruta al ráster de clasificación del suelo |
| $\mathrm{Warmup\_Depth\_path}$ | — | Camino hacia la condición inicial de profundidad del agua de calentamiento |
| $\mathrm{Initial\_Buildup\_path}$ | — | Ruta hacia el mapa inicial de acumulación de contaminantes |
| $\mathrm{Initial\_Soil\_Moisture\_path}$ | — | Camino hacia la condición inicial de humedad del suelo. |
| $\mathrm{Albedo\_path}$ | — | Camino a la trama de albedo |
| $\mathrm{PHTOKEN0XYZ\_path}$ | — | Ruta al ráster de índice de área foliar |
| $\mathrm{RiverWidths\_path}$ | — | Ruta al ráster de ancho del río |
| $\mathrm{RiverDepths\_path}$ | — | Trama de ruta a la profundidad del río |
| $\mathrm{PHTOKEN0XYZ\_path}$ | — | Ruta al ráster desde la profundidad hasta el lecho de roca |
| $\mathrm{B1\_path}$ | — | Ruta al ráster de parámetros relacionados con contaminantes |
| $\mathrm{B2\_path}$ | — | Ruta al ráster de parámetros relacionados con contaminantes |
| $\mathrm{W1\_path}$ | — | Ruta hacia el ráster de parámetros de eliminación de contaminantes |
| $\mathrm{W2\_path}$ | — | Ruta hacia el ráster de parámetros de eliminación de contaminantes |
| $\mathrm{hydropol2d\_tools}$ | — | Ruta a la biblioteca de funciones HydroPol2D |

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

## Notas

Las descripciones proporcionadas aquí representan la función funcional de cada parámetro dentro de HydroPol2D.
Las definiciones finales deben perfeccionarse en función de:
- comentarios de hoja de cálculo
- estrategia de calibración
- contexto de aplicación

Esta tabla sirve como referencia central para la configuración del modelo.
