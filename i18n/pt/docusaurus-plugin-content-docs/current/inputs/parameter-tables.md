---
title: Tabelas de parâmetros
---

# Tabelas de parâmetros

HydroPol2D usa tabelas de parâmetros para atribuir propriedades físicas a entradas raster categóricas.
Mapas categóricos como LULC e Solo não são usados ​​diretamente nas equações governantes. Em vez disso, cada classe atua como um índice em uma tabela de parâmetros, onde os parâmetros físicos correspondentes são definidos.
Essa estrutura separa as informações espaciais da definição dos parâmetros e torna o modelo mais fácil de calibrar, adaptar e interpretar.

---

## Onde Ficam as Tabelas {#where-the-tables-live}

No modo Excel do MATLAB, as tabelas de classes são abas da planilha do caso, `HydroPol2D_Inputs.xlsx`. Cada aba é uma cópia, célula a célula, da planilha que substitui, porque o modelo lê algumas colunas por posição. Mantenha as linhas e a ordem das colunas, e acrescente uma classe como uma nova linha.

| Aba | Antes | Lida quando |
|---|---|---|
| Soil classes | `SOIL_parameters.xlsx` | sempre |
| Land use classes | `LULC_parameters.xlsx` | sempre (lida a partir da linha 2, por posição) |
| Human instability | `human_risk.xlsx` | `flag_human_instability = 1` ou `3` |
| Mesh | `Voronoi_Settings.xlsx` | `flag_voronoi = 1` |
| Control structures | `BC_Control_structure.xlsx` | `flag_reservoir = 1` |

No formato antigo, as mesmas tabelas são as planilhas separadas da segunda coluna, na pasta de `General_Data.xlsx`. O modelo lê a aba quando a planilha do caso a tem e, caso contrário, a planilha antiga. O HydroPol2D-Python lê as mesmas propriedades das classes a partir do contrato do Case Builder.

---

## Estrutura Geral

Cada tabela de parâmetros contém:
- um **identificador de classe** (`Index`)
- um conjunto de **parâmetros associados a essa classe**

Em tempo de execução, HydroPol2D:
1. lê o valor raster em cada célula da grade,
2. usa esse valor como um índice,
3. atribui os parâmetros correspondentes da tabela.

Para classes mapeadas, os valores raster e os índices de tabela devem corresponder. Quando um código válido de LULC, solo ou neve não aparece na tabela, o HydroPol2D aplica a média ponderada pela área das propriedades das classes mapeadas e registra a decisão em `Input_Class_Code_Audit.csv`. Índices duplicados, não numéricos ou uma tabela sem classes mapeadas continuam sendo erros de entrada.

---

## Tabela de parâmetros LULC

A tabela LULC define propriedades relacionadas à superfície que controlam a resistência ao fluxo, interceptação, impermeabilidade, comportamento relacionado a poluentes e profundidade da zona radicular quando o armazenamento em camadas do solo está ativo.
### Estrutura de exemplo

| Cobertura do solo | Índice | $n$<br />$(\mathrm{s\,m^{-1/3}})$ | $h_0$<br />$(\mathrm{mm})$ | $d_0$<br />$(\mathrm{mm})$ | $C_1$ | $C_2$ | $C_3$ | $C_4$ | $\mathrm{index\_impervious}$ | $\mathrm{root\_depth\_m}$ | $K_c$ |
|:----------:|:-----:|:---------------------------------:|:--------------------------:|:--------------------------:|:-----:|:-----:|:-----:|:-----:|:----------------------------:|:--------------------------:|:----:|
| Cobertura de árvore | 10 | 0,10 | 0 | 0 | 10 | 0,20 | 800 | 1,20 | 50 | 1,50 | 1,05 |
| Arbustos | 20 | 0,08 | 0 | 0 | 12 | 0,20 | 900 | 1,20 | NaN | 1,00 | 0,70 |
| Pastagem | 30 | 0,06 | 0 | 0 | 15 | 0,22 | 1000 | 1,20 | NaN | 0,60 | 0,85 |
| Terras agrícolas | 40 | 0,05 | 0 | 0 | 30 | 0,25 | 1400 | 1,30 | NaN | 1,00 | 1,00 |
| Construído | 50 | 0,03 | 0 | 0 | 80 | 0,30 | 2000 | 1,30 | NaN | 0,00 | 0 |
| Vegetação nua / esparsa | 60 | 0,035 | 0 | 0 | 45 | 0,25 | 1600 | 1,25 | NaN | 0,10 | 0,30 |
| Neve e gelo | 70 | 0,02 | 0 | 0 | 1 | 0,10 | 200 | 1.10 | NaN | 0,00 | 0 |
| Corpos de água permanentes | 80 | 0,035 | 0 | 0 | 0 | 0 | 0 | 0 | NaN | 0,00 | 0 |
| Zona húmida herbácea | 90 | 0,12 | 0 | 0 | 8 | 0,18 | 700 | 1,20 | NaN | 0,40 | 1,00 |
| Manguezais | 95 | 0,15 | 0 | 0 | 8 | 0,18 | 700 | 1,20 | NaN | 1,00 | 1,05 |
| Musgo e líquen | 100 | 0,08 | 0 | 0 | 5 | 0,15 | 500 | 1,15 | NaN | 0,15 | 0,40 |

