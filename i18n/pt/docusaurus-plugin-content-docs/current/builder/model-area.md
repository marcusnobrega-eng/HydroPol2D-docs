---
title: Escolher a área do modelo
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Escolher a área do modelo

**Prepare a case** tem três abas, uma para cada tipo de área do modelo: **Urban Basin**,
**Urban Area Only** e **Catchment**. Cada aba guarda todas as configurações do seu caso, então você
pode manter um caso diferente em cada uma. Os campos começam com valores de exemplo. Substitua-os
pelo seu próprio local e pelas suas datas.

<p align="center">
  <img src={useBaseUrl('/img/builder/case-builder-areas.pt.svg')} width="760" alt="Três mapas esquemáticos. Urban Basin: uma cidade na extremidade de jusante de várias bacias a montante, todas dentro de uma mesma borda do domínio. Urban Area Only: uma cidade dentro de uma faixa, com dois rios entrando pela borda e o mar em um canto. Catchment: uma bacia com a sua rede de rios, o exutório que você informa e três exutórios candidatos no rio" />
</p>

<p align="center">
  <em>Figura 1. Os três tipos de área do modelo, como mapas esquemáticos. A linha preta grossa é a borda do domínio do modelo.</em>
</p>

| Aba | Domínio | Use para |
|---|---|---|
| **Urban Basin** | a cidade e todas as bacias HydroBASINS de nível 12 a montante dela | inundações urbanas em que a água vinda de montante importa |
| **Urban Area Only** | a mancha urbana e uma faixa ao redor dela | só a cidade, com vazões de entrada dos rios e níveis costeiros na sua borda |
| **Catchment** | tudo o que fica a montante de um exutório que você escolhe | uma bacia hidrográfica, com ou sem cidade |

## Urban Basin {#urban-basin}

**Location input** oferece **City name** ou **Polygon file**.

- **City name**: digite a **City** e o **Country**. O Builder procura a cidade no GHSL Urban Centre
  Database R2024A.
- **Polygon file**: o caminho do seu próprio polígono urbano em **Urban polygon path** (um
  GeoPackage, um Shapefile ou qualquer outro arquivo vetorial que o GeoPandas consiga ler). Use essa
  opção quando o GHSL não lista a cidade ou quando você precisa de outro limite.

O Builder faz a interseção da cidade com as bacias HydroBASINS de nível 12 e segue as ligações delas
para montante. O domínio é a cidade e todas essas bacias a montante. O nível 12 do HydroBASINS é o
nível global mais fino, mas continua sendo um contorno regional. O FABDEM e o HydroBathyDEM dão o
terreno e o roteamento dentro dele.

As duas abas urbanas oferecem dois tipos de grade: uma **Uniform grid** ou uma **Quadtree grid**,
que mantém células finas na cidade e grossas no resto ([Configurações do caso](settings#grid-and-period)).

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-urban-basin.png')} width="760" alt="A aba Urban Basin com City Tucson e Country United States, a Quadtree grid selecionada, tamanho de célula fina de 90 m, tamanho de célula grossa de 360 m, faixa da grade fina de 120 m, aquecimento de 0 dias, área de início dos rios de 5 km2, fonte do terreno FABDEM e as datas e horas da simulação em UTC" />
</p>

<p align="center">
  <em>Figura 2. A aba Urban Basin para Tucson, no Arizona, com uma grade quadtree de células de 90 m sobre a cidade e de 360 m sobre o resto da bacia.</em>
</p>

## Urban Area Only {#urban-area-only}

A entrada da localização é a mesma do Urban Basin. O domínio é a mancha urbana conectada e uma
faixa ao redor dela (**Exterior buffer**, 1 km por padrão), sem as bacias a montante.

Cada borda externa do domínio recebe uma condição de contorno. O escoamento crítico é o padrão. Onde
se aplicam, **GloFAS river inflows** e um **Coastal water level** do GTSM o substituem, nesta ordem
de prioridade: maré, depois vazão de entrada do GloFAS, depois escoamento crítico. As configurações
estão em [Urban boundary conditions](settings#urban-boundary-conditions).

A prévia lista, em **Rivers entering the domain**, os pontos em que os rios do HydroRIVERS cruzam a
borda do domínio, em um mapa e em uma tabela. Na tabela, você pode desmarcar **accepted** em um
cruzamento ou movê-lo com a sua **longitude** e **latitude**. **Save river-entry review** salva as
suas escolhas, e **Prepare complete case** as usa.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-river-entries.png')} width="700" alt="Rios que entram no domínio de Tucson: um mapa do domínio só urbano com as linhas do HydroRIVERS e pontos vermelhos de entrada dos rios na sua borda e, abaixo, a tabela de candidatos com o ID do rio, a área a montante, a longitude, a latitude e uma caixa de seleção accepted, e o botão Save river-entry review" />
</p>

<p align="center">
  <em>Figura 3. Rios que entram no domínio só urbano de Tucson, depois da prévia. Cada ponto vermelho é um lugar onde um rio cruza a borda do domínio. A tabela os lista com a sua área a montante.</em>
</p>

Os casos Urban Area Only rodam no solver de malha nativo do HydroPol2D (UGRID), nos dois tipos de
grade.

## Catchment {#catchment}

Dê ao caso um **Catchment name** e escolha como informar o exutório em **Outlet input**:

| Outlet input | O que você informa |
|---|---|
| **Map click** | clique no exutório em um mapa topográfico. A página mostra a latitude e a longitude clicadas. |
| **Coordinates** | **Longitude** e **Latitude** em graus (WGS 84). |
| **Point file** | um arquivo vetorial com um ponto. |
| **Polygon file** | um polígono, usado **exact** (como a bacia) ou como área de busca, **search** (**Polygon use**). |

Mais três configurações posicionam o exutório na rede de rios:

- **Snap radius (km, 0 = automatic)**: até onde o exutório pode se mover para chegar ao rio. O
  automático é o maior valor entre 1 km e duas células do modelo.
- **Outlet candidate**: a prévia encontra as três células de exutório próximas com a maior
  acumulação de fluxo do HydroSHEDS. Escolha 1, 2 ou 3. Mudar essa escolha atualiza a prévia
  sozinha.
- **Critical outlet cells**: o número de células de contorno conectadas, no exutório, que recebem
  uma condição de profundidade crítica (10 por padrão).

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-prepare-catchment.png')} width="760" alt="A aba Catchment para o San Francisquito Creek: nome da bacia, Coordinates selecionado com longitude -122,1889 e latitude 37,4239, raio de ajuste 0, candidato de exutório 1, 10 células críticas no exutório, tamanho de célula de 10 m, as datas, chuva IMERG, HydroPol2D Python e os quatro processos simulados marcados" />
</p>

<p align="center">
  <em>Figura 4. A aba Catchment para o San Francisquito Creek, em Stanford, na Califórnia, com o exutório dado pelas suas coordenadas e uma grade de 10 m.</em>
</p>

A prévia desenha um primeiro contorno da bacia a partir do HydroSHEDS. A montagem completa então
preenche as depressões do terreno na resolução do modelo, calcula as direções de fluxo D8, ajusta de
novo o exutório ao rio e traça todas as células a montante. A bacia final e o primeiro contorno são
guardados. Se as áreas deles diferirem por um fator maior que dois, o caso não passa na verificação
até que você o revise (tente outro candidato ou um raio de ajuste maior).

Os casos Catchment usam uma grade uniforme. Eles são os únicos casos com o escoamento de base do
aquífero profundo e a calibração das águas subterrâneas a partir da vazão observada
([Configurações do caso](settings#hydraulic-parameters)).
