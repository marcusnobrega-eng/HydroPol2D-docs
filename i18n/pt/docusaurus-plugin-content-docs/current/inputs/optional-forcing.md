---
title: Forçantes Opcionais
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Forçantes Opcionais

O HydroPol2D aceita vários tipos de forçantes meteorológicas e hidrológicas além de uma única série de chuva. Na planilha do caso MATLAB, `HydroPol2D_Inputs.xlsx`, as chaves ficam nas abas Rain and ET, Design storm, Soil and groundwater e Surface flow, as séries temporais ficam em cinco abas de séries e as listas de arquivos de mapas ficam na aba Rain and ET.

---

## Onde Cada Forçante é Definida {#where-each-forcing-is-set}

| Forçante | Chave (aba) | Dados |
|---|---|---|
| Série uniforme de chuva | `flag_rainfall` (Rain and ET), sem outra fonte de chuva | Aba Rain series |
| Pluviômetros, interpolados | `flag_spatial_rainfall` (Rain and ET) | Aba Rain gauges |
| Mapas de chuva | `flag_input_rainfall_map` (Rain and ET) | Lista Rainfall maps (aba Rain and ET) |
| Chuva por satélite | `flag_satellite_rainfall`, `flag_real_time_satellite_rainfall` (Rain and ET) | Preparada pelo fluxo de trabalho de satélite |
| Chuva de projeto | `flag_alternated_blocks` ou `flag_huff` (Design storm) | Configurações do hietograma e da IDF na mesma aba |
| Evapotranspiração por Penman–Monteith | `flag_ETP` (Soil and groundwater), sem mapas de ET | Aba Climate stations |
| Mapas de evaporação e transpiração | `flag_input_ETP_map` (Rain and ET) | Listas Transpiration maps e Evaporation maps (aba Rain and ET) |
| Hidrogramas de entrada | `flag_inflow` (Surface flow) | Aba Inflow hydrographs |
| Hidrogramas de nível | `flag_stage_hydrograph` (Surface flow) | Aba Stage hydrographs |

Use uma fonte de chuva por vez. Uma série que as chaves do caso não leem pode ficar como modelo vazio, com os seus cabeçalhos. Todas as chaves e configurações estão listadas em [Configurações da Planilha do Caso](../configuration/general_data).

---

## Chuva {#rainfall}

<p align="center">
  <a href={useBaseUrl('/img/workbook/rain-series.png')}><img src={useBaseUrl('/img/workbook/rain-series.png')} width="746" style={{maxWidth: '100%', height: 'auto'}} alt="A aba Rain series da planilha do caso" /></a>
</p>

<p align="center">
  <em>A aba Rain series da planilha do exemplo Stanford. Clique na imagem para abri-la em tamanho real.</em>
</p>


### Série uniforme {#uniform-series}

A aba Rain series contém um único pluviômetro, com a intensidade de chuva (mm/h) ao longo do tempo. A chuva é aplicada de forma uniforme sobre o domínio. A aba é lida quando a chuva está ativa e não há chuva de projeto, mapas, satélite nem chuva espacial selecionados.

Cada tempo marca o início de um intervalo. Um valor vale até o tempo seguinte; o último valor vale por mais um intervalo, e depois a taxa é 0. No exemplo V-tilted, 10.8 mm/h em 0 min e 0 mm/h em 90 min significam chuva de 10.8 mm/h de 0 a 90 min e nenhuma chuva de 90 a 180 min. A mesma regra vale para pluviômetros, mapas de chuva, mapas de evaporação e transpiração e hidrogramas de entrada. Um hidrograma de nível mantém cada profundidade do seu tempo até o seguinte.

:::warning[Alterado em 2026-10-29]
Antes de 2026-10-29, o MATLAB lia os tempos de chuva, vazão de entrada e mapas de ET como fim de intervalo, e o HydroPol2D-Python os lia como início de intervalo. Agora o MATLAB também os lê como início de intervalo. A primeira linha de uma tabela que começa em 0 min, como toda tabela com datas, passa a ser usada. Uma tabela escrita com fins de intervalo (primeiro tempo = um passo) precisa adiantar cada tempo em um passo para manter o seu significado. As chuvas de projeto são reajustadas automaticamente.
:::

