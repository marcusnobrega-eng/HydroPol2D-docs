---
title: Working in Studio
---

# Working in Studio

## Edits, Save and Revert to saved

Edits go into the open model as you make them; only **Save** writes the model file.

- A typed value applies when you press Enter or Tab or leave the field. A tick box or a list choice
  applies at once. A half-typed number is never used.
- A table applies when a cell is finished, and once per paste or row removal.
- The header shows "Unsaved changes" until you **Save** (Cmd+S on a Mac, Ctrl+S elsewhere). Studio
  asks before closing or leaving a model with unsaved changes.
- **Save**, **Check inputs** and **Run** first take every edit that has not been applied yet.
- **Revert to saved**, on the Processes and Parameters pages and in the File menu, asks first, then
  opens the model file again and drops every change since the last save.

The mesh editor is the exception: it keeps **Apply edits** and **Discard edits**, and Apply writes
the edited mesh to the model folder at once.

## Values Studio cannot use

A value Studio cannot use gets a red border, and a red line under the page says why, for example
"Maximum model time step [s] must be a number." The other values still apply. **Save**, **Check
inputs** and **Run** refuse until the value is fixed.

## Error messages

An error message says what went wrong in a sentence, and under it why, in words: file names instead
of full paths, and no Python class names. The technical details are under **Show details**.
**Copy details** puts them on the clipboard, ready to attach to a problem report.

**Help > Open the log folder** opens the folder with Studio's log and crash reports.

## Theme

**View > Theme** offers **Match system** (the default), **Dark** and **Light**. Match system follows
the macOS or Windows appearance, also when it changes while Studio is open; a chosen theme also
sets the window title bar. The button at the foot of the left rail switches to the other theme.

## Menus and shortcuts

On Windows, use Ctrl for Cmd.

| Menu | Command | Shortcut |
|---|---|---|
| File | New model… | Cmd+N |
| File | Open model… | Cmd+O |
| File | Save model | Cmd+S |
| File | Save model as… | Shift+Cmd+S |
| File | Revert to saved | |
| File | Edit model file (YAML)… | |
| File | Open results… | |
| File | Quit | Cmd+Q (Alt+F4 on Windows) |
| View | Setup, Run, Results, Calibrate | Cmd+1, Cmd+2, Cmd+3, Cmd+4 |
| View | Theme: Match system, Dark, Light | |
| Help | About HydroPol2D Studio (version and licence) | |
| Help | Documentation (this website) | |
| Help | Open the log folder | |

Run has no shortcut on purpose: a model run can take a long time, and one key press should not
start one.

## Paths

Long paths, such as the model file, the DEM and the results folder, are shortened in the middle
("/Users/…/my_model/case.yaml") so the start and the file name stay in view; the whole path is in
the tooltip. **Show in Finder** (Explorer on Windows) opens the folder with the file selected.

## Small screens

Every page fits a 1280 × 720 window, the size a 1080p Windows laptop gives at its default 150 %
scaling. When the window is that short, the Study area tool rail shows icons only; each tool's
name is in its tooltip, and the labels come back when the window is taller.
