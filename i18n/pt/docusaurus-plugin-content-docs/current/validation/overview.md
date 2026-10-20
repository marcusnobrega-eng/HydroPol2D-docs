---
title: Visao geral da validacao
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Visao geral da validacao

O HydroPol2D e avaliado por uma suite de validacao que testa cada modulo computacional em relacao a uma referencia conhecida. A suite combina solucoes analiticas, calculos independentes, balancos exatos de agua e massa, hidrogramas de referencia e simulacoes numericas refinadas. Cada caso define dados de entrada, resposta esperada, metricas, criterios de aceitacao e resultados.

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Baixar o relatorio de validacao
  </a>
</div>

## Evidencias

| Tipo de evidencia | Uso na validacao do HydroPol2D |
|---|---|
| Solucao analitica | Testa as equacoes em relacao a uma solucao fechada ou exata. |
| Referencia independente | Compara o modelo com um calculo separado do mesmo processo. |
| Balanco exato | Testa a conservacao sob forcantes ou condicoes de contorno prescritas. |
| Hidrograma de referencia | Compara a resposta roteada com um benchmark publicado ou digitalizado. |
| Referencia numerica | Compara uma representacao mais grosseira ou reduzida com uma simulacao refinada documentada. |

Casos uteis para diagnostico, mas sem uma referencia apropriada, permanecem visiveis como diagnosticos e nao constituem evidencia de aceitacao.

## Bacia sintetica em V

Muitos casos hidrologicos e de aguas subterraneas usam a bacia sintetica em V. Ela fornece um DEM, solo, cobertura do solo, IAF, aguas subterraneas e condicoes de contorno comuns, enquanto cada processo e avaliado em relacao a sua propria referencia. Os benchmarks hidrodinamicos dedicados, incluindo a ruptura de barragem de Ritter e a onda nao quebrante, usam geometrias especificas.

## Casos de validacao

- [Modulos hidrologicos](./hydrologic-modules)
- [Aguas subterraneas e recarga](./groundwater-recharge)
- [Hidrodinamica e roteamento](./hydrodynamics-routing)
- [Reservatorios, contornos, qualidade da agua e risco](./ancillary-modules)

A pagina [Estado da validacao](./validation-status) resume as evidencias disponiveis para cada modulo.
