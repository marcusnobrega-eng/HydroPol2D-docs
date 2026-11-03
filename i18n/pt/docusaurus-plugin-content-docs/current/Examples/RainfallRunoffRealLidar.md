---
title: Bacia Hidrográfica de San Francisquito - Evento Controlado LiDAR de 10 m
# Hidden until the 10 m case is rerun with the current model; its numbers are from an older code.
draft: true
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Bacia Hidrográfica de San Francisquito - Evento Controlado LiDAR de 10 m

## Propósito

Este exemplo apresenta a simulação de San Francisquito com LiDAR de 10 m. Ele mostra como o modelo responde quando o terreno é representado com um DEM mais detalhado.

## Configuração do caso

O exemplo de 10 m usa:
- um 10 m USGS ou 3DEP DEM real para o domínio Stanford;
- rasters auxiliares Stanford alinhados a essa grade 10 m;
- o mesmo evento de chuva controlada usado no exemplo 30 m;
- um tratamento de saída pelo perímetro.

| Item | Valor |
|---|---|
| Resolução de grade | 10 m |
| Forçamento | 100 mm/h por 1 hora |
| Duração da simulação | 6 h |
| Intervalo de saída do mapa | 15 min |
| Quadros de mapa salvos | 24 |
| Família de roteamento | Inercial local |
| Tratamento de saída | Saída pelo perímetro |

## Vídeo da simulação

A animação abaixo mostra a simulação em 10 m. Os painéis mostram profundidade de inundação, velocidade, métrica de perigo e infiltração cumulativa.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.mp4')} type="video/mp4" />
    Seu navegador não suporta a tag de vídeo.
  </video>

  <p><em>Simulação LiDAR de 10 m em San Francisquito: profundidade de inundação, velocidade, perigo e infiltração cumulativa ao longo de seis horas.</em></p>
</div>

## Resumo da resposta em seis horas

O resumo abaixo se refere à mesma simulação de seis horas mostrada na sequência de mapas.

| Métrica | Valor |
|---|---:|
| Resolução de grade | 10 m |
| Duração publicada | 6 h |
| Quadros de mapa salvos | 24 |
| Sequência de mapas coberta | 00:00 a 05:45 |
| Vazão de pico na janela de seis horas | 448.06 m³/s |
| Tempo do pico | 180.00 min |
| Vazão de saída em 6 h | 115.69 m³/s |
| Profundidade máxima nos quadros salvos | 6.91 m |
| Velocidade máxima nos quadros salvos | 10.00 m/s |
| Métrica máxima de perigo nos quadros salvos | 25.38 m²/s |
| Infiltração cumulativa máxima | 474.60 mm |

### Hidrograma e chuva
<img src={useBaseUrl('/figures/Stanford_10m_6h_Hydrograph_Rainfall.png')} alt="Hidrograma recuperado de 10 m" />

## O que este exemplo mostra

Este exemplo destaca:

- o efeito de uma representação mais detalhada do terreno sobre os padrões locais de inundação;
- a resposta roteada nas primeiras seis horas de simulação;
- as diferenças que surgem quando o mesmo forçamento é aplicado nos domínios de 10 m e 30 m.
