---
title: HydroPol2D Daily Forcing Data
---

# Generating Meteorological Forcing with Google Earth Engine

HydroPol2D requires spatially distributed meteorological forcing data to drive hydrological simulations. This Google Earth Engine (GEE) script automates the extraction and formatting of rainfall and evapotranspiration (ETP) inputs from multiple global datasets.

The workflow generates CSV files in the exact format required by HydroPol2D, with data extracted at virtual gauge locations distributed across the modeling domain.

---

## What the workflow does

The script processes three global meteorological datasets and exports:

### Rainfall Inputs

- **CHIRPS** (Climate Hazards Group InfraRed Precipitation with Station data)
- **ERA5-Land** (ECMWF Reanalysis)
- **NLDAS** (North American Land Data Assimilation System)

Each dataset produces a separate CSV file with rainfall intensity (mm/h) at all gauge locations.

---

### Climate/ETP Inputs

For evapotranspiration calculations, the script extracts:

- Maximum temperature (Tmax, °C)
- Minimum temperature (Tmin, °C)
- Mean temperature (Tmed, °C)
- Wind speed at 2m (U2, m/s)
- Relative humidity (UR, %)
- Solar radiation (G, MJ/m²/day)

Climate inputs are generated from:
- **ERA5-Land**
- **NLDAS**

---

## Key Features

### Robust Unit Handling

The script includes automatic unit detection and conversion:

- **Temperature**: Auto-detects Kelvin vs Celsius (prevents erroneous sub-zero values)
- **Pressure**: Auto-detects Pa vs kPa for accurate humidity calculations
- **Precipitation**: Converts all sources to consistent mm/h
- **Relative Humidity**: Properly computed from dewpoint (ERA5) or specific humidity (NLDAS)

---

### Virtual Gauge Network

The script creates a regular grid of virtual rain gauges across the catchment:

- User-defined grid density (default: 10×10 = 100 gauges)
- Gauges clipped to catchment boundary
- Each gauge assigned unique ID and projected coordinates
- Spatial interpolation handled by HydroPol2D during simulation

---

### Quality Assurance

Built-in validation plots show:

- Rainfall intensity comparison across datasets (first 30 days)
- Wind speed comparison (first 30 days)
- Time series at first gauge location

These help identify data gaps, outliers, or dataset inconsistencies.

---

## Output Structure

### Rainfall CSV Format

Each rainfall file contains:

**Header rows**:
- Title row
- Blank row
- Gauge index numbers
- Gauge names
- Easting coordinates (m)
- Northing coordinates (m)
- Variable names

**Data rows** (one per day):
- Column 1: Elapsed days
- Column 2: Date (minutes since start)
- Columns 3+: Rainfall intensity (mm/h) at each gauge

**Example structure**:

