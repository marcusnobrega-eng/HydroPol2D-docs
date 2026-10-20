---
title: GPM IMERG Extracción de datos de lluvia
---

# Descargando GPM IMERG Lluvia con Google Earth Engine

Este script independiente Google Earth Engine (GEE) automatiza la extracción de datos de lluvia satelitales de alta resolución del conjunto de datos IMERG GPM (Medición de precipitación global) de NASA para cualquier cuenca en todo el mundo.
El flujo de trabajo genera rásteres GeoTIFF individuales para cada paso de tiempo, listos para el modelado hidrológico con HydroPol2D u otros modelos distribuidos.

---

## Qué hace el flujo de trabajo

El script descarga datos de precipitación de **GPM IMERG V07** (Recuperaciones multisatélite integradas para GPM), el producto de precipitación global de última generación de NASA que combina observaciones de múltiples sensores satelitales.
### Características clave

- **Resolución nativa de 30 minutos**: captura la variabilidad de las precipitaciones subhorarias, crucial para el modelado de inundaciones repentinas.
- **Cobertura global**: 60°N-60°S (cubre las regiones más pobladas del mundo)
- **Resolución espacial de 0,1°**: Aproximadamente 11 km en el ecuador
- **Registro largo**: desde junio de 2000 hasta casi tiempo real (actualizado con un retraso de aproximadamente 3 meses)
- **Datos calibrados**: utiliza estimaciones de precipitación ajustadas por medidor
- **Múltiples resoluciones temporales**: agregadas por hora, cada 3 horas, cada 6 horas o diariamente
- **Entrada de cuenca flexible**: Funciona con HydroBASINS o archivos de forma personalizados

---

## Especificaciones de salida

### Propiedades de ráster

| Propiedad | Valor |
|----------|-------|
| **Resolución** | 0,1° × 0,1° (aproximadamente 11 km en el ecuador) |
| **Unidades** | mm/h (tasa de precipitación) |
| **Formato** | geoTIFF |
| **Sistema de coordenadas** | EPSG: 4326 (WGS84) de forma predeterminada |
| **Sin valor de datos** | -9999 |
| **Región de exportación** | Cuadro delimitador de captación |

### Convención de nombre de archivo

El script genera nombres de archivos descriptivos que codifican información temporal:
**Datos de 30 minutos**:- GPM_30min_2023_01_14_00_00.tif
- GPM_30min_2023_01_14_00_30.tif
- GPM_30min_2023_01_14_01_00.tif

**Agregación horaria**:- GPM_60min_2023_01_14_00_00.tif
- GPM_60min_2023_01_14_01_00.tif
- GPM_60min_2023_01_14_02_00.tif

**Agregación cada 3 horas** (misma resolución temporal que MSWEP):- GPM_180min_2023_01_14_00_00.tif
- GPM_180min_2023_01_14_03_00.tif
- GPM_180min_2023_01_14_06_00.tif

**Agregación diaria**:- GPM_1440min_2023_01_14_00_00.tif
- GPM_1440min_2023_01_15_00_00.tif
- GPM_1440min_2023_01_16_00_00.tif

---

## Cómo utilizar el guión

### Paso 1: Defina su área de estudio

**Opción A: uso de HydroBASINS** (recomendado para la mayoría de los usuarios)
Modifique estos parámetros en el script:- Establecer useHydroBASINS en verdadero
- Elija el nivel HydroBASINS (1-12, donde más alto equivale a cuencas más pequeñas)
- Ingrese su(s) ID de cuenca en la lista de ID de cuenca

Recomendaciones de nivel:- Nivel 5-6: Grandes cuencas fluviales (mayores que 10,000 km²)
- Nivel 7: Cuencas medias (1,000-5,000 km²)
- Nivel 8-9: Pequeñas cuencas (100-1,000 km²)

**Encontrar su HYBAS_ID**:1. Visite el sitio web HydroSHEDS o utilice la herramienta Inspector de GEE
2. Cargue HydroBASINS en el nivel deseado en Google Earth Engine
3. Haga clic en su cuenca con la herramienta Inspector
4. Copie el valor HYBAS_ID

**Opción B: uso de Shapefile personalizado**
Si tiene su propio archivo de forma de captación:1. Cargue el archivo de forma en los activos GEE (Activo → Nuevo → Archivos de forma)
2. Establezca useHydroBASINS en falso en el script
3. Descomente y modifique la línea customCatchment con la ruta de su activo

