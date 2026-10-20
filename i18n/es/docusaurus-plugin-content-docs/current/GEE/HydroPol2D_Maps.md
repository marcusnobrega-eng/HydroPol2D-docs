---
title: Descripción general
---

# Caracterización de cuencas con Google Earth Engine

HydroPol2D incluye un script Google Earth Engine (GEE) para generar los conjuntos de datos espaciales necesarios para definir un dominio de modelado hidrológico.
El flujo de trabajo extrae, procesa y exporta múltiples variables ambientales de conjuntos de datos geoespaciales alojados en la nube, produciendo un conjunto consistente de entradas ráster y tablas de resumen para una cuenca o grupo de cuencas seleccionadas.

---

## Accediendo a Google Earth Engine

Para utilizar este flujo de trabajo, los usuarios deben tener acceso a Google Earth Engine.
### 1. Crea una cuenta

Ir a:
https://earthengine.google.com/
Haga clic en **“Registrarse”** y regístrese usando una cuenta de Google.
La aprobación suele ser automática para uso académico o de investigación, pero puede llevar algún tiempo según la solicitud.

---

### 2. Abra el editor de código

Una vez concedido el acceso, abra el editor de código GEE:
https://code.earthengine.google.com/
Este es el entorno donde se ejecuta el script.

---

### 3. Agregue el script HydroPol2D

Copie el código JavaScript proporcionado en el Editor de código y ejecútelo directamente en el navegador.
El script utiliza la API de Earth Engine para acceder a conjuntos de datos, realizar operaciones espaciales y exportar resultados a Google Drive.

---

## Qué hace el flujo de trabajo

El script construye un dominio de modelado a partir de cuencas hidrográficas HydroBASINS y genera una base de datos estandarizada de capas ráster y estadísticas resumidas.
Los principales resultados incluyen:
### Conjuntos de datos ráster

- Modelo de elevación digital (DEM)
- Uso del suelo / Cobertura del suelo (LULC)
- Clase de textura del suelo
- Profundidad hasta el lecho de roca (DTB)
- Albedo superficial
- Índice de área foliar (LAI)
- Densidad de población (WorldPop)

Todos los rásteres son:
- Recortado al dominio seleccionado
- Exportado con una resolución espacial consistente
- Reproyectado a un sistema de coordenadas definido por el usuario.
- Se le asigna un valor común sin datos

---

### Salidas vectoriales y tabulares

El script también genera:
- Un archivo de forma del dominio de cuenca fusionado
- Una tabla de resumen a nivel de dominio (CSV)
- Una tabla resumen por cuenca (CSV)

Estos resultados proporcionan metadatos y estadísticas agregadas para el área de estudio.

---

## Estructura general del flujo de trabajo

El código sigue una secuencia estructurada:
### 1. Entradas definidas por el usuario

El usuario especifica:
- Nivel HydroBASINS (por ejemplo, 6, 7, 8)
- Lista de valores `HYBAS_ID`
- Nombre de la carpeta de salida
- Resolución espacial (escala de exportación)
- Sistema de referencia de coordenadas (CRS)
- Rango de tiempo para conjuntos de datos dependientes del tiempo
- Año para datos de población

Estos parámetros controlan la definición del dominio y el procesamiento del conjunto de datos.

---

### 2. Selección y fusión de cuencas

El script carga polígonos HydroBASINS y los filtra utilizando los valores `HYBAS_ID` seleccionados.
Las cuencas seleccionadas se fusionan en una única geometría, que define el dominio de modelado.

---

### 3. Construcción de dominio

La geometría fusionada se utiliza para:
- Recortar todos los datasets ráster
- Definir los límites de exportación
- Calcular estadísticas resumidas
- Exportar el límite de la cuenca como un archivo de forma

---

### 4. Recuperación y procesamiento de conjuntos de datos

El script accede a múltiples conjuntos de datos disponibles en Google Earth Engine, que incluyen:
- MERIT DEM para topografía
- ESA WorldCover para el uso de la tierra
- OpenLandMap para clases de suelo
- Productos MODIS para albedo y LAI
- WorldPop para la densidad de población

Para conjuntos de datos que dependen del tiempo (por ejemplo, albedo y LAI), el script calcula los valores medianos en el rango de tiempo seleccionado.

---

### 5. Exportación de capas ráster

Cada conjunto de datos es:
- Recortado al dominio
- Estandarizados en resolución y proyección.
- Exportado a Google Drive como GeoTIFF

---

### 6. Cálculo de estadísticas resumidas.

El script calcula métricas a nivel de dominio como:
- Área total
- Elevación media
- Profundidad media al lecho de roca
- Media LAI y albedo
- Uso dominante de la tierra y clase de suelo
- Población total
- Fracción impermeable media

Se genera una segunda tabla con las mismas métricas calculadas individualmente para cada cuenca.

---

## Estructura de salida

Todos los resultados se guardan en la carpeta especificada de Google Drive e incluyen:
- Mapas ráster (GeoTIFF)
- Archivo de forma de captación (SHP)
- Tabla resumen de dominio (CSV)
- Tabla resumen por cuenca (CSV)

Estos archivos se pueden utilizar directamente como entradas para HydroPol2D o procesarse posteriormente en entornos SIG o de modelado.

---

## Próximos pasos

Las siguientes secciones describen cómo configurar el script y exportar cada conjunto de datos paso a paso.