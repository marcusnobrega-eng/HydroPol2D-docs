---
title: Resumen
---

# Configuración del modelo

En el modo Excel de MATLAB, un caso de HydroPol2D es un solo libro de Excel, `HydroPol2D_Inputs.xlsx`. Sus pestañas de parámetros seleccionan el conjunto de procesos, la familia de enrutamiento, los controles del agua subterránea, los archivos de entrada y los diagnósticos opcionales. Sus otras pestañas contienen las tablas de clases y las series temporales. Los casos antiguos con `General_Data.xlsx` y libros de Excel separados siguen funcionando (ver [Ejecutar desde Excel](../getting-started/excel-workflow#older-layout)). HydroPol2D-Python lee los mismos parámetros desde el YAML de su caso.

Las páginas de configuración y teoría cumplen funciones distintas:

- la teoría explica lo que hace cada módulo;
- la configuración explica qué controles públicos exponen ese comportamiento.

## Lógica actual de configuración

La configuración pública debe coincidir con el modelo implementado:

- el almacenamiento vadoso en capas y el acoplamiento con groundwater son la ruta por defecto cuando el groundwater está activo;
- la familia de enrutamiento incluye local inertial, full momentum, diffusive D4, kinematic D4 y cellular automata;
- solo una familia principal de enrutamiento debe estar activa por simulación.

## Capacidades y madurez

| Capacidad | Principales controles públicos | Estado actual |
|---|---|---|
| Núcleo hidrologico | `flag_infiltration`, controles de ET, lluvia y nieve, tablas de suelo y LULC | Predeterminado + validado |
| Recarga subterránea en capas y programador asíncrono | `flag_groundwater_modeling`, `groundwater_target_dt_min`, `groundwater_min_dt_min`, `groundwater_max_head_change_m`, `groundwater_courant` | Predeterminado + validado |
| Ascenso capilar | `flag_capillary_rise` | Opcional + validado en benchmarks controlados |
| Subsuelo en capas | `flag_layered_subsurface`, `flag_implicit_water_table_flux` | Opcional + pruebas controladas y paridad Python-MATLAB |
| Estrés de Feddes en la absorción de agua por las raíces | `flag_feddes` | Opcional + pruebas de consistencia |
| Acuífero profundo | `flag_deep_aquifer` | Opcional + pruebas con fixtures del estado inicial |
| Enrutamiento local inertial | `flag_inertial`, `flag_numerical_scheme` | Predeterminado + validado |
| Enrutamiento full momentum | `flag_full_momentum` | Opcional + validado en benchmarks controlados |
| Enrutamiento diffusive | `flag_diffusive` | Opcional + validado en benchmarks controlados |
| Enrutamiento kinematic | `flag_kinematic` | Opcional + validado en benchmarks controlados |
| Cellular automata | `flag_CA` | Opcional + validado para conservación y bookkeeping |
| Inestabilidad humana | `flag_human_instability` | Opcional + validada para los modos `1` y `3` |

## Principales dominios de configuración

### 1. Control de simulación y forzantes

Las pestañas Run control, Rain and ET, Design storm y Surface flow definen el tiempo de simulación, los forzamientos de lluvia y meteorológicos, las condiciones de contorno de caudal de entrada y de nivel, la frecuencia de salida y las opciones de ejecución, como el paso de tiempo adaptativo o la ejecución en GPU. Todos los parámetros se listan en [Parámetros del libro del caso](./general_data).

### 2. Selección de la familia de enrutamiento

La interfaz pública de enrutamiento incluye:

- `flag_inertial`
- `flag_full_momentum`
- `flag_diffusive`
- `flag_kinematic`
- `flag_CA`

Solo una de estas flags principales debe estar activa en cada simulación. D8 existe como ruta secundaria y no debe documentarse como una familia teórica paralela.

### 3. Controles de groundwater

Cuando el groundwater está activo, HydroPol2D expone comportamientos que deben documentarse de forma explícita:

- actualizaciones asíncronas del groundwater saturado;
- resoluciones disparadas por cambios acumulados de carga;
- límite explícito de estabilidad para el time step del groundwater;
- ascenso capilar opcional;
- flujo lateral de Boussinesq cuando el baseflow está activo.

### 4. Diagnósticos de riesgo y calidad del agua

Módulos opcionales, como calidad del agua e inestabilidad humana, tienen flags y parámetros propios. Para inestabilidad humana, la documentación pública debe reflejar que:

- el modo `1` está implementado;
- el modo `3` está implementado;
- el modo `2` no está implementado.

## Lectura recomendada de una configuración

En simulaciones publicas de HydroPol2D, debe quedar claro:

1. qué familia de enrutamiento está activa;
2. si el groundwater está acoplado solo localmente o también lateralmente mediante Boussinesq;
3. si el ascenso capilar está activo;
4. si los diagnósticos de inestabilidad humana o calidad del agua están activos.

Si esas cuatro preguntas quedan claras, la configuración está alineada con la historia actual del modelo.
