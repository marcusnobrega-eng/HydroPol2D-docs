---
title: Install and license
---

# Install and license

HydroPol2D Studio, the desktop program of HydroPol2D-Python, runs with a license code. Codes are
not sold or downloaded on this site: write to Marcus N. Gomes Jr., who develops HydroPol2D, and he
sends you the installer and your code.

**Contact:** Marcus N. Gomes Jr., [marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com).

## 1. Ask for a license {#ask-for-a-license}

Write to Marcus with:

- your name and the email address the license should carry (the code holds both);
- your computer: a Mac with Apple silicon (M1 or later) or Windows (64-bit).

You receive two things:

- the installer for your computer, a `.zip` file;
- your license code, a long line of text that starts with `HP2D1-`. Each code has a last valid day.

There is no installer for Macs with an Intel processor: JAX, the numerical library the model
runs on, has published no version for them since December 2024. There is no installer for Linux
either.

## 2. Install {#install}

### Mac (Apple silicon) {#mac-apple-silicon}

1. Unzip `HydroPol2D-Studio-macOS-arm64.zip`.
2. Drag **HydroPol2D Studio** into your **Applications** folder.
3. Double-click it. The first time, macOS says it cannot check the app for malicious software.
   Click **Done**.
4. Open **System Settings › Privacy & Security**, scroll down to the message about HydroPol2D
   Studio and click **Open Anyway**. Confirm with your password.

You do steps 3 and 4 only once.

### Windows (64-bit) {#windows-64-bit}

1. Unzip `HydroPol2D-Studio-Windows-x64.zip` into a folder you keep, for example
   `Documents\HydroPol2D Studio`.
2. Double-click **HydroPol2D Studio.exe**.
3. If Windows shows "Windows protected your PC", click **More info**, then **Run anyway**.

## 3. Activate {#activate}

The first time Studio opens, the license window asks for your code. Paste the whole code and click
**Activate**. Studio then shows who the license is for and its last day, and opens on Home.
**Help > About HydroPol2D Studio** shows the same line later.

- The same code works on every computer you install Studio on: enter it on each one.
- Studio checks the code on your computer and needs no internet for this.

## Renewing or changing the code {#renewing-or-changing-the-code}

- Studio tells you when fewer than 30 days are left. For a new code, write to Marcus again.
- Studio keeps the code in `license.txt`, in this folder:
  - Mac: `~/Library/Application Support/HydroPol2D Studio/`
  - Windows: `%APPDATA%\HydroPol2D Studio\`

  To enter a different code, delete that file and open Studio again.
- Keep your computer's date correct. Studio refuses to start when the date is set back more than
  two days before the last time Studio was used.

## Uninstalling {#uninstalling}

Delete **HydroPol2D Studio** from Applications (Mac) or its folder (Windows). Studio also keeps
these, which you can delete when you no longer need them:

| What | Mac | Windows |
|---|---|---|
| License code | `~/Library/Application Support/HydroPol2D Studio/` | `%APPDATA%\HydroPol2D Studio\` |
| Crash reports and error log | `~/Library/Logs/HydroPol2D Studio/` | `%LOCALAPPDATA%\HydroPol2D Studio\Logs\` |
| Downloaded data and tools (can be several GB) | `~/.cache/hydropol2d-case-builder/` | `%USERPROFILE%\.cache\hydropol2d-case-builder\` |
| Window layout and recent models | `~/Library/Preferences/com.hydropol2d.Studio.plist` | Registry: `HKEY_CURRENT_USER\Software\HydroPol2D\Studio` |
| Copernicus and NASA Earthdata logins | Keychain Access: entries named `hydropol2d:…` | Credential Manager: entries named `hydropol2d:…` |
| NASA Earthdata token (if you saved one) | `~/.config/hydropol2d-case-builder/earthdata_token` | `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token` |

Your models and results stay in the folders you chose for them.