### Pluviômetros {#rain-gauges}

A aba Rain gauges contém vários pluviômetros, interpolados para cada célula por ponderação pelo inverso da distância. Ela é lida quando `flag_spatial_rainfall = 1` e não há mapas de chuva. Cada pluviômetro ocupa uma coluna, com o seu índice, nome e coordenadas (m, na projeção do DEM) e, em seguida, a intensidade (mm/h) em cada tempo (min) da coluna B.

<p align="center">
  <a href={useBaseUrl('/img/workbook/rain-gauges.png')}><img src={useBaseUrl('/img/workbook/rain-gauges.png')} width="1700" style={{maxWidth: '100%', height: 'auto'}} alt="A aba Rain gauges da planilha do caso" /></a>
</p>

<p align="center">
  <em>A aba Rain gauges da planilha do exemplo Stanford. Clique na imagem para abri-la em tamanho real. O caso Stanford não usa esta aba; ela mantém as colunas do modelo.</em>
</p>


### Mapas de chuva {#rainfall-maps}

A lista Rainfall maps da aba Rain and ET tem uma linha por mapa, com o tempo em minutos desde a data inicial e o caminho de um GeoTIFF em mm/h. Ela é lida quando `flag_input_rainfall_map = 1` ou quando uma chave de chuva por satélite vale 1.

---

## Chuvas de Projeto {#design-storms}

A aba Design storm gera um hietograma sintético em vez de ler uma série de chuva.

| Configuração | Variável | Unidade |
|---|---|---|
| Blocos alternados ou curvas de Huff | `flag_alternated_blocks`, `flag_huff` | 0 / 1 |
| Período de retorno | `RP` | anos |
| Duração da chuva | `Rainfall Duration` | min |
| Passo de tempo do hietograma | `dt_design` | min |
| Coeficientes da IDF | `K`, `a`, `b`, `c` | ver abaixo |

A intensidade segue a relação IDF local

$$
i = \frac{K\,\mathrm{RP}^{a}}{(b + t_d)^{c}}
$$

em que $i$ é a intensidade (mm/h), $\mathrm{RP}$ é o período de retorno (anos) e $t_d$ é a duração (min). $K$ deve ser coerente com essas unidades, $a$ e $c$ são adimensionais e $b$ está em minutos. Use coeficientes ajustados para o local de estudo.

---

## Evapotranspiração {#evapotranspiration}

### Penman–Monteith a partir de estações climatológicas {#penman-monteith-from-climate-stations}

Com `flag_ETP = 1` e sem mapas de ET, o HydroPol2D calcula a evapotranspiração por Penman–Monteith a partir de dados meteorológicos diários de uma ou mais estações, interpolados para a grade por ponderação pelo inverso da distância. Na aba Climate stations, a linha 2 nomeia o bloco de cada estação (índice e coordenadas leste e norte em m), a linha 3 traz os cabeçalhos das colunas e cada linha a partir da linha 4 corresponde a um dia. As variáveis típicas são temperatura do ar, radiação, umidade relativa e velocidade do vento.

<p align="center">
  <a href={useBaseUrl('/img/workbook/climate-stations.png')}><img src={useBaseUrl('/img/workbook/climate-stations.png')} width="1700" style={{maxWidth: '100%', height: 'auto'}} alt="A aba Climate stations da planilha do caso" /></a>
</p>

<p align="center">
  <em>A aba Climate stations da planilha do exemplo Stanford. Clique na imagem para abri-la em tamanho real. O caso Stanford não usa esta aba; ela mantém as colunas do modelo.</em>
</p>


### Mapas de evaporação e transpiração {#evaporation-and-transpiration-maps}

Com `flag_input_ETP_map = 1`, o modelo lê duas listas da aba Rain and ET, Transpiration maps e Evaporation maps. Cada linha traz o tempo em dias desde a data inicial e o caminho de um GeoTIFF em mm/dia. As duas listas devem ter os mesmos tempos. Os fluxos são aplicados diretamente à água superficial e à umidade do solo, de modo que nenhuma forçante meteorológica é necessária.

