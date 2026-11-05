---
title: Prévia e custo
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Prévia e custo

**Preview domain and cost** desenha o domínio e estima o tamanho do caso em segundos, antes de
qualquer download grande. Nada é montado ainda, então você pode mudar as configurações e fazer a
prévia de novo até o domínio ficar certo. **Prepare complete case** fica desativado até que a prévia
corresponda às configurações atuais.

## Antes da prévia {#before-the-preview}

Acima dos dois botões, a página confere o pedido:

- o período de cada fonte de chuva, por exemplo "NASA IMERG Final Run availability: 1998-01-01
  through 2025-09-30";
- as contas e as ferramentas de que o caso precisa. Quando falta uma, uma caixa amarela diz "This
  case cannot be prepared yet:" e a nomeia (veja [Fontes de dados e contas](data-accounts));
- no AORC, que o domínio inteiro fica dentro da grade do AORC, o que a prévia confirma;
- quando tudo está pronto: "Required credentials, source coverage, and local tools are ready for
  this request."

## O que a prévia mostra {#what-the-preview-shows}

1. **Case files**: a pasta do caso, em verde. A prévia já grava ali o pedido, o domínio e os mapas
   da prévia.
2. **O domínio em um mapa.** O mapa é interativo, sobre o OpenTopoMap. O controle de camadas troca
   para um mapa de ruas ou esconde as sobreposições. O mapa online é só um fundo: ele não muda o
   caso.
3. **Estimated quadtree grid** (casos quadtree): as zonas de resolução da malha.
4. **Rivers entering the domain** (Urban Area Only): veja [Escolher a área do modelo](model-area#urban-area-only).
5. **O tamanho do caso**: seis números e, para uma grade quadtree, as células de cada tamanho.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-map.jpg')} width="760" alt="A prévia da bacia urbana de Tucson: a mensagem de pronto, os botões Preview domain and cost e Prepare complete case, a linha verde Case files e um mapa topográfico interativo com a área urbana em laranja, as bacias conectadas e as bacias a montante em azul, e a rede de rios" />
</p>

<p align="center">
  <em>Figura 1. A prévia da bacia urbana de Tucson. A cidade (laranja) fica a jusante na bacia do rio Santa Cruz, então as bacias a montante se estendem para o sul, cruzando a fronteira com o México.</em>
</p>

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-quadtree.jpg')} width="560" alt="Grade quadtree estimada da bacia urbana de Tucson: a cidade coberta por células de 90 m, uma faixa estreita de células de 180 m ao redor dela e o resto da bacia em células de 360 m" />
</p>

<p align="center">
  <em>Figura 2. As zonas quadtree do mesmo caso: células de 90 m sobre a cidade e a faixa ao redor dela, uma faixa de células de 180 m e células de 360 m sobre o resto da bacia.</em>
</p>

Para um caso Catchment, o mapa mostra o exutório que você informou, os três exutórios candidatos na
rede de rios e um primeiro contorno da bacia.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-catchment.jpg')} width="760" alt="A prévia do San Francisquito Creek em um mapa topográfico, com o exutório informado como um ponto vermelho, os exutórios candidatos em laranja na rede de rios, o primeiro contorno da bacia e, abaixo, as células da matriz, as células ativas e a área da bacia" />
</p>

<p align="center">
  <em>Figura 3. A prévia do San Francisquito Creek. O ponto vermelho é o exutório que você informou, os pontos laranja são os exutórios candidatos e o contorno é um primeiro esboço da bacia. A montagem completa delimita a bacia de novo na grade do modelo.</em>
</p>

## O tamanho do caso {#size}

| Número | O que significa |
|---|---|
| **Matrix cells** | linhas vezes colunas do retângulo em torno do domínio inteiro |
| **Active cells** | as células dentro do domínio |
| **Basin area** | a área do domínio, em km² |
| **Temporary transfer ceiling** | um limite superior dos dados de origem que a montagem baixa, mapas estáticos e forçantes juntos |
| **Retained forcing inputs** | a chuva e o clima guardados com o caso pronto |
| **Estimated saved outputs** | o tamanho dos resultados que o modelo vai salvar, a partir das saídas que você escolheu |

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-metrics.png')} width="760" alt="Os seis números da prévia quadtree de Tucson: 1.743.840 células da matriz, 107.512 células ativas, área da bacia de 8.227 km2, teto de transferência de 195,2 MiB, 0,5 MiB de forçantes retidas e 1,36 GiB de saídas salvas, depois uma tabela com 40.230 células de 90 m, 8.426 de 180 m e 58.856 de 360 m, e o painel recolhido How these values are estimated" />
</p>

<p align="center">
  <em>Figura 4. O tamanho do caso de Tucson: 107.512 células ativas em uma bacia de 8.227 km², menos de 200 MiB para baixar e cerca de 1,4 GiB de resultados.</em>
</p>

A memória depende sobretudo da matriz, não só das células ativas. Um domínio longo ou recortado pode
precisar de mais memória do que a sua área sugere. **How these values are estimated** explica cada
número e lista o download e as saídas salvas por fonte. Algumas notas desse painel:

- A transferência conta os valores de origem na resolução própria de cada produto, sobre o domínio e
  o período. Ela não conta os rasters do HydroPol2D que a montagem grava. O MSWEP é contado como
  valores sem compressão, então o tráfego real é menor.
- Os arquivos brutos de origem são removidos depois de uma montagem bem-sucedida. Uma montagem que
  falha os mantém, para que a próxima tentativa continue de onde parou.
- A estimativa das saídas salvas conta só os arquivos selecionados, como valores sem compressão.

Comece os modelos regionais grandes com um tamanho de célula grosso, leia os números e só refine a
grade quando eles couberem no seu computador.

## Quando as configurações mudam {#settings-change}

Qualquer mudança depois de uma prévia mostra "Settings changed. Run the preview again before
preparing this case." O **Process log**, no pé da aba, guarda as mensagens da última prévia ou
montagem.
