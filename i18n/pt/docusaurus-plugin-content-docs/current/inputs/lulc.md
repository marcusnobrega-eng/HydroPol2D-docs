---
title: LULC
---

# Uso/Cobertura do Solo (LULC)

O mapa Uso/Cobertura do Solo (LULC) define a distribuição espacial das características da superfície em todo o domínio de simulação.
Em HydroPol2D, a entrada LULC é usada para representar como diferentes porções do domínio respondem à precipitação e ao fluxo superficial por meio da atribuição de parâmetros.

---

## Função em HydroPol2D

O mapa LULC é usado para definir a variabilidade espacial em:
- Rugosidade superficial (coeficiente Manning)
- Armazenamento de interceptação
- Fração impermeável
- Comportamento de evapotranspiração relacionado à superfície

Essas propriedades influenciam diretamente a geração de escoamento superficial, a velocidade do fluxo e a retenção de água na superfície.

---

## Representação LULC

HydroPol2D requer um **mapa LULC categórico**.
Cada célula da grade deve receber um identificador de classe de uso do solo (valor inteiro ou categórico). Essas classes não são usadas diretamente nas equações governantes. Em vez disso, eles servem como **índices em tabelas de parâmetros**.
Para cada classe LULC, um conjunto de parâmetros é definido externamente nas tabelas de entrada. Isso inclui:
- Coeficiente de rugosidade de Manning
- Capacidade de interceptação
- Fração impermeável
- Parâmetros adicionais específicos do processo

Esta abordagem separa as informações espaciais da definição de parâmetros e permite total flexibilidade na configuração do comportamento do modelo.

---

## Conjuntos de dados LULC disponíveis

Vários conjuntos de dados LULC globais e regionais de alta qualidade estão disponíveis gratuitamente:
### NLCD (banco de dados nacional de cobertura do solo)
- Região: Estados Unidos
- Resolução: 30 m
- Inclui classes urbanas detalhadas e superfícies impermeáveis
- Baixar: https://www.mrlc.gov/

---

### ESA WorldCover
- Região: Global
- Resolução: 10 m
- Classificação global de alta resolução
- Baixar: https://worldcover2020.esa.int/

---

### Serviço de monitorização terrestre Copernicus
- Região: Europa e produtos globais
- Resolução: 10–100 m
- Inclui várias camadas temáticas
- Baixar: https://land.copernicus.eu/

---

### Cobertura do solo MODIS (MCD12Q1)
- Região: Global
- Resolução: 500 m
- Série temporal anual de longo prazo
- Baixar: https://lpdaac.usgs.gov/products/mcd12q1v061/

---

### Mundo Dinâmico
- Região: Global
- Resolução: 10 m
- Classificação quase em tempo real derivada do Sentinel-2
- Fornece resultados de classe probabilística
- Particularmente útil para ambientes dinâmicos ou em rápida mudança
- Acesso: Google Earth Engine

---

## Associação de parâmetros

As classes LULC são mapeadas para parâmetros do modelo por meio das tabelas de entrada.
Cada classe deve estar associada a um conjunto consistente de valores físicos. Este mapeamento determina como o modelo representa:
- Resistência superficial ao fluxo
- Interceptação de chuva
- Comportamento de geração de escoamento

A atribuição de parâmetros incorreta ou inconsistente afetará diretamente os resultados da simulação.

---

## Superfícies Impermeáveis

As classes urbanas normalmente incluem uma fração significativa de áreas impermeáveis ​​(estradas, telhados, calçadas).
Estas áreas são caracterizadas por:
- Infiltração insignificante
- Geração rápida de escoamento
- Aumento das velocidades de fluxo

O parâmetro fração impermeável é utilizado para representar esse comportamento e deve ser cuidadosamente atribuído às classes de uso do solo urbano.
### Substituição raster impermeável fracionária

HydroPol2D também pode ingerir um raster `ImperviousFraction_path` opcional. Quando presente, ele refina a fração impermeável por célula além da atribuição LULC baseada em classe.
Detalhes de implementação atuais:
- valores raster podem ser fornecidos em porcentagem `[0,1]` ou `[0,100]`,
- o raster está alinhado ao DEM internamente,
- classes LULC construídas/explicitamente impermeáveis ​​ainda são forçadas a permanecer totalmente impermeáveis.

Portanto, a tabela LULC ainda define o comportamento impermeável da base, enquanto o raster de fração impermeável fornece um refinamento espacial sobre essa base.

---

## Resolução e Alinhamento

O raster LULC deve:
- Corresponder ou ser reamostrado para a resolução DEM
- Use o mesmo sistema de referência de coordenadas projetadas (CRS)
- Alinhe espacialmente com todas as outras entradas raster

O desalinhamento leva à atribuição incorreta de parâmetros e à representação inconsistente do fluxo.

---

## Reclassificação

Os conjuntos de dados LULC brutos geralmente contêm um grande número de classes.
Para aplicações HydroPol2D, geralmente é preferível:
- Agregue classes em um conjunto reduzido de categorias representativas
- Agrupar tipos de uso de solo semelhantes
- Simplifique o esquema de parametrização

Isso melhora a robustez do modelo e reduz a complexidade desnecessária.

---

## Interação com outras entradas

O mapa LULC define o comportamento da superfície e deve ser consistente com:
- **DEM** → define terreno e roteamento de fluxo
- **Solo** → controla a capacidade de infiltração
- **LAI** → influencia processos relacionados à vegetação
- **Albedo** → afeta o equilíbrio energético da superfície

Cada uma dessas entradas contribui com um aspecto diferente da variabilidade espacial no modelo.

---

## Resumo

Em HydroPol2D, LULC é tratado como um mapa categórico usado para atribuir parâmetros relacionados à superfície por meio de tabelas de pesquisa.
A qualidade da classificação e a consistência do mapeamento dos parâmetros são críticas para representar com precisão a resistência ao fluxo superficial, a geração de escoamento superficial e os efeitos da vegetação.