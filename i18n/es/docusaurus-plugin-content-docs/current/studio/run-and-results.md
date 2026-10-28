---
title: Ejecución y resultados
---

# Ejecución y resultados

## Run {#run}

El espacio de trabajo Run tiene dos paneles.

- **Outputs**: el perfil de salida, la carpeta de salida, los intervalos de registro de mapas, series
  temporales, salida nativa de la malla y pilas de rásteres, cómo se almacenan los mapas durante la
  simulación y los ajustes de animación.
- **Computing backend**: los backends que este equipo puede ejecutar. En las apps para Mac y
  Windows es la CPU; las GPU de Apple no tienen la aritmética de 64 bits que el modelo necesita.
- **Save results to**: la carpeta de esta simulación. Puede escribir otra carpeta solo para esta
  simulación; **Show in Finder** (Explorer en Windows) la abre.
- **Check inputs** ejecuta la verificación de entradas, **Run model** inicia la simulación y
  **Cancel run** la detiene. Run verifica primero las entradas.
- **Live diagnostics** grafica la simulación en cada intervalo guardado, y el registro de la
  simulación lista cada paso.

## Results {#results}

**Results** abre la salida de una simulación, o un paquete de resultados abierto desde la pantalla
Home. Tiene su propio panel de capas, así que cambiar una superposición de resultados no cambia el
mapa de Study area.

- La reproducción avanza hacia adelante o hacia atrás y puede repetirse en bucle, avanzar fotograma a
  fotograma o saltar a un tiempo transcurrido o a una fecha del calendario. Los mapas de máximo,
  mínimo y final resumen la variable activa sin modificar el archivo.
- Haga clic derecho en una celda de resultados para graficar su serie temporal guardada, exportar los
  datos de la celda, inspeccionar todas las variables de mapa guardadas o iniciar una línea de
  perfil.
- Los mapas se exportan en PNG, PDF, SVG, GeoTIFF o MP4. Los gráficos de series temporales mantienen
  variables independientes en los ejes izquierdo y derecho y se exportan en PNG, PDF, SVG o CSV.
- En el drenaje urbano, las tuberías, los pozos de registro, los sumideros y las condiciones de
  contorno internas aceptadas se pueden colorear según una magnitud guardada en el tiempo
  seleccionado, y cada uno también está disponible como una serie temporal con nombre.
