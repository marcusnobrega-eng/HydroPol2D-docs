---
title: Mapas de entrada HydroPol2D
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
Clique em **"Cadastre-se"** e cadastre-se usando uma conta Google.
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
- Camada Global de Assentamento Humano para superfícies construídas

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
- Fração média de superfície construída

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

## Parâmetros principais explicados

### Níveis HydroBASINS

HydroBASINS fornece limites de bacias hidrográficas em diferentes níveis hierárquicos (1-12), onde:
- **Nível 1-3**: bacias hidrográficas continentais e principais
- **Nível 4-6**: Grandes bacias hidrográficas regionais (recomendado para estudos regionais)
- **Nível 7-9**: Sub-bacias hidrográficas (recomendado para estudos locais/bacias hidrográficas)
- **Nível 10-12**: Pequenas bacias hidrográficas de cabeceira

**Como escolher**: Níveis mais altos = bacias hidrográficas menores e mais detalhadas. Para a maioria das aplicações, os níveis 6 a 8 proporcionam um bom equilíbrio.
---

### Encontrando Valores HYBAS_ID

Para identificar os valores `HYBAS_ID` para sua área de estudo:
#### Opção 1 - Usando o Editor de Código GEE

- Carregue HydroBASINS no Editor de Código
- Clique nas áreas de interesse
- O `HYBAS_ID` aparece no painel do Inspetor

#### Opção 2 - Baixar shapefile

