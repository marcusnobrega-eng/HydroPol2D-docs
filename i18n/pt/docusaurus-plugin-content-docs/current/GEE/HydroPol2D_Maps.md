---
title: Visão geral
---

# Caracterização de captação com Google Earth Engine

HydroPol2D inclui um script Google Earth Engine (GEE) para gerar os conjuntos de dados espaciais necessários para definir um domínio de modelagem hidrológica.
O fluxo de trabalho extrai, processa e exporta diversas variáveis ​​ambientais de conjuntos de dados geoespaciais hospedados na nuvem, produzindo um conjunto consistente de entradas raster e tabelas de resumo para uma captação ou grupo de captação selecionado.

---

## Acessando Google Earth Engine

Para usar este fluxo de trabalho, os usuários devem ter acesso a Google Earth Engine.
### 1. Crie uma conta

Vá para:
https://earthengine.google.com/
Clique em **“Cadastre-se”** e cadastre-se usando uma conta Google.
A aprovação normalmente é automática para uso acadêmico ou de pesquisa, mas pode levar algum tempo dependendo da solicitação.

---

### 2. Abra o Editor de Código

Assim que o acesso for concedido, abra o Editor de Código GEE:
https://code.earthengine.google.com/
Este é o ambiente onde o script é executado.

---

### 3. Adicione o script HydroPol2D

Copie o código JavaScript fornecido no Editor de Código e execute-o diretamente no navegador.
O script usa a API Earth Engine para acessar conjuntos de dados, realizar operações espaciais e exportar resultados para o Google Drive.

---

## O que o fluxo de trabalho faz

O script constrói um domínio de modelagem a partir de bacias hidrográficas HydroBASINS e gera um banco de dados padronizado de camadas raster e estatísticas resumidas.
Os principais resultados incluem:
### Conjuntos de dados rasterizados

- Modelo Digital de Elevação (DEM)
- Uso/Cobertura do Solo (LULC)
- Classe de textura do solo
- Profundidade até o leito rochoso (DTB)
- Albedo de superfície
- Índice de área foliar (LAI)
- Densidade populacional (WorldPop)

Todos os rasters são:
- Cortado para o domínio selecionado
- Exportado em uma resolução espacial consistente
- Reprojetado para um sistema de coordenadas definido pelo usuário
- Atribuído um valor comum sem dados

---

### Saídas vetoriais e tabulares

O script também gera:
- Um shapefile do domínio de captação mesclado
- Uma tabela de resumo em nível de domínio (CSV)
- Uma tabela de resumo por bacia hidrográfica (CSV)

Estes resultados fornecem metadados e estatísticas agregadas para a área de estudo.

---

## Estrutura geral do fluxo de trabalho

O código segue uma sequência estruturada:
### 1. Entradas definidas pelo usuário

O usuário especifica:
- Nível HydroBASINS (por exemplo, 6, 7, 8)
- Lista de valores `HYBAS_ID`
- Nome da pasta de saída
- Resolução espacial (escala de exportação)
- Sistema de referência de coordenadas (CRS)
- Intervalo de tempo para conjuntos de dados dependentes de tempo
- Ano para dados populacionais

Esses parâmetros controlam a definição do domínio e o processamento do conjunto de dados.

---

### 2. Seleção e fusão de bacias hidrográficas

O script carrega polígonos HydroBASINS e os filtra usando os valores `HYBAS_ID` selecionados.
As bacias hidrográficas selecionadas são mescladas em uma única geometria, que define o domínio de modelagem.

---

### 3. Construção de domínio

A geometria mesclada é usada para:
- Recorte todos os conjuntos de dados raster
- Definir limites de exportação
- Calcular estatísticas resumidas
- Exportar o limite da bacia hidrográfica como um shapefile

---

### 4. Recuperação e processamento de conjuntos de dados

O script acessa vários conjuntos de dados disponíveis em Google Earth Engine, incluindo:
- MERIT DEM para topografia
- ESA WorldCover para uso da terra
- OpenLandMap para classes de solo
- Produtos MODIS para albedo e LAI
- WorldPop para densidade populacional

Para conjuntos de dados dependentes do tempo (por exemplo, albedo e LAI), o script calcula valores medianos no intervalo de tempo selecionado.

---

### 5. Exportação de camadas raster

Cada conjunto de dados é:
- Cortado ao domínio
- Padronizado em resolução e projeção
- Exportado para o Google Drive como GeoTIFF

---

### 6. Cálculo de estatísticas resumidas

O script calcula métricas em nível de domínio, como:
- Área total
- Elevação média
- Profundidade média até o leito rochoso
- Média LAI e albedo
- Uso dominante da terra e classe de solo
- População total
- Fração impermeável média

Uma segunda tabela é gerada com as mesmas métricas calculadas individualmente para cada bacia hidrográfica.

---

## Estrutura de saída

Todas as saídas são salvas na pasta especificada do Google Drive e incluem:
- Mapas raster (GeoTIFF)
- Shapefile de captação (SHP)
- Tabela de resumo de domínio (CSV)
- Tabela de resumo por bacia hidrográfica (CSV)

Esses arquivos podem ser usados ​​diretamente como entradas para HydroPol2D ou posteriormente processados ​​em GIS ou ambientes de modelagem.

---

## Próximas etapas

As seções a seguir descrevem como configurar o script e exportar cada conjunto de dados passo a passo.