---
title: Data sources and accounts
---

# Data sources and accounts

Most data the Case Builder uses are open downloads. Three sources need an account of your own.
Your logins stay on your computer: the Builder reads them from your own files or environment
variables, and never writes them into a case.

| Source | Needed for | Account |
|---|---|---|
| Copernicus Climate Data Store (CDS) | ERA5 weather, ERA5-Land starting soil water, ERA5 rain, and the GloFAS and GTSM boundaries | free, every case made in the app |
| NASA Earthdata | IMERG rain, and leaf area when the ORNL MODIS service is unavailable | free |
| MSWEP (GloH2O) | MSWEP rain | approval from GloH2O, and rclone for its Google Drive folder |

AORC rain (United States) and the static maps (terrain, basins, land cover, soils, groundwater)
need no account. Leaf area comes from the ORNL MODIS web service, with no account. When that
service is unavailable, the Builder takes it from NASA LP DAAC, which uses your Earthdata login.

The page checks the accounts before it downloads anything. When one is missing, a yellow box
says "This case cannot be prepared yet:" and names it, and **Prepare complete case** stays greyed
out.

## Copernicus Climate Data Store {#copernicus-cds}

1. Create an account at the [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/).
2. Log in and accept the terms of use of the ERA5 and ERA5-Land datasets.
3. Copy your personal access token from your CDS profile page.
4. Create a text file named `.cdsapirc` in your home folder with these two lines:

   ```yaml
   url: https://cds.climate.copernicus.eu/api
   key: YOUR_CDS_PERSONAL_ACCESS_TOKEN
   ```

   On a Mac the file is `~/.cdsapirc`, on Windows `%USERPROFILE%\.cdsapirc`. On a Mac, protect it
   with `chmod 600 ~/.cdsapirc`.

The token can also come from the environment variable `CDSAPI_KEY`. CDS puts each request in a
queue, so the first download of a case can wait some minutes before it starts.

## NASA Earthdata {#nasa-earthdata}

1. Create a [NASA Earthdata Login](https://urs.earthdata.nasa.gov/) account and accept the terms
   for GPM IMERG data.
2. Generate a token in your Earthdata profile.
3. Save the token, alone on one line, in this file:
   - Mac: `~/.config/hydropol2d-case-builder/earthdata_token`
   - Windows: `%USERPROFILE%\.config\hydropol2d-case-builder\earthdata_token`

   On a Mac, protect the folder and the file:

   ```bash
   mkdir -p ~/.config/hydropol2d-case-builder
   chmod 700 ~/.config/hydropol2d-case-builder
   chmod 600 ~/.config/hydropol2d-case-builder/earthdata_token
   ```

The Builder also accepts the token in the environment variable `EARTHDATA_TOKEN`, a `~/.netrc`
file with your Earthdata login, or the variables `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD`.

## MSWEP {#mswep}

MSWEP needs prior approval from GloH2O.

1. Ask for access on the [MSWEP page](https://www.gloh2o.org/). The approval email gives you a
   shared Google Drive folder.
2. Install [rclone](https://rclone.org) (on a Mac with Homebrew: `brew install rclone`).
3. Run `rclone config` and create a remote named `GoogleDrive` of type `drive`. Complete the
   authorization in your browser, and do not set the shared folder up as a Team Drive.
4. Check that the shared folder is visible:

   ```bash
   rclone lsd --drive-shared-with-me GoogleDrive:
   ```

When you choose **MSWEP (hourly)** or **MSWEP (3 hourly)**, the page searches your rclone remotes
for the authorized MSWEP folder. When it finds one, it says "Authorized MSWEP V3.16 folder found.
Automatic MSWEP download is ready." and fills **MSWEP rclone folder** and **Shared-folder ID
(optional)**. Both stay visible, and you can change them. The Builder downloads only the time
steps of the case, cuts them to the domain, and records the source in
`quality_report/mswep_download.json`. When a request crosses the end of the **Past** record, the
later time steps come from the **NRT** (near real time) folder by themselves.

The page warns that MSWEP V3.16 has a documented artificial trend in precipitation around 2015.
For trend studies over 1979 to 2021, use V2.80. Recent NRT files are preliminary and are revised
after their first release. MSWEP V3 is cited as Wang et al. (2026),
[MSWEP V3](https://arxiv.org/abs/2602.01436).

If you already have the rainfall as files, use **Existing rainfall directory (optional)** instead
([Case settings](settings#rainfall-folders)).

## Data licenses {#data-licenses}

The input datasets keep their own licenses and access terms, and you follow them when you use
their data. Each case records every source and its version in
`quality_report/public_static_sources.json` and in its `manifest.json`.