---

### Paso 2: establecer el rango de fechas

Especifique el evento de lluvia o el período de estudio que desea descargar.
**Formato**: AAAA-MM-DD
**Notas importantes**:- GPM IMERG V07 disponible desde el **1 de junio de 2000** hasta casi en tiempo real
- Normalmente hay un retraso de 3 meses para el producto final.
- Para eventos cortos (de días a semanas): use una resolución de 30 minutos
- Para períodos largos (meses a años): considere resoluciones agregadas

**Configuraciones de ejemplo**:- **Evento de inundación repentina**: 2-3 días con una resolución de 30 minutos
- **Simulación mensual**: 30 días con resolución horaria o de 3 horas
- **Análisis estacional**: 90 días con resolución de 3 horas o diaria
- **Balance hídrico anual**: 365 días a resolución diaria

---

### Paso 3: elija la resolución temporal

Seleccione el paso de tiempo (en minutos) para sus resultados de lluvia.
| Resolución | Minutos | Archivos por día | Caso de uso típico |
|------------|---------|---------------|------------------|
| **30 minutos** | 30 | 48 | Inundaciones repentinas, drenaje urbano, tormentas cortas |
| **Cada hora** | 60 | 24 | Modelado basado en eventos, análisis detallado de tormentas. |
| **cada 3 horas** | 180 | 8 | Eventos de varios días, simulaciones a medio plazo. |
| **cada 6 horas** | 360 | 4 | Simulaciones semanales a mensuales. |
| **cada 12 horas** | 720 | 2 | Análisis climático a largo plazo |
| **A diario** | 1440 | 1 | Balance hídrico, análisis estacional/anual. |

**Ejemplos de recuento de archivos**:- Evento de 2 días a 30 min: 96 archivos (aproximadamente 200 MB)
- 1 mes por hora: 720 archivos (aproximadamente 1,5 GB)
- 1 mes a 3 horas: 240 archivos (aproximadamente 500 MB)
- 1 año al día: 365 archivos (aproximadamente 750 MB)

**Método de agregación**: para resoluciones temporales superiores a 30 minutos, el script calcula la **tasa de precipitación media** durante el período de agregación, preservando las unidades mm/h.

---

### Paso 4: configurar los ajustes de salida

**Carpeta de salida**: especifique el nombre de la carpeta de Google Drive donde se guardarán los archivos. El script creará esta carpeta si no existe.
**Sistema de coordenadas**: manténgalo como EPSG:4326 (WGS84) para la proyección nativa GPM o especifique una proyección local (por ejemplo, zonas UTM, plano estatal) para su región.
Proyecciones comunes:- EPSG:4326 - WGS84 (global, recomendado para GPM)
- EPSG:3310 - Albers de California
- EPSG:32610 - Zona UTM 10N (California)
- EPSG: 32643 - Zona UTM 43N (India)

---

### Paso 5: ejecute el script

1. **Copia el script completo** de la sección de códigos a continuación
2. **Abrir Google Earth Engine** Editor de código
3. **Pegue el script** en un nuevo archivo de script
4. **Modificar las entradas del usuario** (Sección 1)
5. **Ejecute el script** (haga clic en el botón Ejecutar o presione Ctrl+Entrar)
6. **Espera a que se procese**: la consola mostrará el progreso.
7. **Vaya a la pestaña Tareas** (panel derecho)
8. **Haga clic en EJECUTAR** en cada tarea de exportación
9. **Espere a que se completen las exportaciones**: los archivos aparecen en Google Drive

**Tiempo de procesamiento**:- Envío de tareas: 10-30 segundos
- Exportación por archivo: 1-5 minutos (depende del tamaño de la cuenca)
- Tiempo total: varía según la cantidad de archivos

---

## Comprender los resultados

### Cuadro delimitador frente a captación exacta

El script exporta datos de lluvia para el **cuadro delimitador rectangular** alrededor de su cuenca, no la forma exacta de la cuenca.
**¿Por qué?**- Procesamiento más rápido
- Mantiene la estructura de cuadrícula regular GPM
- Proporciona contexto para áreas adyacentes.
- HydroPol2D y la mayoría de los modelos hidrológicos pueden ajustarse a límites exactos durante el procesamiento

**Si necesita un recorte exacto de la cuenca de captación**: el archivo de forma de la cuenca de captación exportado se puede utilizar para recortar rásteres en el software SIG o durante el preprocesamiento del modelo.