*Tabela 1. Tabela de parâmetros HydroPol2D LULC. Os valores `Index` devem corresponder aos valores categóricos no raster LULC.*
### Definições de variáveis

- $n$: coeficiente de rugosidade de Manning
- $h_0$: parâmetro de interceptação
- $d_0$: parâmetro inicial de armazenamento de superfície
- $C_1$–$C_4$: coeficientes associados ao acúmulo de poluentes e formulação de lavagem
- $\mathrm{index\_impervious}$: o `Index` da classe tratada como totalmente impermeável, informado uma única vez (a planilha-modelo usa a primeira linha de dados, 50 = área construída), com a coluna vazia em todas as outras linhas. Essa classe não tem armazenamento de infiltração no solo
- $\mathrm{root\_depth\_m}$: profundidade da zona radicular controlada pela vegetação usada pelo modelo de solo/vadoso em camadas
- $K_c$: coeficiente de cultura e de cobertura do solo. Ele converte a ET de referência calculada internamente na ET potencial do solo das células permeáveis sem lâmina d'água. Não se aplica a mapas de ET prescritos, e a água empoçada evapora à parte. Use 0 para classes impermeáveis, de água permanente e de neve ou gelo

Os valores mostrados acima correspondem à tabela de parâmetros HydroPol2D atual e devem ser revisados ​​conforme necessário para o esquema de classificação adotado e área de estudo.
Na implementação atual, `root_depth_m` é a forma suportada de fornecer entrada de profundidade raiz para o modelo. Não existe um caminho raster de profundidade de raiz separado; a profundidade da raiz é atribuída por classe LULC e então mapeada para a grade por meio do raster categórico LULC.

---

## Tabela de parâmetros do solo

A tabela de solos define as propriedades hidráulicas básicas usadas para estimar a infiltração, o armazenamento vadoso em camadas, a recarga e o comportamento das águas subterrâneas.
### Estrutura de exemplo

