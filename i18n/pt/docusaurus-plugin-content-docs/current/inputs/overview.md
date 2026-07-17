---
title: Visao geral
---

# Entradas do modelo

O HydroPol2D usa uma combinacao de rasters, planilhas de parametros e arquivos de forcantes. Esta pagina e o ponto de entrada para os arquivos que o modelo atual consegue ler.

## Entradas espaciais principais

A maioria das simulacoes comeca com tres rasters obrigatorios:

1. [DEM](./dem)
2. [LULC](./lulc)
3. [Soil](./soil)

Eles definem a grade do modelo, as classes de uso e cobertura da terra e as propriedades hidraulicas basicas do solo.

## Entradas espaciais suplementares

Outros rasters podem ser usados quando o fluxo de trabalho precisa deles:

- [DTB](./dtb) para profundidade do solo ou profundidade ate o embasamento;
- [LAI](./lai) para estrutura espacial da vegetacao;
- [Albedo](./albedo) para propriedades espaciais de energia na superficie;
- [Additional Spatial Inputs](./additional-spatial-inputs) para groundwater inicial, fracao impermeavel, estados de warmup e rasters de qualidade da agua.

Essas entradas sao opcionais por caso de uso, nao experimentais por definicao. Sempre que estiverem ativas em um estudo de caso, isso deve ser documentado.

## Entradas tabulares e de controle

O HydroPol2D tambem le planilhas:

- [Parameter Tables](./parameter-tables) para classes de LULC e solo;
- `General_Data.xlsx` para flags, tempo de simulacao, caminhos de arquivos e controles de execucao;
- planilhas de forcantes ou condicoes de contorno para chuva, evapotranspiracao, inflow, stage ou estruturas de controle, quando essas opcoes estiverem ativas.

## Entradas de forcantes

As forcantes podem ser prescritas por planilhas, agendas de rasters ou tempestades sinteticas. A pagina [Optional Forcing](./optional-forcing) documenta os caminhos suportados, incluindo series temporais de chuva, rasters de chuva, forcantes de evapotranspiracao, hidrográficas de entrada, contornos de nivel e tempestades de projeto.

## Regras praticas

Os rasters devem:

- usar um sistema de coordenadas projetado;
- estar alinhados ao DEM, ou ser reamostraveis para essa grade;
- usar unidades consistentes;
- cobrir o dominio do modelo de forma limpa.

O HydroPol2D consegue reamostrar e mascarar muitos rasters opcionais internamente, mas fluxos de trabalho reprodutiveis ainda dependem de arquivos de origem limpos e consistentes com o dominio.

## Mapa rapido de entradas

| Grupo de entrada | Arquivos tipicos |
|---|---|
| Terreno e classes principais | `DEM_path`, `LULC_path`, `SOIL_path` |
| Apoio da zona vadosa e groundwater | `DTB_path`, `GW_table_path` |
| Refinamentos de propriedade superficial | `LAI_path`, `Albedo_path`, `ImperviousFraction_path` |
| Estados iniciais | `Warmup_Depth_path`, `Initial_Soil_Moisture_path`, `Initial_Buildup_path` |
| Geometria do canal | `RiverWidths_path`, `RiverDepths_path` |
| Rasters de qualidade da agua | `B1_path`, `B2_path`, `W1_path`, `W2_path` |
| Forcantes e arquivos de contorno | planilhas ou agendas raster de chuva, ETP, inflow, stage e estruturas de controle |

O comportamento detalhado dos rasters suplementares e dos estados iniciais esta documentado em [Additional Spatial Inputs](./additional-spatial-inputs).
