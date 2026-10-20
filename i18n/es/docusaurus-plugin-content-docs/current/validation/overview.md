---
title: Resumen de validacion
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Resumen de validacion

HydroPol2D se evalua mediante una suite de validacion que contrasta cada modulo computacional con una referencia conocida. La suite combina soluciones analiticas, calculos independientes, balances exactos de agua y masa, hidrogramas de referencia y simulaciones numericas refinadas. Cada caso define datos de entrada, respuesta esperada, metricas, criterios de aceptacion y resultados.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Descargar el informe de validacion
  </a>
</div>

## Evidencia

| Tipo de evidencia | Uso en la validacion de HydroPol2D |
|---|---|
| Solucion analitica | Prueba las ecuaciones frente a una solucion cerrada o exacta. |
| Referencia independiente | Compara el modelo con un calculo independiente del mismo proceso. |
| Balance exacto | Prueba la conservacion bajo forzantes o condiciones de contorno prescritas. |
| Hidrograma de referencia | Compara la respuesta enrutada con un benchmark publicado o digitalizado. |
| Referencia numerica | Compara una representacion mas gruesa o reducida con una simulacion refinada documentada. |

Los casos utiles para diagnostico, pero sin una referencia apropiada, permanecen visibles como diagnosticos y no se usan como evidencia de aceptacion.

## Cuenca sintetica en V

Muchos casos hidrologicos y de aguas subterraneas usan la cuenca sintetica en V. Proporciona un DEM, suelo, cobertura del suelo, IAF, aguas subterraneas y condiciones de contorno comunes, mientras cada proceso se evalua frente a su propia referencia. Los benchmarks hidrodinamicos dedicados, incluida la rotura de presa de Ritter y la onda no rompiente, usan geometrias especificas.

## Casos de validacion

- [Modulos hidrologicos](./hydrologic-modules)
- [Aguas subterraneas y recarga](./groundwater-recharge)
- [Hidrodinamica y enrutamiento](./hydrodynamics-routing)
- [Embalses, contornos, calidad del agua y riesgo](./ancillary-modules)

La pagina [Estado de validacion](./validation-status) resume la evidencia disponible para cada modulo.
