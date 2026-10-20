---
title: Flujo de trabajo de construcción del modelo
---

# Flujo de trabajo de construcción del modelo

HydroPol2D tiene un flujo de trabajo científico para construir casos y dos motores
de modelo compatibles. El Case Builder crea el caso. HydroPol2D-Python y
HydroPol2D-MATLAB lo utilizan. La calibración del agua subterránea es un
procedimiento opcional en Python que actualiza el caso antes de lanzar cualquiera
de los dos motores.

```text
Case Builder: provisional physical domain
                    |
                    v
       Optional Python groundwater calibration
                    |
                    v
Case Builder: finalized parameters and initial states
                    |
                    v
                 Preflight
                    |
          +---------+---------+
          |                   |
          v                   v
 HydroPol2D-Python     HydroPol2D-MATLAB
          |                   |
          +---------+---------+
                    |
                    v
          Shared results and QA
```

## La regla central {#the-central-rule}

Un dominio preparado no es necesariamente un caso listo para ejecutar. Un caso
está listo para ejecutar solo después de que sus parámetros y estados iniciales
seleccionados se han escrito en los adaptadores de solucionador y de que ha
superado la verificación previa (preflight).

El directorio del caso gestionado por el Builder es la fuente de referencia. El
YAML de Python, los libros de MATLAB, los adaptadores de rutas de MATLAB y los
scripts de lanzamiento generados son vistas de ese caso para cada solucionador.
No deben adquirir configuraciones científicas independientes.

## Flujo de trabajo estándar {#standard-workflow}

Esta ruta se usa cuando los parámetros predeterminados o los suministrados por
el usuario son adecuados.

1. **Definir el experimento.** Seleccionar el dominio, la resolución del modelo,
   el período, el forzamiento, los procesos activos, el tratamiento del terreno,
   la representación del río, los adaptadores de solucionador, las variables de
   salida y el intervalo de salida.
2. **Previsualizar el dominio y el costo.** Inspeccionar la cuenca, la salida, el
   número de celdas activas, la disponibilidad de datos fuente, la memoria, la
   transferencia y las estimaciones de salidas guardadas.
3. **Preparar el caso completo.** El Builder descarga o prepara los datos fuente,
   crea el terreno hidráulico y los productos fluviales, alinea los rásteres
   estáticos, prepara el forzamiento y registra la procedencia y el control de
   calidad (QA).
4. **Finalizar parámetros y estados iniciales.** Los valores predeterminados, los
   rásteres espaciales o los valores explícitos del usuario se resuelven en los
   campos finales de la malla del modelo.
5. **Ejecutar el preflight.** El preflight verifica archivos, mallas, unidades,
   cobertura del forzamiento, condiciones de contorno, parámetros requeridos y
   combinaciones de solucionadores admitidas.
6. **Seleccionar el motor.** Ejecutar Python, MATLAB o ambos. Elegir un motor no
   reconstruye el dominio ni cambia el caso científico.
7. **Inspeccionar los resultados.** Usar las marcas de tiempo guardadas del
   modelo, los diagnósticos de balance de masa, los hidrogramas, los mapas y las
   animaciones. El tiempo de actualización de la interfaz no es tiempo del modelo.

## Flujo de trabajo calibrado con agua subterránea {#groundwater-calibrated-workflow}

La calibración del agua subterránea introduce de forma deliberada una
construcción en dos pasadas.

### Pasada 1: caso provisional {#pass-1-provisional-case}

El Builder prepara la geometría del dominio y las entradas que necesita el
experimento de calibración.

- DEM hidráulico, dominio activo, ríos, salidas y subcuencas;
- mapas de suelo, cobertura del suelo, profundidad de raíces, fondo del acuífero
  y lecho del río;
- forzamiento y registro observado de la estación de aforo, cuando está
  disponible;
- parámetros provisionales de agua subterránea suficientes para cargar el
  dominio.

Este caso provisional no es la simulación de producción.

