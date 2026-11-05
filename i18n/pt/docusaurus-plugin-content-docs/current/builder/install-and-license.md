---
title: Instalação e licença
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Instalação e licença

O Case Builder funciona com um código de licença. Os instaladores estão na
[página de download](https://github.com/marcusnobrega-eng/HydroPol2D-Case-Builder-releases) pública,
em **Releases**. O código chega por e-mail, enviado por Marcus N. Gomes Jr., que desenvolve o
HydroPol2D.

**Contato:** Marcus N. Gomes Jr., [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).

## 1. Peça uma licença {#ask-for-a-license}

Escreva para o Marcus informando:

- o seu nome e o e-mail que a licença deve levar (o código guarda os dois);
- o seu computador: um Mac com Apple silicon (M1 ou mais recente) ou Windows (64 bits).

Você recebe o seu código de licença, uma linha longa de texto que começa com `HP2D1-`. Cada código
tem um último dia de validade.

## 2. Baixe {#download}

Na página de download, abra **Releases** e baixe o zip do seu computador.

| Computador | Arquivo | Espaço livre em disco |
|---|---|---|
| Mac com Apple silicon (M1 ou mais recente) | `HydroPol2D-Case-Builder-macOS-arm64.zip` | cerca de 600 MB, mais os dados que você baixar |
| Windows (64 bits) | `HydroPol2D-Case-Builder-Windows-x64.zip` | cerca de 600 MB, mais os dados que você baixar |

As notas da versão listam o checksum SHA-256 de cada zip.

## 3. Instale {#install}

### Mac (Apple silicon) {#mac-apple-silicon}

1. Descompacte `HydroPol2D-Case-Builder-macOS-arm64.zip`.
2. Arraste o **HydroPol2D Case Builder** para a pasta **Aplicativos** (**Applications**).
3. Dê um clique duplo nele. Na primeira vez, o macOS avisa que não consegue verificar se o app
   contém software malicioso. Clique em **Concluído** (**Done**).
4. Abra **Ajustes do Sistema › Privacidade e Segurança** (**System Settings › Privacy & Security**).
   Role até a mensagem sobre o HydroPol2D Case Builder e clique em **Abrir Mesmo Assim** (**Open
   Anyway**). Confirme com a sua senha.

Os passos 3 e 4 são feitos só uma vez. Se você prefere o Terminal, este comando deixa o macOS abrir
o app sem o passo 4:

```bash
xattr -dr com.apple.quarantine "/Applications/HydroPol2D Case Builder.app"
```

### Windows (64 bits) {#windows-64-bit}

1. Descompacte `HydroPol2D-Case-Builder-Windows-x64.zip` em uma pasta que você vá manter, por
   exemplo `Documents\HydroPol2D Case Builder`.
2. Dê um clique duplo em **HydroPol2D Case Builder.exe**.
3. Se o Windows mostrar "O Windows protegeu o computador", clique em **Mais informações** e depois
   em **Executar assim mesmo**.

## 4. Inicie e ative {#activate}

Ao abrir o app, aparece uma janela pequena. Ela inicia o Case Builder e, depois de alguns segundos,
o abre no seu navegador. Na primeira vez, a página pede o seu código. Cole o código inteiro em
**License code** e clique em **Activate**.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-license.png')} width="760" alt="A página do Case Builder que pede um código de licença, com a caixa License code, o botão Activate e a linha de contato" />
</p>

<p align="center">
  <em>Figura 1. A página de licença. Cole o código que começa com HP2D1- e clique em Activate. Depois disso, a página abre direto em Prepare a case.</em>
</p>

Depois da ativação, uma linha no alto da página mostra para quem é a licença e o último dia de
validade.

## Trabalhando com o app {#working-with-the-app}

- Mantenha a janela pequena aberta enquanto trabalha. **Open in browser** traz a página de volta se
  você fechou a aba dela. **Quit**, ou fechar a janela pequena, encerra o Case Builder.
- A página fica em `http://127.0.0.1:8501`, ou na próxima porta livre. Só o seu próprio computador
  consegue abri-la. O próprio Case Builder roda no seu computador, e os seus casos ficam nele.
- Os casos novos vão para `Documents/HydroPol2D Case Builder/outputs`, na sua pasta pessoal, a menos
  que você escolha outra pasta em **Folders and advanced paths** (veja
  [Configurações do caso](settings#folders)).
- O primeiro caso de uma região baixa os dados dela. Os casos seguintes os reaproveitam do cache.

## Sobre a sua licença {#about-your-license}

- O seu código é pessoal. Ele funciona em qualquer computador em que você instalar o Case Builder.
  Digite o mesmo código em cada um. Por favor, não o compartilhe.
- O Case Builder confere o código no próprio computador. Ele não precisa de internet para isso.
- A página avisa quando faltam menos de 30 dias. Para um código novo, escreva de novo para o Marcus.
- O Case Builder guarda o código em `license.txt`, nesta pasta:
  - Mac: `~/Library/Application Support/HydroPol2D Case Builder/`
  - Windows: `%APPDATA%\HydroPol2D Case Builder\`

  Para digitar outro código, apague esse arquivo e abra o Case Builder de novo.
- Mantenha a data do computador correta. O Case Builder se recusa a iniciar quando a data é
  atrasada mais de dois dias em relação à última vez em que ele foi usado.
- Um código do HydroPol2D Studio não abre o Case Builder. O Studio tem o Case Builder embutido
  (**New model**), com o código do próprio Studio.

Os termos da licença estão em `LICENSE.txt`, ao lado do app no zip. As partes de código aberto do
app e as suas licenças estão listadas em `THIRD_PARTY_NOTICES.txt`. Os conjuntos de dados de
entrada mantêm as suas próprias licenças e termos.

## Desinstalar {#uninstalling}

Apague o **HydroPol2D Case Builder** da pasta Aplicativos (Mac) ou a pasta dele (Windows). O Case
Builder também guarda os itens abaixo, que você pode apagar quando não precisar mais deles:

| O quê | Mac | Windows |
|---|---|---|
| Código de licença | `~/Library/Application Support/HydroPol2D Case Builder/` | `%APPDATA%\HydroPol2D Case Builder\` |
| Dados e ferramentas baixados (podem ocupar vários GB) | `~/.cache/hydropol2d-case-builder/` | `%USERPROFILE%\.cache\hydropol2d-case-builder\` |
| Token do NASA Earthdata (se você salvou um) | `~/.config/hydropol2d-case-builder/earthdata_token` | `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token` |

O HydroPol2D Studio usa o mesmo cache de dados. Apague-o só se nenhum dos dois programas precisar
dele. Os seus casos continuam nas pastas que você escolheu para eles.
