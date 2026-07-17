---
title: DTB
---

# Profundidade até o leito rochoso (DTB)

A Profundidade até a Rocha (DTB) define a extensão vertical da coluna de solo disponível para armazenamento de água em HydroPol2D.
Representa a distância entre a superfície terrestre e uma camada limitante que restringe o movimento vertical da água. Esta camada pode corresponder ao leito rochoso real ou a um limite efetivo, como o topo de um aquífero raso.
---

## Função em HydroPol2D

DTB é usado para definir:
- Capacidade máxima de armazenamento subterrâneo
- Limite vertical de infiltração e percolação
- Espessura efetiva da zona vadosa
- Início da saturação na coluna do solo

Dentro do modelo, DTB atua como uma **restrição geométrica** no armazenamento, em vez de um perfil vertical totalmente resolvido.
DTB não deve ser confundido com o raster inicial opcional do lençol freático. No modelo atual, `PHTOKEN1XYZ_path` define a espessura da coluna do solo, enquanto `GW_table_path` define a carga/elevação saturada inicial quando a inicialização da água subterrânea é fornecida explicitamente.
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

Se um mapa DTB não estiver disponível, os valores podem ser atribuídos através das **tabelas de parâmetros de solo**.
Nesse caso:
- Cada classe de solo está associada a um valor representativo de DTB
- O campo DTB é construído implicitamente a partir da classificação do solo

Esta abordagem garante consistência entre:
- Propriedades hidráulicas do solo
- Profundidade de armazenamento disponível

É particularmente útil em ambientes com escassez de dados.
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

DTB define o armazenamento vertical efetivo disponível para o modelo e restringe a profundidade da zona vadosa.
Pode representar a profundidade até o leito rochoso ou a profundidade até a superfície do aquífero, dependendo do objetivo da modelagem.
Embora tenha uma forma simples, desempenha um papel central no controle da geração de escoamento e na capacidade de armazenamento em HydroPol2D.