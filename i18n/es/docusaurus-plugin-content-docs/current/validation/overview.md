---
title: Resumen
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Resumen de validacion

La validacion de HydroPol2D esta organizada en benchmarks controlados de Fase 1. El objetivo de esta fase es verificar que cada modulo computacional reproduzca las ecuaciones, las actualizaciones de almacenamiento, las condiciones de contorno y el comportamiento numerico esperados en casos donde la respuesta conocida esta disponible.

El informe tecnico completo esta disponible aqui:

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Descargar el informe de validacion de la Fase 1
  </a>
</div>

## Filosofia de validacion

Una afirmacion de validacion solo se hace cuando el caso tiene una solucion analitica, un calculo de referencia independiente, un objetivo exacto de bookkeeping, un hidrograma de benchmark o una referencia numerica documentada. Los casos basados solo en comportamiento cualitativo se tratan como diagnosticos.

La Fase 1 no reclama calibracion de campo ni validacion observacional a escala de cuenca. Los casos de campo y los ejercicios de modelacion inversa constituyen niveles distintos de evidencia y deben reportarse por separado.

## Niveles de evidencia

| Nivel de evidencia | Significado |
|---|---|
| Solucion analitica | Existe una solucion matematica cerrada o exacta. |
| Referencia independiente | Una implementacion separada calcula el resultado esperado. |
| Bookkeeping exacto | El objetivo de validacion es conservacion, forzante prescrita o volumen impuesto en contorno. |
| Hidrograma de benchmark | Se usa un hidrograma publicado o digitalizado como comparacion. |
| Referencia numerica | Una simulacion numerica refinada o simplificada se usa como referencia. |
| Diagnostico | El caso es util para depuracion, pero no sostiene una afirmacion formal de validacion. |

## Alcance actual

El paquete de Fase 1 cubre intercepcion del dosel, nieve, infiltracion, evapotranspiracion, groundwater y recarga, enrutamiento hidrodinamico, comportamiento de embalses y contornos, lluvia espacial, calidad del agua y diagnosticos de inestabilidad humana. Consulte la pagina [Human Instability](../theory/human-instability) para los modos implementados.
