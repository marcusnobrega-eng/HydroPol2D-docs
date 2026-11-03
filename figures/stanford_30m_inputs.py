r"""Input maps of the San Francisquito 30 m example: terrain and land cover.

Draws the two spatial inputs of Examples/Stanford in the MATLAB repository: the USGS 3DEP
DEM (10 m averaged to 30 m) with a hillshade, and ESA WorldCover 2020 land cover with the
share of each class. Searsville Lake, where the example's deepest water is, is marked.

    python3 figures/stanford_30m_inputs.py <MATLAB repository folder> [preview-folder]

writes static/img/examples/stanford-30m-inputs{,.pt,.es}.svg.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import rasterio
from matplotlib.colors import LightSource, LinearSegmentedColormap, ListedColormap

from site_style import BOLD, INK, LIGHT, SOFT, STATIC, Sheet, oklch_hex

W, H = 680, 880
MAP_W, MAP_H = 420, 350
ROW_A, ROW_B = 76, 506  # top of each map

# The example's deepest water (5.87 m) is in the Searsville Lake basin (EPSG:3310).
SEARSVILLE_XY = (-197415.0, -65085.0)

# ESA WorldCover class codes and the product's own colours.
WORLDCOVER = {
    10: "#006400", 20: "#ffbb22", 30: "#ffff4c", 40: "#f096ff", 50: "#fa0000",
    60: "#b4b4b4", 70: "#f0f0f0", 80: "#0064c8", 90: "#0096a0", 95: "#00cf75", 100: "#fae6a0",
}

LABELS = {
    "en": {
        "a": "Terrain", "a_src": "USGS 3DEP, 10 m averaged to 30 m",
        "b": "Land cover", "b_src": "ESA WorldCover 2020, share of the domain",
        "elev": "Elevation (m)", "lake": "Searsville Lake", "km": "5 km",
        "classes": {10: "Tree cover", 20: "Shrubland", 30: "Grassland", 40: "Cropland",
                    50: "Built-up", 60: "Bare / sparse", 70: "Snow and ice",
                    80: "Permanent water", 90: "Herbaceous wetland", 95: "Mangroves",
                    100: "Moss and lichen"},
    },
    "pt": {
        "a": "Terreno", "a_src": "USGS 3DEP, 10 m agregado para 30 m",
        "b": "Cobertura do solo", "b_src": "ESA WorldCover 2020, fração do domínio",
        "elev": "Elevação (m)", "lake": "Lago Searsville", "km": "5 km",
        "classes": {10: "Cobertura arbórea", 20: "Arbustos", 30: "Campo", 40: "Agricultura",
                    50: "Área construída", 60: "Solo exposto / esparso",
                    70: "Neve e gelo", 80: "Água permanente", 90: "Área úmida herbácea",
                    95: "Mangue", 100: "Musgo e líquen"},
    },
    "es": {
        "a": "Terreno", "a_src": "USGS 3DEP, 10 m agregado a 30 m",
        "b": "Cobertura del suelo", "b_src": "ESA WorldCover 2020, fracción del dominio",
        "elev": "Elevación (m)", "lake": "Lago Searsville", "km": "5 km",
        "classes": {10: "Cubierta arbórea", 20: "Matorral", 30: "Pastizal", 40: "Cultivos",
                    50: "Zona construida", 60: "Suelo desnudo / escaso",
                    70: "Nieve y hielo", 80: "Agua permanente", 90: "Humedal herbáceo",
                    95: "Manglar", 100: "Musgo y liquen"},
    },
}

# Hypsometric ramp in OKLCH: green lowlands, tan hills, brown ridges.
ELEVATION_CMAP = LinearSegmentedColormap.from_list("elevation", [
    oklch_hex(0.83, 0.085, 150), oklch_hex(0.79, 0.090, 125), oklch_hex(0.76, 0.075, 90),
    oklch_hex(0.62, 0.065, 62), oklch_hex(0.48, 0.050, 50)])


def read(path: Path) -> tuple[np.ndarray, rasterio.coords.BoundingBox]:
    with rasterio.open(path) as src:
        values = src.read(1).astype("float64")
        if src.nodata is not None:
            values[values == src.nodata] = np.nan
        return values, src.bounds


def map_axes(sheet: Sheet, x: float, y: float, bounds) -> object:
    ax = sheet.fig.add_axes((x / W, 1 - (y + MAP_H) / H, MAP_W / W, MAP_H / H))
    ax.set_xlim(bounds.left, bounds.right)
    ax.set_ylim(bounds.bottom, bounds.top)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    return ax


def draw(lang: str, matlab_repo: Path, preview: Path | None) -> Path:
    t = LABELS[lang]
    static = matlab_repo / "Examples" / "Stanford" / "Static"
    dem, bounds = read(static / "DEM.tif")
    lulc, _ = read(static / "LULC.tif")
    extent = (bounds.left, bounds.right, bounds.bottom, bounds.top)
    s = Sheet(W, H, "stanford-30m-inputs")

    # a: terrain with a hillshade
    ax_x = 28
    s.text(ax_x, ROW_A - 42, t["a"], bold=True, size=11)
    s.text(ax_x, ROW_A - 22, t["a_src"], c=SOFT)
    ax = map_axes(s, ax_x, ROW_A, bounds)
    valid = np.isfinite(dem)
    lo, hi = np.nanpercentile(dem, 0.5), np.nanpercentile(dem, 99.5)
    filled = np.where(valid, dem, np.nanmin(dem))
    rgb = LightSource(azdeg=315, altdeg=45).shade(
        filled, cmap=ELEVATION_CMAP, blend_mode="soft", vert_exag=2.0, dx=30.0, dy=30.0,
        vmin=lo, vmax=hi)
    rgb[..., 3] = valid.astype(float)
    ax.imshow(rgb, extent=extent, interpolation="nearest", zorder=1)
    lake_x, lake_y = SEARSVILLE_XY
    ax.plot([lake_x], [lake_y], marker="o", ms=6, mfc="none", mec=INK, mew=1.4, zorder=3)
    ax.annotate(t["lake"], (lake_x, lake_y), xytext=(lake_x - 5200, lake_y + 3300),
                fontproperties=LIGHT, fontsize=9.5, color=INK, zorder=3,
                arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.9})
    bar_x, bar_y = bounds.left + 600, bounds.bottom + 900
    ax.plot([bar_x, bar_x + 5000], [bar_y, bar_y], color=INK, lw=2.0, solid_capstyle="butt")
    ax.text(bar_x + 2500, bar_y + 450, t["km"], fontproperties=LIGHT, fontsize=9.5,
            color=INK, ha="center", va="bottom")

    cb_x = ax_x + MAP_W + 18
    cax = s.fig.add_axes((cb_x / W, 1 - (ROW_A + 300) / H, 12 / W, 250 / H))
    ramp = np.linspace(lo, hi, 256)[:, None]
    cax.imshow(ramp, cmap=ELEVATION_CMAP, aspect="auto", origin="lower",
               extent=(0, 1, lo, hi))
    cax.set_xticks([])
    cax.yaxis.tick_right()
    ticks = [v for v in range(0, 1000, 200) if lo <= v <= hi]
    cax.set_yticks(ticks)
    cax.set_yticklabels([str(v) for v in ticks], fontproperties=LIGHT, fontsize=9.5, color=INK)
    cax.tick_params(length=3, color=INK, width=0.8)
    for spine in cax.spines.values():
        spine.set_edgecolor(INK)
        spine.set_linewidth(0.8)
    s.text(cb_x - 2, ROW_A + 32, t["elev"], size=9.5)

    # b: land cover, legend with the share of the active cells
    bx = ax_x
    s.text(bx, ROW_B - 42, t["b"], bold=True, size=11)
    s.text(bx, ROW_B - 22, t["b_src"], c=SOFT)
    ax = map_axes(s, bx, ROW_B, bounds)
    present = [code for code in WORLDCOVER if np.any(lulc == code)]
    index = np.full(lulc.shape, np.nan)
    for i, code in enumerate(present):
        index[lulc == code] = i
    ax.imshow(np.ma.masked_invalid(index), extent=extent, interpolation="nearest",
              cmap=ListedColormap([WORLDCOVER[c] for c in present]),
              vmin=-0.5, vmax=len(present) - 0.5, zorder=1)
    ax.plot([lake_x], [lake_y], marker="o", ms=6, mfc="none", mec=INK, mew=1.4, zorder=3)

    total = np.isfinite(lulc).sum()
    shares = sorted(((np.sum(lulc == c) / total, c) for c in present), reverse=True)
    lx, ly = bx + MAP_W + 10, ROW_B + 40
    for row, (share, code) in enumerate(shares):
        y = ly + 26 * row
        s.box(lx, y - 7, 14, 14, fill=WORLDCOVER[code], edge=INK, radius=2, lw=0.6)
        pct = f"{100 * share:.1f}%" if share >= 0.001 else "<0.1%"
        s.text(lx + 62, y, pct, ha="right", c=SOFT)
        s.text(lx + 70, y, t["classes"][code])

    return s.save(STATIC / "examples", lang, preview)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    matlab_repo = Path(sys.argv[1]).expanduser().resolve()
    preview = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    if preview is not None:
        preview.mkdir(parents=True, exist_ok=True)
    for lang in ("en", "pt", "es"):
        print(draw(lang, matlab_repo, preview))


if __name__ == "__main__":
    main()
