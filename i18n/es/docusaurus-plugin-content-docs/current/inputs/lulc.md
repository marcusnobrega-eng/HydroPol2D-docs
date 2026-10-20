---
title: LULC
---

# Uso del suelo / Cobertura del suelo (LULC)

El mapa de uso del suelo/cobertura del suelo (LULC) define la distribución espacial de las características de la superficie en todo el dominio de simulación.
En HydroPol2D, la entrada LULC se utiliza para representar cómo diferentes partes del dominio responden a la lluvia y al flujo superficial mediante la asignación de parámetros.

---

## Papel en HydroPol2D

El mapa LULC se utiliza para definir la variabilidad espacial en:
- Rugosidad de la superficie (coeficiente de Manning)
- Almacenamiento de interceptación
- fracción impermeable
- Comportamiento de la evapotranspiración relacionado con la superficie

Estas propiedades influyen directamente en la generación de escorrentía, la velocidad del flujo y la retención de agua en la superficie.

---

## Representación LULC

HydroPol2D requiere un **mapa LULC categórico**.
A cada celda de la cuadrícula se le debe asignar un identificador de clase de uso del suelo (valor entero o categórico). Estas clases no se utilizan directamente en las ecuaciones rectoras. En cambio, sirven como **índices en tablas de parámetros**.
Para cada clase LULC, se define externamente un conjunto de parámetros en las tablas de entrada. Esto incluye:
- Coeficiente de rugosidad de Manning
- Capacidad de interceptación
- fracción impermeable
- Parámetros adicionales específicos del proceso

Este enfoque separa la información espacial de la definición de parámetros y permite una flexibilidad total en la configuración del comportamiento del modelo.

---

## Conjuntos de datos LULC disponibles

Varios conjuntos de datos LULC globales y regionales de alta calidad están disponibles gratuitamente:
### NLCD (Base de datos nacional de cobertura terrestre)
- Región: Estados Unidos
- Resolución: 30 m
- Incluye clases urbanas detalladas y superficies impermeables.
- Descargar: https://www.mrlc.gov/

---

### Portada mundial de la ESA
- Región: Global
- Resolución: 10 m
- Clasificación global de alta resolución.
- Descargar: https://worldcover2020.esa.int/

---

### Servicio de vigilancia terrestre de Copernicus
- Región: Europa y productos globales.
- Resolución: 10–100 m
- Incluye múltiples capas temáticas.
- Descargar: https://land.copernicus.eu/

---

### Cobertura terrestre MODIS (MCD12Q1)
- Región: Global
- Resolución: 500 m
- Series temporales anuales a largo plazo
- Descargar: https://lpdaac.usgs.gov/products/mcd12q1v061/

---

### Mundo dinámico
- Región: Global
- Resolución: 10 m
- Clasificación casi en tiempo real derivada de Sentinel-2
- Proporciona resultados de clase probabilística
- Particularmente útil para entornos dinámicos o que cambian rápidamente
- Acceso: Google Earth Engine

---

## Asociación de parámetros

Las clases LULC se asignan a los parámetros del modelo a través de las tablas de entrada.
Cada clase debe estar asociada con un conjunto consistente de valores físicos. Este mapeo determina cómo el modelo representa:
- Resistencia superficial al flujo
- Intercepción de lluvia
- Comportamiento de generación de escorrentía

La asignación de parámetros incorrecta o inconsistente afectará directamente los resultados de la simulación.

---

## Superficies impermeables

Las clases urbanas suelen incluir una fracción significativa de áreas impermeables (carreteras, tejados, aceras).
Estas zonas se caracterizan por:
- Infiltración insignificante
- Generación rápida de escorrentía
- Mayores velocidades de flujo

El parámetro de fracción impermeable se utiliza para representar este comportamiento y debe asignarse cuidadosamente para las clases de uso de suelo urbano.
### Anulación de ráster impermeable fraccional

HydroPol2D también puede ingerir un ráster `ImperviousFraction_path` opcional. Cuando está presente, refina la fracción impermeable celular más allá de la asignación LULC basada en clases.
Detalles de implementación actual:
- los valores ráster se pueden dar en porcentaje `[0,1]` o `[0,100]`,
- el ráster está alineado internamente con DEM,
- Las clases LULC construidas/explícitamente impermeables todavía se ven obligadas a permanecer completamente impermeables.

Por lo tanto, la tabla LULC aún define el comportamiento impermeable de la base, mientras que el ráster de fracción impermeable proporciona un refinamiento espacial sobre esa base.

---

## Resolución y alineación

El ráster LULC debe:
- Coincidir o volver a muestrear con la resolución DEM
- Utilice el mismo sistema de referencia de coordenadas proyectadas (CRS)
- Alinear espacialmente con todas las demás entradas ráster

Una desalineación conduce a una parametrización incorrecta y a una representación del flujo inconsistente.

---

## Reclasificación

Los conjuntos de datos sin procesar LULC suelen contener una gran cantidad de clases.
Para aplicaciones HydroPol2D, suele ser preferible:
- Agregar clases en un conjunto reducido de categorías representativas
- Agrupar tipos de uso de suelo similares
- Simplifique el esquema de parametrización

Esto mejora la solidez del modelo y reduce la complejidad innecesaria.

---

## Interacción con otras entradas

El mapa LULC define el comportamiento de la superficie y debe ser consistente con:
- **DEM** → define el terreno y la ruta del flujo
- **Suelo** → controla la capacidad de infiltración
- **LAI** → influye en los procesos relacionados con la vegetación
- **Albedo** → afecta el equilibrio energético de la superficie

Cada una de estas entradas aporta un aspecto diferente de la variabilidad espacial en el modelo.

---

## Resumen

En HydroPol2D, LULC se trata como un mapa categórico utilizado para asignar parámetros relacionados con la superficie a través de tablas de búsqueda.
La calidad de la clasificación y la coherencia del mapeo de parámetros son fundamentales para representar con precisión la resistencia al flujo superficial, la generación de escorrentía y los efectos de la vegetación.