### Calibración en Python {#python-calibration}

El procedimiento de calibración en Python realiza los pasos siguientes.

1. filtra el hidrograma observado y construye una curva maestra de recesión;
2. identifica el tiempo de respuesta del embalse lineal profundo a partir de la
   cola lenta;
3. ejecuta el período de calentamiento (spin-up) y la liberación del acuífero de
   Boussinesq distribuido;
4. estima la conductividad horizontal uniforme efectiva y el rendimiento
   específico;
5. guarda el campo de carga del agua subterránea, el almacenamiento somero y el
   caudal somero en cada estado de la recesión;
6. escribe los diagnósticos de calibración y el archivo de estados de vuelta en
   el directorio del caso.

La calibración se implementa una sola vez, en Python. MATLAB no repite este
procedimiento inverso.

### Pasada 2: caso final {#pass-2-final-case}

El Builder importa los artefactos de calibración aceptados y resuelve las
condiciones iniciales finales.

- un estado del acuífero somero seleccionado según el agotamiento normalizado
  del almacenamiento;
- un caudal profundo igual al flujo base inicial filtrado menos el caudal somero
  seleccionado;
- un almacenamiento profundo igual al caudal profundo multiplicado por el tiempo
  de respuesta calibrado;
- la fracción configurada de la recarga futura enrutada hacia el embalse
  profundo;
- humedad cercana a la superficie y de la zona de raíces al inicio del evento, a
  partir de campos de ERA5-Land con información de profundidad;
- humedad de la zona de transmisión a partir del drenaje gravitacional
  estacionario y de la influencia capilar del nivel freático seleccionado.

Luego, el Builder regenera los dos adaptadores de solucionador solicitados y
vuelve a ejecutar el preflight. Solo este caso finalizado debe usarse para la
simulación de producción.

En el Builder, se elige **Calibrate from observed streamflow** en
**Hydraulic parameters**. Una vez preparado el caso provisional, se abre en
**Check a case**. Allí, el panel de calibración acepta un identificador de
estación de aforo del USGS o un CSV local, valores candidatos de `Ksat,h` y `Sy`,
y la fracción normalizada de agotamiento del almacenamiento somero. La
calibración se ejecuta en segundo plano y continúa aunque se cierre la pestaña
del navegador. **Refresh calibration status** lee el progreso y los artefactos
guardados. Un trabajo exitoso aplica el resultado y vuelve a ejecutar el
preflight.

El estado vadoso finalizado conserva información vertical. Las capas de
ERA5-Land se promedian según su superposición en profundidad para el
almacenamiento superficial de 0.05 m y para la zona de raíces derivada de LULC.
El almacenamiento de transmisión se inicializa con un perfil de equilibrio de
van Genuchten condicionado al nivel freático seleccionado. Ambos solucionadores
leen estos tres mapas, mientras que los casos anteriores con una sola humedad
conservan su alternativa documentada.

### Casos con subsuelo en capas {#layered-subsurface-cases}

Con `--subsurface-scheme layered` (`legacy` por defecto), el Builder prepara un
caso con [subsuelo en capas](../theory/layered-subsurface) para Python, MATLAB o
ambos.

