r"""Pictures of every tab of a MATLAB case workbook (HydroPol2D_Inputs.xlsx), as Excel shows them.

Each tab is drawn as an HTML grid from the workbook itself: column widths, row heights, fills,
fonts, borders, merged cells, hidden rows and columns, and the red corner of cells with a note.
Below the grid, the tab bar names every tab and marks the one shown. A headless Chromium
(Playwright) takes the picture, so nothing opens on screen. Long tabs show their first rows and
wide tabs their first columns, as a window would.

    python3 figures/workbook_tabs.py <case workbook .xlsx> [preview-folder]

writes static/img/workbook/<tab>.png.
"""

from __future__ import annotations

import datetime as dt
import html
import re
import sys
import tempfile
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "static" / "img" / "workbook"

MAX_ROWS = 34          # rows shown, like one window of a laptop screen
MAX_WIDTH_PX = 1500    # grid width before the columns are cut
DEFAULT_COL = 8.43     # Excel default column width (characters)
DEFAULT_ROW_PT = 15.0
SCALE = 2              # device pixels per CSS pixel
# Tabs cut earlier: the Rain and ET map lists hold another case's file paths, so the picture
# ends at the column titles of the first list.
ROW_LIMIT = {"Rain and ET": 20}
# Cells drawn as "(gauge name)": the Inflow hydrographs template keeps another case's gauge names.
LEFT_OUT = {"Inflow hydrographs": {"E2", "J2", "O2"}}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def col_px(width: float | None) -> int:
    return int(round((width if width else DEFAULT_COL) * 7 + 5))


def color(c, default=None):
    """'#rrggbb' for an ARGB colour; theme 0 and 1 (light 1, dark 1) as white and black."""
    if c is None:
        return default
    if c.type == "rgb" and isinstance(c.rgb, str) and len(c.rgb) == 8 and c.rgb != "00000000":
        return "#" + c.rgb[2:].lower()
    if c.type == "theme":
        return {0: "#ffffff", 1: "#000000"}.get(c.theme, default)
    return default


def text_of(cell) -> str:
    v = cell.value
    if v is None:
        return ""
    if isinstance(v, dt.datetime):
        fmt = cell.number_format.lower()
        if "h" in fmt:
            return v.strftime("%Y-%m-%d %H:%M:%S" if "ss" in fmt else "%Y-%m-%d %H:%M")
        return v.strftime("%Y-%m-%d")
    if isinstance(v, dt.date):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, float):
        if v.is_integer() and abs(v) < 1e15:
            return str(int(v))
        return f"{v:.10g}"
    return str(v)


def border_css(side) -> str:
    if side is None or side.style is None:
        return ""
    width = {"thin": 1, "hair": 1, "dotted": 1, "dashed": 1, "medium": 2, "thick": 3,
             "double": 3}.get(side.style, 1)
    style = {"dotted": "dotted", "dashed": "dashed", "double": "double"}.get(side.style, "solid")
    return f"{width}px {style} {color(side.color, '#000000')}"


