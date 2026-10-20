---
title: Rodar pelo Excel
---

# Rodar o HydroPol2D pelo Excel

O HydroPol2D aceita duas fontes de configuração. No modo Excel, o modelo lê
os parâmetros das planilhas. No modo `bypass`, ele lê os mesmos tipos de
parâmetros dos arquivos MATLAB na pasta `Config/`. Os dois caminhos usam o
mesmo solver numérico.

## Comece pelo exemplo testado

O repositório inclui um caso V-tilted pequeno para as duas meshes:

| Mesh | Planilha principal | Launcher MATLAB |
|---|---|---|
| Grade raster regular | `General_Data_regular.xlsx` | `run_regular_excel.m` |
| Mesh Voronoi UGRID | `General_Data_voronoi.xlsx` | `run_voronoi_excel.m` |

Abra o MATLAB na pasta do repositório e rode um dos comandos:

```matlab
run('Examples/VTilted_Excel/run_regular_excel.m')
```

```matlab
run('Examples/VTilted_Excel/run_voronoi_excel.m')
```

O exemplo completo está em
[`Examples/VTilted_Excel`](https://github.com/marcusnobrega-eng/HydroPol2D/tree/integration/performance-modernization-2026-09/Examples/VTilted_Excel).

## Arquivos necessários

Mantenha a planilha principal `General_Data*.xlsx` e as planilhas auxiliares
na mesma pasta:

- `LULC_parameters.xlsx`
- `SOIL_parameters.xlsx`
- a planilha da forçante ativa, como `Rainfall_Intensity_Data.xlsx`
- planilhas de vazão de entrada, nível, reservatório, ET ou qualidade da água
  somente quando suas flags estiverem ativas

Os caminhos dos rasters podem ser absolutos ou relativos. O modelo resolve os
caminhos relativos a partir da pasta da planilha principal.

## Mesh regular

Use `flag_voronoi = 0`. O modelo lê o DEM, o uso do solo e o mapa de solos e
monta a grade estruturada usada pelo solver MATLAB principal.

## Mesh Voronoi

Use `flag_voronoi = 1` e informe um caso MAT preparado no campo
`Voronoi case file`. Esse caso aponta para a mesh UGRID e para o arquivo de
sobreposição raster gerados pelo HydroBathyDEM.

Os parâmetros de mesh da planilha devem coincidir com os metadados gravados no
arquivo UGRID. Antes da simulação, o HydroPol2D compara largura de fundo,
largura mínima, razão entre células adjacentes, largura urbana, buffer de
transição e tratamento dos rios não resolvidos. Essa verificação impede que a
planilha rode silenciosamente com uma mesh diferente da selecionada.

A planilha seleciona uma mesh Voronoi pronta. Ela não gera nem modifica a mesh
durante a simulação. O solver Voronoi MATLAB atual roda apenas em CPU.

## Selecionar outra planilha sem editar o launcher

Defina os caminhos no MATLAB e rode o launcher normal:

```matlab
setenv('HYDROPOL_RUN_MODE','excel')
setenv('HYDROPOL_INPUT_EXCEL_FILE','/caminho/absoluto/General_Data.xlsx')
setenv('HYDROPOL_EXPORT_ROOT_DIR','/caminho/absoluto/Outputs/minha_simulacao')
setenv('HYDROPOL_SKIP_POSTPROCESS','')
run('HydroPol2D_V115.m')
```

Use `HYDROPOL_SKIP_POSTPROCESS = 1` somente para testar o solver sem gerar o
pacote final. Deixe a variável vazia para uma simulação normal.

## Configuração pelo código MATLAB

Para estudos automatizados, ensembles ou configurações revisadas linha a linha
no Git, use o modo `bypass`:

1. Defina `run_mode = 'bypass'` em `HydroPol2D_V115.m`.
2. Ajuste processos e controles numéricos em `Config/input_data_bypass_script.m`.
3. Ajuste os caminhos em `Config/input_paths_bypass.m`.
4. Rode `HydroPol2D_V115.m`.

Use o modo Excel quando a planilha for o registro mais prático do projeto. Use
o modo `bypass` quando a configuração precisar ser gerada ou revisada como
código.
