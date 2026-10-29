---
title: Instalação e licença
---

# Instalação e licença

O HydroPol2D Studio, o programa desktop do HydroPol2D-Python, funciona com um código de licença. Os
códigos não são vendidos nem baixados neste site: escreva para Marcus N. Gomes Jr., que desenvolve o
HydroPol2D, e ele envia o instalador e o seu código.

**Contato:** Marcus N. Gomes Jr., [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).

## 1. Peça uma licença {#ask-for-a-license}

Escreva para o Marcus informando:

- o seu nome e o e-mail que a licença deve levar (o código guarda os dois);
- o seu computador: um Mac com Apple silicon (M1 ou mais recente) ou Windows (64 bits).

Você recebe duas coisas:

- o instalador para o seu computador, um arquivo `.zip`;
- o seu código de licença, uma linha longa de texto que começa com `HP2D1-`. Cada código tem um
  último dia de validade.

Não há instalador para Macs com processador Intel: o JAX, a biblioteca numérica em que o modelo
roda, não publica versões para eles desde dezembro de 2024. Também não há instalador para
Linux.

## 2. Instale {#install}

### Mac (Apple silicon) {#mac-apple-silicon}

1. Descompacte `HydroPol2D-Studio-macOS-arm64.zip`.
2. Arraste o **HydroPol2D Studio** para a pasta **Aplicativos** (**Applications**).
3. Dê um clique duplo nele. Na primeira vez, o macOS avisa que não consegue verificar se o app
   contém software malicioso. Feche esse aviso.
4. Abra **Ajustes do Sistema › Privacidade e Segurança** (**System Settings › Privacy & Security**),
   role até a mensagem sobre o HydroPol2D Studio e clique em **Abrir Mesmo Assim** (**Open
   Anyway**). Confirme com a sua senha.

Os passos 3 e 4 são feitos só uma vez.

### Windows (64 bits) {#windows-64-bit}

1. Descompacte `HydroPol2D-Studio-Windows-x64.zip` em uma pasta que você vá manter, por exemplo
   `Documentos\HydroPol2D Studio`.
2. Dê um clique duplo em **HydroPol2D Studio.exe**.
3. Se o Windows mostrar "O Windows protegeu o computador", clique em **Mais informações** e depois
   em **Executar assim mesmo**.

## 3. Ative {#activate}

Na primeira vez que o Studio abre, a janela de licença pede o seu código. Cole o código inteiro e
clique em **Activate**. O Studio então mostra para quem é a licença e o último dia de validade, e
abre na tela Home. **Help > About HydroPol2D Studio** mostra a mesma informação depois.

- O mesmo código funciona em todos os computadores em que você instalar o Studio: digite o código
  em cada um.
- O Studio confere o código no próprio computador e não precisa de internet para isso.

## Renovar ou trocar o código {#renewing-or-changing-the-code}

- O Studio avisa quando faltam menos de 30 dias. Para um código novo, escreva de novo para o Marcus.
- O Studio guarda o código em `license.txt`, nesta pasta:
  - Mac: `~/Library/Application Support/HydroPol2D Studio/`
  - Windows: `%APPDATA%\HydroPol2D Studio\`

  Para digitar outro código, apague esse arquivo e abra o Studio de novo.
- Mantenha a data do computador correta. O Studio se recusa a abrir quando a data é atrasada mais de
  dois dias em relação à última vez em que ele foi usado.

## Desinstalar {#uninstalling}

Apague o **HydroPol2D Studio** da pasta Aplicativos (Mac) ou a pasta dele (Windows). O Studio também
guarda os itens abaixo, que você pode apagar quando não precisar mais deles:

| O quê | Mac | Windows |
|---|---|---|
| Código de licença | `~/Library/Application Support/HydroPol2D Studio/` | `%APPDATA%\HydroPol2D Studio\` |
| Relatórios de falha e log de erros | `~/Library/Logs/HydroPol2D Studio/` | `%LOCALAPPDATA%\HydroPol2D Studio\Logs\` |
| Dados e ferramentas baixados (podem ocupar vários GB) | `~/.cache/hydropol2d-case-builder/` | `%USERPROFILE%\.cache\hydropol2d-case-builder\` |
| Layout da janela e modelos recentes | `~/Library/Preferences/com.hydropol2d.Studio.plist` | Registro: `HKEY_CURRENT_USER\Software\HydroPol2D\Studio` |
| Logins do Copernicus e do NASA Earthdata | Acesso às Chaves: itens chamados `hydropol2d:…` | Gerenciador de Credenciais: itens chamados `hydropol2d:…` |
| Token do NASA Earthdata (se você salvou um) | `~/.config/hydropol2d-case-builder/earthdata_token` | `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token` |

Os seus modelos e resultados continuam nas pastas que você escolheu para eles.
