---
title: Entradas Espaciais Adicionais
---

# Entradas Espaciais Adicionais

Além dos principais DEM, LULC e rasters de solo, HydroPol2D pode ingerir um conjunto mais amplo de rasters opcionais e entradas de estado inicial. Esta página documenta as entradas baseadas em arquivo suportadas que foram historicamente subdescritas nos documentos.

---

## Entradas Raster Suplementares

| Entrada | Chave de caminho público | Quando usado | Notas |
|---|---|---|---|
| Tabela inicial de águas subterrâneas | `GW_table_path` | Quando a água subterrânea está ativa e um raster inicial é fornecido | Raster é interpretado como **elevação/altura inicial do lençol freático** em metros, alinhado ao DEM. Se estiver faltando, o modelo volta para um lençol freático padrão raso acima da rocha. |
| Impermeabilidade fracionária | `ImperviousFraction_path` | Quando um raster impermeável fracionário é fornecido | Os valores podem estar em porcentagem `[0,1]` ou `[0,100]`. Isso refina a impermeabilidade para células não acumuladas. As células classificadas como acumuladas/impermeáveis ​​pelo LULC permanecem totalmente seladas. |
| LAI espacial | `LAI_path` | Quando o LAI é usado pela configuração ativa | Raster opcional de vegetação alinhado ao DEM. |
| Albedo espacial | `Albedo_path` | Quando `flag_spatial_albedo = 1` | Raster de albedo opcional alinhado ao DEM. |
| Largura do rio | `RiverWidths_path` | Quando o modo de canal subgrade de Neal (2012) usa geometria em raster | Largura do canal em metros. Os valores devem ser positivos e menores que a resolução da célula. |
| Profundidade do rio | `RiverDepths_path` | Quando o modo de canal subgrade de Neal (2012) usa geometria em raster | Profundidade retangular do canal ou altura da margem em metros. Uma profundidade positiva é necessária onde a largura do rio for positiva. |
| Rasters de coeficiente de qualidade da água | `B1_path`, `B2_path`, `W1_path`, `W2_path` | Quando a qualidade da água está ativa e os coeficientes raster estão ativados | Rasters opcionais de acúmulo de poluentes/coeficiente de lavagem. |

---

## Entradas raster de estado inicial

| Entrada | Chave de caminho público | Quando usado | Notas |
|---|---|---|---|
| Profundidade inicial da água superficial | `Warmup_Depth_path` | Quando `flag_warmup = 1` e um raster de profundidade de aquecimento são fornecidos | Raster é lido como a profundidade inicial da lagoa em metros e convertido internamente em milímetros. |
| Armazenamento inicial do solo | `Initial_Soil_Moisture_path` | Quando `flag_warmup = 1` e um raster de solo inicial são fornecidos | Apesar do nome legado, o código atual interpreta esse raster como **armazenamento inicial ativo do solo acima do conteúdo de água residual** em milímetros, e não volumétrico bruto $\theta$. |
| Equivalente inicial de água na neve | `Initial_SWE_path` | Quando a modelagem de neve está ativa e um raster de SWE é fornecido | SWE em milímetros de equivalente de água. Nodata indica que não foi especificada neve inicial. |
| Profundidade inicial da neve | `Initial_Snow_Depth_path` | Quando a modelagem de neve está ativa e um raster de profundidade de neve é fornecido | Profundidade física da neve em milímetros. Nodata indica que não foi especificada neve inicial. |
| Acúmulo inicial de poluentes | `Initial_Buildup_path` | Quando a qualidade da água usa um raster de acúmulo inicial | Usado para inicializar estados de massa/acúmulo de poluentes. |

---

## Entrada do lençol freático

Se `GW_table_path` for fornecido, HydroPol2D usará esse raster como a elevação inicial do lençol freático:
- está alinhado ao DEM,
- cortado para que uma espessura mínima de vadose seja preservada,
- mascarado para o domínio ativo,
- e preenchido localmente apenas onde o raster tiver valores ausentes.

