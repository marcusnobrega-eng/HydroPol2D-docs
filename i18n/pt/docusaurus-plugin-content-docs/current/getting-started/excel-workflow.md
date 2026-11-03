---
title: Rodar pelo Excel
---

# Rodar o HydroPol2D pelo Excel

No modo Excel, um caso MATLAB inteiro fica em uma única planilha, `HydroPol2D_Inputs.xlsx`, com todas as configurações, as tabelas de classes e as séries temporais. O modo bypass lê as mesmas configurações de arquivos MATLAB na pasta `Config/`. Os dois modos usam o mesmo solver numérico.

## Comece pelo exemplo testado {#start-with-the-tested-example}

O repositório inclui um caso V-tilted pequeno. A sua planilha é `Examples/VTilted_Excel/Input_Data_Sheets/HydroPol2D_Inputs.xlsx`. Abra o MATLAB no repositório do HydroPol2D e rode o comando abaixo.

```matlab
run('Examples/VTilted_Excel/run_excel.m')
```

O launcher lê `flag_voronoi` (aba Surface flow) e grava os resultados em `Examples/VTilted_Excel/Outputs/regular` ou `Examples/VTilted_Excel/Outputs/voronoi`. Para rodar a malha Voronoi preparada, mude `flag_voronoi` de `0` para `1` na mesma planilha. Não crie uma segunda planilha.

## A planilha do caso {#the-case-workbook}

| Abas | Conteúdo |
|---|---|
| Start here | Como preencher a planilha, a legenda de cores e um link para cada aba |
| Run control, Input maps, Soil and groundwater, Surface flow, Rain and ET, Design storm, Water quality, Risk and gauges | Todas as configurações, uma por linha, com uma nota em cada valor. Um bloco fica em cinza enquanto a sua chave vale 0. |
| Soil classes, Land use classes, Human instability, Mesh, Control structures | As tabelas de classes |
| Rain series, Rain gauges, Climate stations, Inflow hydrographs, Stage hydrographs | As séries temporais |

As abas de tabelas de classes e de séries mantêm o arranjo de células das planilhas que substituem, porque o modelo lê algumas delas por posição. Mantenha as linhas e as colunas onde estão. Uma aba comporta até 1 048 576 linhas, o que equivale a dois anos de dados a cada 1 min.

As configurações estão listadas em [Configurações da Planilha do Caso](../configuration/general_data), as chaves em [Flags do Modelo](../configuration/flags), as tabelas de classes em [Tabelas de parâmetros](../inputs/parameter-tables) e as séries em [Forçantes Opcionais](../inputs/optional-forcing).

## Preencha um caso {#fill-a-case}

1. **Start here.** Leia a legenda de cores. Uma linha cinza está desligada, um bloco cinza é avançado (mantenha os padrões) e um bloco âmbar está pausado (mantenha-o em 0).
2. **Abas de configurações.** Ligue ou desligue os processos com a chave no topo de cada bloco. Um asterisco vermelho marca um valor obrigatório. Um valor opcional vazio mantém o padrão, e a nota de cada valor indica qual é.
3. **Tabelas de classes.** Informe uma linha por código de classe dos mapas de uso da terra e de solo. Um código válido que falte em uma tabela recebe a média ponderada pela área das classes mapeadas, e a decisão é registrada em `Input_Class_Code_Audit.csv`.
4. **Séries.** Preencha apenas as séries que as suas chaves leem. As demais podem ficar como modelos vazios, com os seus cabeçalhos.
5. **Caminhos.** Os caminhos de rasters e de arquivos podem ser absolutos ou relativos à pasta da planilha.

## Grade regular ou malha Voronoi {#regular-grid-or-voronoi-mesh}

`flag_voronoi` (aba Surface flow, bloco Unstructured mesh) seleciona a malha.

| `flag_voronoi` | Malha |
|---|---|
| `0` | Grade raster construída a partir do DEM e dos mapas de uso da terra e de solo |
| `1` | Um arquivo de caso preparado, indicado na aba Mesh, que referencia a malha UGRID e os arquivos de sobreposição raster gerados pelo HydroBathyDEM |

