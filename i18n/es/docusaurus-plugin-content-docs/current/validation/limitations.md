---
title: Limitaciones
---

# Limitaciones de la validación

El paquete de validación actual corresponde a una campaña de verificación y de análisis de dinámica controlada. Las pruebas evalúan las ecuaciones, el almacenamiento, la interpretación de los forzamientos, las opciones de enrutamiento y las condiciones de contorno en casos con referencias conocidas.

Estas pruebas no sustituyen la calibración de campo, el análisis de incertidumbre ni la validación observacional específica de cada sitio.

## Subsuelo en capas y calibración por recesión {#layered-subsurface-and-recession-calibration}

El subsuelo en capas cuenta con pruebas controladas y paridad entre Python y MATLAB en dominios sintéticos en V, pero no con validación de campo. Sus límites abiertos son los siguientes.

- no hay flujo lateral del agua colgada sobre regolito no saturado;
- no hay tabla de clases de regolito ni salidas ráster por capa;
- el agua circula hacia arriba y hacia abajo cerca de un nivel freático somero, lo que infla el ascenso capilar bruto y la recarga bruta en el balance, mientras el valor neto se mantiene cercano a cero;
- el flujo implícito en el nivel freático solo se prueba en Python;
- el bucle compilado de ciudad de Python todavía no ejecuta el esquema en capas con flujo lateral de agua subterránea.

La calibración por recesión se probó con un experimento gemelo en un valle sintético, no con pozos observados ni con un hidrograma de campo.

## Límites de la evidencia

Algunos casos hidrodinámicos y de agua subterránea usan referencias numéricas. Estas comparaciones permiten verificar la implementación cuando no existe una solución analítica, pero deben distinguirse de la validación analítica.

Los ejemplos aplicados, como Stanford, muestran la configuración y la ejecución del modelo. Solo constituyen validación cuando incluyen observaciones, resultados calibrados o de modelación inversa, u otra referencia independiente adecuada.

## Recesión del modelo submalla de Neal (2012)

Las pruebas del canal submalla de Neal (2012) reproducen el flujo dentro de las márgenes, la activación de la llanura, el caudal pico y la extensión máxima de inundación en las geometrías evaluadas. Una celda gruesa con canal tiene un solo nivel representativo de agua. Por ello, el agua almacenada en las banquetas internas o en la llanura externa no puede receder de forma independiente del canal embebido.

En la prueba escalonada, este comportamiento hace que la llanura del modelo de Neal (2012) se seque antes que la referencia numérica de malla fina. Las aplicaciones en las que el drenaje tardío de la llanura controla el resultado deben comparar el tiempo de recesión con observaciones o con una simulación hidráulica más fina.