def sheet_html(ws, tabs: list[str]) -> str:
    merged = {}
    covered = set()
    for rng in ws.merged_cells.ranges:
        merged[(rng.min_row, rng.min_col)] = (rng.max_row - rng.min_row + 1, rng.max_col - rng.min_col + 1)
        for r in range(rng.min_row, rng.max_row + 1):
            for c in range(rng.min_col, rng.max_col + 1):
                if (r, c) != (rng.min_row, rng.min_col):
                    covered.add((r, c))

    cols, used = [], 0
    for c in range(1, ws.max_column + 1):
        dim = ws.column_dimensions[get_column_letter(c)]
        if dim.hidden:
            continue
        w = col_px(dim.width)
        if used + w > MAX_WIDTH_PX and cols:
            break
        cols.append((c, w))
        used += w
    last_col = cols[-1][0]
    # Stop one row after the last filled row, or at the first run of four empty rows.
    last_row, empty_run = 1, 0
    for r in range(1, ws.max_row + 1):
        if any(ws.cell(r, c).value not in (None, "") for c, _ in cols):
            last_row, empty_run = r + 1, 0
        else:
            empty_run += 1
            if empty_run >= 4:
                break
    rows = [r for r in range(1, min(ws.max_row, last_row) + 1)
            if not ws.row_dimensions[r].hidden][:ROW_LIMIT.get(ws.title, MAX_ROWS)]
    gridlines = ws.sheet_view.showGridLines is not False

    out = ['<table class="grid"><colgroup><col style="width:42px">']
    out += [f'<col style="width:{w}px">' for _, w in cols]
    out.append('</colgroup><tr class="hdr"><th class="corner"></th>')
    out += [f"<th>{get_column_letter(c)}</th>" for c, _ in cols]
    out.append("</tr>")
    for r in rows:
        h = (ws.row_dimensions[r].height or DEFAULT_ROW_PT) * 96 / 72
        out.append(f'<tr style="height:{h:.0f}px"><th class="rn">{r}</th>')
        for c, _ in cols:
            if (r, c) in covered:
                continue
            cell = ws.cell(r, c)
            span = merged.get((r, c))
            attrs = ""
            if span:
                rs, cs = span
                cs = min(cs, last_col - c + 1)
                attrs = (f' rowspan="{rs}"' if rs > 1 else "") + (f' colspan="{cs}"' if cs > 1 else "")
            st = []
            if cell.fill is not None and cell.fill.fill_type == "solid":
                fill = color(cell.fill.fgColor)
                if fill:
                    st.append(f"background:{fill}")
            f = cell.font
            if f is not None:
                if f.b:
                    st.append("font-weight:700")
                if f.i:
                    st.append("font-style:italic")
                if f.sz:
                    st.append(f"font-size:{float(f.sz) * 96 / 72:.1f}px")
                fc = color(f.color)
                if fc:
                    st.append(f"color:{fc}")
            a = cell.alignment
            horiz = a.horizontal if a is not None and a.horizontal not in (None, "general") else (
                "right" if isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool) else "left")
            st.append(f"text-align:{'center' if horiz in ('center', 'centerContinuous') else horiz}")
            st.append(f"vertical-align:{({'top': 'top', 'center': 'middle'}).get(a.vertical if a else None, 'bottom')}")
            if a is not None and a.wrap_text:
                st.append("white-space:normal")
            if a is not None and a.indent:
                st.append(f"padding-left:{3 + 9 * int(a.indent)}px")
            b = cell.border
            for side, name in ((b.left, "left"), (b.right, "right"), (b.top, "top"), (b.bottom, "bottom")):
                css = border_css(side)
                if css:
                    st.append(f"border-{name}:{css}")
            note = '<span class="note"></span>' if cell.comment is not None else ""
            shown = html.escape(text_of(cell))
            if cell.coordinate in LEFT_OUT.get(ws.title, ()):
                shown = '<i style="color:#8a8a8a;font-weight:400">(gauge name)</i>'
            out.append(f'<td{attrs} style="{";".join(st)}"><div>{shown}</div>{note}</td>')
        out.append("</tr>")
    out.append("</table>")

    tab_bar = "".join(
        f'<span class="tab{" on" if t == ws.title else ""}">{html.escape(t)}</span>' for t in tabs)
    css = f"""
    body {{ margin:0; background:#ffffff; font-family:Calibri, Aptos, Carlito, 'Helvetica Neue', Arial, sans-serif; }}
    #shot {{ display:inline-block; border:1px solid #c8c8c8; background:#ffffff; }}
    table.grid {{ border-collapse:collapse; table-layout:fixed; font-size:14.7px; color:#000; }}
    table.grid td {{ position:relative; padding:0 3px; overflow:hidden; white-space:nowrap;
                     border:1px solid {'#e1e1e1' if gridlines else 'transparent'}; line-height:1.15; }}
    table.grid td > div {{ overflow:hidden; text-overflow:clip; }}
    table.grid th {{ background:#f3f3f3; color:#555; font-weight:400; font-size:12px;
                     border:1px solid #d4d4d4; height:20px; }}
    th.rn {{ text-align:center; }}
    th.corner {{ background:#e8e8e8; }}
    span.note {{ position:absolute; top:0; right:0; width:0; height:0; border-top:6px solid #d0021b;
                 border-left:6px solid transparent; }}
    .tabs {{ display:flex; flex-wrap:wrap; gap:0; background:#f0f0f0; border-top:1px solid #c8c8c8;
             padding:3px 6px; font-size:12.5px; color:#333; max-width:{used + 42}px; }}
    .tab {{ padding:3px 9px; border-right:1px solid #d0d0d0; white-space:nowrap; }}
    .tab.on {{ background:#ffffff; color:#107c41; font-weight:700; border-bottom:2px solid #107c41; }}
    """
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>"
            f"<div id='shot'>{''.join(out)}<div class='tabs'>{tab_bar}</div></div></body></html>")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    workbook = Path(sys.argv[1]).expanduser().resolve()
    preview = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
    from playwright.sync_api import sync_playwright

    wb = openpyxl.load_workbook(workbook)
    tabs = wb.sheetnames
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="hp2d-workbook-"))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=SCALE, viewport={"width": 1700, "height": 1000})
        for ws in wb.worksheets:
            if only and ws.title not in only:
                continue
            page_html = tmp / f"{slug(ws.title)}.html"
            page_html.write_text(sheet_html(ws, tabs), encoding="utf-8")
            page.goto(page_html.as_uri())
            raw = tmp / f"{slug(ws.title)}.raw.png"
            page.locator("#shot").screenshot(path=str(raw))
            png = OUT / f"{slug(ws.title)}.png"
            Image.open(raw).convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(png, optimize=True)
            if preview is not None:
                preview.mkdir(parents=True, exist_ok=True)
                (preview / png.name).write_bytes(png.read_bytes())
            print(png.relative_to(HERE.parent), Image.open(png).size, f"{png.stat().st_size // 1024} KB")
        browser.close()


if __name__ == "__main__":
    main()