- Visite [HydroSHEDS](https://www.hydrosheds.org/products/hydrobasins)
- Baixe o nível apropriado para sua região
- Abra no QGIS/ArcGIS e identifique captações por atributos

#### Opção 3 – Visualizador interativo

- Use o [visualizador HydroSHEDS](https://www.hydrosheds.org/hydroatlas)

**Exemplo**: Para um estudo no norte da Califórnia, você pode selecionar diversas bacias hidrográficas de nível 7 que drenam para o rio Sacramento.
---

### Escolhendo Sistemas de Referência de Coordenadas (CRS)

Selecione um CRS apropriado para sua região de estudo:
| Região | CRS recomendado | Código EPSG | Notas |
|--------|----------------|-----------|-------|
| Califórnia, EUA | Albers da Califórnia | `EPSG:3310` | Projeção de áreas iguais |
| EUA continentais | Albers contíguos dos EUA | `EPSG:5070` | Padrão USGS |
| Global/multirregional | WGS 84/UTM | `EPSG:326XX` | Substitua XX por zona |
| Índia | Zona WGS 84/UTM 43N-45N | `EPSG:32643-32645` | Dependendo da longitude |
| Europa | ETRS89 LAEA | `EPSG:3035` | Área igual |

**Por que é importante**: Usar uma projeção local minimiza distorções de área/distância e garante cálculos hidrológicos precisos.
---

### Configurando a escala de exportação

O parâmetro `scale_of_image` controla a resolução de saída:
- **30m**: Alto detalhe, tamanhos de arquivo grandes, processamento mais longo
- **90m** (padrão): Bom equilíbrio para estudos regionais
- **250m**: Processamento mais rápido, arquivos menores, apropriado para domínios grandes
- **1000m**: Resolução grosseira para análise em escala continental

**Recomendação**: corresponda ou exceda ligeiramente a resolução da grade computacional do seu modelo.
---

### Intervalos de datas para dados que variam no tempo

O script calcula **valores medianos** no intervalo de tempo especificado para:
- **Albedo** (MODIS MCD43A3)
- **LAI** (MODIS MCD15A3H)

**Escolhendo datas**:- Use períodos de 3 a 5 anos para suavizar a variabilidade interanual
- Evite períodos com eventos extremos conhecidos (a menos que os estude)
- Exemplo: `'2015-01-01'` a `'2020-01-01'` captura condições recentes e relativamente estáveis

---

## Fontes de dados e resoluções

### Conjuntos de dados de entrada

| Conjunto de dados | Fonte | Resolução nativa | Cobertura Temporal | Notas |
|---------|--------|------------------|-------------------|-------|
| **DEM** | MÉRITO DEM v1.0.3 | ~90m | Estático (anos 2000) | Elevação removida por erro |
| **Uso do solo** | ESA WorldCover | 10m | 2020, 2021 | 11 aulas globais |
| **Textura do solo** | OpenLandMap | 250m | Estático | Classes de textura do USDA |
| **Profundidade até a rocha** | Conjunto de dados globais de solo ORNL DAAC | 1 km | Estático | Estimativas derivadas de ML |
| **Albedo** | MODIS MCD43A3 | 500m | Diariamente desde 2000 | Ondas curtas do céu negro |
| **LAI** | MODIS MCD15A3H | 500m | 4 dias desde 2002 | Índice de área foliar |
| **População** | MundoPop | 100m | Anual 2000-2020 | Estimativa restrita |
| **Superfície construída** | Superfície construída GHSL | 100m | 1975-2030 | Cobertura global |

---

### Classes de Uso/Cobertura do Solo (ESA WorldCover)

A saída LULC usa a seguinte classificação:
| Valor | Aula | Descrição |
|-------|-------|-------------|
| 10 | Cobertura de árvore | Florestas, bosques |
| 20 | Arbustos | Arbustos, arbustos |
| 30 | Pastagem | Pastagens naturais |
| 40 | Terras agrícolas | Áreas agrícolas |
| 50 | Construído | Urbano, assentamentos |
| 60 | Vegetação nua/esparra | Pedra, areia, vegetais escassos |
| 70 | Neve e gelo | Neve/gelo permanente |
| 80 | Corpos d'água | Rios, lagos, oceano |
| 90 | Zona húmida herbácea | Pântanos, pântanos |
| 95 | Manguezais | Florestas de mangue |
| 100 | Musgo e líquen | Vegetação ártica/alpina |

---

### Classes de textura do solo (USDA)

A saída SOIL contém classes de textura do USDA:
| Valor | Classe de Textura | Descrição |
|-------|--------------|-------------|
| 1 | Argila | > 40% argila |
| 2 | Argila siltosa | 40-60% de lodo, > 40% de argila |
| 3 | Argila arenosa | < 45% sand, > 35% argila |
| 4 | Argila argilosa | 27-40% de argila, 20-45% de areia |
| 5 | Argila siltosa | 27-40% de argila, &lt; 20% de areia |
| 6 | Argila arenosa | 20-35% de argila, > 45% de areia |
| 7 | Argila | 7-27% de argila, areia/silte balanceados |
| 8 | Argila siltosa | &lt; 50% de areia, 50-87% de lodo |
| 9 | Argila arenosa | > 50% de areia, 0-50% de lodo |
| 10 | Lodo | > 80% lodo |
| 11 | Areia argilosa | 70-90% areia |
| 12 | Areia | > 85% areia |

---

## Compreendendo os arquivos de saída

### Saídas raster (GeoTIFF)

Todos os arquivos GeoTIFF compartilham:- **Valor sem dados**: `-9999`
- **Projeção**: Conforme especificado por `crs`
- **Resolução**: conforme especificado por `scale_of_image`
- **Extensão**: Recortado ao limite da união de captação

**Nomeação de arquivo**:- `PHTOKEN0XYZ.tif` – Elevação em metros
- `PHTOKEN0XYZ.tif` – Códigos de classe de uso do solo (10-100)
- `SOIL.tif` – Códigos de classe de textura do solo (1-12)
- `PHTOKEN0XYZ.tif` – Profundidade até o leito rochoso em metros
- `Albedo.tif` – Albedo de superfície (0-1, sem unidade)
- `PHTOKEN0XYZ.tif` – Índice de área foliar (m²/m²)
- `WorldPop.tif` – Densidade populacional (pessoas/pixel)

---

### Saída do arquivo shape

**Catchment_Union.shp** contém:- Limite mesclado de todas as bacias hidrográficas selecionadas
- Atributos HydroBASINS originais para cada sub-bacia
- Pode ser usado para:
  - Visualize o domínio em GIS
  - Recorte conjuntos de dados adicionais
  - Definir limites do modelo

---

### Saídas CSV

#### Domain_Log.csv

Resumo de linha única de todo o domínio de modelagem:
| Coluna | Descrição | Unidades |
|--------|-------------|-------|
| `folder_name` | Pasta de exportação do Google Drive | - |
| `hybas_level` | Nível HydroBASINS usado | - |
| `catchment_ids_used` | HYBAS_IDs separados por ponto e vírgula | - |
| `number_of_catchments` | Contagem de bacias hidrográficas mescladas | - |
| `catchment_area_km2` | Área total do domínio | km² |
| `population_in_domain` | População total | pessoas |
| `mean_built_surface_percent` | Superfície construída média | % |
| `dominant_PHTOKEN0XYZ` | Classe de uso da terra mais comum | código |
| `dominant_SOIL` | Classe de solo mais comum | código |
| `avg_albedo` | Albedo médio da superfície | 0-1 |
| `mean_elevation_m` | Elevação média | eu |
| `mean_PHTOKEN0XYZ_m` | Profundidade média até o leito rochoso | eu |
| `mean_PHTOKEN0XYZ` | Índice médio de área foliar | m²/m² |
| `worldpop_year` | Ano de dados do WorldPop | ano |
| `export_scale_m` | Resolução de exportação | eu |
| `crs` | Sistema de coordenadas | Código EPSG |

---

#### Catchment_Log.csv

Estatísticas por bacia hidrográfica com uma linha por sub-bacia hidrográfica:
| Coluna | Descrição | Fonte |
|--------|-------------|--------|
| `HYBAS_ID` | Identificador exclusivo de captação | HydroBASINS |
| `MAIN_BAS` | ID da bacia principal | HydroBASINS |
| `NEXT_DOWN` | ID de captação a jusante | HydroBASINS |
| `UP_AREA` | Área de drenagem a montante | km² |
| `SUB_AREA` | Área de sub-captação | km² |
| `PFAF_ID` | Código Pfafstetter | HydroBASINS |
| `catchment_area_km2` | Área calculada | km² |
| `population` | População total | pessoas |
| `mean_built_surface_percent` | Superfície construída | % |
| `dominant_PHTOKEN0XYZ` | Uso dominante da terra | código |
| `dominant_SOIL` | Classe de solo dominante | código |
| `avg_albedo` | Albedo médio | 0-1 |
| `mean_elevation_m` | Elevação média | eu |
| `mean_PHTOKEN0XYZ_m` | Profundidade média até o leito rochoso | eu |
| `mean_PHTOKEN0XYZ` | Média LAI | m²/m² |

**Caso de uso**: Compare características da sub-bacia, identifique padrões espaciais, valide dados do modelo.
---

## Solução de problemas

### Problemas comuns

#### 1. Erros de memória ("Tempo limite de cálculo esgotado")

**Solução**:- Reduzir o número de captações
- Aumente `scale_stats_continuous` e `scale_stats_categorical`
- Exporte regiões menores separadamente
- Utilize o parâmetro `tileScale` nas operações de redução (já implementado no script)

---

#### 2. Acesso à profundidade até a rocha (DTB)

A profundidade até a camada rochosa é proveniente do conjunto de dados globais de solo ORNL DAAC:
**Citação**: Pelletier, J.D., et al. (2016). Um conjunto de dados globais em grade de solo, regolito intacto e espessuras de depósitos sedimentares para modelagem regional e global da superfície terrestre. *Jornal de Avanços na Modelagem de Sistemas Terrestres*, 8(1), 41-65.
**Acesso**:- Dados originais: [ORNL DAAC](https://daac.ornl.gov/SOILS/guides/Global_Soil_Regolith_Sediment.html)
- O script usa uma versão pré-processada enviada para Google Earth Engine como um ativo personalizado

**Se DTB não estiver disponível**:- Entre em contato com os autores do script para obter acesso aos ativos
- Use uma profundidade alternativa para o conjunto de dados rochosos
- Comente a Seção 7 se não for necessário para sua aplicação

---

## Código GEE
```javascript
//// ============================================================================
//// HYDROLOGICAL DATABASE EXPORT FOR UNION OF HYDROBASINS
//// Author........: Marcus Nobrega, PhD
//// Stanford University
//// Adapted.......: 2026
//// Purpose.......: Export DEM, LULC, SOIL, DTB, Albedo, LAI, and WorldPop for
////                 the union of multiple HydroBASINS catchments selected by HYBAS_ID.
////                 Also export:
////                   1) a domain summary CSV log
////                   2) a per-catchment CSV log with catchment IDs/attributes/stats
////
//// Notes:
//// - User specifies HydroBASINS level and a list of HYBAS_IDs
//// - Outputs are clipped to the union of selected catchments
//// - Filenames are simplified: DEM, LULC, SOIL, DTB, Albedo, LAI, WorldPop
//// - Summary logs are computed at coarser scale to avoid memory errors
//// ============================================================================


//// ============================================================================
//// SECTION 1: USER INPUTS
//// ============================================================================

// -----------------------------
// HydroBASINS level to use
// Examples: 7, 8, 9, ...
// -----------------------------
var hybasLevel = 6;

// -----------------------------
// List of HYBAS_ID values to merge
// Replace with your own IDs
// -----------------------------
var catchmentIds = [
  4060922650,
  4060953900,
  4060952550,
  4060954060
];


// -----------------------------
// Output folder name in Google Drive
// -----------------------------
var Folder_Name = 'Domain_India';

// -----------------------------
// Export scale (m) for rasters
// -----------------------------
var scale_of_image = 90;

// -----------------------------
// Coarser scales for summary logs
// -----------------------------
var scale_stats_continuous = 250;   // DEM, DTB, Albedo, LAI, Impervious
var scale_stats_categorical = 250;  // LULC, SOIL
var scale_stats_population = 100;   // WorldPop

// -----------------------------
// Date range for time-dependent datasets
// -----------------------------
var startDate = '2015-01-01';
var endDate   = '2020-01-01';

// -----------------------------
// WorldPop year
// Available in EE for 2000–2020
// -----------------------------
var worldpopYear = 2020;

// -----------------------------
// Output CRS
// Recommended for California:
//   EPSG:3310 = California Albers
// -----------------------------
var crs = 'EPSG:3310';

// -----------------------------
var noDataValue = -9999;
var mapZoom = 8;


//// ============================================================================
//// SECTION 2: LOAD HYDROBASINS AND BUILD UNION GEOMETRY
//// ============================================================================

// Build HydroBASINS asset path dynamically
var hybasPath = 'WWF/HydroSHEDS/v1/Basins/hybas_' + hybasLevel;

// Load HydroBASINS
var hybas = ee.FeatureCollection(hybasPath);

// Filter selected catchments
var catchments = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));

// Dissolve into a single feature/geometry
var catchmentUnion = catchments.union(1);

// Alternatively, you can enter the shapefile of your catchment
// Simply change the variable named CatchmentUnion to the catchment you need

var geometry = catchmentUnion.geometry();

// Display
Map.centerObject(catchmentUnion, mapZoom);
Map.addLayer(catchments, {color: 'yellow'}, 'Selected HydroBASINS');
Map.addLayer(catchmentUnion, {color: 'red'}, 'Union Catchment');

// Print basic info
print('HydroBASINS level:', hybasLevel);
print('Selected HYBAS_IDs:', catchmentIds);
print('Selected catchments:', catchments);
print('Union area (km²):', geometry.area(1).divide(1e6));


//// ============================================================================
//// SECTION 3: EXPORT UNION CATCHMENT SHAPEFILE
//// ============================================================================

Export.table.toDrive({
  collection: catchmentUnion,
  description: 'Catchment_Union',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Union',
  fileFormat: 'SHP'
});


//// ============================================================================
//// SECTION 4: DEM
//// Source: MERIT DEM
//// ============================================================================

var MERIT = ee.Image("MERIT/DEM/v1_0_3");
var DEM = MERIT.select('dem').rename('DEM').clip(geometry);

var demVis = {
  min: 0,
  max: 4000,
  palette: ['0000ff', '00ff00', 'ffff00', 'ff7f00', 'ff0000']
};

Map.addLayer(DEM, demVis, 'DEM');

Export.image.toDrive({
  image: DEM.unmask(noDataValue),
  description: 'DEM',
  folder: Folder_Name,
  fileNamePrefix: 'DEM',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 5: LULC
//// Source: ESA/WorldCover/v100/2020
//// ============================================================================

var LULC = ee.Image('ESA/WorldCover/v100/2020')
  .select('Map')
  .rename('LULC')
  .clip(geometry);

var lulcVis = {
  min: 10,
  max: 100,
  palette: [
    '#006400',
    '#ffbb22',
    '#ffff4c',
    '#f096ff',
    '#fa0000',
    '#b4b4b4',
    '#f0f0f0',
    '#0064c8',
    '#0096a0',
    '#00cf75',
    '#fae6a0'
  ]
};

Map.addLayer(LULC, lulcVis, 'LULC');

Export.image.toDrive({
  image: LULC.unmask(noDataValue),
  description: 'LULC',
  folder: Folder_Name,
  fileNamePrefix: 'LULC',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 6: SOIL
//// Source: OpenLandMap USDA texture class
//// ============================================================================

var SOIL = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
  .select('b0')
  .rename('SOIL')
  .clip(geometry);

var soilVis = {
  min: 1,
  max: 12,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(SOIL, soilVis, 'SOIL');

Export.image.toDrive({
  image: SOIL.unmask(noDataValue),
  description: 'SOIL',
  folder: Folder_Name,
  fileNamePrefix: 'SOIL',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 7: DEPTH TO BEDROCK (DTB)
//// Source: custom asset
//// ============================================================================

var DTB = ee.Image("projects/ee-marcusep2025/assets/Depth_to_bedrock")
  .rename('DTB')
  .clip(geometry);

var dtbVis = {
  min: 1,
  max: 50,
  palette: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};

Map.addLayer(DTB, dtbVis, 'DTB');

Export.image.toDrive({
  image: DTB.unmask(noDataValue),
  description: 'DTB',
  folder: Folder_Name,
  fileNamePrefix: 'DTB',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 8: ALBEDO
//// Source: MODIS/061/MCD43A3
//// ============================================================================

var albedoCollection = ee.ImageCollection("MODIS/061/MCD43A3")
  .select('Albedo_BSA_shortwave')
  .filterDate(startDate, endDate);

var Albedo = albedoCollection
  .median()
  .multiply(0.001)
  .rename('Albedo')
  .clip(geometry);

var albedoVis = {
  min: 0,
  max: 0.5,
  palette: ['blue', 'white', 'yellow', 'red']
};

Map.addLayer(Albedo, albedoVis, 'Albedo');

Export.image.toDrive({
  image: Albedo.unmask(noDataValue),
  description: 'Albedo',
  folder: Folder_Name,
  fileNamePrefix: 'Albedo',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 9: LEAF AREA INDEX (LAI)
//// Source: MODIS/061/MCD15A3H
//// Notes:
//// - MODIS LAI scaled by 0.1
//// - Median value over user-defined time range
//// ============================================================================

var laiCollection = ee.ImageCollection('MODIS/061/MCD15A3H')
  .select('Lai')
  .filterDate(startDate, endDate);

var LAI = laiCollection
  .median()
  .multiply(0.1)
  .rename('LAI')
  .clip(geometry);

var laiVis = {
  min: 0,
  max: 6,
  palette: ['red', 'yellow', 'green']
};

Map.addLayer(LAI, laiVis, 'LAI');

Export.image.toDrive({
  image: LAI.unmask(noDataValue),
  description: 'LAI',
  folder: Folder_Name,
  fileNamePrefix: 'LAI',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 10: WORLDPOP
//// Source: WorldPop/GP/100m/pop
//// ============================================================================

var WorldPop = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.calendarRange(worldpopYear, worldpopYear, 'year'))
  .mosaic()
  .rename('WorldPop')
  .clip(geometry);

Map.addLayer(WorldPop, {
  min: 0,
  max: 100,
  palette: ['white', 'yellow', 'orange', 'red', 'darkred']
}, 'WorldPop ' + worldpopYear);

Export.image.toDrive({
  image: WorldPop.unmask(noDataValue),
  description: 'WorldPop',
  folder: Folder_Name,
  fileNamePrefix: 'WorldPop',
  region: geometry,
  scale: scale_of_image,
  crs: crs,
  formatOptions: {noData: noDataValue},
  maxPixels: 1e13
});


//// ============================================================================
//// SECTION 11: IMPERVIOUS RATE (for logs only)
//// Source: NLCD impervious (U.S.-only; appropriate for California)
//// ============================================================================

var Impervious = ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
  .select('impervious')
  .median()
  .rename('Impervious')
  .clip(geometry);

Map.addLayer(Impervious, {
  min: 0,
  max: 100,
  palette: ['white', 'pink', 'red', 'darkred']
}, 'Impervious (%)');


//// ============================================================================
//// SECTION 12: HELPER FUNCTIONS FOR STATS (MEMORY-SAFE)
//// ============================================================================

function reduceMean(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceSum(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function reduceMode(image, geom, scale) {
  var band = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geom,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  return out.get(band);
}

function safeProp(feature, propName) {
  var props = feature.propertyNames();
  return ee.Algorithms.If(props.contains(propName), feature.get(propName), null);
}


//// ============================================================================
//// SECTION 13: DOMAIN SUMMARY LOG (CSV)
//// ============================================================================

var totalPopulation = reduceSum(WorldPop, geometry, scale_stats_population);
var meanImpervious = reduceMean(Impervious, geometry, scale_stats_continuous);
var area_km2 = geometry.area(1).divide(1e6);
var nCatchments = catchments.size();
var dominantLULC = reduceMode(LULC, geometry, scale_stats_categorical);
var dominantSOIL = reduceMode(SOIL, geometry, scale_stats_categorical);
var meanAlbedo = reduceMean(Albedo, geometry, scale_stats_continuous);
var meanElevation = reduceMean(DEM, geometry, scale_stats_continuous);
var meanDTB = reduceMean(DTB, geometry, scale_stats_continuous);
var meanLAI = reduceMean(LAI, geometry, scale_stats_continuous);

// Store catchment IDs as a string for traceability
var catchmentIdsString = ee.List(catchmentIds).join(';');

// Build one-row feature
var domainLogFeature = ee.Feature(null, {
  'folder_name': Folder_Name,
  'hybas_level': hybasLevel,
  'catchment_ids_used': catchmentIdsString,
  'number_of_catchments': nCatchments,
  'catchment_area_km2': area_km2,
  'population_in_domain': totalPopulation,
  'mean_impervious_rate_percent': meanImpervious,
  'dominant_LULC': dominantLULC,
  'dominant_SOIL': dominantSOIL,
  'avg_albedo': meanAlbedo,
  'mean_elevation_m': meanElevation,
  'mean_DTB_m': meanDTB,
  'mean_LAI': meanLAI,
  'worldpop_year': worldpopYear,
  'export_scale_m': scale_of_image,
  'crs': crs
});

var domainLogTable = ee.FeatureCollection([domainLogFeature]);

print('Domain summary log:', domainLogTable);

Export.table.toDrive({
  collection: domainLogTable,
  description: 'Domain_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Domain_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 14: PER-CATCHMENT LOG (CSV)
//// ============================================================================

var catchmentLogTable = catchments.map(function(ft) {
  var g = ft.geometry();
  var areaLocal_km2 = g.area(1).divide(1e6);

  var domLULC_local = reduceMode(LULC, g, scale_stats_categorical);
  var domSOIL_local = reduceMode(SOIL, g, scale_stats_categorical);
  var meanAlb_local = reduceMean(Albedo, g, scale_stats_continuous);
  var meanDEM_local = reduceMean(DEM, g, scale_stats_continuous);
  var meanDTB_local = reduceMean(DTB, g, scale_stats_continuous);
  var meanLAI_local = reduceMean(LAI, g, scale_stats_continuous);
  var pop_local = reduceSum(WorldPop, g, scale_stats_population);
  var imp_local = reduceMean(Impervious, g, scale_stats_continuous);

  return ee.Feature(null, {
    'HYBAS_ID': safeProp(ft, 'HYBAS_ID'),
    'MAIN_BAS': safeProp(ft, 'MAIN_BAS'),
    'NEXT_DOWN': safeProp(ft, 'NEXT_DOWN'),
    'UP_AREA': safeProp(ft, 'UP_AREA'),
    'SUB_AREA': safeProp(ft, 'SUB_AREA'),
    'PFAF_ID': safeProp(ft, 'PFAF_ID'),
    'ENDO': safeProp(ft, 'ENDO'),
    'COAST': safeProp(ft, 'COAST'),
    'catchment_area_km2': areaLocal_km2,
    'population': pop_local,
    'mean_impervious_rate_percent': imp_local,
    'dominant_LULC': domLULC_local,
    'dominant_SOIL': domSOIL_local,
    'avg_albedo': meanAlb_local,
    'mean_elevation_m': meanDEM_local,
    'mean_DTB_m': meanDTB_local,
    'mean_LAI': meanLAI_local
  });
});

print('Per-catchment log:', catchmentLogTable);

Export.table.toDrive({
  collection: catchmentLogTable,
  description: 'Catchment_Log',
  folder: Folder_Name,
  fileNamePrefix: 'Catchment_Log',
  fileFormat: 'CSV'
});


//// ============================================================================
//// SECTION 15: OPTIONAL PRINTED SUMMARY
//// ============================================================================

function computeMeanPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mean:', stats);
}

function computeSumPrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' sum:', stats);
}

function computeModePrint(image, name, scale) {
  var stats = image.reduceRegion({
    reducer: ee.Reducer.mode(),
    geometry: geometry,
    scale: scale,
    maxPixels: 1e13,
    bestEffort: true,
    tileScale: 4
  });
  print(name + ' mode:', stats);
}

computeMeanPrint(DEM, 'DEM', scale_stats_continuous);
computeModePrint(LULC, 'LULC', scale_stats_categorical);
computeModePrint(SOIL, 'SOIL', scale_stats_categorical);
computeMeanPrint(DTB, 'DTB', scale_stats_continuous);
computeMeanPrint(Albedo, 'Albedo', scale_stats_continuous);
computeMeanPrint(LAI, 'LAI', scale_stats_continuous);
computeMeanPrint(Impervious, 'Impervious (%)', scale_stats_continuous);
computeSumPrint(WorldPop, 'Total WorldPop', scale_stats_population);

## GEE Code
```javascript
//// ==========================================================================
//// EXPORTAÇÃO DE BANCO DE DADOS HYDROLOGICAL PARA UNIÃO DE HIDROBACIAS
//// Autor........: Marcus Nóbrega, PhD
//// Universidade Stanford
//// Adaptado.......: 2026
//// Objetivo.......: Exportar DEM, LULC, SOIL, DTB, Albedo, LAI e WorldPop para
//// a união de múltiplas bacias hidrográficas HydroBASINS selecionadas por HYBAS_ID.
//// Exportar também:
//// 1) um log CSV de resumo do domínio
//// 2) um log CSV por bacia hidrográfica com IDs/atributos/estatísticas da bacia hidrográfica
////
//// Notas:
//// - O usuário especifica o nível HydroBASINS e uma lista de HYBAS_IDs
//// - As saídas são cortadas para a união das bacias hidrográficas selecionadas
//// - Os nomes dos arquivos são simplificados: DEM, LULC, SOIL, DTB, Albedo, LAI, WorldPop
//// - Logs de resumo são calculados em escala mais grosseira para evitar erros de memória
//// ==========================================================================

//// ==========================================================================
//// SEÇÃO 1: ENTRADAS DO USUÁRIO
//// ==========================================================================
// -----------------------------
// Nível HydroBASINS a ser usado
// Exemplos: 7, 8, 9, ...
// -----------------------------
var hybasLevel = 6;
// -----------------------------
// Lista de valores HYBAS_ID para mesclar
//Substitua pelos seus próprios IDs
// -----------------------------
var catchmentIds = [
  4060922650,
  4060953900,
  4060952550,
  4060954060
];

// -----------------------------
// Nome da pasta de saída no Google Drive
// -----------------------------
var Folder_Name = 'Domínio_Índia';
// -----------------------------
// Exporta escala (m) para rasters
// -----------------------------
var escala_de_imagem = 90;
// -----------------------------
// Escalas mais grosseiras para logs de resumo
// -----------------------------
var escala_stats_continuo = 250;   // DEM, DTB, Albedo, LAI, Impermeável
var escala_stats_categorical = 250;  // LULC, SOLO
var escala_stats_população = 100;   //WorldPop
// -----------------------------
// Intervalo de datas para conjuntos de dados dependentes de tempo
// -----------------------------
var datainicial = '01-01-2015';
var data final = '2020-01-01';
// -----------------------------
// Ano MundialPop
// Disponível em EE para 2000–2020
// -----------------------------
var mundopopAno = 2020;
// -----------------------------
//Saída CRS
// Recomendado para Califórnia:
// EPSG:3310 = Califórnia Albers
// -----------------------------
var crs = 'EPSG:3310';
// -----------------------------
var noDataValue = -9999;
var mapaZoom = 8;

//// ==========================================================================
//// SEÇÃO 2: CARREGAR HIDROBACIAS E CONSTRUIR GEOMETRIA DE UNIÃO
//// ==========================================================================
// Construa o caminho do ativo HydroBASINS dinamicamente
var hybasPath = 'WWF/HydroSHEDS/v1/Bacias/hybas_' + hybasLevel;
//Carrega HydroBASINS
var hybas = ee.FeatureCollection(hybasPath);
// Filtra as bacias selecionadas
var catchments = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));
// Dissolve-se em um único recurso/geometria
var catchmentUnion = catchments.union(1);
// Alternativamente, você pode inserir o shapefile da sua captação
// Simplesmente altere a variável chamada CatchmentUnion para a área de captação que você precisa
var geometria = catchmentUnion.geometry();
//Exibição
Map.centerObject(catchmentUnion, mapZoom);
Map.addLayer(bacias hidrográficas, {color: 'yellow'}, 'HydroBASINS selecionado');
Map.addLayer(catchmentUnion, {color: 'red'}, 'União Captação');
// Imprime informações básicas
print('Nível HydroBASINS:', hybasLevel);
print('HYBAS_IDs selecionados:', catchmentIds);
print('Captações selecionadas:', bacias hidrográficas);
print('Área de união (km²):', geometria.area(1).divide(1e6));

//// ==========================================================================
//// SEÇÃO 3: EXPORTAR UNIÃO CATCHMENT SHAPEFILE
//// ==========================================================================
Exportar.table.toDrive({
  coleção: captaçãoUnion,
  descrição: 'Catchment_Union',
  pasta: Nome_pasta,
  fileNamePrefix: 'Catchment_Union',
  formato de arquivo: 'SHP'
});

//// ==========================================================================
//// SEÇÃO 4: DEM
//// Fonte: MÉRITO DEM
//// ==========================================================================
var MÉRITO = ee.Image("MÉRITO/DEM/v1_0_3");
var DEM = MERIT.select('dem').rename('DEM').clip(geometria);
var demVis = {
  min: 0,
  máximo: 4000,
  paleta: ['0000ff', '00ff00', 'ffff00', 'ff7f00', 'ff0000']
};
Map.addLayer(DEM, demVis, 'DEM');
Exportar.imagem.toDrive({
  imagem: DEM.unmask(noDataValue),
  descrição: 'DEM',
  pasta: Nome_pasta,
  fileNamePrefix: 'DEM',
  região: geometria,
  escala: escala_de_imagem,
  crs: crs,
  opções de formato: {noData: noDataValue},
  máximoPixels: 1e13
});

//// ==========================================================================
//// SEÇÃO 5: LULC
//// Fonte: ESA/WorldCover/v100/2020
//// ==========================================================================
var LULC = ee.Image('ESA/WorldCover/v100/2020')
  .select('Mapa')
  .renomear('LULC')
  .clip(geometria);
var lulcVis = {
  min: 10,
  máximo: 100,
  paleta: [
    '#006400',
    '#ffbb22',
    '#ffff4c',
    '#f096ff',
    '#fa0000',
    '#b4b4b4',
    '#f0f0f0',
    '#0064c8',
    '#0096a0',
    '#00cf75',
    '#fae6a0'
  ]
};
Map.addLayer(LULC, lulcVis, 'LULC');
Exportar.imagem.toDrive({
  imagem: LULC.unmask(noDataValue),
  descrição: 'LULC',
  pasta: Nome_pasta,
  fileNamePrefix: 'LULC',
  região: geometria,
  escala: escala_de_imagem,
  crs: crs,
  opções de formato: {noData: noDataValue},
  máximoPixels: 1e13
});

//// ==========================================================================
//// SEÇÃO 6: SOLO
//// Fonte: classe de textura OpenLandMap USDA
//// ==========================================================================
var SOIL = ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
  .select('b0')
  .rename('SOLO')
  .clip(geometria);
var soloVis = {
  min: 1,
  máximo: 12,
  paleta: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};
Map.addLayer(SOIL, soloVis, 'SOIL');
Exportar.imagem.toDrive({
  imagem: SOIL.unmask(noDataValue),
  descrição: 'SOLO',
  pasta: Nome_pasta,
  fileNamePrefix: 'SOLO',
  região: geometria,
  escala: escala_de_imagem,
  crs: crs,
  opções de formato: {noData: noDataValue},
  máximoPixels: 1e13
});

//// ==========================================================================
//// SEÇÃO 7: PROFUNDIDADE À ROCHA (DTB)
//// Fonte: ativo personalizado
//// ==========================================================================
var DTB = ee.Image("projetos/ee-marcusep2025/assets/Depth_to_bedrock")
  .renomear('DTB')
  .clip(geometria);
var dtbVis = {
  min: 1,
  máximo: 50,
  paleta: [
    'd5c36b', 'b96947', '9d3706', 'ae868f', 'f86714', '46d143',
    '368f20', '3e5a14', 'ffd557', 'fff72e', 'ff5a9d', 'ff005b'
  ]
};
Map.addLayer(DTB, dtbVis, 'DTB');
Exportar.imagem.toDrive({
  imagem: DTB.unmask(noDataValue),
  descrição: 'DTB',
  pasta: Nome_pasta,
  fileNamePrefix: 'DTB',
  região: geometria,
  escala: escala_de_imagem,
  crs: crs,
  opções de formato: {noData: noDataValue},
  máximoPixels: 1e13
});

//// ==========================================================================
//// SEÇÃO 8: ALBEDO
//// Fonte: MODIS/061/MCD43A3
//// ==========================================================================
var albedoCollection = ee.ImageCollection("MODIS/061/MCD43A3")
  .select('Albedo_BSA_ondas curtas')
  .filterDate(datainicial,datafinal);
var Albedo = albedoCollection
  .mediana()
  .multiplicar (0,001)
  .renome('Albedo')
  .clip(geometria);
var albedoVis = {
  min: 0,
  máximo: 0,5,
  paleta: ['azul', 'branco', 'amarelo', 'vermelho']
};
Map.addLayer(Albedo, albedoVis, 'Albedo');
Exportar.imagem.toDrive({
  imagem: Albedo.unmask(noDataValue),
  descrição: 'Albedo',
  pasta: Nome_pasta,
  fileNamePrefix: 'Albedo',
  região: geometria,
  escala: escala_de_imagem,
  crs: crs,
  opções de formato: {noData: noDataValue},
  máximoPixels: 1e13
});

//// ==========================================================================
//// SEÇÃO 9: ÍNDICE DE ÁREA FOLHA (LAI)
//// Fonte: MODIS/061/MCD15A3H
//// Notas:
//// - MODIS LAI dimensionado em 0,1
//// - Valor mediano no intervalo de tempo definido pelo usuário
//// ==========================================================================
var laiCollection = ee.ImageCollection('MODIS/061/MCD15A3H')
  .select('Lai')
  .filterDate(datainicial,datafinal);
var LAI = laiCollection
  .mediana()
  .multiplicar (0,1)
  .renomear('LAI')
  .clip(geometria);
var laiVis = {
  min: 0,
  máximo: 6,
  paleta: ['vermelho', 'amarelo', 'verde']
};
Map.addLayer(LAI, laiVis, 'LAI');
Exportar.imagem.toDrive({
  imagem: LAI.unmask(noDataValue),
  descrição: 'LAI',
  pasta: Nome_pasta,
  fileNamePrefix: 'LAI',
  região: geometria,
  escala: escala_de_imagem,
  crs: crs,
  opções de formato: {noData: noDataValue},
  máximoPixels: 1e13
});

//// ==========================================================================
//// SEÇÃO 10: WORLDPOP
//// Fonte: WorldPop/GP/100m/pop
//// ==========================================================================
var WorldPop = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.calendarRange(worldpopYear, worldpopYear, 'ano'))
  .mosaico()
  .rename('WorldPop')
  .clip(geometria);
