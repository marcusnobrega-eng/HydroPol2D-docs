---
title: GPM IMERG Extração de dados de precipitação
---

# Baixando GPM IMERG Chuva com Google Earth Engine

Este script autônomo Google Earth Engine (GEE) automatiza a extração de dados de precipitação de satélite de alta resolução do conjunto de dados NASA GPM (Medição de Precipitação Global) IMERG para qualquer bacia hidrográfica em todo o mundo.
O fluxo de trabalho gera rasters GeoTIFF individuais para cada intervalo de tempo, prontos para modelagem hidrológica com HydroPol2D ou outros modelos distribuídos.

---

## O que o fluxo de trabalho faz

O script baixa dados de precipitação de **GPM IMERG V07** (Integrated Multi-satellitE Retrievals for GPM), o produto de precipitação global de última geração do NASA que combina observações de vários sensores de satélite.
### Principais recursos

- **Resolução nativa de 30 minutos**: Captura a variabilidade da precipitação sub-horária, crucial para a modelagem de inundações repentinas
- **Cobertura global**: 60°N-60°S (cobre as regiões mais populosas do mundo)
- **Resolução espacial de 0,1°**: Aproximadamente 11 km no equador
- **Registro longo**: junho de 2000 quase em tempo real (atualizado com atraso de aproximadamente 3 meses)
- **Dados calibrados**: usa estimativas de precipitação ajustadas pelo medidor
- **Várias resoluções temporais**: agregar por hora, 3 horas, 6 horas ou diariamente
- **Entrada de captação flexível**: Funciona com HydroBASINS ou shapefiles personalizados

---

## Especificações de saída

### Propriedades rasterizadas

| Propriedade | Valor |
|----------|-------|
| **Resolução** | 0,1° × 0,1° (aproximadamente 11 km no equador) |
| **Unidades** | mm/h (taxa de precipitação) |
| **Formatar** | GeoTIFF |
| **Sistema de Coordenadas** | EPSG:4326 (WGS84) por padrão |
| **Sem valor de dados** | -9999 |
| **Região de exportação** | Caixa delimitadora de captação |

### Convenção de nome de arquivo

O script gera nomes de arquivos descritivos que codificam informações temporais:

**Dados de 30 minutos**:
- GPM_30min_2023_01_14_00_00.tif
- GPM_30min_2023_01_14_00_30.tif
- GPM_30min_2023_01_14_01_00.tif

**Agregação por hora**:
- GPM_60min_2023_01_14_00_00.tif
- GPM_60min_2023_01_14_01_00.tif
- GPM_60min_2023_01_14_02_00.tif

**Agregação de 3 horas** (mesma resolução temporal do MSWEP):
- GPM_180min_2023_01_14_00_00.tif
- GPM_180min_2023_01_14_03_00.tif
- GPM_180min_2023_01_14_06_00.tif

**Agregação diária**:
- GPM_1440min_2023_01_14_00_00.tif
- GPM_1440min_2023_01_15_00_00.tif
- GPM_1440min_2023_01_16_00_00.tif

---

## Como usar o script

### Passo 1: Defina sua área de estudo

**Opção A - Usando HydroBASINS** (recomendado para a maioria dos usuários)

Modifique estes parâmetros no script:
- Defina useHydroBASINS como verdadeiro
- Escolha o nível HydroBASINS (1-12, onde maior é igual a bacias hidrográficas menores)
- Insira seus IDs de captação na lista catchmentIds

Recomendações de nível:
- Nível 5-6: Grandes bacias hidrográficas (maiores que 10,000 km²)
- Nível 7: Captações médias (1.000-5,000 km²)
- Nível 8-9: Pequenas bacias hidrográficas (100-1,000 km²)

**Encontrando seu HYBAS_ID**:
1. Visite o site HydroSHEDS ou use a ferramenta Inspector do GEE
2. Carregue HydroBASINS no nível desejado em Google Earth Engine
3. Clique na sua captação com a ferramenta Inspetor
4. Copie o valor HYBAS_ID

**Opção B - Usando Shapefile Personalizado**

Se você tiver seu próprio shapefile de captação:
1. Carregar shapefile para ativos GEE (Ativo → Novo → Arquivos de forma)
2. Defina useHydroBASINS como false no script
3. Remova o comentário e modifique a linha customCatchment com o caminho do seu ativo

---

### Etapa 2: definir intervalo de datas