As configurações da aba Mesh devem coincidir com os metadados gravados no arquivo UGRID. Antes da simulação, o HydroPol2D verifica a largura de fundo, a largura mínima, a razão entre tamanhos adjacentes, a largura urbana, o buffer de transição e a regra para rios não resolvidos, de modo que uma planilha não rode silenciosamente com outra malha. O Excel seleciona uma malha preparada, mas não a gera nem a modifica durante a simulação. O executor Voronoi do MATLAB roda apenas em CPU.

## Rode qualquer planilha sem editar o launcher {#run-any-workbook-without-editing-the-launcher}

`run_HydroPol2D.m` lê `Input_Data_Sheets/HydroPol2D_Inputs.xlsx` por padrão. Para rodar outro caso, defina os caminhos no MATLAB e rode o launcher normal.

```matlab
setenv('HYDROPOL_RUN_MODE','excel')
setenv('HYDROPOL_INPUT_EXCEL_FILE','/absolute/path/to/HydroPol2D_Inputs.xlsx')
setenv('HYDROPOL_EXPORT_ROOT_DIR','/absolute/path/to/Outputs/my_run')
setenv('HYDROPOL_SKIP_POSTPROCESS','')
run('run_HydroPol2D.m')
```

Antes da versão 1.19.0-rc2, o script principal se chamava `HydroPol2D_V115.m`. Esse nome ainda funciona.

Defina `HYDROPOL_SKIP_POSTPROCESS` como `1` para uma simulação de diagnóstico apenas do solver. Deixe a variável vazia para a simulação completa normal.

## Converta um caso antigo {#convert-an-older-case}

Na pasta `tools/workbook_builder` do repositório MATLAB, rode o comando abaixo.

```bash
python build_input_workbook.py input_catalog.yaml General_Data.xlsx HydroPol2D_Inputs.xlsx
```

O gerador transfere todos os valores, caminhos de mapas, listas de mapas e postos, e copia as tabelas de classes e as séries das planilhas que estão ao lado da origem. O caso V-tilted dá resultados idênticos com a planilha convertida e com os arquivos antigos (`Validation/Workbook/run_single_workbook_checks.m`).

## Formato antigo {#older-layout}

Os casos criados antes de 2026-10-20 usam `General_Data.xlsx`, com a sua aba `Flags`, e planilhas separadas (`SOIL_parameters.xlsx`, `LULC_parameters.xlsx`, `Rainfall_Intensity_Data.xlsx` e as demais). Eles continuam rodando sem mudanças.

- `run_HydroPol2D.m` usa `General_Data.xlsx` quando a pasta de entrada não tem `HydroPol2D_Inputs.xlsx`, ou o arquivo indicado por `HYDROPOL_INPUT_EXCEL_FILE`.
- Cada leitor busca a sua aba na planilha do caso, quando o caso tem uma, e na planilha antiga, caso contrário.
- Mantenha as planilhas auxiliares na mesma pasta de `General_Data.xlsx`. Os caminhos relativos são resolvidos a partir dessa pasta.

## Configure com arquivos MATLAB, em vez da planilha {#configure-with-matlab-files-instead}

Para estudos automatizados, ensembles ou configurações acompanhadas linha a linha no Git, use o modo bypass.

1. Defina `run_mode = 'bypass'` em `run_HydroPol2D.m`.
2. Ajuste os controles de processos e os controles numéricos em `Config/input_data_bypass_script.m`.
3. Ajuste os caminhos de rasters e de forçantes em `Config/input_paths_bypass.m`.
4. Rode `run_HydroPol2D.m`.

O exemplo V-tilted tem a sua própria configuração em código. Rode `addpath('Examples/VTilted_Excel')` e, em seguida, `run_code('regular')` ou `run_code('voronoi')`.

Use o modo Excel quando a planilha for o registro mais prático do projeto. Use o modo bypass quando a configuração precisar ser gerada ou revisada como código.