:::warning[Corrigido em 2026-10-20]
Em `General_Data.xlsx`, as listas de chuva, transpiração e evaporação compartilham uma única linha de cabeçalho. Antes de 2026-10-20, a lista de transpiração lia a coluna `Time [min]` da lista de chuva (sem conversão de dias para minutos), e a lista de evaporação lia os caminhos da transpiração. As simulações com `flag_input_ETP_map = 1` feitas antes dessa data usaram tempos de ET e mapas de evaporação errados. Rode esses casos de novo. Cada lista agora termina na sua primeira linha vazia, e as suas colunas são procuradas apenas sob o seu próprio título, nos dois formatos.
:::

---

## Hidrogramas de Contorno {#boundary-hydrographs}

### Hidrogramas de entrada {#inflow-hydrographs}

A aba Inflow hydrographs, lida quando `flag_inflow = 1`, comporta até 50 postos. Cada posto é um bloco de cinco colunas, com o tempo (min), a vazão (m³/s) e as coordenadas leste e norte (m) de cada célula por onde a vazão entra, uma célula por linha. A vazão é distribuída entre essas células. Mantenha os 50 blocos, mesmo os vazios.

<p align="center">
  <a href={useBaseUrl('/img/workbook/inflow-hydrographs.png')}><img src={useBaseUrl('/img/workbook/inflow-hydrographs.png')} width="1700" style={{maxWidth: '100%', height: 'auto'}} alt="A aba Inflow hydrographs da planilha do caso" /></a>
</p>

<p align="center">
  <em>A aba Inflow hydrographs da planilha do exemplo Stanford. Clique na imagem para abri-la em tamanho real. O caso Stanford não usa esta aba; os nomes de postos do modelo foram omitidos da imagem.</em>
</p>


Os hidrogramas de entrada representam contornos de montante, vazões afluentes de rios e descargas por ruptura de barragem ou controladas.

### Hidrogramas de nível {#stage-hydrographs}

A aba Stage hydrographs, lida quando `flag_stage_hydrograph = 1`, tem o mesmo arranjo, com o tempo (min), a profundidade da água (m) e as coordenadas leste e norte (m) de cada célula do contorno. Todas as células de um contorno recebem a mesma profundidade imposta. Mantenha os 50 blocos, mesmo os vazios.

<p align="center">
  <a href={useBaseUrl('/img/workbook/stage-hydrographs.png')}><img src={useBaseUrl('/img/workbook/stage-hydrographs.png')} width="1700" style={{maxWidth: '100%', height: 'auto'}} alt="A aba Stage hydrographs da planilha do caso" /></a>
</p>

<p align="center">
  <em>A aba Stage hydrographs da planilha do exemplo Stanford. Clique na imagem para abri-la em tamanho real. O caso Stanford não usa esta aba; ela mantém as colunas do modelo.</em>
</p>


Os hidrogramas de nível representam controle de jusante, remanso e outras restrições hidráulicas.

---

## Considerações Práticas {#practical-considerations}

- Mantenha todas as forçantes na mesma referência de tempo de `date_begin` e `date_end`.
- Confira as unidades de cada série, com a chuva em mm/h, os mapas de ET em mm/dia, a vazão de entrada em m³/s e o nível em m.
- Não misture fontes de chuva, e confira se os pluviômetros e as células de contorno estão na projeção do DEM.
- Use um intervalo de forçante que resolva os picos necessários, considerando o passo de tempo do modelo.

---

## Formato Antigo {#older-layout}

Nos casos que usam `General_Data.xlsx`, cada série fica em uma planilha própria, na mesma pasta. São elas `Rainfall_Intensity_Data.xlsx` (Rain series), `Rainfall_Spatial_Input.xlsx` (Rain gauges), `ETP_input_data.xlsx` (Climate stations), `Inflow_Hydrograph.xlsx` e `Stage_Hydrograph.xlsx`. As listas de mapas são as tabelas Satellite or Radar Rainfall, Satellite transpiration e Satellite evaporation de `General_Data`. A planilha do caso mantém o mesmo arranjo de células, e por isso o modelo lê os dois formatos da mesma forma.
