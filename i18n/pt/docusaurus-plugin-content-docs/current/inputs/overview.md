---
title: Visão geral
---

# Entradas do modelo

O HydroPol2D usa uma combinação de rasters, planilhas de parâmetros e arquivos de forçantes. Esta página é o ponto de entrada para os arquivos que o modelo atual consegue ler.

## Entradas espaciais principais

A maioria das simulações começa com três rasters obrigatórios:

1. [DEM](./dem)
2. [LULC](./lulc)
3. [Soil](./soil)

Eles definem a grade do modelo, as classes de uso e cobertura da terra e as propriedades hidráulicas básicas do solo.

## Entradas espaciais suplementares

Outros rasters podem ser usados quando o fluxo de trabalho precisa deles:

- [DTB](./dtb) para profundidade do solo ou profundidade até o embasamento;
- [LAI](./lai) para estrutura espacial da vegetação;
- [Albedo](./albedo) para propriedades espaciais de energia na superfície;
- [Additional Spatial Inputs](./additional-spatial-inputs) para groundwater inicial, fração impermeável, estados de warmup e rasters de qualidade da água.

Essas entradas são opcionais por caso de uso, não experimentais por definição. Sempre que estiverem ativas em um estudo de caso, isso deve ser documentado.

## Entradas tabulares e de controle

O HydroPol2D também lê planilhas:

- [Parameter Tables](./parameter-tables) para classes de LULC, solo e neve;
- `General_Data.xlsx` para flags, tempo de simulação, caminhos de arquivos e controles de execução;
- planilhas de forçantes ou condições de contorno para chuva, evapotranspiração, inflow, stage ou estruturas de controle, quando essas opções estiverem ativas.

## Entradas de forçantes

As forçantes podem ser prescritas por planilhas, agendas de rasters ou tempestades sintéticas. A página [Optional Forcing](./optional-forcing) documenta os caminhos suportados, incluindo séries temporais de chuva, rasters de chuva, forçantes de evapotranspiração, hidrográficas de entrada, contornos de nível e tempestades de projeto.

## Regras práticas

Os rasters devem:

- usar um sistema de coordenadas projetado;
- estar alinhados ao DEM, ou ser reamostráveis para essa grade;
- usar unidades consistentes;
- cobrir o domínio do modelo de forma limpa.

O HydroPol2D consegue reamostrar e mascarar muitos rasters opcionais internamente, mas fluxos de trabalho reprodutíveis ainda dependem de arquivos de origem limpos e consistentes com o domínio.

## Mapa rápido de entradas

| Grupo de entrada | Arquivos típicos |
|---|---|
| Terreno e classes principais | `DEM_path`, `LULC_path`, `SOIL_path` |
| Apoio da zona vadosa e groundwater | `DTB_path`, `GW_table_path` |
| Subsuperfície em camadas (opcional) | `SoilBaseDepth_path`, `RegolithThetaS_path`, `RegolithThetaR_path`, `RegolithAlphaVG_path`, `RegolithNVG_path`, `RegolithKsatV_path`, `RegolithKsatH_path`, `RegolithSpecificYield_path` |
| Aquífero profundo (opcional) | `DeepAquiferSubbasins_path`, `DeepAquiferChannelWeight_path`, `DeepAquiferInitialState_path` |
| Refinamentos de propriedade superficial | `LAI_path`, `Albedo_path`, `ImperviousFraction_path` |
| Estados iniciais | `Warmup_Depth_path`, `Initial_Soil_Moisture_path`, `Initial_SWE_path`, `Initial_Snow_Depth_path`, `Initial_Buildup_path` |
| Geometria do canal | `RiverWidths_path`, `RiverDepths_path` |
| Rasters de qualidade da água | `B1_path`, `B2_path`, `W1_path`, `W2_path` |
| Forçantes e arquivos de contorno | planilhas ou agendas raster de chuva, ETP, inflow, stage e estruturas de controle |

O comportamento detalhado dos rasters suplementares e dos estados iniciais está documentado em [Additional Spatial Inputs](./additional-spatial-inputs).
