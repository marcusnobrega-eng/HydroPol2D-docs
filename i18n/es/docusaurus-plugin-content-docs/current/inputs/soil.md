---
title: Suelo
---

# Propiedades del suelo

Los datos del suelo definen la respuesta hidráulica de la superficie terrestre y controlan la velocidad a la que el agua se infiltra en el subsuelo en HydroPol2D.
Dentro de la formulación actual del modelo, las propiedades del suelo se utilizan para estimar **la capacidad de infiltración, el almacenamiento en capas de la zona vadosa, el drenaje/recarga, el ascenso capilar y el comportamiento del almacenamiento de agua subterránea**.

---

## Papel en HydroPol2D

La entrada de suelo se utiliza para representar:
- Capacidad de infiltración en la superficie.
- Almacenamiento de agua cerca de la superficie, en la zona de las raíces y en la zona de transmisión
- Conductividad hidráulica efectiva por capa.
- Condiciones iniciales de humedad del suelo (cuando no se proporciona como campo espacial)
- Rendimiento específico del agua subterránea y conductividad hidráulica saturada.

Estas propiedades influyen directamente en la generación de escorrentía y el momento de la respuesta hidrológica.

---

## Representación del suelo

HydroPol2D requiere un **mapa de suelo categórico**.
A cada celda de la cuadrícula se le debe asignar un identificador de clase de suelo, que luego se vincula a un conjunto de parámetros hidráulicos a través de las tablas de entrada.
Esta estructura permite al modelo:
- Asignar propiedades hidráulicas distribuidas espacialmente
- Mantenga la coherencia en todo el dominio
- Separar los datos espaciales de la definición de parámetros

El mapa de suelo todavía proporciona una clase de suelo categórica por celda del modelo. Esa clase define los parámetros hidráulicos base para la columna. La implementación en capas actual divide la profundidad vadosa disponible en:
- una capa cercana a la superficie, con una profundidad objetivo predeterminada de $0.10\,\mathrm{m}$;
- una capa de zona raíz, cuya profundidad está definida por la clase LULC;
- una capa de zona de transmisión debajo de la zona de raíz;
- una zona de agua subterránea que comienza en el nivel freático actual.

La geometría de la capa se adapta a la profundidad, al lecho rocoso y a la posición del agua subterránea. Si la profundidad de la raíz es menor que la capa cercana a la superficie, la capa explícita de la zona de la raíz colapsa en la capa cercana a la superficie. Si el lecho de roca o el nivel freático es menos profundo que la profundidad de raíz solicitada, la zona de raíz se trunca a la profundidad vadosa disponible.

