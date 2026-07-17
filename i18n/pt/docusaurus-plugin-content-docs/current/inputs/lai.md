---
title: LAI
---

# Índice de área foliar (LAI)

O Índice de Área Foliar (LAI) representa a área foliar total por unidade de área terrestre e é usado no HydroPol2D para caracterizar a densidade da vegetação e sua interação com a precipitação e os processos atmosféricos.
Na implementação atual do modelo, LAI é usado para representar os efeitos do dossel na interceptação e evapotranspiração.
---

## Função em HydroPol2D

LAI é usado para representar:
- Interceptação de chuvas pela cobertura vegetal
- Particionamento entre armazenamento throughfall e dossel
- Influência da vegetação na evapotranspiração

Valores mais elevados de LAI correspondem a vegetação mais densa e maior capacidade de armazenamento da copa.
---

## Representação

LAI é fornecido como um **mapa raster contínuo**, onde cada célula da grade contém um valor que representa a densidade da vegetação.
Os valores típicos variam de:
- ~0 → solo descoberto ou superfícies impermeáveis
- 1–3 → vegetação esparsa a moderada
- 4–7+ → vegetação densa (por exemplo, florestas)

Os valores devem ser consistentes com as condições de cobertura do solo no domínio.
---

## Representação Temporal

O LAI dinâmico **não está implementado atualmente** em HydroPol2D.
Como resultado, LAI deve ser fornecido como uma **entrada estática**.
As abordagens recomendadas são:
- **Mediana LAI** → para simulações climatológicas ou de longo prazo
- **Estação chuvosa LAI** → para simulações focadas em alta atividade vegetal
- **Estação seca LAI** → para simulações focadas em condições de vegetação reduzida

A escolha deve ser consistente com o objetivo da simulação e o período de tempo.
---

## Fontes de dados

Vários conjuntos de dados fornecem estimativas globais de LAI:
### MODIS LAI (MOD15A2H)
- Região: Global
- Resolução: 500 m
- Resolução temporal: 8 dias
- Produto amplamente utilizado e consistente
- Baixar: https://lpdaac.usgs.gov/products/mod15a2hv061/

---

### Serviço Terrestre Global Copernicus (LAI)
- Região: Global
- Resolução: 300 m
- Resolução temporal: 10 dias
- Derivado de observações de satélite
- Baixar: https://land.copernicus.eu/global/products/lai

---

### VIIRS LAI
- Região: Global
- Resolução moderada
- Continuação dos produtos da era MODIS

---

### Google Earth Engine

Os conjuntos de dados LAI do MODIS, Copernicus e VIIRS estão disponíveis em Google Earth Engine e podem ser processados ​​para extrair valores medianos ou sazonais.
---

## Consistência com LULC

LAI deve ser consistente com a classificação LULC.
A correspondência típica inclui:
- Floresta → alta LAI
- Pastagem → moderado LAI
- Urbano → LAI baixo ou próximo de zero

Inconsistências entre LULC e LAI resultarão em um comportamento irreal do velame.
---

## Considerações Práticas

Ao preparar entradas LAI:
- Use valores representativos para o período de simulação
- Evite valores extremos ou ruidosos de produtos de satélite brutos
- Aplicar agregação temporal (mediana ou médias sazonais) quando necessário
- Garanta consistência espacial com outras entradas raster

Se nenhum conjunto de dados LAI estiver disponível, os valores poderão ser atribuídos com base nas classes LULC, embora isso introduza suposições adicionais.
---

## Resumo

LAI é usado em HydroPol2D para representar os efeitos da vegetação na interceptação e evapotranspiração.
O modelo atualmente assume um campo estático LAI e os usuários devem selecionar valores representativos com base no período de simulação pretendido.
A seleção cuidadosa de LAI é necessária para garantir consistência com a cobertura da terra e representação realista dos processos de vegetação.