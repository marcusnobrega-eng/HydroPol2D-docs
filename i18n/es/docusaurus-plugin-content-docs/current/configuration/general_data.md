---
title: Parámetros del libro del caso
---

# Parámetros del libro del caso

Un caso de MATLAB es un solo libro de Excel, `HydroPol2D_Inputs.xlsx`. Esta página lista todos los parámetros de sus ocho pestañas de parámetros. Las demás pestañas se describen en otras páginas.

- tablas de clases (suelo, uso del suelo, inestabilidad humana, malla, estructuras de control) en [Tablas de parámetros](../inputs/parameter-tables);
- series temporales (lluvia, estaciones climáticas, hidrogramas de entrada y de nivel) en [Forzamientos opcionales](../inputs/optional-forcing);
- todos los interruptores en una sola página en [Banderas del modelo](./flags);
- cómo abrir, completar y ejecutar un caso en [Ejecutar desde Excel](../getting-started/excel-workflow).

Los nombres de las pestañas y de los bloques se mantienen en inglés, como aparecen en el libro de Excel.

Los casos antiguos, con `General_Data.xlsx`, su hoja `Flags` y libros de Excel separados, siguen funcionando. Ver [Formato anterior](#older-layout).

---

## El libro de un vistazo {#the-workbook-at-a-glance}

| Grupo | Pestañas |
|---|---|
| Guía | Start here, con cómo completar el libro, la leyenda de colores y un enlace a cada pestaña |
| Parámetros (8) | Run control, Input maps, Soil and groundwater, Surface flow, Rain and ET, Design storm, Water quality, Risk and gauges |
| Tablas de clases (5) | Soil classes, Land use classes, Human instability, Mesh, Control structures |
| Series (5) | Rain series, Rain gauges, Climate stations, Inflow hydrographs, Stage hydrographs |

`HydroPol2D_V115.m` lee `Input_Data_Sheets/HydroPol2D_Inputs.xlsx` por defecto. `HYDROPOL_INPUT_EXCEL_FILE` lo dirige a otro libro de Excel.

---

## Cómo funciona una pestaña de parámetros {#how-a-settings-tab-works}

Cada parámetro ocupa una fila con su nombre, su clave, el valor, la unidad, el valor predeterminado y cuándo se usa. Una nota en cada valor lo explica.

- **Bloques e interruptores.** Los parámetros se agrupan en bloques. Un bloque que puede desactivarse comienza con su interruptor, y sus filas se muestran en gris mientras el interruptor vale 0. Los valores en gris se ignoran. No hay una hoja `Flags` separada.
- **Los valores obligatorios** se marcan con un asterisco rojo. Un valor opcional vacío mantiene su valor predeterminado o la alternativa indicada en su nota.
- **Los bloques avanzados** (encabezado gris) contienen parámetros heredados. Se recomienda mantener sus valores predeterminados, salvo que haya una razón para cambiarlos.
- **Los bloques en pausa** (encabezado ámbar) contienen funciones en pausa. Se deben mantener en 0, ya que el valor 1 detiene la simulación.
- **Las rutas** pueden ser absolutas o relativas a la carpeta del libro de Excel.

---

## Referencia de parámetros {#settings-reference}

Las tablas siguientes se generan a partir del catálogo que construye el libro de Excel (`tools/workbook_builder/input_catalog.yaml` en el repositorio de MATLAB), por lo que coinciden fila por fila con el libro. Las descripciones son las notas del libro.

### Run control {#tab-run-control}

Período de simulación, paso de tiempo, rendimiento y lo que registra el modelo.

#### Simulation period {#simulation-period}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Fecha y hora de inicio | `date_begin` | fecha | obligatorio | siempre | date_begin es la fecha y hora de inicio de la simulación. Se debe usar la misma referencia de tiempo que en las series temporales de lluvia, evapotranspiración, caudal de entrada, nivel y observaciones. |
| Fecha y hora de fin | `date_end` | fecha | obligatorio | siempre | date_end es la fecha y hora de fin de la simulación. Debe ser posterior a date_begin. Los valores de forzamiento fuera de este intervalo no forman parte de la simulación. |

#### Surface time step {#surface-time-step}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Paso de tiempo inicial | `time_step_model` | s | obligatorio | siempre | time_step_model es el paso de tiempo nominal del modelo superficial, en segundos. Inicializa el ciclo de enrutamiento. El paso de tiempo adaptativo puede reemplazarlo por un valor estable entre min_time_step y max_time_step. |
| Paso de tiempo mínimo | `min_time_step` | s | obligatorio | siempre | min_time_step es el paso de tiempo de enrutamiento superficial más pequeño permitido, en segundos. Se debe usar un valor positivo lo bastante pequeño para resolver el humedecimiento rápido, el flujo somero y el terreno empinado. |
| Paso de tiempo máximo | `max_time_step` | s | obligatorio | siempre | max_time_step es el paso de tiempo de enrutamiento superficial más grande permitido, en segundos. Limita el paso de tiempo durante los períodos de variación lenta y debe ser mayor o igual que min_time_step. |
| Factor de Courant, inferior | `alfa_min` | - | obligatorio | siempre | alfa_min es el coeficiente de seguridad de Courant inferior que HydroPol2D usa al calcular un paso de tiempo estable para el enrutamiento superficial. Los valores más pequeños son más conservadores y suelen aumentar el tiempo de ejecución. |
| Paso de tiempo adaptativo | `flag_adaptive_timestepping` | 0 / 1 | obligatorio | siempre | Actualiza el paso de tiempo del enrutamiento superficial a partir de los límites de estabilidad durante la simulación. Se recomienda mantenerlo activado en la mayoría de las simulaciones dinámicas. |

#### Computing {#computing}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Ejecutar en la GPU | `flag_GPU` | 0 / 1 | obligatorio | siempre | Ejecuta los arreglos y cálculos admitidos en una GPU compatible con MATLAB. Se debe dejar desactivado cuando no hay una GPU compatible. |
| Precisión simple | `flag_single` | 0 / 1 | obligatorio | siempre | Almacena los arreglos numéricos admitidos en precisión simple para reducir el uso de memoria. Se debe mantener desactivado cuando se requiere la máxima precisión numérica. |

#### Recording intervals {#recording-intervals}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Guardar mapas cada | `record_time_maps` | min | obligatorio | siempre | record_time_maps es el intervalo, en minutos, entre los mapas espaciales guardados del modelo. Un intervalo más corto aumenta el detalle de las salidas y el uso de disco sin cambiar la física de la simulación. |
| Guardar hidrogramas cada | `record_time_hydrographs` | min | obligatorio | siempre | record_time_hydrographs es el intervalo, en minutos, entre los registros guardados de los hidrogramas de salida, de entrada y de las estaciones. Se debe elegir un intervalo que resuelva la respuesta esperada del hidrograma. |
| Guardar mapas de lluvia cada | `record_time_spatial_rainfall` | min | obligatorio | con lluvia espacial | record_time_spatial_rainfall es el intervalo, en minutos, usado para guardar o agregar la información de lluvia espacial. Para la lluvia en ráster, debe ser compatible con el intervalo de salida de los mapas. |
| Guardar mapas de ET cada | `record_time_spatial_ETP` | min | obligatorio | con ET | record_time_spatial_ETP es el intervalo, en minutos, entre los productos espaciales guardados de evaporación y transpiración. Los intervalos más cortos producen archivos más detallados y aumentan la demanda de almacenamiento. |

#### Outputs and display {#outputs-and-display}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Exportar mapas | `flag_export_maps` | 0 / 1 | obligatorio | siempre | Exporta las salidas espaciales programadas del modelo, como la profundidad de inundación y mapas relacionados. |
| Exportar mapas de agua subterránea | `flag_export_groundwater_maps` | 0 / 1 | `0` | con agua subterránea | Exporta los rásteres programados de profundidad del nivel freático cuando la modelación del agua subterránea está activada. |
| Mapas de elevación de la superficie del agua | `flag_wse` | 0 / 1 | obligatorio | siempre | flag_wse controla la salida de mapas de elevación de la superficie del agua (0 la desactiva y 1 la activa). El mapa usa la elevación del DEM más la profundidad de agua simulada donde la profundidad supera depth_wse. |
| Profundidad mínima para esos mapas | `depth_wse` | m | obligatorio | con mapas de superficie del agua | depth_wse es la profundidad mínima de agua, en metros, usada al producir los mapas de elevación de la superficie del agua. Evita informar la elevación de la superficie del agua donde la celda está prácticamente seca. |
| Informe del balance hídrico | `flag_waterbalance` | 0 / 1 | obligatorio | siempre | Escribe diagnósticos del balance hídrico durante la simulación. Se recomienda activarlo para la validación y para las verificaciones rutinarias del modelo. |
| Panel en vivo | `flag_dashboard` | 0 / 1 | obligatorio | siempre | Crea las salidas configuradas orientadas al panel durante la simulación. |
| Mostrar el tiempo transcurrido | `flag_elapsed_time` | 0 / 1 | obligatorio | siempre | Imprime o registra el tiempo de cómputo transcurrido de la simulación. |

#### Warm start {#warm-start}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Iniciar desde un estado de calentamiento | `flag_warmup` | 0 / 1 | obligatorio | siempre | Inicializa la simulación desde el estado de calentamiento configurado en lugar de los rásteres estándar de estado inicial. |

#### Advanced (keep the defaults unless you know why) {#advanced-keep-the-defaults-unless-you-know-why}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Factor de Courant, superior | `alfa_max` | - | obligatorio | siempre | alfa_max es el coeficiente superior del paso de tiempo adaptativo, que se conserva por compatibilidad con configuraciones de control del tiempo. Debe ser positivo y no menor que alfa_min. Los cálculos actuales de estabilidad del enrutamiento usan alfa_min para el paso candidato conservador. |
| Incremento de actualización del paso de tiempo | `time_step_change` | s | obligatorio | siempre | time_step_change es el incremento de tiempo positivo, en segundos, usado para el registro de la actualización del paso de tiempo y para la alineación de los diagnósticos. No es el intervalo de actualización del agua subterránea. |
| Verificación completa de estabilidad del paso de tiempo | `flag_timestep` | 0 / 1 | obligatorio | siempre | Selecciona el tratamiento completo de estabilidad del paso de tiempo para los solucionadores de enrutamiento compatibles. Se recomienda usar el valor predeterminado validado, salvo al probar una formulación numérica específica. |

### Input maps {#tab-input-maps}

Rutas a los mapas GeoTIFF. Los mapas opcionales se dejan vacíos para usar las tablas de clases o los escalares.

#### Required maps {#required-maps}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Elevación del terreno (DEM) | `DEM_path` | m | obligatorio | siempre | DEM_path es la ruta obligatoria al GeoTIFF de elevación del terreno, con elevaciones en metros. Define el dominio del modelo, la geometría de la malla y los gradientes topográficos. |
| Clases de uso y cobertura del suelo | `LULC_path` | clase | obligatorio | siempre | LULC_path es el GeoTIFF categórico obligatorio de uso y cobertura del suelo. Los códigos de clase del ráster se asocian con la pestaña Land use classes. Los códigos sin asignación reciben el valor alternativo documentado, ponderado por área. |
| Clases de suelo | `SOIL_path` | clase | obligatorio | siempre | SOIL_path es el GeoTIFF categórico obligatorio de clases de suelo. Los códigos de clase del ráster se asocian con la pestaña Soil classes. Los códigos sin asignación reciben el valor alternativo documentado, ponderado por área. |

#### Land surface {#land-surface}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Albedo | `Albedo_path` | 0 a 1 | vacío | con albedo espacial | Albedo_path es un ráster opcional de albedo superficial, de 0 a 1. Solo se usa cuando el albedo espacial está activado para el cálculo de la evapotranspiración por balance de energía. |
| Índice de área foliar | `LAI_path` | m2/m2 | vacío | con intercepción | LAI_path es un ráster opcional de índice de área foliar, en m2 de área foliar por m2 de suelo. Lo usan la intercepción del dosel y la evapotranspiración asociada a la vegetación cuando los interruptores correspondientes están activados. |
| Fracción impermeable | `ImperviousFraction_path` | 0 a 1 | vacío | opcional | ImperviousFraction_path es un ráster opcional de la fracción de cobertura impermeable, de 0 a 1. Refina el comportamiento de la infiltración dentro de una celda. Los valores fuera de este rango no tienen sentido físico. |

#### Rivers and terrain {#rivers-and-terrain}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Ancho del río | `RiverWidths_path` | m | vacío | submalla de canal con mapas de ríos | RiverWidths_path es un GeoTIFF opcional del ancho del río, en metros. Es obligatorio para el modelo de canal embebido de Neal (2012) cuando flag_subgrid y flag_river_rasters están activados. Los anchos embebidos válidos deben ser menores que el tamaño de la celda gruesa. |
| Profundidad del río | `RiverDepths_path` | m | vacío | submalla de canal con mapas de ríos | RiverDepths_path es un GeoTIFF opcional de la profundidad del río, en metros. Se combina con RiverWidths_path para el modelo de canal embebido y debe ser positivo donde hay un canal. |

#### Initial states {#initial-states}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Profundidad inicial del agua superficial | `Warmup_Depth_path` | m | vacío | con calentamiento | Warmup_Depth_path es un GeoTIFF opcional de la profundidad inicial del agua superficial, en metros. Solo se lee cuando flag_warmup está activado, e inicializa el almacenamiento superficial antes del enrutamiento. |
| Agua inicial en el suelo | `Initial_Soil_Moisture_path` | ver nota | vacío | con calentamiento | Initial_Soil_Moisture_path es un GeoTIFF opcional del almacenamiento inicial de agua en el suelo. A pesar de su nombre heredado, los valores se interpretan como almacenamiento por encima de la humedad residual, en mm, y no como contenido volumétrico de agua. Se lee con flag_warmup. |
| Elevación inicial del nivel freático | `GW_table_path` | m | vacío | con agua subterránea | GW_table_path es un GeoTIFF opcional de la elevación inicial del nivel freático, en metros, con el mismo datum vertical que el DEM. Se lee cuando el agua subterránea o el flujo base están activados, y se limita por debajo de la superficie del terreno. |
| Equivalente de agua de nieve inicial | `Initial_SWE_path` | mm | vacío | con nieve | Initial_SWE_path es un GeoTIFF opcional del equivalente de agua de nieve inicial, en mm de agua equivalente. Solo se lee cuando la modelación de nieve está activada. Los valores negativos no son válidos, y las celdas sin datos usan la condición predeterminada sin nieve. |
| Profundidad inicial de nieve | `Initial_Snow_Depth_path` | mm | vacío | con nieve | Initial_Snow_Depth_path es un GeoTIFF opcional de la profundidad inicial de nieve, en mm. Solo se lee cuando la modelación de nieve está activada. Cuando se combina con el SWE, el modelo verifica su consistencia física y deriva la densidad. |

#### Soil-property maps (override the SOIL classes) {#soil-property-maps-override-the-soil-classes}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| theta_s del suelo | `ThetaS_path` | m3/m3 | vacío | opcional | ThetaS_path es un GeoTIFF opcional del contenido de agua a saturación del suelo, theta_s, en m3/m3. Sobrescribe el valor de SOIL_parameters de cada clase donde es finito (nodata conserva el valor de la clase), en todas las capas de suelo. |
| theta_r del suelo | `ThetaR_path` | m3/m3 | vacío | opcional | ThetaR_path es un GeoTIFF opcional del contenido de agua residual del suelo, theta_r, en m3/m3. Sobrescribe el valor de SOIL_parameters de cada clase donde es finito (nodata conserva el valor de la clase). |
| alfa de van Genuchten del suelo | `AlphaVG_path` | 1/m | vacío | opcional | AlphaVG_path es un GeoTIFF opcional del alfa de van Genuchten del suelo, en 1/m. Sobrescribe el valor de SOIL_parameters de cada clase donde es finito (nodata conserva el valor de la clase). |
| n de van Genuchten del suelo | `NVG_path` | - | vacío | opcional | NVG_path es un GeoTIFF opcional del n de van Genuchten del suelo (mayor que 1, adimensional). Sobrescribe el valor de SOIL_parameters de cada clase donde es finito (nodata conserva el valor de la clase). |
| Ksat, capa superficial | `KsatNearSurface_path` | mm/h | vacío | opcional | KsatNearSurface_path es un GeoTIFF opcional de la conductividad hidráulica saturada de la capa superficial del suelo, en mm/h. Sobrescribe ksat x Ks_multiplier_near_surface de cada clase de SOIL donde es finito (nodata conserva el valor de la clase). |
| Ksat, capa de la zona de raíces | `KsatRootZone_path` | mm/h | vacío | opcional | KsatRootZone_path es un GeoTIFF opcional de la conductividad hidráulica saturada de la capa de la zona de raíces, en mm/h. Sobrescribe ksat x Ks_multiplier_root_zone de cada clase de SOIL donde es finito (nodata conserva el valor de la clase). |
| Ksat, capa de transmisión | `KsatTransmission_path` | mm/h | vacío | opcional | KsatTransmission_path es un GeoTIFF opcional de la conductividad hidráulica saturada de la capa de transmisión del suelo, en mm/h. Sobrescribe ksat x Ks_multiplier_transmission de cada clase de SOIL donde es finito (nodata conserva el valor de la clase). |
| Ksat del acuífero (kgsat) | `GroundwaterKsat_path` | mm/h | vacío | opcional | GroundwaterKsat_path es un GeoTIFF opcional de la conductividad horizontal del acuífero, kgsat, en mm/h. Sobrescribe el kgsat de SOIL_parameters de cada clase donde es finito. En el subsuelo en capas, es el Kh alternativo de la roca cuando regolith_ksat_h_mm_h y RegolithKsatH_path están vacíos. |
| Rendimiento específico del acuífero | `SpecificYield_path` | - | vacío | esquema de agua subterránea heredado | SpecificYield_path es un GeoTIFF opcional del rendimiento específico del acuífero, Sy (adimensional), para el esquema de agua subterránea heredado. Sobrescribe el Sy de SOIL_parameters de cada clase donde es finito. El subsuelo en capas no lo usa, ya que allí Sy proviene de las curvas de retención (o de regolith_specific_yield). |

#### Water-quality maps {#water-quality-maps}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Masa inicial de contaminante | `Initial_Buildup_path` | kg/celda | vacío | con build-up inicial | Initial_Buildup_path es un GeoTIFF opcional de masa de contaminante, en kg por celda. Solo se lee cuando flag_initial_buildup y el módulo de calidad del agua están activados. |
| Asíntota de build-up C1 | `B1_path` | ver nota | vacío | calidad del agua con mapas | B1_path es la ruta opcional a un GeoTIFF de la asíntota espacial de build-up C1. Solo se lee cuando la calidad del agua y las entradas ráster de calidad del agua están activadas. Se deben usar valores y unidades consistentes con el parámetro C1 de LULC. |
| Tasa de build-up C2 | `B2_path` | ver nota | vacío | calidad del agua con mapas | B2_path es la ruta opcional a un GeoTIFF del parámetro espacial de tasa de build-up C2. Solo se lee cuando la calidad del agua y las entradas ráster de calidad del agua están activadas. |
| Coeficiente de wash-off C3 | `W1_path` | ver nota | vacío | calidad del agua con mapas | W1_path es la ruta opcional a un GeoTIFF del coeficiente espacial de wash-off C3. Solo se lee cuando la calidad del agua y las entradas ráster de calidad del agua están activadas. |
| Exponente de wash-off C4 | `W2_path` | ver nota | vacío | calidad del agua con mapas | W2_path es la ruta opcional a un GeoTIFF del exponente espacial de wash-off C4. Solo se lee cuando la calidad del agua y las entradas ráster de calidad del agua están activadas. |

### Soil and groundwater {#tab-soil-and-groundwater}

Infiltración, evapotranspiración, agua subterránea, subsuelo en capas y acuífero profundo. Cada mapa está debajo del valor que sobrescribe.

#### Infiltration and evapotranspiration {#infiltration-and-evapotranspiration}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Infiltración | `flag_infiltration` | 0 / 1 | obligatorio | siempre | Activa la infiltración y el balance de agua del suelo en capas. Desactivarla también desactiva la evapotranspiración en el modelo actual. |
| Evapotranspiración | `flag_ETP` | 0 / 1 | obligatorio | siempre | Activa la evapotranspiración. HydroPol2D usa las entradas meteorológicas o de mapas configuradas para calcular la evaporación y la transpiración. |
| Intercepción del dosel | `flag_abstraction` | 0 / 1 | obligatorio | siempre | Activa la intercepción del dosel y los procesos de abstracción inicial. |
| Ascenso capilar | `flag_capillary_rise` | 0 / 1 | `1` | con agua subterránea | Activa el flujo ascendente limitado desde el agua subterránea somera hacia la zona de transmisión o de raíces cuando existen déficits de almacenamiento. |
| Nieve | `flag_snow_modeling` | 0 / 1 | obligatorio | siempre | Activa la partición de la precipitación, el almacenamiento de nieve, el derretimiento, la sublimación y la compactación, con las columnas de nieve de la pestaña Land use classes. |
| Albedo desde un mapa | `flag_spatial_albedo` | 0 / 1 | obligatorio | con nieve o ET | Usa el ráster de albedo suministrado en lugar del albedo escalar predeterminado. |
| Sin infiltración en celdas de río | `flag_neglect_infiltration_river` | 0 / 1 | obligatorio | con infiltración | Fija en cero la infiltración y la abstracción inicial en las celdas de río identificadas. |

#### Groundwater {#groundwater}

El interruptor es `flag_groundwater_modeling`. El resto del bloque se muestra en gris mientras vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Agua subterránea | `flag_groundwater_modeling` | 0 / 1 | obligatorio | interruptor de este bloque | Activa el módulo acoplado de recarga del suelo en capas y de agua subterránea saturada. |
| Flujo lateral de agua subterránea | `flag_baseflow` | 0 / 1 | obligatorio | con agua subterránea | Activa la contribución de flujo base configurada donde el flujo de trabajo hidrológico seleccionado lo admite. |
| Mapa de profundidad hasta el lecho de roca | `DTB_path` | m | vacío | heredado: obligatorio; en capas: opcional | DTB_path es un GeoTIFF opcional de PROFUNDIDAD HASTA EL LECHO DE ROCA, en metros bajo la superficie del terreno. En el esquema de agua subterránea heredado, es la profundidad del suelo, y el acuífero está dentro de ella. En el subsuelo en capas, es el fondo de toda la columna (suelo más roca meteorizada), y el espesor del suelo se define por separado con subsurface_soil_base_depth_m o SoilBaseDepth_path. Es obligatorio en el esquema heredado y opcional con flag_layered_subsurface = 1. En ese caso, un DTB_path vacío recurre a subsurface_depth_to_bedrock_m y luego a la DTB (m) de cada clase de suelo de la pestaña Soil classes. |
| Mapa de carga fija de agua subterránea | `GW_Dirichlet_Head_path` | m | vacío | con agua subterránea | GW_Dirichlet_Head_path es un GeoTIFF opcional de la elevación prescrita de la carga del agua subterránea, en metros. Las celdas finitas del ráster definen el contorno de Dirichlet del agua subterránea. Las celdas sin datos quedan sin restricción. |
| Serie de recarga prescrita | `flag_prescribed_recharge` | 0 / 1 | `0` | con agua subterránea | Reemplaza la recarga calculada hacia el nivel freático por la serie de Prescribed_Recharge_Timeseries_File (pestaña Input maps). Valor predeterminado 0. |
| Archivo de recarga prescrita | `Prescribed_Recharge_Timeseries_File` | archivo | vacío | con recarga prescrita | Prescribed_Recharge_Timeseries_File es un archivo opcional con una serie temporal de recarga que reemplaza la recarga calculada hacia el nivel freático. Solo se lee cuando flag_prescribed_recharge = 1. |
| Factor de Courant del agua subterránea | `groundwater_courant` | - | `0.25` | con flujo lateral | groundwater_courant es el factor de seguridad adimensional que limita el paso de tiempo del agua subterránea de Boussinesq. Se debe usar un valor mayor que cero y no mayor que uno. Los valores más pequeños mejoran la estabilidad a costa de más actualizaciones. |
| Tolerancia relativa del reloj lateral | `groundwater_relative_tolerance` | - | `0.001` | con flujo lateral | groundwater_relative_tolerance es el cambio relativo del almacenamiento de agua subterránea que activa la siguiente actualización lateral del agua subterránea (el reloj lateral). Los valores más pequeños actualizan con más frecuencia y cuestan más. Valor predeterminado 0.001. |
| Tolerancia de carga del reloj lateral | `groundwater_head_tolerance_m` | m | `0.001` | con flujo lateral | groundwater_head_tolerance_m es el cambio del nivel freático, en metros, que activa la siguiente actualización lateral del agua subterránea (el reloj lateral). Los valores más pequeños actualizan con más frecuencia y cuestan más. Valor predeterminado 0.001 m. |
| Espesor del lecho del río | `riverbed_thickness_m` | m | `0.5` | con agua subterránea | riverbed_thickness_m es el espesor del lecho del río, en metros, usado en el intercambio río-acuífero, con conductancia = Ksat del lecho x área del lecho / espesor. Valor predeterminado 0.5 m. |

#### Layered subsurface: column {#layered-subsurface-column}

El interruptor es `flag_layered_subsurface`. El resto del bloque se muestra en gris mientras vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Subsuelo en capas | `flag_layered_subsurface` | 0 / 1 | `0` | interruptor de estos bloques | Activa el subsuelo en capas, con tres capas de suelo sobre capas de roca meteorizada hasta el lecho de roca y un nivel freático por celda (reglas de Miguez-Macho et al., 2007). Los parámetros están en los bloques del subsuelo en capas de la pestaña Soil and groundwater, y los rásteres opcionales están debajo de los valores que sobrescriben. Requiere flag_groundwater_modeling = 1. |
| Espesor del suelo | `subsurface_soil_base_depth_m` | m | `2.0` | con subsuelo en capas | subsurface_soil_base_depth_m es el ESPESOR DEL SUELO, en metros bajo el terreno, es decir, donde termina el suelo y comienza la roca meteorizada (regolito). Las tres capas de suelo (superficial, zona de raíces y transmisión) usan la pestaña Soil classes hasta esta profundidad. SoilBaseDepth_path lo sobrescribe celda por celda. Se limita a la profundidad hasta el lecho de roca. Valor predeterminado 2.0 m. |
| Mapa de espesor del suelo | `SoilBaseDepth_path` | m | vacío | con subsuelo en capas (prevalece donde tiene datos) | SoilBaseDepth_path es un GeoTIFF opcional del ESPESOR DEL SUELO, en metros bajo el terreno (la base del suelo). Sobrescribe subsurface_soil_base_depth_m donde es finito. Solo para el subsuelo en capas. Fuente global: SoilGrids BDRICM. |
| Profundidad hasta el lecho de roca | `subsurface_depth_to_bedrock_m` | m | vacío | subsuelo en capas, donde el mapa de DTB está vacío | subsurface_depth_to_bedrock_m es la PROFUNDIDAD HASTA EL LECHO DE ROCA, en metros bajo el terreno, es decir, el fondo de toda la columna modelada, con el suelo y la roca meteorizada que está debajo. Es mayor o igual que el espesor del suelo. Prioridad: ráster DTB_path, luego este valor y luego la DTB (m) de cada clase de suelo de la pestaña Soil classes, con una advertencia. Se limita a subsurface_max_depth_m. |
| Columna más profunda | `subsurface_max_depth_m` | m | `50.0` | con subsuelo en capas | subsurface_max_depth_m limita la columna modelada, en metros bajo el terreno, con fondo de la columna = min(profundidad hasta el lecho de roca, este valor). Valor predeterminado 50 m. |
| Espesor de la primera capa de roca | `subsurface_deep_first_thickness_m` | m | `0.25` | con subsuelo en capas | subsurface_deep_first_thickness_m es el espesor, en metros, de la primera capa de roca, justo debajo de la base del suelo. Cada capa siguiente es subsurface_deep_growth_ratio veces más gruesa, hasta subsurface_deep_max_thickness_m. Valor predeterminado 0.25 m. |
| Razón de crecimiento de las capas de roca | `subsurface_deep_growth_ratio` | - | `2.0` | con subsuelo en capas | subsurface_deep_growth_ratio multiplica el espesor de cada capa de roca para obtener el de la siguiente. Con los valores predeterminados, los espesores son 0.25, 0.5, 1, 2, 4, 4, ... m. Se debe usar un valor de al menos 1. Valor predeterminado 2. |
| Capa de roca más gruesa | `subsurface_deep_max_thickness_m` | m | `4.0` | con subsuelo en capas | subsurface_deep_max_thickness_m es el mayor espesor de una capa de roca, en metros. Las capas mantienen este espesor hasta el fondo de la columna. Valor predeterminado 4 m. |

#### Layered subsurface: rock properties {#layered-subsurface-rock-properties}

Se muestra en gris mientras `flag_layered_subsurface` vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| theta_s de la roca | `regolith_theta_s` | m3/m3 | `0.35` | con subsuelo en capas | regolith_theta_s es el contenido de agua a saturación (porosidad) de las capas de roca debajo de la base del suelo, en m3/m3. RegolithThetaS_path lo sobrescribe celda por celda. Valor predeterminado 0.35. |
| Mapa de theta_s de la roca | `RegolithThetaS_path` | m3/m3 | vacío | con subsuelo en capas (prevalece donde tiene datos) | RegolithThetaS_path es un GeoTIFF opcional del contenido de agua a saturación de las capas de roca, en m3/m3. Sobrescribe regolith_theta_s donde es finito. Solo para el subsuelo en capas. |
| theta_r de la roca | `regolith_theta_r` | m3/m3 | `0.05` | con subsuelo en capas | regolith_theta_r es el contenido de agua residual de las capas de roca, en m3/m3, menor que regolith_theta_s. RegolithThetaR_path lo sobrescribe celda por celda. Valor predeterminado 0.05. |
| Mapa de theta_r de la roca | `RegolithThetaR_path` | m3/m3 | vacío | con subsuelo en capas (prevalece donde tiene datos) | RegolithThetaR_path es un GeoTIFF opcional del contenido de agua residual de las capas de roca, en m3/m3. Sobrescribe regolith_theta_r donde es finito. Solo para el subsuelo en capas. |
| alfa de van Genuchten de la roca | `regolith_alpha_vg_m_inverse` | 1/m | `2.0` | con subsuelo en capas | regolith_alpha_vg_m_inverse es el alfa de van Genuchten de las capas de roca, en 1/m. Junto con regolith_n_vg, define cuánta agua retiene la roca después de drenar y, por lo tanto, su rendimiento específico. RegolithAlphaVG_path lo sobrescribe celda por celda. Valor predeterminado 2. |
| Mapa de alfa de van Genuchten de la roca | `RegolithAlphaVG_path` | 1/m | vacío | con subsuelo en capas (prevalece donde tiene datos) | RegolithAlphaVG_path es un GeoTIFF opcional del alfa de van Genuchten de las capas de roca, en 1/m. Sobrescribe regolith_alpha_vg_m_inverse donde es finito. Solo para el subsuelo en capas. |
| n de van Genuchten de la roca | `regolith_n_vg` | - | `1.5` | con subsuelo en capas | regolith_n_vg es el n de van Genuchten de las capas de roca (adimensional, mayor que 1). RegolithNVG_path lo sobrescribe celda por celda. Valor predeterminado 1.5. |
| Mapa de n de van Genuchten de la roca | `RegolithNVG_path` | - | vacío | con subsuelo en capas (prevalece donde tiene datos) | RegolithNVG_path es un GeoTIFF opcional del n de van Genuchten de las capas de roca. Sobrescribe regolith_n_vg donde es finito. Solo para el subsuelo en capas. |
| Ksat vertical de la roca | `regolith_ksat_v_mm_h` | mm/h | `5.0` | con subsuelo en capas | regolith_ksat_v_mm_h es la conductividad hidráulica saturada vertical de las capas de roca, en mm/h. Limita el drenaje y la recarga a través de la roca. RegolithKsatV_path lo sobrescribe celda por celda. Valor predeterminado 5 mm/h. |
| Mapa de Ksat vertical de la roca | `RegolithKsatV_path` | mm/h | vacío | con subsuelo en capas (prevalece donde tiene datos) | RegolithKsatV_path es un GeoTIFF opcional de la conductividad saturada vertical de las capas de roca, en mm/h. Sobrescribe regolith_ksat_v_mm_h donde es finito. Solo para el subsuelo en capas. |
| Ksat horizontal de la roca | `regolith_ksat_h_mm_h` | mm/h | vacío | con subsuelo en capas (vacío: kgsat) | regolith_ksat_h_mm_h es la conductividad hidráulica saturada horizontal de las capas de roca, en mm/h, usada para el flujo lateral del agua subterránea. Si se deja vacío, se usa el Ksat del agua subterránea (kgsat) de la pestaña Soil classes. RegolithKsatH_path lo sobrescribe celda por celda. |
| Mapa de Ksat horizontal de la roca | `RegolithKsatH_path` | mm/h | vacío | con subsuelo en capas (prevalece donde tiene datos) | RegolithKsatH_path es un GeoTIFF opcional de la conductividad saturada horizontal de las capas de roca, en mm/h, usada para el flujo lateral del agua subterránea. Sobrescribe regolith_ksat_h_mm_h donde es finito. Solo para el subsuelo en capas. Fuente global: permeabilidad de GLHYMPS 2.0. |
| Rendimiento específico de la roca | `regolith_specific_yield` | - | vacío | con subsuelo en capas (vacío: de la curva) | regolith_specific_yield es la porosidad drenable de las capas de roca (adimensional). Si se deja vacío, se deriva de los valores de van Genuchten como theta_s menos el contenido de agua a capacidad de campo. Un valor aquí o RegolithSpecificYield_path sobrescribe ese cálculo, y no debe superar theta_s menos theta_r. |
| Mapa de rendimiento específico de la roca | `RegolithSpecificYield_path` | - | vacío | con subsuelo en capas (prevalece donde tiene datos) | RegolithSpecificYield_path es un GeoTIFF opcional del rendimiento específico de las capas de roca. Sobrescribe el valor derivado (theta_s menos capacidad de campo) donde es finito. Solo para el subsuelo en capas. |

#### Layered subsurface: soil and numerics {#layered-subsurface-soil-and-numerics}

Se muestra en gris mientras `flag_layered_subsurface` vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Kh / Kv del suelo | `soil_lateral_anisotropy` | - | `1.0` | con subsuelo en capas | soil_lateral_anisotropy es la razón entre la conductividad horizontal y la vertical de las tres capas de suelo, con Kh = anisotropía x Ksat. El valor 1 significa isotropía. Valor predeterminado 1. |
| Succión de capacidad de campo | `capillary_field_capacity_head_m` | m | `3.3` | con subsuelo en capas | capillary_field_capacity_head_m es la carga de succión, en metros, que define la capacidad de campo, es decir, el agua que una capa retiene después de que el nivel freático desciende por debajo de ella. El rendimiento específico es theta_s menos theta a esta carga, y el ascenso capilar desde el nivel freático rellena una capa solo hasta este contenido de agua. Valor predeterminado 3.3 m (cerca de 33 kPa). Reducirlo representa una franja capilar sobre niveles freáticos someros (el rendimiento específico disminuye con él). |
| Subpasos de drenaje | `subsurface_drainage_substeps` | - | `1` | con subsuelo en capas | subsurface_drainage_substeps es el número de subpasos del drenaje por gravedad entre capas dentro de un paso de tiempo del modelo. El valor 1 basta en la mayoría de los casos. Se puede aumentar (de 2 a 10) para capas delgadas y muy conductoras. Valor predeterminado 1. |
| Intervalo de actualización lateral | `groundwater_target_dt_s` | s | `86400` | con agua subterránea | groundwater_target_dt_s es el intervalo, en segundos, entre las actualizaciones laterales del agua subterránea, en los dos esquemas de subsuelo. Se usa un intervalo más corto cuando el límite de estabilidad lo requiere. Los flujos verticales del suelo se siguen calculando en cada paso de tiempo del modelo. Valor predeterminado 86400 s (un día). |
| Intervalo lateral más corto | `groundwater_min_dt_s` | s | `60` | con agua subterránea | groundwater_min_dt_s es el intervalo más corto permitido, en segundos, entre actualizaciones laterales del agua subterránea, incluso cuando el límite de estabilidad pide uno menor. Valor predeterminado 60 s. |
| Flujo implícito en el nivel freático | `flag_implicit_water_table_flux` | 0 / 1 | `1` | con subsuelo en capas | Resuelve de forma implícita el flujo de Darcy entre el suelo y el nivel freático en el subsuelo en capas (un paso de Euler implícito linealizado por celda). Con 1 (predeterminado), el flujo sigue siendo preciso con pasos de tiempo largos cuando el nivel freático es somero. Con 0, se usa el flujo explícito, que en ese caso requiere pasos cortos. Solo se usa con flag_layered_subsurface = 1. |

#### Lateral conductivity multipliers {#lateral-conductivity-multipliers}

Se muestra en gris mientras `flag_layered_subsurface` vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Multiplicador de Kh del suelo | `soil_lateral_conductivity_multiplier` | - | `1.0` | con subsuelo en capas | soil_lateral_conductivity_multiplier escala la conductividad horizontal de las tres capas de suelo (Ksat del suelo x soil_lateral_anisotropy) para el flujo lateral del agua subterránea. El Ksat vertical y la infiltración no cambian. Se ajusta con la calibración por recesión del agua subterránea en capas (los caudales altos drenan a través del suelo). El valor 1 mantiene los valores de los mapas. |
| Multiplicador de Kh de la roca | `regolith_lateral_conductivity_multiplier` | - | `1.0` | con subsuelo en capas | regolith_lateral_conductivity_multiplier escala la conductividad horizontal de las capas de roca debajo de la base del suelo (regolith_ksat_h_mm_h, RegolithKsatH_path o kgsat). Se ajusta con la calibración por recesión del agua subterránea en capas (los caudales bajos drenan a través de la roca). El valor 1 mantiene los valores de los mapas. |

#### Feddes root-water stress {#feddes-root-water-stress}

El interruptor es `flag_feddes`. El resto del bloque se muestra en gris mientras vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Estrés de Feddes | `flag_feddes` | 0 / 1 | `0` | interruptor de este bloque | Activa el estrés de Feddes en la absorción de agua por las raíces, que reduce la transpiración de cada capa de suelo según su carga de succión. Las cargas están en este bloque. Funciona con el esquema de suelo en capas y con el heredado. |
| h1, anaerobiosis | `feddes_h1_m` | m | `-0.1` | con Feddes | feddes_h1_m es la carga de anaerobiosis, en metros (negativa). En condiciones más húmedas que h1, las raíces no toman agua (falta oxígeno). Valor predeterminado -0.1 m. |
| h2, inicio de la absorción óptima | `feddes_h2_m` | m | `-0.25` | con Feddes | feddes_h2_m es la carga, en metros (negativa), a partir de la cual la absorción es óptima. Entre h1 y h2, el factor de estrés sube de 0 a 1. Valor predeterminado -0.25 m. |
| h3, inicio del estrés | `feddes_h3_m` | m | `-4.0` | con Feddes | feddes_h3_m es la carga, en metros (negativa), donde comienza el estrés hídrico. Entre h3 y h4, el factor baja de 1 a 0. Se usa cuando feddes_h3_low_m y feddes_h3_high_m están vacíos. Valor predeterminado -4 m. |
| h3 con demanda baja | `feddes_h3_low_m` | m | vacío | con Feddes (vacío: h3) | feddes_h3_low_m es h3 con una demanda de transpiración baja (ET potencial de 1 mm/d o menos), en metros (negativa). Junto con feddes_h3_high_m, h3 se interpola según la demanda, como en SWAP. Si se deja vacío, se usa feddes_h3_m. |
| h3 con demanda alta | `feddes_h3_high_m` | m | vacío | con Feddes (vacío: h3) | feddes_h3_high_m es h3 con una demanda de transpiración alta (ET potencial de 5 mm/d o más), en metros (negativa). Suele ser menos negativa que feddes_h3_low_m, de modo que el estrés comienza antes en los días de alta demanda. Si se deja vacío, se usa feddes_h3_m. |
| h4, punto de marchitez | `feddes_h4_m` | m | `-80.0` | con Feddes | feddes_h4_m es la carga del punto de marchitez, en metros (negativa). En condiciones más secas que h4, las raíces no toman agua. Valor predeterminado -80 m (-0.8 MPa). |

#### Deep aquifer {#deep-aquifer}

El interruptor es `flag_deep_aquifer`. El resto del bloque se muestra en gris mientras vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Acuífero profundo | `flag_deep_aquifer` | 0 / 1 | `0` | interruptor de este bloque | Activa el acuífero profundo. La fracción deep_recharge_fraction de la recarga del nivel freático va a un embalse lineal por subcuenca y vuelve a la superficie después de deep_aquifer_tau_days. Requiere DeepAquiferSubbasins_path y DeepAquiferChannelWeight_path. |
| Mapa de subcuencas del acuífero profundo | `DeepAquiferSubbasins_path` | ID | vacío | con acuífero profundo: obligatorio | DeepAquiferSubbasins_path es un GeoTIFF entero de identificadores de subcuenca (1, 2, ...). Cada identificador es un embalse del acuífero profundo. Solo es obligatorio cuando flag_deep_aquifer = 1, y cada celda activa necesita un identificador positivo. Un ráster con todos los valores en 1 da un solo embalse para todo el dominio. |
| Mapa de pesos de retorno del acuífero profundo | `DeepAquiferChannelWeight_path` | - | vacío | con acuífero profundo: obligatorio | DeepAquiferChannelWeight_path es un GeoTIFF de pesos no negativos que indica dónde vuelve a la superficie el caudal de salida del acuífero profundo de cada subcuenca, por ejemplo, 1 en las celdas de río y 0 en las demás. Los pesos se normalizan dentro de cada subcuenca, que necesita al menos un peso positivo. Solo es obligatorio cuando flag_deep_aquifer = 1. |
| Fracción de la recarga hacia el acuífero profundo | `deep_recharge_fraction` | - | `0.05` | con acuífero profundo | deep_recharge_fraction es la fracción, en (0, 1], de la recarga del nivel freático que se envía al acuífero profundo, un embalse lineal lento por subcuenca debajo del modelo 2-D de agua subterránea. El resto recarga el acuífero somero. Solo se lee cuando flag_deep_aquifer = 1. |
| Tiempo de respuesta | `deep_aquifer_tau_days` | días | `180` | con acuífero profundo | deep_aquifer_tau_days es el tiempo de respuesta del acuífero profundo, en días. Cada embalse de subcuenca drena con caudal de salida = almacenamiento / tau, y ese caudal vuelve a la superficie en las celdas ponderadas por DeepAquiferChannelWeight_path. Solo se lee cuando flag_deep_aquifer = 1. |

#### Deep aquifer: starting storage (give one, or none to start empty) {#deep-aquifer-starting-storage-give-one-or-none-to-start-empty}

Se muestra en gris mientras `flag_deep_aquifer` vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Flujo base profundo inicial (desde una estación de aforo) | `deep_aquifer_initial_baseflow_mm_day` | mm/día | vacío | opción 1 | deep_aquifer_initial_baseflow_mm_day es el flujo base del acuífero profundo por unidad de área en la fecha de inicio, en mm/día (opción 1, desde una estación de aforo, por ejemplo con hydropol2d estimate-deep-baseflow, que divide la parte profunda del flujo base de la fecha de inicio por el área de drenaje). Cada subcuenca comienza con un almacenamiento S0 = q0 x área de la subcuenca x deep_aquifer_tau_days. Si se deja vacío, el acuífero comienza vacío. Se define este valor o deep_aquifer_mean_recharge_mm_year, no ambos. |
| Recarga media de largo plazo (sin estación de aforo) | `deep_aquifer_mean_recharge_mm_year` | mm/año | vacío | opción 2: estado estacionario | deep_aquifer_mean_recharge_mm_year es la recarga media de largo plazo hacia el nivel freático, en mm/año (opción 2, sin necesidad de una estación de aforo). El acuífero profundo comienza en estado estacionario, con q0 = deep_recharge_fraction x esta recarga y S0 = q0 x área de la subcuenca x deep_aquifer_tau_days. Se define este valor o deep_aquifer_initial_baseflow_mm_day, no ambos. |
| Almacenamiento inicial calibrado (JSON) | `DeepAquiferInitialState_path` | archivo | vacío | opción 3: desde el Builder | DeepAquiferInitialState_path es un archivo JSON opcional con el almacenamiento inicial de cada subcuenca del acuífero profundo (el DeepAquiferInitialState.json del Builder, obtenido en la calibración por recesión). Se usa en lugar de los dos valores de Deep Aquifer Initial State, no junto con ellos. |

### Surface flow {#tab-surface-flow}

Esquema de enrutamiento, salidas, canales de río, tratamiento del terreno y estructuras.

#### Routing scheme {#routing-scheme}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Enrutamiento inercial local | `flag_inertial` | 0 / 1 | obligatorio | siempre | Selecciona el solucionador hidrodinámico inercial local. Es el solucionador de enrutamiento obligatorio para la extensión de submalla de canal de Neal (2012). |
| Discretización inercial | `flag_numerical_scheme` | 1 / 2 / 3 | obligatorio | con inercial local | Elige la discretización inercial local, con 1 = Bates, 2 = pendiente aguas arriba (upwind) y 3 = pendiente centrada. El valor solo lo usan las opciones de enrutamiento que llaman al esquema inercial. |
| Enrutamiento por autómatas celulares | `flag_CA` | 0 / 1 | obligatorio | siempre | Selecciona la opción de enrutamiento hidrodinámico por autómatas celulares. No se debe activar junto con el enrutamiento inercial local o de momento completo. |
| Onda cinemática | `flag_kinematic` | 0 / 1 | obligatorio | siempre | Selecciona la alternativa de enrutamiento por onda cinemática. No se debe combinar con el enrutamiento inercial local, de momento completo o por autómatas celulares. |
| Onda difusiva | `flag_diffusive` | 0 / 1 | obligatorio | siempre | Selecciona la alternativa de enrutamiento por onda difusiva. No se debe combinar con el enrutamiento inercial local, de momento completo o por autómatas celulares. |
| Direcciones de flujo D8 | `flag_D8` | 0 / 1 | obligatorio | siempre | Retirado: manténgalo en 0. El D8 ráster antiguo estaba incompleto, y 1 detiene la simulación. El enrutamiento inercial local D8 es `flag_d8_local_inertial`, definido en el script de bypass (vea [Limitaciones](../validation/limitations#matlab-optional-modules)). |

#### Outlets and boundaries {#outlets-and-boundaries}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Tratamiento del contorno abierto | `flag_boundary` | 0 / 1 | obligatorio | siempre | Activa el tratamiento configurado del contorno abierto o perimetral. La máscara y la pendiente de salida deben definirse con cuidado, porque este parámetro controla la salida de agua en el borde del dominio. |
| Relación de salida | `flag_outlet_type` | 1 / 2 | obligatorio | siempre | Elige la relación de salida, con 1 = salida de flujo normal con slope_outlet y 2 = salida de flujo crítico. Las celdas de salida seleccionadas determinan dónde se aplica esta relación. |
| Salida de flujo crítico | `flag_critical` | 0 / 1 | obligatorio | siempre | Usa el tratamiento de salida de flujo crítico donde el solucionador de enrutamiento seleccionado lo admite. Es distinto de la salida de flujo normal seleccionada con flag_outlet_type. |
| Pendiente de energía en la salida | `slope_outlet` | m/m | obligatorio | salida de flujo normal | slope_outlet es la pendiente de energía positiva de flujo normal, en m/m, aplicada en las celdas de salida configuradas. Debe representar el gradiente del canal o del terreno aguas abajo, fuera del dominio modelado. |
| Número de celdas de salida | `n_outlets_data` | - | `1` | siempre | n_outlets_data es el número de celdas del borde del dominio usadas como salidas (redondeado, al menos 1). Las salidas crecen desde la celda perimetral más baja, salvo que se suministre un CSV de celdas de salida. Valor predeterminado 1. |

#### River channel (sub-grid) {#river-channel-sub-grid}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Submalla de canal de Neal (2012) | `flag_neal_channel` | 0 / 1 | obligatorio | siempre | Activa la extensión de canal rectangular embebido y llanura de inundación de Neal (2012). Requiere flag_inertial = 1, topología ráster estructurada y rásteres válidos de ancho y profundidad del río. |
| Ancho y profundidad del río desde mapas | `flag_river_rasters` | 0 / 1 | obligatorio | con submalla de canal | Usa los rásteres RiverWidths y RiverDepths suministrados para definir la geometría del canal del modelo de submalla activo. |
| n de Manning del canal | `Manning` | s m^-1/3 | obligatorio | siempre | Manning es la rugosidad de Manning del canal dentro de las márgenes, en s m^-1/3, aplicada en las celdas de río. Las celdas de terreno y fuera del cauce usan la rugosidad de la pestaña Land use classes. |
| Coeficiente de la ley de profundidad | `alfa_1` | - | obligatorio | canal derivado del área de drenaje | alfa_1 es el coeficiente de la relación derivada de profundidad del canal H = alfa_1 A^alfa_2, donde A es el área de contribución en km2. Solo se usa cuando la geometría del canal se deriva en lugar de suministrarse como rásteres. |
| Exponente de la ley de profundidad | `alfa_2` | - | obligatorio | canal derivado del área de drenaje | alfa_2 es el exponente de la relación derivada de profundidad del canal H = alfa_1 A^alfa_2. Se debe usar un valor calibrado o justificado para la red fluvial de interés. |
| Coeficiente de la ley de ancho | `beta_1` | - | obligatorio | canal derivado del área de drenaje | beta_1 es el coeficiente de la relación derivada de ancho del canal W = beta_1 A^beta_2, donde A es el área de contribución en km2. No se usa cuando se suministran rásteres de ancho del río. |
| Exponente de la ley de ancho | `beta_2` | - | obligatorio | canal derivado del área de drenaje | beta_2 es el exponente de la relación derivada de ancho del canal W = beta_1 A^beta_2. Controla qué tan rápido se ensanchan aguas abajo los canales generados. |

#### Terrain treatment {#terrain-treatment}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Remuestrear la malla | `flag_resample` | 0 / 1 | obligatorio | siempre | Remuestrea los rásteres auxiliares a la malla del DEM durante el preprocesamiento cuando su malla difiere de la del DEM. |
| Resolución del modelo | `resolution_resample` | m | obligatorio | con remuestreo | resolution_resample es la resolución de trabajo de la malla del modelo, en metros, cuando el remuestreo de rásteres está activado. Todas las entradas del modelo se alinean a esta resolución durante el preprocesamiento. |
| Rellenar depresiones | `flag_fill_DEM` | 0 / 1 | obligatorio | siempre | Rellena las depresiones del terreno antes de derivar las direcciones de drenaje y la acumulación de flujo. |
| Suavizar los perfiles de los ríos | `flag_smoothening` | 0 / 1 | obligatorio | siempre | Aplica un suavizado restringido del perfil de los cauces durante el preprocesamiento del DEM. Esta opción requiere Optimization Toolbox. |
| Área umbral de cauces | `min_area` | km2 | obligatorio | con suavizado | min_area es el umbral de área de contribución, en km2, usado para extraer la red de cauces modelada y derivar la geometría hidráulica a partir de la acumulación de flujo. |
| Intensidad del suavizado | `K_value` | 0 a 20 | obligatorio | con suavizado | K_value es la intensidad del suavizado que se pasa al suavizador restringido y regularizado del perfil de los cauces. Solo se usa cuando el suavizado del DEM está activado. Los valores mayores producen una regularización más fuerte del perfil. |
| Regularización del suavizado | `tau` | 0 a 1 | obligatorio | con suavizado | tau es el parámetro adimensional de regularización que se pasa al suavizador restringido y regularizado del perfil de los cauces. Solo se usa cuando el suavizado del DEM está activado. |
| Pendiente mínima impuesta | `sl` | m/m | obligatorio | con suavizado | sl es el gradiente mínimo de drenaje impuesto, en m/m, usado por el acondicionamiento del terreno cuando la imposición de pendiente mínima está activada. |
| Suavizar celdas | `flag_smooth_cells` | 0 / 1 | obligatorio | siempre | Aplica el tratamiento configurado de suavizado del DEM por celda durante el preprocesamiento. |
| Solo cauces principales | `flag_trunk` | 0 / 1 | obligatorio | siempre | Usa la opción de procesamiento de cauces principales durante la preparación del terreno y de la red de drenaje. |
| Rebajar el DEM | `flag_reduce_DEM` | 0 / 1 | obligatorio | siempre | Aplica la reducción configurada del DEM en los canales de los ríos durante el preprocesamiento. |
| Filtro DTM | `flag_DTM` | 0 / 1 | obligatorio | siempre | Usa la ruta de procesamiento DTM para preparar el terreno cuando los datos de entrada requieren ese flujo de trabajo. |
| Pendiente del filtro DTM | `slope_DTM` | % | obligatorio | con filtro DTM | slope_DTM es el umbral de pendiente, en porcentaje, usado por el filtro DTM. Solo se lee cuando la opción de filtrado DTM está activada. |

#### Unstructured mesh {#unstructured-mesh}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Malla de Voronoi | `flag_voronoi` | 0 / 1 | `0` | siempre | Ejecuta el modelo en una malla de Voronoi (no estructurada) preparada en lugar de la malla ráster. Las opciones de la malla se leen de la pestaña Mesh. |
| Tablas de submalla de Voronoi | `flag_voronoi_subgrid` | 0 / 1 | obligatorio | con Voronoi | Activa las tablas de submalla por cara (nivel frente a área de flujo, perímetro mojado y capacidad de conducción) en la malla de Voronoi. Solo se usa con flag_voronoi = 1. La ruta de la tabla se define en la pestaña Mesh. |

#### Inflows and structures {#inflows-and-structures}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Hidrogramas de entrada | `flag_inflow` | 0 / 1 | obligatorio | siempre | Aplica uno o más hidrogramas de caudal prescritos en las coordenadas de entrada definidas en la pestaña Inflow hydrographs. |
| Hidrogramas de nivel | `flag_stage_hydrograph` | 0 / 1 | obligatorio | siempre | Aplica un hidrograma de nivel del agua prescrito en las ubicaciones configuradas del contorno de nivel. |
| Embalses | `flag_reservoir` | 0 / 1 | obligatorio | siempre | Activa el módulo de embalses y estructuras de control con las entradas de embalses configuradas. |

#### Paused (keep at 0: setting 1 stops the run) {#paused-keep-at-0-setting-1-stops-the-run}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Submalla con tablas de consulta (en pausa) | `flag_structured_lookup_subgrid` | 0 / 1 | `0` | en pausa | Activa la formulación de submalla estructurada con tablas de consulta en el modelo ráster regular. Usa propiedades de celdas y caras que dependen del nivel, y no puede combinarse con la submalla de Neal ni con la de Voronoi. |
| DEM de alta resolución para esa submalla (en pausa) | `Subgrid_DEM_path` | m | vacío | en pausa | Subgrid_DEM_path es un GeoTIFF opcional de DEM de alta resolución, en metros, para la submalla con tablas de consulta. Solo se lee cuando la submalla con tablas de consulta está activada sin el modo de desborde. |

### Rain and ET {#tab-rain-and-et}

Origen de la lluvia y de la evapotranspiración, y listas de archivos de mapas.

#### Rainfall source {#rainfall-source}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Lluvia | `flag_rainfall` | 0 / 1 | obligatorio | siempre | Activa el forzamiento de lluvia. Se usa con una sola fuente de lluvia seleccionada, que puede ser una serie temporal agregada, la interpolación de pluviómetros, una secuencia programada de rásteres o un producto satelital. |
| Lluvia con variación espacial | `flag_spatial_rainfall` | 0 / 1 | obligatorio | con lluvia | Interpola la lluvia de los pluviómetros configurados a cada celda del modelo. Se requieren las coordenadas de los pluviómetros y una serie temporal de lluvia común. |
| Lluvia desde la lista de mapas de abajo | `flag_input_rainfall_map` | 0 / 1 | obligatorio | con lluvia | Lee una secuencia de rásteres de lluvia indexada en el tiempo desde la lista Rainfall maps. No se debe activar junto con otra fuente de lluvia espacial. |
| Lluvia satelital | `flag_satellite_rainfall` | 0 / 1 | obligatorio | con lluvia | Activa el flujo de trabajo de forzamiento con lluvia satelital. Prepara una programación horaria de lluvia espacial y activa la lluvia automáticamente. |
| Lluvia satelital en tiempo real | `flag_real_time_satellite_rainfall` | 0 / 1 | obligatorio | con lluvia | Activa el flujo de trabajo de lluvia satelital en tiempo real. Esta opción experimental crea una programación corta y móvil de lluvia espacial. |

#### Evapotranspiration source {#evapotranspiration-source}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| ET desde las listas de mapas de abajo | `flag_input_ETP_map` | 0 / 1 | obligatorio | con ET | Lee programaciones pareadas de rásteres de transpiración y evaporación desde la pestaña Rain and ET. Ambas programaciones deben tener las mismas entradas de tiempo. |

#### Advanced (keep the defaults unless you know why) {#advanced-keep-the-defaults-unless-you-know-why-1}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Múltiples simulaciones de lluvia (flujo de trabajo heredado) | `flag_rainfall_multiple_runs` | 0 / 1 | obligatorio | con lluvia | Activa el flujo de trabajo heredado de múltiples simulaciones de lluvia. Se debe dejar desactivado para un solo evento de lluvia estándar. |

### Design storm {#tab-design-storm}

Tormentas sintéticas a partir de una relación IDF local i = K RP^a / (b + duration)^c.

#### Hyetograph {#hyetograph}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Bloques alternados | `flag_alternated_blocks` | 0 / 1 | obligatorio | tormenta de diseño | Genera la tormenta de diseño configurada de bloques alternados en lugar de leer una serie temporal de lluvia. |
| Curvas de Huff | `flag_huff` | 0 / 1 | obligatorio | tormenta de diseño | Genera la tormenta de diseño configurada de Huff en lugar de leer una serie temporal de lluvia. |
| Período de retorno | `RP` | años | obligatorio | tormenta de diseño | RP es el período de retorno de la tormenta de diseño, en años. La relación IDF seleccionada lo usa para calcular la intensidad de la lluvia. |
| Duración de la tormenta | `Rainfall Duration` | min | obligatorio | tormenta de diseño | Rainfall Duration es la duración total de la tormenta de diseño, en minutos. Define la longitud del hietograma generado por bloques alternados o por Huff. |
| Paso de tiempo del hietograma | `dt_design` | min | obligatorio | tormenta de diseño | dt_design es el incremento de tiempo, en minutos, usado para discretizar el hietograma de diseño generado. Debe ser lo bastante corto para resolver el pico de lluvia buscado. |

#### IDF relation {#idf-relation}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Escala K de la IDF | `K` | ver nota | obligatorio | tormenta de diseño | K es el coeficiente de escala de la relación IDF local i = K RP^a / (b + duration)^c. Sus unidades deben ser consistentes con la intensidad en mm/h y la duración en minutos. |
| Exponente a del período de retorno en la IDF | `a` | - | obligatorio | tormenta de diseño | a es el exponente adimensional del período de retorno en la relación IDF local. Se deben usar coeficientes ajustados para el sitio de estudio. |
| Desplazamiento b de la duración en la IDF | `b` | min | obligatorio | tormenta de diseño | b es el desplazamiento de la duración en la relación IDF local, expresado en minutos cuando la duración se ingresa en minutos. |
| Exponente c de la duración en la IDF | `c` | - | obligatorio | tormenta de diseño | c es el exponente adimensional de la duración en la relación IDF local. Controla cómo disminuye la intensidad a medida que aumenta la duración de la tormenta. |

### Water quality {#tab-water-quality}

Build-up y wash-off de contaminantes.

#### Water quality {#water-quality}

El interruptor es `flag_waterquality`. El resto del bloque se muestra en gris mientras vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Calidad del agua | `flag_waterquality` | 0 / 1 | obligatorio | interruptor de este bloque | Activa los cálculos de build-up, wash-off y transporte de contaminantes, y sus salidas. |
| Parámetros desde mapas | `flag_WQ_Rasters` | 0 / 1 | obligatorio | con calidad del agua | Usa los rásteres espaciales de coeficientes de calidad del agua B1, B2, W1 y W2 en lugar de los coeficientes de la tabla de cobertura del suelo. |
| Build-up inicial desde un mapa | `flag_initial_buildup` | 0 / 1 | obligatorio | con calidad del agua | Inicializa el build-up de calidad del agua con los parámetros configurados del período seco antecedente y del build-up. |
| Días secos antecedentes | `ADD` | días | obligatorio | con calidad del agua | ADD son los días secos antecedentes. Cuando no se usa un ráster de build-up inicial, entra en la inicialización exponencial del build-up B0 = C1 [1 - exp(-C2 ADD)]. |
| Masa superficial mínima | `min_Bt` | g/m2 | obligatorio | con calidad del agua | min_Bt es la densidad de masa superficial mínima de contaminante, en g/m2, que conserva el cálculo de wash-off de calidad del agua. Evita el tratamiento numérico de masas de contaminante despreciables. |
| Límite inferior del build-up | `Bmin` | g/m2 | obligatorio | con calidad del agua | Bmin es el límite inferior del build-up de contaminante, en g/m2, usado por la formulación de build-up y wash-off seleccionada. Se debe usar un valor no negativo y no mayor que Bmax. |
| Límite superior del build-up | `Bmax` | g/m2 | obligatorio | con calidad del agua | Bmax es el límite superior del build-up de contaminante, en g/m2, usado por la formulación de build-up y wash-off seleccionada. Limita la masa de contaminante almacenada físicamente cuando esa opción está activa. |
| Umbral de visualización en los mapas | `Pol_min` | mg/L | obligatorio | con calidad del agua | Pol_min es la concentración mínima de contaminante, en mg/L, que se muestra en los mapas de calidad del agua. Es un umbral de visualización. Los valores inferiores se ocultan en los gráficos, pero no se eliminan del balance de masa. |

#### Advanced (keep the defaults unless you know why) {#advanced-keep-the-defaults-unless-you-know-why-2}

Se muestra en gris mientras `flag_waterquality` vale 0.

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Formulación (0 = build-up / wash-off basado en masa) | `flag_wq_model` | 0 / ... | obligatorio | con calidad del agua | Selecciona la formulación de calidad del agua. El valor 0 usa el modo de build-up y wash-off basado en masa. Otros valores solo se deben usar en configuraciones heredadas compatibles. |

### Risk and gauges {#tab-risk-and-gauges}

Riesgo de inestabilidad humana y puntos de observación.

#### Human instability {#human-instability}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Riesgo de inestabilidad humana | `flag_human_instability` | 0 / 1 / 3 | obligatorio | siempre | Calcula indicadores de inestabilidad humana según la profundidad y la velocidad. El valor 0 lo desactiva, el valor 1 usa la clasificación básica y el valor 3 activa la clasificación extendida. |

#### Observation points {#observation-points}

| Parámetro | Clave | Unidad | Predeterminado | Se usa cuando | Descripción |
|---|---|---|---|---|---|
| Registrar en las estaciones de abajo | `flag_obs_gauges` | 0 / 1 | obligatorio | siempre | Exporta los valores modelados en las coordenadas de las estaciones de observación de la tabla de estaciones. |

---

## Tabla de estaciones y secciones transversales de caudal {#gauge-table-and-discharge-cross-sections}

Con `flag_obs_gauges = 1`, el modelo registra resultados en cada estación de la tabla de estaciones de la pestaña Risk and gauges.

| Columna | Obligatoria | Significado |
|---|---|---|
| Gauge | sí | Número de la estación |
| Easting (m), Northing (m) | sí | Posición de la estación, en la proyección del DEM |
| Label Name | sí | Nombre usado en las salidas |
| Cross-section width (cells) | no | Número de celdas de la sección transversal de caudal. Vacío: 5. Un ancho par se aumenta en 1, de modo que la estación quede en el centro. |
| Downstream direction | no | `auto` (predeterminado), o `N`, `S`, `E`, `W` |

La tabla termina en la primera fila vacía.

**Qué registra una estación.** La profundidad y el nivel del agua se toman en la celda de la estación. El caudal se suma a lo largo de una sección transversal, es decir, una línea de celdas perpendicular al flujo y centrada en la celda de la estación.

1. Con `auto`, la dirección aguas abajo sigue la pendiente descendente del gradiente medio del terreno en una ventana de ancho × ancho alrededor de la estación. Donde el terreno es plano, se usa `N`, `S`, `E` u `W`. `N` o `S` da una línea este-oeste, y `E` u `W` da una línea norte-sur.
2. Las celdas fuera de la malla o del dominio se eliminan de la línea.
3. El caudal es la suma con signo sobre las caras aguas abajo de la línea, con la misma regla que las estaciones de enrutamiento de HydroPol2D-Python. Las diagonales D8 que cruzan la línea se cuentan.
4. Se manejan las dos convenciones de caras de los solucionadores de enrutamiento, es decir, los caudales de salida en un solo sentido (autómatas celulares, inercial D8) y los flujos con signo almacenados en ambas caras (inercial D4, difusivo, cinemático, momento completo). Por lo tanto, las simulaciones inerciales no se cuentan dos veces.

**Salidas.**

| Salida | Contenido |
|---|---|
| Figuras de hidrogramas de las estaciones | Una línea de trazos y puntos con el caudal de la sección transversal |
| `Rating_Curve_Gauges.csv` | La columna `Cross-section Discharge (m3/s)` |
| `Gauge_Cross_Sections.csv` | La fila y la columna de la malla de cada celda de cada sección transversal |

En el modo bypass, las dos columnas opcionales del CSV de estaciones son `Cross_section_width_cells` y `Downstream_direction`. Las verificaciones están en `Validation/Gauges/run_gauge_cross_section_checks.m`.

---

## Modo bypass y variables de entorno {#bypass-mode-and-environment-variables}

- En el modo bypass, las mismas claves son campos de `InputData_Bypass.flags` (interruptores y parámetros del subsuelo en capas y de Feddes) y de `InputData_Bypass.general` (otros parámetros, como el estado inicial del acuífero profundo).
- Las variables de entorno tienen prioridad sobre el libro de Excel. El Case Builder las usa.

| Variable | Sobrescribe |
|---|---|
| `HYDROPOL_INPUT_EXCEL_FILE` | El libro de Excel que se lee |
| `HYDROPOL_SUBSURFACE_SCHEME`, `HYDROPOL_ENABLE_FEDDES`, `HYDROPOL_IMPLICIT_WATER_TABLE_FLUX` | Los interruptores del subsuelo en capas, de Feddes y del flujo implícito |
| `HYDROPOL_<NAME>` | Cualquier parámetro numérico del subsuelo en capas o de Feddes, por su clave en mayúsculas |
| `HYDROPOL_DEEP_INITIAL_BASEFLOW_MM_DAY`, `HYDROPOL_DEEP_MEAN_RECHARGE_MM_YEAR`, `HYDROPOL_DEEP_INITIAL_STATE_PATH` | El estado inicial del acuífero profundo |
| `HYDROPOL_SOIL_LATERAL_CONDUCTIVITY_MULTIPLIER`, `HYDROPOL_REGOLITH_LATERAL_CONDUCTIVITY_MULTIPLIER` | Los multiplicadores ajustados de la conductividad lateral |

---

## Formato anterior {#older-layout}

Los casos creados antes del 2026-10-20 usan `General_Data.xlsx`, con su hoja `Flags` y libros de Excel separados. Siguen funcionando sin cambios. Cada lector toma su pestaña del libro del caso cuando el caso lo tiene y, si no, del libro de Excel anterior.

| Libro del caso | Formato anterior |
|---|---|
| Ocho pestañas de parámetros | La hoja `General_Data`, con los parámetros en bloques y las rutas de rásteres en las columnas T y U |
| Interruptores dentro de sus bloques | La hoja `Flags`, con un interruptor por fila y el valor en la columna E |
| Soil classes, Land use classes, Human instability, Mesh, Control structures | `SOIL_parameters.xlsx`, `LULC_parameters.xlsx`, `human_risk.xlsx`, `Voronoi_Settings.xlsx`, `BC_Control_structure.xlsx` |
| Rain series, Rain gauges, Climate stations, Inflow hydrographs, Stage hydrographs | `Rainfall_Intensity_Data.xlsx`, `Rainfall_Spatial_Input.xlsx`, `ETP_input_data.xlsx`, `Inflow_Hydrograph.xlsx`, `Stage_Hydrograph.xlsx` |

Para convertir un caso antiguo, se ejecuta el constructor del libro desde `tools/workbook_builder` en el repositorio de MATLAB.

```bash
python build_input_workbook.py input_catalog.yaml General_Data.xlsx HydroPol2D_Inputs.xlsx
```

El constructor traslada cada valor, ruta de mapa, lista de mapas y estación, y copia las tablas de clases y las series de los libros de Excel ubicados junto al archivo de origen. Una serie que los interruptores del caso no leen se conserva como una plantilla vacía con sus encabezados. El caso en V da resultados idénticos con cualquiera de los dos formatos (`Validation/Workbook/run_single_workbook_checks.m`).

Los libros de Excel antiguos ya no necesitan los interruptores retirados `flag_data_source`, `flag_dam_break` y `flag_river_heigth_compensation` (todos con valor predeterminado 0). `flag_subgrid` y `flag_overbanks` se derivan de los interruptores del canal, y `time_save_ETP` es opcional.
