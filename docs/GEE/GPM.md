---
title: GPM IMERG Rainfall Data Extraction
---

# Downloading GPM IMERG Rainfall with Google Earth Engine

This standalone Google Earth Engine (GEE) script automates the extraction of high-resolution satellite rainfall data from NASA's GPM (Global Precipitation Measurement) IMERG dataset for any catchment worldwide.

The workflow generates individual GeoTIFF rasters for each time step, ready for hydrological modeling with HydroPol2D or other distributed models.

---

## What the workflow does

The script downloads precipitation data from **GPM IMERG V07** (Integrated Multi-satellitE Retrievals for GPM), NASA's state-of-the-art global precipitation product that combines observations from multiple satellite sensors.

### Key Features

- **Native 30-minute resolution**: Captures sub-hourly rainfall variability crucial for flash flood modeling
- **Global coverage**: 60°N-60°S (covers most populated regions worldwide)
- **0.1° spatial resolution**: Approximately 11 km at the equator
- **Long record**: June 2000 to near real-time (updated with approximately 3-month lag)
- **Calibrated data**: Uses gauge-adjusted precipitation estimates
- **Multiple temporal resolutions**: Aggregate to hourly, 3-hourly, 6-hourly, or daily
- **Flexible catchment input**: Works with HydroBASINS or custom shapefiles

---

## Output Specifications

### Raster Properties

| Property | Value |
|----------|-------|
| **Resolution** | 0.1° × 0.1° (approximately 11 km at equator) |
| **Units** | mm/h (precipitation rate) |
| **Format** | GeoTIFF |
| **Coordinate System** | EPSG:4326 (WGS84) by default |
| **NoData Value** | -9999 |
| **Export Region** | Bounding box of catchment |

### Filename Convention

The script generates descriptive filenames encoding temporal information:

**30-minute data**:
- GPM_30min_2023_01_14_00_00.tif
- GPM_30min_2023_01_14_00_30.tif
- GPM_30min_2023_01_14_01_00.tif

**Hourly aggregation**:
- GPM_60min_2023_01_14_00_00.tif
- GPM_60min_2023_01_14_01_00.tif
- GPM_60min_2023_01_14_02_00.tif

**3-hourly aggregation** (same temporal resolution as MSWEP):
- GPM_180min_2023_01_14_00_00.tif
- GPM_180min_2023_01_14_03_00.tif
- GPM_180min_2023_01_14_06_00.tif

**Daily aggregation**:
- GPM_1440min_2023_01_14_00_00.tif
- GPM_1440min_2023_01_15_00_00.tif
- GPM_1440min_2023_01_16_00_00.tif

---

## How to Use the Script

### Step 1: Define Your Study Area

**Option A - Using HydroBASINS** (recommended for most users)

Modify these parameters in the script:
- Set useHydroBASINS to true
- Choose HydroBASINS level (1-12, where higher equals smaller catchments)
- Enter your catchment ID(s) in the catchmentIds list

Level recommendations:
- Level 5-6: Large river basins (greater than 10,000 km²)
- Level 7: Medium catchments (1,000-5,000 km²)
- Level 8-9: Small catchments (100-1,000 km²)

**Finding your HYBAS_ID**:
1. Visit the HydroSHEDS website or use GEE's Inspector tool
2. Load HydroBASINS at your desired level in Google Earth Engine
3. Click on your catchment with the Inspector tool
4. Copy the HYBAS_ID value

**Option B - Using Custom Shapefile**

If you have your own catchment shapefile:
1. Upload shapefile to GEE Assets (Asset → New → Shape files)
2. Set useHydroBASINS to false in the script
3. Uncomment and modify the customCatchment line with your asset path

---

### Step 2: Set Date Range

Specify the rainfall event or study period you want to download.

**Format**: YYYY-MM-DD

**Important notes**:
- GPM IMERG V07 available from **June 1, 2000** to near real-time
- There is typically a 3-month lag for the final product
- For short events (days to weeks): use 30-minute resolution
- For long periods (months to years): consider aggregated resolutions

**Example configurations**:
- **Flash flood event**: 2-3 days at 30-minute resolution
- **Monthly simulation**: 30 days at hourly or 3-hourly resolution
- **Seasonal analysis**: 90 days at 3-hourly or daily resolution
- **Annual water balance**: 365 days at daily resolution

---

### Step 3: Choose Temporal Resolution

Select the time step (in minutes) for your rainfall outputs.

| Resolution | Minutes | Files per Day | Typical Use Case |
|------------|---------|---------------|------------------|
| **30-min** | 30 | 48 | Flash floods, urban drainage, short storm events |
| **Hourly** | 60 | 24 | Event-based modeling, detailed storm analysis |
| **3-hourly** | 180 | 8 | Multi-day events, medium-term simulations |
| **6-hourly** | 360 | 4 | Weekly to monthly simulations |
| **12-hourly** | 720 | 2 | Long-term climate analysis |
| **Daily** | 1440 | 1 | Water balance, seasonal/annual analysis |

**File count examples**:
- 2-day event at 30-min: 96 files (approximately 200 MB)
- 1-month at hourly: 720 files (approximately 1.5 GB)
- 1-month at 3-hourly: 240 files (approximately 500 MB)
- 1-year at daily: 365 files (approximately 750 MB)

**Aggregation method**: For temporal resolutions greater than 30 minutes, the script calculates the **mean precipitation rate** over the aggregation period, preserving mm/h units.

---

### Step 4: Configure Output Settings

