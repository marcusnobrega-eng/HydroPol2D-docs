---
title: Visão geral da validação
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Visão geral da validação

O HydroPol2D é avaliado por uma suíte de validação que testa cada módulo computacional em relação a uma referência conhecida. A suíte combina soluções analíticas, cálculos independentes, balanços exatos de água e massa, hidrogramas de referência e simulações numéricas refinadas. Cada caso define dados de entrada, resposta esperada, métricas, critérios de aceitação e resultados.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Baixar o relatório de validação
  </a>
</div>

## Evidências

| Tipo de evidência | Uso na validação do HydroPol2D |
|---|---|
| Solução analítica | Testa as equações em relação a uma solução fechada ou exata. |
| Referência independente | Compara o modelo com um cálculo separado do mesmo processo. |
| Balanço exato | Testa a conservação sob forçantes ou condições de contorno prescritas. |
| Hidrograma de referência | Compara a resposta roteada com um benchmark publicado ou digitalizado. |
| Referência numérica | Compara uma representação mais grosseira ou reduzida com uma simulação refinada documentada. |

Casos úteis para diagnóstico, mas sem uma referência apropriada, permanecem visíveis como diagnósticos e não constituem evidência de aceitação.

<p align="center">
  <img src={useBaseUrl('/img/validation/validation-logic.pt.svg')} width="720" alt="Fluxo de um módulo para o seu caso de validação e para a comparação com uma referência de um dos cinco tipos de evidência, que termina em evidência de aceitação ou em diagnóstico; abaixo, a bacia sintética em V, os benchmarks hidrodinâmicos dedicados e dois casos passo a passo" />
</p>

<p align="center">
  <em>Figura 1. Como um módulo é validado. Um caso só conta como evidência de aceitação quando tem uma referência adequada e atinge os limiares; caso contrário, continua visível como diagnóstico.</em>
</p>

## Bacia sintética em V

Muitos casos hidrológicos e de águas subterrâneas usam a bacia sintética em V. Ela fornece um DEM, solo, cobertura do solo, IAF, águas subterrâneas e condições de contorno comuns, enquanto cada processo é avaliado em relação a sua própria referência. Os benchmarks hidrodinâmicos dedicados, incluindo a ruptura de barragem de Ritter e a onda não quebrante, usam geometrias específicas.

<p align="center">
  <img src={useBaseUrl('/img/validation/vtilted-catchment.pt.svg')} width="720" alt="Vista oblíqua da bacia em V: duas encostas com declividade 0,05 em direção a um canal central de duas células, tudo descendo 0,02 até o exutório na borda norte, com a configuração comum de solo, cobertura, IAF e águas subterrâneas e os casos de validação que a usam" />
</p>

<p align="center">
  <em>Figura 2. A bacia sintética em V, com 81 por 50 células de 20 m e o exutório na borda norte. Vários casos rodam em grades menores com as mesmas três zonas, como mostram as etiquetas cinza.</em>
</p>

## Casos de validação

- [Módulos hidrológicos](./hydrologic-modules)
- [Águas subterrâneas e recarga](./groundwater-recharge)
- [Hidrodinâmica e roteamento](./hydrodynamics-routing)
- [Validação da malha Voronoi](./voronoi-mesh)
- [Reservatórios, contornos, qualidade da água e risco](./ancillary-modules)

A página [Estado da validação](./validation-status) resume as evidências disponíveis para cada módulo.