Este es el esquema predeterminado. El [subsuelo en capas](#soil-and-regolith-in-the-layered-subsurface) opcional conserva las mismas tres capas de suelo, pero coloca debajo de ellas capas de regolito con sus propios parámetros.

---

## Parámetros requeridos del suelo

Los parámetros hidráulicos se definen externamente y se asocian con las clases de suelo. Los parámetros típicos incluyen:
- Conductividad hidráulica saturada (Ks)
- Porosidad del suelo
- Contenido de agua residual
- Parámetros de retención de agua del suelo (por ejemplo, parámetros de Van Genuchten)
- Humedad inicial del suelo (cuando no está prescrita como campo espacial)
- Rendimiento específico y conductividad saturada del agua subterránea.
- Multiplicadores de capa opcionales para conductividad hidráulica saturada

Estos parámetros deben ser físicamente consistentes y representativos de las clases de suelo definidas en el ráster.

---

## Suelo y regolito en el subsuelo en capas {#soil-and-regolith-in-the-layered-subsurface}

Con el [subsuelo en capas](../theory/layered-subsurface), la columna tiene tres capas de suelo por encima de la base del suelo y capas de regolito por debajo. Cada capa tiene su propia curva de van Genuchten.

### Capas de suelo {#soil-slots}

Las tres capas de suelo usan los parámetros de la clase de suelo, que son `ksat` con los tres multiplicadores de capa, `n`, `alpha`, `θsat`, `θr` y `l_vg`. Dos columnas de la tabla de suelos cambian de función.

| Columna | Esquema predeterminado | Subsuelo en capas |
|---|---|---|
| `Sy` | Rendimiento específico del acuífero | Se ignora. Cada capa toma $S_y$ de su curva de retención. |
| `kgsat` | Conductividad lateral del acuífero | Conductividad horizontal de las capas de regolito, usada cuando `regolith_ksat_h_mm_h` está vacío |

El rendimiento específico de cada capa es la porosidad drenable a capacidad de campo,

$$
S_y = \theta_s - \theta\left(\psi = -h_{fc}\right)
$$

con $h_{fc}$ = `capillary_field_capacity_head_m` (3.3 m por defecto). En HydroPol2D-Python, el esquema en capas no usa `vertical.specific_yield` ni `static.specific_yield_path`. Si se indica esa ruta, se emite una advertencia.

La conductividad horizontal de las capas de suelo es `ksat` × `soil_lateral_anisotropy` (1 por defecto) × `soil_lateral_conductivity_multiplier` (1 por defecto).

### Capas de regolito {#regolith-slots}

Los parámetros del regolito son escalares o rásteres. Un ráster tiene prioridad donde es finito, y el escalar completa el resto.

| Parámetro | Unidades | Predeterminado | Ráster de MATLAB (pestaña Soil and groundwater) | Ráster de Python |
|---|---|---|---|---|
| `regolith_theta_s` | m³/m³ | 0.35 | `RegolithThetaS_path` | `static.regolith_theta_s_path` |
| `regolith_theta_r` | m³/m³ | 0.05 | `RegolithThetaR_path` | `static.regolith_theta_r_path` |
| `regolith_alpha_vg_m_inverse` | 1/m | 2.0 | `RegolithAlphaVG_path` | `static.regolith_alpha_vg_m_inverse_path` |
| `regolith_n_vg` | - | 1.5 | `RegolithNVG_path` | `static.regolith_n_vg_path` |
| `regolith_ksat_v_mm_h` | mm/h | 5.0 | `RegolithKsatV_path` | `static.regolith_ksat_v_mm_h_path` |
| `regolith_ksat_h_mm_h` | mm/h | vacío: `kgsat` | `RegolithKsatH_path` | `static.regolith_ksat_h_mm_h_path` |
| `regolith_specific_yield` | - | vacío: $\theta_s - \theta_{fc}$ | `RegolithSpecificYield_path` | `static.regolith_specific_yield_path` |

Un $S_y$ del regolito indicado debe estar en $(0,\ \theta_s - \theta_r]$. La conductividad horizontal de las capas de regolito se multiplica por `regolith_lateral_conductivity_multiplier` (1 por defecto).

Todavía no hay una tabla de clases de regolito. Las propiedades del regolito solo pueden ser escalares o rásteres.

### Mapas de propiedades del suelo {#soil-property-maps}

Las propiedades del suelo también pueden provenir de rásteres. Las celdas finitas sobrescriben el valor de la clase de suelo, y las celdas sin datos (nodata) lo conservan. En el modo Excel de MATLAB, los mapas forman el bloque "Soil-property maps" de la pestaña Input maps (desde 2026-10-20). En el modo bypass, son los mapas del Case Builder.

| Mapa | Sobrescribe |
|---|---|
| `ThetaS_path`, `ThetaR_path` | $\theta_s$, $\theta_r$ |
| `AlphaVG_path`, `NVG_path` | $\alpha$ y $n$ de van Genuchten |
| `KsatNearSurface_path`, `KsatRootZone_path`, `KsatTransmission_path` | $K_{sat}$ de las tres capas de suelo |
| `GroundwaterKsat_path` | `kgsat` |
| `SpecificYield_path` | `Sy` (solo el esquema de agua subterránea predeterminado) |

Una ruta que no corresponde a un archivo genera una advertencia.

### Cargas de absorción de agua por las raíces {#root-water-uptake-heads}

Las cargas de Feddes $h_1$ a $h_4$ son parámetros globales, no parámetros de la clase de suelo. Ver [Modelo hidrológico, sección 3.5](../theory/hydrologic-model#35-feddes-root-water-uptake-stress).

### Fuentes globales usadas por el Case Builder {#global-sources-used-by-the-case-builder}

El Case Builder (`--subsurface-scheme layered`) deriva los mapas del regolito a partir de datos globales, por lo que las mismas reglas se aplican a cualquier dominio.

| Mapa | Regla | Fuente |
|---|---|---|
| `RegolithThetaS/ThetaR/AlphaVG/NVG.tif` | Clase textural del USDA a 200 cm, asignada a parámetros de van Genuchten mediante la tabla de suelos del Builder | OpenLandMap texture v0.2, 200 cm |
| `RegolithKsatH.tif` | Permeabilidad × $\rho g/\mu$ a 20 °C. Donde GLHYMPS no tiene polígono, se usa el Ksat de agua subterránea de la clase textural a 200 cm. | Teselas globales de GLHYMPS 2.0 (Gleeson et al., 2014; Huscroft et al., 2018) |
| `RegolithKsatV.tif` | `RegolithKsatH` ÷ `groundwater_vertical_anisotropy_ratio` | - |
| `RegolithSpecificYield.tif` | Regla predeterminada `derived_capped`: $\theta_s - \theta(3.3\ \mathrm{m})$, limitado por la porosidad de GLHYMPS; sin datos (nodata) donde falta GLHYMPS, de modo que el modelo deriva $S_y$ allí. Con `derived`, no se escribe ningún mapa. | `--regolith-specific-yield-rule` |

Las teselas de GLHYMPS se descargan una vez, se verifican con el SHA-256 del manifiesto y se guardan en caché. La procedencia, la cobertura y las estadísticas se escriben en `quality_report/layered_subsurface_rasters.json`. En los casos en capas, el Builder no conecta `SpecificYield.tif` al caso.

---

## Fuentes de datos del suelo

Se pueden utilizar varios conjuntos de datos para derivar clasificaciones de suelos y parámetros hidráulicos asociados.
### Redes de suelo (ISRIC)
- Región: Global
- Resolución: hasta 250 m
- Proporciona estimaciones continuas de las propiedades del suelo (textura, densidad aparente, contenido orgánico)
- Puede usarse para derivar clases de textura del suelo del USDA
- Descargar: https://soilgrids.org/

---

### FAO / HWSD (Base de datos mundial armonizada sobre suelos)
- Región: Global
- Resolución más gruesa
- Proporciona unidades de mapeo de suelos y propiedades asociadas.
- Adecuado para aplicaciones continentales y a gran escala
- Descargar: https://www.fao.org/soils-portal/data-hub/en/

---

### Clasificación de suelos del USDA (basada en textura)

HydroPol2D comúnmente se basa en **clases de textura del suelo del USDA** (por ejemplo, arena, marga, arcilla) para definir el comportamiento hidráulico.
Estas clases se pueden derivar de:
- Fracciones de textura SoilGrids
- Bases de datos de suelos de la FAO
- Estudios regionales de suelos

Este enfoque proporciona un marco consistente para asignar parámetros hidráulicos como conductividad y características de retención.

---

### SSURGO (Base de datos geográfica de estudios de suelos)
- Región: Estados Unidos
- Resolución espacial muy alta
- Taxonomía detallada del suelo y propiedades físicas.
- Recomendado para aplicaciones de alta resolución
- Descargar: https://websoilsurvey.sc.egov.usda.gov/

---

### STATSGO (Base de datos geográfica estatal de suelos)
- Región: Estados Unidos
- Resolución más gruesa que SSURGO
- Adecuado para estudios regionales a continentales.
- Descargar: https://www.nrcs.usda.gov/resources/data-and-reports/statsgo


## Asociación de parámetros

Las clases de suelo no se utilizan directamente en las ecuaciones rectoras. En cambio, sirven como **índices en tablas de parámetros**.
Cada clase de suelo debe estar asociada con un conjunto consistente de propiedades hidráulicas. La calidad de este mapeo tiene un impacto directo en el rendimiento del modelo.
Los usuarios son responsables de garantizar que:
- Los valores de los parámetros son físicamente realistas.
- Las unidades son consistentes
- Las clases de suelo están adecuadamente definidas e interpretadas.

---

## Resolución y alineación

La trama del suelo debe:
- Coincidir o volver a muestrear con la resolución DEM
- Utilice el mismo sistema de referencia de coordenadas proyectadas (CRS)
- Alinear espacialmente con todas las demás entradas ráster

Cualquier discrepancia en la resolución o alineación dará como resultado una asignación espacial incorrecta de las propiedades del suelo.

---

## Consideraciones prácticas

Al preparar los insumos del suelo:
- Prefiera representaciones categóricas a conjuntos de datos continuos sin procesar
- Agregar clasificaciones detalladas de suelos cuando sea necesario.
- Evite valores de parámetros extremos o no físicos
- Verificar la coherencia entre las clases ráster y las tablas de parámetros

En muchos casos, simplificar el número de clases de suelo mejora la estabilidad y la interpretabilidad del modelo.

---

## Resumen

En HydroPol2D, los datos del suelo se utilizan para controlar la infiltración, el almacenamiento vadoso en capas, la recarga, el almacenamiento de agua subterránea y la retroalimentación del agua subterránea a la superficie.
El modelo se basa en una representación categórica del suelo junto con parámetros hidráulicos definidos externamente, profundidades de la zona de raíces basadas en LULC y multiplicadores de capas opcionales. La definición y el mapeo adecuados de estos parámetros son esenciales para obtener simulaciones confiables.