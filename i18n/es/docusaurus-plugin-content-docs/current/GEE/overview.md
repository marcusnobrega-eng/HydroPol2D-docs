---
title: HydroPol2D Mapas de entrada
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
Haga clic en **"Registrarse"** y regístrese usando una cuenta de Google.
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
- Capa global de asentamientos humanos para superficies urbanizadas

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
- Fracción media de superficie edificada

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

## Parámetros clave explicados

### Niveles HydroBASINS

HydroBASINS proporciona límites de cuencas hidrográficas en diferentes niveles jerárquicos (1-12), donde:
- **Nivel 1-3**: Cuencas fluviales continentales y principales
- **Nivel 4-6**: Grandes cuencas regionales (recomendado para estudios regionales)
- **Nivel 7-9**: Subcuencas (recomendadas para estudios locales/de cuencas)
- **Nivel 10-12**: Pequeñas cuencas de cabecera

**Cómo elegir**: Niveles más altos = cuencas de captación más pequeñas y detalladas. Para la mayoría de las aplicaciones, los niveles 6-8 proporcionan un buen equilibrio.

---

### Encontrar valores HYBAS_ID

Para identificar los valores `HYBAS_ID` para su área de estudio:
#### Opción 1: usar el editor de código GEE

- Cargue HydroBASINS en el editor de código
- Haga clic en cuencas de interés
- El `HYBAS_ID` aparece en el panel Inspector.

#### Opción 2: descargar el archivo de forma

