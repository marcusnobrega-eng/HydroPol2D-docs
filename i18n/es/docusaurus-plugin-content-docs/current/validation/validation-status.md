---
title: Estado de validación
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Estado de validación

El <a href={useBaseUrl('/reports/validation_report.pdf')}>informe de validación</a> documenta los métodos, métricas y resultados de la suite de validación de HydroPol2D. La tabla presenta un índice conciso de la evidencia disponible.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Abrir el informe de validación
  </a>
</div>

| Módulo | Estado | Evidencia |
|---|---|---|
| Intercepción del dosel | Validado | Referencia independiente de almacenamiento del dosel y balance exacto de masa. |
| Nieve | Validado | Parámetros por LULC, mapas iniciales opcionales, refinamiento temporal, equivalencia entre hoja de cálculo y script, y balance del evento en V. |
| Infiltración | Validado | Casos analíticos y de suelo estratificado en dominios de columna y en V. |
| Evapotranspiración | Validado | Cálculos independientes de ET de referencia y límites de extracción. |
| Aguas subterráneas y recarga | Validado | Pruebas de ascenso del nivel freático, programación, ascenso capilar y laderas analíticas. |
| Subsuelo en capas (opcional) | Pruebas controladas y paridad Python-MATLAB | Paridad de núcleos y de pasos de la columna (flujo implícito en ambos modelos), simulaciones del modelo completo en V, cierre de masa en la malla de Voronoi y pruebas del flujo implícito y del rellenado capilar. Sin caso de campo. |
| Estrés hídrico de Feddes en las raíces (opcional) | Pruebas controladas de consistencia | La ET de Feddes del esquema predeterminado y la del esquema en capas coinciden para el mismo estado; Feddes nunca supera la absorción sin estrés. |
| Estado inicial del acuífero profundo (opcional) | Paridad con fixtures | $S_0 = q_0 A \tau$ verificado en Python y MATLAB con un fixture compartido. |
| Calibración por recesión en capas | Solo experimento gemelo | Multiplicadores conocidos recuperados con 0, 5 y 10 % de ruido en un valle sintético, como el único par aceptable. Sin prueba de campo. |
| Secciones transversales de caudal en las estaciones (MATLAB) | Verificaciones controladas | Caudal en la sección transversal en el caso en V, con ambas convenciones de caras del enrutamiento; 3 de 3 verificaciones. |
| Libro del caso único (MATLAB) | Verificación de equivalencia | El caso en V da resultados idénticos desde `HydroPol2D_Inputs.xlsx` y desde el formato anterior con `General_Data.xlsx`; 3 de 3 verificaciones. |
| Hidrodinámica de momento completo | Validado | Plano inclinado, cuenca en V, rotura de presa de Ritter, onda no rompiente y contornos. |
| Hidrodinámica inercial local | Validado | Plano inclinado, cuenca en V, contorno de nivel y conservación. |
| Autómatas celulares | Validado | Casos de cuenca en V, plano y condiciones de contorno. |
| Ondas cinemática y difusiva | Validado | Benchmarks de plano, cuenca en V y contorno de nivel adecuados para las ecuaciones reducidas. |
| Modelo subgrid de Neal (2012) | Validado para las geometrías evaluadas | Referencias de malla fina para flujo en canal, canal compuesto, activación de márgenes y extensión inundada. |
| Malla de volúmenes finitos de Voronoi | Validación controlada en CPU | Inercial local con el grafo de Neal; cinemática, difusiva y momento completo en 2D resuelto. Los módulos opcionales (nieve, calidad del agua, inestabilidad humana, embalses, drenaje urbano, infraestructura verde, estanques de detención) reproducen la malla ráster regular en una malla formada por sus propias celdas cuadradas. La ejecución en GPU y a escala de la India sigue sin validar. |
| Embalses y estructuras de control | Validado | Solución de vaciado por curva de gasto y balance de volumen. |
| Contorno por hidrograma de entrada | Validado | Volumen del hidrograma prescrito y balance de almacenamiento o salida. |
| Contorno por hidrograma de nivel | Validado | Aplicación del nivel prescrito y respuesta de volumen. |
| Rásteres de lluvia espacial | Validado | Totales exactos por celda y por dominio. |
| Calidad del agua | Validado | Escala de acumulación de SWMM y soluciones analíticas de lavado. |
| Riesgo e inestabilidad humana | Validado | Referencias independientes de umbrales y equilibrio de fuerzas. |

Resultados más recientes de las suites completas de pruebas.

| Suite | Resultado | Fecha |
|---|---|---|
| HydroPol2D-Python | 937 aprobadas, 0 fallidas, 2 pruebas opcionales omitidas | 2026-10-19 |
| Case Builder | 181 aprobadas | 2026-10-19 |
| Verificaciones de publicación del agua subterránea (MATLAB) | 17 de 17 | 2026-10-20 |
| Verificaciones de estaciones y del libro único (MATLAB) | 3 de 3 cada una | 2026-10-20 |
| Validación de publicación (MATLAB) | 22 de 23 directamente; la verificación de intercepción del dosel se evalúa con su script de comparación en Python y se aprueba cuando ese script se ejecuta | 2026-10-20 |

Los cambios del modelo que afectan los resultados se listan en el [Registro de Cambios](./changelog).

Los casos de enrutamiento se interpretan de acuerdo con las ecuaciones que resuelve cada método. La rotura de presa seca de Ritter es un benchmark de aceptación para el momento completo; los métodos reducidos se evalúan con casos de flujo gradual, conservación, simetría y condiciones de contorno.