---

### Archivos incluidos en la exportación

**Rásteres de lluvia**:- Un GeoTIFF por paso de tiempo
- El nombre del archivo incluye fecha y hora.
- Unidades: mm/h (tasa de precipitación)

**Límite de cuenca**:- Shapefile (.shp + archivos de soporte)
- Mismo sistema de coordenadas que los rásteres de lluvia
- Úselo para recortar o visualizar

---

### Seguro de calidad

El script incluye capas de visualización en el mapa:- **Polígono rojo**: Límite de cuenca fusionado
- **Rectángulo azul**: Exportar cuadro delimitador
- **Capa de lluvia de muestra**: visualización del primer paso
- **Capa de lluvia total**: Precipitación acumulada durante todo el período

**Salidas de consola**:- Área de captación en kilómetros cuadrados
- Número de imágenes de 30 minutos disponibles
- Confirmación del rango de fechas
- Exportar estado de envío de tarea
- Estadísticas de precipitaciones totales

---

## Consideraciones de datos

### GPM IMERG Fortalezas

- **Alta resolución temporal**: observaciones de 30 minutos
- **Cobertura global**: datos consistentes en todo el mundo
- **Registro largo**: más de 20 años de datos
- **Calibración de pluviómetros**: precisión mejorada en regiones con redes de pluviómetros
- **Fusión multisensor**: combina datos pasivos de microondas, infrarrojos y radar

### GPM IMERG Limitaciones

- **Resolución espacial**: 11 km pueden ser aproximados para cuencas pequeñas (menos de 100 kilómetros cuadrados)
- **Latencia**: aproximadamente 3 meses de retraso para el producto calibrado final (V07)
- **Incertidumbre**: menor precisión sobre océanos, montañas y nieve/hielo
- **Sesgo**: se puede subestimar o sobreestimar en ciertas regiones (especialmente en terrenos complejos)
- **Brechas de cobertura**: 60°N-60°S únicamente (sin regiones polares)

### Recomendaciones de validación

**Siempre valide GPM con observaciones locales cuando estén disponibles**:- Comparar con los datos del pluviómetro
- Comparar con estimaciones de radar
- Verificar acumulaciones totales
- Evaluar patrones espaciales

Para aplicaciones críticas, considere:- Corrección de sesgo utilizando datos de calibre local.
- Enfoques conjuntos con múltiples conjuntos de datos
- Cuantificación de la incertidumbre

---

## Aplicaciones

Este flujo de trabajo está diseñado para:
### Modelización hidrológica
- HydroPol2D Simulación distribuida de lluvia-escorrentía
- Previsión de inundaciones repentinas
- Análisis de drenaje urbano.
- Estudios de balance hídrico.

### Análisis de eventos
- Caracterización de tormentas
- Análisis de intensidad-duración-frecuencia de las precipitaciones.
- Reconstrucción de eventos extremos
- Análisis histórico de inundaciones

### Estudios climáticos
- Tendencias de precipitación a largo plazo
- Patrones de lluvia estacionales
- Monitoreo de sequía
- Validación de modelos climáticos

### Recursos hídricos
- Estimación del flujo de entrada al yacimiento
- Planificación del riego
- Evaluación de energía hidroeléctrica
- Estudios de disponibilidad de agua

---

## Solución de problemas

### Problemas comunes

**Error "Capacidad de memoria excedida"**:- Reduzca el rango de fechas (pruebe con períodos de tiempo más pequeños)
- Aumentar la resolución temporal (p. ej., usar diariamente en lugar de 30 minutos)
- Reducir el tamaño de la cuenca (use un nivel HydroBASINS más pequeño)

**No hay datos en rásteres exportados**:- El rango de fechas de verificación está dentro del período GPM (2000-06-01 en adelante)
- Verifique que la cuenca esté dentro de la cobertura GPM (60°N-60°S)
- Confirmar que el ID de la cuenca es correcto

**Las exportaciones no aparecen en Tareas**:- Espere entre 10 y 30 segundos después de ejecutar el script
- Verifique la consola para ver mensajes de error
- Actualizar pestaña Tareas

**Tamaños de archivos muy grandes**:- Considere utilizar resolución temporal agregada
- Exportar rangos de fechas más pequeños
- Utilice la resolución espacial adecuada para su aplicación

---

## Recursos adicionales

