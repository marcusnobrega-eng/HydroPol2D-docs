---
title: Preview and cost
---
import useBaseUrl from '@docusaurus/useBaseUrl';

# Preview and cost

**Preview domain and cost** draws the domain and estimates the size of the case in seconds,
before any large download. Nothing is built yet, so you can change the settings and preview again
until the domain is right. **Prepare complete case** stays greyed out until the preview matches
the current settings.

## Before the preview {#before-the-preview}

Above the two buttons, the page checks the request:

- the period each rainfall source has, for example "NASA IMERG Final Run availability: 1998-01-01
  through 2025-09-30";
- the accounts and tools the case needs. When one is missing, a yellow box says "This case cannot
  be prepared yet:" and names it (see [Data sources and accounts](data-accounts));
- for AORC, that the whole domain lies inside the AORC grid, which the preview confirms;
- when everything is in place: "Required credentials, source coverage, and local tools are ready
  for this request."

## What the preview shows {#what-the-preview-shows}

1. **Case files**: the folder of the case, in green. The preview already writes the request, the
   domain and the preview maps there.
2. **The domain on a map.** The map is interactive, over OpenTopoMap. The layer control switches
   to a street map or hides the overlays. The online map is only a background: it does not change
   the case.
3. **Estimated quadtree grid** (quadtree cases): the resolution zones of the mesh.
4. **Rivers entering the domain** (Urban Area Only): see [Choose the model area](model-area#urban-area-only).
5. **The size of the case**: six numbers, and for a quadtree grid the cells of each size.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-map.jpg')} width="760" alt="The preview of the Tucson urban basin: the ready message, the Preview domain and cost and Prepare complete case buttons, the green Case files line, and an interactive topographic map with the urban area in orange, the connected catchments and the upstream catchments in blue, and the river network" />
</p>

<p align="center">
  <em>Figure 1. The preview of the Tucson urban basin. The city (orange) lies downstream in the Santa Cruz River basin, so the upstream catchments reach south across the border into Mexico.</em>
</p>

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-quadtree.jpg')} width="560" alt="Estimated quadtree grid of the Tucson urban basin: the city covered by 90 m cells, a thin band of 180 m cells around it, and the rest of the basin in 360 m cells" />
</p>

<p align="center">
  <em>Figure 2. The quadtree zones of the same case: 90 m cells over the city and its buffer, a band of 180 m cells, and 360 m cells over the rest of the basin.</em>
</p>

For a Catchment case, the map shows the outlet you entered, the three candidate outlets on the
river network and a first outline of the catchment.

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-catchment.jpg')} width="760" alt="The preview of San Francisquito Creek on a topographic map, with the outlet entered as a red dot, the orange candidate outlets on the river network, the first outline of the catchment, and the matrix cells, active cells and basin area below" />
</p>

<p align="center">
  <em>Figure 3. The preview of San Francisquito Creek. The red dot is the outlet you entered, the orange dots are the candidate outlets, and the outline is a first sketch of the catchment. The complete build delineates the catchment again on the model grid.</em>
</p>

## The size of the case {#size}

| Number | What it means |
|---|---|
| **Matrix cells** | rows times columns of the rectangle around the whole domain |
| **Active cells** | the cells inside the domain |
| **Basin area** | the area of the domain, in km² |
| **Temporary transfer ceiling** | an upper bound of the source data the build downloads, static maps and forcing together |
| **Retained forcing inputs** | the rain and weather kept with the finished case |
| **Estimated saved outputs** | the size of the results the model will save, from the outputs you chose |

<p align="center">
  <img src={useBaseUrl('/img/builder/builder-preview-metrics.png')} width="760" alt="The six numbers of the Tucson quadtree preview: 1,743,840 matrix cells, 107,512 active cells, a basin area of 8,227 km2, a transfer ceiling of 195.2 MiB, 0.5 MiB of retained forcing and 1.36 GiB of saved outputs, then a table with 40,230 cells of 90 m, 8,426 of 180 m and 58,856 of 360 m, and the folded How these values are estimated panel" />
</p>

<p align="center">
  <em>Figure 4. The size of the Tucson case: 107,512 active cells on a 8,227 km² basin, under 200 MiB to download and about 1.4 GiB of results.</em>
</p>

Memory depends mostly on the matrix, not only on the active cells. A long or broken-up domain can
need more memory than its area suggests. **How these values are estimated** explains each number
and lists the download and the saved outputs by source. Some notes from it:

- The transfer counts the source values at each product's own resolution, over the domain and the
  period. It does not count the HydroPol2D rasters the build writes. MSWEP is counted as
  uncompressed values, so the real traffic is lower.
- Raw source files are removed after a successful build. A failed build keeps them, so the next
  attempt resumes.
- The saved-output estimate counts the selected files only, as uncompressed values.

Start large regional models at a coarse cell size, read the numbers, and go finer only when they
fit your computer.

## When the settings change {#settings-change}

Any change after a preview shows "Settings changed. Run the preview again before preparing this
case." The **Process log** at the bottom of the tab keeps the messages of the last preview or
build.
