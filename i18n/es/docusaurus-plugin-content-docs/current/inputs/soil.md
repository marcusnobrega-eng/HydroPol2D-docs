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