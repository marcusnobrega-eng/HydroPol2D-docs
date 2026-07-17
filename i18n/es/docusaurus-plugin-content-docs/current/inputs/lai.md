---
title: LAI
---

# Índice de área foliar (LAI)

El índice de área foliar (LAI) representa el área foliar total por unidad de superficie de suelo y se utiliza en HydroPol2D para caracterizar la densidad de la vegetación y su interacción con la lluvia y los procesos atmosféricos.
En la implementación actual del modelo, LAI se utiliza para representar los efectos del dosel sobre la interceptación y la evapotranspiración.
---

## Papel en HydroPol2D

LAI se utiliza para representar:
- Intercepción de lluvia por parte del dosel vegetal.
- Partición entre almacenamiento de paso y dosel
- Influencia de la vegetación en la evapotranspiración.

Los valores más altos de LAI corresponden a una vegetación más densa y una mayor capacidad de almacenamiento del dosel.
---

## Representación

LAI se proporciona como un **mapa ráster continuo**, donde cada celda de la cuadrícula contiene un valor que representa la densidad de la vegetación.
Los valores típicos oscilan entre:
- ~0 → suelo desnudo o superficies impermeables
- 1–3 → vegetación escasa a moderada
- 4–7+ → vegetación densa (p. ej., bosques)

Los valores deben ser consistentes con las condiciones de cobertura del suelo en el dominio.
---

## Representación Temporal

El LAI dinámico **no está implementado actualmente** en HydroPol2D.
Como resultado, LAI debe proporcionarse como **entrada estática**.
Los enfoques recomendados son:
- **Mediana LAI** → para simulaciones climatológicas o de largo plazo
- **Época húmeda LAI** → para simulaciones enfocadas en alta actividad de vegetación
- **Época seca LAI** → para simulaciones enfocadas en condiciones de vegetación reducida

La elección debe ser coherente con el objetivo de la simulación y el período de tiempo.
---

## Fuentes de datos

Varios conjuntos de datos proporcionan estimaciones globales de LAI:
### MODIS LAI (MOD15A2H)
- Región: Global
- Resolución: 500 m
- Resolución temporal: 8 días
- Producto ampliamente utilizado y consistente.
- Descargar: https://lpdaac.usgs.gov/products/mod15a2hv061/

---

### Servicio Terrestre Global Copernicus (LAI)
- Región: Global
- Resolución: 300 m
- Resolución temporal: 10 días
- Derivado de observaciones satelitales
- Descargar: https://land.copernicus.eu/global/products/lai

---

### VIIRS LAI
- Región: Global
- Resolución moderada
- Continuación de los productos de la era MODIS

---

### Google Earth Engine

Los conjuntos de datos LAI de MODIS, Copernicus y VIIRS están disponibles en Google Earth Engine y se pueden procesar para extraer valores medianos o estacionales.
---

## Coherencia con LULC

LAI debe ser consistente con la clasificación LULC.
La correspondencia típica incluye:
- Bosque → alto LAI
- Pastizales → moderado LAI
- Urbano → bajo o cercano a cero LAI

Las inconsistencias entre LULC y LAI darán como resultado un comportamiento poco realista del dosel.
---

## Consideraciones prácticas

Al preparar las entradas LAI:
- Utilice valores representativos para el período de simulación.
- Evite valores extremos o ruidosos de productos satelitales sin procesar
- Aplicar agregación temporal (mediana o promedios estacionales) cuando sea necesario
- Garantice la coherencia espacial con otras entradas ráster

Si no hay ningún conjunto de datos LAI disponible, se pueden asignar valores en función de las clases LULC, aunque esto introduce suposiciones adicionales.
---

## Resumen

LAI se utiliza en HydroPol2D para representar los efectos de la vegetación en la interceptación y la evapotranspiración.
Actualmente, el modelo asume un campo LAI estático y los usuarios deben seleccionar valores representativos según el período de simulación previsto.
Se requiere una selección cuidadosa de LAI para garantizar la coherencia con la cobertura del suelo y una representación realista de los procesos de vegetación.