**Output folder**: Specify the Google Drive folder name where files will be saved. The script will create this folder if it doesn't exist.

**Coordinate system**: Keep as EPSG:4326 (WGS84) for GPM native projection, or specify a local projection (e.g., UTM zones, State Plane) for your region.

Common projections:
- EPSG:4326 - WGS84 (global, recommended for GPM)
- EPSG:3310 - California Albers
- EPSG:32610 - UTM Zone 10N (California)
- EPSG:32643 - UTM Zone 43N (India)

---

### Step 5: Run the Script

1. **Copy the complete script** from the code section below
2. **Open Google Earth Engine** Code Editor
3. **Paste the script** into a new script file
4. **Modify the user inputs** (Section 1)
5. **Run the script** (click Run button or press Ctrl+Enter)
6. **Wait for processing** - The console will show progress
7. **Go to Tasks tab** (right panel)
8. **Click RUN** on each export task
9. **Wait for exports to complete** - Files appear in Google Drive

**Processing time**:
- Task submission: 10-30 seconds
- Export per file: 1-5 minutes (depends on catchment size)
- Total time: varies with number of files

---

## Understanding the Outputs

### Bounding Box vs Exact Catchment

The script exports rainfall data for the **rectangular bounding box** around your catchment, not the exact catchment shape.

**Why?**
- Faster processing
- Maintains regular GPM grid structure
- Provides context for adjacent areas
- HydroPol2D and most hydrological models can clip to exact boundaries during processing

**If you need exact catchment clipping**: The exported catchment shapefile can be used to clip rasters in GIS software or during model preprocessing.

---

### Files Included in Export

**Rainfall rasters**:
- One GeoTIFF per time step
- Filename includes date and time
- Units: mm/h (precipitation rate)

**Catchment boundary**:
- Shapefile (.shp + supporting files)
- Same coordinate system as rainfall rasters
- Use for clipping or visualization

---

### Quality Assurance

The script includes visualization layers on the map:
- **Red polygon**: Merged catchment boundary
- **Blue rectangle**: Export bounding box
- **Sample rainfall layer**: First time step visualization
- **Total rainfall layer**: Cumulative precipitation over entire period

**Console outputs**:
- Catchment area in square kilometers
- Number of 30-minute images available
- Date range confirmation
- Export task submission status
- Total rainfall statistics

---

## Data Considerations

### GPM IMERG Strengths

- **High temporal resolution**: 30-minute observations
- **Global coverage**: Consistent data worldwide
- **Long record**: 20+ years of data
- **Gauge calibration**: Improved accuracy in regions with rain gauge networks
- **Multi-sensor fusion**: Combines passive microwave, infrared, and radar data

### GPM IMERG Limitations

- **Spatial resolution**: 11 km may be coarse for small catchments (less than 100 square kilometers)
- **Latency**: approximately 3 month lag for final calibrated product (V07)
- **Uncertainty**: Lower accuracy over oceans, mountains, and snow/ice
- **Bias**: Can underestimate or overestimate in certain regions (especially complex terrain)
- **Coverage gaps**: 60°N-60°S only (no polar regions)

### Validation Recommendations

**Always validate GPM against local observations when available**:
- Compare with rain gauge data
- Check against radar estimates
- Verify total accumulations
- Assess spatial patterns

For critical applications, consider:
- Bias correction using local gauge data
- Ensemble approaches with multiple datasets
- Uncertainty quantification

---

## Applications

This workflow is designed for:

### Hydrological Modeling
- HydroPol2D distributed rainfall-runoff simulation
- Flash flood forecasting
- Urban drainage analysis
- Water balance studies

### Event Analysis
- Storm characterization
- Rainfall intensity-duration-frequency analysis
- Extreme event reconstruction
- Historical flood event analysis

### Climate Studies
- Long-term precipitation trends
- Seasonal rainfall patterns
- Drought monitoring
- Climate model validation

### Water Resources
- Reservoir inflow estimation
- Irrigation planning
- Hydropower assessment
- Water availability studies

---

## Troubleshooting

### Common Issues

**"Memory capacity exceeded" error**:
- Reduce date range (try smaller time periods)
- Increase temporal resolution (e.g., use daily instead of 30-min)
- Reduce catchment size (use smaller HydroBASINS level)

**No data in exported rasters**:
- Check date range is within GPM period (2000-06-01 onwards)
- Verify catchment is within GPM coverage (60°N-60°S)
- Confirm catchment ID is correct

**Exports not appearing in Tasks**:
- Wait 10-30 seconds after running script
- Check console for error messages
- Refresh Tasks tab

**Very large file sizes**:
- Consider using aggregated temporal resolution
- Export smaller date ranges
- Use appropriate spatial resolution for your application

---

## Additional Resources

- [GPM Mission Website](https://gpm.nasa.gov/)
- [GPM IMERG Technical Documentation](https://gpm.nasa.gov/data/imerg)
- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)
- [HydroBASINS Database](https://www.hydrosheds.org/products/hydrobasins)
- [HydroPol2D Model](https://marcusnobrega-eng.github.io/HydroPol2D-docs/)

---

## Support

For issues with:
- **The script**: Contact your support team
- **GPM data**: Visit GES DISC or GPM help desk
- **Google Earth Engine**: Check GEE Developers forum
- **HydroPol2D**: Visit model documentation website

---

## Version History

- **v1.0** (2026): Initial release with GPM IMERG V07 support
  - 30-minute to daily temporal resolutions
  - HydroBASINS and custom shapefile support
  - Automatic task generation
  - Quality assurance visualizations

---

## GEE Code
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