- Visita [HydroSHEDS](https://www.hydrosheds.org/products/hydrobasins)
- Descargue el nivel apropiado para su región
- Abrir en QGIS/ArcGIS e identificar cuencas por atributos

#### Opción 3: visor interactivo

- Utilice el [visor HydroSHEDS](https://www.hydrosheds.org/hydroatlas)

**Ejemplo**: Para un estudio en el norte de California, puede seleccionar varias cuencas de captación de nivel 7 que desembocan en el río Sacramento.

---

### Elección de sistemas de referencia de coordenadas (CRS)

Seleccione un CRS apropiado para su región de estudio:
| Región | SRI recomendado | Código EPSG | Notas |
|--------|----------------|-----------|-------|
| California, Estados Unidos | Albers de California | `EPSG:3310` | Proyección de áreas iguales |
| Estados Unidos continental | Estados Unidos contiguos Albers | `EPSG:5070` | Estándar USGS |
| Global/Multirregión | WGS 84/UTM | `EPSG:326XX` | Reemplazar XX con zona |
| India | WGS 84 / UTM Zona 43N-45N | `EPSG:32643-32645` | Dependiendo de la longitud |
| Europa | ETRS89 LAEA | `EPSG:3035` | áreas iguales |

**Por qué es importante**: El uso de una proyección local minimiza las distorsiones de área/distancia y garantiza cálculos hidrológicos precisos.

---

### Configuración de la escala de exportación

El parámetro `scale_of_image` controla la resolución de salida:
- **30m**: Alto nivel de detalle, archivos de gran tamaño, procesamiento más prolongado
- **90m** (predeterminado): Buen equilibrio para estudios regionales
- **250m**: Procesamiento más rápido, archivos más pequeños, apropiados para dominios grandes
- **1000m**: Resolución gruesa para análisis a escala continental

**Recomendación**: Iguale o supere ligeramente la resolución de la cuadrícula computacional de su modelo.

---

### Rangos de fechas para datos que varían en el tiempo

El script calcula **valores medianos** durante el rango de tiempo especificado para:
- **Albedo** (MODIS MCD43A3)
- **LAI** (MODIS MCD15A3H)

**Elegir fechas**:
- Utilice períodos de 3 a 5 años para suavizar la variabilidad interanual
- Evite períodos con eventos extremos conocidos (a menos que los estudie)
- Ejemplo: `'2015-01-01'` a `'2020-01-01'` captura condiciones recientes y relativamente estables

---

## Fuentes de datos y resoluciones

### Conjuntos de datos de entrada

| Conjunto de datos | Fuente | Resolución nativa | Cobertura Temporal | Notas |
|---------|--------|------------------|-------------------|-------|
| **DEM** | MÉRITO DEM v1.0.3 | ~90m | Estático (década de 2000) | Elevación eliminada por error |
| **Uso de la tierra** | Portada mundial de la ESA | 10m | 2020, 2021 | 11 clases globales |
| **Textura del suelo** | OpenLandMap | 250m | Estático | Clases de textura del USDA |
| **Profundidad hasta el lecho de roca** | Conjunto de datos globales de suelos ORNL DAAC | 1 kilometro | Estático | Estimaciones derivadas de ML |
| **Albedo** | MODIS MCD43A3 | 500m | Diariamente desde 2000 | Onda corta de cielo negro |
| **LAI** | MODIS MCD15A3H | 500m | 4 días desde 2002 | Índice de área foliar |
| **Población** | pop mundial | 100m | Anual 2000-2020 | Estimación restringida |
| **Superficie construida** | Superficie edificada GHSL | 100m | 1975-2030 | Cobertura global |

---

### Clases de uso y cobertura del suelo (ESA WorldCover)

La salida LULC utiliza la siguiente clasificación:
| Valor | Clase | Descripción |
|-------|-------|-------------|
| 10 | Cobertura de árboles | Bosques, bosques |
| 20 | Matorral | Arbustos, arbustos |
| 30 | Pradera | Pastizales naturales |
| 40 | Tierras de cultivo | Zonas agrícolas |
| 50 | Construido | Asentamientos urbanos |
| 60 | Vegetación desnuda/escasa | Roca, arena, verduras escasas |
| 70 | Nieve y hielo | Nieve/hielo permanente |
| 80 | Cuerpos de agua | Ríos, lagos, océano. |
| 90 | Humedal herbáceo | Marismas, pantanos |
| 95 | Manglares | Bosques de manglares |
| 100 | musgo y liquen | Vegetación ártica/alpina |

---

### Clases de textura del suelo (USDA)

La salida SOIL contiene clases de textura USDA:
| Valor | Clase de textura | Descripción |
|-------|--------------|-------------|
| 1 | Arcilla | > 40% arcilla |
| 2 | Arcilla limosa | 40-60% limo, > 40% arcilla |
| 3 | Arcilla arenosa | < 45% sand, > 35% arcilla |
| 4 | franco arcilloso | 27-40% arcilla, 20-45% arena |
| 5 | Franco arcilloso limoso | 27-40% arcilla, < 20% arena |
| 6 | Franco arcilloso arenoso | 20-35% arcilla, > 45% arena |
| 7 | Marga | 7-27 % arcilla, equilibrio arena/limo |
| 8 | franco limoso | < 50% arena, 50-87% limo |
| 9 | franco arenoso | > 50% arena, 0-50% limo |
| 10 | Limo | > 80% limo |
| 11 | Arena franca | 70-90% arena |
| 12 | Arena | > 85% arena |

---

## Comprender los archivos de salida

### Salidas ráster (GeoTIFF)

Todos los archivos GeoTIFF comparten:
- **Valor sin datos**: `-9999`
- **Proyección**: Según lo especificado por `crs`
- **Resolución**: Según lo especificado por `scale_of_image`
- **Extensión**: Recortado al límite de la unión de cuencas

**Nombre de archivo**:
- `DEM.tif` – Elevación en metros
- `LULC.tif` – Códigos de clase de uso del suelo (10-100)
- `SOIL.tif` – Códigos de clase de textura del suelo (1-12)
- `DTB.tif` – Profundidad hasta el lecho de roca en metros
- `Albedo.tif` – Albedo de superficie (0-1, sin unidades)
- `LAI.tif` – Índice de área foliar (m²/m²)
- `WorldPop.tif` – Densidad de población (personas/píxel)

---

### Salida de archivo de forma

**Catchment_Union.shp** contiene:
- Límite fusionado de todas las cuencas seleccionadas
- Atributos originales HydroBASINS para cada subcuenca
- Se puede utilizar para:
  - Visualizar el dominio en SIG
  - Recortar conjuntos de datos adicionales
  - Definir los límites del modelo

---

### Salidas CSV

#### Domain_Log.csv

Resumen de una sola fila de todo el dominio de modelado:
| Columna | Descripción | Unidades |
|--------|-------------|-------|
| `folder_name` | Carpeta de exportación de Google Drive | - |
| `hybas_level` | Nivel HydroBASINS utilizado | - |
| `catchment_ids_used` | HYBAS_ID separados por punto y coma | - |
| `number_of_catchments` | Recuento de cuencas fusionadas | - |
| `catchment_area_km2` | Área total de dominio | km² |
| `population_in_domain` | Población total | personas |
| `mean_built_surface_percent` | Superficie media edificada | % |
| `dominant_LULC` | Clase de uso de suelo más común | código |
| `dominant_SOIL` | Clase de suelo más común | código |
| `avg_albedo` | Albedo medio de la superficie | 0-1 |
| `mean_elevation_m` | Elevación media | m |
| `mean_DTB_m` | Profundidad media al lecho de roca | m |
| `mean_LAI` | Índice de área foliar media | m²/m² |
| `worldpop_year` | Año de datos del WorldPop | año |
| `export_scale_m` | Resolución de exportación | m |
| `crs` | sistema de coordenadas | código EPSG |

---

#### Catchment_Log.csv

Estadísticas por cuenca con una fila por subcuenca:
| Columna | Descripción | Fuente |
|--------|-------------|--------|
| `HYBAS_ID` | Identificador único de cuenca | HydroBASINS |
| `MAIN_BAS` | ID de la cuenca principal | HydroBASINS |
| `NEXT_DOWN` | ID de cuenca aguas abajo | HydroBASINS |
| `UP_AREA` | Área de drenaje aguas arriba | km² |
| `SUB_AREA` | Zona de subcuenca | km² |
| `PFAF_ID` | código pfafstetter | HydroBASINS |
| `catchment_area_km2` | Área calculada | km² |
| `population` | Población total | personas |
| `mean_built_surface_percent` | superficie edificada | % |
| `dominant_LULC` | Uso de suelo dominante | código |
| `dominant_SOIL` | Clase de suelo dominante | código |
| `avg_albedo` | albedo medio | 0-1 |
| `mean_elevation_m` | Elevación media | m |
| `mean_DTB_m` | Profundidad media al lecho de roca | m |
| `mean_LAI` | Media LAI | m²/m² |

**Caso de uso**: comparar características de subcuencas, identificar patrones espaciales, validar entradas del modelo.

---

## Solución de problemas

### Problemas comunes

#### 1. Errores de memoria ("Se agotó el tiempo de cálculo")

**Solución**:
- Reducir el número de captaciones
- Aumentar `scale_stats_continuous` y `scale_stats_categorical`
- Exportar regiones más pequeñas por separado
- Utilice el parámetro `tileScale` en operaciones de reducción (ya implementado en el script)

---

#### 2. Acceso a profundidad hasta lecho rocoso (DTB)

La profundidad hasta la capa de lecho de roca proviene del conjunto de datos de suelos globales ORNL DAAC:
**Cita**: Pelletier, J.D., et al. (2016). Un conjunto de datos globales cuadriculados de suelos, regolitos intactos y espesores de depósitos sedimentarios para el modelado de la superficie terrestre regional y global. *Revista de avances en el modelado de sistemas terrestres*, 8(1), 41-65.

**Acceso**:
- Datos originales: [ORNL DAAC](https://daac.ornl.gov/SOILS/guides/Global_Soil_Regolith_Sediment.html)
- El script utiliza una versión preprocesada cargada en Google Earth Engine como recurso personalizado

**Si DTB no está disponible**:
- Póngase en contacto con los autores del script para acceder a los activos
- Utilice una profundidad alternativa al conjunto de datos de lecho de roca
- Comente la Sección 7 si no es necesaria para su solicitud.

---

## Código GEE
```javascript
//// ============================================================================
//// HYDROLOGICAL DATABASE EXPORT FOR UNION OF HYDROBASINS
//// Author........: Marcus Nobrega, PhD
//// Stanford University
//// Adapted.......: 2026
//// Purpose.......: Export DEM, LULC, SOIL, DTB, Albedo, LAI, and WorldPop for
////                 the union of multiple HydroBASINS catchments selected by HYBAS_ID.
////                 Also export:
////                   1) a domain summary CSV log
////                   2) a per-catchment CSV log with catchment IDs/attributes/stats
////
//// Notes:
//// - User specifies HydroBASINS level and a list of HYBAS_IDs
//// - Outputs are clipped to the union of selected catchments
//// - Filenames are simplified: DEM, LULC, SOIL, DTB, Albedo, LAI, WorldPop
//// - Summary logs are computed at coarser scale to avoid memory errors
//// ============================================================================


//// ============================================================================
//// SECTION 1: USER INPUTS
//// ============================================================================

// -----------------------------
// HydroBASINS level to use
// Examples: 7, 8, 9, ...
// -----------------------------
var hybasLevel = 6;

// -----------------------------
// List of HYBAS_ID values to merge
// Replace with your own IDs
// -----------------------------
var catchmentIds = [
  4060922650,
  4060953900,
  4060952550,
  4060954060
];


// -----------------------------
// Output folder name in Google Drive
// -----------------------------
var Folder_Name = 'Domain_India';

// -----------------------------
// Export scale (m) for rasters
// -----------------------------
var scale_of_image = 90;

// -----------------------------
// Coarser scales for summary logs
// -----------------------------
var scale_stats_continuous = 250;   // DEM, DTB, Albedo, LAI, Impervious
var scale_stats_categorical = 250;  // LULC, SOIL
var scale_stats_population = 100;   // WorldPop

// -----------------------------
// Date range for time-dependent datasets
// -----------------------------
var startDate = '2015-01-01';
var endDate   = '2020-01-01';

// -----------------------------
// WorldPop year
// Available in EE for 2000–2020
// -----------------------------
var worldpopYear = 2020;

// -----------------------------
// Output CRS
// Recommended for California:
//   EPSG:3310 = California Albers
// -----------------------------
var crs = 'EPSG:3310';

// -----------------------------
var noDataValue = -9999;
var mapZoom = 8;


//// ============================================================================
//// SECTION 2: LOAD HYDROBASINS AND BUILD UNION GEOMETRY
//// ============================================================================

// Build HydroBASINS asset path dynamically
var hybasPath = 'WWF/HydroSHEDS/v1/Basins/hybas_' + hybasLevel;

// Load HydroBASINS
var hybas = ee.FeatureCollection(hybasPath);

// Filter selected catchments
var catchments = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));

// Dissolve into a single feature/geometry
var catchmentUnion = catchments.union(1);

// Alternatively, you can enter the shapefile of your catchment
// Simply change the variable named CatchmentUnion to the catchment you need

var geometry = catchmentUnion.geometry();

// Display
Map.centerObject(catchmentUnion, mapZoom);
Map.addLayer(catchments, {color: 'yellow'}, 'Selected HydroBASINS');
Map.addLayer(catchmentUnion, {color: 'red'}, 'Union Catchment');

// Print basic info
print('HydroBASINS level:', hybasLevel);
print('Selected HYBAS_IDs:', catchmentIds);
print('Selected catchments:', catchments);
print('Union area (km²):', geometry.area(1).divide(1e6));


//// ============================================================================
//// SECTION 3: EXPORT UNION CATCHMENT SHAPEFILE
//// ============================================================================

Export.table.toDrive({
  collection: catchmentUnion,
  description: 'Catchment_Union',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Union',
  fileFormat: 'SHP'
});


//// ============================================================================
//// SECTION 4: DEM
//// Source: MERIT DEM
//// ============================================================================

var MERIT = ee.Image("MERIT/DEM/v1_0_3");
var DEM = MERIT.select('dem').rename('DEM').clip(geometry);

var demVis = {
  min: 0,
  max: 4000,
  palette: ['0000ff', '00ff00', 'ffff00', 'ff7f00', 'ff0000']
};

Map.addLayer(DEM, demVis, 'DEM');

Export.image.toDrive({
  image: DEM.unmask(noDataValue),
  description: 'DEM',
  folder: Folder_Name,
  fileNamePrefix: 'DEM',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 5: LULC
//// Source: ESA/WorldCover/v100/2020
//// ============================================================================

var LULC = ee.Image('ESA/WorldCover/v100/2020')
  .select('Map')
  .rename('LULC')
  .clip(geometry);

var lulcVis = {
  min: 10,
  max: 100,
  palette: [
    '#006400',
    '#ffbb22',
    '#ffff4c',
    '#f096ff',
    '#fa0000',
    '#b4b4b4',
    '#f0f0f0',
    '#0064c8',
    '#0096a0',
    '#00cf75',
    '#fae6a0'
  ]
};

Map.addLayer(LULC, lulcVis, 'LULC');

Export.image.toDrive({
  image: LULC.unmask(noDataValue),
  description: 'LULC',
  folder: Folder_Name,
  fileNamePrefix: 'LULC',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 6: SOIL
//// Source: OpenLandMap USDA texture class
//// ============================================================================

var SOIL = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
  .select('b0')
  .rename('SOIL')
  .clip(geometry);

var soilVis = {
  min: 1,
  max: 12,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(SOIL, soilVis, 'SOIL');

Export.image.toDrive({
  image: SOIL.unmask(noDataValue),
  description: 'SOIL',
  folder: Folder_Name,
  fileNamePrefix: 'SOIL',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 7: DEPTH TO BEDROCK (DTB)
//// Source: custom asset
//// ============================================================================

var DTB = ee.Image("projects/ee-marcusep2025/assets/Depth_to_bedrock")
  .rename('DTB')
  .clip(geometry);

var dtbVis = {
  min: 1,
  max: 50,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(DTB, dtbVis, 'DTB');

Export.image.toDrive({
  image: DTB.unmask(noDataValue),
  description: 'DTB',
  folder: Folder_Name,
  fileNamePrefix: 'DTB',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 8: ALBEDO
//// Source: MODIS/061/MCD43A3
//// ============================================================================

var albedoCollection = ee.ImageCollection("MODIS/061/MCD43A3")
  .select('Albedo_BSA_shortwave')
  .filterDate(startDate, endDate);

var Albedo = albedoCollection
  .median()
  .multiply(0.001)
  .rename('Albedo')
  .clip(geometry);

var albedoVis = {
  min: 0,
  max: 0.5,
  palette: ['blue', 'white', 'yellow', 'red']
};

Map.addLayer(Albedo, albedoVis, 'Albedo');

Export.image.toDrive({
  image: Albedo.unmask(noDataValue),
  description: 'Albedo',
  folder: Folder_Name,
  fileNamePrefix: 'Albedo',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 9: LEAF AREA INDEX (LAI)
//// Source: MODIS/061/MCD15A3H
//// Notes:
//// - MODIS LAI scaled by 0.1
//// - Median value over user-defined time range
//// ============================================================================

var laiCollection = ee.ImageCollection('MODIS/061/MCD15A3H')
  .select('Lai')
  .filterDate(startDate, endDate);

var LAI = laiCollection
  .median()
  .multiply(0.1)
  .rename('LAI')
  .clip(geometry);

var laiVis = {
  min: 0,
  max: 6,
  palette: ['red', 'yellow', 'green']
};

Map.addLayer(LAI, laiVis, 'LAI');

Export.image.toDrive({
  image: LAI.unmask(noDataValue),
  description: 'LAI',
  folder: Folder_Name,
  fileNamePrefix: 'LAI',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 10: WORLDPOP
//// Source: WorldPop/GP/100m/pop
//// ============================================================================

var WorldPop = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.calendarRange(worldpopYear, worldpopYear, 'year'))
  .mosaic()
  .rename('WorldPop')
  .clip(geometry);

Map.addLayer(WorldPop, {
  min: 0,
  max: 100,
  palette: ['white', 'yellow', 'orange', 'red', 'darkred']
}, 'WorldPop ' + worldpopYear);

Export.image.toDrive({
  image: WorldPop.unmask(noDataValue),
  description: 'WorldPop',
  folder: Folder_Name,
  fileNamePrefix: 'WorldPop',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 11: IMPERVIOUS RATE (for logs only)
//// Source: NLCD impervious (U.S.-only; appropriate for California)
//// ============================================================================

var Impervious = ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
  .select('impervious')
  .median()
  .rename('Impervious')
  .clip(geometry);

Map.addLayer(Impervious, {
  min: 0,
  max: 100,
  palette: ['white', 'pink', 'red', 'darkred']
}, 'Impervious (%)');


//// ============================================================================
//// SECTION 12: HELPER FUNCTIONS FOR STATS (MEMORY-SAFE)
//// ============================================================================

function reduceMean(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceSum(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceMode(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function safeProp(feature, propName) {
  var props = feature.propertyNames();
  return ee.Algorithms.If(props.contains(propName), feature.get(propName), null);
}


//// ============================================================================
//// SECTION 13: DOMAIN SUMMARY LOG (CSV)
//// ============================================================================

var totalPopulation = reduceSum(WorldPop, geometry, scale_stats_population);
var meanImpervious = reduceMean(Impervious, geometry, scale_stats_continuous);
var area_km2 = geometry.area(1).divide(1e6);
var nCatchments = catchments.size();
var dominantLULC = reduceMode(LULC, geometry, scale_stats_categorical);
var dominantSOIL = reduceMode(SOIL, geometry, scale_stats_categorical);
var meanAlbedo = reduceMean(Albedo, geometry, scale_stats_continuous);
var meanElevation = reduceMean(DEM, geometry, scale_stats_continuous);
var meanDTB = reduceMean(DTB, geometry, scale_stats_continuous);
var meanLAI = reduceMean(LAI, geometry, scale_stats_continuous);

// Store catchment IDs as a string for traceability
var catchmentIdsString = ee.List(catchmentIds).join(';');

// Build one-row feature
var domainLogFeature = ee.Feature(null, {
  'folder_name': Folder_Name,
  'hybas_level': hybasLevel,
  'catchment_ids_used': catchmentIdsString,
  'number_of_catchments': nCatchments,
  'catchment_area_km2': area_km2,
  'population_in_domain': totalPopulation,
  'mean_impervious_rate_percent': meanImpervious,
  'dominant_LULC': dominantLULC,
  'dominant_SOIL': dominantSOIL,
  'avg_albedo': meanAlbedo,
  'mean_elevation_m': meanElevation,
  'mean_DTB_m': meanDTB,
  'mean_LAI': meanLAI,
  'worldpop_year': worldpopYear,
  'export_scale_m': scale_of_image,
  'crs': crs
});

var domainLogTable = ee.FeatureCollection([domainLogFeature]);

print('Domain summary log:', domainLogTable);

Export.table.toDrive({
  collection: domainLogTable,
  description: 'Domain_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Domain_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 14: PER-CATCHMENT LOG (CSV)
//// ============================================================================

var catchmentLogTable = catchments.map(function(ft) {
  var g = ft.geometry();
  var areaLocal_km2 = g.area(1).divide(1e6);

  var domLULC_local = reduceMode(LULC, g, scale_stats_categorical);
  var domSOIL_local = reduceMode(SOIL, g, scale_stats_categorical);
  var meanAlb_local = reduceMean(Albedo, g, scale_stats_continuous);
  var meanDEM_local = reduceMean(DEM, g, scale_stats_continuous);
  var meanDTB_local = reduceMean(DTB, g, scale_stats_continuous);
  var meanLAI_local = reduceMean(LAI, g, scale_stats_continuous);
  var pop_local = reduceSum(WorldPop, g, scale_stats_population);
  var imp_local = reduceMean(Impervious, g, scale_stats_continuous);

  return ee.Feature(null, {
    'HYBAS_ID': safeProp(ft, 'HYBAS_ID'),
    'MAIN_BAS': safeProp(ft, 'MAIN_BAS'),
    'NEXT_DOWN': safeProp(ft, 'NEXT_DOWN'),
    'UP_AREA': safeProp(ft, 'UP_AREA'),
    'SUB_AREA': safeProp(ft, 'SUB_AREA'),
    'PFAF_ID': safeProp(ft, 'PFAF_ID'),
    'ENDO': safeProp(ft, 'ENDO'),
    'COAST': safeProp(ft, 'COAST'),
    'catchment_area_km2': areaLocal_km2,
    'population': pop_local,
    'mean_impervious_rate_percent': imp_local,
    'dominant_LULC': domLULC_local,
    'dominant_SOIL': domSOIL_local,
    'avg_albedo': meanAlb_local,
    'mean_elevation_m': meanDEM_local,
    'mean_DTB_m': meanDTB_local,
    'mean_LAI': meanLAI_local
  });
});

print('Per-catchment log:', catchmentLogTable);

Export.table.toDrive({
  collection: catchmentLogTable,
  description: 'Catchment_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 15: OPTIONAL PRINTED SUMMARY
//// ============================================================================

function computeMeanPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mean:', stats);
}

function computeSumPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' sum:', stats);
}

function computeModePrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mode:', stats);
}

computeMeanPrint(DEM, 'DEM', scale_stats_continuous);
computeModePrint(LULC, 'LULC', scale_stats_categorical);
computeModePrint(SOIL, 'SOIL', scale_stats_categorical);
computeMeanPrint(DTB, 'DTB', scale_stats_continuous);
computeMeanPrint(Albedo, 'Albedo', scale_stats_continuous);
computeMeanPrint(LAI, 'LAI', scale_stats_continuous);
computeMeanPrint(Impervious, 'Impervious (%)', scale_stats_continuous);
computeSumPrint(WorldPop, 'Total WorldPop', scale_stats_population);

## GEE Code
```javascript
//// ================================================================================
//// EXPORTACIÓN DE BASE DE DATOS HYDROLOGICAL PARA LA UNIÓN DE HIDROBACINAS
//// Autor.........: Marcus Nobrega, PhD
//// Universidad Stanford
//// Adaptado.......: 2026
//// Propósito.......: Exportar DEM, LULC, SOIL, DTB, Albedo, LAI y WorldPop para
//// la unión de múltiples cuencas HydroBASINS seleccionadas por HYBAS_ID.
//// Exportar también:
//// 1) un registro CSV de resumen del dominio
//// 2) un registro CSV por cuenca con ID/atributos/estadísticas de la cuenca
////
//// Notas:
//// - El usuario especifica el nivel HydroBASINS y una lista de HYBAS_ID
//// - Las salidas se recortan a la unión de cuencas seleccionadas
//// - Los nombres de los archivos están simplificados: DEM, LULC, SOIL, DTB, Albedo, LAI, WorldPop
//// - Los registros de resumen se calculan a una escala más aproximada para evitar errores de memoria
//// ================================================================================

//// ================================================================================
//// SECCIÓN 1: ENTRADAS DEL USUARIO
//// ================================================================================
// -----------------------
// Nivel HydroBASINS a utilizar
// Ejemplos: 7, 8, 9, ...
// -----------------------
var hybasNivel = 6;
// -----------------------
// Lista de valores HYBAS_ID para fusionar
// Reemplazar con sus propios ID
// -----------------------
var captaciónIds = [
  4060922650,
  4060953900,
  4060952550,
  4060954060
];

// -----------------------
// Nombre de la carpeta de salida en Google Drive
// -----------------------
var Folder_Name = 'Dominio_India';
// -----------------------
// Escala de exportación (m) para rásteres
// -----------------------
var escala_de_imagen = 90;
// -----------------------
// Escalas más gruesas para registros resumidos
// -----------------------
var scale_stats_continuous = 250;   // DEM, DTB, Albedo, LAI, Impermeable
var scale_stats_categorical = 250;  // LULC, SUELO
var escala_stats_población = 100;   // pop mundial
// -----------------------
// Intervalo de fechas para conjuntos de datos dependientes del tiempo
// -----------------------
var fecha de inicio = '2015-01-01';
var fecha final = '2020-01-01';
// -----------------------
// Año mundial del pop
// Disponible en EE para 2000-2020
// -----------------------
var worldpopAño = 2020;
// -----------------------
// Salida CRS
// Recomendado para California:
// EPSG:3310 = Albers de California
// -----------------------
var crs = 'EPSG:3310';
// -----------------------
var noDataValue = -9999;
var mapaZoom = 8;

//// ================================================================================
//// SECCIÓN 2: CARGAR HIDROBASINAS Y CONSTRUIR GEOMETRÍA DE UNIÓN
//// ================================================================================
// Construye dinámicamente la ruta del activo HydroBASINS
var hybasPath = 'WWF/HydroSHEDS/v1/Basins/hybas_' + hybasLevel;
// Carga HydroBASINS
var hybas = ee.FeatureCollection(hybasPath);
// Filtrar cuencas seleccionadas
var captaciones = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));
// Disolver en una sola característica/geometría
var catchmentUnion = catchments.union(1);
// Alternativamente, puedes ingresar el archivo de forma de tu cuenca
// Simplemente cambia la variable llamada CatchmentUnion a la cuenca que necesitas
var geometría = catchmentUnion.geometry();
// Mostrar
Map.centerObject(catchmentUnion, mapZoom);
Map.addLayer(captaciones, {color: 'yellow'}, 'HydroBASINS seleccionado');
Map.addLayer(catchmentUnion, {color: 'red'}, 'Union Catchment');
// Imprimir información básica
print('HydroBASINS nivel:', hybasLevel);
print('HYBAS_ID seleccionados:', catchmentIds);
print('Cuencas seleccionadas:', cuencas);
print('Área de unión (km²):', geometría.area(1).divide(1e6));

//// ================================================================================
//// SECCIÓN 3: SHAPEFILE CATCHMENT DE LA UNIÓN DE EXPORTACIÓN
//// ================================================================================
Exportar.table.toDrive({
  colección: catchmentUnion,
  descripción: 'Unión_captación',
  carpeta: Nombre_carpeta,
  fileNamePrefix: 'Catchment_Union',
  Formato de archivo: 'SHP'
});

//// ================================================================================
//// SECCIÓN 4: DEM
//// Fuente: MÉRITO DEM
//// ================================================================================
var MÉRITO = ee.Image("MÉRITO/DEM/v1_0_3");
var DEM = MERIT.select('dem').rename('DEM').clip(geometría);
var demVis = {
  mín: 0,
  máx: 4000,
  paleta: ['0000ff', '00ff00', 'ffff00', 'ff7f00', 'ff0000']
};
Map.addLayer(DEM, demVis, 'DEM');
Exportar.imagen.aDrive({
  imagen: DEM.unmask(noDataValue),
  descripción: 'DEM',
  carpeta: Nombre_carpeta,
  PrefijoNombreDeArchivo: 'DEM',
  región: geometría,
  escala: escala_de_imagen,
  crs: crs,
  opciones de formato: {noData: noDataValue},
  maxPixels: 1e13
});

//// ================================================================================
//// SECCIÓN 5: LULC
//// Fuente: ESA/WorldCover/v100/2020
//// ================================================================================
var LULC = ee.Image('ESA/WorldCover/v100/2020')
  .select('Mapa')
  .renombrar('LULC')
  .clip(geometría);
var lulcVis = {
  mín.: 10,
  máx: 100,
  paleta: [
    '#006400',
    '#ffbb22',
    '#ffff4c',
    '#f096ff',
    '#fa0000',
    '#b4b4b4',
    '#f0f0f0',
    '#0064c8',
    '#0096a0',
    '#00cf75',
    '#fae6a0'
  ]
};
Map.addLayer(LULC, lulcVis, 'LULC');
Exportar.imagen.aDrive({
  imagen: LULC.unmask(noDataValue),
  descripción: 'LULC',
  carpeta: Nombre_carpeta,
  PrefijoNombreDeArchivo: 'LULC',
  región: geometría,
  escala: escala_de_imagen,
  crs: crs,
  opciones de formato: {noData: noDataValue},
  maxPixels: 1e13
});

//// ================================================================================
//// SECCIÓN 6: SUELO
//// Fuente: clase de textura OpenLandMap USDA
//// ================================================================================
var SUELO = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
  .select('b0')
  .rename('SUELO')
  .clip(geometría);
var sueloVis = {
  mín.: 1,
  máx: 12,
  paleta: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};
Map.addLayer(SUELO, sueloVis, 'SUELO');
Exportar.imagen.aDrive({
  imagen: SUELO.unmask(noDataValue),
  descripción: 'SUELO',
  carpeta: Nombre_carpeta,
  fileNamePrefix: 'SUELO',
  región: geometría,
  escala: escala_de_imagen,
  crs: crs,
  opciones de formato: {noData: noDataValue},
  maxPixels: 1e13
});

//// ================================================================================
//// SECCIÓN 7: PROFUNDIDAD DEL LECHO DE ROCA (DTB)
//// Fuente: activo personalizado
//// ================================================================================
var DTB = ee.Image("proyectos/ee-marcusep2025/assets/Depth_to_bedrock")
  .renombrar('DTB')
  .clip(geometría);
var dtbVis = {
  mín.: 1,
  máx: 50,
  paleta: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};
Map.addLayer(DTB, dtbVis, 'DTB');
Exportar.imagen.aDrive({
  imagen: DTB.unmask(noDataValue),
  descripción: 'DTB',
  carpeta: Nombre_carpeta,
  PrefijoNombreDeArchivo: 'DTB',
  región: geometría,
  escala: escala_de_imagen,
  crs: crs,
  opciones de formato: {noData: noDataValue},
  maxPixels: 1e13
});

//// ================================================================================
//// SECCIÓN 8: ALBEDO
//// Fuente: MODIS/061/MCD43A3
//// ================================================================================
var albedoCollection = ee.ImageCollection("MODIS/061/MCD43A3")
  .select('Albedo_BSA_ondacorta')
  .filterDate(fecha de inicio, fecha de finalización);
var Albedo = colección albedo
  .mediana()
  .multiplicar(0.001)
  .renombrar('Albedo')
  .clip(geometría);
var albedoVis = {
  mín: 0,
  máx: 0,5,
  paleta: ['azul', 'blanco', 'amarillo', 'rojo']
};
Map.addLayer(Albedo, albedoVis, 'Albedo');
Exportar.imagen.aDrive({
  imagen: Albedo.unmask (noDataValue),
  descripción: 'Albedo',
  carpeta: Nombre_carpeta,
  fileNamePrefix: 'Albedo',
  región: geometría,
  escala: escala_de_imagen,
  crs: crs,
  opciones de formato: {noData: noDataValue},
  maxPixels: 1e13
});

//// ================================================================================
//// SECCIÓN 9: ÍNDICE DEL ÁREA DE LA HOJA (LAI)
//// Fuente: MODIS/061/MCD15A3H
//// Notas:
//// - MODIS LAI escalado en 0,1
//// - Valor medio durante el rango de tiempo definido por el usuario
//// ================================================================================
var laiCollection = ee.ImageCollection('MODIS/061/MCD15A3H')
  .select('Lai')
  .filterDate(fecha de inicio, fecha de finalización);
var LAI = laiCollection
  .mediana()
  .multiplicar(0.1)
  .renombrar('LAI')
  .clip(geometría);
var laiVis = {
  mín: 0,
  máx: 6,
  paleta: ['rojo', 'amarillo', 'verde']
};
Map.addLayer(LAI, laiVis, 'LAI');
Exportar.imagen.aDrive({
  imagen: LAI.unmask(noDataValue),
  descripción: 'LAI',
  carpeta: Nombre_carpeta,
  PrefijoNombreDeArchivo: 'LAI',
  región: geometría,
  escala: escala_de_imagen,
  crs: crs,
  opciones de formato: {noData: noDataValue},
  maxPixels: 1e13
});

//// ================================================================================
//// SECCIÓN 10: POP MUNDIAL
//// Fuente: WorldPop/GP/100m/pop
//// ================================================================================
var WorldPop = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.calendarRange(worldpopYear, worldpopYear, 'año'))
  .mosaico()
  .rename('MundoPop')
  .clip(geometría);