Especifique o evento de chuva ou período de estudo que deseja baixar.
**Formato**: AAAA-MM-DD

**Notas importantes**:
- GPM IMERG V07 disponível de **1º de junho de 2000** até quase em tempo real
- Normalmente há um atraso de 3 meses para o produto final
- Para eventos curtos (dias a semanas): use resolução de 30 minutos
- Por longos períodos (meses a anos): considere resoluções agregadas

**Exemplos de configurações**:
- **Evento de inundação repentina**: 2 a 3 dias com resolução de 30 minutos
- **Simulação mensal**: 30 dias com resolução horária ou 3 horas
- **Análise sazonal**: 90 dias com resolução de 3 horas ou diária
- **Balanço hídrico anual**: 365 dias na resolução diária

---

### Etapa 3: escolha a resolução temporal

Selecione o intervalo de tempo (em minutos) para seus resultados de precipitação.
| Resolução | Minutos | Arquivos por dia | Caso de uso típico |
|------------|---------|---------------|------------------|
| **30 minutos** | 30 | 48 | Inundações repentinas, drenagem urbana, tempestades curtas |
| **Por hora** | 60 | 24 | Modelagem baseada em eventos, análise detalhada de tempestades |
| **3 horas** | 180 | 8 | Eventos de vários dias, simulações de médio prazo |
| **6 horas** | 360 | 4 | Simulações semanais a mensais |
| **12 horas** | 720 | 2 | Análise climática de longo prazo |
| **Diário** | 1440 | 1 | Balanço hídrico, análise sazonal/anual |

**Exemplos de contagem de arquivos**:
- Evento de 2 dias com 30 minutos: 96 arquivos (aproximadamente 200 MB)
- 1 mês por hora: 720 arquivos (aproximadamente 1,5 GB)
- 1 mês a cada 3 horas: 240 arquivos (aproximadamente 500 MB)
- 1 ano diariamente: 365 arquivos (aproximadamente 750 MB)

**Método de agregação**: para resoluções temporais superiores a 30 minutos, o script calcula a **taxa média de precipitação** durante o período de agregação, preservando as unidades mm/h.

---

### Etapa 4: definir as configurações de saída

**Pasta de saída**: Especifique o nome da pasta do Google Drive onde os arquivos serão salvos. O script criará esta pasta se ela não existir.
**Sistema de coordenadas**: mantenha como EPSG:4326 (WGS84) para projeção nativa GPM ou especifique uma projeção local (por exemplo, zonas UTM, plano estadual) para sua região.

Projeções comuns:
- EPSG:4326 - WGS84 (global, recomendado para GPM)
- EPSG:3310 - Califórnia Albers
- EPSG:32610 - UTM Zona 10N (Califórnia)
- EPSG:32643 - UTM Zona 43N (Índia)

---

### Etapa 5: execute o script

1. **Copie o script completo** da seção de código abaixo
2. **Abra Google Earth Engine** Editor de código
3. **Cole o script** em um novo arquivo de script
4. **Modifique as entradas do usuário** (Seção 1)
5. **Execute o script** (clique no botão Executar ou pressione Ctrl+Enter)
6. **Aguarde o processamento** - O console mostrará o progresso
7. **Vá para a guia Tarefas** (painel direito)
8. **Clique em EXECUTAR** em cada tarefa de exportação
9. **Aguarde a conclusão das exportações** - Os arquivos aparecem no Google Drive

**Tempo de processamento**:
- Envio de tarefas: 10-30 segundos
- Exportação por arquivo: 1 a 5 minutos (depende do tamanho da área de captação)
- Tempo total: varia com o número de arquivos

---

## Compreendendo as saídas

### Caixa delimitadora vs captação exata

O script exporta dados de precipitação para a **caixa delimitadora retangular** ao redor da sua bacia hidrográfica, não para o formato exato da bacia hidrográfica.

**Por que?**
- Processamento mais rápido
- Mantém a estrutura de grade regular do GPM
- Fornece contexto para áreas adjacentes
- HydroPol2D e a maioria dos modelos hidrológicos podem ser cortados em limites exatos durante o processamento

**Se você precisar de um recorte exato da área de captação**: O shapefile da área de captação exportado pode ser usado para recortar rasters no software GIS ou durante o pré-processamento do modelo.

---

### Arquivos incluídos na exportação

