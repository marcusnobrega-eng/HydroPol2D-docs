---
title: Run and results
---

# Run and results

## Run

The Run workspace has two panes.

- **Outputs**: the output profile, the output folder, the recording intervals for maps, time
  series, native mesh output and raster stacks, how maps are stored during the run, and the
  animation settings.
- **Computing backend**: the backends this computer can run. In the Mac and Windows apps that is
  the CPU; Apple GPUs lack the 64-bit arithmetic the model needs.
- **Save results to**: the folder for this run. You may type another folder for this run only;
  **Show in Finder** (Explorer on Windows) opens it.
- **Check inputs** runs the input check, **Run model** starts the run, and **Cancel run** stops it.
  Run checks the inputs first.
- **Live diagnostics** charts the run at each saved interval, and the run log lists each step.

## Results

**Results** opens the output of a run, or a results package opened from Home. It has its own layer
panel, so changing a result overlay does not change the Study area map.

- Playback runs forward or backward and can loop, step by frame or jump to an elapsed or calendar
  time. Maximum, minimum and final maps summarize the active variable without changing the file.
- Right-click a result cell to plot its saved time series, export the cell data, inspect every
  saved map variable, or start a profile line.
- Maps export as PNG, PDF, SVG, GeoTIFF or MP4. Time-series charts keep independent left- and
  right-axis variables and export as PNG, PDF, SVG or CSV.
- For urban drainage, pipes, manholes, inlets and accepted internal boundaries can be coloured by a
  saved quantity at the selected time, and each one is also available as a named time series.