Map.addLayer(WorldPop, {
  mín: 0,
  máx: 100,
  paleta: ['blanco', 'amarillo', 'naranja', 'rojo', 'rojo oscuro']
}, 'WorldPop ' + worldpopYear);
Exportar.imagen.aDrive({
  imagen: WorldPop.unmask (noDataValue),
  descripción: 'WorldPop',
  carpeta: Nombre_carpeta,
  fileNamePrefix: 'WorldPop',
  región: geometría,
  escala: escala_de_imagen,
  crs: crs,
  opciones de formato: {noData: noDataValue},
  maxPixels: 1e13
});

//// ================================================================================
//// SECCIÓN 11: TARIFA IMPERMEABLE (solo para registros)
//// Fuente: NLCD impermeable (solo EE. UU.; apropiado para California)
//// ================================================================================
var Impermeable = ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
  .select('impermeable')
  .mediana()
  .rename('Impermeable')
  .clip(geometría);
Map.addLayer(Impermeable, {
  mín: 0,
  máx: 100,
  paleta: ['blanco', 'rosa', 'rojo', 'rojo oscuro']
}, 'Impermeable (%)');

//// ================================================================================
//// SECCIÓN 12: FUNCIONES DE AYUDA PARA ESTADÍSTICAS (MEMORIA SEGURA)
//// ================================================================================
función reducirMedia(imagen, geom, escala) {
  var banda = ee.String(image.bandNames().get(0));
  var fuera = imagen.reduceRegión({
    reductor: ee.Reducer.mean(),
    geometría: geom,
    escala: escala,
    maxPixels: 1e13,
    mejor esfuerzo: verdadero,
    BaldosaEscala: 4
  });
  return out.get(banda);
}
función reducirSuma(imagen, geom, escala) {
  var banda = ee.String(image.bandNames().get(0));
  var fuera = imagen.reduceRegión({
    reductor: ee.Reducer.sum(),
    geometría: geom,
    escala: escala,
    maxPixels: 1e13,
    mejor esfuerzo: verdadero,
    BaldosaEscala: 4
  });
  return out.get(banda);
}
función reducirModo(imagen, geom, escala) {
  var banda = ee.String(image.bandNames().get(0));
  var fuera = imagen.reduceRegión({
    reductor: ee.Reducer.mode(),
    geometría: geom,
    escala: escala,
    maxPixels: 1e13,
    mejor esfuerzo: verdadero,
    BaldosaEscala: 4
  });
  return out.get(banda);
}
function safeProp(característica, propName) {
  var props = característica.propertyNames();
  return ee.Algorithms.If(props.contains(propName), feature.get(propName), null);
}