**Rasters de precipitação**:
- Um GeoTIFF por intervalo de tempo
- O nome do arquivo inclui data e hora
- Unidades: mm/h (taxa de precipitação)

**Limite da bacia hidrográfica**:
- Shapefile (.shp + arquivos de suporte)
- Mesmo sistema de coordenadas dos rasters de chuva
- Use para recorte ou visualização

---

### Garantia de qualidade

O script inclui camadas de visualização no mapa:
- **Polígono vermelho**: Limite de captação mesclado
- **Retângulo azul**: caixa delimitadora de exportação
- **Exemplo de camada de chuva**: visualização da primeira etapa
- **Camada total de chuvas**: Precipitação acumulada durante todo o período

**Saídas do console**:
- Área de captação em quilômetros quadrados
- Número de imagens de 30 minutos disponíveis
- Confirmação do período
- Exportar status de envio de tarefa
- Estatísticas totais de precipitação

---

## Considerações sobre dados

### GPM IMERG Pontos fortes

- **Alta resolução temporal**: observações de 30 minutos
- **Cobertura global**: dados consistentes em todo o mundo
- **Registro longo**: mais de 20 anos de dados
- **Calibração de medidores**: precisão aprimorada em regiões com redes de pluviômetros
- **Fusão multisensor**: combina dados passivos de micro-ondas, infravermelho e radar

### Limitações GPM IMERG

- **Resolução espacial**: 11 km podem ser grosseiros para pequenas bacias hidrográficas (menos de 100 quilômetros quadrados)
- **Latência**: atraso de aproximadamente 3 meses para o produto final calibrado (V07)
- **Incerteza**: Menor precisão em oceanos, montanhas e neve/gelo
- **Viés**: pode subestimar ou superestimar em certas regiões (especialmente em terrenos complexos)
- **Lacunas de cobertura**: somente 60°N-60°S (sem regiões polares)

### Recomendações de validação

**Sempre valide GPM em relação às observações locais, quando disponíveis**:
- Compare com os dados do pluviômetro
- Verifique as estimativas do radar
- Verifique os acúmulos totais
- Avalie padrões espaciais

Para aplicações críticas, considere:
- Correção de polarização usando dados de medidor local
- Abordagens de conjunto com vários conjuntos de dados
- Quantificação da incerteza

---

## Aplicativos

Este fluxo de trabalho foi projetado para:
### Modelagem Hidrológica
- Simulação distribuída de chuva-escoamento HydroPol2D
- Previsão de inundações repentinas
- Análise de drenagem urbana
- Estudos de equilíbrio hídrico

### Análise de Eventos
- Caracterização da tempestade
- Análise intensidade-duração-frequência de chuva
- Reconstrução de eventos extremos
- Análise histórica de eventos de inundação

### Estudos Climáticos
- Tendências de precipitação a longo prazo
- Padrões sazonais de chuva
- Monitoramento de seca
- Validação do modelo climático

### Recursos hídricos
- Estimativa de vazão do reservatório
- Planejamento de irrigação
- Avaliação de energia hidrelétrica
- Estudos de disponibilidade de água

---

## Solução de problemas

### Problemas comuns

**Erro "Capacidade de memória excedida"**:
- Reduza o intervalo de datas (tente períodos menores)
- Aumente a resolução temporal (por exemplo, use diariamente em vez de 30 minutos)
- Reduzir o tamanho da captação (use um nível menor de HydroBASINS)

**Nenhum dado em rasters exportados**:
- Verifique se o intervalo de datas está dentro do período GPM (01/06/2000 em diante)
- Verifique se a captação está dentro da cobertura GPM (60°N-60°S)
- Confirme se o ID da área de captação está correto

**Exportações não aparecem em Tarefas**:
- Aguarde 10 a 30 segundos após executar o script
- Verifique o console em busca de mensagens de erro
- Guia Atualizar Tarefas

**Tamanhos de arquivo muito grandes**:
- Considere usar resolução temporal agregada
- Exportar intervalos de datas menores
- Use resolução espacial apropriada para sua aplicação

---

## Recursos Adicionais

