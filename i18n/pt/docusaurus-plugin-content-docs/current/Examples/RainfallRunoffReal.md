---
title: Bacia Hidrográfica de San Francisquito - Exemplo com Chuva Observada
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Bacia Hidrográfica de San Francisquito - Exemplo com Chuva Observada

## Propósito

Este exemplo descreve a configuração de evento da bacia de San Francisquito quando o forçamento de chuva vem de dados observados. O foco está nos dados necessários para a simulação do evento e para a comparação de hidrogramas.

## Configuração do caso

A simulação atual do evento usa:

| Item | Valor |
|---|---|
| Resolução de grade | 30 m |
| Profundidade de chuva | 75 mm |
| Duração da simulação | 48 h |
| Família de roteamento | Inercial local |
| Tratamento de saída | Saída pelo perímetro |
| Observações de vazão na execução atual | Não disponíveis |
| Pontos de comparação | Gerados a partir de percentis de acumulação de fluxo |

A reexecução atual não incluiu um arquivo válido de vazão observada. Por isso, o HydroPol2D gerou pontos de comparação a partir da rede de drenagem. A página documenta a configuração do evento e a resposta do modelo para a estrutura atual.

## Vídeo da simulação

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_30m_outlet020_fullperiod_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_30m_outlet020_fullperiod_panels.mp4')} type="video/mp4" />
    Seu navegador não suporta a tag de vídeo.
  </video>

  <p><em>Simulação de evento em San Francisquito, 30 m: profundidade de inundação, velocidade, perigo e infiltração cumulativa.</em></p>
</div>

## O que este exemplo mostra

A configuração com chuva observada exige:
- forçamento de chuva observado, idealmente interpolado a partir de múltiplos medidores quando esses dados estiverem disponíveis;
- dados de descarga ou estágio observados no local de comparação;
- tratamento explícito das condições iniciais, especialmente da umidade antecedente;
- confirmação cuidadosa de que o ponto de observação representa a área de drenagem modelada.

## Resultados resumidos

A simulação atual do evento produziu:

- uma vazão de pico de `260.57 m³/s`;
- uma profundidade máxima de inundação de `0.31 m`;
- uma resposta roteada de 48 h com mapas salvos no mesmo formato de quatro painéis usado no exemplo controlado.