//// ================================================================================
//// SECCIÓN 13: REGISTRO DE RESUMEN DE DOMINIO (CSV)
//// ================================================================================
var población total = reducirSum(WorldPop, geometría, escala_stats_población);
var meanImpervious = reduceMean(Impermeable, geometría, scale_stats_continuous);
var area_km2 = geometría.area(1).divide(1e6);
var nCatchments = capturas.size();
var dominanteLULC = reduceMode(LULC, geometría, escala_stats_categorical);
var dominanteSOIL = reduceMode(SUELO, geometría, escala_stats_categorical);
var meanAlbedo = reduceMean(Albedo, geometría, escala_stats_continuous);
var meanElevation = reduceMean(DEM, geometría, scale_stats_continuous);
var meanDTB = reduceMean(DTB, geometría, scale_stats_continuous);
var meanLAI = reduceMean(LAI, geometría, scale_stats_continuous);
// Almacena los ID de las cuencas como una cadena para su trazabilidad
var catchmentIdsString = ee.List(catchmentIds).join(';');
// Construir característica de una fila
var domainLogFeature = ee.Feature(nulo, {
  'nombre_carpeta': Nombre_carpeta,
  'hybas_level': hybasLevel,
  'catchment_ids_used': catchmentIdsString,
  'número_de_captaciones': nCaptaciones,
  'catchment_area_km2': área_km2,
  'población_en_dominio': población total,
  'mean_impervious_rate_percent': meanImpervious,
  'dominante_LULC': dominanteLULC,
  'SUELO_dominante': SUELO dominante,
  'avg_albedo': significaAlbedo,
  'mean_elevation_m': mediaElevación,
  'media_DTB_m': mediaDTB,
  'mean_LAI': significaLAI,
  'worldpop_year': añopopmundial,
  'export_scale_m': escala_de_imagen,
  'crs': crs
});
var domainLogTable = ee.FeatureCollection([domainLogFeature]);
print('Registro de resumen de dominio:', domainLogTable);
Exportar.table.toDrive({
  colección: domainLogTable,
  descripción: 'Domain_Log',
  carpeta: Nombre_carpeta,
  fileNamePrefix: 'Domain_Log',
  Formato de archivo: 'CSV'
});