Map.addLayer(WorldPop, {
  min: 0,
  máximo: 100,
  paleta: ['branco', 'amarelo', 'laranja', 'vermelho', 'vermelho escuro']
}, 'WorldPop ' + worldpopYear);
Exportar.imagem.toDrive({
  imagem: WorldPop.unmask(noDataValue),
  descrição: 'WorldPop',
  pasta: Nome_pasta,
  fileNamePrefix: 'WorldPop',
  região: geometria,
  escala: escala_de_imagem,
  crs: crs,
  opções de formato: {noData: noDataValue},
  máximoPixels: 1e13
});

//// ==========================================================================
//// SEÇÃO 11: TAXA IMPERMEÁVEL (somente para toras)
//// Fonte: NLCD impermeável (somente nos EUA; apropriado para a Califórnia)
//// ==========================================================================
var Impermeável = ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
  .select('impermeável')
  .mediana()
  .rename('Impermeável')
  .clip(geometria);
Map.addLayer(Impermeável, {
  min: 0,
  máximo: 100,
  paleta: ['branco', 'rosa', 'vermelho', 'vermelho escuro']
}, 'Impermeável (%)');

//// ==========================================================================
//// SEÇÃO 12: FUNÇÕES AJUDANTES PARA ESTATÍSTICAS (MEMÓRIA SEGURA)
//// ==========================================================================
function reduzMédia(imagem, geom, escala) {
  var banda = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    redutor: ee.Reducer.mean(),
    geometria: geom,
    escala: escala,
    máximoPixels: 1e13,
    melhor esforço: verdadeiro,
    escala de bloco: 4
  });
  retorne out.get(banda);
}
function reduzSoma(imagem, geom, escala) {
  var banda = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    redutor: ee.Reducer.sum(),
    geometria: geom,
    escala: escala,
    máximoPixels: 1e13,
    melhor esforço: verdadeiro,
    escala de bloco: 4
  });
  retorne out.get(banda);
}
function reduzMode(imagem, geom, escala) {
  var banda = ee.String(image.bandNames().get(0));
  var out = image.reduceRegion({
    redutor: ee.Reducer.mode(),
    geometria: geom,
    escala: escala,
    máximoPixels: 1e13,
    melhor esforço: verdadeiro,
    escala de bloco: 4
  });
  retorne out.get(banda);
}
function safeProp(feature, propName) {
  var props = feature.propertyNames();
  return ee.Algorithms.If(props.contains(propName), feature.get(propName), null);
}