- [Site da Missão GPM](https://gpm.nasa.gov/)
- [GPM Documentação técnica IMERG](https://gpm.nasa.gov/data/imerg)
- [Documentação Google Earth Engine](https://developers.google.com/earth-engine)
- [Banco de dados HydroBASINS](https://www.hydrosheds.org/products/hydrobasins)
- [Modelo HydroPol2D](https://marcusnobrega-eng.github.io/HydroPol2D-docs/)

---

## Apoiar

Para problemas com:
- **O script**: entre em contato com sua equipe de suporte
- **Dados GPM**: Visite o suporte técnico GES DISC ou GPM
- **Google Earth Engine**: Verifique o fórum de desenvolvedores do GEE
- **HydroPol2D**: Visite o site de documentação do modelo

---

## Histórico de versões

- **v1.0** (2026): lançamento inicial com suporte para GPM IMERG V07
  - Resoluções temporais de 30 minutos a diárias
  - HydroBASINS e suporte a shapefile personalizado
  - Geração automática de tarefas
  - Visualizações de garantia de qualidade

---

## Código GEE
```javascript
//// ============================================================================
//// GPM IMERG V07 RAINFALL DOWNLOADER - STANDALONE
//// Author........: Marcus Nobrega
//// Date..........: 2026
//// Purpose.......: Download GPM IMERG V07 rainfall data for any catchment
//// Resolution....: 0.1° × 0.1° (native, ~11 km at equator)
//// Units.........: mm/h (precipitation rate)
//// Data Range....: June 2000 - Present (near real-time)
//// ============================================================================


//// ============================================================================
//// SECTION 1: USER INPUTS - MODIFY THESE PARAMETERS
//// ============================================================================

// =============================================================================
// OPTION 1: Use HydroBASINS Catchment
// =============================================================================
// HydroBASINS level: 1-12 (higher = smaller catchments)
// Level 7 = medium-sized catchments (~1000-5000 km²)
// Level 8 = smaller catchments (~200-1000 km²)
var useHydroBASINS = true;  // Set to true to use HydroBASINS
var hybasLevel = 7;         // HydroBASINS level (1-12)

// List of HYBAS_ID values to download rainfall for
// You can find HYBAS_IDs by:
// 1. Going to: https://www.hydrosheds.org/hydrobasins
// 2. Or using the Inspector tool in GEE to click on catchments
var catchmentIds = [
  7071457620  // Example: San Francisco Bay Area catchment
];

// =============================================================================
// OPTION 2: Use Your Own Shapefile (uploaded to GEE Assets)
// =============================================================================
// Uncomment the line below and comment out the HydroBASINS section if using custom shapefile
// var useHydroBASINS = false;
// var customCatchment = ee.FeatureCollection('users/yourusername/your_catchment_shapefile');

// =============================================================================
// Date Range for Rainfall Download
// =============================================================================
// Format: 'YYYY-MM-DD'
// GPM IMERG V07 available from: 2000-06-01 to near real-time
var gpmStartDate = '2023-01-01';  // Start date
var gpmEndDate   = '2023-01-31';  // End date

// =============================================================================
// Temporal Resolution (in minutes)
// =============================================================================
// Choose ONE of the following options:
//   30    = Native 30-minute resolution (best for short periods: days/weeks)
//   60    = Hourly (good for weeks/months)
//   180   = 3-hourly (same as MSWEP, good for months)
//   360   = 6-hourly (good for long periods)
//   720   = 12-hourly
//   1440  = Daily (good for years)
var gpmTemporalResolution = 360;  // Minutes

// =============================================================================
// Output Settings
// =============================================================================
// Google Drive folder name where files will be saved
var outputFolder = 'GPM_SanFrancisco';

// Coordinate Reference System (CRS)
// Recommended: Keep as 'EPSG:4326' (WGS84 lat/lon) for GPM data
// For local projections, use appropriate EPSG code (e.g., 'EPSG:32610' for UTM Zone 10N California)
var outputCRS = 'EPSG:4326';

// No data value for exported rasters
var noDataValue = -9999;

// =============================================================================
// Visualization Settings
// =============================================================================
var mapZoom = 9;  // Initial map zoom level


//// ============================================================================
//// SECTION 2: LOAD CATCHMENT GEOMETRY
//// ============================================================================

var catchmentUnion;
var geometry;

if (useHydroBASINS) {
  // Build HydroBASINS asset path
  var hybasPath = 'WWF/HydroSHEDS/v1/Basins/hybas_' + hybasLevel;

  // Load HydroBASINS and filter by HYBAS_ID
  var hybas = ee.FeatureCollection(hybasPath);
  var catchments = hybas.filter(ee.Filter.inList('HYBAS_ID', catchmentIds));

  // Dissolve into single geometry
  catchmentUnion = catchments.union(1);
  geometry = catchmentUnion.geometry();

  print('Using HydroBASINS Level:', hybasLevel);
  print('Selected HYBAS_IDs:', catchmentIds);
  print('Number of catchments:', catchments.size());

} else {
  // Use custom shapefile
  catchmentUnion = customCatchment;
  geometry = catchmentUnion.geometry();

  print('Using custom catchment shapefile');
}

// Create bounding box for export (not clipped - for HydroPol2D compatibility)
var bounds = geometry.bounds();

// Display on map
Map.centerObject(geometry, mapZoom);
Map.addLayer(geometry, {color: 'red'}, 'Catchment');
Map.addLayer(bounds, {color: 'blue'}, 'Export Bounds');

// Print catchment info
print('============================================');
print('CATCHMENT INFORMATION');
print('============================================');
print('Catchment area (km²):', geometry.area(1).divide(1e6));
print('Export bounds:', bounds.coordinates());


//// ============================================================================
//// SECTION 3: LOAD GPM IMERG V07 RAINFALL DATA
//// ============================================================================

print('============================================');
print('GPM IMERG V07 CONFIGURATION');
print('============================================');
print('Date range:', gpmStartDate, 'to', gpmEndDate);
print('Temporal resolution:', gpmTemporalResolution, 'minutes');

// Load GPM IMERG V07 collection
// The 'precipitation' band contains calibrated precipitation rate in mm/h
var gpmCollection = ee.ImageCollection('NASA/GPM_L3/IMERG_V07')
  .select('precipitation')
  .filterDate(gpmStartDate, gpmEndDate)
  .filterBounds(bounds);

print('Total 30-min images available:', gpmCollection.size());

// Native GPM resolution: 0.1 degree ≈ 11132 meters at equator
var gpmNativeScale = 11132;


//// ============================================================================
//// SECTION 4: EXPORT RAINFALL RASTERS
//// ============================================================================

// -----------------------------
// OPTION A: Native 30-minute resolution
// -----------------------------
if (gpmTemporalResolution === 30) {

  print('============================================');
  print('EXPORTING 30-MINUTE RAINFALL');
  print('============================================');
  print('Units: mm/h (precipitation rate)');
  print('Resolution: 0.1° (~11 km)');
  print('Filename format: GPM_30min_yyyy_mm_dd_hh_mm.tif');
  print('Output folder:', outputFolder);

  // Get collection as list
  var gpmList = gpmCollection.toList(gpmCollection.size());
  var numImages = gpmCollection.size();

  // Create export tasks for each image
  numImages.evaluate(function(n) {
    print('Creating', n, 'export tasks...');

    for (var i = 0; i < n; i++) {
      (function(index) {
        var img = ee.Image(gpmList.get(index));
        var date = ee.Date(img.get('system:time_start'));

        // Format date as yyyy_mm_dd_hh_mm
        date.format('yyyy_MM_dd_HH_mm').evaluate(function(dateStr) {
          var exportName = 'GPM_30min_' + dateStr;

          Export.image.toDrive({
            image: img.unmask(noDataValue).float(),
            description: exportName,
            folder: outputFolder,
            fileNamePrefix: exportName,
            region: bounds,
            scale: gpmNativeScale,
            crs: outputCRS,
            formatOptions: {noData: noDataValue},
            maxPixels: 1e13
          });
        });
      })(i);
    }

    print('✓ All export tasks submitted!');
    print('✓ Go to Tasks tab (right panel) to run exports');
    print('✓ Each file contains precipitation rate in mm/h');
  });

}

// -----------------------------
// OPTION B: Aggregated temporal resolution
// -----------------------------
else {

  print('============================================');
  print('EXPORTING', gpmTemporalResolution, 'MINUTE RAINFALL');
  print('============================================');
  print('Units: mm/h (mean precipitation rate)');
  print('Resolution: 0.1° (~11 km)');

  var resStr = gpmTemporalResolution.toString();
  print('Filename format: GPM_' + resStr + 'min_yyyy_mm_dd_hh_mm.tif');
  print('Output folder:', outputFolder);

  // Calculate aggregation parameters
  var intervalsPerPeriod = gpmTemporalResolution / 30;
  print('30-min intervals per output:', intervalsPerPeriod);

  // Time period calculations
  var startMillis = ee.Date(gpmStartDate).millis();
  var endMillis = ee.Date(gpmEndDate).millis();
  var millisPerPeriod = gpmTemporalResolution * 60 * 1000;
  var numPeriods = endMillis.subtract(startMillis).divide(millisPerPeriod).floor();

  var periods = ee.List.sequence(0, numPeriods.subtract(1));

  // Create aggregated collection
  var aggregatedCollection = ee.ImageCollection(periods.map(function(p) {
    var periodStart = ee.Date(startMillis.add(ee.Number(p).multiply(millisPerPeriod)));
    var periodEnd = periodStart.advance(gpmTemporalResolution, 'minute');

    var periodImages = gpmCollection.filterDate(periodStart, periodEnd);

    // Mean precipitation rate over period (still in mm/h)
    var aggregated = periodImages
      .mean()
      .rename('precipitation')
      .set('system:time_start', periodStart.millis())
      .set('period_start', periodStart.format('yyyy-MM-dd HH:mm'))
      .set('period_end', periodEnd.format('yyyy-MM-dd HH:mm'))
      .set('temporal_resolution_min', gpmTemporalResolution)
      .set('units', 'mm/h');

    return aggregated;
  }));

  print('Number of aggregated images:', aggregatedCollection.size());

  // Get collection as list
  var aggList = aggregatedCollection.toList(aggregatedCollection.size());
  var numAggImages = aggregatedCollection.size();

  // Create export tasks for each aggregated image
  numAggImages.evaluate(function(n) {
    print('Creating', n, 'export tasks...');

    for (var i = 0; i < n; i++) {
      (function(index) {
        var img = ee.Image(aggList.get(index));
        var date = ee.Date(img.get('system:time_start'));

        // Format date as yyyy_mm_dd_hh_mm
        date.format('yyyy_MM_dd_HH_mm').evaluate(function(dateStr) {
          var exportName = 'GPM_' + resStr + 'min_' + dateStr;

          Export.image.toDrive({
            image: img.unmask(noDataValue).float(),
            description: exportName,
            folder: outputFolder,
            fileNamePrefix: exportName,
            region: bounds,
            scale: gpmNativeScale,
            crs: outputCRS,
            formatOptions: {noData: noDataValue},
            maxPixels: 1e13
          });
        });
      })(i);
    }

    print('✓ All export tasks submitted!');
    print('✓ Go to Tasks tab (right panel) to run exports');
    print('✓ Each file contains mean precipitation rate in mm/h');
  });
}


//// ============================================================================
//// SECTION 5: VISUALIZATION
//// ============================================================================

// Visualize first rainfall image
var sampleGPM = ee.Image(gpmCollection.first());

Map.addLayer(sampleGPM, {
  min: 0,
  max: 10,
  palette: ['white', 'lightblue', 'blue', 'darkblue', 'purple', 'red']
}, 'Sample Rainfall (mm/h)');

// Calculate and visualize total rainfall over period
var totalRainfall = gpmCollection.sum().multiply(0.5);  // mm (30-min * mm/h = mm/0.5hr)

Map.addLayer(totalRainfall.clip(geometry), {
  min: 0,
  max: 200,
  palette: ['white', 'lightblue', 'blue', 'darkblue', 'purple', 'red']
}, 'Total Rainfall (mm)');

// Print statistics
print('============================================');
print('RAINFALL STATISTICS');
print('============================================');
print('Sample image date:', ee.Date(sampleGPM.get('system:time_start')));

var stats = totalRainfall.reduceRegion({
  reducer: ee.Reducer.minMax().combine(ee.Reducer.mean(), '', true),
  geometry: geometry,
  scale: gpmNativeScale,
  maxPixels: 1e13,
  bestEffort: true
});

print('Total rainfall over period (mm):', stats);


//// ============================================================================
//// SECTION 6: EXPORT CATCHMENT BOUNDARY
//// ============================================================================

// Export catchment shapefile for reference
Export.table.toDrive({
  collection: catchmentUnion,
  description: 'Catchment_Boundary',
  folder: outputFolder,
  fileNamePrefix: 'Catchment_Boundary',
  fileFormat: 'SHP'
});

print('============================================');
print('EXPORT SUMMARY');
print('============================================');
print('✓ Rainfall rasters configured for export');
print('✓ Catchment boundary shapefile configured');
print('✓ Go to Tasks tab to start downloads');
print('============================================');