//// ================================================================================
//// SECCIÓN 14: REGISTRO PER-CATCHMENT (CSV)
//// ================================================================================
var catchmentLogTable = captaciones.map(función(pies) {
  var g = pies.geometría();
  var areaLocal_km2 = g.area(1).divide(1e6);
var domLULC_local = reduceMode(LULC, g, scale_stats_categorical);
  var domSOIL_local = reduceMode(SUELO, g, scale_stats_categorical);
  var meanAlb_local = reduceMean(Albedo, g, scale_stats_continuous);
  var meanDEM_local = reduceMean(DEM, g, scale_stats_continuous);
  var meanDTB_local = reduceMean(DTB, g, scale_stats_continuous);
  var meanLAI_local = reduceMean(LAI, g, scale_stats_continuous);
  var pop_local = reduceSum(WorldPop, g, scale_stats_population);
  var imp_local = reduceMean(Impermeable, g, scale_stats_continuous);
return ee.Feature(nulo, {
    'HYBAS_ID': safeProp(pies, 'HYBAS_ID'),
    'MAIN_BAS': safeProp(pies, 'MAIN_BAS'),
    'NEXT_DOWN': safeProp(ft, 'NEXT_DOWN'),
    'UP_AREA': safeProp(pies, 'UP_AREA'),
    'SUB_AREA': safeProp(pies, 'SUB_AREA'),
    'PFAF_ID': safeProp(ft, 'PFAF_ID'),
    'ENDO': safeProp(pies, 'ENDO'),
    'COSTA': safeProp(ft, 'COSTA'),
    'catchment_area_km2': áreaLocal_km2,
    'población': pop_local,
    'mean_impervious_rate_percent': imp_local,
    'dominante_LULC': domLULC_local,
    'SOIL_dominante': domSOIL_local,
    'avg_albedo': meanAlb_local,
    'media_elevación_m': mediaDEM_local,
    'media_DTB_m': mediaDTB_local,
    'media_LAI': mediaLAI_local
  });
});
print('Registro por cuenca:', catchmentLogTable);
Exportar.table.toDrive({
  colección: catchmentLogTable,
  descripción: 'Catchment_Log',
  carpeta: Nombre_carpeta,
  fileNamePrefix: 'Catchment_Log',
  Formato de archivo: 'CSV'
});

