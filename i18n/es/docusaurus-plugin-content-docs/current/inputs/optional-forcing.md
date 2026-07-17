---
title: Forzado opcional
---

# Forzado opcional

HydroPol2D admite múltiples tipos de forzamiento meteorológico e hidrológico más allá de la entrada básica de lluvia.
Todas las configuraciones de forzado se definen a través del archivo `General_Data.xlsx`, que controla:
- el tipo de forzado utilizado,
- la activación de los componentes del modelo,
- y los conjuntos de datos de entrada asociados.

El modelo puede operar bajo diferentes estrategias de forzamiento dependiendo de la disponibilidad de datos y los objetivos de la simulación.
---

## Descripción general

HydroPol2D admite las siguientes opciones de forzado:
- Forzamiento meteorológico para la evapotranspiración (Penman-Monteith)
- Entradas directas de evaporación ($E$) y transpiración ($T$)
- Forzamiento espacial de la lluvia (basado en ráster o interpolado por calibre)
- Tormentas de diseño sintético (Huff y Alternating Block)
- Hidrogramas de entrada externos
- Condiciones de contorno del escenario

Cada tipo de forzado se activa y configura a través de `General_Data.xlsx`.
---

## Forzamiento meteorológico (Penman-Monteith)

HydroPol2D calcula la evapotranspiración utilizando una formulación de Penman-Monteith cuando se proporciona forzamiento meteorológico.
### Fuente de entrada

Los datos meteorológicos se proporcionan a través de:
- `ETP_input_data.xlsx`

---

### Interpolación espacial

Las variables meteorológicas se distribuyen espacialmente mediante:
- ponderación de distancia inversa (IDW)

Esto garantiza que el forzamiento atmosférico sea consistente en todo el dominio según los puntos de medición disponibles.
---

### Variables requeridas

Las entradas típicas incluyen:
- temperatura del aire
- radiación (neta o solar)
- humedad relativa
- velocidad del viento

---

### Papel en el modelo

El forzamiento meteorológico se utiliza para calcular la evapotranspiración, que elimina agua de:
- almacenamiento en superficie
- humedad del suelo

Este enfoque se recomienda cuando se dispone de forzamiento atmosférico total.
---

## Entradas directas de evaporación y transpiración

HydroPol2D permite la especificación directa de la evaporación y la transpiración.
### Entradas

- evaporación ($E$) ráster o serie temporal
- transpiración ($T$) ráster o serie temporal

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### Papel en el modelo

Estos fundentes se aplican directamente a:
- almacenamiento de agua superficial
- humedad del suelo

Este enfoque evita la necesidad de forzamiento meteorológico.
---

## Forzamiento de lluvia

HydroPol2D admite múltiples configuraciones de entrada de lluvia.
---

### 1. Precipitaciones concentradas (uniformes)

Definido a través de:
- `Rainfall_Intensity_Data.xlsx`

---

#### Descripción

- la lluvia se aplica uniformemente sobre el dominio
- definido como una serie de tiempo

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### 2. Precipitación medida (interpolación espacial)

Definido a través de:
- `Rainfall_Spatial_Input.xlsx`

---

#### Interpolación espacial

Los campos de lluvia se calculan usando:
- ponderación de distancia inversa (IDW)

Las mediciones de calibre se interpolan en todas las celdas de la cuadrícula en función de su ubicación espacial.
---

#### Descripción

- Se pueden especificar varios calibres.
- Las precipitaciones varían espacial y temporalmente.
- adecuado para conjuntos de datos de precipitación observados

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### 3. Lluvia basada en ráster

Las precipitaciones también se pueden proporcionar como:
- pilas de ráster que varían en el tiempo

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### Papel en el modelo

Las precipitaciones impulsan:
- infiltración
- generación de escorrentía
- encaminamiento del flujo superficial

---

## Tormentas de diseño

HydroPol2D incluye generación de tormentas sintéticas incorporada.
### Métodos disponibles

- Distribuciones de resoplidos
- Método de bloque alterno

---

### Configuración

Definido a través de `General_Data.xlsx`, que incluye:
- profundidad total de lluvia
- duración de la tormenta
- distribución temporal

El modelo genera internamente el hietograma de lluvia.
---

## Hidrogramas de entrada externos

El ingreso externo se define a través de:
- `Inflow_Hydrograph.xlsx`

---

### Papel en el modelo

Utilizado para:
- condiciones de contorno aguas arriba
- afluencia del río
- escenarios de rotura de presa o afluencia controlada

---

### Implementación

- Se pueden definir múltiples calibres.
- cada calibre está asociado con coordenadas espaciales
- El flujo de entrada se distribuye en todas las celdas asociadas con cada medidor.

Unidades:
- $\mathrm{m^3\,s^{-1}}$

---

## Condiciones de límite de etapa

Las condiciones de contorno de etapa se definen a través de:
- `Stage_Hydrograph.xlsx`

---

### Papel en el modelo

Utilizado para:
- control aguas abajo
- efectos de remanso
- restricciones hidráulicas

---

### Implementación

- La etapa se prescribe como profundidad o elevación del agua.
- todas las celdas asociadas con el límite reciben el mismo valor impuesto

Unidades:
- $\mathrm{m}$

---

## Control a través de `General_Data.xlsx`

El archivo `General_Data.xlsx` define:
- qué componentes forzadores están activos
- qué conjuntos de datos se utilizan
- resolución temporal
- consistencia unitaria

Actúa como interfaz central entre las entradas definidas por el usuario y el modelo.
---

## Interacción entre componentes forzados

Las entradas forzadas interactúan de la siguiente manera:
- La lluvia introduce agua en el sistema.
- La evapotranspiración elimina el agua del almacenamiento.
- las variables meteorológicas controlan los flujos impulsados ​​por la energía
- Los hidrogramas de entrada añaden descarga externa.
- Los límites de las etapas limitan la respuesta hidráulica.

Estas interacciones definen la dinámica del sistema.
---

## Consideraciones prácticas

- Garantizar la coherencia temporal en todas las entradas de forzamiento.
- verificar las unidades antes de la simulación
- Evite mezclar resoluciones temporales incompatibles.
- Confirmar la ubicación espacial correcta de los medidores.
- Asegúrese de que las entradas de interpolación estén bien distribuidas espacialmente.
- hacer coincidir la resolución forzada con el paso de tiempo del modelo

---

## Resumen

El forzamiento opcional en HydroPol2D permite configuraciones de simulación flexibles que van desde escenarios simples impulsados ​​por la lluvia hasta sistemas meteorológicos-hidrológicos totalmente acoplados.
Todas las configuraciones de forzado se administran a través de `General_Data.xlsx`, lo que permite a los usuarios:
- cambiar entre estrategias de forzamiento
- integrar conjuntos de datos externos
- y definir eventos sintéticos

El enfoque de forzamiento seleccionado debe reflejar:
- el objetivo de la simulación
- disponibilidad de datos
- y el nivel requerido de representación física