r"""Input maps of the San Francisquito 10 m LiDAR example: terrain and land cover.

The figure of the 30 m example (stanford_30m_inputs.py) drawn from
Examples/Stanford/Static_10m_LiDAR: the 10 m USGS 3DEP DEM with a hillshade, and the 30 m
ESA WorldCover 2020 map the model reads on the 10 m grid.

    python3 figures/stanford_10m_inputs.py <MATLAB repository folder> [preview-folder]

writes static/img/examples/stanford-10m-inputs{,.pt,.es}.svg.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

from stanford_30m_inputs import LABELS, draw

SOURCES = {
    "en": ("USGS 3DEP, 10 m", "ESA WorldCover 2020 (30 m map), share of the domain"),
    "pt": ("USGS 3DEP, 10 m", "ESA WorldCover 2020 (mapa de 30 m), fração do domínio"),
    "es": ("USGS 3DEP, 10 m", "ESA WorldCover 2020 (mapa de 30 m), fracción del dominio"),
}


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    matlab_repo = Path(sys.argv[1]).expanduser().resolve()
    preview = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    if preview is not None:
        preview.mkdir(parents=True, exist_ok=True)
    labels = copy.deepcopy(LABELS)
    for lang, (terrain, land_cover) in SOURCES.items():
        labels[lang]["a_src"], labels[lang]["b_src"] = terrain, land_cover
    for lang in ("en", "pt", "es"):
        print(draw(lang, matlab_repo, preview, static_folder="Static_10m_LiDAR", cell_m=10.0,
                   name="stanford-10m-inputs", labels=labels))


if __name__ == "__main__":
    main()
