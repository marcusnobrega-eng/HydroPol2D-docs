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

Este é o esquema padrão. A [subsuperfície em camadas](#soil-and-regolith-in-the-layered-subsurface), opcional, mantém as mesmas três camadas de solo, mas coloca camadas de regolito abaixo delas, com parâmetros próprios.

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

## Solo e Regolito na Subsuperfície em Camadas {#soil-and-regolith-in-the-layered-subsurface}

Na [subsuperfície em camadas](../theory/layered-subsurface), a coluna tem três camadas de solo acima da base do solo e camadas de regolito abaixo dela. Cada camada tem a sua própria curva de van Genuchten.

### Camadas de solo {#soil-slots}

As três camadas de solo usam os parâmetros da classe de solo, ou seja, `ksat` com os três multiplicadores de camada, `n`, `alpha`, `θsat`, `θr` e `l_vg`. Duas colunas da tabela de solos mudam de papel.

| Coluna | Esquema padrão | Subsuperfície em camadas |
|---|---|---|
| `Sy` | Rendimento específico do aquífero | Ignorada. Cada camada toma $S_y$ da sua curva de retenção. |
| `kgsat` | Condutividade lateral do aquífero | Condutividade horizontal das camadas de regolito, usada quando `regolith_ksat_h_mm_h` está vazio |

O rendimento específico de cada camada é a porosidade drenável na capacidade de campo

$$
S_y = \theta_s - \theta\left(\psi = -h_{fc}\right)
$$

com $h_{fc}$ = `capillary_field_capacity_head_m` (padrão 3.3 m). No HydroPol2D-Python, o esquema em camadas não usa `vertical.specific_yield` nem `static.specific_yield_path`. Informar esse caminho gera um aviso.

A condutividade horizontal das camadas de solo é `ksat` × `soil_lateral_anisotropy` (padrão 1) × `soil_lateral_conductivity_multiplier` (padrão 1).

### Camadas de regolito {#regolith-slots}

Os parâmetros do regolito são escalares ou rasters. Um raster prevalece onde for finito, e o escalar preenche o restante.

| Parâmetro | Unidades | Padrão | Raster MATLAB (`General_Data`) | Raster Python |
|---|---|---|---|---|
| `regolith_theta_s` | m³/m³ | 0.35 | `RegolithThetaS_path` | `static.regolith_theta_s_path` |
| `regolith_theta_r` | m³/m³ | 0.05 | `RegolithThetaR_path` | `static.regolith_theta_r_path` |
| `regolith_alpha_vg_m_inverse` | 1/m | 2.0 | `RegolithAlphaVG_path` | `static.regolith_alpha_vg_m_inverse_path` |
| `regolith_n_vg` | - | 1.5 | `RegolithNVG_path` | `static.regolith_n_vg_path` |
| `regolith_ksat_v_mm_h` | mm/h | 5.0 | `RegolithKsatV_path` | `static.regolith_ksat_v_mm_h_path` |
| `regolith_ksat_h_mm_h` | mm/h | vazio: `kgsat` | `RegolithKsatH_path` | `static.regolith_ksat_h_mm_h_path` |
| `regolith_specific_yield` | - | vazio: $\theta_s - \theta_{fc}$ | `RegolithSpecificYield_path` | `static.regolith_specific_yield_path` |

Um $S_y$ do regolito informado deve estar em $(0,\ \theta_s - \theta_r]$. A condutividade horizontal das camadas de regolito é multiplicada por `regolith_lateral_conductivity_multiplier` (padrão 1).

Ainda não existe tabela de classes de regolito. As propriedades do regolito são apenas escalares ou rasters.

### Cargas da absorção de água pelas raízes {#root-water-uptake-heads}

As cargas de Feddes $h_1$ a $h_4$ são configurações globais, e não parâmetros da classe de solo. Veja [Modelo Hidrológico, Seção 3.5](../theory/hydrologic-model#35-feddes-root-water-uptake-stress).

### Fontes globais usadas pelo Case Builder {#global-sources-used-by-the-case-builder}

O Case Builder (`--subsurface-scheme layered`) deriva os mapas do regolito de dados globais, e as mesmas regras valem para qualquer domínio.

| Mapa | Regra | Fonte |
|---|---|---|
| `RegolithThetaS/ThetaR/AlphaVG/NVG.tif` | Classe textural do USDA a 200 cm, convertida em parâmetros de van Genuchten pela tabela de solos do Builder | OpenLandMap texture v0.2, 200 cm |
| `RegolithKsatH.tif` | Permeabilidade × $\rho g/\mu$ a 20 °C. Onde o GLHYMPS não tem polígono, usa o Ksat das águas subterrâneas da classe textural a 200 cm. | Tiles globais do GLHYMPS 2.0 (Gleeson et al., 2014; Huscroft et al., 2018) |
| `RegolithKsatV.tif` | `RegolithKsatH` ÷ `groundwater_vertical_anisotropy_ratio` | - |
| `RegolithSpecificYield.tif` | Padrão `derived_capped`: $\theta_s - \theta(3.3\ \mathrm{m})$, limitado pela porosidade do GLHYMPS; nodata onde falta o GLHYMPS, para que o modelo derive $S_y$ ali. Com `derived`, nenhum mapa é gravado. | `--regolith-specific-yield-rule` |

Os tiles do GLHYMPS são baixados uma vez, conferidos contra o SHA-256 do manifesto e guardados em cache. Proveniência, cobertura e estatísticas vão para `quality_report/layered_subsurface_rasters.json`. Em casos em camadas, o Builder não conecta `SpecificYield.tif` ao caso.

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