//// ================================================================================
//// SECCIÓN 15: RESUMEN IMPRESO OPCIONAL
//// ================================================================================
función calcularMeanPrint(imagen, nombre, escala) {
  var estadísticas = imagen.reduceRegión({
    reductor: ee.Reducer.mean(),
    geometría: geometría,
    escala: escala,
    maxPixels: 1e13,
    mejor esfuerzo: verdadero,
    BaldosaEscala: 4
  });
  print(nombre + 'significa:', estadísticas);
}
función ComputeSumPrint(imagen, nombre, escala) {
  var estadísticas = imagen.reduceRegión({
    reductor: ee.Reducer.sum(),
    geometría: geometría,
    escala: escala,
    maxPixels: 1e13,
    mejor esfuerzo: verdadero,
    BaldosaEscala: 4
  });
  print(nombre + 'suma:', estadísticas);
}
función ComputeModePrint (imagen, nombre, escala) {
  var estadísticas = imagen.reduceRegión({
    reductor: ee.Reducer.mode(),
    geometría: geometría,
    escala: escala,
    maxPixels: 1e13,
    mejor esfuerzo: verdadero,
    BaldosaEscala: 4
  });
  print(nombre + 'modo:', estadísticas);
}
ComputeMeanPrint(DEM, 'DEM', scale_stats_continuous);
ComputeModePrint(LULC, 'LULC', scale_stats_categorical);
ComputeModePrint(SUELO, 'SUELO', scale_stats_categorical);
ComputeMeanPrint(DTB, 'DTB', scale_stats_continuous);
ComputeMeanPrint(Albedo, 'Albedo', scale_stats_continuous);
ComputeMeanPrint(LAI, 'LAI', scale_stats_continuous);
ComputeMeanPrint(Impermeable, 'Impermeable (%)', scale_stats_continuous);
ComputeSumPrint(WorldPop, 'Total WorldPop', scale_stats_population);