---
title: DEM
---

# Modelo Digital de Elevação (DEM)

O Modelo Digital de Elevação (DEM) define a estrutura topográfica do domínio de simulação e é o controle primário na dinâmica do fluxo superficial em HydroPol2D.
É uma das entradas mais críticas do modelo, pois governa os gradientes do terreno, as direções dos fluxos e a organização espacial dos processos hidrológicos.

---

## Função em HydroPol2D

O DEM é usado para calcular:
- Elevação da superfície em todo o domínio
- Encostas locais impulsionam o roteamento do fluxo
- Conectividade de fluxo entre células da grade
- Limites de bacias hidrográficas e padrões de drenagem

Como o HydroPol2D opera em uma grade raster, o DEM também define a malha computacional na qual todos os processos de superfície são simulados.

---

## Conjuntos de dados DEM disponíveis

Vários conjuntos de dados DEM globais de alta qualidade estão disponíveis gratuitamente e são adequados para aplicações HydroPol2D:
### SRTM (Missão de Topografia de Radar Shuttle)
- Resolução: ~30 m (1 segundo de arco)
- Cobertura: Quase global (±60° de latitude)
- Amplamente utilizado e facilmente acessível
- Pode conter vegetação e artefatos urbanos
- Baixar: https://earthexplorer.usgs.gov/

---

### Copérnico DEM (GLO-30 / GLO-90)
- Resolução: 30 m e 90 m
- Conjunto de dados globais de alta qualidade
- Consistência melhorada e menos vazios que SRTM
- Recomendado para aplicações gerais
- Baixar: https://spacedata.copernicus.eu/

---

### FABDEM (Floresta e edifícios removidos DEM)
- Resolução: ~30 m
- Derivado de Copérnico DEM
- Desvios de vegetação e construção removidos
- Particularmente útil para modelagem hidrológica
- Baixar: https://data.bris.ac.uk/data/dataset/25wfy0f9ukoge2gs7a5mqpq2j7

---

### MÉRITO DEM
- Resolução: ~90 m
- DEM global com redução de erros
- Corrigido para vários vieses (listras, ruído, efeitos de vegetação)
- Adequado para simulações em grande escala
- Baixar: http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/

---

### USGS 3DEP (Programa de Elevação 3D)
- Região: Estados Unidos
- Resolução: 1 m a 10 m (dependendo da localização)
- Inclui DEMs derivados de LiDAR de alta resolução
- Uma das melhores fontes para estudos baseados nos EUA
- Baixar: https://apps.nationalmap.gov/downloader/

---

## Dados de alta resolução (recomendado)

Se disponíveis, **LiDARs baseados em LiDAR** são fortemente recomendados.
Vantagens:- Resolução espacial muito alta (de submetros a alguns metros)
- Representação precisa do terreno e microtopografia
- Melhor representação de caminhos de fluxo, canais e características urbanas

Esses conjuntos de dados são particularmente valiosos para:
- Modelagem de inundações urbanas
- Pequenas bacias hidrográficas
- Análise hidráulica detalhada

### Dados LiDAR (Estados Unidos)

Os dados LiDAR para os EUA podem ser acessados ​​através de:
- Mapa Nacional USGS (3DEP): https://apps.nationalmap.gov/downloader/
- Costa Digital NOAA: https://coast.noaa.gov/dataviewer/#/lidar/search/

Essas plataformas fornecem acesso a conjuntos de dados de elevação de alta resolução derivados de levantamentos aéreos LiDAR.

---

## Coordenar requisitos do sistema

O DEM **deve estar em um sistema de referência de coordenadas projetadas (CRS)**.
- Coordenadas geográficas (latitude/longitude) **não suportadas**
- As unidades devem estar em **metros**
- Distâncias e inclinações devem ser fisicamente significativas

Todas as outras entradas raster (LULC, Solo, DTB, LAI, Albedo) devem:
- Use o **mesmo CRS**
- Têm a **mesma resolução espacial**
- Compartilhe a **mesma extensão espacial**

---

## Definição e mascaramento de domínio

Na prática, os rasters de entrada podem não se sobrepor perfeitamente.
HydroPol2D lida com isso:
- Definindo um **domínio comum mínimo**
- Criando uma máscara onde **todos os rasters necessários são válidos**
- Restringindo simulações a este domínio consistente

Isso garante:
- Nenhum dado faltante durante a simulação
- Acoplamento consistente entre processos
- Estabilidade numérica

---

## Reamostragem e alinhamento

Se os rasters de entrada não estiverem alinhados, HydroPol2D fornece uma **opção de reamostragem**.
Quando o sinalizador de reamostragem é ativado:
- O DEM é automaticamente interpolado para corresponder à grade do modelo
- **Interpolação bilinear** é usada

Isso permite que os usuários:
- Integre conjuntos de dados com diferentes resoluções
- Evite o pré-processamento manual em software GIS

No entanto, os usuários ainda devem garantir que:
- A reamostragem não introduz artefatos
- A resolução permanece apropriada para a escala de simulação

---

## Recomendações de pré-processamento

Antes de usar um DEM, os usuários devem:
- Verifique se há valores ausentes ou vazios
- Remova ruídos ou artefatos
- Garanta o alinhamento adequado com outros rasters
- Verifique CRS e unidades
- Avalie se é necessária suavização ou filtragem

Em alguns casos, o preenchimento ou condicionamento da depressão pode ser aplicado dependendo dos objetivos da modelagem.

---

## Uso de DEM vs. DSM em diferentes aplicações

Deve-se ter cuidado ao selecionar o tipo de modelo de elevação dependendo da abordagem de modelagem.
Para **simulações de chuva na rede**, onde a chuva é aplicada diretamente em todo o domínio, é recomendado usar um **DEM** de terra nua. Os Modelos Digitais de Superfície (MDS), que incluem edifícios e outras estruturas elevadas, podem introduzir inclinações e barreiras artificiais que não são consistentes com os pressupostos da formulação inercial local. As arestas dos edifícios podem gerar gradientes irrealistas que levam a um comportamento de fluxo não físico.
Em contraste, para **simulações fluviais** conduzidas por hidrogramas de afluência nos limites do domínio, os DSMs podem ser usados ​​para representar melhor as características urbanas, desde que as profundidades simuladas da água permaneçam fisicamente consistentes e não excedam as elevações dos edifícios.
Portanto:
- **Aplicações de chuva na rede** → use **DEM em terra nua**
- **Aplicações fluviais/orientadas por limites** → O DSM pode ser usado com cuidado

---

## Resumo

O DEM fornece a base geométrica e hidráulica das simulações HydroPol2D.
Sua resolução, precisão e consistência com outras entradas influenciam diretamente o desempenho do modelo, a estabilidade numérica e o realismo físico.
A seleção cuidadosa e o pré-processamento do DEM são essenciais para obter resultados de simulação confiáveis.
