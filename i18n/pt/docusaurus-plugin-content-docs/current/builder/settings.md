---
title: Configurações do caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Configurações do caso

Abaixo da área do modelo, cada aba de **Prepare a case** tem os mesmos grupos de configurações, de
cima para baixo: **Grid and period**, **Forcing and model adapter**, **Simulated processes**,
**River representation** (com **Hydraulic parameters**), **Saved outputs**, **Urban boundary
conditions** (Urban Area Only), as pastas de chuva e **Folders and advanced paths**.

Os padrões diferem entre as abas urbanas e a aba Catchment:

| Configuração | Urban Basin e Urban Area Only | Catchment |
|---|---|---|
| Tamanho da célula | 90 m | 1.000 m |
| Área de início dos rios | 5 km² | 10 km² |
| Produto de chuva | IMERG (30 minutes) | MSWEP (3 hourly) |
| Escoamento de base do aquífero profundo | desligado | ligado |
| Pacote de saída | Standard | Full |
| Intervalo dos mapas | 60 minutos | 180 minutos |
| Intervalo dos hidrogramas | 10 minutos | 60 minutos |

Qualquer mudança em uma configuração pede uma nova [prévia](preview-and-cost) antes que o caso possa
ser preparado.

## Grid and period {#grid-and-period}

| Configuração | O que ela define |
|---|---|
| **Grid type** | Só nas abas urbanas. **Uniform grid** ou **Quadtree grid** (veja abaixo). |
| **Cell size (m)** | O tamanho da célula do modelo. Ele não pode ser mais fino que o terreno: cerca de 30 m com o FABDEM. |
| **Warm-up (days)** | Dias simulados antes da data de início, para que solos e rios se estabilizem. A chuva e o clima são preparados a partir do início do aquecimento. Padrão 0. |
| **River initiation area (km2)** | A área a montante a partir da qual começa um canal de rio. |
| **Terrain source** | **FABDEM**, ou **Local georeferenced DEM** com o seu **Local DEM path**. |
| **Simulation start date (UTC)**, **Start time (UTC)** | O início da simulação. |
| **Simulation end date (UTC)**, **End time (UTC)** | O fim da simulação. |

As datas estão em UTC, de 1979-01-01 até hoje. Você pode digitar o ano no campo da data.

### Grade quadtree {#quadtree-grid}

Uma grade quadtree usa células quadradas de vários tamanhos. A cidade mantém as células finas e o
resto do domínio recebe células mais grossas, o que reduz o número de células de uma bacia grande.

- **Fine cell size (m)**: as células sobre a cidade e a sua faixa.
- **Coarse cell size (m)**: as células longe da cidade. Ele deve ser o tamanho fino vezes 2, 4, 8 e
  assim por diante. O padrão é quatro vezes o tamanho fino.
- **Fine-grid buffer (m)**: até onde, ao redor da cidade, chegam as células finas (120 m por
  padrão).

Entre os níveis, a transição usa duas células por nível, e células vizinhas diferem no máximo por um
fator de dois. Os rios não mudam o tamanho da célula. Com 90 m e 360 m, por exemplo, a cidade e os
120 m ao redor dela têm células de 90 m, depois vem uma faixa de células de 180 m, e o resto da
bacia tem células de 360 m. O modelo lê essa malha diretamente com o seu solver de malha nativo.

## Forcing and model adapter {#forcing}

**Rainfall product** escolhe uma única fonte de chuva para o caso inteiro. O Builder nunca completa
um produto com outro.

| Rainfall product | Passo de tempo | Área | Conta |
|---|---|---|---|
| **IMERG (30 minutes)** | 30 min | global | NASA Earthdata |
| **MSWEP (hourly)** | 1 h | global | aprovação da GloH2O e rclone |
| **MSWEP (3 hourly)** | 3 h | global | aprovação da GloH2O e rclone |
| **ERA5 (hourly)** | 1 h | global | Copernicus CDS |
| **AORC CONUS (hourly, approximately 1 km)** | 1 h | Estados Unidos contíguos | nenhuma |

