"""Figures for Lecture 2: where the elements were made, the notation, galevo, observations.
Run: python make_element_figs.py  ->  slides_elements/*.png
Data for the periodic table: stellarpops/origins.py (approximate fractions, see the references there).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch
from stellarpops.origins import ELEMENTS, SOURCES, position
from stellarpops.toy_gce import _imf_numbers, YIELD_IA
from stellarpops.style import BG, FG, BLUE, ORANGE, PINK, GREEN, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_elements"); os.makedirs(OUT, exist_ok=True)
FONT = os.environ.get("XKCD_FONT", "/home/claude/ext/fonts/xkcd-font/xkcd-script/font/xkcd-script.ttf")
HAVE_XKCD = os.path.exists(FONT)
if HAVE_XKCD:
    font_manager.fontManager.addfont(FONT)
ORDER = ["bb", "cr", "agb", "ccsn", "ia", "r", "none"]


def clean_style():
    plt.rcdefaults()
    mpl.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
                         "text.color": FG, "axes.edgecolor": FG, "axes.labelcolor": FG,
                         "xtick.color": FG, "ytick.color": FG, "font.size": 18,
                         "font.family": "DejaVu Sans"})


def sketch_style():
    plt.rcdefaults()
    plt.xkcd(scale=1.0, length=120, randomness=2)
    mpl.rcParams.update({"font.family": "xkcd Script" if HAVE_XKCD else "sans-serif",
                         "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
                         "text.color": FG, "axes.edgecolor": FG, "axes.labelcolor": FG,
                         "xtick.color": FG, "ytick.color": FG, "path.effects": [], "font.size": 24})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=110)
    plt.close(fig)
    print("saved", name)


def cell(ax, x, y, e, w=0.94, h=0.94, big=True, fs=17):
    """One element: horizontal colour strips proportional to the fractions."""
    y0 = y
    for k in ORDER:
        f = e["frac"].get(k, 0)
        if f > 0:
            ax.add_patch(Rectangle((x, y0), w, h * f, color=SOURCES[k][1], lw=0))
            y0 += h * f
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=BG, lw=2))
    dark = e["frac"].get("cr", 0) > 0.5 or e["frac"].get("bb", 0) > 0.5 or e["frac"].get("ia", 0) > 0.5
    col = BG if dark else "white"
    ax.text(x + w / 2, y + h * 0.48, e["symbol"], ha="center", va="center", fontsize=fs,
            fontweight="bold", color=col)
    if big:
        ax.text(x + 0.07, y + h - 0.07, str(e["Z"]), ha="left", va="top", fontsize=8, color=col)


# 1 ------------------------------------------------------------ the periodic table of origins
def periodic_table():
    clean_style()
    fig = plt.figure(figsize=(18, 9.0))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98]); ax.set_xlim(-0.1, 18.1); ax.set_ylim(9.75, -0.1); ax.axis("off")
    for e in ELEMENTS:
        r, c = position(e["Z"])
        yy = r - (0.4 if r >= 8 else 0)
        cell(ax, c, yy, e)
    # La/Ac placeholders in the main table
    for r, lab in ((5, "57–71"), (6, "89–")):
        ax.text(2.47, r + 0.47, lab, ha="center", va="center", fontsize=11, color=GREY)
    # legend inside the gap above the transition metals
    for i, k in enumerate(ORDER):
        xx, yy = 2.6 + (i % 2) * 4.9, 0.15 + (i // 2) * 0.62
        ax.add_patch(Rectangle((xx, yy), 0.5, 0.45, color=SOURCES[k][1]))
        ax.text(xx + 0.7, yy + 0.24, SOURCES[k][0], va="center", fontsize=17)
    ax.text(7.5, 2.1, "strips = approximate share of each\nsource in the Solar System (rounded)", fontsize=14, color=GREY, va="center")
    ax.text(18.0, 9.65, "after Johnson (2019, Science 363, 474); Kobayashi, Karakas & Lugaro (2020, ApJ 900, 179)",
            ha="right", fontsize=12, color=GREY)
    save(fig, "periodic_origins")


# 2 ------------------------------------------------------------ the elements in your body
BODY = [("O", "oxygen", 65.0), ("C", "carbon", 18.5), ("H", "hydrogen", 9.5), ("N", "nitrogen", 3.2),
        ("Ca", "calcium", 1.5), ("P", "phosphorus", 1.0), ("K", "potassium", 0.4), ("S", "sulphur", 0.3),
        ("Na", "sodium", 0.2), ("Cl", "chlorine", 0.2), ("Mg", "magnesium", 0.1), ("Fe", "iron", 0.006),
        ("I", "iodine", 0.00002), ("Au", "gold (a ring)", None)]


def body():
    clean_style()
    by = {e["symbol"]: e for e in ELEMENTS}
    fig = plt.figure(figsize=(18, 8.4))
    ax = fig.add_axes([0.17, 0.13, 0.70, 0.84])
    n = len(BODY)
    for i, (s, name, pct) in enumerate(BODY):
        y = n - 1 - i; x0 = 0
        for k in ORDER:
            f = by[s]["frac"].get(k, 0)
            if f > 0:
                ax.barh(y, f, left=x0, color=SOURCES[k][1], height=0.78, lw=0)
                if f >= 0.12:
                    ax.text(x0 + f / 2, y, f"{f:.0%}", ha="center", va="center", fontsize=13,
                            color=BG if k in ("bb", "cr", "ia") else "white")
                x0 += f
        lab = f"{s}  {name}"
        ax.text(-0.02, y, lab, ha="right", va="center", fontsize=17, fontweight="bold" if i < 4 else "normal")
        if pct is not None:
            ax.text(1.02, y, f"{pct:g}%" if pct >= 0.1 else (f"{pct:.3f}%" if pct >= 0.001 else "trace"),
                    va="center", fontsize=15, color=GREY)
    ax.text(1.02, n - 0.45, "% of your body mass", fontsize=14, color=GREY, va="bottom")
    ax.set_xlim(0, 1); ax.set_ylim(-0.6, n + 0.1); ax.axis("off")
    lx = fig.add_axes([0.03, 0.0, 0.94, 0.08]); lx.axis("off"); lx.set_xlim(0, 6); lx.set_ylim(0, 1)
    for i, k in enumerate(["bb", "agb", "ccsn", "ia", "r"]):
        lx.add_patch(Rectangle((0.15 + i * 1.18, 0.3), 0.12, 0.45, color=SOURCES[k][1]))
        lx.text(0.32 + i * 1.18, 0.52, SOURCES[k][0], va="center", fontsize=15)
    save(fig, "body_elements")


# 3 ------------------------------------------------------------ the dex ruler
def dex_ruler():
    clean_style()
    fig, ax = plt.subplots(figsize=(18, 6.2))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.72, bottom=0.30)
    ax.set_xlim(-6.2, 0.8); ax.set_ylim(0, 1); ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.set_xticks(np.arange(-6, 1, 1)); ax.tick_params(axis="x", labelsize=20, length=10, width=2)
    ax.set_xlabel("[Fe/H]", fontsize=24)
    top = ax.secondary_xaxis("top")
    top.set_xticks(np.arange(-6, 1, 1))
    top.set_xticklabels(["1/1 000 000", "1/100 000", "1/10 000", "1/1000", "1/100", "1/10", "Sun"], fontsize=16)
    top.tick_params(length=10, width=2)
    top.set_xlabel("iron per hydrogen, relative to the Sun", fontsize=18, labelpad=12)
    objs = [(-5.5, "most iron-poor\nstars known", PINK, 0.78), (-2.8, "ultra-faint\ndwarf galaxies", GREEN, 0.30),
            (-2.2, "metal-poor\nglobular clusters", ORANGE, 0.78), (-1.5, "Milky Way\nhalo (typical)", BLUE, 0.30),
            (-0.6, "thick disc", GREEN, 0.78), (0.0, "Sun", "#ffd34d", 0.30), (0.35, "bulge /\nmassive\nellipticals", ORANGE, 0.7)]
    for x, lab, col, y in objs:
        ax.plot([x, x], [0, y - (0.1 if "\n" in lab else 0.06)], color=col, lw=2)
        ax.plot(x, 0.02, "o", ms=14, color=col, clip_on=False)
        ax.text(x, y, lab, ha="center", va="center", fontsize=15, color=col)
    ax.text(-6.1, -0.62, "each step of 1 dex = factor 10;   +0.3 dex = factor 2;   −0.3 dex = half", transform=ax.get_xaxis_transform(), fontsize=17, color=GREY)
    save(fig, "dex_ruler")


# 4 ------------------------------------------------------------ SN budget per 1000 Msun formed
def sn_budget():
    clean_style()
    n2, n1, y = _imf_numbers()
    mg = [1000 * n2 * y["Mg"], 1000 * n1 * YIELD_IA["Mg"]]
    fe = [1000 * n2 * y["Fe"], 1000 * n1 * YIELD_IA["Fe"]]
    fig, axs = plt.subplots(1, 3, figsize=(18, 7.2), gridspec_kw=dict(wspace=0.35))
    fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.12)
    for ax, vals, title, fmt in ((axs[0], [1000 * n2, 1000 * n1], "number of supernovae", "{:.1f}"),
                                 (axs[1], mg, "magnesium made [M☉]", "{:.2f}"),
                                 (axs[2], fe, "iron made [M☉]", "{:.2f}")):
        b = ax.bar(["SN II", "SN Ia"], vals, color=[BLUE, ORANGE], width=0.6)
        for bb, v in zip(b, vals):
            ax.text(bb.get_x() + bb.get_width() / 2, v * 1.02 + 0.01 * max(vals), fmt.format(v),
                    ha="center", va="bottom", fontsize=22)
        ax.set_title(title, fontsize=22, pad=14); ax.set_ylim(0, max(vals) * 1.25)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.tick_params(labelsize=18)
    fig.suptitle("per 1000 M☉ of stars formed (Kroupa IMF, toy model of notebook 03)", fontsize=18, color=GREY, y=0.99)
    print(f"SN budget: {1000*n2:.1f} SN II, {1000*n1:.1f} SN Ia; Mg {mg}; Fe {fe}; Ia share of Fe {fe[1]/sum(fe):.0%}")
    save(fig, "sn_budget")


# 5 ------------------------------------------------------------ galevo flow (sketch)
def box(ax, x, y, w, h, txt, col, fs=22):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", fill=False, ec=col, lw=3))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, color=col)


def arr(ax, a, b, col=FG, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=30, lw=3, color=col,
                                 connectionstyle=f"arc3,rad={rad}"))


def galevo_flow():
    sketch_style()
    fig = plt.figure(figsize=(18, 9)); ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18); ax.set_ylim(0, 9); ax.axis("off")
    box(ax, 0.6, 6.4, 3.6, 1.5, "gas: mass +\nmetallicity Z", BLUE)
    box(ax, 5.4, 6.4, 3.4, 1.5, "SFR in this\n10 Myr epoch", FG)
    box(ax, 10.0, 6.4, 3.6, 1.5, "star clusters\n(biggest grows\nwith SFR)", GREEN)
    box(ax, 14.6, 6.4, 3.0, 1.5, "IMF in each\ncluster (Z, ρ)", ORANGE)
    box(ax, 13.7, 2.7, 3.9, 1.6, "sum = galaxy-wide IMF\n(IGIMF)", PINK)
    box(ax, 7.9, 2.7, 4.4, 1.6, "stars live & die:\nlifetimes, yields(m, Z)", FG)
    box(ax, 0.6, 2.7, 5.9, 1.6, "SN II (fast), AGB, SN Ia (delayed:\ndelay-time distribution)", ORANGE, fs=20)
    arr(ax, (4.35, 7.15), (5.25, 7.15)); arr(ax, (8.95, 7.15), (9.85, 7.15)); arr(ax, (13.75, 7.15), (14.45, 7.15))
    arr(ax, (16.1, 6.25), (16.0, 4.45)); arr(ax, (13.55, 3.5), (12.45, 3.5)); arr(ax, (7.75, 3.5), (6.65, 3.5))
    arr(ax, (2.4, 4.45), (2.4, 6.25), BLUE)
    ax.text(0.7, 5.2, "metals back\ninto the gas", fontsize=19, color=BLUE)
    ax.text(5.6, 5.3, "repeat every 10 Myr", fontsize=22, color=GREY)
    ax.text(0.6, 0.9, "galevo (GalIMF): Yan, Jeřábková & Kroupa 2017, 2019, 2020 - github.com/Azeret/galIMF", fontsize=18, color=GREY)
    ax.text(0.6, 8.35, "inputs: inflow, SFH, outflow;  output: [X/H] of gas and stars, M/L, SN rates", fontsize=19, color=GREY)
    save(fig, "galevo_flow")


# 6 ------------------------------------------------------------ what the data look like (schematic)
def obs_schematic():
    sketch_style()
    fig, ax = plt.subplots(figsize=(17, 8.6)); fig.subplots_adjust(left=0.1, right=0.97, top=0.95, bottom=0.14)
    fe = np.linspace(-3, 0.4, 200)

    def track(fe, plateau, knee, slope):
        return np.where(fe < knee, plateau, plateau - slope * (fe - knee))
    ax.plot(fe[fe > -2.5], track(fe, 0.32, -0.4, 0.45)[fe > -2.5], color=ORANGE, lw=4)
    ax.text(-2.4, 0.38, "Milky Way halo + thick disc (high-α)", color=ORANGE, fontsize=20)
    thin = fe[(fe > -0.8)]
    ax.plot(thin, 0.07 - 0.12 * (thin + 0.2), color=BLUE, lw=4)
    ax.text(-0.75, -0.15, "thin disc (low-α)", color=BLUE, fontsize=20)
    scl = fe[(fe > -2.9) & (fe < -1.0)]
    ax.plot(scl, track(scl, 0.3, -1.8, 0.4), color=GREEN, lw=4)
    ax.text(-2.95, -0.05, "Sculptor dwarf\n(knee ≈ −1.8)", color=GREEN, fontsize=20)
    fnx = fe[(fe > -1.6) & (fe < -0.3)]
    ax.plot(fnx, 0.1 - 0.35 * (fnx + 1.6), color=PINK, lw=4)
    ax.text(-0.95, -0.34, "Fornax dwarf", color=PINK, fontsize=20)
    ax.set_xlim(-3, 0.5); ax.set_ylim(-0.5, 0.55)
    ax.axhline(0, color=GREY, lw=1.5, ls=":"); ax.axvline(0, color=GREY, lw=1.5, ls=":")
    ax.set_xlabel("[Fe/H]"); ax.set_ylabel("[Mg/Fe]  (or [α/Fe])")
    ax.text(0.45, 0.5, "schematic — after Tolstoy, Hill & Tosi 2009 (ARA&A 47, 371);\nHayden et al. 2015 (APOGEE, ApJ 808, 132)",
            ha="right", va="top", fontsize=15, color=GREY)
    save(fig, "obs_schematic")


if __name__ == "__main__":
    periodic_table(); body(); dex_ruler(); sn_budget(); galevo_flow(); obs_schematic()
