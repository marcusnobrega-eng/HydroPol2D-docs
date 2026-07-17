---
title: Tabelas de parâmetros
---

# Tabelas de parâmetros

HydroPol2D usa tabelas de parâmetros para atribuir propriedades físicas a entradas raster categóricas.
Mapas categóricos como LULC e Solo não são usados ​​diretamente nas equações governantes. Em vez disso, cada classe atua como um índice em uma tabela de parâmetros, onde os parâmetros físicos correspondentes são definidos.
Essa estrutura separa as informações espaciais da definição dos parâmetros e torna o modelo mais fácil de calibrar, adaptar e interpretar.
---

## Estrutura Geral

Cada tabela de parâmetros contém:
- um **identificador de classe** (`Index`)
- um conjunto de **parâmetros associados a essa classe**

Em tempo de execução, HydroPol2D:
1. lê o valor raster em cada célula da grade,
2. usa esse valor como um índice,
3. atribui os parâmetros correspondentes da tabela.

Por esse motivo, as classes raster e os índices de tabela devem corresponder exatamente.
---

## Tabela de parâmetros LULC

A tabela LULC define propriedades relacionadas à superfície que controlam a resistência ao fluxo, interceptação, impermeabilidade, comportamento relacionado a poluentes e profundidade da zona radicular quando o armazenamento em camadas do solo está ativo.
### Estrutura de exemplo

| Cobertura do solo | Índice | $n$<br />$(\mathrm{s\,m^{-1/3}})$ | $h_0$<br />$(\mathrm{mm})$ | $d_0$<br />$(\mathrm{mm})$ | $C_1$ | $C_2$ | $C_3$ | $C_4$ | $\mathrm{index\_impervious}$ | $\mathrm{root\_depth\_m}$ |
|:----------:|:-----:|:---------------------------------:|:--------------------------:|:--------------------------:|:-----:|:-----:|:-----:|:-----:|:----------------------------:|:--------------------------:|
| Cobertura de árvore | 10 | 0,10 | 0 | 0 | 10 | 0,20 | 800 | 1,20 | 50 | 1,50 |
| Arbustos | 20 | 0,08 | 0 | 0 | 12 | 0,20 | 900 | 1,20 | NaN | 1,00 |
| Pastagem | 30 | 0,06 | 0 | 0 | 15 | 0,22 | 1000 | 1,20 | NaN | 0,60 |
| Terras agrícolas | 40 | 0,05 | 0 | 0 | 30 | 0,25 | 1400 | 13h30 | NaN | 1,00 |
| Construído | 50 | 0,03 | 0 | 0 | 80 | 0h30 | 2000 | 13h30 | NaN | 0,00 |
| Vegetação nua / esparsa | 60 | 0,035 | 0 | 0 | 45 | 0,25 | 1600 | 1,25 | NaN | 0,10 |
| Neve e gelo | 70 | 0,02 | 0 | 0 | 1 | 0,10 | 200 | 1.10 | NaN | 0,00 |
| Corpos de água permanentes | 80 | 0,035 | 0 | 0 | 0 | 0 | 0 | 0 | NaN | 0,00 |
| Zona húmida herbácea | 90 | 0,12 | 0 | 0 | 8 | 0,18 | 700 | 1,20 | NaN | 0,40 |
| Manguezais | 95 | 0,15 | 0 | 0 | 8 | 0,18 | 700 | 1,20 | NaN | 1,00 |
| Musgo e líquen | 100 | 0,08 | 0 | 0 | 5 | 0,15 | 500 | 1,15 | NaN | 0,15 |

*Tabela 1. Tabela de parâmetros HydroPol2D LULC. Os valores `Index` devem corresponder aos valores categóricos no raster LULC.*
### Definições de variáveis