| Tipo de solo | Índice | $K_{\mathrm{sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $n$ | $\alpha$<br />$(\mathrm{m^{-1}})$ | $\theta_{\mathrm{sat}}$ | $\theta_{\mathrm{r}}$ | $\theta_{\mathrm{i}}$ | $S_{\mathrm{y}}$ | $K_{\mathrm{g,sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $\mathrm{DTB}$<br />$(\mathrm{m})$ | $K_s$ perto | $K_s$ raiz | transmissão $K_s$ |
|:---------:|:-----:|:-----------------------------------------------:|:---:|:----------------------------------:|:----------------------:|:--------------------:|:--------------------:|:---------------:|:---------------------------------------------------:|:--------------------------------:|:------------:|:----------:|:--------------------:|
| Argila | 1 | 0,3 | 1,09 | 0,8 | 0,385 | 0,068 | 0,0997 | 0,03 | 6 | 1 | 1 | 1 | 1 |
| Argila siltosa | 2 | 0,5 | 1,09 | 0,5 | 0,423 | 0,070 | 0,1053 | 0,04 | 10 | 1 | 1 | 1 | 1 |
| Argila arenosa | 3 | 0,6 | 1,23 | 2,7 | 0,321 | 0,100 | 0,1221 | 0,06 | 12 | 1 | 1 | 1 | 1 |
| Franco-argilosa | 4 | 1,0 | 1,31 | 1,9 | 0,309 | 0,095 | 0,1164 | 0,08 | 20 | 1 | 1 | 1 | 1 |
| Franco-argilossiltosa | 5 | 1,0 | 1,23 | 1,0 | 0,432 | 0,089 | 0,1233 | 0,09 | 20 | 1 | 1 | 1 | 1 |
| Franco-argiloarenosa | 6 | 1,5 | 1,48 | 5,9 | 0,330 | 0,100 | 0,1230 | 0,11 | 30 | 1 | 1 | 1 | 1 |
| Franca | 7 | 3,4 | 1,56 | 3,6 | 0,434 | 0,078 | 0,1136 | 0,18 | 68 | 1 | 1 | 1 | 1 |
| Franco-siltosa | 8 | 6,5 | 1,41 | 2,0 | 0,486 | 0,067 | 0,1298 | 0,14 | 130 | 1 | 1 | 1 | 1 |
| Franco-arenosa | 9 | 10,9 | 1,89 | 7,5 | 0,412 | 0,065 | 0,0997 | 0,22 | 218 | 1 | 1 | 1 | 1 |
| Silte | 10 | 2,5 | 1,37 | 1,6 | 0,460 | 0,034 | 0,1192 | 0,12 | 50 | 1 | 1 | 1 | 1 |
| Areia franca | 11 | 29,9 | 2,28 | 12,4 | 0,401 | 0,057 | 0,1258 | 0,25 | 598 | 1 | 1 | 1 | 1 |
| Areia | 12 | 117,8 | 2,68 | 14,5 | 0,417 | 0,045 | 0,1194 | 0,30 | 2356 | 1 | 1 | 1 | 1 |
| Água | 0 | 0,3 | 1,09 | 0,8 | 0,385 | 0,068 | 0,0997 | 0,03 | 6 | 1 | 1 | 1 | 1 |

*Tabela 2. Tabela de parâmetros do solo do HydroPol2D. Os valores de `Index` devem corresponder aos valores categóricos do raster de solo; os códigos padrão seguem a legenda de textura USDA do OpenLandMap (7 franca, 8 franco-siltosa). $K_{\mathrm{sat}}$ e $\theta_{\mathrm{sat}}$ são a condutividade de Green–Ampt e a porosidade efetiva de [Rawls et al. (1983)](https://doi.org/10.1061/%28ASCE%290733-9429%281983%29109%3A1%2862%29); $n$, $\alpha$ e $\theta_{\mathrm{r}}$ são as médias por classe de [Carsel e Parrish (1988)](https://doi.org/10.1029/WR024i005p00755). O silte, que Rawls et al. não listam, usa $K_{\mathrm{sat}}$ e $\theta_{\mathrm{sat}}$ de Carsel e Parrish. $\theta_{\mathrm{i}} = \theta_{\mathrm{r}} + S_e(\theta_{\mathrm{sat}} - \theta_{\mathrm{r}})$, com $S_e = 0{,}1$ (0,15 para franco-siltosa; 0,2 para silte, areia franca e areia), e $K_{\mathrm{g,sat}} = 20\,K_{\mathrm{sat}}$.*
### Definições de variáveis

- $K_{\mathrm{sat}}$: condutividade hidráulica saturada
- $n$: parâmetro de forma de Van Genuchten
- $\alpha$: parâmetro de entrada de ar inverso
- $\theta_{\mathrm{sat}}$: teor de água saturada
- $\theta_{\mathrm{r}}$: teor de água residual
- $\theta_{\mathrm{i}}$: umidade inicial do solo
- $S_{\mathrm{y}}$: rendimento específico
- $K_{\mathrm{g,sat}}$: condutividade saturada associada à parametrização de águas subterrâneas ou subterrâneas
- $\mathrm{DTB}$: profundidade até o leito rochoso ou profundidade efetiva de armazenamento
- `Ks_multiplier_near_surface`: multiplicador aplicado à base $K_{\mathrm{sat}}$ na camada próxima à superfície
- `Ks_multiplier_root_zone`: multiplicador aplicado à base $K_{\mathrm{sat}}$ na camada da zona raiz
- `Ks_multiplier_transmission`: multiplicador aplicado à base $K_{\mathrm{sat}}$ na camada de transmissão
- `Ltop_m`: espessura $L_{\mathrm{top}}$ da camada de solo próxima à superfície (m). É também a escala de comprimento da capacidade de infiltração do [Modelo Hidrológico, Seção 4.5](../theory/hydrologic-model#45-darcy-based-infiltration-capacity). A planilha-modelo usa 0,05 m em todas as classes
- `dh_max_m`: limite $\Delta h_{\max}$ da diferença de carga que move essa capacidade de infiltração (m). Padrão de 1 m
- `l_vg`: parâmetro de conectividade dos poros $l$ de Mualem na condutividade não saturada de van Genuchten–Mualem (adimensional; 0,5 é o valor usual)

A aba Soil classes tem 17 colunas nesta ordem: nome, `Index`, $K_{\mathrm{sat}}$, $n$, $\alpha$, $\theta_{\mathrm{sat}}$, $\theta_{\mathrm{r}}$, $\theta_{\mathrm{i}}$, $S_{\mathrm{y}}$, $K_{\mathrm{g,sat}}$, DTB, os três multiplicadores, `Ltop_m`, `dh_max_m` e `l_vg`. O modelo as lê pela posição.

A classe categórica do solo define as propriedades hidráulicas básicas do pilar. A implementação em camadas atribui essas propriedades às camadas próximas à superfície, zona raiz e zona de transmissão e, em seguida, aplica multiplicadores de condutividade opcionais onde eles são fornecidos.
LULC controla a profundidade da zona raiz. A profundidade do leito rochoso e a posição atual do lençol freático restringem as espessuras finais da camada, de modo que geometrias de camada fisicamente impossíveis colapsam ou truncam, em vez de produzir armazenamento negativo.
Os valores mostrados acima correspondem à tabela atual de parâmetros de solo HydroPol2D e devem ser revisados ​​conforme necessário para o cenário de classificação e simulação de solo adotado.

---

## Atribuição DTB através da tabela de solos {#dtb-assignment-through-the-soil-table}

A coluna `DTB (m)` dá uma profundidade até o leito rochoso por classe de solo. O uso dessa coluna depende do esquema de subsuperfície.

| Esquema | Papel de `DTB (m)` |
|---|---|
| [Subsuperfície em camadas](../theory/layered-subsurface) | Fundo da coluna onde `DTB_path` e `subsurface_depth_to_bedrock_m` estão ambos vazios (no MATLAB desde 2026-10-20; o HydroPol2D-Python lê a sua tabela de solos da mesma forma) |
| Esquema padrão de águas subterrâneas (MATLAB) | Não é lida. `DTB_path` é obrigatório. Sem águas subterrâneas, um `DTB_path` vazio dá uma profundidade do solo de 1 m |

Cada classe de solo passa então a ter uma profundidade representativa, e o fundo da coluna acompanha o mapa de solos. Isso é útil em aplicações com escassez de dados.


---

## Requisitos de consistência

As seguintes condições devem ser satisfeitas:
- todos os valores da classe raster devem existir na tabela correspondente,
- identificadores de classe não devem ser duplicados,
- os campos de parâmetro não devem ser deixados vazios,
- as unidades devem ser consistentes com a formulação do modelo.

Qualquer inconsistência entre classes raster e tabelas de parâmetros levará à atribuição incorreta de propriedades físicas.

---

## Uso prático

As tabelas de parâmetros são o principal mecanismo usado para:
- calibrar o modelo,
- adaptar o modelo a diferentes ambientes,
- realizar análise de sensibilidade,
- testar suposições físicas alternativas sem modificar o código.

No HydroPol2D, as modificações mais práticas no comportamento do modelo são feitas editando essas tabelas.

---

## Tabela de instabilidade humana {#human-instability-table}

A aba Human instability (antes `human_risk.xlsx`) tem uma coluna de valores por método. O modelo lê os valores pela posição, então mantenha cada célula no lugar. Veja [Instabilidade Humana](../theory/human-instability) para as equações.

| Coluna | Lida quando | Valores |
|---|---|---|
| Method No. 1 (coluna B) | `flag_human_instability = 1` | uma pessoa representativa, 9 valores |
| Method No. 2 (coluna E) | nunca | o modo 2 não está implementado |
| Method No. 3 (coluna J) | `flag_human_instability = 3` | água, atrito e arrasto, depois 8 tipos de corpo |

**Method No. 1.**

| Chave | Unidade | Padrão | Significado |
|---|---|---|---|
| `ro_water` | kg/m³ | 1000 | Massa específica da água $\rho_{\mathrm{w}}$ |
| `gravity` | m/s² | 9,81 | Gravidade $g$ |
| `mu` | – | 0,5 | Coeficiente de atrito com o chão $\mu$ |
| `Cd` | – | 1,1 | Coeficiente de arrasto $C_d$ |
| `ro_person` | kg/m³ | 1000 | Massa específica do corpo |
| `weight_person` | kg | 75 | Massa do corpo |
| `height_person` | m | 1,75 | Altura do corpo |
| `width1_person` | m | 0,3 | Largura do corpo de frente para o escoamento ($w_1$ na força de arrasto) |
| `width2_person` | m | 0,3 | Espessura do corpo no sentido do escoamento; com $w_1$ define o volume submerso |

**Method No. 3.** `ro_water` (1000 kg/m³), `gravity` (9,81 m/s²), `mu` (0,46) e `Cd` (1), depois uma massa `m_` e uma altura `y_` para cada tipo de corpo:

| Tipo de corpo | Chave da massa | Padrão (kg) | Chave da altura | Padrão (m) |
|---|---|---|---|---|
| Criança, masculino | `m_c_m` | 22,915 | `y_c_m` | 1,160 |
| Adolescente, masculino | `m_t_m` | 56,645 | `y_t_m` | 1,587 |
| Homem adulto | `m_a_m` | 84,587 | `y_a_m` | 1,720 |
| Homem idoso | `m_o_m` | 76,892 | `y_o_m` | 1,667 |
| Criança, feminino | `m_c_f` | 22,719 | `y_c_f` | 1,155 |
| Adolescente, feminino | `m_t_f` | 59,271 | `y_t_f` | 1,571 |
| Mulher adulta | `m_a_f` | 76,858 | `y_a_f` | 1,602 |
| Mulher idosa | `m_o_f` | 70,284 | `y_o_f` | 1,547 |

O modelo calcula a largura de cada corpo, $w = \sqrt{16\,m / (3\pi \rho_{\mathrm{w}}\, y)}$, e a espessura, $w/2$, a partir da massa e da altura.

---

## Tabela da malha {#mesh-table}

A aba Mesh (antes `Voronoi_Settings.xlsx`) só é lida com `flag_voronoi = 1`. Os valores de compatibilidade precisam coincidir com os metadados da malha preparada: a verificação prévia interrompe uma simulação cuja planilha aponta para outra malha. A aba escolhe uma malha preparada; ela nunca gera nem altera uma malha.

| Seção | Parâmetro | Padrão | Unidade | Usado quando | Descrição |
|---|---|---|---|---|---|
| Prepared case | Voronoi case file | – | .mat | `flag_voronoi = 1` | Caso preparado com a malha UGRID, os dados de sobreposição, o forçamento e o estado inicial |
| Mesh compatibility | Background width | 2000 | m | verificação prévia | Largura-alvo das células de fundo gravada nos metadados; não redimensiona a malha |
| Mesh compatibility | Minimum cell width | 100 | m | verificação prévia | Menor largura hidráulica permitida |
| Mesh compatibility | Adjacent size ratio | 2 | – | verificação prévia | Maior razão de tamanho-alvo entre células vizinhas |
| Mesh compatibility | Urban target width | 200 | m | verificação prévia | Largura-alvo das células nas regiões urbanas refinadas |
| Mesh compatibility | Urban buffer | 1000 | m | verificação prévia | Distância de transição em torno das regiões urbanas refinadas |
| Mesh compatibility | Unresolved rivers | `neal_subgrid` | `none` ou `neal_subgrid` | verificação prévia | Tratamento de rio gravado na malha: nenhum, ou o subgrade de Neal para canais mais estreitos que uma célula |
| Optional subgrid | Voronoi subgrid table | – | caminho | `flag_voronoi_subgrid = 1` | Tabela de propriedades de células e faces (no estilo do HEC-RAS); vazia para células prismáticas planas |
| Output | Write native archive | 1 | 0 ou 1 | saída da malha | Mantém o resultado NetCDF nativo não estruturado |
| Output | Native output interval s | 300 | s | saída da malha | Intervalo entre quadros do arquivo NetCDF |
| Output | Write final GeoTIFFs | 1 | 0 ou 1 | saída da malha | Mapas finais pela sobreposição conservativa malha-raster |
| Output | Write temporal GeoTIFFs | 1 | 0 ou 1 | saída da malha | Mapas a cada intervalo da pilha raster |
| Output | Raster stack interval s | 3600 | s | saída da malha | Intervalo de exportação raster, múltiplo inteiro do intervalo nativo |
| Output | Write figures | 1 | 0 ou 1 | saída da malha | Figuras dos resultados |
| Output | Write videos | 1 | 0 ou 1 | saída da malha | Animações dos resultados (exige suporte a vídeo) |
| Output | Write gauge hydrographs | 1 | 0 ou 1 | saída da malha | Hidrogramas dos postos e da saída |

A linha "River cells across" (Legacy) não é lida: a geometria UGRID carregada define a resolução do rio.

---

## Condições de limite interno (estruturas de controle)

HydroPol2D permite a definição de condições de contorno interno (IBCs) que modificam localmente a resposta hidráulica do domínio.
Estas estruturas são implementadas através de uma abordagem simples de curva nominal que converte a profundidade da água em descarga. Nas células de controle selecionadas, o fluxo não é mais determinado apenas pela atualização inercial local padrão. Em vez disso, a descarga é imposta através de uma relação profundidade-descarga definida por parâmetros especificados pelo usuário.
Isso permite que o modelo represente controles hidráulicos localizados, como:
- bueiros
- portões
- açudes
- pontos de venda
- seções de controle projetadas

---

### Conceito

Cada condição de contorno interno está ligada a uma célula de controle definida por suas coordenadas espaciais. A vazão através desse controle é calculada a partir da profundidade local da água usando uma formulação de curva nominal.
Na implementação atual do HydroPol2D, a planilha da estrutura de controle define duas ramificações da curva de classificação, cada uma com seus próprios parâmetros de coeficiente e limite. Isto torna possível representar o comportamento hidráulico por partes sob diferentes profundidades de fluxo ou condições operacionais.
A descarga resultante é imposta no local de controle correspondente e, portanto, modifica a dinâmica do fluxo local dentro do solucionador numérico.

---

### Função no modelo

As condições de contorno internas afetam a simulação por:
- impondo uma resposta de descarga com base na profundidade local
- modificando os fluxos de células de entrada ou saída dentro do solucionador inercial local
- introduzindo troca de fluxo interno controlado dentro do domínio computacional

Estas estruturas podem influenciar fortemente:
- armazenamento a montante
- propagação a jusante
- atenuação de inundações
- efeitos de remanso local

---

### Papel no modelo numérico

Nas células onde uma condição de limite interna é definida:
- a profundidade da água é avaliada no ponto de controle
- a descarga é calculada a partir dos parâmetros da curva nominal
- o fluxo resultante é imposto na atualização hidráulica

Isto significa que o solucionador inercial local é modificado localmente pelo comportamento da estrutura de controle. A descarga é prescrita a partir da relação nominal, em vez de ser obtida exclusivamente a partir do cálculo de fluxo padrão baseado em face.

---

### Estrutura da tabela de entrada

As condições de contorno internas são definidas na aba Control structures da planilha do caso (`BC_Control_structure.xlsx` no formato antigo), lida quando `flag_reservoir = 1`. Cada linha é uma estrutura. A vazão de saída é $Q = k_1 (h - h_{0,1})^{k_2}$ para a célula $(x_{d,1}, y_{d,1})$ e $Q = k_3 (h - h_{0,2})^{k_4}$ para a célula $(x_{d,2}, y_{d,2})$, com coordenadas na projeção do DEM.

#### Estrutura da tabela

| Parâmetro | Unidades | Descrição |
|:---------:|:-----:|-------------|
| $\mathrm{Index}$ | - | Identificador da estrutura de controle |
| $x$ | $\mathrm{m}$ | Coordenada leste da célula de controle |
| $y$ | $\mathrm{m}$ | Coordenada norte da célula de controle |
| $k_1$ | - | Coeficiente da primeira ramificação da curva de classificação |
| $h_{0,1}$ | $\mathrm{m}$ | Profundidade ou limite de referência associado ao primeiro ramo |
| $k_2$ | - | Parâmetro de expoente ou forma associado ao primeiro ramo |
| $x_{\mathrm{d},1}$ | $\mathrm{m}$ | Coordenada leste do primeiro ponto de controle de descarga |
| $y_{\mathrm{d},1}$ | $\mathrm{m}$ | Coordenada norte do primeiro ponto de controle de descarga |
| $k_3$ | - | Coeficiente do segundo ramo da curva de classificação |
| $h_{0,2}$ | $\mathrm{m}$ | Profundidade ou limite de referência associado ao segundo ramo |
| $k_4$ | - | Parâmetro de expoente ou forma associado ao segundo ramo |
| $x_{\mathrm{d},2}$ | $\mathrm{m}$ | Coordenada leste do segundo ponto de controle de descarga |
| $y_{\mathrm{d},2}$ | $\mathrm{m}$ | Coordenada norte do segundo ponto de controle de descarga |

*Tabela 3. Tabela de parâmetros de condição de limite interno HydroPol2D. Esses parâmetros definem o comportamento da curva nominal usada para converter profundidade em vazão.*

---

### Valores de exemplo

| $\mathrm{Index}$ | $x$ $(\mathrm{m})$ | $y$ $(\mathrm{m})$ | $k_1$ | $h_{0,1}$ $(\mathrm{m})$ | $k_2$ | $x_{\mathrm{d},1}$ $(\mathrm{m})$ | $y_{\mathrm{d},1}$ $(\mathrm{m})$ | $k_3$ | $h_{0,2}$ $(\mathrm{m})$ | $k_4$ | $x_{\mathrm{d},2}$ $(\mathrm{m})$ | $y_{\mathrm{d},2}$ $(\mathrm{m})$ |
|:----------------:|-------------------:|-------------------:|------:|-------------------------:|------:|-----------------------------------:|-----------------------------------:|------:|-------------------------:|------:|-----------------------------------:|-----------------------------------:|
| 1 | -5166015.11 | -2706361,32 | 1,5 | 0,0 | 0,50 | -5166037,22 | -2706321.554 | 3,0 | 2,5 | 1,5 | -5166037,22 | -2706321.554 |
| 2 | -5166922,84 | -2704154,64 | 16,0 | 0,0 | 1,5 | -5166922,84 | -2704174,64 | 0,538951413 | 0,1 | 0,5 | -5166922,84 | -2704174,64 |

*Tabela 4. Exemplo de parâmetros de condição de limite interno usados ​​atualmente em HydroPol2D.*

---

### Interpretação

A formulação da estrutura de controle é baseada em uma relação profundidade-descarga da forma geral:
$$
Q = f(h)
$$
onde:
- $Q$ é descarregado através da estrutura em $\mathrm{m^3\,s^{-1}}$
- $h$ é a profundidade local da água em $\mathrm{m}$
- os coeficientes $k_1$, $k_2$, $k_3$ e $k_4$ definem a resposta da curva de classificação
- os termos $h_{0,1}$ e $h_{0,2}$ definem as profundidades de referência associadas a cada ramo

As coordenadas $\left(x_{\mathrm{d},1}, y_{\mathrm{d},1}\right)$ e $\left(x_{\mathrm{d},2}, y_{\mathrm{d},2}\right)$ são as células que recebem a vazão de cada ramo. A vazão sai da célula de controle e entra nessa célula, de modo que a transferência conserva a massa. Cada liberação é limitada à água acima do seu limiar, e o segundo ramo usa a profundidade que sobra depois do primeiro. Um destino $(0, 0)$ manda a vazão para fora do modelo, e ela é contada como vazão no exutório. Um destino vazio desliga esse ramo.
Esta estrutura permite representar uma relação simples de descarga por partes usando dois ramos parametrizados.

---

### Significado prático dos parâmetros

- $k_1$ e $k_3$ controlam a magnitude da resposta de descarga
- $k_2$ e $k_4$ controlam a curvatura ou não linearidade da resposta
- $h_{0,1}$ e $h_{0,2}$ definem limites de ativação ou profundidades de referência
- $x_{\mathrm{d},1}, y_{\mathrm{d},1}, x_{\mathrm{d},2}, y_{\mathrm{d},2}$ definem onde a descarga controlada está ligada espacialmente

Juntos, esses parâmetros definem como a estrutura interna converte a profundidade da água em fluxo.

---

### Considerações Práticas

- as coordenadas de controle devem ser consistentes com a projeção DEM
- as células selecionadas devem coincidir com células hidráulicas válidas no domínio do modelo
- os coeficientes da curva de classificação devem ser fisicamente realistas
- curvas de classificação excessivamente íngremes podem criar instabilidade numérica
- estruturas de controle devem ser testadas cuidadosamente porque alteram diretamente os fluxos de massa locais

---

### Resumo

As condições de contorno interno em HydroPol2D são representadas através de uma estrutura de curva nominal simples que converte a profundidade local da água em descarga.
Eles estão acostumados a:
- impor fluxos controlados de entrada ou saída
- representam estruturas de controle hidráulico
- modificar a dinâmica inercial local em células específicas

Sua parametrização correta é essencial para uma simulação estável e fisicamente significativa de sistemas hidráulicos projetados.

---

## Tabela de parâmetros de neve

A tabela de parâmetros LULC contém as colunas de neve a seguir em cada linha de `LULC_Index`. Não existe uma planilha separada de neve; todas as propriedades dependentes da cobertura do solo permanecem no mesmo registro de classe.

| Coluna | Unidades | Descrição |
|---|---|---|
| `LULC_Index` | — | Código LULC da linha. |
| `Snow_Albedo` | — | Albedo de onda curta da superfície de neve. |
| `Snow_Emissivity` | — | Emissividade de onda longa usada no balanço de radiação. |
| `Sublimation_Coefficient_d_1` | dia⁻¹ (m s⁻¹)⁻¹ | Coeficiente do termo de sublimação. |
| `Degree_Day_Factor_mm_C_day` | mm °C⁻¹ dia⁻¹ | Fator de derretimento por graus-dia. |
| `T_Snow_All_C` | °C | Temperatura na qual toda a precipitação é neve. |
| `T_Rain_All_C` | °C | Temperatura na qual toda a precipitação é chuva; não pode ser menor que `T_Snow_All_C`. |
| `Rho_Snow_Init_kg_m3` | kg m⁻³ | Densidade de neve nova usada na inicialização. |
| `Rho_Snow_Max_kg_m3` | kg m⁻³ | Limite superior de densidade após compactação. |
| `Compaction_Temperature_kg_m3_C_day` | kg m⁻³ °C⁻¹ dia⁻¹ | Aumento de densidade dependente da temperatura. |
| `Compaction_SWE_kg_m3_mm_day` | kg m⁻³ mm⁻¹ dia⁻¹ | Aumento de densidade dependente de SWE. |
| `Compaction_Depth_kg_m3_mm_day` | kg m⁻³ mm⁻¹ dia⁻¹ | Aumento de densidade dependente da profundidade. |

Os fatores de graus-dia, sublimação e compactação são taxas e o modelo os multiplica pelo passo de tempo atual. A neve exige a forçante meteorológica interna, para obter temperatura média, temperatura mínima e vento.

---

## Filosofia de Design

HydroPol2D separa:
- **entradas espaciais**, que definem onde cada aula ocorre,
- **tabelas de parâmetros**, que definem como cada classe se comporta.

Isso torna o modelo mais fácil de manter, calibrar e aplicar em diferentes domínios.

---

## Resumo

As tabelas de parâmetros definem como HydroPol2D traduz dados espaciais categóricos em comportamento físico.
Eles são um componente central da estrutura do modelo e devem ser cuidadosamente preparados para garantir simulações consistentes, estáveis ​​e fisicamente significativas.
