---
title: Albedo
---

# Albedo

El albedo representa la fracción de la radiación de onda corta entrante que se refleja en la superficie.
En HydroPol2D, el albedo se utiliza para caracterizar las propiedades radiativas de la superficie y su influencia en los procesos relacionados con la energía, en particular la evapotranspiración y la dinámica de la nieve.

---

## Papel en HydroPol2D

Albedo se utiliza para representar:
- Reflectividad de la superficie a la radiación solar entrante.
- Energía disponible para la evapotranspiración
- Condiciones del balance de energía superficial.
- Comportamiento del deshielo (cuando se activan los procesos de nieve)

Las superficies con albedo más bajo absorben más energía, mientras que las superficies con albedo más alto reflejan una fracción mayor de la radiación entrante.

---

## Representación

Albedo se proporciona como un **mapa ráster continuo**, donde cada celda de la cuadrícula contiene un valor entre 0 y 1.
Los valores típicos incluyen:
- 0,05 – 0,15 → cuerpos de agua, superficies oscuras
- 0,15 – 0,25 → vegetación
- 0,25 – 0,40 → suelos secos
- 0,60 – 0,90 → superficies nevadas

Los valores deben ser físicamente consistentes con la cobertura del suelo y las condiciones ambientales.

---

## Representación Temporal

En la implementación actual de HydroPol2D, el albedo se trata como una **entrada estática**.
Los usuarios deben seleccionar valores representativos de las condiciones de simulación:
- Simulaciones a largo plazo → use albedo promedio o mediano
- Simulaciones estacionales → utilizar valores consistentes con la condición de superficie dominante

Las variaciones dinámicas del albedo (por ejemplo, debido a la capa de nieve o cambios en la vegetación) no se resuelven explícitamente a menos que se proporcionen externamente.

---

## Fuentes de datos

Varios conjuntos de datos proporcionan estimaciones del albedo global:
### MODIS Albedo (MCD43A3)
- Región: Global
- Resolución: 500 m
- Resolución temporal: 16 días
- Producto derivado de satélite ampliamente utilizado
- Descargar: https://lpdaac.usgs.gov/products/mcd43a3v061/

---

### Servicio Terrestre Global Copernicus (Albedo)
- Región: Global
- Resolución: 300 m
- Derivado de observaciones satelitales
- Descargar: https://land.copernicus.eu/global/products/albedo

---

### Google Earth Engine

Los conjuntos de datos de albedo de MODIS y Copernicus están disponibles en Google Earth Engine y pueden procesarse para extraer valores representativos para el dominio de simulación.

---

## Coherencia con otras entradas

Albedo debe ser consistente con:
- **LULC** → define el tipo de superficie
- **LAI** → refleja la densidad de la vegetación
- **Condiciones de nieve** → influyen fuertemente en la reflectividad

Los valores de albedo inconsistentes pueden llevar a una partición de energía poco realista.

---

## Consideraciones prácticas

Al preparar entradas de albedo:
- Evite los valores extremos o no físicos.
- Utilice valores agregados temporalmente cuando sea necesario
- Garantizar la alineación espacial con todas las entradas ráster
- Verificar la coherencia con la cobertura del suelo y las condiciones climáticas.

Si no hay ningún conjunto de datos de albedo disponible, se pueden asignar valores basados ​​en clases LULC, con la justificación adecuada.

---

## Resumen

Albedo define las propiedades radiativas de la superficie en HydroPol2D e influye en los procesos impulsados ​​por la energía, como la evapotranspiración y el deshielo.
Aunque de estructura simple, desempeña un papel importante a la hora de garantizar una representación físicamente consistente de las interacciones superficie-atmósfera.