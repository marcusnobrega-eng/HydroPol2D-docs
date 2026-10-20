---
title: Ecosystem Architecture
---

# Ecosystem Architecture

HydroPol2D uses one versioned mesh package across its MATLAB and Python
implementations. This prevents each solver from rebuilding geometry or
interpreting mesh properties differently.

## Repository responsibilities

| Component | Responsibility | Candidate version |
|---|---|---|
| HydroBathyDEM | Production generator for regular and Voronoi meshes, terrain products, conservative raster overlap, subgrid tables, UGRID, GeoPackage inspection layers, and mesh QA. | `0.3.0rc1` |
| HydroPol2D-Python | Python model engine and Studio. It validates and consumes the mesh package; it does not regenerate hydraulic mesh geometry. | `0.8.0rc1` |
| HydroPol2D-MATLAB | MATLAB reference implementation and compatible consumer of the same mesh package. | `1.18.0-rc1` |
| HydroPolMesh | Archived migration prototype. Useful validated capabilities are being retained in HydroBathyDEM; it is not a production runtime dependency. | prototype |

The stable MATLAB `v1.17.0` release remains the numerical reference while the
coordinated release candidates complete parity and long-duration checks.

## Shared mesh contract

Mesh contract `1.0` requires the package to declare:

- cell and face geometry, connectivity, areas, lengths, and orientation;
- zero-based file indices, converted explicitly to one-based MATLAB indices;
- `cell_cfl_width_m`, defined from the minimum centre separation normal to a face;
- CRS, units, source resolution, provenance, and contract version;
- conservative raster-to-cell overlap weights;
- compatible cell-level and face-level subgrid tables when subgrid routing is enabled.

Both solvers reject malformed indices, zero-length faces, negative areas,
missing units or CRS, undefined CFL widths, non-conservative overlap, and
incompatible subgrid tables. They do not silently reconstruct missing mesh
properties.

## Subgrid formulations

The following options solve different representations and are not aliases:

| Option | Intended representation |
|---|---|
| Neal channel | Rectangular channel embedded in the structured raster grid; supported with local-inertial routing. |
| Structured lookup subgrid | SFINCS-style depth-dependent cell and face lookup tables on a structured grid. |
| Voronoi subgrid | Area, wetted-perimeter, and conductance relations on an unstructured Voronoi mesh. |

Legacy names are accepted only by case migration. Incompatible combinations
must be corrected before a simulation can start.

## Release status

The release candidates are integration builds, not final coordinated releases.
Final publication requires clean-clone installation, MATLAB-Python comparisons
on identical mesh and hydrologic inputs, the Pune 2 h, 6 h, and 12 h runs, and
passing scientific, Studio, lint, type, and provenance checks.
