---
title: Arquitetura do ecossistema
---

# Arquitetura do ecossistema

O HydroPol2D usa um único pacote de malha versionado nas suas implementações em
MATLAB e em Python. Isso evita que cada solver reconstrua a geometria ou
interprete as propriedades da malha de forma diferente.

## Responsabilidades dos repositórios {#repository-responsibilities}

| Componente | Responsabilidade | Versão candidata |
|---|---|---|
| HydroBathyDEM | Gerador de produção das malhas regulares e Voronoi, dos produtos de terreno, da sobreposição conservativa com os rasters, das tabelas subgrade, do UGRID, das camadas de inspeção em GeoPackage e do QA da malha. | `0.3.0rc1` |
| HydroPol2D-Python | Motor do modelo em Python e Studio. Ele valida e consome o pacote de malha; não regenera a geometria hidráulica da malha. | `0.8.0rc1` |
| HydroPol2D-MATLAB | Implementação de referência em MATLAB e consumidor compatível do mesmo pacote de malha. | `1.18.0-rc1` |
| HydroPolMesh | Protótipo de migração arquivado. As funcionalidades úteis já validadas estão sendo mantidas no HydroBathyDEM; ele não é uma dependência de execução em produção. | protótipo |

A versão estável `v1.17.0` do MATLAB continua sendo a referência numérica enquanto as
versões candidatas coordenadas concluem as verificações de paridade e de longa duração.

## Contrato de malha compartilhado {#shared-mesh-contract}

O contrato de malha `1.0` exige que o pacote declare:

- a geometria e a conectividade das células e das faces, as áreas, os comprimentos e a orientação;
- índices de arquivo com base zero, convertidos explicitamente para os índices com base um do MATLAB;
- `cell_cfl_width_m`, definido a partir da menor distância entre centros medida na direção normal a uma face;
- o CRS, as unidades, a resolução de origem, a proveniência e a versão do contrato;
- pesos conservativos de sobreposição entre o raster e as células;
- tabelas subgrade compatíveis, no nível das células e das faces, quando o roteamento subgrade está ativado.

Os dois solvers rejeitam índices malformados, faces de comprimento zero, áreas negativas,
unidades ou CRS ausentes, larguras de CFL indefinidas, sobreposição não conservativa e
tabelas subgrade incompatíveis. Eles não reconstroem silenciosamente as propriedades da
malha que estiverem faltando.

## Formulações subgrade {#subgrid-formulations}

As opções a seguir resolvem representações diferentes e não são sinônimas:

| Opção | Representação pretendida |
|---|---|
| Canal de Neal | Canal retangular embutido na grade raster estruturada; suportado com o roteamento local inertial. |
| Subgrade estruturada por tabela de consulta | Tabelas de consulta de células e faces dependentes da profundidade, no estilo do SFINCS, em uma grade estruturada. |
| Subgrade Voronoi | Relações de área, perímetro molhado e condutância em uma malha Voronoi não estruturada. |

Os nomes antigos só são aceitos pela migração do caso. Combinações incompatíveis
precisam ser corrigidas antes que uma simulação possa começar.

## Estado das versões {#release-status}

As versões candidatas são builds de integração, e não as versões coordenadas finais.
A publicação final exige instalação a partir de um clone limpo, comparações entre MATLAB e
Python com a mesma malha e as mesmas entradas hidrológicas, as simulações de Pune de 2 h,
6 h e 12 h e a aprovação nas verificações científicas, do Studio, de lint, de tipos e de
proveniência.
