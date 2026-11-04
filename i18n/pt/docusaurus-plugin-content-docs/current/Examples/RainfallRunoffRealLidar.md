---
title: Bacia Hidrográfica de San Francisquito - Evento Controlado LiDAR de 10 m
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Bacia Hidrográfica de San Francisquito - Evento Controlado LiDAR de 10 m

## Propósito

Este exemplo simula a chuva do [exemplo de 30 m](RainfallRunoff) em uma grade de 10 m da mesma bacia. Ele mostra como um terreno mais detalhado muda o caminho da água e a rapidez com que ela sai.

## Configuração do caso

O caso `Stanford_10m_LiDAR_Website_100mmh_1h_6h` usa:

| Item | Valor |
|---|---|
| Domínio | Bacia do San Francisquito Creek, Califórnia, EUA |
| Grade | 10 m, NAD83 / California Albers (EPSG:3310) |
| Tipo de forçamento | Chuva espacialmente uniforme |
| Evento de chuva | 100 mm/h de 15 a 75 min (100 mm) |
| Duração da simulação | 6 h |
| Intervalo de saída dos mapas | 15 min |
| Família de roteamento | Inercial local |
| Tratamento de saída | Saída pelo perímetro |
| Processos | Infiltração ligada; água subterrânea, evapotranspiração, neve e qualidade da água desligadas |

## Dados de entrada

Duas entradas são mapas (Figura 1):

- **Terreno.** Um DEM de terreno nu de 10 m do USGS 3D Elevation Program (3DEP), domínio público dos EUA. A maior parte dele é um download antigo do 3DEP guardado com o exemplo. A lacuna de 5,9 km² nas cabeceiras do oeste foi preenchida em 2026-11-03 com dados do serviço 3DEPElevation em 10 m, com uma transição para que o preenchimento encontre o arquivo antigo sem degrau. Vinte e seis depressões e picos de uma célula foram suavizados, e o DEM foi recortado na bacia. Os dois downloads diferem em 2,8 m RMS, sobretudo nas encostas íngremes do oeste, então este DEM não é só uma cópia mais fina do DEM de 30 m.
- **Uso e cobertura da terra.** ESA WorldCover 2020 (v100), o mapa de 30 m do exemplo de 30 m, lido na grade de 10 m. CC BY 4.0. © ESA WorldCover project 2020 / Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium.

As demais entradas são os valores uniformes do exemplo de 30 m: uma classe de solo (a classe 8 da tabela de solos), profundidade até a rocha de 1,5 m, LAI de 1, albedo de 0,25 e umidade inicial do solo de 0,1104. Esses mapas estão na grade de 30 m. Em 8.374 células na borda do domínio (0,5%), que o mapa de LAI de 30 m não alcança, o modelo usa LAI de 0, então ali não há interceptação da chuva.

<p align="center">
  <img src={useBaseUrl('/img/examples/stanford-10m-inputs.pt.svg')} width="680" alt="Dois mapas da bacia do San Francisquito Creek: terreno do DEM de 10 m do USGS 3DEP com sombreamento de relevo e cobertura do solo do ESA WorldCover com a fração de cada classe" />
</p>

<p align="center">
  <em>Figura 1. As duas entradas espaciais. Acima: terreno do DEM de 10 m do USGS 3DEP. Abaixo: cobertura do solo do ESA WorldCover 2020 (mapa de 30 m), com a fração de cada classe no domínio. O círculo marca o Lago Searsville, onde fica a maior profundidade da simulação.</em>
</p>

## Vídeo de simulação

A animação abaixo mostra a simulação em 10 m. Os painéis mostram profundidade de inundação, velocidade, métrica de perigo e infiltração cumulativa sobre o sombreamento do DEM. O quadro de capa é t = 3,0 h, o instante da vazão máxima que sai pela borda do domínio.