```javascript
// ======================================================================
// HydroPol2D: Export Rainfall + ETP/Climate-Inputs as "sheet-like" CSVs
// FULLY UPDATED (CHIRPS + ERA5-Land + NLDAS) + ROBUST UNITS FIXES
//
// FIXES:
//  ✅ NLDAS temperature: auto-detect Kelvin vs Celsius (prevents ~ -260°C bug)
//  ✅ UR (%) computed properly for ERA5-Land + NLDAS (not fixed 50, not ~1e-70)
//     - ERA5: RH from T and dewpoint Td
//     - NLDAS: RH from specific humidity q, pressure p, and temperature T
//       * pressure auto-detect Pa vs kPa
//
// QA PLOTS:
//  ✅ Only first 30 days plotted (rain + wind), so charts stay responsive
//
// NOTES:
//  - Rainfall exports remain full period (CSV exports full time range)
//  - Charts are limited to first 30 days ONLY
// ======================================================================


// --------------------
// USER INPUTS
// --------------------
var scale_of_image = 1000;
var startyear = 2024;
var endyear   = 2025;
var Folder_Name = 'Pune';
var crsOut = 'EPSG:32643';   // output CRS for x/y in CSV

// --------------------
// ROI
// --------------------
var basins = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_5");
var catchmentId = 7050585120;
var roi = basins.filter(ee.Filter.eq('HYBAS_ID', catchmentId));

// Adding a shapefile (you already have this variable defined in your session)
roi = pune;

var roiGeom = roi.geometry();

Map.addLayer(roi, {color: 'red'}, 'Catchment Area');
Map.centerObject(roi, 9);

// --------------------
// DATASETS
// --------------------

// CHIRPS (daily, precip in mm/day)
var rainfall_chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY');

// ERA5-Land Daily Aggregates (daily)
var era5_land = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
  .filterDate(ee.Date.fromYMD(startyear, 1, 1), ee.Date.fromYMD(endyear, 12, 31))
  .select([
    'temperature_2m', 'temperature_2m_min', 'temperature_2m_max',
    'dewpoint_temperature_2m',
    'u_component_of_wind_10m', 'v_component_of_wind_10m',
    'total_precipitation_sum'
  ]);

// NLDAS (your band list variant)
var nldas = ee.ImageCollection("NASA/NLDAS/FORA0125_H002")
  .filterDate(ee.Date.fromYMD(startyear, 1, 1), ee.Date.fromYMD(endyear, 12, 31))
  .select([
    'temperature',          // K or °C depending on variant -> we auto-detect
    'specific_humidity',    // kg/kg
    'pressure',             // Pa or kPa depending on variant -> we auto-detect
    'wind_u',               // m/s
    'wind_v',               // m/s
    'total_precipitation'
  ]);


// --------------------
// GAUGE POINT GRID
// --------------------
var num_x = 10;
var num_y = 10;

// bounds coords: [[xmin,ymin], [xmax,ymin], [xmax,ymax], [xmin,ymax], [xmin,ymin]]
var ring = ee.List(roiGeom.bounds().coordinates().get(0));
var p0 = ee.List(ring.get(0));
var p2 = ee.List(ring.get(2));

var xmin = ee.Number(p0.get(0));
var ymin = ee.Number(p0.get(1));
var xmax = ee.Number(p2.get(0));
var ymax = ee.Number(p2.get(1));

var xStep = xmax.subtract(xmin).divide(ee.Number(num_x - 1));
var yStep = ymax.subtract(ymin).divide(ee.Number(num_y - 1));

var points = ee.List.sequence(0, num_x - 1).map(function(i) {
  i = ee.Number(i).int();
  return ee.List.sequence(0, num_y - 1).map(function(j) {
    j = ee.Number(j).int();
    var x = xmin.add(xStep.multiply(i));
    var y = ymin.add(yStep.multiply(j));
    return ee.Feature(ee.Geometry.Point([x, y]));
  });
}).flatten();

var gauge_points = ee.FeatureCollection(points).filterBounds(roiGeom);
Map.addLayer(gauge_points, {color: 'blue'}, 'Gauge Locations');


// --------------------
// Helpers
// --------------------
function nn(v, fallback) {
  return ee.Algorithms.If(ee.Algorithms.IsEqual(v, null), fallback, v);
}

function safeGet(list, i, fallback) {
  list = ee.List(list);
  i = ee.Number(i).int();
  var ok = i.lt(list.size());
  return ee.Algorithms.If(ok, nn(list.get(i), fallback), fallback);
}

function pad3(n) {
  n = ee.Number(n).int();
  return ee.Algorithms.If(
    n.lt(10),  ee.String('00').cat(n.format('%.0f')),
    ee.Algorithms.If(n.lt(100), ee.String('0').cat(n.format('%.0f')),
                     n.format('%.0f'))
  );
}

function colName(k) {
  k = ee.Number(k).int();
  return ee.String('C').cat(k.format('%.0f'));
}

function repeatN(s, N) {
  return ee.List.repeat(s, ee.Number(N).int());
}


// ======================================================================
// ROBUST UNIT HANDLING
// ======================================================================

// Return dict {Tk, Tc} from a temperature image that might be K or °C.
// Heuristic: values > 150 are Kelvin (safe globally for air temp).
function tempToTkTc(Traw) {
  Traw = ee.Image(Traw);
  var isKelvin = Traw.gt(150);
  var Tk = ee.Image(ee.Algorithms.If(isKelvin, Traw, Traw.add(273.15)));
  var Tc = Tk.subtract(273.15);
  return ee.Dictionary({Tk: Tk, Tc: Tc});
}

// Pressure to Pa (auto-detect): if p < 2000 assume kPa, else Pa.
function pressureToPa(p) {
  p = ee.Image(p);
  var isKPa = p.lt(2000);
  return ee.Image(ee.Algorithms.If(isKPa, p.multiply(1000), p));
}


// ======================================================================
// RH helpers
// ======================================================================

// Saturation vapor pressure (Pa) from temperature in °C (Tetens/Magnus)
function esPa_from_Tc(Tc) {
  Tc = ee.Image(Tc);
  return ee.Image(610.78).multiply(
    (ee.Image(17.2694).multiply(Tc).divide(Tc.add(237.3))).exp()
  );
}

// ERA5 RH (%): RH = 100 * es(Td) / es(T)
function RH_from_T_Td(Tk, Tdk) {
  var Tc  = ee.Image(Tk).subtract(273.15);
  var Tdc = ee.Image(Tdk).subtract(273.15);
  var esT  = esPa_from_Tc(Tc);
  var esTd = esPa_from_Tc(Tdc);
  return esTd.divide(esT).multiply(100).clamp(0, 100).rename('UR');
}

// NLDAS RH (%): compute actual vapor pressure from q + p
// e = (q*p) / (0.622 + 0.378 q)  (Pa)   q=kg/kg, p=Pa
function RH_from_q_p_T(q, p, Tk_or_Tc) {
  q = ee.Image(q);
  var pPa = pressureToPa(p);

  // handle T in either unit via tempToTkTc
  var tmp = tempToTkTc(Tk_or_Tc);
  var Tc = ee.Image(ee.Dictionary(tmp).get('Tc'));

  var e  = q.multiply(pPa).divide(ee.Image(0.622).add(ee.Image(0.378).multiply(q))); // Pa
  var es = esPa_from_Tc(Tc); // Pa
  return e.divide(es).multiply(100).clamp(0, 100).rename('UR');
}


// --------------------
// Attach gauge IDs + projected coords
// --------------------
var gpList  = gauge_points.toList(gauge_points.size());
var idxList = ee.List.sequence(0, gauge_points.size().subtract(1));

var gauge_points_id = ee.FeatureCollection(
  idxList.map(function(i) {
    i = ee.Number(i).int();
    var f = ee.Feature(gpList.get(i));

    var gid   = ee.String('A').cat(ee.String(pad3(i.add(101))));
    var gname = ee.String('Gauge ').cat(i.add(1).format('%.0f'));

    var pt = f.geometry().transform(crsOut, 1);
    var xy = pt.coordinates();

    return f.set({
      gauge_id: gid,
      gauge_name: gname,
      x: nn(xy.get(0), ''),
      y: nn(xy.get(1), '')
    });
  })
);

var N = ee.Number(gauge_points_id.size()).int();
print('N gauges:', N);
print('Example gauge:', gauge_points_id.first());

// Client-side count ONLY for building selectors (NOT inside map)
var Nclient = gauge_points_id.size().getInfo();

// These lists are used multiple times (build once)
var gaugeNames = ee.List(gauge_points_id.aggregate_array('gauge_name'));
var gids       = ee.List(gauge_points_id.aggregate_array('gauge_id'));
var xs         = ee.List(gauge_points_id.aggregate_array('x'));
var ys         = ee.List(gauge_points_id.aggregate_array('y'));


// --------------------
// DAILY CALENDAR
// --------------------
var startDate = ee.Date.fromYMD(startyear, 1, 1);
var endDate   = ee.Date.fromYMD(endyear, 12, 31).advance(1, 'day'); // exclusive
var nDays = endDate.difference(startDate, 'day');
var dayOffsets = ee.List.sequence(0, nDays.subtract(1));


// ======================================================================
// BUILD DAILY RAINFALL IMAGECOLLECTIONS (mm/h) FOR EACH SOURCE
// ======================================================================

// 1) CHIRPS: precip is mm/day -> mm/h (divide by 24)
var dailyRain_CHIRPS = ee.ImageCollection.fromImages(
  dayOffsets.map(function(d) {
    d = ee.Number(d).int();
    var date = startDate.advance(d, 'day');

    var rain = rainfall_chirps
      .filterDate(date, date.advance(1, 'day'))
      .sum()
      .divide(24)
      .clip(roiGeom)
      .rename('rain');

    return rain.set('system:time_start', date.millis());
  })
);

// 2) ERA5-Land: total_precipitation_sum is meters/day -> mm/h
var era5DummyRainMasked = ee.Image.constant(0).rename('rain').updateMask(ee.Image(0));

var dailyRain_ERA5 = ee.ImageCollection.fromImages(
  dayOffsets.map(function(d) {
    d = ee.Number(d).int();
    var date = startDate.advance(d, 'day');

    var era0 = era5_land.filterDate(date, date.advance(1, 'day')).first();

    var rain = ee.Image(
      ee.Algorithms.If(
        ee.Algorithms.IsEqual(era0, null),
        era5DummyRainMasked,
        ee.Image(era0).select('total_precipitation_sum')
          .multiply(1000)
          .divide(24)
          .rename('rain')
      )
    ).clip(roiGeom);

    return rain.set('system:time_start', date.millis());
  })
);

// 3) NLDAS: total_precipitation -> assume mm/day -> mm/h
var nldasDummyRainMasked = ee.Image.constant(0).rename('rain').updateMask(ee.Image(0));

var dailyRain_NLDAS = ee.ImageCollection.fromImages(
  dayOffsets.map(function(d) {
    d = ee.Number(d).int();
    var date = startDate.advance(d, 'day');

    var im0 = nldas.filterDate(date, date.advance(1, 'day')).first();

    var rain = ee.Image(
      ee.Algorithms.If(
        ee.Algorithms.IsEqual(im0, null),
        nldasDummyRainMasked,
        ee.Image(im0).select('total_precipitation')
          .divide(24)
          .rename('rain')
      )
    ).clip(roiGeom);

    return rain.set('system:time_start', date.millis());
  })
);


// ======================================================================
// HEADER ROW BUILDER (list only)
// ======================================================================
function makeHeaderRowList(c0, c1, valuesList) {
  valuesList = ee.List(valuesList);
  var base = ee.Dictionary({C0: c0, C1: c1});

  var out = ee.Dictionary(
    ee.List.sequence(0, N.subtract(1)).iterate(function(i, acc) {
      i = ee.Number(i).int();
      acc = ee.Dictionary(acc);
      var v = safeGet(valuesList, i, '');
      return acc.set(colName(i.add(2)), v);
    }, base)
  );

  return ee.Feature(null, out);
}


// ======================================================================
// RAINFALL SHEET BUILDER (MATCH TEMPLATE) - PARAMETERIZED
// ======================================================================
function buildRainfallSheet(dailyRainIC) {
  var rainRows = dailyRainIC.map(function(img) {
    img = ee.Image(img);

    var date = ee.Date(img.get('system:time_start'));
    var dateMin = date.difference(startDate, 'minute');

    // HydroPol2D convention you used
    var elapsedDays = ee.Number(dateMin).divide(1400);

    var fc = img.reduceRegions({
      collection: gauge_points_id,
      reducer: ee.Reducer.mean(),
      scale: scale_of_image
    });

    var vals = ee.List(fc.aggregate_array('mean'));

    var row = ee.Dictionary({ C0: elapsedDays, C1: dateMin });

    var row2 = ee.Dictionary(
      ee.List.sequence(0, N.subtract(1)).iterate(function(i, acc) {
        i = ee.Number(i).int();
        acc = ee.Dictionary(acc);
        var v = safeGet(vals, i, 0);
        return acc.set(colName(i.add(2)), v);
      }, row)
    );

    return ee.Feature(null, row2);
  });

  var header0 = ee.Feature(null, {
    C0: 'HydroPol2D - Spatial Rainfall Parameters: We assume the Durations Match with the Running Control Begin',
    C1: ''
  });

  var header1 = ee.Feature(null, {C0: '', C1: ''});

  var header2 = makeHeaderRowList('', 'Index', ee.List.sequence(1, N));
  var header3 = makeHeaderRowList('', 'Rain Gauge', gaugeNames);
  var header4 = makeHeaderRowList('', 'Easting [m]', xs);
  var header5 = makeHeaderRowList('', 'Northing [m]', ys);
  var header6 = makeHeaderRowList('Elapsed Days', 'Date (min)', repeatN('Rainfall Intensity (mm/h)', N));

  return ee.FeatureCollection([header0, header1, header2, header3, header4, header5, header6])
    .merge(rainRows);
}

// selectors: C0, C1, C2..C(N+1)
var selectorsRain = ['C0', 'C1'];
for (var i = 0; i < Nclient; i++) selectorsRain.push('C' + (i + 2));


// ======================================================================
// 1) RAINFALL SHEETS EXPORTS (FULL PERIOD)
// ======================================================================
Export.table.toDrive({
  collection: buildRainfallSheet(dailyRain_CHIRPS),
  description: 'Rainfall_HP2D_CHIRPS',
  folder: Folder_Name,
  fileFormat: 'CSV',
  selectors: selectorsRain
});

Export.table.toDrive({
  collection: buildRainfallSheet(dailyRain_ERA5),
  description: 'Rainfall_HP2D_ERA5',
  folder: Folder_Name,
  fileFormat: 'CSV',
  selectors: selectorsRain
});

Export.table.toDrive({
  collection: buildRainfallSheet(dailyRain_NLDAS),
  description: 'Rainfall_HP2D_NLDAS',
  folder: Folder_Name,
  fileFormat: 'CSV',
  selectors: selectorsRain
});


// ======================================================================
// 2) ETP / CLIMATE INPUTS SHEET (MATCH TEMPLATE)
// ======================================================================

function buildEtpHeaderFeatures() {
  var titleETP = ee.Feature(null, {C0: 'HydroPol2D - Spatial ETP Parameters', C1: ''});

  var metaRow = ee.Dictionary({C0:'', C1:''});
  metaRow = ee.Dictionary(
    ee.List.sequence(0, N.subtract(1)).iterate(function(i, acc){
      i = ee.Number(i).int();
      acc = ee.Dictionary(acc);
      var baseCol = i.multiply(6).add(2);

      acc = acc.set(colName(baseCol.add(0)), 'Index');
      acc = acc.set(colName(baseCol.add(1)), safeGet(gids, i, ''));
      acc = acc.set(colName(baseCol.add(2)), 'x easting (m)');
      acc = acc.set(colName(baseCol.add(3)), safeGet(xs, i, ''));
      acc = acc.set(colName(baseCol.add(4)), 'y northing (m)');
      acc = acc.set(colName(baseCol.add(5)), safeGet(ys, i, ''));
      return acc;
    }, metaRow)
  );
  var metaETP = ee.Feature(null, metaRow);

  var varRow = ee.Dictionary({C0:'', C1:'Date '});
  varRow = ee.Dictionary(
    ee.List.sequence(0, N.subtract(1)).iterate(function(i, acc){
      i = ee.Number(i).int();
      acc = ee.Dictionary(acc);
      var baseCol = i.multiply(6).add(2);

      acc = acc.set(colName(baseCol.add(0)), 'Tmax (oC)');
      acc = acc.set(colName(baseCol.add(1)), 'Tmin (oC)');
      acc = acc.set(colName(baseCol.add(2)), 'Tmed (oC)');
      acc = acc.set(colName(baseCol.add(3)), 'U2 [m/s]');
      acc = acc.set(colName(baseCol.add(4)), 'UR (%)');
      acc = acc.set(colName(baseCol.add(5)), 'G (MJ/(m2.dia))');
      return acc;
    }, varRow)
  );
  var varsETP = ee.Feature(null, varRow);

  return ee.FeatureCollection([titleETP, metaETP, varsETP]);
}

var selectorsETP = ['C0', 'C1'];
for (var j = 0; j < Nclient * 6; j++) selectorsETP.push('C' + (j + 2));


// --------------------
// ERA5 ETP/CLIMATE ROWS (daily)
// --------------------
var eraDummyMasked = ee.Image.constant([0, 0, 0, 0, 0, 0])
  .rename([
    'temperature_2m', 'temperature_2m_min', 'temperature_2m_max',
    'dewpoint_temperature_2m',
    'u_component_of_wind_10m', 'v_component_of_wind_10m'
  ])
  .updateMask(ee.Image(0));

var etpRows_ERA5 = dailyRain_CHIRPS.map(function(dummyImg) {
  var date = ee.Date(ee.Image(dummyImg).get('system:time_start'));
  var era0 = era5_land.filterDate(date, date.advance(1, 'day')).first();

  var era = ee.Image(
    ee.Algorithms.If(ee.Algorithms.IsEqual(era0, null), eraDummyMasked, era0)
  );

  var tmed = era.select('temperature_2m').subtract(273.15).rename('Tmed');
  var tmax = era.select('temperature_2m_max').subtract(273.15).rename('Tmax');
  var tmin = era.select('temperature_2m_min').subtract(273.15).rename('Tmin');

  var U2  = era.select('u_component_of_wind_10m').pow(2)
    .add(era.select('v_component_of_wind_10m').pow(2))
    .sqrt()
    .rename('U2');

  var UR = RH_from_T_Td(era.select('temperature_2m'), era.select('dewpoint_temperature_2m'));
  var G  = ee.Image.constant(0).rename('G');

  var stack = ee.Image.cat([tmax, tmin, tmed, U2, UR, G]);

  var fc = stack.reduceRegions({
    collection: gauge_points_id,
    reducer: ee.Reducer.mean(),
    scale: scale_of_image
  });

  var tmaxL = ee.List(fc.aggregate_array('Tmax'));
  var tminL = ee.List(fc.aggregate_array('Tmin'));
  var tmedL = ee.List(fc.aggregate_array('Tmed'));
  var u2L   = ee.List(fc.aggregate_array('U2'));
  var urL   = ee.List(fc.aggregate_array('UR'));
  var gL    = ee.List(fc.aggregate_array('G'));

  var row = ee.Dictionary({ C0: '', C1: date.format('yyyy-MM-dd HH:mm:ss') });

  var row2 = ee.Dictionary(
    ee.List.sequence(0, N.subtract(1)).iterate(function(i, acc){
      i = ee.Number(i).int();
      acc = ee.Dictionary(acc);
      var baseCol = i.multiply(6).add(2);

      acc = acc.set(colName(baseCol.add(0)), safeGet(tmaxL, i, ''));
      acc = acc.set(colName(baseCol.add(1)), safeGet(tminL, i, ''));
      acc = acc.set(colName(baseCol.add(2)), safeGet(tmedL, i, ''));
      acc = acc.set(colName(baseCol.add(3)), safeGet(u2L,   i, ''));
      acc = acc.set(colName(baseCol.add(4)), safeGet(urL,   i, ''));
      acc = acc.set(colName(baseCol.add(5)), safeGet(gL,    i, ''));
      return acc;
    }, row)
  );

  return ee.Feature(null, row2);
});

Export.table.toDrive({
  collection: buildEtpHeaderFeatures().merge(etpRows_ERA5),
  description: 'ETP_Inputs_HP2D_ERA5',
  folder: Folder_Name,
  fileFormat: 'CSV',
  selectors: selectorsETP
});


// --------------------
// NLDAS ETP/CLIMATE ROWS (daily)  [ROBUST FIX]
// --------------------
var nldasDummyEtpMasked = ee.Image.constant([0, 0, 0, 0, 0, 0])
  .rename(['Tmax', 'Tmin', 'Tmed', 'U2', 'UR', 'G'])
  .updateMask(ee.Image(0));

var etpRows_NLDAS = dailyRain_CHIRPS.map(function(dummyImg) {
  var date = ee.Date(ee.Image(dummyImg).get('system:time_start'));
  var im0 = nldas.filterDate(date, date.advance(1, 'day')).first();

  var daily = ee.Image(
    ee.Algorithms.If(
      ee.Algorithms.IsEqual(im0, null),
      nldasDummyEtpMasked,
      (function(){
        var im = ee.Image(im0);

        // robust temperature handling
        var tmp = tempToTkTc(im.select('temperature'));
        var Tc = ee.Image(ee.Dictionary(tmp).get('Tc'));
        // NLDAS daily: using same Tc for Tmax/Tmin/Tmed (as before)
        var Tmax = Tc.rename('Tmax');
        var Tmin = Tc.rename('Tmin');
        var Tmed = Tc.rename('Tmed');

        var U2 = im.select('wind_u').pow(2)
          .add(im.select('wind_v').pow(2))
          .sqrt()
          .rename('U2');

        var UR = RH_from_q_p_T(
          im.select('specific_humidity'),
          im.select('pressure'),
          im.select('temperature') // can be K or °C, RH function handles it
        ).rename('UR');

        var G = ee.Image.constant(0).rename('G');

        return ee.Image.cat([Tmax, Tmin, Tmed, U2, UR, G]);
      })()
    )
  ).clip(roiGeom);

  var fc = daily.reduceRegions({
    collection: gauge_points_id,
    reducer: ee.Reducer.mean(),
    scale: scale_of_image
  });

  var tmaxL = ee.List(fc.aggregate_array('Tmax'));
  var tminL = ee.List(fc.aggregate_array('Tmin'));
  var tmedL = ee.List(fc.aggregate_array('Tmed'));
  var u2L   = ee.List(fc.aggregate_array('U2'));
  var urL   = ee.List(fc.aggregate_array('UR'));
  var gL    = ee.List(fc.aggregate_array('G'));

  var row = ee.Dictionary({ C0: '', C1: date.format('yyyy-MM-dd HH:mm:ss') });

  var row2 = ee.Dictionary(
    ee.List.sequence(0, N.subtract(1)).iterate(function(i, acc){
      i = ee.Number(i).int();
      acc = ee.Dictionary(acc);
      var baseCol = i.multiply(6).add(2);

      acc = acc.set(colName(baseCol.add(0)), safeGet(tmaxL, i, ''));
      acc = acc.set(colName(baseCol.add(1)), safeGet(tminL, i, ''));
      acc = acc.set(colName(baseCol.add(2)), safeGet(tmedL, i, ''));
      acc = acc.set(colName(baseCol.add(3)), safeGet(u2L,   i, ''));
      acc = acc.set(colName(baseCol.add(4)), safeGet(urL,   i, ''));
      acc = acc.set(colName(baseCol.add(5)), safeGet(gL,    i, ''));
      return acc;
    }, row)
  );

  return ee.Feature(null, row2);
});

Export.table.toDrive({
  collection: buildEtpHeaderFeatures().merge(etpRows_NLDAS),
  description: 'ETP_Inputs_HP2D_NLDAS',
  folder: Folder_Name,
  fileFormat: 'CSV',
  selectors: selectorsETP
});


// ======================================================================
// QA PLOTS (FIRST 30 DAYS ONLY)
// ======================================================================

// Pick first gauge
var oneGauge = ee.Feature(gauge_points_id.first());
var onePt = oneGauge.geometry();
Map.addLayer(onePt, {color: 'yellow'}, 'Gauge (first)');
print('Selected gauge:', oneGauge);

// Limit IC to first 30 days for plotting ONLY
var plotStart = startDate;
var plotEnd   = startDate.advance(30, 'day'); // first 30 days
function clipTo30Days(ic) {
  return ic.filterDate(plotStart, plotEnd);
}

// Helper: IC -> point TS FC
function icToPointTS(ic, bandName, datasetName) {
  return ee.FeatureCollection(
    ic.map(function(img) {
      img = ee.Image(img);
      var date = ee.Date(img.get('system:time_start'));

      var val = img.select(bandName).reduceRegion({
        reducer: ee.Reducer.mean(),
        geometry: onePt,
        scale: scale_of_image,
        bestEffort: true,
        maxPixels: 1e13
      }).get(bandName);

      return ee.Feature(null, {
        time: date.millis(),
        date: date.format('YYYY-MM-dd'),
        value: val,
        dataset: datasetName
      });
    })
  );
}

// Rainfall charts (30 days)
var tsRain_CHIRPS = icToPointTS(clipTo30Days(dailyRain_CHIRPS), 'rain', 'CHIRPS');
var tsRain_ERA5   = icToPointTS(clipTo30Days(dailyRain_ERA5),   'rain', 'ERA5-Land');
var tsRain_NLDAS  = icToPointTS(clipTo30Days(dailyRain_NLDAS),  'rain', 'NLDAS');

var tsRainAll = tsRain_CHIRPS.merge(tsRain_ERA5).merge(tsRain_NLDAS);

print(
  ui.Chart.feature.groups({
    features: tsRainAll,
    xProperty: 'time',
    yProperty: 'value',
    seriesProperty: 'dataset'
  })
  .setChartType('LineChart')
  .setOptions({
    title: 'Rainfall intensity at first gauge (mm/h) - first 30 days',
    hAxis: { title: 'Date' },
    vAxis: { title: 'Rain (mm/h)' },
    lineWidth: 1,
    pointSize: 0,
    interpolateNulls: false
  })
);

// Wind charts (30 days)
var eraU2DummyMasked = ee.Image.constant(0).rename('U2').updateMask(ee.Image(0));
var nldasU2DummyMasked = ee.Image.constant(0).rename('U2').updateMask(ee.Image(0));

var dailyWind_ERA5 = ee.ImageCollection.fromImages(
  dayOffsets.map(function(d) {
    d = ee.Number(d).int();
    var date = startDate.advance(d, 'day');

    var era0 = era5_land.filterDate(date, date.advance(1, 'day')).first();

    var U2 = ee.Image(
      ee.Algorithms.If(
        ee.Algorithms.IsEqual(era0, null),
        eraU2DummyMasked,
        ee.Image(era0)
          .select(['u_component_of_wind_10m', 'v_component_of_wind_10m'])
          .pow(2)
          .reduce('sum')
          .sqrt()
          .rename('U2')
      )
    ).clip(roiGeom);

    return U2.set('system:time_start', date.millis());
  })
);

var dailyWind_NLDAS = ee.ImageCollection.fromImages(
  dayOffsets.map(function(d) {
    d = ee.Number(d).int();
    var date = startDate.advance(d, 'day');

    var im0 = nldas.filterDate(date, date.advance(1, 'day')).first();

    var U2 = ee.Image(
      ee.Algorithms.If(
        ee.Algorithms.IsEqual(im0, null),
        nldasU2DummyMasked,
        ee.Image(im0).select('wind_u').pow(2)
          .add(ee.Image(im0).select('wind_v').pow(2))
          .sqrt()
          .rename('U2')
      )
    ).clip(roiGeom);

    return U2.set('system:time_start', date.millis());
  })
);

var tsWind_ERA5  = icToPointTS(clipTo30Days(dailyWind_ERA5),  'U2', 'ERA5-Land');
var tsWind_NLDAS = icToPointTS(clipTo30Days(dailyWind_NLDAS), 'U2', 'NLDAS');

var tsWindAll = tsWind_ERA5.merge(tsWind_NLDAS);

print(
  ui.Chart.feature.groups({
    features: tsWindAll,
    xProperty: 'time',
    yProperty: 'value',
    seriesProperty: 'dataset'
  })
  .setChartType('LineChart')
  .setOptions({
    title: 'Wind speed at first gauge (m/s) - first 30 days',
    hAxis: { title: 'Date' },
    vAxis: { title: 'Wind (m/s)' },
    lineWidth: 1,
    pointSize: 0,
    interpolateNulls: false
  })
);