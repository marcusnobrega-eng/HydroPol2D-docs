---
title: Linha de comando
---

# Linha de comando

O app também é a linha de comando do Case Builder, `hydropol-case`, para scripts e lotes de casos.
Ele usa o mesmo código de licença e o mesmo cache do app.

| Computador | Comando |
|---|---|
| Mac | `"/Applications/HydroPol2D Case Builder.app/Contents/MacOS/HydroPol2D Case Builder"` |
| Windows | `hydropol-case.exe`, na pasta em que você descompactou o app |

No Mac, um nome curto poupa digitação. Acrescente esta linha a `~/.zshrc` e abra um novo Terminal:

```bash
alias hydropol-case='"/Applications/HydroPol2D Case Builder.app/Contents/MacOS/HydroPol2D Case Builder"'
```

Os exemplos abaixo usam `hydropol-case`.

## Comandos {#commands}

| Comando | O que faz |
|---|---|
| `hydropol-case urban` | um caso Urban Basin |
| `hydropol-case urban-only` | um caso Urban Area Only |
| `hydropol-case catchment` | um caso Catchment |
| `hydropol-case preflight CASE_DIR` | verifica um caso preparado. Imprime `Ready to run: True` ou a lista de problemas. |
| `hydropol-case license status` | mostra para quem é a licença guardada e quantos dias faltam |
| `hydropol-case license activate` | confere um código e o guarda (pede o código quando você não o informa) |

`hydropol-case urban --help`, e o mesmo nos outros comandos, lista todas as opções.

## Prévia primeiro {#preview-first}

`--plan-only` para depois da prévia: ele delimita o domínio, grava `case.json`, `domain.gpkg` e os
mapas da prévia e imprime o tamanho do caso. Esta prévia Catchment do San Francisquito Creek leva
alguns segundos:

```bash
hydropol-case catchment \
  --name "San Francisquito Creek" \
  --outlet-lon -122.1889 --outlet-lat 37.4239 \
  --resolution 30 \
  --start "2023-01-08 00:00" --end "2023-01-10 00:00" --warmup-days 0 \
  --rainfall aorc \
  --configure-hydropol matlab \
  --riverbed-hydraulic-conductivity-m-s 1e-6 \
  --plan-only
```

Ela imprime, entre outras linhas:

```text
Domain area: 107.8 km2
Matrix: 523 rows x 422 columns (220,706 cells)
Estimated active cells: 119,737
Temporary source-transfer ceiling: 2.8 MiB
Estimated retained forcing inputs: 0.1 MiB
Case directory: /…/outputs/san_francisquito_creek_candidate1_30m_20230108
```

Abra `figures/domain_preview.html` na pasta do caso para ver o domínio em um mapa.

## Preparar o caso {#prepare}

Rode o mesmo comando sem `--plan-only`. Ele mostra a prévia de novo e pergunta
`Continue preparing this case? [y/N]`. Responda `y` depois de ler o tamanho. `--yes` pula a
pergunta, para scripts cujo domínio você já revisou. Um caso completo termina com:

```text
Complete HydroPol2D input package created and accepted by preflight.
```

Este caso Urban Area Only de Tucson, no Arizona, com células de 250 m, para um dia, com chuva do
AORC e modelos para Python e MATLAB, foi preparado com:

```bash
hydropol-case urban-only \
  --city Tucson --country "United States" \
  --resolution 250 \
  --start "2021-07-23 00:00" --end "2021-07-24 00:00" --warmup-days 0 \
  --rainfall aorc \
  --configure-hydropol both \
  --dem-source fabdem \
  --riverbed-hydraulic-conductivity-m-s 1e-6 \
  --yes
```

A aba **Python and command line** do app mostra o comando para as configurações atuais da aba
**Urban Basin**, com todas as opções por extenso. Copie-o para repetir um caso a partir de um
script.

## Padrões diferentes dos do app {#defaults}

| Opção | Linha de comando | App |
|---|---|---|
| `--warmup-days` | 30 | 0 |
| `--configure-hydropol` | `none` (só entradas) | HydroPol2D Python |
| `--dem-source` | `copernicus_glo30` | FABDEM |
| `--output-dir` | `outputs` na pasta atual | `Documents/HydroPol2D Case Builder/outputs` |

Com a troca rio-águas subterrâneas ligada (o padrão), informe `--riverbed-hydraulic-conductivity-m-s`,
que faz o papel da caixa de confirmação do app. `--no-river-groundwater-exchange` ou
`--no-groundwater` desligam a troca.

## Opções {#options}

As opções mais usadas. Todas as datas são em UTC.

