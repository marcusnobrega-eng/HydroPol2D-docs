---
title: Preparar um caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Preparar um caso

Depois de uma prévia com as configurações atuais, **Prepare complete case** monta o caso. Uma caixa
de status mostra a etapa e uma barra de progresso. A montagem:

1. baixa os dados que ainda não tem: terreno, cobertura do solo, solos, profundidade até a rocha,
   águas subterrâneas, área foliar e a chuva e o clima do período (o primeiro caso de uma região é o
   mais demorado, e os casos seguintes reaproveitam o cache);
2. condiciona o terreno com o HydroBathyDEM, que vem com o app, para que a água chegue aos
   exutórios, e dá larguras e profundidades aos canais dos rios;
3. num caso Catchment, delimita a bacia final na grade do modelo;
4. leva cada camada para a grade do modelo e grava as séries de chuva, clima e contorno;
5. grava os arquivos de modelo que você escolheu em **Prepare for**;
6. roda a [verificação prévia](check-a-case).

Quando termina, a caixa diz "Case preparation complete" e a página mostra o caso, o resultado da
verificação e os painéis de simulação ([Rodar o caso](run-the-case)). Se a montagem parar, a caixa
diz "Case preparation stopped" com o erro, e o **Process log** traz os detalhes. Uma montagem que
falha mantém os arquivos que baixou, então a próxima tentativa continua de onde parou.

O tempo depende do tamanho do domínio, do período e dos serviços de dados. O caso de 10 m do San
Francisquito Creek abaixo (99 km², 987.647 células ativas) levou de 2 a 4 minutos, a maior parte
esperando o serviço do Copernicus, e baixou cerca de 10 MB.

<p align="center">
  <img src={useBaseUrl('/img/builder/stanford-terrain.jpg')} width="620" alt="Terreno sombreado da bacia do San Francisquito Creek, em Stanford, na Califórnia, em uma grade de 10 m, com a rede de rios em azul e a borda da bacia" />
</p>

<p align="center">
  <em>Figura 1. Terreno da bacia do San Francisquito Creek preparado pelo Case Builder em uma grade de 10 m, com a rede de rios e a borda da bacia. O terreno é o USGS 3DEP, que você informa como um DEM local ou escolhe na linha de comando.</em>
</p>

<p align="center">
  <img src={useBaseUrl('/img/builder/stanford-layers.png')} width="760" alt="Três mapas do caso San Francisquito Creek na mesma grade de 10 m: classes de cobertura do solo, larguras dos canais dos rios e profundidade até a rocha" />
</p>

<p align="center">
  <em>Figura 2. Mais três camadas do mesmo caso, na mesma grade: cobertura do solo, os canais dos rios e a profundidade até a rocha.</em>
</p>

## O que fica na pasta do caso {#case-folder}

A pasta leva o nome do local, do tamanho da célula e da data de início, por exemplo
`tucson_urban_only_250m_20210723`. Um caso completo tem esta estrutura geral. As pastas aparecem só
quando o caso precisa delas: `hydropol_matlab` não existe em um caso preparado só para Python, por
exemplo.

```text
CASE_DIR/
├── case.json                     o pedido e a estimativa do domínio
├── manifest.json                 cada fonte, versão e arquivo do caso
├── domain.gpkg                   o domínio do modelo
├── final_domain.gpkg             Catchment: a bacia na grade do modelo
├── outlet_candidates.gpkg        Catchment: o exutório informado e os três candidatos
├── preliminary_catchment.gpkg    Catchment: o primeiro contorno do HydroSHEDS
├── hydropol_config.json          as configurações do modelo para o caso
├── input_contract.json           a lista das entradas do modelo e dos seus arquivos
├── figures/                      domain_preview.html e .png, outros mapas da prévia
├── hydropol_python/              case.yaml, run_case.py e o NetCDF de chuva
├── hydropol_matlab/              run_case.m e os caminhos das suas entradas
├── processed_inputs/
│   ├── Static/                   os mapas na grade do modelo
│   └── Forcing/                  séries de chuva, clima e contorno
├── rainfall_summaries/           totais de chuva para conferência
├── quality_report/               preflight.json e as outras verificações
└── Outputs/                      resultados do modelo, depois de uma simulação
```

### Os mapas {#maps}

Os principais mapas em `processed_inputs/Static/` são:

| Arquivo | O que contém |
|---|---|
| `DEM.tif` | o terreno condicionado pelo HydroBathyDEM, a superfície do modelo |
| `DomainMask.tif` | o domínio ativo do modelo |
| `LULC.tif` | classes de cobertura do solo do ESA WorldCover |
| `SOIL.tif` | classes de textura do solo do USDA |
| `DTB.tif` | profundidade até a rocha |
| `GW_table.tif` | cota inicial das águas subterrâneas |
| `Initial_Soil_Moisture.tif` | umidade inicial do solo para o MATLAB, em mm acima do teor de água residual |
| `Initial_Soil_Moisture_Fraction.tif` | teor volumétrico inicial de água para o Python |
| `LAI.tif` | índice de área foliar |
| `Albedo.tif` | albedo, uma constante de 0,25 nesta versão |
| `RiverWidths.tif`, `RiverDepths.tif` | a geometria dos canais |
| `D4_flow_direction.tif`, `D4_idx_facc.tif` | os mapas de roteamento do HydroBathyDEM |
| `FlowDirectionD8.tif`, `FlowAccumulationD8.tif` | Catchment: os mapas D8 que delimitam a bacia |
| `BoundaryConditionMask.tif` | Catchment: as células de exutório com profundidade crítica |

Os mapas categóricos (cobertura do solo, classes de solo) são reamostrados pelo vizinho mais
próximo, e os mapas contínuos por uma interpolação adequada a cada fonte.

### Os relatórios {#reports}

`quality_report/` guarda as verificações da montagem, entre elas:

- `preflight.json`: o resultado da verificação ([Verificar um caso](check-a-case));
- `terrain_domain_qa.json` e `hydraulic_terrain_qa.json`: o terreno, o domínio e as mudanças que o
  HydroBathyDEM fez;
- `public_static_sources.json`: as fontes dos mapas estáticos;
- `rainfall_summary.json`, `initial_soil_moisture.json` e, para o MSWEP, `mswep_download.json`.

Guarde `case.json`, `manifest.json`, `quality_report/` e os arquivos de modelo com qualquer simulação
publicada: eles registram como o caso foi feito.

## Antes de confiar em um caso novo {#before-you-trust}

Um caso que passa na verificação está completo e consistente, o que ainda não diz nada sobre a sua
precisão. Antes de ler os resultados de um lugar novo:

1. olhe a bacia e a rede de rios;
2. abra os mapas de terreno, cobertura do solo, solo, águas subterrâneas e canais em um SIG;
3. compare os totais de chuva com o produto de origem;
4. confira as condições de contorno e a costa;
5. compare a vazão ou a inundação simuladas com observações independentes;
6. anote qualquer parâmetro que você mudar depois que o caso for feito.