<div style={{ textAlign: 'center' }}>
  <video
    width="90%"
    controls
    poster={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.png')}>
    <source src={useBaseUrl('/videos/stanford_10m_lidar_100mmh_1h_6h_panels.mp4')} type="video/mp4" />
    Seu navegador não suporta a tag de vídeo.
  </video>

  <p><em>Simulação de Stanford em 10 m: profundidade de inundação, velocidade, perigo e infiltração cumulativa ao longo de seis horas.</em></p>
</div>

Cada painel usa uma única escala de cores para toda a sequência. A escala é baseada no percentil `99` de todos os quadros salvos.

## Resultados resumidos

A simulação salvou `25` quadros de mapa, um a cada 15 min. O resumo da simulação dá:

| Resultado | Valor |
|---|---|
| Área de drenagem | `157,661 km²` |
| Chuva aplicada | `100,00 mm` |
| Coeficiente de escoamento | `0,40` (nas 6 h) |
| Vazão máxima que sai pela borda do domínio | `663,01 m³/s` em 3,0 h |
| Primeiro pico dessa vazão | `377,13 m³/s` em 75 min, quando a chuva termina |
| Profundidade máxima de inundação | `7,38 m`, na bacia do Lago Searsville (37,411° N, 122,238° W) |
| Área que passou de 1 m de profundidade em algum instante | `4,4 km²` (2,8% do domínio) |
| Erro de volume | `-1,68 × 10⁻¹¹` da entrada |

Como no exemplo de 30 m, toda célula na borda do domínio deixa a água sair (saída pelo perímetro), então o hidrograma é a vazão que sai pela borda do domínio, e não só a vazão na foz do córrego. As vazões são suas amostras de 15 min. O primeiro pico, 377,13 m³/s em 75 min, é o escoamento das encostas saindo ao longo de toda a borda. Depois a vazão cai para 123 m³/s em 1,75 h. Em seguida, a onda de cheia chega ao trecho em que o San Francisquito Creek corre na borda norte do domínio. A água que transborda ali sai do modelo, e a vazão volta a subir até 663,01 m³/s em 3,0 h. Nesse instante, a maior parte da vazão sai pela borda norte. Em 6 h a vazão é de 186,36 m³/s.

## 10 m e 30 m nas mesmas seis horas

O exemplo de 30 m dura 24 h. A tabela compara as primeiras 6 h das duas simulações, com as mesmas amostras de 15 min e os mesmos quadros salvos:

| Resultado, primeiras 6 h | 30 m | 10 m |
|---|---|---|
| Área de drenagem | 156,8 km² | 157,7 km² |
| Primeiro pico da vazão que sai pela borda do domínio | 402,84 m³/s em 75 min | 377,13 m³/s em 75 min |
| Menor vazão entre os dois picos | 110,1 m³/s em 2,0 h | 123,1 m³/s em 1,75 h |
| Vazão máxima que sai pela borda do domínio | 473,69 m³/s em 3,5 h | 663,01 m³/s em 3,0 h |
| Vazão em 6 h | 144,72 m³/s | 186,36 m³/s |
| Água que saiu pela borda | 5,34 milhões de m³ (34% da chuva) | 6,27 milhões de m³ (40% da chuva) |
| Profundidade máxima nos quadros salvos | 5,82 m | 7,38 m |
| Área com mais de 1 m em algum quadro salvo | 4,2 km² | 4,3 km² |

A chuva e as demais entradas são as mesmas, então as diferenças vêm do terreno: a grade mais fina e um DEM de outro download do 3DEP. Na grade de 10 m, o pico das encostas é um pouco menor. A água do córrego que transborda para a borda norte chega 30 min antes, e seu pico é 40% maior. Em seis horas, sai do domínio 17% mais água. A maior profundidade fica na bacia do Lago Searsville nas duas grades, 1,56 m maior na grade de 10 m.

## Como executar

O caso está no repositório do HydroPol2D em MATLAB, em `Examples/Stanford`. No MATLAB, a partir da raiz do repositório:

```matlab
addpath(fullfile(pwd,'Examples','Stanford'))
run_stanford_local_case('Resolution',10, ...
  'StaticFolder',fullfile('Examples','Stanford','Static_10m_LiDAR'), ...
  'SimulationMinutes',360, ...
  'RainfallTimeseriesPath',fullfile('Examples','Stanford','Forcing','Rainfall','Rainfall_Intensity_Website_100mmh_1h_24h.csv'), ...
  'RecordTimeMapsMinutes',15,'RecordTimeHydrographsMinutes',15, ...
  'OutputTag','Stanford_10m_LiDAR_Website_100mmh_1h_6h')
```

Os resultados vão para `Examples/Stanford/Outputs/Reruns_CurrentModel/Stanford_10m_LiDAR_Website_100mmh_1h_6h/Modeling_Results`, com os mesmos arquivos do exemplo de 30 m. A grade de 10 m tem nove vezes mais células que a de 30 m. A simulação levou cerca de 10 h na CPU de um laptop (Apple M4, 24 GB).
