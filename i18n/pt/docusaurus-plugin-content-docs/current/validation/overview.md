---
title: Visao geral
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Visao geral da validacao

A validacao do HydroPol2D esta organizada em benchmarks controlados de Fase 1. O objetivo desta fase e verificar se cada modulo computacional reproduz as equacoes, as atualizacoes de armazenamento, as condicoes de contorno e o comportamento numerico esperados em casos onde a resposta conhecida esta disponivel.

O relatorio tecnico completo esta disponivel aqui:

<div style={{margin: '1rem 0 1.5rem 0'}}>
  <a className="button button--primary button--lg" href={useBaseUrl('/reports/validation_report.pdf')}>
    Baixar o relatorio de validacao da Fase 1
  </a>
</div>

## Filosofia de validacao

Uma afirmacao de validacao so e feita quando o caso possui solucao analitica, calculo de referencia independente, alvo exato de bookkeeping, hidrográfica de benchmark ou referencia numerica documentada. Casos baseados apenas em comportamento qualitativo sao tratados como diagnosticos.

A Fase 1 nao reivindica calibracao de campo nem validacao observacional em escala de bacia. Casos de campo e exercicios de modelagem inversa constituem niveis diferentes de evidencia e devem ser relatados separadamente.

## Niveis de evidencia

| Nivel de evidencia | Significado |
|---|---|
| Solucao analitica | Existe uma solucao matematica fechada ou exata. |
| Referencia independente | Uma implementacao separada calcula o resultado esperado. |
| Bookkeeping exato | O alvo de validacao e conservacao, forcante prescrita ou volume imposto em contorno. |
| Hidrografa de benchmark | Uma hidrografa publicada ou digitalizada e usada como comparacao. |
| Referencia numerica | Uma simulacao numerica refinada ou simplificada e usada como referencia. |
| Diagnostico | O caso e util para depuracao, mas nao sustenta uma afirmacao formal de validacao. |

## Escopo atual

O pacote de Fase 1 cobre interceptacao pelo dossel, neve, infiltracao, evapotranspiracao, groundwater e recarga, roteamento hidrodinamico, comportamento de reservatorios e contornos, ingestao de chuva espacial, qualidade da agua e diagnosticos de instabilidade humana. Consulte a pagina [Human Instability](../theory/human-instability) para os modos implementados.
