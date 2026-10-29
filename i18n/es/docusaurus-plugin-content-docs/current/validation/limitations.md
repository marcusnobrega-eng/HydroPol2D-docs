---
title: Limitaciones
---

# Limitaciones de la validación

El paquete de validación actual corresponde a una campaña de verificación y de análisis de dinámica controlada. Las pruebas evalúan las ecuaciones, el almacenamiento, la interpretación de los forzamientos, las opciones de enrutamiento y las condiciones de contorno en casos con referencias conocidas.

Estas pruebas no sustituyen la calibración de campo, el análisis de incertidumbre ni la validación observacional específica de cada sitio.

## Modo de malla de Voronoi {#voronoi-mesh-mode}

La vía de volúmenes finitos en malla de Voronoi cuenta con validación controlada en CPU, pero no con validación a escala de campo. La ejecución en GPU y el rendimiento a escala de la India están bloqueados, y los canales no resueltos solo se admiten con el solucionador inercial local. Un caso que necesite enrutamiento cinemático, difusivo o de momento completo debe usar canales 2D totalmente resueltos hasta que se añada una validación propia del acoplamiento de canales.

En HydroPol2D-Python, la malla ejecuta los módulos opcionales de la malla ráster regular en su motor de CPU (NumPy): nieve, calidad del agua, inestabilidad humana, embalses, drenaje urbano, infraestructura verde y estanques de detención. Cada uno se comparó con la malla ráster en una malla formada por sus propias celdas cuadradas, donde ambas coinciden hasta el redondeo. Ninguno se ha comparado con observaciones en una malla irregular. Sus límites abiertos son los siguientes.

- el motor de malla en GPU (JAX) todavía no ejecuta estos módulos;
- la inestabilidad humana se ejecuta solo como índice de riesgo continuo (modo 1); un caso en malla con la clasificación de deslizamiento y vuelco (`human_risk.method: classification`, modo 3) se detiene en la verificación de entrada, que ofrece la malla ráster regular;
- los embalses, el drenaje urbano, la infraestructura verde y los estanques de detención requieren una malla sin canales de río ni tablas de submalla, y la calidad del agua, una malla sin canales de río;
- un embalse, un sumidero, un compartimento de infraestructura verde o un dispositivo de estanque pasa a la celda de la malla que contiene la mayor parte de su celda ráster, y un estanque ocupa las celdas de la malla que cubre en la mitad o más;
- con un exponente de lavado distinto de 1, el lavado depende de cuántas aristas atraviesa el agua al salir de una celda, de modo que una malla de Voronoi (unas seis aristas por celda) lava de forma distinta que la malla ráster (cuatro caras).

## Subsuelo en capas y calibración por recesión {#layered-subsurface-and-recession-calibration}

El subsuelo en capas cuenta con pruebas controladas y paridad entre Python y MATLAB en dominios sintéticos en V, pero no con validación de campo. Sus límites abiertos son los siguientes.

- no hay flujo lateral del agua colgada sobre regolito no saturado;
- no hay tabla de clases de regolito ni salidas ráster por capa;
- no hay franja capilar, ya que el ascenso capilar rellena el suelo por encima del nivel freático solo hasta la capacidad de campo;
- el bucle compilado de ciudad de Python todavía no ejecuta el esquema en capas con flujo lateral de agua subterránea.

La calibración por recesión se probó con un experimento gemelo en un valle sintético, no con pozos observados ni con un hidrograma de campo.

## Límites de la evidencia

Algunos casos hidrodinámicos y de agua subterránea usan referencias numéricas. Estas comparaciones permiten verificar la implementación cuando no existe una solución analítica, pero deben distinguirse de la validación analítica.

Los ejemplos aplicados, como Stanford, muestran la configuración y la ejecución del modelo. Solo constituyen validación cuando incluyen observaciones, resultados calibrados o de modelación inversa, u otra referencia independiente adecuada.

## Recesión del modelo submalla de Neal (2012)

Las pruebas del canal submalla de Neal (2012) reproducen el flujo dentro de las márgenes, la activación de la llanura, el caudal pico y la extensión máxima de inundación en las geometrías evaluadas. Una celda gruesa con canal tiene un solo nivel representativo de agua. Por ello, el agua almacenada en las banquetas internas o en la llanura externa no puede receder de forma independiente del canal embebido.

En la prueba escalonada, este comportamiento hace que la llanura del modelo de Neal (2012) se seque antes que la referencia numérica de malla fina. Las aplicaciones en las que el drenaje tardío de la llanura controla el resultado deben comparar el tiempo de recesión con observaciones o con una simulación hidráulica más fina.
