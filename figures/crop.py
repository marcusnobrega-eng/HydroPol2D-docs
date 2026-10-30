"""Save zoomed crops of a figure PNG (rendered at 200 dpi, so 2 px per figure px).

    python -B crop.py c1_data_to_results.png name x0 y0 x1 y1 [name x0 y0 x1 y1 ...]

Coordinates are figure px (the drawing units); crops are saved as crop_<name>.png, scaled x2.
"""
import sys
from pathlib import Path
from PIL import Image

src = Path(sys.argv[1])
im = Image.open(src)
args = sys.argv[2:]
for k in range(0, len(args), 5):
    name, *box = args[k:k + 5]
    x0, y0, x1, y1 = (int(float(v) * 2) for v in box)
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    out = src.parent / f"crop_{name}.png"
    c.save(out)
    print(out.name, c.size)
