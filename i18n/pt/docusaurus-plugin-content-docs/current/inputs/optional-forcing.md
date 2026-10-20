---
title: Forçamento Opcional
---

# Forçamento Opcional

HydroPol2D suporta vários tipos de forçamento meteorológico e hidrológico além da entrada básica de chuva.
Todas as configurações de forçamento são definidas através do arquivo `General_Data.xlsx`, que controla:
- o tipo de forçamento usado,
- a ativação de componentes do modelo,
- e os conjuntos de dados de entrada associados.

O modelo pode operar sob diferentes estratégias de forçamento dependendo da disponibilidade de dados e dos objetivos da simulação.

---

## Visão geral

HydroPol2D suporta as seguintes opções de forçamento:
- Forçamento meteorológico para evapotranspiração (Penman – Monteith)
- Entradas diretas de evaporação ($E$) e transpiração ($T$)
- Forçamento espacial de chuva (baseado em raster ou interpolado em medidor)
- Tempestades de design sintético (Huff e Bloco Alternado)
- Hidrogramas de afluência externa
- Condições de limite do palco

Cada tipo de forçamento é ativado e configurado através de `General_Data.xlsx`.

---

## Forçamento Meteorológico (Penman – Monteith)

HydroPol2D calcula a evapotranspiração usando uma formulação de Penman-Monteith quando o forçamento meteorológico é fornecido.
### Fonte de entrada

Os dados meteorológicos são fornecidos através de:
- `ETP_input_data.xlsx`

---

### Interpolação espacial

As variáveis ​​meteorológicas são distribuídas espacialmente usando:
- ponderação de distância inversa (IDW)

Isto garante que o forçamento atmosférico seja consistente em todo o domínio com base nos pontos de medição disponíveis.

---

### Variáveis ​​obrigatórias

As entradas típicas incluem:
- temperatura do ar
- radiação (rede ou solar)
- umidade relativa
- velocidade do vento

---

### Papel no modelo

O forçamento meteorológico é usado para calcular a evapotranspiração, que remove água de:
- armazenamento de superfície
- umidade do solo

Esta abordagem é recomendada quando o forçamento atmosférico total está disponível.

---

## Entradas diretas de evaporação e transpiração

HydroPol2D permite especificação direta de evaporação e transpiração.
### Entradas

- evaporação ($E$) raster ou série temporal
- transpiração ($T$) raster ou série temporal

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### Papel no modelo

Esses fluxos são aplicados diretamente a:
- armazenamento de água superficial
- umidade do solo

Esta abordagem ignora a necessidade de forçamento meteorológico.

---

## Forçamento de chuva

HydroPol2D suporta múltiplas configurações de entrada de chuva.

---

### 1. Chuvas concentradas (uniformes)

Definido através de:
- `Rainfall_Intensity_Data.xlsx`

---

#### Descrição

- a chuva é aplicada uniformemente sobre o domínio
- definida como uma série temporal

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### 2. Precipitação medida (interpolação espacial)

Definido através de:
- `Rainfall_Spatial_Input.xlsx`

---

#### Interpolação espacial

Os campos de precipitação são calculados usando:
- ponderação de distância inversa (IDW)

As medições do medidor são interpoladas para todas as células da grade com base em sua localização espacial.

---

#### Descrição

- vários medidores podem ser especificados
- a precipitação varia espacial e temporalmente
- adequado para conjuntos de dados de precipitação observados

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### 3. Precipitação baseada em raster

A precipitação também pode ser fornecida como:
- pilhas raster variáveis ​​​​no tempo

Unidades:
- $\mathrm{mm\,h^{-1}}$

---

### Papel no modelo

Impulsos de chuva:
- infiltração
- geração de escoamento
- roteamento de fluxo de superfície

---

## Tempestades de design

HydroPol2D inclui geração de tempestade sintética integrada.
### Métodos disponíveis

- Distribuições Huff
- Método de bloco alternado

---

### Configuração

Definido por meio de `General_Data.xlsx`, incluindo:
- profundidade total de precipitação
- duração da tempestade
- distribuição temporal

O modelo gera internamente o hietógrafo de chuvas.

---

## Hidrogramas de afluência externa

A entrada externa é definida por meio de:
- `Inflow_Hydrograph.xlsx`

---

### Papel no modelo

Usado para:
- condições de contorno a montante
- afluência do rio
- cenários de ruptura de barragem ou influxo controlado

---

### Implementação

- vários medidores podem ser definidos
- cada medidor está associado a coordenadas espaciais
- o fluxo de entrada é distribuído por todas as células associadas a cada medidor

Unidades:
- $\mathrm{m^3\,s^{-1}}$

---

## Condições de limite do estágio

As condições de limite do estágio são definidas por meio de:
- `Stage_Hydrograph.xlsx`

---

### Papel no modelo

Usado para:
- controle a jusante
- efeitos de remanso
- restrições hidráulicas

---

### Implementação

- estágio é prescrito como profundidade ou elevação da água
- todas as células associadas ao limite recebem o mesmo valor imposto

Unidades:
- $\mathrm{m}$

---

## Controle através de `General_Data.xlsx`

O arquivo `General_Data.xlsx` define:
- quais componentes de forçamento estão ativos
- quais conjuntos de dados são usados
- resolução temporal
- consistência da unidade

Ele atua como a interface central entre as entradas definidas pelo usuário e o modelo.

---

## Interação entre componentes de força

As entradas forçadas interagem da seguinte forma:
- a chuva introduz água no sistema
- evapotranspiração remove água do armazenamento
- variáveis ​​​​meteorológicas controlam fluxos movidos por energia
- hidrogramas de entrada adicionam descarga externa
- limites do estágio restringem a resposta hidráulica

Essas interações definem a dinâmica do sistema.

---

## Considerações Práticas

- garantir consistência temporal em todas as entradas forçadas
- verifique as unidades antes da simulação
- evite misturar resoluções de tempo incompatíveis
- confirmar o posicionamento espacial correto dos medidores
- garantir que as entradas de interpolação sejam bem distribuídas espacialmente
- combinar a resolução forçada com o passo de tempo do modelo

---

## Resumo

O forçamento opcional no HydroPol2D permite configurações de simulação flexíveis que vão desde cenários simples baseados em chuva até sistemas hidrológicos meteorológicos totalmente acoplados.
Todas as configurações forçadas são gerenciadas através do `General_Data.xlsx`, permitindo aos usuários:
- alternar entre estratégias de forçamento
- integrar conjuntos de dados externos
- e definir eventos sintéticos

A abordagem de forçamento selecionada deve refletir:
- o objetivo da simulação
- disponibilidade de dados
- e o nível exigido de representação física