- [Sitio web de la misión GPM](https://gpm.nasa.gov/)
- [GPM IMERG Documentación técnica](https://gpm.nasa.gov/data/imerg)
- [Documentación Google Earth Engine](https://developers.google.com/earth-engine)
- [Base de datos HydroBASINS](https://www.hydrosheds.org/products/hydrobasins)
- [Modelo HydroPol2D](https://marcusnobrega-eng.github.io/HydroPol2D-docs/)

---

## Apoyo

Para problemas con:- **El guión**: contacta a tu equipo de soporte
- **Datos GPM**: Visite la mesa de ayuda de GES DISC o GPM
- **Google Earth Engine**: Consulte el foro de desarrolladores GEE
- **HydroPol2D**: Visite el sitio web de documentación del modelo

---

## Historial de versiones

- **v1.0** (2026): Versión inicial con soporte GPM IMERG V07
  - Resoluciones temporales de 30 minutos a diarias
  - HydroBASINS y compatibilidad con archivos de forma personalizados
  - Generación automática de tareas
  - Visualizaciones de control de calidad

---

## Código GEE
```javascript
//// ============================================================================
//// GPM IMERG V07 RAINFALL DOWNLOADER - STANDALONE
//// Author........: Marcus Nobrega
//// Date..........: 2026
//// Purpose.......: Download GPM IMERG V07 rainfall data for any catchment
//// Resolution....: 0.1° × 0.1° (native, ~11 km at equator)
//// Units.........: mm/h (precipitation rate)
//// Data Range....: June 2000 - Present (near real-time)
//// ============================================================================


//// ============================================================================
//// SECTION 1: USER INPUTS - MODIFY THESE PARAMETERS
//// ============================================================================

// =============================================================================
// OPTION 1: Use HydroBASINS Catchment
// =============================================================================
// HydroBASINS level: 1-12 (higher = smaller catchments)
// Level 7 = medium-sized catchments (~1000-5000 km²)
// Level 8 = smaller catchments (~200-1000 km²)
var useHydroBASINS = true;  // Set to true to use HydroBASINS
var hybasLevel = 7;         // HydroBASINS level (1-12)

// List of HYBAS_ID values to download rainfall for
// You can find HYBAS_IDs by:
// 1. Going to: https://www.hydrosheds.org/hydrobasins
// 2. Or using the Inspector tool in GEE to click on catchments
var catchmentIds = [
  7071457620  // Example: San Francisco Bay Area catchment
];

// =============================================================================
// OPTION 2: Use Your Own Shapefile (uploaded to GEE Assets)
// =============================================================================
// Uncomment the line below and comment out the HydroBASINS section if using custom shapefile
// var useHydroBASINS = false;
// var customCatchment = ee.FeatureCollection('users/yourusername/your_catchment_shapefile');

// =============================================================================
// Date Range for Rainfall Download
// =============================================================================
// Format: 'YYYY-MM-DD'
// GPM IMERG V07 available from: 2000-06-01 to near real-time
var gpmStartDate = '2023-01-01';  // Start date
var gpmEndDate   = '2023-01-31';  // End date

// =============================================================================
// Temporal Resolution (in minutes)
// =============================================================================
// Choose ONE of the following options:
//   30    = Native 30-minute resolution (best for short periods: days/weeks)
//   60    = Hourly (good for weeks/months)
//   180   = 3-hourly (same as MSWEP, good for months)
//   360   = 6-hourly (good for long periods)
//   720   = 12-hourly
//   1440  = Daily (good for years)
var gpmTemporalResolution = 360;  // Minutes

// =============================================================================
// Output Settings
// =============================================================================
// Google Drive folder name where files will be saved
var outputFolder = 'GPM_SanFrancisco';

// Coordinate Reference System (CRS)
// Recommended: Keep as 'EPSG:4326' (WGS84 lat/lon) for GPM data
// For local projections, use appropriate EPSG code (e.g., 'EPSG:32610' for UTM Zone 10N California)
var outputCRS = 'EPSG:4326';

// No data value for exported rasters
var noDataValue = -9999;

// =============================================================================
// Visualization Settings
// =============================================================================
var mapZoom = 9;  // Initial map zoom level


//// ============================================================================
//// SECTION 2: LOAD CATCHMENT GEOMETRY
//// ============================================================================

var catchmentUnion;
var geometry;

if (useHydroBASINS) {
  // Build HydroBASINS asset path
  var hybasPath = 'WWF/HydroSHEDS/v1/Basins/hybas_' + hybasLevel;

  // Load HydroBASINS and filter by HYBAS_ID
  var hybas = ee.FeatureCollection(hybasPath);
  var catchments = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));

  // Dissolve into single geometry
  catchmentUnion = catchments.union(1);
  geometry = catchmentUnion.geometry();

  print('Using HydroBASINS Level:', hybasLevel);
  print('Selected HYBAS_IDs:', catchmentIds);
  print('Number of catchments:', catchments.size());

} else {
  // Use custom shapefile
  catchmentUnion = customCatchment;
  geometry = catchmentUnion.geometry();

  print('Using custom catchment shapefile');
}

// Create bounding box for export (not clipped - for HydroPol2D compatibility)
var bounds = geometry.bounds();

// Display on map
Map.centerObject(geometry, mapZoom);
Map.addLayer(geometry, {color: 'red'}, 'Catchment');
Map.addLayer(bounds, {color: 'blue'}, 'Export Bounds');

// Print catchment info
print('============================================');
print('CATCHMENT INFORMATION');
print('============================================');
print('Catchment area (km²):', geometry.area(1).divide(1e6));
print('Export bounds:', bounds.coordinates());


//// ============================================================================
//// SECTION 3: LOAD GPM IMERG V07 RAINFALL DATA
//// ============================================================================

print('============================================');
print('GPM IMERG V07 CONFIGURATION');
print('============================================');
print('Date range:', gpmStartDate, 'to', gpmEndDate);
print('Temporal resolution:', gpmTemporalResolution, 'minutes');

// Load GPM IMERG V07 collection
// The 'precipitation' band contains calibrated precipitation rate in mm/h
var gpmCollection = ee.ImageCollection('NASA/GPM_L3/IMERG_V07')
  .select('precipitation')
  .filterDate(gpmStartDate, gpmEndDate)
  .filterBounds(bounds);

print('Total 30-min images available:', gpmCollection.size());

// Native GPM resolution: 0.1 degree ≈ 11132 meters at equator
var gpmNativeScale = 11132;


//// ============================================================================
//// SECTION 4: EXPORT RAINFALL RASTERS
//// ============================================================================

// -----------------------------
// OPTION A: Native 30-minute resolution
// -----------------------------
if (gpmTemporalResolution === 30) {

  print('============================================');
  print('EXPORTING 30-MINUTE RAINFALL');
  print('============================================');
  print('Units: mm/h (precipitation rate)');
  print('Resolution: 0.1° (~11 km)');
  print('Filename format: GPM_30min_yyyy_mm_dd_hh_mm.tif');
  print('Output folder:', outputFolder);

  // Get collection as list
  var gpmList = gpmCollection.toList(gpmCollection.size());
  var numImages = gpmCollection.size();

  // Create export tasks for each image
  numImages.evaluate(function(n) {
    print('Creating', n, 'export tasks...');

    for (var i = 0; i < n; i++) {
      (function(index) {
        var img = ee.Image(gpmList.get(index));
        var date = ee.Date(img.get('system:time_start'));

        // Format date as yyyy_mm_dd_hh_mm
        date.format('yyyy_MM_dd_HH_mm').evaluate(function(dateStr) {
          var exportName = 'GPM_30min_' + dateStr;

          Export.image.toDrive({
            image: img.unmask(noDataValue).float(),
            description: exportName,
            folder: outputFolder,
            fileNamePrefix: exportName,
            region: bounds,
            scale: gpmNativeScale,
            crs: outputCRS,
            formatOptions: {noData: noDataValue},
            maxPixels: 1e13
          });
        });
      })(i);
    }

    print('✓ All export tasks submitted!');
    print('✓ Go to Tasks tab (right panel) to run exports');
    print('✓ Each file contains precipitation rate in mm/h');
  });

}

// -----------------------------
// OPTION B: Aggregated temporal resolution
// -----------------------------
else {

  print('============================================');
  print('EXPORTING', gpmTemporalResolution, 'MINUTE RAINFALL');
  print('============================================');
  print('Units: mm/h (mean precipitation rate)');
  print('Resolution: 0.1° (~11 km)');

  var resStr = gpmTemporalResolution.toString();
  print('Filename format: GPM_' + resStr + 'min_yyyy_mm_dd_hh_mm.tif');
  print('Output folder:', outputFolder);

  // Calculate aggregation parameters
  var intervalsPerPeriod = gpmTemporalResolution / 30;
  print('30-min intervals per output:', intervalsPerPeriod);

  // Time period calculations
  var startMillis = ee.Date(gpmStartDate).millis();
  var endMillis = ee.Date(gpmEndDate).millis();
  var millisPerPeriod = gpmTemporalResolution * 60 * 1000;
  var numPeriods = endMillis.subtract(startMillis).divide(millisPerPeriod).floor();

  var periods = ee.List.sequence(0, numPeriods.subtract(1));

  // Create aggregated collection
  var aggregatedCollection = ee.ImageCollection(periods.map(function(p) {
    var periodStart = ee.Date(startMillis.add(ee.Number(p).multiply(millisPerPeriod)));
    var periodEnd = periodStart.advance(gpmTemporalResolution, 'minute');

    var periodImages = gpmCollection.filterDate(periodStart, periodEnd);

    // Mean precipitation rate over period (still in mm/h)
    var aggregated = periodImages
      .mean()
      .rename('precipitation')
      .set('system:time_start', periodStart.millis())
      .set('period_start', periodStart.format('yyyy-MM-dd HH:mm'))
      .set('period_end', periodEnd.format('yyyy-MM-dd HH:mm'))
      .set('temporal_resolution_min', gpmTemporalResolution)
      .set('units', 'mm/h');

    return aggregated;
  }));

  print('Number of aggregated images:', aggregatedCollection.size());

  // Get collection as list
  var aggList = aggregatedCollection.toList(aggregatedCollection.size());
  var numAggImages = aggregatedCollection.size();

  // Create export tasks for each aggregated image
  numAggImages.evaluate(function(n) {
    print('Creating', n, 'export tasks...');

    for (var i = 0; i < n; i++) {
      (function(index) {
        var img = ee.Image(aggList.get(index));
        var date = ee.Date(img.get('system:time_start'));

        // Format date as yyyy_mm_dd_hh_mm
        date.format('yyyy_MM_dd_HH_mm').evaluate(function(dateStr) {
          var exportName = 'GPM_' + resStr + 'min_' + dateStr;

          Export.image.toDrive({
            image: img.unmask(noDataValue).float(),
            description: exportName,
            folder: outputFolder,
            fileNamePrefix: exportName,
            region: bounds,
            scale: gpmNativeScale,
            crs: outputCRS,
            formatOptions: {noData: noDataValue},
            maxPixels: 1e13
          });
        });
      })(i);
    }

    print('✓ All export tasks submitted!');
    print('✓ Go to Tasks tab (right panel) to run exports');
    print('✓ Each file contains mean precipitation rate in mm/h');
  });
}


//// ============================================================================
//// SECTION 5: VISUALIZATION
//// ============================================================================

// Visualize first rainfall image
var sampleGPM = ee.Image(gpmCollection.first());

Map.addLayer(sampleGPM, {
  min: 0,
  max: 10,
  palette: ['white', 'lightblue', 'blue', 'darkblue', 'purple', 'red']
}, 'Sample Rainfall (mm/h)');

// Calculate and visualize total rainfall over period
var totalRainfall = gpmCollection.sum().multiply(0.5);  // mm (30-min * mm/h = mm/0.5hr)

Map.addLayer(totalRainfall.clip(geometry), {
  min: 0,
  max: 200,
  palette: ['white', 'lightblue', 'blue', 'darkblue', 'purple', 'red']
}, 'Total Rainfall (mm)');

// Print statistics
print('============================================');
print('RAINFALL STATISTICS');
print('============================================');
print('Sample image date:', ee.Date(sampleGPM.get('system:time_start')));

var stats = totalRainfall.reduceRegion({
  reducer: ee.Reducer.minMax().combine(ee.Reducer.mean(), '', true),
  geometry: geometry,
  scale: gpmNativeScale,
  maxPixels: 1e13,
  bestEffort: true
});

print('Total rainfall over period (mm):', stats);


//// ============================================================================
//// SECTION 6: EXPORT CATCHMENT BOUNDARY
//// ============================================================================

// Export catchment shapefile for reference
Export.table.toDrive({
  collection: catchmentUnion,
  description: 'Catchment_Boundary',
  folder: outputFolder,
  fileNamePrefix: 'Catchment_Boundary',
  fileFormat: 'SHP'
});

print('============================================');
print('EXPORT SUMMARY');
print('============================================');
print('✓ Rainfall rasters configured for export');
print('✓ Catchment boundary shapefile configured');
print('✓ Go to Tasks tab to start downloads');
print('============================================');