---
title: Run the case
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Run the case

A case that passed the check runs in HydroPol2D MATLAB or in HydroPol2D Studio, depending on
what you chose under **Prepare for**. The run panels appear below the result of the check, both
after **Prepare complete case** and on **Check a case**.

| Prepared for | Run it in | From |
|---|---|---|
| **HydroPol2D MATLAB** | HydroPol2D MATLAB (open source) | the **Run HydroPol2D MATLAB** panel, or MATLAB itself |
| **HydroPol2D Python** | HydroPol2D Studio | **Open existing model** in Studio, with `hydropol_python/case.yaml` |
| **Python and MATLAB** | either | both |

## In HydroPol2D MATLAB, from the app {#matlab-from-the-app}

You need MATLAB on your computer. The panel **Run HydroPol2D MATLAB** has:

- **HydroPol2D MATLAB folder**: a folder with the HydroPol2D MATLAB code. A folder that already
  holds it is used as it is, without updating it. If the folder does not exist, the app downloads
  HydroPol2D from its [GitHub repository](https://github.com/marcusnobrega-eng/HydroPol2D)
  (`main` branch) into it. That download needs [Git](https://git-scm.com).
- **MATLAB executable**: found by itself when MATLAB is installed in the usual place. Otherwise
  give its path, for example `/Applications/MATLAB_R2025b.app/bin/matlab` on a Mac or
  `C:\Program Files\MATLAB\R2025b\bin\matlab.exe` on Windows.

**Run HydroPol2D MATLAB** starts MATLAB in the background. The button is active only after the
check passed. **Refresh status** updates the page while the model runs:

- the state ("MATLAB is running in the background", "MATLAB simulation completed successfully",
  or the exit code when it stopped);
- a progress bar with the stage and the share of simulated time;
- **Simulated time**, **Time step**, **Elapsed** and **Estimated remaining**;
- the mean and maximum rainfall, the maximum depth, the outlet discharge, the total storage, the
  mass-balance error and the mean groundwater depth;
- the **MATLAB run log**, open by itself when the run fails.

When the run is complete, **Results** shows the maximum surface-water depth as a number, a map
and an animation, and names the maximum-depth GeoTIFF for a GIS. The status and the logs are in
`model_runs/` inside the case, and the results in `Outputs/`.

## In HydroPol2D MATLAB, by hand {#matlab-by-hand}

The case's `run_case.m` sets the case paths, dates, resolution, rainfall, boundary conditions,
outputs and execution options, then starts HydroPol2D. In MATLAB:

```matlab
addpath('/path/to/CASE_DIR/hydropol_matlab')
run_case('/path/to/HydroPol2D')
```

The first path is the case folder, the second your HydroPol2D MATLAB folder. `run_case.m` does
not change the configuration files of HydroPol2D: it passes the case to the model in memory, so
the same HydroPol2D folder can run many cases. A case on the native mesh (a quadtree grid, an Urban
Area Only case, or hydraulic tables) runs on the native mesh solver of HydroPol2D and writes a
native mesh result archive. See the
[MATLAB workflow](../getting-started/excel-workflow) for the model itself.

## In HydroPol2D Studio {#studio}

1. Open HydroPol2D Studio.
2. On **Home**, choose **Open existing model**.
3. Choose `hydropol_python/case.yaml` in the case folder.

The case opens in **Setup**, ready to check and run. From there Studio's tools work on it, for
example urban drainage, ponds, green infrastructure, crossings, results and calibration. See the
[Studio guide](../studio/overview).

The app's **Run HydroPol2D Python** panel asks for a folder that holds HydroPol2D Python. The app
does not download HydroPol2D Python, which comes with Studio. Without such a folder the panel
says so and points to Studio.

## Where the results go {#results}

| Run | Results |
|---|---|
| MATLAB, regular grid | `Outputs/`, with the result previews in `Outputs/PostProcessing/` |
| MATLAB, native mesh | `Outputs/Modeling_Results/Native/unstructured_results.nc` and the previews |
| Python | `Outputs/python/Modeling_Results/`: figures, static GeoTIFFs and animations |

The saved maps and their interval follow **Saved outputs** ([Case settings](settings#saved-outputs)).