- $n$: coeficiente de rugosidade de Manning
- $h_0$: parâmetro de interceptação
- $d_0$: parâmetro inicial de armazenamento de superfície
- $C_1$–$C_4$: coeficientes associados ao acúmulo de poluentes e formulação de lavagem
- $\mathrm{index\_impervious}$: identificador usado para associar uma classe com comportamento impermeável
- $\mathrm{root\_depth\_m}$: profundidade da zona radicular controlada pela vegetação usada pelo modelo de solo/vadoso em camadas

Os valores mostrados acima correspondem à tabela de parâmetros HydroPol2D atual e devem ser revisados ​​conforme necessário para o esquema de classificação adotado e área de estudo.
Na implementação atual, `root_depth_m` é a forma suportada de fornecer entrada de profundidade raiz para o modelo. Não existe um caminho raster de profundidade de raiz separado; a profundidade da raiz é atribuída por classe LULC e então mapeada para a grade por meio do raster categórico LULC.
---

## Tabela de parâmetros do solo

A tabela de solos define as propriedades hidráulicas básicas usadas para estimar a infiltração, o armazenamento vadoso em camadas, a recarga e o comportamento das águas subterrâneas.
### Estrutura de exemplo

| Tipo de solo | Índice | $K_{\mathrm{sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $n$ | $\alpha$<br />$(\mathrm{m^{-1}})$ | $\theta_{\mathrm{sat}}$ | $\theta_{\mathrm{r}}$ | $\theta_{\mathrm{i}}$ | $S_{\mathrm{y}}$ | $K_{\mathrm{g,sat}}$<br />$(\mathrm{mm\,h^{-1}})$ | $\mathrm{PHTOKEN0XYZ}$<br />$(\mathrm{m})$ | $K_s$ perto | $K_s$ raiz | transmissão $K_s$ |
|:---------:|:-----:|:-----------------------------------------------:|:---:|:----------------------------------:|:----------------------:|:--------------------:|:--------------------:|:---------------:|:---------------------------------------------------:|:--------------------------------:|:------------:|:----------:|:--------------------:|
| Argila | 1 | 0,3 | 1.09 | 0,8 | 0,385 | 0,068 | 0,0997 | 0,03 | 6 | 1 | 1 | 1 | 1 |
| Argila Siltosa | 2 | 0,5 | 1.23 | 1,0 | 0,423 | 0,089 | 0,1224 | 0,04 | 10 | 1 | 1 | 1 | 1 |
| Argila arenosa | 3 | 0,6 | 1.31 | 1,5 | 0,321 | 0,075 | 0,0996 | 0,06 | 12 | 1 | 1 | 1 | 1 |
| Argila Argilosa | 4 | 1,0 | 1.31 | 1,9 | 0,309 | 0,095 | 0,1164 | 0,08 | 20 | 1 | 1 | 1 | 1 |
| Argila Siltosa | 5 | 1,0 | 1.23 | 1,5 | 0,432 | 0,089 | 0,1233 | 0,09 | 20 | 1 | 1 | 1 | 1 |
| Argila arenosa | 6 | 1,5 | 1,48 | 3,0 | 0,330 | 0,065 | 0,0915 | 0,11 | 30 | 1 | 1 | 1 | 1 |
| Argila Siltosa | 7 | 7.6 | 1,41 | 4,5 | 0,434 | 0,067 | 0,1220 | 0,14 | 152 | 1 | 1 | 1 | 1 |
| Argila | 8 | 3.4 | 1,56 | 3.6 | 0,486 | 0,078 | 0,1104 | 0,18 | 68 | 1 | 1 | 1 | 1 |
| Argila arenosa | 9 | 10.9 | 1,89 | 7,5 | 0,412 | 0,065 | 0,1287 | 0,22 | 218 | 1 | 1 | 1 | 1 |
| Lodo | 10 | 3.4 | 1,37 | 4,0 | 0,486 | 0,067 | 0,1234 | 0,12 | 68 | 1 | 1 | 1 | 1 |
| Areia Argilosa | 11 | 29,9 | 2.28 | 14,5 | 0,401 | 0,057 | 0,1172 | 0,25 | 598 | 1 | 1 | 1 | 1 |
| Areia | 12 | 117,8 | 2,68 | 14,5 | 0,417 | 0,045 | 0,1225 | 0h30 | 2356 | 1 | 1 | 1 | 1 |
| Água | 0 | 0,3 | 1.09 | 0,8 | 0,385 | 0,068 | 0,0997 | 0,03 | 6 | 1 | 1 | 1 | 1 |

*Tabela 2. Tabela de parâmetros do solo HydroPol2D. Os valores `Index` devem corresponder aos valores categóricos no raster do solo.*
### Definições de variáveis

- $K_{\mathrm{sat}}$: condutividade hidráulica saturada
- $n$: parâmetro de forma de Van Genuchten
- $\alpha$: parâmetro de entrada de ar inverso
- $\theta_{\mathrm{sat}}$: teor de água saturada
- $\theta_{\mathrm{r}}$: teor de água residual
- $\theta_{\mathrm{i}}$: umidade inicial do solo
- $S_{\mathrm{y}}$: rendimento específico
- $K_{\mathrm{g,sat}}$: condutividade saturada associada à parametrização de águas subterrâneas ou subterrâneas
- $\mathrm{PHTOKEN0XYZ}$: profundidade até o leito rochoso ou profundidade efetiva de armazenamento
- `Ks_multiplier_near_surface`: multiplicador aplicado à base $K_{\mathrm{sat}}$ na camada próxima à superfície
- `Ks_multiplier_root_zone`: multiplicador aplicado à base $K_{\mathrm{sat}}$ na camada da zona raiz
- `Ks_multiplier_transmission`: multiplicador aplicado à base $K_{\mathrm{sat}}$ na camada de transmissão

A classe categórica do solo define as propriedades hidráulicas básicas do pilar. A implementação em camadas atribui essas propriedades às camadas próximas à superfície, zona raiz e zona de transmissão e, em seguida, aplica multiplicadores de condutividade opcionais onde eles são fornecidos.
LULC controla a profundidade da zona raiz. A profundidade do leito rochoso e a posição atual do lençol freático restringem as espessuras finais da camada, de modo que geometrias de camada fisicamente impossíveis colapsam ou truncam, em vez de produzir armazenamento negativo.
Os valores mostrados acima correspondem à tabela atual de parâmetros de solo HydroPol2D e devem ser revisados ​​conforme necessário para o cenário de classificação e simulação de solo adotado.
---

## Atribuição DTB através da tabela de solos

Se um raster DTB não estiver disponível, os valores DTB podem ser atribuídos diretamente na tabela de solos.
Nesse caso:
- cada classe de solo está associada a um valor representativo de DTB,
- o campo DTB é construído implicitamente a partir do mapa do solo,
- a profundidade de armazenamento permanece consistente com a classificação de solo adotada.

Isto é particularmente útil em aplicações com escassez de dados.


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

As condições de contorno interno são definidas através de uma planilha dedicada.
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

As coordenadas $\left(x_{\mathrm{d},1}, y_{\mathrm{d},1}\right)$ e $\left(x_{\mathrm{d},2}, y_{\mathrm{d},2}\right)$ definem os locais nos quais o controle de descarga é aplicado ou avaliado.
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

## Filosofia de Design

HydroPol2D separa:
- **entradas espaciais**, que definem onde cada aula ocorre,
- **tabelas de parâmetros**, que definem como cada classe se comporta.

Isso torna o modelo mais fácil de manter, calibrar e aplicar em diferentes domínios.
---

## Resumo

As tabelas de parâmetros definem como HydroPol2D traduz dados espaciais categóricos em comportamento físico.
Eles são um componente central da estrutura do modelo e devem ser cuidadosamente preparados para garantir simulações consistentes, estáveis ​​e fisicamente significativas.