//// ==========================================================================
//// SEÇÃO 13: LOG DE RESUMO DO DOMÍNIO (CSV)
//// ==========================================================================
var totalPopulation = reduzSum(WorldPop, geometria, scale_stats_population);
var significaImpermeável = reduzMean(Impermeável, geometria, escala_stats_continuo);
var área_km2 = geometria.area(1).divide(1e6);
var nCatchments = catchments.size();
var dominanteLULC = reduzMode(LULC, geometria, escala_stats_categorical);
var dominanteSOIL = reduzMode(SOIL, geometria, escala_stats_categorical);
var médioAlbedo = reduzMean(Albedo, geometria, escala_stats_continuo);
var médiaElevação = reduzMean(DEM, geometria, escala_stats_continuo);
var médiaDTB = reduzMean(DTB, geometria, escala_stats_continuo);
var médiaLAI = reduzMean(LAI, geometria, escala_stats_continuo);
// Armazena IDs de captação como uma string para rastreabilidade
var catchmentIdsString = ee.List(catchmentIds).join(';');
// Construa recurso de uma linha
var domínioLogFeature = ee.Feature(null, {
  'nome_pasta': nome_pasta,
  'hybas_level': hybasLevel,
  'catchment_ids_used': catchmentIdsString,
  'número_de_captações': nCaptações,
  'captação_area_km2': área_km2,
  'população_no_domínio': população total,
  'mean_impervious_rate_percent': significaImpermeável,
  'dominante_LULC': dominanteLULC,
  'SOIL_dominante': SOIL dominante,
  'avg_albedo': significaAlbedo,
  'média_elevação_m': médiaElevação,
  'média_DTB_m': médiaDTB,
  'média_LAI': médiaLAI,
  'worldpop_year': worldpopYear,
  'export_scale_m': escala_de_imagem,
  'crs': crs
});
var domainLogTable = ee.FeatureCollection([domainLogFeature]);
print('Registro de resumo do domínio:', domainLogTable);
Exportar.table.toDrive({
  coleção: domínioLogTable,
  descrição: 'Domain_Log',
  pasta: Nome_pasta,
  fileNamePrefix: 'Domínio_Log',
  formato de arquivo: 'CSV'
});

