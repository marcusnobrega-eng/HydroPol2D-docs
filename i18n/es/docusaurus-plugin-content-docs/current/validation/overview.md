---
title: Resumen de validación
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Resumen de validación

HydroPol2D se evalúa mediante una suite de validación que contrasta cada módulo computacional con una referencia conocida. La suite combina soluciones analíticas, cálculos independientes, balances exactos de agua y masa, hidrogramas de referencia y simulaciones numéricas refinadas. Cada caso define datos de entrada, respuesta esperada, métricas, criterios de aceptación y resultados.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Descargar el informe de validación
  </a>
</div>

## Evidencia

| Tipo de evidencia | Uso en la validación de HydroPol2D |
|---|---|
| Solución analítica | Prueba las ecuaciones frente a una solución cerrada o exacta. |
| Referencia independiente | Compara el modelo con un cálculo independiente del mismo proceso. |
| Balance exacto | Prueba la conservación bajo forzantes o condiciones de contorno prescritas. |
| Hidrograma de referencia | Compara la respuesta enrutada con un benchmark publicado o digitalizado. |
| Referencia numérica | Compara una representación más gruesa o reducida con una simulación refinada documentada. |

Los casos útiles para diagnóstico, pero sin una referencia apropiada, permanecen visibles como diagnósticos y no se usan como evidencia de aceptación.

## Cuenca sintética en V

Muchos casos hidrológicos y de aguas subterráneas usan la cuenca sintética en V. Proporciona un DEM, suelo, cobertura del suelo, IAF, aguas subterráneas y condiciones de contorno comunes, mientras cada proceso se evalúa frente a su propia referencia. Los benchmarks hidrodinámicos dedicados, incluida la rotura de presa de Ritter y la onda no rompiente, usan geometrías específicas.

## Casos de validación

- [Módulos hidrológicos](./hydrologic-modules)
- [Aguas subterráneas y recarga](./groundwater-recharge)
- [Hidrodinámica y enrutamiento](./hydrodynamics-routing)
- [Validación de la malla de Voronoi](./voronoi-mesh)
- [Embalses, contornos, calidad del agua y riesgo](./ancillary-modules)

La página [Estado de validación](./validation-status) resume la evidencia disponible para cada módulo.
