---
title: DTB
---

# Profundidade até o leito rochoso (DTB)

A Profundidade até a Rocha (DTB) define a extensão vertical da coluna de solo disponível para armazenamento de água em HydroPol2D.
Representa a distância entre a superfície terrestre e uma camada limitante que restringe o movimento vertical da água. Esta camada pode corresponder ao leito rochoso real ou a um limite efetivo, como o topo de um aquífero raso.
---

## Função em HydroPol2D

O que DTB controla depende do esquema de subsuperfície. No esquema padrão, DTB é a profundidade do solo, e o solo e o aquífero compartilham a mesma coluna. Na [subsuperfície em camadas](#dtb-in-the-layered-subsurface), DTB é apenas o fundo do aquífero, e uma base do solo separada marca onde o solo termina.

No esquema padrão, DTB é usado para definir:
- Capacidade máxima de armazenamento subterrâneo
- Limite vertical de infiltração e percolação
- Espessura efetiva da zona vadosa
- Início da saturação na coluna do solo

Dentro do modelo, DTB atua como uma **restrição geométrica** no armazenamento, em vez de um perfil vertical totalmente resolvido.
DTB não deve ser confundido com o raster inicial opcional do lençol freático. No modelo atual, `DTB_path` define a espessura da coluna do solo, enquanto `GW_table_path` define a carga/elevação saturada inicial quando a inicialização da água subterrânea é fornecida explicitamente.
---

## Representação

DTB é fornecido como um **mapa raster contínuo**, onde cada célula contém um valor de profundidade (em metros).
Isso permite variabilidade espacial na capacidade de armazenamento em todo o domínio.
- Raso DTB → rápida saturação e geração de escoamento
- Profundo DTB → maior armazenamento e resposta hidrológica atrasada

---

## Definição Alternativa: Profundidade do Aquífero

Em muitas aplicações, o objetivo não é resolver explicitamente a dinâmica das águas subterrâneas, mas restringir a profundidade da zona vadosa.
Neste caso, DTB pode ser interpretado como a **profundidade da superfície do aquífero**, em vez da profundidade do leito rochoso impermeável.
Sob esta suposição:
- A zona vadosa é limitada à profundidade entre a superfície e o aquífero
- O armazenamento é limitado pelo volume de solo não saturado disponível
- Nenhuma representação explícita do aquífero saturado é necessária

Esta abordagem é apropriada quando:
- Os processos das águas subterrâneas não são explicitamente modelados
- O foco está na resposta hidrológica superficial e próxima à superfície
- É necessário um limite superior realista para o armazenamento do solo

---

## Atribuição padrão de classes de solo

Se um mapa DTB não estiver disponível, uma profundidade do solo por classe de solo pode substituí-lo.

- O **HydroPol2D-Python** pode tomar a profundidade do solo da sua tabela de solos, de um raster de profundidade do solo ou do escalar `vertical.soil_depth_m`.
- O **HydroPol2D (MATLAB)** atualmente não lê a coluna `DTB (m)` de `SOIL_parameters.xlsx`. Com `DTB_path` vazio, a profundidade do solo é 1 m.

Ainda está em aberto se a coluna `DTB (m)` do MATLAB deve ser lida ou removida.

---

## Unidades e Requisitos

A entrada DTB deve:
- Ser expresso em **metros**
- Use um **CRS projetado** consistente com todos os outros rasters
- Alinhe espacialmente com DEM e outras entradas

Os valores devem permanecer dentro de faixas fisicamente realistas para a área de estudo.
---

## Fontes de dados

Os dados DTB não são tão amplamente padronizados quanto DEM ou LULC, mas podem ser derivados de:
### SoilGrids (profundidade até a rocha)
- Região: Global
- Fornece estimativas de profundidade até o leito rochoso
- Baixar: https://soilgrids.org/

---

### Pesquisas Geológicas Regionais
- Conjuntos de dados nacionais ou regionais podem fornecer estimativas de maior qualidade
- Freqüentemente derivado de mapeamento geológico ou modelos de subsuperfície

---

### Valores Derivados ou Presumidos
- DTB pode ser aproximado com base no tipo de solo ou contexto geológico
- Valores constantes podem ser usados ​​quando a variabilidade espacial é desconhecida

---

## DTB na Subsuperfície em Camadas {#dtb-in-the-layered-subsurface}

Na [subsuperfície em camadas](../theory/layered-subsurface) (Python `vertical.subsurface.scheme: layered`, MATLAB `flag_layered_subsurface = 1`), duas profundidades definem a coluna.

| Profundidade | O que marca | Entrada |
|---|---|---|
| Base do solo | Onde terminam as propriedades do solo e começa o regolito | raster `SoilBaseDepth_path`; na falta dele, `subsurface_soil_base_depth_m` (padrão 2 m) |
| Profundidade até o leito rochoso | Onde termina o aquífero | raster `DTB_path`; na falta dele, `subsurface_depth_to_bedrock_m`; na falta deste, a profundidade do solo do esquema padrão (com aviso) |

A base do aquífero é o terreno menos $\min(\mathrm{DTB},\ D_{\max})$, com $D_{\max}$ = `subsurface_max_depth_m` (padrão 50 m). Células com DTB mais profundo que o teto param no teto.

Entre a base do solo e a base da coluna, o modelo distribui camadas de regolito segundo uma régua fixa, com espessuras de 0.25, 0.5, 1, 2, 4, 4, … m a partir da base do solo (a primeira espessura, a razão de crescimento e a espessura máxima são configuráveis). A régua é cortada na base da coluna, e um DTB mais profundo acrescenta mais camadas de 4 m.

No Python, as chaves equivalentes são `vertical.subsurface.soil_base_depth_m`, `depth_to_bedrock_m`, `max_depth_m` e `deep_layers`, e os rasters são `static.soil_base_depth_path` e `static.depth_to_bedrock_path`.

Ainda está em aberto se `DTB_path` deve ser obrigatório no modo Excel do MATLAB quando o esquema em camadas está ativo. Hoje vale o recurso à profundidade do solo padrão, com aviso.

### Fontes globais usadas pelo Case Builder {#global-sources-used-by-the-case-builder}

O Case Builder aplica as mesmas regras a qualquer domínio.

| Mapa | Fonte |
|---|---|
| `DTB.tif` (fundo da coluna) | Profundidade até o leito rochoso do SoilGrids, BDTICM (Shangguan et al., 2017) |
| `SoilBaseDepth.tif` (base do solo) | Profundidade até o horizonte R do SoilGrids, BDRICM, censurada em 2 m e convertida de cm para m |

Os dois mapas vêm do mesmo modelo de Shangguan et al. (2017), e por isso as suas definições são coerentes.

---

## Interação com propriedades do solo

DTB complementa a parametrização do solo:
- Parâmetros do solo controlam o comportamento de infiltração
- DTB limita o volume total disponível para armazenamento

Esta combinação determina a resposta efetiva do sistema sem exigir discretização vertical explícita.
---

## Considerações Práticas

Ao definir DTB:
- Evite valores irrealisticamente grandes
- Mantenha a consistência com a classificação do solo
- Garanta a coerência espacial
- Use suposições simplificadas quando necessário, mas documente-as

DTB costuma ser incerto e deve ser avaliado como parte da análise de sensibilidade, quando possível.
---

## Resumo

No esquema padrão, DTB define o armazenamento vertical efetivo disponível para o modelo e restringe a profundidade da zona vadosa. Na subsuperfície em camadas, DTB define a base do aquífero, e a base do solo define o fundo do solo.
Pode representar a profundidade até o leito rochoso ou a profundidade até a superfície do aquífero, dependendo do objetivo da modelagem.
Embora tenha uma forma simples, desempenha um papel central no controle da geração de escoamento e na capacidade de armazenamento em HydroPol2D.