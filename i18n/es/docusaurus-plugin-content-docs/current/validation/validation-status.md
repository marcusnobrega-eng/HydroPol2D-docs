---
title: Estado de validacion
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Estado de validacion

El informe de validacion documenta los metodos, metricas y resultados de la suite de validacion de HydroPol2D. La tabla presenta un indice conciso de la evidencia disponible.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Abrir el informe de validacion
  </a>
</div>

| Modulo | Estado | Evidencia |
|---|---|---|
| Intercepcion del dosel | Validado | Referencia independiente de almacenamiento del dosel y balance exacto de masa. |
| Nieve | Validado | Parametros por LULC, mapas iniciales opcionales, refinamiento temporal, equivalencia entre hoja de calculo y script, y balance del evento en V. |
| Infiltracion | Validado | Casos analiticos y de suelo estratificado en dominios de columna y en V. |
| Evapotranspiracion | Validado | Calculos independientes de ET de referencia y limites de extraccion. |
| Aguas subterraneas y recarga | Validado | Pruebas de ascenso del nivel freatico, programacion, ascenso capilar y laderas analiticas. |
| Hidrodinamica de momento completo | Validado | Plano inclinado, cuenca en V, rotura de presa de Ritter, onda no rompiente y contornos. |
| Hidrodinamica inercial local | Validado | Plano inclinado, cuenca en V, contorno de nivel y conservacion. |
| Automatas celulares | Validado | Casos de cuenca en V, plano y condiciones de contorno. |
| Ondas cinematica y difusiva | Validado | Benchmarks de plano, cuenca en V y contorno de nivel adecuados para las ecuaciones reducidas. |
| Modelo subgrid de Neal (2012) | Validado para las geometrias evaluadas | Referencias de malla fina para flujo en canal, canal compuesto, activacion de margenes y extension inundada. |
| Embalses y estructuras de control | Validado | Solucion de vaciado por curva de gasto y balance de volumen. |
| Contorno por hidrograma de entrada | Validado | Volumen del hidrograma prescrito y balance de almacenamiento o salida. |
| Contorno por hidrograma de nivel | Validado | Aplicacion del nivel prescrito y respuesta de volumen. |
| Rasters de lluvia espacial | Validado | Totales exactos por celda y por dominio. |
| Calidad del agua | Validado | Escala de acumulacion de SWMM y soluciones analiticas de lavado. |
| Riesgo e inestabilidad humana | Validado | Referencias independientes de umbrales y equilibrio de fuerzas. |

Los casos de enrutamiento se interpretan de acuerdo con las ecuaciones que resuelve cada metodo. La rotura de presa seca de Ritter es un benchmark de aceptacion para el momento completo; los metodos reducidos se evaluan con casos de flujo gradual, conservacion, simetria y condiciones de contorno.
