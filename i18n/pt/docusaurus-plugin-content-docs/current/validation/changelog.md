---
title: Registro de Alterações
---

# Registro de Alterações

Mudanças no modelo que afetam entradas, resultados ou validação, das mais recentes para as mais antigas. As datas estão no horário da Califórnia (PDT). Os códigos entre colchetes são commits no HydroPol2D-Python (Py), no modelo MATLAB (ML) e no Case Builder (CB).

## 2026-10-20 {#2026-10-20}

- **Uma única planilha do caso (ML).** Um caso MATLAB agora é uma única planilha, `HydroPol2D_Inputs.xlsx`, com 8 abas de configurações, 5 abas de tabelas de classes, 5 abas de séries e uma nota em cada valor. As chaves ficam no topo dos seus blocos, e não existe aba `Flags`. Os casos antigos (`General_Data.xlsx`, a sua aba `Flags` e planilhas separadas) continuam rodando, e um gerador os converte. Verificação: o caso V-tilted dá resultados idênticos nos dois formatos, com todas as planilhas antigas apagadas, e dobrar a aba Rain series dobra a chuva (3 de 3 verificações). Veja [Rodar pelo Excel](../getting-started/excel-workflow). [ML `a0a6b7a`, `993d830`]
- **Correção: listas de mapas de ET (ML, nos dois formatos).** Em `General_Data.xlsx`, as listas de mapas de chuva, transpiração e evaporação compartilham uma única linha de cabeçalho. Antes desta correção, a lista de transpiração lia os tempos da lista de chuva (em minutos, sem conversão de dias para minutos), e a lista de evaporação lia os caminhos da transpiração. As simulações com `flag_input_ETP_map = 1` feitas antes de 2026-10-20 usaram entradas de ET erradas e devem ser rodadas de novo. Cada lista agora termina na sua primeira linha vazia, e as suas colunas são procuradas apenas sob o seu próprio título. [ML `993d830`]
- **Seções transversais de vazão nos postos (ML).** Cada posto registra a profundidade e o nível da água na sua célula e a vazão ao longo de uma linha de células que atravessa o escoamento (5 células por padrão, com direção de jusante automática ou N/S/E/W). Novas saídas: uma linha no hidrograma, uma coluna em `Rating_Curve_Gauges.csv` e `Gauge_Cross_Sections.csv`. A tabela de postos agora termina na sua primeira linha vazia. Verificações: 3 de 3. Veja [Tabela de postos](../configuration/general_data#gauge-table-and-discharge-cross-sections). [ML `fa36e1f`]
- **Fluxo implícito no lençol freático no MATLAB (ML).** Chave `flag_implicit_water_table_flux`, padrão 1. O MATLAB calcula as derivadas por diferenças centrais de quarta ordem e concorda com o Python até cerca de $10^{-9}$. Uma faixa acima do lençol já saturada agora drena a $K_{sat}$ por uma regra explícita nos dois modelos (resultados inalterados). [ML `2559060`; Py `04ca62a`]
- **`DTB_path` opcional no modo em camadas (ML).** O fundo da coluna recorre a `subsurface_depth_to_bedrock_m` e, depois, ao `DTB (m)` de cada classe de solo. Antes, a falta de `DTB_path` significava 1 m, sem aviso. O esquema padrão de águas subterrâneas continua exigindo `DTB_path`. [ML `2559060`]
- **Mapas de propriedades do solo no modo Excel (ML).** Nove mapas opcionais (`ThetaS_path` … `SpecificYield_path`) substituem célula a célula os valores das classes de solo. [ML `2559060`]
- **Correção na validação (ML).** A rotina de verificação das águas subterrâneas gravava a sua grade `Flags` deslocada em uma célula, e por isso a simulação V-tilted com Feddes rodava com o Feddes desligado. Agora ela roda com o Feddes ligado, e três simulações foram acrescentadas (sem `DTB_path`, fluxo explícito, mapas de solo). Verificações de release das águas subterrâneas: 17 de 17. [ML `2559060`]

## 2026-10-19 {#2026-10-19}

- **Regra de reposição capilar (Py, ML).** A ascensão capilar repõe a água de uma camada de solo apenas até a capacidade de campo (como no HBV). Isso eliminou uma circulação de água entre o solo e um lençol freático raso. No vale gêmeo, a ascensão capilar bruta caiu de 0.016 para 0 m³/s, com a vazão do rio inalterada. O fluxo implícito no lençol freático agora toma a derivada em relação à carga ao longo do movimento real do lençol. Veja [Subsuperfície em Camadas, Seção 4.4](../theory/layered-subsurface#44-darcy-flux-at-the-water-table). [Py `fe81252`; ML `051b52b`]
- **Calibração por recessão em camadas (Py, CB).** Dois multiplicadores da condutividade lateral, do solo e do regolito, ajustados a uma curva mestra de recessão, com saídas de identificabilidade e um spin-up que roda os próprios fluxos da coluna do modelo. Veja [Calibração por Recessão das Águas Subterrâneas](../calibration/groundwater-recession). [Py `b1f686e`, `1ffddd8`, `3390dc6`, `e837f7d`; ML `f78a130`; CB `d45e5be`]
- **Fluxo implícito no lençol freático (Py)** e **passo em camadas compilado** (cerca de 6 vezes mais rápido, com resultados idênticos). [Py `c384ea4`, `0a4b393`]
- **Estado inicial do aquífero profundo (Py, ML, CB).** $S_0 = q_0 A \tau$ a partir de um escoamento de base inicial ou de uma recarga média. Veja [Modelo de Águas Subterrâneas, Seção 13.3](../theory/groundwater-model#133-starting-state). [Py `57ea20a`, `83d7071`; ML `13fa3d8`; CB `52bdbad`]

## 2026-10-15 a 2026-10-17 {#2026-10-15-to-2026-10-17}

- **Subsuperfície em camadas e estresse de Feddes (Py, ML).** A coluna de solo sobre regolito na grade estruturada e na malha Voronoi, o estresse hídrico radicular de Feddes nos dois esquemas de solo e a versão em MATLAB, com paridade entre Python e MATLAB. Veja [Subsuperfície em Camadas](../theory/layered-subsurface). [Py `b6ced47` … `c268969`; ML `0ded343`, `282cac9`, `383ea82`]
- **Entradas em camadas (CB, ML).** Regras globais para os mapas da base do solo e do regolito, casos MATLAB em camadas e as entradas no Excel para os novos blocos. [CB `06f5e75`, `1ec94f4`; ML `2074ae6`]
