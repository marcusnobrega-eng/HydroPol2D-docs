---
title: Arquitetura do ecossistema
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Arquitetura do ecossistema

O HydroPol2D usa um único pacote de malha versionado nas suas implementações em
MATLAB e em Python. Isso evita que cada solver reconstrua a geometria ou
interprete as propriedades da malha de forma diferente.

<p align="center">
  <img src={useBaseUrl('/img/getting-started/ecosystem.pt.svg')} width="720" alt="O HydroBathyDEM gera o pacote de malha, com o protótipo arquivado HydroPolMesh apontando para ele; o pacote contém a malha UGRID, os pesos de sobreposição com o raster, as tabelas subgrade e as camadas GeoPackage e declara os itens do contrato de malha; o HydroPol2D-Python e o HydroPol2D-MATLAB o validam ao carregar, e uma lista mostra o que os dois rejeitam" />
</p>

<p align="center">
  <em>Figura 1. O HydroBathyDEM grava um único pacote de malha versionado, que o HydroPol2D-Python e o HydroPol2D-MATLAB validam e usam. Um pacote que falha numa verificação é rejeitado, e nenhum dos solvers reconstrói propriedades ausentes.</em>
</p>

## Responsabilidades dos repositórios {#repository-responsibilities}

| Componente | Responsabilidade | Versão candidata |
|---|---|---|
| HydroBathyDEM | Gerador de produção das malhas regulares e Voronoi, dos produtos de terreno, da sobreposição conservativa com os rasters, das tabelas subgrade, do UGRID, das camadas de inspeção em GeoPackage e do QA da malha. | `0.4.0rc1` |
| HydroPol2D-Python | Motor do modelo em Python e Studio. Ele valida e consome o pacote de malha; não regenera a geometria hidráulica da malha. | `0.9.0rc2` |
| HydroPol2D-MATLAB | Implementação de referência em MATLAB e consumidor compatível do mesmo pacote de malha. | `1.19.0-rc1` |
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

Os dois solvers rejeitam índices malformados, faces de comprimento zero, áreas nulas ou
negativas, unidades ou CRS ausentes, larguras de CFL indefinidas, sobreposição não
conservativa, tabelas subgrade incompatíveis e a ausência da versão do contrato. Eles não reconstroem silenciosamente as propriedades da
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
