---
title: Albedo
---

# Albedo

Albedo representa a fração da radiação de ondas curtas que é refletida pela superfície.
No HydroPol2D, o albedo é usado para caracterizar as propriedades radiativas da superfície e sua influência nos processos relacionados à energia, particularmente a evapotranspiração e a dinâmica da neve.
---

## Função em HydroPol2D

Albedo é usado para representar:
- Reflexividade da superfície à radiação solar recebida
- Energia disponível para evapotranspiração
- Condições de equilíbrio de energia superficial
- Comportamento do derretimento da neve (quando os processos de neve são ativados)

As superfícies de albedo mais baixo absorvem mais energia, enquanto as superfícies de albedo mais altas refletem uma fração maior da radiação recebida.
---

## Representação

Albedo é fornecido como um **mapa raster contínuo**, onde cada célula da grade contém um valor entre 0 e 1.
Os valores típicos incluem:
- 0,05 – 0,15 → corpos d'água, superfícies escuras
- 0,15 – 0,25 → vegetação
- 0,25 – 0,40 → solos secos
- 0,60 – 0,90 → superfícies cobertas de neve

Os valores devem ser fisicamente consistentes com a cobertura do solo e as condições ambientais.
---

## Representação Temporal

Na implementação atual do HydroPol2D, o albedo é tratado como uma **entrada estática**.
Os usuários devem selecionar valores representativos das condições de simulação:
- Simulações de longo prazo → use albedo médio ou mediano
- Simulações sazonais → usam valores consistentes com a condição dominante da superfície

Variações dinâmicas do albedo (por exemplo, devido à cobertura de neve ou mudanças na vegetação) não são explicitamente resolvidas, a menos que sejam fornecidas externamente.
---

## Fontes de dados

Vários conjuntos de dados fornecem estimativas de albedo global:
### MODIS Albedo (MCD43A3)
- Região: Global
- Resolução: 500 m
- Resolução temporal: 16 dias
- Produto derivado de satélite amplamente utilizado
- Baixar: https://lpdaac.usgs.gov/products/mcd43a3v061/

---

### Serviço Terrestre Global Copernicus (Albedo)
- Região: Global
- Resolução: 300 m
- Derivado de observações de satélite
- Baixar: https://land.copernicus.eu/global/products/albedo

---

### Google Earth Engine

Os conjuntos de dados MODIS e Copernicus albedo estão disponíveis em Google Earth Engine e podem ser processados ​​para extrair valores representativos para o domínio de simulação.
---

## Consistência com outras entradas

Albedo deve ser consistente com:
- **LULC** → define o tipo de superfície
- **LAI** → reflete a densidade da vegetação
- **Condições de neve** → influenciam fortemente a refletividade

Valores inconsistentes de albedo podem levar a uma partição de energia irrealista.
---

## Considerações Práticas

Ao preparar entradas de albedo:
- Evite valores extremos ou não físicos
- Use valores agregados temporalmente quando necessário
- Garanta o alinhamento espacial com todas as entradas raster
- Verifique a consistência com a cobertura da terra e as condições climáticas

Se nenhum conjunto de dados de albedo estiver disponível, os valores poderão ser atribuídos com base nas classes LULC, com justificativa apropriada.
---

## Resumo

Albedo define as propriedades radiativas da superfície em HydroPol2D e influencia processos movidos a energia, como evapotranspiração e degelo.
Embora de estrutura simples, desempenha um papel importante na garantia de uma representação fisicamente consistente das interações superfície-atmosfera.