//// ==========================================================================
//// SEÇÃO 14: LOG PER-CATCHMENT (CSV)
//// ==========================================================================
var catchmentLogTable = catchments.map(function(ft) {
  var g = ft.geometria();
  var areaLocal_km2 = g.area(1).divide(1e6);
var domLULC_local = reduzMode(LULC, g, escala_stats_categorical);
  var domSOIL_local = reduzMode(SOIL, g, escala_stats_categorical);
  var médioAlb_local = reduzMean(Albedo, g, escala_stats_continuo);
  var médiaDEM_local = reduzMean(DEM, g, escala_stats_continuo);
  var médiaDTB_local = reduzMean(DTB, g, escala_stats_continuo);
  var médiaLAI_local = reduzMean(LAI, g, escala_stats_continuo);
  var pop_local = reduzSum(WorldPop, g, scale_stats_population);
  var imp_local = reduzMean(Impermeável, g, escala_stats_continuo);
retornar ee.Feature(nulo, {
    'HYBAS_ID': safeProp(ft, 'HYBAS_ID'),
    'MAIN_BAS': safeProp(ft, 'MAIN_BAS'),
    'NEXT_DOWN': safeProp(ft, 'NEXT_DOWN'),
    'UP_AREA': safeProp(ft, 'UP_AREA'),
    'SUB_AREA': safeProp(ft, 'SUB_AREA'),
    'PFAF_ID': safeProp(ft, 'PFAF_ID'),
    'ENDO': safeProp(ft, 'ENDO'),
    'COAST': safeProp(ft, 'COAST'),
    'catchment_area_km2': áreaLocal_km2,
    'população': pop_local,
    'mean_impervious_rate_percent': imp_local,
    'dominante_LULC': domLULC_local,
    'dominante_SOIL': domSOIL_local,
    'avg_albedo':meanAlb_local,
    'média_elevação_m': médiaDEM_local,
    'média_DTB_m': médiaDTB_local,
    'média_LAI': médiaLAI_local
  });
});
print('Registro por captação:', catchmentLogTable);
Exportar.table.toDrive({
  coleção: catchmentLogTable,
  descrição: 'Catchment_Log',
  pasta: Nome_pasta,
  fileNamePrefix: 'Catchment_Log',
  formato de arquivo: 'CSV'
});

