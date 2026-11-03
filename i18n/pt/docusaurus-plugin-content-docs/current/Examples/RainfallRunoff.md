---
title: Bacia Hidrográfica de San Francisquito - Exemplo de Chuva Controlada
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Bacia Hidrográfica de San Francisquito - Exemplo de Chuva Controlada

## Propósito

Este exemplo apresenta uma simulação controlada de chuva e escoamento para a bacia do San Francisquito Creek, perto de Stanford, Califórnia. Ele mostra como o HydroPol2D responde, em uma bacia real, a uma chuva cujo instante e volume são conhecidos com exatidão.

## Configuração do caso

O caso `Stanford_30m_Website_100mmh_1h_24h` usa:

| Item | Valor |
|---|---|
| Domínio | Bacia do San Francisquito Creek, Califórnia, EUA |
| Grade | 30 m, NAD83 / California Albers (EPSG:3310) |
| Tipo de forçamento | Chuva espacialmente uniforme |
| Evento de chuva | 100 mm/h de 15 a 75 min (100 mm) |
| Duração da simulação | 24 h |
| Intervalo de saída dos mapas | 15 min |
| Família de roteamento | Inercial local |
| Tratamento de saída | Saída pelo perímetro |
| Processos | Infiltração ligada; água subterrânea, evapotranspiração, neve e qualidade da água desligadas |

## Dados de entrada

Duas entradas são mapas (Figura 1):

- **Terreno.** O DEM de terreno nu do USGS 3D Elevation Program (3DEP), lido do serviço 3DEPElevation em 10 m e agregado pela média para a grade de 30 m (baixado em 2026-11-02, domínio público dos EUA).
- **Uso e cobertura da terra.** ESA WorldCover 2020 (v100), CC BY 4.0. © ESA WorldCover project 2020 / Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium. Os códigos de classe 10 a 90 da tabela de uso da terra são os do WorldCover.

As demais entradas são valores uniformes definidos para o exemplo, sem dados externos: uma classe de solo (a classe 8 da tabela de solos), profundidade até a rocha de 1,5 m, LAI de 1, albedo de 0,25 e umidade inicial do solo de 0,1104. Os demais parâmetros vêm da planilha do caso Stanford distribuída com o modelo em MATLAB.

<p align="center">
  <img src={useBaseUrl('/img/examples/stanford-30m-inputs.pt.svg')} width="680" alt="Dois mapas da bacia do San Francisquito Creek: terreno do USGS 3DEP com sombreamento de relevo e cobertura do solo do ESA WorldCover com a fração de cada classe" />
</p>

<p align="center">
  <em>Figura 1. As duas entradas espaciais na grade de 30 m. Acima: terreno do USGS 3DEP. Abaixo: cobertura do solo do ESA WorldCover 2020, com a fração de cada classe no domínio. O círculo marca o Lago Searsville, onde fica a maior profundidade da simulação.</em>
</p>

## O que este caso pretende mostrar

Este caso destaca:

- geração de escoamento superficial sob um forçamento simples e conhecido;
- a interação entre topografia, rugosidade e infiltração;
- a organização espacial da profundidade, velocidade, perigo e infiltração cumulativa da inundação;
- comportamento de recessão longa após o término do pulso de chuva.

## Vídeo de simulação

A animação abaixo mostra a simulação em 30 m. Os painéis mostram profundidade de inundação, velocidade, métrica de perigo e infiltração cumulativa sobre o sombreamento do DEM. O quadro de capa é t = 3,5 h, o instante da vazão máxima na saída.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_30m_website_100mmh_1h_24h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_30m_website_100mmh_1h_24h_panels.mp4')} type="video/mp4" />
    Seu navegador não suporta a tag de vídeo.
  </video>

  <p><em>Simulação controlada de chuva em Stanford, 30 m: profundidade de inundação, velocidade, perigo e infiltração cumulativa.</em></p>
</div>

Cada painel usa uma única escala de cores para toda a sequência. A escala é baseada no percentil `99` de todos os quadros salvos.

## Resultados resumidos

A simulação salvou `97` quadros de mapa, um a cada 15 min. O resumo da simulação dá:

| Resultado | Valor |
|---|---|
| Área de drenagem | `156,823 km²` |
| Chuva aplicada | `100,00 mm` |
| Coeficiente de escoamento | `0,47` |
| Vazão máxima na saída | `473,69 m³/s` em 3,5 h |
| Primeiro pico na saída | `402,84 m³/s` em 75 min, quando a chuva termina |
| Profundidade máxima de inundação | `5,87 m`, na bacia do Lago Searsville (37,410° N, 122,234° W) |
| Área que passou de 1 m de profundidade em algum instante | `4,3 km²` (2,7% do domínio) |
| Erro de volume | `-6,45 × 10⁻¹²` da entrada |

As vazões são as amostras de 15 min do hidrograma de saída. Ele tem dois picos: 402,84 m³/s em 75 min, quando a chuva termina, e 473,69 m³/s em 3,5 h. Entre eles, a vazão cai para 110 m³/s em 2 h e depois volta a subir.

:::warning[Alterado em 2026-11-02]
Esta página informava uma profundidade máxima de 0,64 m e uma vazão máxima de 335,03 m³/s. Esses números vinham de um DEM de 30 m mais antigo, de origem não registrada, que diferia do 3DEP em 7,3 m RMS, e de uma versão mais antiga do modelo em MATLAB. O resumo antigo também tomava a profundidade máxima só do último bloco de mapas salvos, então 0,64 m estava baixo demais.
:::

## Como executar

O caso está no repositório do HydroPol2D em MATLAB, em `Examples/Stanford`. No MATLAB, a partir da raiz do repositório:

```matlab
addpath(fullfile(pwd,'Examples','Stanford'))
run_stanford_local_case('Resolution',30,'SimulationMinutes',1440, ...
  'RainfallTimeseriesPath',fullfile('Examples','Stanford','Forcing','Rainfall','Rainfall_Intensity_Website_100mmh_1h_24h.csv'), ...
  'RecordTimeMapsMinutes',15,'RecordTimeHydrographsMinutes',15, ...
  'OutputTag','Stanford_30m_Website_100mmh_1h_24h')
```

Os resultados vão para `Examples/Stanford/Outputs/Reruns_CurrentModel/Stanford_30m_Website_100mmh_1h_24h/Modeling_Results`: mapas de profundidade, velocidade e perigo a cada 15 min, o hidrograma de saída (`Tables_CSV/Outlet_Hydrograph_Data_Outlet.csv`) e o resumo da simulação (`Tables_CSV/Summary_Table.csv`).

Uma simulação mais curta da mesma chuva, de 3 h em vez de 24 h, começa com `run('Examples/Stanford/run_excel.m')` e leva cerca de 14 min em um laptop. O README do repositório lista os resultados esperados.