| Opção | O que ela define |
|---|---|
| `--city NAME --country COUNTRY` | uma cidade do GHSL (urban e urban-only) |
| `--polygon PATH` | o seu próprio polígono (urban e urban-only), ou um polígono de bacia ou de busca (catchment, com `--polygon-mode exact` ou `search`) |
| `--name NAME` | o nome do caso (catchment) |
| `--outlet-lon`, `--outlet-lat` | o exutório em graus (catchment) |
| `--outlet-point PATH` | um arquivo vetorial com um ponto de exutório (catchment) |
| `--candidate-rank 1\|2\|3` | o candidato de exutório (catchment, padrão 1) |
| `--snap-radius-km`, `--outlet-cells` | o raio de ajuste e as células críticas no exutório (catchment) |
| `--resolution METRES` | o tamanho da célula (obrigatório) |
| `--grid-mode uniform\|quadtree` | o tipo de grade (urban e urban-only) |
| `--coarse-resolution`, `--urban-refinement-buffer` | o tamanho da célula grossa e a faixa da grade fina na quadtree |
| `--start`, `--end`, `--warmup-days` | o período (início e fim obrigatórios) |
| `--rainfall PRODUCT` | `imerg`, `era5`, `mswep-hourly`, `mswep-3hourly` ou `aorc` (obrigatório) |
| `--configure-hydropol MODE` | `python`, `matlab`, `both` ou `none` |
| `--dem-source SOURCE` | `fabdem`, `local` (com `--source-dem PATH`), `usgs_3dep` (Estados Unidos, 10 m) ou `copernicus_glo30` |
| `--river-area-km2 AREA` | a área de início dos rios (padrão 5) |
| `--subgrid-method`, `--hydraulic-table-coverage` | a representação dos rios: `auto`, `neal`, `hydraulic_tables` ou `none`, e `rivers` ou `all` |
| `--no-canopy-interception`, `--no-infiltration`, `--no-groundwater`, `--no-evapotranspiration` | deixam um processo de fora |
| `--deep-aquifer` e as opções `--deep-...` | o escoamento de base do aquífero profundo (catchment) |
| `--groundwater-parameter-source`, `--groundwater-ksat-h-m-s`, `--groundwater-specific-yield` | os parâmetros do aquífero raso (`spatial`, `uniform` ou `calibration`) |
| `--urban-buffer-km`, `--glofas-inflow`, `--coastal-tide`, `--tide-datum-offset-m`, `--groundwater-boundary` | as condições de contorno urbanas (urban-only) |
| `--output-profile`, `--map-output-interval-minutes`, `--diagnostic-output-interval-minutes`, `--output-map-variable` | as saídas salvas |
| `--rainfall-source-dir PATH` | arquivos de chuva que você já tem |
| `--mswep-rclone-source`, `--mswep-rclone-root-folder-id` | a pasta do MSWEP |
| `--output-dir`, `--cache-dir` | as pastas do caso e do cache |
| `--plan-only`, `--yes` | parar depois da prévia, ou pular a pergunta |

A linha de comando tem algumas opções que o app não mostra, entre elas:

| Opção | O que ela define |
|---|---|
| `--land-cover worldcover\|nlcd` | ESA WorldCover (global, padrão) ou USGS NLCD 2021 com impermeabilidade (os 48 estados contíguos) |
| `--snow`, `--water-quality`, `--human-risk` | neve, acúmulo e lavagem de poluentes e perigo da inundação para as pessoas (HydroPol2D Python) |
| `--layer NAME=PATH` | o seu próprio raster para uma camada: `lulc`, `soil`, `depth_to_bedrock`, `groundwater_table`, `impervious_fraction`, `lai`, `initial_soil_moisture`, `initial_swe` ou `initial_snow_depth` (repita para mais camadas) |
| `--refinement-polygon PATH`, `--river-corridor` | quadtree: refinar ao redor de outro polígono, ou manter os rios e a sua planície de inundação no tamanho fino |
| `--rainfall dataset --rainfall-dataset PATH` | chuva de um arquivo NetCDF ou Zarr (com `--rainfall-interval-minutes`) |
| `--rainfall meteostat` | chuva horária das estações do Meteostat, mantida como pluviômetros (HydroPol2D Python) |
| `--meteorology-source era5\|meteostat\|dataset` | a fonte do clima |
| `--imerg-run final\|late\|auto` | a versão (run) do IMERG (padrão `final`) |

## Códigos de saída {#exit-codes}

`0` quando o comando deu certo (no `preflight`, quando o caso está pronto), `2` quando o caso não
está pronto, o pedido tem um erro ou a licença está ausente ou inválida. Em um terminal, a falta de
licença faz o comando pedir o código uma vez.
