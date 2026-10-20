---
title: DEM
---

# Modelo de elevación digital (DEM)

El Modelo de Elevación Digital (DEM) define la estructura topográfica del dominio de simulación y es el control principal de la dinámica del flujo superficial en HydroPol2D.
Es una de las entradas más críticas del modelo, ya que gobierna los gradientes del terreno, las direcciones del flujo y la organización espacial de los procesos hidrológicos.

---

## Papel en HydroPol2D

El DEM se utiliza para calcular:
- Elevación de la superficie en todo el dominio.
- Las pendientes locales impulsan la ruta del flujo
- Conectividad de flujo entre celdas de la red.
- Límites de cuencas y patrones de drenaje

Debido a que HydroPol2D opera en una cuadrícula ráster, DEM también define la malla computacional en la que se simulan todos los procesos de superficie.

---

## Conjuntos de datos DEM disponibles

Varios conjuntos de datos DEM globales de alta calidad están disponibles gratuitamente y son adecuados para aplicaciones HydroPol2D:
### SRTM (Misión de Topografía de Radar Shuttle)
- Resolución: ~30 m (1 segundo de arco)
- Cobertura: Casi global (±60° de latitud)
- Ampliamente utilizado y de fácil acceso.
- Puede contener vegetación y artefactos urbanos.
- Descargar: https://earthexplorer.usgs.gov/

---

### Copérnico DEM (GLO-30 / GLO-90)
- Resolución: 30 m y 90 m
- Conjunto de datos globales de alta calidad
- Consistencia mejorada y menos huecos que SRTM
- Recomendado para aplicaciones generales.
- Descargar: https://spacedata.copernicus.eu/

---

### FABDEM (Bosque y edificios eliminados DEM)
- Resolución: ~30 m
- Derivado de Copérnico DEM
- Se eliminaron los sesgos de vegetación y construcción.
- Particularmente útil para el modelado hidrológico.
- Descargar: https://data.bris.ac.uk/data/dataset/25wfy0f9ukoge2gs7a5mqpq2j7

---

### MÉRITO DEM
- Resolución: ~90 m
- DEM global con reducción de errores
- Corregido por múltiples sesgos (rayas, ruido, efectos de vegetación)
- Adecuado para simulaciones a gran escala
- Descargar: http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/

---

### USGS 3DEP (Programa de elevación 3D)
- Región: Estados Unidos
- Resolución: 1 m a 10 m (dependiendo de la ubicación)
- Incluye DEM derivados de LiDAR de alta resolución
- Una de las mejores fuentes de estudios realizados en EE. UU.
- Descargar: https://apps.nationalmap.gov/downloader/

---

## Datos de alta resolución (recomendado)

Si están disponibles, se recomienda encarecidamente **DEM basados ​​en LiDAR**.

Ventajas:
- Resolución espacial muy alta (de submetro a unos pocos metros)
- Representación precisa del terreno y la microtopografía.
- Mejor representación de rutas de flujo, canales y características urbanas.

Estos conjuntos de datos son particularmente valiosos para:
- Modelización de inundaciones urbanas
- Pequeñas cuencas
- Análisis hidráulico detallado

### Datos LiDAR (Estados Unidos)

Se puede acceder a los datos LiDAR para EE. UU. a través de:
- USGS Mapa Nacional (3DEP): https://apps.nationalmap.gov/downloader/
- Costa digital NOAA: https://coast.noaa.gov/dataviewer/#/lidar/search/

Estas plataformas brindan acceso a conjuntos de datos de elevación de alta resolución derivados de estudios aéreos LiDAR.

---

## Requisitos del sistema de coordenadas

El DEM **debe estar en un sistema de referencia de coordenadas proyectadas (CRS)**.
- Las coordenadas geográficas (latitud/longitud) **no se admiten**
- Las unidades deben estar en **metros**
- Las distancias y pendientes deben ser físicamente significativas.

Todas las demás entradas ráster (LULC, Suelo, DTB, LAI, Albedo) deben:
- Utilice el **mismo CRS**
- Tener la **misma resolución espacial**
- Compartir la **misma extensión espacial**

---

## Definición y enmascaramiento de dominio

En la práctica, es posible que los rásteres de entrada no se superpongan perfectamente.
HydroPol2D maneja esto mediante:
- Definición de un **dominio común mínimo**
- Crear una máscara donde **todos los rásteres requeridos sean válidos**
- Restringir las simulaciones a este dominio consistente

Esto asegura:
- No faltan datos durante la simulación
- Acoplamiento consistente entre procesos
- Estabilidad numérica

---

## Remuestreo y alineación

Si los rásteres de entrada no están alineados, HydroPol2D proporciona una **opción de remuestreo**.
Cuando se activa la bandera de remuestreo:
- El DEM se interpola automáticamente para que coincida con la cuadrícula del modelo.
- **Se utiliza interpolación bilineal**

Esto permite a los usuarios:
- Integre conjuntos de datos con diferentes resoluciones
- Evite el preprocesamiento manual en el software SIG

Sin embargo, los usuarios aún deben asegurarse de que:
- El remuestreo no introduce artefactos
- La resolución sigue siendo adecuada para la escala de simulación.

---

## Recomendaciones de preprocesamiento

Antes de utilizar un DEM, los usuarios deben:
- Compruebe si hay valores faltantes o vacíos
- Eliminar ruido o artefactos
- Garantizar una alineación adecuada con otros rásteres
- Verificar CRS y unidades
- Evaluar si es necesario suavizar o filtrar

En algunos casos, se puede aplicar relleno o acondicionamiento de depresión dependiendo de los objetivos del modelado.

---

## Uso de DEM frente a DSM en diferentes aplicaciones

Se debe tener cuidado al seleccionar el tipo de modelo de elevación dependiendo del enfoque de modelado.
Para **simulaciones de lluvia en red**, donde la lluvia se aplica directamente sobre todo el dominio, se recomienda utilizar un **DEM** de tierra desnuda. Los modelos digitales de superficie (DSM), que incluyen edificios y otras estructuras elevadas, pueden introducir pendientes y barreras artificiales que no son consistentes con los supuestos de la formulación inercial local. Los bordes de la construcción pueden generar gradientes poco realistas que conducen a un comportamiento de flujo no físico.
Por el contrario, para **simulaciones fluviales** impulsadas por hidrogramas de afluencia en los límites del dominio, los DSM se pueden utilizar para representar mejor las características urbanas, siempre que las profundidades del agua simuladas permanezcan físicamente consistentes y no excedan las elevaciones de los edificios.
Por lo tanto:
- **Aplicaciones de lluvia sobre red** → use **tierra desnuda DEM**
- **Aplicaciones fluviales/basadas en límites** → DSM se puede utilizar con cuidado

---

## Resumen

El DEM proporciona la base geométrica e hidráulica de las simulaciones HydroPol2D.
Su resolución, precisión y coherencia con otras entradas influyen directamente en el rendimiento del modelo, la estabilidad numérica y el realismo físico.
La selección cuidadosa y el preprocesamiento del DEM son esenciales para obtener resultados de simulación confiables.
