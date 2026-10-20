---
title: Limitaciones
---

# Limitaciones de la validación

El paquete actual corresponde a la validación de verificación y análisis de dinámica controlada. Las pruebas evalúan las ecuaciones, el almacenamiento, la interpretación de los forzamientos, las opciones de enrutamiento y las condiciones de contorno en casos con referencias conocidas.

Estas pruebas no sustituyen la calibración de campo, el análisis de incertidumbre ni la validación observacional específica de cada sitio.

## Límites de la evidencia

Algunos casos hidrodinámicos y de agua subterránea usan referencias numéricas. Estas comparaciones permiten verificar la implementación cuando no existe una solución analítica, pero deben distinguirse de la validación analítica.

Los ejemplos aplicados, como Stanford, muestran la configuración y la ejecución del modelo. Solo constituyen validación cuando incluyen observaciones, resultados calibrados o de modelación inversa, u otra referencia independiente adecuada.

## Recesión del modelo submalla de Neal (2012)

Las pruebas del canal submalla de Neal (2012) reproducen el flujo dentro de las márgenes, la activación de la llanura, el caudal pico y la extensión máxima de inundación en las geometrías evaluadas. Una celda gruesa con canal tiene un solo nivel representativo de agua. Por ello, el agua almacenada en las banquetas internas o en la llanura externa no puede receder de forma independiente del canal embebido.

En la prueba escalonada, este comportamiento hace que la llanura del modelo de Neal (2012) se seque antes que la referencia numérica de malla fina. Las aplicaciones en las que el drenaje tardío de la llanura controla el resultado deben comparar el tiempo de recesión con observaciones o con una simulación hidráulica más fina.