Antes da prévia, a página mostra o período de cada fonte (por exemplo "NASA IMERG Final Run
availability") e não aceita um pedido fora dele. Os casos MSWEP horários começam em uma hora UTC
cheia, e os de 3 horas às 00, 03, 06, 09, 12, 15, 18 ou 21 UTC. O clima sempre vem do ERA5. A chuva e
o clima ficam nas suas próprias grades, e o HydroPol2D os amostra durante a simulação: uma grade de
90 m no modelo não dá à chuva uma resolução de 90 m.

**Prepare for** escolhe os arquivos de modelo que o caso recebe:

| Prepare for | O caso recebe |
|---|---|
| **HydroPol2D Python** | `hydropol_python/case.yaml` e `run_case.py`, para o HydroPol2D Studio |
| **HydroPol2D MATLAB** | `hydropol_matlab/run_case.m`, para o HydroPol2D MATLAB |
| **Python and MATLAB** | os dois |
| **Inputs only** | os mapas e as séries, sem arquivos de modelo |

## Simulated processes {#processes}

**Canopy interception**, **Infiltration**, **Groundwater** e **Evapotranspiration** vêm marcados
por padrão. Desmarque um processo para deixá-lo de fora. Os mapas que dependem dele saem então das
saídas salvas, e as configurações de águas subterrâneas abaixo ficam desativadas quando
**Groundwater** está desligado. A chuva, o roteamento superficial inercial local e os contornos de
escoamento crítico continuam sempre ligados.

## River representation {#river-representation}

**Subgrid formulation** define como são representados os rios mais estreitos que uma célula:

| Opção | O que ela faz |
|---|---|
| **Auto** | **No subgrid** quando as maiores células coincidem com a resolução do terreno. Caso contrário, **Neal channel** em grades uniformes e **Hydraulic tables** em grades quadtree e em casos Urban Area Only. |
| **Neal channel** | um canal de largura e profundidade dadas dentro de cada célula de rio. Só em grades uniformes, então não é oferecido para grades quadtree nem para Urban Area Only. |
| **Hydraulic tables** | tabelas de armazenamento e de condução calculadas a partir do terreno fino. **Hydraulic table coverage** escolhe **Rivers only** ou **All active cells**. |
| **No subgrid** | só o terreno da célula. |

**All active cells** trata cada célula como um reservatório de nível horizontal (level pool). A
página avisa que isso pode distorcer o escoamento gerado pela chuva em encostas íngremes, então
escolha essa opção de propósito. O terreno condicionado pelo HydroBathyDEM vira a superfície do
modelo. Depois da montagem, a página informa a parcela de células que o condicionamento alterou, o
maior rebaixamento e a maior elevação.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-river-hydraulics.png')} width="760" alt="As caixas de seleção de Simulated processes, as opções de River representation Auto, Neal channel, Hydraulic tables e No subgrid, e o painel Hydraulic parameters aberto, com os valores de n de Manning, a troca rio-águas subterrâneas, as configurações do aquífero profundo, a fonte dos parâmetros do aquífero raso, a condutividade e a espessura do leito do rio, a caixa de confirmação e o raster opcional de condutividade do leito do rio" />
</p>

<p align="center">
  <em>Figura 1. Simulated processes, River representation e o painel Hydraulic parameters aberto, em um caso Urban Basin. As configurações do aquífero profundo estão desativadas porque Deep-aquifer baseflow está desligado.</em>
</p>

### Hydraulic parameters {#hydraulic-parameters}

O painel **Hydraulic parameters** vem recolhido por padrão.

| Configuração | Padrão | O que ela define |
|---|---|---|
| **Channel Manning n** | 0,035 | rugosidade dos canais dos rios |
| **Surface Manning fallback** | 0,05 | rugosidade onde a tabela de cobertura do solo não tem valor |
| **River-groundwater exchange** | ligado | troca de água entre os rios e as águas subterrâneas (exige **Groundwater**) |
| **Deep-aquifer baseflow** | ligado em Catchment | um reservatório profundo e lento por sub-bacia, que alimenta o escoamento de base (aba Catchment, sem tabelas hidráulicas) |
| **Deep recharge fraction** | 0,05 | parcela da recarga que vai para o reservatório profundo |
| **Deep response time (days)** | 180 | a lentidão com que o reservatório profundo se esvazia |
| **Subbasin threshold (km²)** | 100 | o tamanho das sub-bacias do aquífero profundo |
| **Deep-aquifer starting state** | Empty | **Empty**, **Baseflow on the start date** (com **Deep baseflow q0 (mm/day)**) ou **Steady state from mean recharge** (com **Mean recharge (mm/year)**) |
| **Shallow-aquifer Ksat,h and Sy** | Spatial maps with class fallback | veja abaixo |
| **Riverbed conductivity (m/s)** | 1,0e-6 | condutividade do leito do rio para a troca |
| **Riverbed thickness (m)** | 0,50 | espessura do leito do rio |
| **Confirm this riverbed conductivity for the case** | desmarcada | precisa estar marcada enquanto a troca estiver ligada |
| **Riverbed conductivity raster (optional)** | vazio | um mapa que substitui o valor único |

A condutividade do leito do rio não tem um mapa global confiável, então o Builder pede que você
confirme o valor. Com a troca ligada e a caixa desmarcada, a prévia para com "Confirm riverbed
hydraulic conductivity when river-groundwater exchange is enabled."

**Shallow-aquifer Ksat,h and Sy** define a condutividade horizontal e o rendimento específico do
aquífero raso:

- **Spatial maps with class fallback**: os mapas de águas subterrâneas onde eles têm valores, e as
  tabelas de classes no restante.
- **Uniform effective values**: um único **Uniform groundwater Ksat,h (m/s)** (padrão 1,000e-5) e um
  único **Uniform specific yield Sy** (padrão 0,100) sobre todo o domínio, por exemplo valores de
  uma calibração por recessão.
- **Calibrate from observed streamflow**: aba Catchment, quando o caso é preparado para Python. O
  caso é preparado primeiro, e a calibração roda depois a partir de **Check a case**
  ([Verificar um caso](check-a-case#groundwater-calibration)).

## Saved outputs {#saved-outputs}

| Configuração | O que ela define |
|---|---|
| **Output package** | **Quick** salva os extremos e os hidrogramas. **Standard** acrescenta o arquivo nativo de mapas, as figuras e os vídeos principais. **Full** também grava cópias em GeoTIFF de cada mapa salvo. |
| **Map interval (minutes)** | a frequência com que os mapas são salvos |
| **Hydrograph interval (minutes)** | a frequência com que os hidrogramas e os diagnósticos são salvos |

As caixas de seleção abaixo escolhem os mapas salvos: profundidade de inundação fora da calha,
velocidade no canal e na planície de inundação, intensidade da chuva, chuva acumulada, infiltração
acumulada, profundidade do lençol freático, recarga acumulada das águas subterrâneas, ascensão
capilar acumulada, saturação da zona radicular, saturação da zona de transmissão, evaporação
potencial acumulada e evapotranspiração real acumulada. Um mapa cujo processo está desligado fica
desativado. A prévia estima o tamanho do que você escolher.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-saved-outputs.png')} width="760" alt="O grupo Saved outputs com Output package Standard, intervalo dos mapas de 60 minutos, intervalo dos hidrogramas de 10 minutos e doze saídas de mapa marcadas" />
</p>

<p align="center">
  <em>Figura 2. Saved outputs de um caso urbano: o pacote Standard, mapas a cada hora, hidrogramas a cada 10 minutos e os doze mapas.</em>
</p>

## Urban boundary conditions {#urban-boundary-conditions}

Este grupo fica na aba **Urban Area Only**.

| Configuração | O que ela define |
|---|---|
| **Exterior buffer (km)** | a faixa ao redor da mancha urbana (1 km por padrão) |
| **GloFAS river inflows** | vazões de entrada dos rios do GloFAS v4 onde os rios entram no domínio. A vazão de entrada usa a largura do canal do mapa de rios do caso. |
| **GloFAS time handling** | **step** ou **linear** entre os valores do GloFAS |
| **Coastal water level** | **Disabled**, **GTSM total water level** ou **GTSM astronomical tide** |
| **Tide time handling** | **linear** ou **step** entre os valores do GTSM |
| **Groundwater boundary** | **Local storage only**, **Dynamic no-flow** ou **Dynamic fixed head** |
| **GTSM-to-model datum offset (m)** e **Datum confirmed** | aparecem quando um nível costeiro está ligado. O GTSM se refere ao nível médio do mar. Digite a diferença local até o datum do terreno e marque **Datum confirmed**. Zero, confirmado, diz que os dois são iguais nesse local. |
| **Reviewed boundary overrides (optional JSON)** | um arquivo com escolhas de contorno revisadas |

A maré vai só para as células externas baixas que o WorldCover marca como água permanente, perto da
costa do GTSM. O GTSM dá o nível da água, não a linha de costa. As séries do GTSM terminam em 2024,
então datas posteriores exigem **Disabled**. A montagem grava o plano e as séries dos contornos em
`processed_inputs/Forcing/Boundary`, e a verificação não passa se bordas se sobrepõem ou se um
contorno ligado não tem dados.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-urban-boundaries.png')} width="760" alt="O grupo Urban boundary conditions com faixa externa de 1 km, GloFAS river inflows desmarcado, GloFAS time handling step, coastal water level Disabled, tide time handling linear, groundwater boundary Local storage only e um campo de substituições vazio, com a nota de que a prioridade é maré, depois vazão de entrada do GloFAS, depois escoamento crítico" />
</p>

<p align="center">
  <em>Figura 3. Urban boundary conditions nos padrões: escoamento crítico em cada borda externa.</em>
</p>

## Pastas de chuva {#rainfall-folders}

**Existing rainfall directory (optional)** usa arquivos de chuva que você já tem, em vez de um
download. A pasta precisa ter cada passo de tempo, do início do aquecimento ao fim da simulação,
como GeoTIFFs em mm/h com nomes assim:

```text
IMERG_30min_mmhr_YYYY_MM_DD_HH_MM.tif
AORC_1h_mmhr_YYYY_MM_DD_HH_MM.tif
ERA5_1h_mmhr_YYYY_MM_DD_HH_MM.tif
MSWEP_1h_mmhr_YYYY_MM_DD_HH_MM.tif
MSWEP_3h_mmhr_YYYY_MM_DD_HH_MM.tif
```

Para um produto MSWEP sem pasta local, aparecem mais dois campos: **MSWEP rclone folder** e
**Shared-folder ID (optional)**. Quando o rclone já tem acesso à pasta do MSWEP, a página a encontra
e preenche os dois. Veja [Fontes de dados e contas](data-accounts#mswep).

## Folders and advanced paths {#folders}

O painel **Folders and advanced paths** vem recolhido por padrão.

| Configuração | O que ela define |
|---|---|
| **Output directory** | onde ficam os casos novos. No app: `Documents/HydroPol2D Case Builder/outputs`, na sua pasta pessoal. |
| **Cache directory** | onde os dados e as ferramentas baixados são guardados (`~/.cache/hydropol2d-case-builder`), em comum para todos os casos |
| **HydroPol2D checkout (optional)** | uma pasta do HydroPol2D MATLAB, registrada com o caso |
| **Vadose and aquifer parameters** | **Class tables** ou **SoilGrids + GLHYMPS (CONUS automatic)** |
| **Groundwater Kh/Kv ratio** | a razão entre a condutividade horizontal e a vertical, usada abaixo de 2 m (100 por padrão) |
| **Subsurface scheme** | **legacy** ou **layered** (camadas de solo sobre camadas de rocha até o embasamento rochoso, para o HydroPol2D Python) |
| **Rock specific yield** | só em layered: **derived_capped** (limitado pela porosidade do GLHYMPS) ou **derived** |
| **Spatial soil parameter raster directory (optional)** | uma pasta de GeoTIFFs de parâmetros do solo. Os valores deles substituem as tabelas de classes onde eles têm dados. |

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-folders.png')} width="760" alt="O painel Folders and advanced paths aberto, com o diretório de saída, o diretório de cache, um campo HydroPol2D checkout vazio, Vadose and aquifer parameters em Class tables, uma razão Kh/Kv de 100, subsurface scheme legacy, rock specific yield derived_capped desativado e o diretório de rasters de parâmetros espaciais do solo" />
</p>

<p align="center">
  <em>Figura 4. Folders and advanced paths. Rock specific yield está desativado porque o subsurface scheme é legacy.</em>
</p>
