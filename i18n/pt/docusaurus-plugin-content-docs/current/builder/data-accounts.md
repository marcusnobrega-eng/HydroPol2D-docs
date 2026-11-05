---
title: Fontes de dados e contas
---

# Fontes de dados e contas

A maior parte dos dados que o Case Builder usa é de download aberto. Três fontes exigem uma conta
sua. Os seus logins ficam no seu computador: o Builder os lê dos seus próprios arquivos ou de
variáveis de ambiente e nunca os grava em um caso.

| Fonte | Necessária para | Conta |
|---|---|---|
| Copernicus Climate Data Store (CDS) | clima do ERA5, umidade inicial do solo do ERA5-Land, chuva do ERA5 e os contornos do GloFAS e do GTSM | gratuita, para todo caso feito no app |
| NASA Earthdata | chuva do IMERG, e área foliar quando o serviço MODIS do ORNL está indisponível | gratuita |
| MSWEP (GloH2O) | chuva do MSWEP | aprovação da GloH2O, e o rclone para a pasta dela no Google Drive |

A chuva do AORC (Estados Unidos) e os mapas estáticos (terreno, bacias, cobertura do solo, solos,
águas subterrâneas) não exigem conta. A área foliar vem do serviço web MODIS do ORNL, sem conta.
Quando esse serviço está indisponível, o Builder a obtém do NASA LP DAAC, que usa o seu login do
Earthdata.

A página confere as contas antes de baixar qualquer coisa. Quando falta uma, uma caixa amarela diz
"This case cannot be prepared yet:" e a nomeia, e **Prepare complete case** fica desativado.

## Copernicus Climate Data Store {#copernicus-cds}

1. Crie uma conta no [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/).
2. Entre e aceite os termos de uso dos conjuntos de dados ERA5 e ERA5-Land.
3. Copie o seu token de acesso pessoal na página do seu perfil no CDS.
4. Crie um arquivo de texto chamado `.cdsapirc` na sua pasta pessoal, com estas duas linhas:

   ```yaml
   url: https://cds.climate.copernicus.eu/api
   key: YOUR_CDS_PERSONAL_ACCESS_TOKEN
   ```

   No Mac, o arquivo é `~/.cdsapirc`, e no Windows, `%USERPROFILE%\.cdsapirc`. No Mac, proteja-o
   com `chmod 600 ~/.cdsapirc`.

O token também pode vir da variável de ambiente `CDSAPI_KEY`. O CDS põe cada pedido em uma fila,
então o primeiro download de um caso pode esperar alguns minutos antes de começar.

## NASA Earthdata {#nasa-earthdata}

1. Crie uma conta [NASA Earthdata Login](https://urs.earthdata.nasa.gov/) e aceite os termos dos
   dados do GPM IMERG.
2. Gere um token no seu perfil do Earthdata.
3. Salve o token, sozinho em uma linha, neste arquivo:
   - Mac: `~/.config/hydropol2d-case-builder/earthdata_token`
   - Windows: `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token`

   No Mac, proteja a pasta e o arquivo:

   ```bash
   mkdir -p ~/.config/hydropol2d-case-builder
   chmod 700 ~/.config/hydropol2d-case-builder
   chmod 600 ~/.config/hydropol2d-case-builder/earthdata_token
   ```

O Builder também aceita o token na variável de ambiente `EARTHDATA_TOKEN`, um arquivo `~/.netrc` com
o seu login do Earthdata ou as variáveis `EARTHDATA_USERNAME` e `EARTHDATA_PASSWORD`.

## MSWEP {#mswep}

O MSWEP exige aprovação prévia da GloH2O.

1. Peça acesso na [página do MSWEP](https://www.gloh2o.org/). O e-mail de aprovação dá a você uma
   pasta compartilhada no Google Drive.
2. Instale o [rclone](https://rclone.org) (no Mac, com o Homebrew: `brew install rclone`).
3. Rode `rclone config` e crie um remote chamado `GoogleDrive` do tipo `drive`. Conclua a
   autorização no navegador e não configure a pasta compartilhada como um Team Drive.
4. Confira se a pasta compartilhada está visível:

   ```bash
   rclone lsd --drive-shared-with-me GoogleDrive:
   ```

Quando você escolhe **MSWEP (hourly)** ou **MSWEP (3 hourly)**, a página procura a pasta autorizada
do MSWEP nos seus remotes do rclone. Quando encontra uma, ela diz "Authorized MSWEP V3.16 folder
found. Automatic MSWEP download is ready." e preenche **MSWEP rclone folder** e **Shared-folder ID
(optional)**. Os dois continuam visíveis, e você pode mudá-los. O Builder baixa só os passos de tempo
do caso, recorta-os no domínio e registra a fonte em `quality_report/mswep_download.json`. Quando um
pedido passa do fim do registro **Past**, os passos de tempo posteriores vêm sozinhos da pasta
**NRT** (near real time, quase em tempo real).

A página avisa que o MSWEP V3.16 tem uma tendência artificial documentada na precipitação por volta
de 2015. Para estudos de tendência de 1979 a 2021, use a V2.80. Os arquivos NRT recentes são
preliminares e são revisados depois da primeira publicação. O MSWEP V3 é citado como Wang et al.
(2026), [MSWEP V3](https://arxiv.org/abs/2602.01436).

Se você já tem a chuva em arquivos, use **Existing rainfall directory (optional)** em vez do
download ([Configurações do caso](settings#rainfall-folders)).

## Licenças dos dados {#data-licenses}

Os conjuntos de dados de entrada mantêm as suas próprias licenças e termos de acesso, e você os
segue quando usa os dados deles. Cada caso registra cada fonte e a sua versão em
`quality_report/public_static_sources.json` e no seu `manifest.json`.
