---
title: Solo
---

# Propriedades do solo

Os dados do solo definem a resposta hidráulica da superfície terrestre e controlam a taxa na qual a água se infiltra no subsolo em HydroPol2D.
Dentro da formulação atual do modelo, as propriedades do solo são usadas para estimar **capacidade de infiltração, armazenamento em camadas da zona vadosa, drenagem/recarga, ascensão capilar e comportamento de armazenamento de água subterrânea**.
---

## Função em HydroPol2D

A entrada do solo é usada para representar:
- Capacidade de infiltração na superfície
- Armazenamento de água próximo à superfície, na zona radicular e na zona de transmissão
- Condutividade hidráulica eficaz por camada
- Condições iniciais de umidade do solo (quando não fornecidas como campo espacial)
- Rendimento específico das águas subterrâneas e condutividade hidráulica saturada

Estas propriedades influenciam diretamente a geração do escoamento e o momento da resposta hidrológica.
---

## Representação do Solo

HydroPol2D requer um **mapa de solo categórico**.
Cada célula da grade deve receber um identificador de classe de solo, que é então vinculado a um conjunto de parâmetros hidráulicos através das tabelas de entrada.
Essa estrutura permite que o modelo:
- Atribuir propriedades hidráulicas distribuídas espacialmente
- Mantenha a consistência em todo o domínio
- Separar dados espaciais da definição de parâmetros

O mapa de solos ainda fornece uma classe categórica de solo por célula do modelo. Essa classe define os parâmetros hidráulicos básicos da coluna. A implementação em camadas atual particiona a profundidade vadose disponível em:
- uma camada próxima à superfície, com profundidade alvo padrão de $0,10\,\mathrm{m}$;
- uma camada de zona raiz, cuja profundidade é definida pela classe LULC;
- uma camada de zona de transmissão abaixo da zona raiz;
- uma zona de águas subterrâneas começando no lençol freático atual.

A geometria da camada se adapta à profundidade da rocha e à posição da água subterrânea. Se a profundidade da raiz for menor que a camada próxima à superfície, a camada explícita da zona raiz colapsará na camada próxima à superfície. Se o leito rochoso ou o lençol freático for mais raso do que a profundidade radicular solicitada, a zona radicular será truncada para a profundidade vadosa disponível.
---

## Parâmetros de solo necessários

Os parâmetros hidráulicos são definidos externamente e associados às classes de solos. Os parâmetros típicos incluem:
- Condutividade hidráulica saturada (Ks)
- Porosidade do solo
- Conteúdo de água residual
- Parâmetros de retenção de água no solo (por exemplo, parâmetros de Van Genuchten)
- Umidade inicial do solo (quando não prescrita como campo espacial)
- Rendimento específico e condutividade saturada das águas subterrâneas
- Multiplicadores de camada opcionais para condutividade hidráulica saturada

Estes parâmetros devem ser fisicamente consistentes e representativos das classes de solos definidas no raster.
---

## Fontes de dados do solo

Vários conjuntos de dados podem ser usados ​​para derivar classificações de solo e parâmetros hidráulicos associados.
### Grades de Solo (ISRIC)
- Região: Global
- Resolução: até 250 m
- Fornece estimativas contínuas das propriedades do solo (textura, densidade aparente, conteúdo orgânico)
- Pode ser usado para derivar classes de textura de solo do USDA
- Baixar: https://soilgrids.org/

---

### FAO / HWSD (Banco de Dados Mundial Harmonizado de Solos)
- Região: Global
- Resolução mais grosseira
- Fornece unidades de mapeamento do solo e propriedades associadas
- Adequado para aplicações continentais e de grande escala
- Baixar: https://www.fao.org/soils-portal/data-hub/en/

---

### Classificação de solo do USDA (baseada em textura)

HydroPol2D geralmente depende de **classes de textura de solo do USDA** (por exemplo, areia, argila, argila) para definir o comportamento hidráulico.
Essas classes podem ser derivadas de:
- Frações de textura SoilGrids
- Bancos de dados de solos da FAO
- Levantamentos regionais de solo

Esta abordagem fornece uma estrutura consistente para atribuir parâmetros hidráulicos, como condutividade e características de retenção.
---

### SSURGO (Banco de dados geográfico de levantamento de solos)
- Região: Estados Unidos
- Resolução espacial muito alta
- Taxonomia detalhada do solo e propriedades físicas
- Recomendado para aplicações de alta resolução
- Baixar: https://websoilsurvey.sc.egov.usda.gov/

---

### STATSGO (Banco de Dados Geográfico do Solo do Estado)
- Região: Estados Unidos
- Resolução mais grosseira que SSURGO
- Adequado para estudos regionais a continentais
- Baixar: https://www.nrcs.usda.gov/resources/data-and-reports/statsgo


## Associação de parâmetros

As classes de solo não são usadas diretamente nas equações governantes. Em vez disso, eles servem como **índices em tabelas de parâmetros**.
Cada classe de solo deve estar associada a um conjunto consistente de propriedades hidráulicas. A qualidade desse mapeamento tem impacto direto no desempenho do modelo.
Os usuários são responsáveis ​​por garantir que:
- Os valores dos parâmetros são fisicamente realistas
- As unidades são consistentes
- As classes de solo são devidamente definidas e interpretadas

---

## Resolução e Alinhamento

O raster de solo deve:
- Corresponder ou ser reamostrado para a resolução DEM
- Use o mesmo sistema de referência de coordenadas projetadas (CRS)
- Alinhe espacialmente com todas as outras entradas raster

Qualquer incompatibilidade na resolução ou alinhamento resultará na atribuição espacial incorreta das propriedades do solo.
---

## Considerações Práticas

Ao preparar os insumos do solo:
- Prefira representações categóricas em vez de conjuntos de dados contínuos brutos
- Agregue classificações detalhadas do solo quando necessário
- Evite valores de parâmetros extremos ou não físicos
- Verifique a consistência entre classes raster e tabelas de parâmetros

Em muitos casos, simplificar o número de classes de solos melhora a estabilidade e a interpretabilidade do modelo.
---

## Resumo

No HydroPol2D, os dados do solo são usados ​​para controlar a infiltração, o armazenamento vadoso em camadas, a recarga, o armazenamento de águas subterrâneas e o feedback das águas subterrâneas para a superfície.
O modelo depende de uma representação categórica do solo juntamente com parâmetros hidráulicos definidos externamente, profundidades da zona radicular baseadas em LULC e multiplicadores de camada opcionais. A definição e mapeamento adequados desses parâmetros são essenciais para a obtenção de simulações confiáveis.