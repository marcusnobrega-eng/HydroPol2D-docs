---
title: Rodar o caso
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Rodar o caso

Um caso que passou na verificação roda no HydroPol2D MATLAB ou no HydroPol2D Studio, conforme o que
você escolheu em **Prepare for**. Os painéis de simulação aparecem abaixo do resultado da
verificação, tanto depois de **Prepare complete case** quanto em **Check a case**.

| Preparado para | Rode no | A partir de |
|---|---|---|
| **HydroPol2D MATLAB** | HydroPol2D MATLAB (código aberto) | o painel **Run HydroPol2D MATLAB**, ou o próprio MATLAB |
| **HydroPol2D Python** | HydroPol2D Studio | **Open existing model** no Studio, com `hydropol_python/case.yaml` |
| **Python and MATLAB** | qualquer um dos dois | os dois |

## No HydroPol2D MATLAB, pelo app {#matlab-from-the-app}

Você precisa do MATLAB no seu computador. O painel **Run HydroPol2D MATLAB** tem:

- **HydroPol2D MATLAB folder**: uma pasta com o código do HydroPol2D MATLAB. Uma pasta que já o
  contém é usada como está, sem atualização. Se a pasta não existe, o app baixa o HydroPol2D do seu
  [repositório no GitHub](https://github.com/marcusnobrega-eng/HydroPol2D) (ramo `main`) para
  dentro dela. Esse download precisa do [Git](https://git-scm.com).
- **MATLAB executable**: encontrado sozinho quando o MATLAB está instalado no lugar de costume. Caso
  contrário, informe o caminho dele, por exemplo `/Applications/MATLAB_R2025b.app/bin/matlab` no Mac
  ou `C:\Program Files\MATLAB\R2025b\bin\matlab.exe` no Windows.

**Run HydroPol2D MATLAB** inicia o MATLAB em segundo plano. O botão só fica ativo depois que a
verificação passou. **Refresh status** atualiza a página enquanto o modelo roda:

- o estado ("MATLAB is running in the background", "MATLAB simulation completed successfully" ou o
  código de saída quando ele parou);
- uma barra de progresso com a etapa e a parcela do tempo simulado;
- **Simulated time**, **Time step**, **Elapsed** e **Estimated remaining**;
- a chuva média e máxima, a profundidade máxima, a vazão no exutório, o armazenamento total, o erro
  de balanço de massa e a profundidade média do lençol freático;
- o **MATLAB run log**, que abre sozinho quando a simulação falha.

Quando a simulação termina, **Results** mostra a profundidade máxima da água superficial como um
número, um mapa e uma animação, e informa o nome do GeoTIFF de profundidade máxima para um SIG. O
status e os logs ficam em `model_runs/`, dentro do caso, e os resultados em `Outputs/`.

## No HydroPol2D MATLAB, à mão {#matlab-by-hand}

O `run_case.m` do caso define os caminhos, as datas, a resolução, a chuva, as condições de contorno,
as saídas e as opções de execução do caso, e depois inicia o HydroPol2D. No MATLAB:

```matlab
addpath('/path/to/CASE_DIR/hydropol_matlab')
run_case('/path/to/HydroPol2D')
```

O primeiro caminho é a pasta do caso, e o segundo, a sua pasta do HydroPol2D MATLAB. O `run_case.m`
não muda os arquivos de configuração do HydroPol2D: ele passa o caso ao modelo na memória, então a
mesma pasta do HydroPol2D pode rodar muitos casos. Um caso na malha nativa (uma grade quadtree, um
caso Urban Area Only ou tabelas hidráulicas) roda no solver de malha nativo do HydroPol2D e grava um
arquivo nativo de resultados da malha. Veja o [fluxo do MATLAB](../getting-started/excel-workflow)
para o próprio modelo.

## No HydroPol2D Studio {#studio}

1. Abra o HydroPol2D Studio.
2. Na tela **Home**, escolha **Open existing model**.
3. Escolha `hydropol_python/case.yaml` na pasta do caso.

O caso abre no **Setup**, pronto para verificar e rodar. A partir daí, as ferramentas do Studio
funcionam nele, por exemplo drenagem urbana, estruturas de detenção, infraestrutura verde,
travessias, resultados e calibração. Veja o [guia do Studio](../studio/overview).

O painel **Run HydroPol2D Python** do app pede uma pasta que contenha o HydroPol2D Python. O app não
baixa o HydroPol2D Python, que vem com o Studio. Sem essa pasta, o painel avisa e indica o Studio.

## Onde ficam os resultados {#results}

| Simulação | Resultados |
|---|---|
| MATLAB, grade regular | `Outputs/`, com as prévias dos resultados em `Outputs/PostProcessing/` |
| MATLAB, malha nativa | `Outputs/Modeling_Results/Native/unstructured_results.nc` e as prévias |
| Python | `Outputs/python/Modeling_Results/`: figuras, GeoTIFFs estáticos e animações |

Os mapas salvos e o seu intervalo seguem **Saved outputs** ([Configurações do caso](settings#saved-outputs)).
