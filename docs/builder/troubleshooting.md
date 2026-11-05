---
title: Troubleshooting
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Troubleshooting

## Starting the app {#starting}

**The browser does not open.** Click **Open in browser** in the small window. The page is at
`http://127.0.0.1:8501`, or the next free port.

**The small window says the Case Builder stopped.** It names a log file. Send that file with your
question to Marcus N. Gomes Jr. ([marcusnobrega.engcivil@gmail.com](mailto:marcusnobrega.engcivil@gmail.com)).

**macOS does not open the app.** Allow it once in **System Settings › Privacy & Security** with
**Open Anyway** ([Install and license](install-and-license#mac-apple-silicon)).

## License {#license}

**"This is a HydroPol2D Studio code".** You pasted your Studio code. The Case Builder needs its own
code.

**The license expired, or fewer than 30 days are left.** Write to Marcus for a new code. To enter
it, delete `license.txt` from the license folder and open the Case Builder again
([About your license](install-and-license#about-your-license)).

**The Case Builder refuses to start after a date change.** Set the computer's date and time
correctly. The Builder refuses to start when the date is set back more than two days before its
last use.

## Before the preview {#before-the-preview}

**"Confirm riverbed hydraulic conductivity when river-groundwater exchange is enabled."** Open
**Hydraulic parameters**, check **Riverbed conductivity (m/s)** and tick **Confirm this riverbed
conductivity for the case**, or untick **River-groundwater exchange**.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-riverbed-confirm.png')} width="760" alt="The ready message, the Preview domain and cost button and a red error box that asks to confirm the riverbed hydraulic conductivity when river-groundwater exchange is enabled" />
</p>

<p align="center">
  <em>Figure 1. The preview stops until the riverbed conductivity is confirmed.</em>
</p>

**"This case cannot be prepared yet:" with an account named.** Set up that account
([Data sources and accounts](data-accounts)), then reload the page.

**The rainfall period is not available.** IMERG, AORC and MSWEP have their own periods, which the
page shows. Choose dates inside them, or another rainfall product. AORC also needs the whole
domain inside the contiguous United States.

**The city cannot be found.** Check the spelling of the city and the country as GHSL writes them.
If GHSL does not have the boundary you need, choose **Polygon file** and give your own polygon.

**"Requested … m cells are finer than the DEM's …".** The cell size cannot be finer than the
terrain. Use a larger cell size, or a finer local DEM.

**"The coarse quadtree resolution must be a power-of-two multiple of the fine resolution."** Make
the coarse cell size 2, 4, 8 or more times the fine size.

## The preview {#the-preview}

**The case is too large.** Stop after the preview. Use a larger cell size, a quadtree grid, or a
smaller area, or move the build and the run to a computer with more memory. Memory follows the
matrix cells more than the active cells.

**The catchment is wrong or far too large.** Choose another **Outlet candidate**, change the
**Snap radius**, or move the outlet onto the river.

## Preparing the case {#preparing}

**Copernicus (CDS) fails or waits for a long time.** CDS puts each request in a queue, which can
take minutes or longer. If it fails, check that `.cdsapirc` has the current URL and token with no
extra quotes, and that you accepted the ERA5 and ERA5-Land terms on the CDS website.

**IMERG returns 401 or 403.** Your Earthdata token expired or the GPM terms are not accepted. Make
a new token and check the file permissions.

**MSWEP does not download.** Run `rclone lsd --drive-shared-with-me GoogleDrive:` and check that the
approved folder is listed. **MSWEP rclone folder** must point at its `Hourly` or `3hourly` folder.
If the folder is listed but a path gives "directory not found", fill **Shared-folder ID** with the
folder's Google Drive ID, from:

```bash
rclone lsjson --dirs-only --drive-shared-with-me --include 'MSWEP_V316_test/' GoogleDrive:
```

**A rainfall time step is missing** (local rainfall files). The folder must hold every time step
from the start of the warm-up to the end, with the names in [Case settings](settings#rainfall-folders).

**The build stopped part way.** Read the **Process log**. Downloaded files are kept, so **Prepare
complete case** resumes after you fix the cause.

## Checking and running {#checking-and-running}

**Preflight fails.** Read the listed problems, or `quality_report/preflight.json`
([Check a case](check-a-case)).

**"The final model-resolution D8 area differs by more than a factor of two from the preliminary
HydroSHEDS area."** The outlet probably snapped to another river. Choose another candidate or
another snap radius, preview, and prepare the case again.

**The MATLAB run does not start.** Check **MATLAB executable**. If the HydroPol2D MATLAB folder does
not exist yet, the app downloads it with Git: install Git, or give a folder that already holds
HydroPol2D MATLAB.

**"HydroPol2D Python comes with HydroPol2D Studio".** The app does not download HydroPol2D
Python. Open `hydropol_python/case.yaml` in HydroPol2D Studio ([Run the case](run-the-case#studio)).

**The model runs out of memory.** Use a coarser grid to test, and run fine regional cases on a
workstation or a cluster.

**Albedo is 0.25 everywhere.** This is expected in this version.
