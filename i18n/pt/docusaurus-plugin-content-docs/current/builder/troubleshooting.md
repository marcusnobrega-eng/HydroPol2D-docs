---
title: Solução de problemas
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Solução de problemas

## Ao iniciar o app {#starting}

**O navegador não abre.** Clique em **Open in browser** na janela pequena. A página fica em
`http://127.0.0.1:8501`, ou na próxima porta livre.

**A janela pequena diz que o Case Builder parou.** Ela indica um arquivo de log. Envie esse arquivo
com a sua pergunta para Marcus N. Gomes Jr. ([marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com)).

**O macOS não abre o app.** Autorize-o uma vez em **Ajustes do Sistema › Privacidade e Segurança**
(**System Settings › Privacy & Security**) com **Abrir Mesmo Assim** (**Open Anyway**)
([Instalação e licença](install-and-license#mac-apple-silicon)).

## Licença {#license}

**"This is a HydroPol2D Studio code".** Você colou o seu código do Studio. O Case Builder precisa do
seu próprio código.

**A licença expirou, ou faltam menos de 30 dias.** Escreva para o Marcus pedindo um código novo. Para
digitá-lo, apague `license.txt` da pasta da licença e abra o Case Builder de novo
([Sobre a sua licença](install-and-license#about-your-license)).

**O Case Builder se recusa a iniciar depois de uma mudança de data.** Acerte a data e a hora do
computador. O Builder se recusa a iniciar quando a data é atrasada mais de dois dias em relação ao
último uso.

## Antes da prévia {#before-the-preview}

**"Confirm riverbed hydraulic conductivity when river-groundwater exchange is enabled."** Abra
**Hydraulic parameters**, confira **Riverbed conductivity (m/s)** e marque **Confirm this riverbed
conductivity for the case**, ou desmarque **River-groundwater exchange**.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-riverbed-confirm.png')} width="760" alt="A mensagem de pronto, o botão Preview domain and cost e uma caixa de erro vermelha que pede a confirmação da condutividade hidráulica do leito do rio quando a troca rio-águas subterrâneas está ligada" />
</p>

<p align="center">
  <em>Figura 1. A prévia não avança até que a condutividade do leito do rio seja confirmada.</em>
</p>

**"This case cannot be prepared yet:" com uma conta indicada.** Configure essa conta
([Fontes de dados e contas](data-accounts)) e recarregue a página.

**O período de chuva não está disponível.** O IMERG, o AORC e o MSWEP têm os seus próprios períodos,
que a página mostra. Escolha datas dentro deles, ou outro produto de chuva. O AORC também exige que o
domínio inteiro esteja dentro dos Estados Unidos contíguos.

**A cidade não é encontrada.** Confira a grafia da cidade e do país como o GHSL os escreve. Se o
GHSL não tem o limite de que você precisa, escolha **Polygon file** e informe o seu próprio polígono.

**"Requested … m cells are finer than the DEM's …".** O tamanho da célula não pode ser mais fino que
o terreno. Use um tamanho de célula maior, ou um DEM local mais fino.

**"The coarse quadtree resolution must be a power-of-two multiple of the fine resolution."** Faça o
tamanho da célula grossa igual a 2, 4, 8 ou mais vezes o tamanho fino.

## A prévia {#the-preview}

**O caso é grande demais.** Pare depois da prévia. Use um tamanho de célula maior, uma grade
quadtree ou uma área menor, ou leve a montagem e a simulação para um computador com mais memória. A
memória acompanha as células da matriz mais do que as células ativas.

**A bacia está errada ou grande demais.** Escolha outro **Outlet candidate**, mude o **Snap radius**
ou mova o exutório para cima do rio.

## Ao preparar o caso {#preparing}

**O Copernicus (CDS) falha ou demora muito.** O CDS põe cada pedido em uma fila, o que pode levar
minutos ou mais. Se falhar, confira se o `.cdsapirc` tem a URL e o token atuais, sem aspas a mais, e
se você aceitou os termos do ERA5 e do ERA5-Land no site do CDS.

**O IMERG retorna 401 ou 403.** O seu token do Earthdata expirou ou os termos do GPM não foram
aceitos. Gere um token novo e confira as permissões do arquivo.

**O MSWEP não baixa.** Rode `rclone lsd --drive-shared-with-me GoogleDrive:` e confira se a pasta
aprovada aparece na lista. **MSWEP rclone folder** precisa apontar para a pasta `Hourly` ou
`3hourly` dela. Se a pasta aparece na lista mas um caminho dá "directory not found", preencha
**Shared-folder ID** com o ID da pasta no Google Drive, obtido com:

```bash
rclone lsjson --dirs-only --drive-shared-with-me --include 'MSWEP_V316_test/' GoogleDrive:
```

**Falta um passo de tempo de chuva** (arquivos de chuva locais). A pasta precisa ter cada passo de
tempo, do início do aquecimento ao fim, com os nomes de [Configurações do caso](settings#rainfall-folders).

**A montagem parou no meio.** Leia o **Process log**. Os arquivos baixados são mantidos, então
**Prepare complete case** continua de onde parou depois que você corrigir a causa.

## Ao verificar e rodar {#checking-and-running}

**A verificação prévia falha.** Leia os problemas listados, ou `quality_report/preflight.json`
([Verificar um caso](check-a-case)).

**"The final model-resolution D8 area differs by more than a factor of two from the preliminary
HydroSHEDS area."** O exutório provavelmente foi ajustado a outro rio. Escolha outro candidato ou
outro raio de ajuste, faça a prévia e prepare o caso de novo.

**A simulação no MATLAB não inicia.** Confira **MATLAB executable**. Se a pasta do HydroPol2D MATLAB
ainda não existe, o app a baixa com o Git: instale o Git, ou informe uma pasta que já contenha o
HydroPol2D MATLAB.

**"HydroPol2D Python comes with HydroPol2D Studio".** O app não baixa o HydroPol2D Python. Abra
`hydropol_python/case.yaml` no HydroPol2D Studio ([Rodar o caso](run-the-case#studio)).

**O modelo fica sem memória.** Use uma grade mais grossa para testar, e rode os casos regionais finos
em uma workstation ou em um cluster.

**O albedo é 0,25 em todo lugar.** Isso é esperado nesta versão.
