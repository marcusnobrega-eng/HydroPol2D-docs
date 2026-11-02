"""Rain or snow, storage, melt and sublimation, for docs/theory/hydrologic-model.md, Section 5.

Left: the path of one time step in one cell. Precipitation is split by the air
temperature (the plot is the snow fraction f_snow of Section 5.1), snow is stored as SWE,
the pack loses melt and sublimation. The partition comes before the canopy: only the rain
enters the canopy store (when interception is on) and reaches the surface water as
throughfall; the melt goes from the snowpack straight to the surface water.
Right: the equations of Sections 5.1 to 5.5 and 5.7, written as in the docs.
Bottom left: an illustration with synthetic forcing (not model output) that runs the
snow-fraction and degree-day equations day by day.

Run from the repository root:

    python3 figures/snow.py [preview-folder]

Output: static/img/theory/snow.svg (en), snow.pt.svg and snow.es.svg, and a PNG of each
in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Polygon, Rectangle

sys.dont_write_bytecode = True  # never leave __pycache__ in the docs repo
from site_style import INK, SOFT, STATIC, WATER, Sheet, bezier, color, oklch_hex  # noqa: E402
import flow_kit as fk  # noqa: E402
from fig_check import _ARROWS, report, track  # noqa: E402

# --- text per language. Math stays the same in every language. ------------------------------
LABELS = {
    "en": {
        "atmosphere": "Atmosphere",
        "forcing": r"$T_{\mathrm{air}}$, $T_{\mathrm{min}}$, wind speed $u$",
        "plot_title": "Rain or snow",
        "area_snow": "snow",
        "area_rain": "rain",
        "snow": ("snow", r"$P_{\mathrm{snow}}$"),
        "rain": ("rain", r"$P_{\mathrm{rain}}$"),
        "sublimation": ("sublimation", r"$E_{\mathrm{s}}$"),
        "melt": ("melt", r"$M_{\mathrm{snow}}$"),
        "pack": "Snowpack",
        "pack_state": r"density $\rho_{\mathrm{snow}}$",
        "canopy": ("Canopy store", "when it is on"),
        "throughfall": ("throughfall", r"$T_{\mathrm{f}}$"),
        "surface": "surface water",
        "notes": [
            ("5.1  Rain or snow", [
                (r"between the thresholds $f_{\mathrm{snow}} = \dfrac{T_{\mathrm{rain}} - T_{\mathrm{air}}}"
                 r"{T_{\mathrm{rain}} - T_{\mathrm{snow}}}$", 28),
                (r"$P_{\mathrm{snow}} = P_{\mathrm{gross}}\,f_{\mathrm{snow}}$,   "
                 r"$P_{\mathrm{rain}} = P_{\mathrm{gross}} - P_{\mathrm{snow}}$", 27),
                (r"$T_{\mathrm{snow}} \leq T_{\mathrm{rain}}$ in $^{\circ}\mathrm{C}$, both set per land-cover class", 17),
            ]),
            ("5.2  Snow water equivalent", [
                (r"$\mathrm{SWE}_t = \mathrm{SWE}_{t-1} + P_{\mathrm{snow}} - M_{\mathrm{snow}}"
                 r" - E_{\mathrm{s}}$", 17),
                ("every term in mm of water equivalent", 17),
            ]),
            ("5.3  Melt", [
                (r"$M_{\mathrm{snow}} = \min\![\,\mathrm{SWE}_{\mathrm{after\ snowfall}},$", 19),
                (r"$\quad\max\!(\mathrm{DDF}\,\max(T_{\mathrm{air}},0)\,\Delta t_d + "
                 r"\dfrac{\max(Q_{\mathrm{net}},0)\,\Delta t_s}{L_f},\ 0)\,]$", 26),
                (r"$\Delta t_d = \Delta t_s/86400$,   $L_f = 3.34\times10^5\ \mathrm{J\,kg^{-1}}$", 27),
                (r"DDF set per class, $Q_{\mathrm{net}}$ the net radiation", 18),
            ]),
            ("5.4  Density and depth", [
                (r"$\rho_{\mathrm{snow}}^{\,\mathrm{new}} = \rho_{\mathrm{snow}}^{\,\mathrm{mixed}} + "
                 r"\Delta t_d\,[k_t\,\max(T_{\mathrm{air}},0) + k_{\mathrm{swe}}\mathrm{SWE} + k_D H_{\mathrm{snow}}]$",
                 20),
                (r"$\rho_{\mathrm{init}} \leq \rho_{\mathrm{snow}} \leq \rho_{\mathrm{max}}$,   "
                 r"$H_{\mathrm{snow}} = 1000\,\mathrm{SWE}/\rho_{\mathrm{snow}}$", 19),
                (r"new snow comes in at $\rho_{\mathrm{init}}$, mixed with the pack by SWE", 17),
            ]),
            ("5.5  Sublimation", [
                (r"$E_{\mathrm{s}} = \min\![\,\mathrm{SWE}_{\mathrm{after\ melt}},$", 19),
                (r"$\quad\max\!(C_e\,u\,(q_s - q_a)\,\mathrm{SWE}_{\mathrm{after\ melt}}\,\Delta t_d,\ 0)\,]$", 19),
                (r"$C_e$ set per class, $u$ the wind speed,", 18),
                (r"$q_s$, $q_a$ saturation and ambient specific humidity", 17),
            ]),
            ("5.7  To the surface water", [
                (r"$d_t = d_p + M_{\mathrm{snow}} + P_{\mathrm{eff}}$", 19),
                (r"$P_{\mathrm{eff}}$ is the rain on the ground (the throughfall", 17),
                (r"$T_{\mathrm{f}}$ with interception on); the melt skips the canopy", 17),
            ]),
        ],
        "ts_title": "Illustration",
        "ts_sub": "synthetic forcing, not model output",
        "ts_snow": "snow",
        "ts_rain": "rain",
        "ts_time": "time",
        "ts_peak": "peak SWE",
    },
    "pt": {
        "atmosphere": "Atmosfera",
        "forcing": r"$T_{\mathrm{air}}$, $T_{\mathrm{min}}$, velocidade do vento $u$",
        "plot_title": "Chuva ou neve",
        "area_snow": "neve",
        "area_rain": "chuva",
        "snow": ("neve", r"$P_{\mathrm{snow}}$"),
        "rain": ("chuva", r"$P_{\mathrm{rain}}$"),
        "sublimation": ("sublimação", r"$E_{\mathrm{s}}$"),
        "melt": ("degelo", r"$M_{\mathrm{snow}}$"),
        "pack": "Manto de neve",
        "pack_state": r"densidade $\rho_{\mathrm{snow}}$",
        "canopy": ("Interceptação", "quando ativa"),
        "throughfall": ("throughfall", r"$T_{\mathrm{f}}$"),
        "surface": "água superficial",
        "notes": [
            ("5.1  Chuva ou neve", [
                (r"entre os limiares $f_{\mathrm{snow}} = \dfrac{T_{\mathrm{rain}} - T_{\mathrm{air}}}"
                 r"{T_{\mathrm{rain}} - T_{\mathrm{snow}}}$", 28),
                (r"$P_{\mathrm{snow}} = P_{\mathrm{gross}}\,f_{\mathrm{snow}}$,   "
                 r"$P_{\mathrm{rain}} = P_{\mathrm{gross}} - P_{\mathrm{snow}}$", 27),
                (r"$T_{\mathrm{snow}} \leq T_{\mathrm{rain}}$ em $^{\circ}\mathrm{C}$, ambos por classe de uso do solo", 17),
            ]),
            ("5.2  Equivalente de água da neve", [
                (r"$\mathrm{SWE}_t = \mathrm{SWE}_{t-1} + P_{\mathrm{snow}} - M_{\mathrm{snow}}"
                 r" - E_{\mathrm{s}}$", 17),
                ("todos os termos em mm de equivalente de água", 17),
            ]),
            ("5.3  Derretimento", [
                (r"$M_{\mathrm{snow}} = \min\![\,\mathrm{SWE}_{\mathrm{after\ snowfall}},$", 19),
                (r"$\quad\max\!(\mathrm{DDF}\,\max(T_{\mathrm{air}},0)\,\Delta t_d + "
                 r"\dfrac{\max(Q_{\mathrm{net}},0)\,\Delta t_s}{L_f},\ 0)\,]$", 26),
                (r"$\Delta t_d = \Delta t_s/86400$,   $L_f = 3.34\times10^5\ \mathrm{J\,kg^{-1}}$", 27),
                (r"DDF definido por classe, $Q_{\mathrm{net}}$ a radiação líquida", 18),
            ]),
            ("5.4  Densidade e profundidade", [
                (r"$\rho_{\mathrm{snow}}^{\,\mathrm{new}} = \rho_{\mathrm{snow}}^{\,\mathrm{mixed}} + "
                 r"\Delta t_d\,[k_t\,\max(T_{\mathrm{air}},0) + k_{\mathrm{swe}}\mathrm{SWE} + k_D H_{\mathrm{snow}}]$",
                 20),
                (r"$\rho_{\mathrm{init}} \leq \rho_{\mathrm{snow}} \leq \rho_{\mathrm{max}}$,   "
                 r"$H_{\mathrm{snow}} = 1000\,\mathrm{SWE}/\rho_{\mathrm{snow}}$", 19),
                (r"neve nova: $\rho_{\mathrm{init}}$, misturada ao manto pelo SWE", 17),
            ]),
            ("5.5  Sublimação", [
                (r"$E_{\mathrm{s}} = \min\![\,\mathrm{SWE}_{\mathrm{after\ melt}},$", 19),
                (r"$\quad\max\!(C_e\,u\,(q_s - q_a)\,\mathrm{SWE}_{\mathrm{after\ melt}}\,\Delta t_d,\ 0)\,]$", 19),
                (r"$C_e$ definido por classe, $u$ a velocidade do vento,", 18),
                (r"$q_s$, $q_a$ umidade específica de saturação e do ar", 17),
            ]),
            ("5.7  Para a água superficial", [
                (r"$d_t = d_p + M_{\mathrm{snow}} + P_{\mathrm{eff}}$", 19),
                (r"$P_{\mathrm{eff}}$ é a chuva no solo (o throughfall $T_{\mathrm{f}}$", 17),
                (r"com interceptação); o degelo não passa pelo dossel", 17),
            ]),
        ],
        "ts_title": "Ilustração",
        "ts_sub": "forçantes sintéticas, não saída do modelo",
        "ts_snow": "neve",
        "ts_rain": "chuva",
        "ts_time": "tempo",
        "ts_peak": "pico de SWE",
    },
    "es": {
        "atmosphere": "Atmósfera",
        "forcing": r"$T_{\mathrm{air}}$, $T_{\mathrm{min}}$, velocidad del viento $u$",
        "plot_title": "Lluvia o nieve",
        "area_snow": "nieve",
        "area_rain": "lluvia",
        "snow": ("nieve", r"$P_{\mathrm{snow}}$"),
        "rain": ("lluvia", r"$P_{\mathrm{rain}}$"),
        "sublimation": ("sublimación", r"$E_{\mathrm{s}}$"),
        "melt": ("fusión", r"$M_{\mathrm{snow}}$"),
        "pack": "Manto de nieve",
        "pack_state": r"densidad $\rho_{\mathrm{snow}}$",
        "canopy": ("Intercepción", "si está activa"),
        "throughfall": ("throughfall", r"$T_{\mathrm{f}}$"),
        "surface": "agua superficial",
        "notes": [
            ("5.1  Lluvia o nieve", [
                (r"entre los umbrales $f_{\mathrm{snow}} = \dfrac{T_{\mathrm{rain}} - T_{\mathrm{air}}}"
                 r"{T_{\mathrm{rain}} - T_{\mathrm{snow}}}$", 28),
                (r"$P_{\mathrm{snow}} = P_{\mathrm{gross}}\,f_{\mathrm{snow}}$,   "
                 r"$P_{\mathrm{rain}} = P_{\mathrm{gross}} - P_{\mathrm{snow}}$", 27),
                (r"$T_{\mathrm{snow}} \leq T_{\mathrm{rain}}$ en $^{\circ}\mathrm{C}$, ambos por clase de cobertura", 17),
            ]),
            ("5.2  Equivalente de agua de nieve", [
                (r"$\mathrm{SWE}_t = \mathrm{SWE}_{t-1} + P_{\mathrm{snow}} - M_{\mathrm{snow}}"
                 r" - E_{\mathrm{s}}$", 17),
                ("todos los términos en mm de equivalente de agua", 17),
            ]),
            ("5.3  Fusión", [
                (r"$M_{\mathrm{snow}} = \min\![\,\mathrm{SWE}_{\mathrm{after\ snowfall}},$", 19),
                (r"$\quad\max\!(\mathrm{DDF}\,\max(T_{\mathrm{air}},0)\,\Delta t_d + "
                 r"\dfrac{\max(Q_{\mathrm{net}},0)\,\Delta t_s}{L_f},\ 0)\,]$", 26),
                (r"$\Delta t_d = \Delta t_s/86400$,   $L_f = 3.34\times10^5\ \mathrm{J\,kg^{-1}}$", 27),
                (r"DDF definido por clase, $Q_{\mathrm{net}}$ la radiación neta", 18),
            ]),
            ("5.4  Densidad y profundidad", [
                (r"$\rho_{\mathrm{snow}}^{\,\mathrm{new}} = \rho_{\mathrm{snow}}^{\,\mathrm{mixed}} + "
                 r"\Delta t_d\,[k_t\,\max(T_{\mathrm{air}},0) + k_{\mathrm{swe}}\mathrm{SWE} + k_D H_{\mathrm{snow}}]$",
                 20),
                (r"$\rho_{\mathrm{init}} \leq \rho_{\mathrm{snow}} \leq \rho_{\mathrm{max}}$,   "
                 r"$H_{\mathrm{snow}} = 1000\,\mathrm{SWE}/\rho_{\mathrm{snow}}$", 19),
                (r"nieve nueva: $\rho_{\mathrm{init}}$, mezclada con el manto según el SWE", 17),
            ]),
            ("5.5  Sublimación", [
                (r"$E_{\mathrm{s}} = \min\![\,\mathrm{SWE}_{\mathrm{after\ melt}},$", 19),
                (r"$\quad\max\!(C_e\,u\,(q_s - q_a)\,\mathrm{SWE}_{\mathrm{after\ melt}}\,\Delta t_d,\ 0)\,]$", 19),
                (r"$C_e$ definido por clase, $u$ la velocidad del viento,", 18),
                (r"$q_s$, $q_a$ humedad específica de saturación y del aire", 17),
            ]),
            ("5.7  Al agua superficial", [
                (r"$d_t = d_p + M_{\mathrm{snow}} + P_{\mathrm{eff}}$", 19),
                (r"$P_{\mathrm{eff}}$ es la lluvia en el suelo (el throughfall $T_{\mathrm{f}}$", 17),
                (r"con intercepción); la fusión no pasa por el dosel", 17),
            ]),
        ],
        "ts_title": "Ilustración",
        "ts_sub": "forzamiento sintético, no salida del modelo",
        "ts_snow": "nieve",
        "ts_rain": "lluvia",
        "ts_time": "tiempo",
        "ts_peak": "pico de SWE",
    },
}
MATH = {
    "p_gross": r"$P_{\mathrm{gross}}$",
    "f_snow": r"$f_{\mathrm{snow}}$",
    "t_air": r"$T_{\mathrm{air}}$",
    "t_snow": r"$T_{\mathrm{snow}}$",
    "t_rain": r"$T_{\mathrm{rain}}$",
    "h_snow": r"$H_{\mathrm{snow}}$",
    "d": r"$d$",
    "ts_rows": [r"$T_{\mathrm{air}}$", r"$P_{\mathrm{gross}}$", "SWE"],
}

# --- colours --------------------------------------------------------------------------------
SKY = color("deep_fill")
SOIL = color("slot_near_surface")
RAIN_FILL = color("slot_wet_even")
# New colours (OKLCH), the same two as in cell_water_budget.py:
SURFACE_WATER = oklch_hex(0.72, 0.090, 245)  # ponded water d
SNOW = oklch_hex(0.975, 0.012, 240)          # snowpack, near white with a trace of the water hue

W, H = 760, 608
LX0, LX1 = 24, 390          # left column
NOTE_X = 408                # notes
NOTE_ROOM = W - 6 - NOTE_X

# --- illustration forcing: synthetic, run through the snow-fraction and degree-day equations --
DAYS = np.arange(0, 121)
T_AIR = -7.0 + 14.0 * DAYS / 120 + 2.6 * np.sin(2 * np.pi * DAYS / 11.0)
P_GROSS = np.zeros_like(DAYS, dtype=float)
for _day, _mm in ((5, 8), (14, 12), (23, 6), (32, 10), (43, 9), (54, 12), (62, 7), (73, 10), (85, 8),
                  (96, 11), (107, 6)):
    P_GROSS[_day] = _mm
T_SNOW, T_RAIN, DDF = -1.0, 1.0, 2.0        # code defaults, mm C-1 day-1
F_SNOW = np.clip((T_RAIN - T_AIR) / (T_RAIN - T_SNOW), 0.0, 1.0)
P_SNOW = P_GROSS * F_SNOW
P_RAIN = P_GROSS - P_SNOW
SWE = np.zeros_like(T_AIR)
_store = 0.0
for _k in range(len(DAYS)):
    _store += P_SNOW[_k]
    _store -= min(DDF * max(T_AIR[_k], 0.0) * 1.0, _store)   # one-day step, no radiation, no sublimation
    SWE[_k] = _store


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


def draw(lang: str, preview: Path | None = None) -> None:
    T = LABELS[lang]
    _ARROWS.clear()  # fig_check keeps the arrows of every sheet; check this one only
    s = Sheet(W, H, "snow")
    ax = s.ax

    def flow(points, c=WATER, **kw):
        kw.setdefault("width", (1.2, 3.8))
        kw.setdefault("head", (12, 11))
        with track(ax):
            s.arrow(points, c=c, **kw)

    def two_line(x, y, pair, ha="left"):
        s.text(x, y, pair[0], ha=ha)
        s.text(x, y + 16, pair[1], ha=ha, size=10)

    # --- atmosphere ---------------------------------------------------------------------------
    s.box(LX0, 16, LX1 - LX0, 32, fill=SKY, edge=color("guide"), radius=8, lw=0.8, z=1)
    s.text(LX0 + 12, 32, T["atmosphere"], bold=True, size=10.5)
    fk.text(s, LX0 + 112, 32, T["forcing"], room=LX1 - 10 - (LX0 + 112))

    # --- 5.1: the split, drawn as f_snow(T_air) -----------------------------------------------
    PX0, PY0, PX1, PY1 = 160, 82, LX1, 200          # frame
    AX0, AX1, F1, F0 = 206, 378, 116, 166           # axes: x range, y of f = 1 and f = 0
    TS_X, TR_X = 262, 314                           # T_snow and T_rain on the axis
    flow([(272, 49), (272, PY0 - 1)])
    s.text(280, 64, MATH["p_gross"], size=10)
    s.box(PX0, PY0, PX1 - PX0, PY1 - PY0, fill=color("card"), edge=color("card_edge"), radius=7, lw=1.0, z=1)
    s.text(PX0 + 10, PY0 + 15, T["plot_title"], bold=True, size=10)
    curve_x = [AX0, TS_X, TR_X, AX1]
    curve_y = [F1, F1, F0, F0]
    ax.add_patch(Polygon([(AX0, F0)] + list(zip(curve_x, curve_y)) + [(AX1, F0)], closed=True,
                         facecolor=SNOW, edgecolor="none", zorder=2))
    ax.add_patch(  # rain fraction 1 - f_snow: the area above the curve
        Polygon([(TS_X, F1), (AX1, F1), (AX1, F0), (TR_X, F0)], closed=True,
                facecolor=RAIN_FILL, edgecolor="none", zorder=2))
    s.line(curve_x, curve_y, c=INK, lw=1.6, z=4)
    s.line([AX0, AX0, AX1], [F1 - 6, F0, F0], c=SOFT, lw=0.9, z=3)       # L-shaped axes
    for x in (TS_X, TR_X):
        s.line([x, x], [F0, F0 + 4], c=SOFT, lw=0.9, z=3)
        s.line([x, x], [F1, F0], c=SOFT, lw=0.7, style=(0, (1, 2.5)), z=3)
    s.text(TS_X, F0 + 15, MATH["t_snow"], ha="center", size=10)
    s.text(TR_X, F0 + 15, MATH["t_rain"], ha="center", size=10)
    s.text(AX1, F0 + 15, MATH["t_air"], ha="right", size=10)
    s.text(AX0 - 5, F1, "1", ha="right", c=SOFT)
    s.text(AX0 - 5, F0, "0", ha="right", c=SOFT)
    s.text(AX0 - 20, (F1 + F0) / 2, MATH["f_snow"], ha="center", size=10, rotation=90)
    s.text(AX0 + 12, F0 - 14, T["area_snow"])
    s.text(AX1 - 8, F1 + 14, T["area_rain"], ha="right")

    # --- the snowpack (5.2 and 5.4) -------------------------------------------------------------
    GY, FY = 355, 339                 # ground, top of the surface water
    SP_X0, SP_X1, SP_TOP = 36, 214, 266
    pack = bezier([(SP_X0, FY), (SP_X0 + 2, SP_TOP + 4), (SP_X0 + 30, SP_TOP), (SP_X1 - 20, SP_TOP)], 30)
    pack = np.vstack([pack, bezier([(SP_X1 - 20, SP_TOP), (SP_X1, SP_TOP + 1), (SP_X1, SP_TOP + 20),
                                    (SP_X1, FY)], 20)])
    ax.add_patch(Polygon(np.vstack([pack, [(SP_X0, FY)]]), closed=True, facecolor=SNOW,
                         edgecolor=color("guide"), lw=0.9, zorder=3))
    # Water equivalent: the same water as a liquid layer, H_snow / SWE = rho_snow / 1000 (here 250).
    BAR_X0, BAR_X1 = 172, 194
    bar_top = FY - (FY - SP_TOP) * 250 / 1000
    ax.add_patch(Rectangle((BAR_X0, bar_top), BAR_X1 - BAR_X0, FY - bar_top, facecolor=SURFACE_WATER,
                           edgecolor="none", zorder=4))
    s.line([BAR_X0 - 7, BAR_X0 - 10, BAR_X0 - 10, BAR_X0 - 7], [bar_top, bar_top, FY - 1, FY - 1], c=SOFT, lw=0.9, z=5)
    s.text(BAR_X0 - 14, (bar_top + FY) / 2, "SWE", ha="right", size=9.5)
    s.text(112, 292, T["pack"], bold=True, size=10, ha="center")
    s.text(112, 311, T["pack_state"], ha="center")
    # Depth bracket on the left of the pack.
    s.line([SP_X0 - 3, SP_X0 - 7, SP_X0 - 7, SP_X0 - 3], [SP_TOP, SP_TOP, FY - 1, FY - 1], c=SOFT, lw=0.9)
    s.text(SP_X0 - 3, SP_TOP - 12, MATH["h_snow"], size=10, c=INK)

    # --- surface water and ground ----------------------------------------------------------------
    ax.add_patch(Rectangle((LX0, FY), LX1 - LX0, GY - FY, facecolor=SURFACE_WATER, lw=0, zorder=2))
    ax.add_patch(Rectangle((LX0, GY), LX1 - LX0, 12, facecolor=SOIL, lw=0, zorder=2))
    s.line([LX0, LX1], [GY, GY], c=color("ground"), lw=2.2, z=3)
    s.text(52, (FY + GY) / 2 + 0.5, T["surface"] + " " + MATH["d"], size=9.5, z=6)

    # --- canopy store, when interception is on: rain only ----------------------------------------
    CB = (276, 246, LX1, 292)
    s.box(CB[0], CB[1], CB[2] - CB[0], CB[3] - CB[1], fill=color("canopy_light"), edge=color("canopy_shade"),
          radius=6, lw=1.0, z=2)
    fk.text(s, (CB[0] + CB[2]) / 2, CB[1] + 15, T["canopy"][0], bold=True, size=10, ha="center")
    fk.text(s, (CB[0] + CB[2]) / 2, CB[1] + 32, T["canopy"][1], ha="center")
    for word, bold in ((T["canopy"][0], True), (T["canopy"][1], False)):
        if fk.width(s, word, bold=bold, size=10 if bold else 9.5) > CB[2] - CB[0] - 12:
            print(f"canopy box: {word!r} is wider than the box")

    # --- fluxes -----------------------------------------------------------------------------------
    TF_X = 312                                                                  # throughfall
    flow([(214, PY1 + 1), (204, 232), (186, SP_TOP - 2)])                    # snow
    two_line(218, 222, T["snow"])
    flow([(350, PY1 + 1), (350, CB[1] - 1)])                                   # rain into the canopy
    two_line(342, 214, T["rain"], ha="right")
    flow([(SP_X1 + 2, 296), (240, 298), (246, FY - 1)])                        # melt straight to d
    two_line(253, 306, T["melt"])
    flow([(TF_X, CB[3] + 1), (TF_X, FY - 1)])                                  # throughfall
    two_line(TF_X + 8, 306, T["throughfall"])
    flow([(70, SP_TOP + 2), (70, 49)], c=SOFT, width=(1.0, 3.2), head=(11, 10))  # sublimation
    two_line(78, 150, T["sublimation"])

    # --- notes ------------------------------------------------------------------------------------
    y = 36
    for heading, lines in T["notes"]:
        fk.text(s, NOTE_X, y, heading, bold=True, size=10, room=NOTE_ROOM)
        y += 4
        for text, step in lines:
            y += step
            fk.text(s, NOTE_X, y, text, room=NOTE_ROOM)
        y += 30

    # --- illustration: synthetic forcing through the snow-fraction and degree-day equations ------
    TX0, TX1 = 96, LX1 - 34
    rows = [(412, 454), (470, 508), (524, 564)]            # (top, bottom) of each row
    fk.text(s, LX0 + 2, 384, T["ts_title"], bold=True, size=10)
    sub_x = LX0 + 2 + fk.width(s, T["ts_title"], bold=True, size=10) + 6
    fk.text(s, sub_x, 384, T["ts_sub"], room=LX1 - sub_x)

    def tx(d):
        return TX0 + (TX1 - TX0) * d / DAYS[-1]

    def row_axes(top, bot, label, y=None):
        s.line([TX0, TX0, TX1], [top - 2, bot, bot], c=SOFT, lw=0.9, z=3)
        s.text(TX0 - 10, (top + bot) / 2 if y is None else y, label, ha="right", size=10)

    # Row 1: air temperature and the two thresholds.
    top, bot = rows[0]
    lo, hi = -10.0, 9.0
    ty = lambda v: bot - (bot - top) * (v - lo) / (hi - lo)  # noqa: E731
    row_axes(top, bot, MATH["ts_rows"][0])
    ax.add_patch(Rectangle((TX0, ty(T_RAIN)), TX1 - TX0, ty(T_SNOW) - ty(T_RAIN), facecolor=RAIN_FILL,
                           alpha=0.55, lw=0, zorder=2))
    s.line([tx(d) for d in DAYS], [ty(v) for v in T_AIR], c=INK, lw=1.3, z=4)
    s.text(TX1 + 4, ty(T_RAIN) - 8, MATH["t_rain"], size=9.5)
    s.text(TX1 + 4, ty(T_SNOW) + 9, MATH["t_snow"], size=9.5)

    # Row 2: precipitation, split into snow (light) and rain (blue).
    top, bot = rows[1]
    py = lambda v: (bot - top) * v / 13.0  # noqa: E731
    row_axes(top, bot, MATH["ts_rows"][1], y=top + 6)
    for k in np.nonzero(P_GROSS)[0]:
        x = tx(DAYS[k])
        if P_SNOW[k] > 0:
            ax.add_patch(Rectangle((x - 3, bot - py(P_SNOW[k])), 6, py(P_SNOW[k]), facecolor=SNOW,
                                   edgecolor=color("guide"), lw=0.8, zorder=4))
        if P_RAIN[k] > 0:
            ax.add_patch(Rectangle((x - 3, bot - py(P_GROSS[k])), 6, py(P_RAIN[k]), facecolor=WATER,
                                   edgecolor="none", zorder=4))
    for k, (name, fill, edge) in enumerate(((T["ts_snow"], SNOW, color("guide")), (T["ts_rain"], WATER, "none"))):
        ly = top + 23 + 16 * k
        ax.add_patch(Rectangle((30, ly - 4), 8, 8, facecolor=fill, edgecolor=edge, lw=0.8, zorder=4))
        fk.text(s, 42, ly, name, room=TX0 - 4 - 42)

    # Row 3: SWE.
    top, bot = rows[2]
    sy = lambda v: bot - (bot - top) * v / max(SWE.max(), 1.0)  # noqa: E731
    row_axes(top, bot, MATH["ts_rows"][2])
    ax.add_patch(Polygon([(TX0, bot)] + [(tx(d), sy(v)) for d, v in zip(DAYS, SWE)] + [(TX1, bot)],
                         closed=True, facecolor=SNOW, edgecolor="none", zorder=2))
    s.line([tx(d) for d in DAYS], [sy(v) for v in SWE], c=color("guide"), lw=1.2, z=3)

    # Shared time axis and the day of peak SWE through all rows.
    k_peak = int(np.argmax(SWE))
    s.line([tx(k_peak)] * 2, [rows[0][0] - 2, rows[2][1]], c=SOFT, lw=0.9, style=(0, (1, 2.5)), z=5)
    s.text(tx(k_peak), rows[0][0] - 10, T["ts_peak"], ha="center", c=INK)
    with track(ax):
        s.arrow([(TX0, rows[2][1] + 16), (TX1, rows[2][1] + 16)], c=SOFT, width=(0.8, 1.6), head=(9, 8))
    fk.text(s, TX1 + 4, rows[2][1] + 16, T["ts_time"], c=INK, room=W - 6 - (TX1 + 4))

    print(lang, end=": ")
    report(s)
    print(s.save(STATIC / "theory", lang, preview))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