Se nenhum raster do lençol freático for fornecido, o modelo volta para uma altura inicial padrão simples, ligeiramente acima do leito rochoso. Isso significa que `GW_table_path` é uma verdadeira entrada opcional de condição inicial, não um raster de águas subterrâneas obrigatório.

---

## Entrada de Impermeabilidade Fracionada

Se `ImperviousFraction_path` for fornecido, HydroPol2D lê um raster de fração impermeável por célula e o converte em:
- fração impermeável `frac_imp`,
- fração permeável `frac_perv`,
- e uma máscara totalmente impermeável para células que são efetivamente seladas.

Comportamento atual importante:
- os valores podem ser fornecidos como frações ou porcentagens,
- o raster refina a impermeabilidade principalmente fora da classe LULC construída,
- células já classificadas como impermeáveis/acumuladas pela tabela LULC são forçadas a permanecer totalmente impermeáveis.

Portanto, o raster impermeável deve ser documentado como uma **substituição/refinamento de impermeabilidade fracionária**, não como um mapa de cobertura de solo independente e separado.

---

## Alinhamento e Reamostragem

Espera-se que esses rasters suplementares sejam consistentes com o DEM, mas o HydroPol2D também realiza trabalho de alinhamento internamente:
- rasters são reamostrados para a grade DEM quando necessário,
- valores inválidos são mascarados do domínio ativo,
- alguns rasters opcionais só são carregados quando os sinalizadores correspondentes estão ativos.

Isso os torna flexíveis, mas não elimina a necessidade de pré-processamento sensato por parte do usuário.

---

## Estados iniciais de neve

Os parâmetros de neve são colunas da tabela de parâmetros LULC e são atribuídos por `LULC_Index`. Os rasters iniciais são opcionais: sem raster, a célula inicia sem neve; com SWE ou profundidade apenas, o outro estado é calculado com a densidade inicial da classe; com ambos, o par define a densidade e deve ser fisicamente compatível. Valores negativos e pares positivos incompatíveis são rejeitados.

---

## Geometria do canal de Neal (2012)

O modo de canal subgrade de Neal (2012) usa o DEM grosseiro como elevação da planície. `RiverDepths_path` rebaixa o leito retangular do canal em relação a essa elevação, enquanto `RiverWidths_path` define a largura do canal em cada célula de rio. Os dois rasters devem ser fornecidos juntos.

A largura do canal deve ser menor que a resolução da célula. Um canal com largura igual ou superior à célula deve ser resolvido pela grade comum. As rugosidades do canal e da planície são definidas separadamente pelas entradas de parâmetros do rio e do uso e cobertura da terra.

Consulte [Bandeiras do modelo](../configuration/flags) para a combinação de roteamento necessária.

---

## Interpretação Pública Recomendada

A maneira mais fácil de pensar sobre a superfície de entrada é:
1. DEM, LULC e SOIL definem o domínio base.
2. DTB, tabela GW, LAI, albedo e fração impermeável refinam esse domínio base.
3. O aquecimento, o armazenamento inicial do solo, os estados iniciais de neve e o acúmulo inicial definem o estado inicial.
4. Rasters WQ suportam módulos especializados opcionais.

Essa é a história de entrada implementada atualmente que os documentos devem seguir.

---

## Profundidade da raiz

A profundidade da raiz faz parte da superfície de entrada do modelo atual, mas **não** como um caminho raster independente.
Comportamento implementado atual:
- a profundidade da raiz é lida na tabela de parâmetros LULC como `root_depth_m`,
- esse valor baseado em classe é expandido para a grade por meio do mapa categórico LULC,
- a profundidade da raiz resultante é então truncada pela profundidade do leito rochoso e pela posição do lençol freático quando o perfil vadoso em camadas é construído.

Então, sim, HydroPol2D pode ingerir informações de profundidade de raiz, mas o caminho público suportado hoje é:
1. Raster LULC para identidade de classe,
2. `root_depth_m` na tabela de parâmetros LULC para profundidade de raiz por classe.

Não há entrada raster `RootDepth_path` separada no código atual.