//// ==========================================================================
//// SEÇÃO 15: RESUMO IMPRESSO OPCIONAL
//// ==========================================================================
function computaMeanPrint(imagem, nome, escala) {
  var estatísticas = imagem.reduceRegion({
    redutor: ee.Reducer.mean(),
    geometria: geometria,
    escala: escala,
    máximoPixels: 1e13,
    melhor esforço: verdadeiro,
    escala de bloco: 4
  });
  print(nome + 'meio:', estatísticas);
}
function computaSumPrint(imagem, nome, escala) {
  var estatísticas = imagem.reduceRegion({
    redutor: ee.Reducer.sum(),
    geometria: geometria,
    escala: escala,
    máximoPixels: 1e13,
    melhor esforço: verdadeiro,
    escala de bloco: 4
  });
  print(nome + 'soma:', estatísticas);
}
function computaModePrint(imagem, nome, escala) {
  var estatísticas = imagem.reduceRegion({
    redutor: ee.Reducer.mode(),
    geometria: geometria,
    escala: escala,
    máximoPixels: 1e13,
    melhor esforço: verdadeiro,
    escala de bloco: 4
  });
  print(nome + 'modo:', estatísticas);
}
computaMeanPrint(DEM, 'DEM', escala_stats_continuo);
computaModePrint(LULC, 'LULC', escala_stats_categorical);
computaModePrint(SOIL, 'SOIL', scale_stats_categorical);
computaMeanPrint(DTB, 'DTB', escala_stats_continuo);
computaMeanPrint(Albedo, 'Albedo', escala_stats_continuo);
computaMeanPrint(LAI, 'LAI', escala_stats_continuo);
computaMeanPrint(Impermeável, 'Impermeável (%)', scale_stats_continuous);
computaSumPrint(WorldPop, 'Total WorldPop', scale_stats_population);