1. **Entradas globales.** Deriva la base del suelo a partir de SoilGrids BDRICM,
   los parámetros de van Genuchten del regolito a partir de la clase textural a
   200 cm y la conductividad del regolito a partir de GLHYMPS 2.0. Las reglas se
   describen en las páginas
   [Suelo](../inputs/soil#global-sources-used-by-the-case-builder) y
   [DTB](../inputs/dtb#global-sources-used-by-the-case-builder).
2. **Adaptadores de solucionador.** El caso de Python recibe
   `vertical.subsurface.scheme: layered` y las rutas estáticas. El adaptador de
   MATLAB pasa los rásteres de base del suelo y del regolito, y
   `HYDROPOL_SUBSURFACE_SCHEME`.
3. **Estado inicial del acuífero profundo.** `--deep-aquifer-initial-baseflow-mm-day`
   o `--deep-aquifer-mean-recharge-mm-year` (como máximo uno de ellos) define el
   almacenamiento inicial de los embalses profundos. El archivo
   `DeepAquiferInitialState.json` de una calibración reemplaza a ambos.
4. **Calibración.** En los casos en capas, la calibración por recesión ajusta dos
   multiplicadores de la conductividad lateral, uno para las capas de suelo y
   otro para las capas de regolito, en lugar de `Ksat,h` y `Sy`. La finalización
   los escribe en el caso de Python y en el ejecutor de MATLAB. $S_y$ permanece
   en las curvas de retención. Ver
   [Calibración por Recesión del Agua Subterránea](../calibration/groundwater-recession).

## Responsabilidades de los componentes {#component-responsibilities}

| Componente | Es responsable de | No es responsable de |
|---|---|---|
| Case Builder | Dominio, datos fuente, terreno, productos de río y submalla, forzamiento, mapas de parámetros alineados, estados iniciales, adaptadores de solucionador, procedencia y preflight | Avance numérico en el tiempo o inversión de parámetros |
| Calibración del agua subterránea | Análisis de la recesión maestra, parámetros efectivos del acuífero somero, tiempo de respuesta profundo y archivo guardado de estados someros | Preparación del terreno, descargas del forzamiento de producción o un segundo formato de caso |
| HydroPol2D-Python | Implementación científica de referencia, entorno de ejecución de la calibración, simulación, pruebas y salidas estándar | Reconstrucción independiente de la geometría del Builder |
| HydroPol2D-MATLAB | Simulación compatible del caso finalizado y verificación entre lenguajes | Un flujo de calibración separado o valores predeterminados del Builder independientes |
| Interfaz de resultados | Lee las salidas guardadas de los solucionadores y sus marcas de tiempo del modelo | Cambiar parámetros o definir el estado de la simulación durante la actualización |

## Estados del caso {#case-states}

| Estado | Significado | ¿Se puede ejecutar? |
|---|---|---:|
| Borrador (Draft) | La configuración todavía se está editando. | No |
| Previsualizado (Previewed) | Se inspeccionaron el dominio y el costo, pero puede que no existan entradas completas. | No |
| Provisional | Existe el dominio físico y puede usarse para la calibración. | Solo calibración |
| Finalizado (Finalized) | Los parámetros y estados iniciales aceptados se escribieron en los adaptadores de solucionador. | Todavía no |
| Preflight aceptado (Preflight accepted) | Se superaron todas las verificaciones de archivos requeridos y de compatibilidad. | Sí |
| En ejecución (Running) | Un solucionador está avanzando el caso finalizado. | En curso |
| Completo (Complete) | El solucionador terminó correctamente y escribió las salidas solicitadas. | Terminado |

El preflight establece consistencia interna, no exactitud hidrológica. Un
conjunto de parámetros calibrado establece una hipótesis ajustada, no una verdad
de campo universal. Ambas distinciones deben seguir visibles en la interfaz y en
los informes.

## Elección entre Python y MATLAB {#choosing-python-or-matlab}

- Usar **Python** para la calibración del agua subterránea, los diagnósticos
  rápidos, las pruebas automatizadas y el flujo de trabajo científico de
  referencia actual.
- Usar **MATLAB** cuando el caso finalizado requiere la implementación de MATLAB
  o un flujo de trabajo de producción existente en MATLAB.
- Usar **ambos** para estudios de paridad. Ambos adaptadores deben provenir del
  mismo caso finalizado del Builder y usar parámetros, forzamiento, estados
  iniciales, contornos y frecuencia de salida idénticos.

Los flujos de trabajo independientes con YAML de Python y Excel de MATLAB siguen
siendo útiles para ejemplos y pruebas controladas. Están separados de un caso
científico gestionado por el Builder y no deben mezclarse con él de forma
silenciosa.
