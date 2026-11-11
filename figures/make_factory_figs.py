"""Line-art sketches of the element 'factories' for Lecture 2 (progenitor + process + products).
Run: python make_factory_figs.py  ->  slides_elements/f*.png
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, Ellipse, Rectangle
from stellarpops.origins import SOURCES
from stellarpops.style import BG

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_elements"); os.makedirs(OUT, exist_ok=True)
FONT = os.environ.get("XKCD_FONT", "/home/claude/ext/fonts/xkcd-font/xkcd-script/font/xkcd-script.ttf")
if os.path.exists(FONT):
    font_manager.fontManager.addfont(FONT)
INK, BLUE, ORANGE, PINK, GREEN, GREY, VIOLET = "#f4f4f6", "#1e8fd5", "#f5a623", "#ef5d8f", "#5cc8a1", "#9a9ab5", "#b39dff"


def sketch(w=16, h=9):
    plt.rcdefaults(); plt.xkcd(scale=0.8, length=120, randomness=2)
    mpl.rcParams.update({"font.family": "xkcd Script" if os.path.exists(FONT) else "sans-serif", "text.color": INK,
                         "path.effects": [], "font.size": 24, "figure.facecolor": BG, "savefig.facecolor": BG})
    fig = plt.figure(figsize=(w, h)); ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off"); ax.set_aspect("equal")
    return fig, ax


def arrow(ax, a, b, col=INK, lw=3, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=28, lw=lw, color=col, connectionstyle=f"arc3,rad={rad}"))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=110); plt.close(fig); plt.rcdefaults(); print("saved", name)


# F1 ------------------------------------------------------------ massive star: onion + collapse
def massive_star():
    fig, ax = sketch()
    cx, cy = 4.6, 4.5
    shells = [(3.9, "H", BLUE), (3.1, "He", GREEN), (2.4, "C", ORANGE), (1.75, "O, Ne", PINK), (1.15, "Si, S", VIOLET), (0.55, "Fe", INK)]
    for r, lab, c in shells:
        ax.add_patch(Circle((cx, cy), r, fill=False, ec=c, lw=3))
    for (r, lab, c), (r2, _, _) in zip(shells, shells[1:] + [(0, "", "")]):
        ax.text(cx, cy + (r + r2) / 2 - 0.15, lab, ha="center", va="center", color=c, fontsize=22)
    ax.text(cx, 0.15, "a star above 8 Msun near its end (not to scale)", ha="center", fontsize=19, color=GREY)
    x0 = 9.3
    ax.text(x0, 8.3, "1. burns H → He → C → O, Ne → Si → Fe", fontsize=22, color=INK)
    ax.text(x0, 7.7, "   in shells, faster and faster (Si: one day)", fontsize=19, color=GREY)
    ax.text(x0, 6.8, "2. iron cannot release energy:", fontsize=22, color=INK)
    ax.text(x0, 6.2, "   the core collapses → neutron star / BH", fontsize=19, color=GREY)
    ax.text(x0, 5.3, "3. the shock heats the shells:", fontsize=22, color=INK)
    ax.text(x0, 4.7, "   explosive burning makes more Si, S, Ca", fontsize=19, color=GREY)
    ax.text(x0, 4.2, "   and ~0.07 Msun of radioactive Ni-56 → Fe", fontsize=19, color=GREY)
    ax.text(x0, 3.3, "4. everything outside is thrown out:", fontsize=22, color=INK)
    ax.text(x0, 2.7, "   O, Ne, Mg, Si, S, Ca ... a bit of Fe", fontsize=19, color=GREY)
    ax.text(x0, 1.6, "life: 3 Myr (100 Msun) to 40 Myr (8 Msun)", fontsize=21, color=BLUE)
    ax.text(x0, 1.0, "→ the PROMPT source of α-elements", fontsize=21, color=BLUE)
    save(fig, "f1_massive_star")


# F2 ------------------------------------------------------------ AGB star: s-process
def agb_star():
    fig, ax = sketch()
    cx, cy = 4.4, 4.6
    ax.add_patch(Circle((cx, cy), 3.9, fill=False, ec=GREEN, lw=3, ls="--"))
    ax.add_patch(Circle((cx, cy), 0.95, fill=False, ec=ORANGE, lw=3))
    ax.add_patch(Circle((cx, cy), 0.6, fill=False, ec=PINK, lw=3))
    ax.add_patch(Circle((cx, cy), 0.35, fill=False, ec=INK, lw=3))
    ax.text(cx, cy, "C,O", ha="center", va="center", fontsize=15)
    ax.text(cx + 1.1, cy + 1.0, "He shell: pulses,\nneutrons → s-process", fontsize=18, color=PINK)
    ax.text(cx - 3.2, cy - 2.3, "huge cool envelope\n(convection)", fontsize=18, color=GREEN)
    arrow(ax, (cx + 0.5, cy - 0.7), (cx + 2.2, cy - 2.4), GREEN, rad=0.3)
    ax.text(cx + 1.7, cy - 3.1, "dredge-up\n→ surface", fontsize=17, color=GREEN)
    for ang in np.linspace(0.3, 2.8, 6):
        arrow(ax, (cx + 4.0 * np.cos(ang), cy + 4.0 * np.sin(ang)), (cx + 4.6 * np.cos(ang), cy + 4.6 * np.sin(ang)), GREY, lw=2)
    ax.text(cx, 8.75, "slow wind", ha="center", fontsize=18, color=GREY)
    ax.text(cx, 0.15, "a 1–8 Msun star at the end of its life (AGB)", ha="center", fontsize=19, color=GREY)
    x0 = 9.4
    ax.text(x0, 8.3, "1. H and He burn in thin shells", fontsize=22)
    ax.text(x0, 7.7, "   around a C/O core (future white dwarf)", fontsize=19, color=GREY)
    ax.text(x0, 6.8, "2. He-shell flashes release neutrons", fontsize=22)
    ax.text(x0, 6.2, "   (C-13 + He-4 → O-16 + n): few neutrons, slowly", fontsize=19, color=GREY)
    ax.text(x0, 5.3, "3. iron seeds catch them one by one:", fontsize=22)
    ax.text(x0, 4.7, "   s-process → Sr, Y, Zr, Ba, La, Pb", fontsize=19, color=GREY)
    ax.text(x0, 3.8, "4. convection lifts C, N, s-elements up;", fontsize=22)
    ax.text(x0, 3.2, "   the wind blows them into space", fontsize=19, color=GREY)
    ax.text(x0, 1.6, "life: ~100 Myr (5 Msun) to 10 Gyr (1 Msun)", fontsize=21, color=GREEN)
    ax.text(x0, 1.0, "→ a DELAYED source of C, N, Ba", fontsize=21, color=GREEN)
    save(fig, "f2_agb_star")


# F3 ------------------------------------------------------------ SN Ia
def sn_ia():
    fig, ax = sketch()
    ax.add_patch(Circle((2.0, 6.2), 0.45, fill=False, ec=INK, lw=3)); ax.text(2.0, 5.3, "white dwarf\n(C/O, ~1.4 Msun)", ha="center", fontsize=16, va="top")
    ax.add_patch(Circle((5.3, 6.2), 1.4, fill=False, ec=ORANGE, lw=3)); ax.text(5.3, 4.5, "companion star\ngives it gas", ha="center", fontsize=16, va="top")
    arrow(ax, (4.0, 6.5), (2.55, 6.3), ORANGE, rad=0.25)
    ax.text(3.5, 8.3, "or: two white dwarfs merge", ha="center", fontsize=17, color=GREY)
    arrow(ax, (3.5, 3.5), (3.5, 2.6), INK)
    for ang in np.linspace(0, 2 * np.pi, 14, endpoint=False):
        ax.plot([3.5 + 0.4 * np.cos(ang), 3.5 + 1.2 * np.cos(ang)], [1.4 + 0.4 * np.sin(ang), 1.4 + 1.2 * np.sin(ang)], color=ORANGE, lw=3)
    ax.text(3.5, 1.4, "boom", ha="center", va="center", fontsize=20, color=ORANGE)
    x0 = 8.4
    ax.text(x0, 8.3, "1. the white dwarf grows towards 1.4 Msun", fontsize=22)
    ax.text(x0, 7.7, "   (Chandrasekhar mass) or two WDs merge", fontsize=19, color=GREY)
    ax.text(x0, 6.8, "2. carbon ignites in degenerate matter:", fontsize=22)
    ax.text(x0, 6.2, "   no expansion to cool it → runaway", fontsize=19, color=GREY)
    ax.text(x0, 5.3, "3. the whole star burns in ~1 s:", fontsize=22)
    ax.text(x0, 4.7, "   ~0.6–0.7 Msun of Ni-56 → Co-56 → Fe-56", fontsize=19, color=GREY)
    ax.text(x0, 4.2, "   + Si, S, Ca, Mn;  almost no O or Mg", fontsize=19, color=GREY)
    ax.text(x0, 3.3, "4. nothing left behind", fontsize=22)
    ax.text(x0, 1.6, "delay: the WD must first form (≥ 40 Myr)", fontsize=21, color=ORANGE)
    ax.text(x0, 1.0, "and grow → ~1/t from 40 Myr to 10+ Gyr", fontsize=21, color=ORANGE)
    save(fig, "f3_sn_ia")


# F4 ------------------------------------------------------------ s vs r on the nuclide chart
def neutron_captures():
    fig, ax = sketch()
    ax.plot([0.8, 8.4], [0.8, 7.6], color=GREY, lw=2)
    ax.annotate("", (8.8, 0.8), (0.6, 0.8), arrowprops=dict(arrowstyle="<-", color=INK, lw=2.5))
    ax.annotate("", (0.8, 8.4), (0.8, 0.6), arrowprops=dict(arrowstyle="<-", color=INK, lw=2.5))
    ax.text(8.9, 0.6, "neutrons N", fontsize=19, va="top", ha="right"); ax.text(1.0, 8.4, "protons Z", fontsize=19)
    ax.text(5.8, 4.4, "stable nuclei", fontsize=17, color=GREY, rotation=38)
    x, y = 1.6, 1.6
    for _ in range(9):
        ax.plot([x, x + 1.1], [y, y], color=GREEN, lw=4); x += 1.1          # two neutron captures: N + 2
        ax.plot([x, x - 0.45], [y, y + 0.55], color=GREEN, lw=4); x -= 0.45; y += 0.55   # beta decay: N - 1, Z + 1
    ax.text(3.4, 5.7, "s-process: capture a neutron (→),\nwait, β-decay n → p (↖),\ncapture again: it walks\nalong the stable nuclei", fontsize=17, color=GREEN)
    ax.plot([2.4, 7.6], [1.9, 3.6], color=PINK, lw=4)
    for xx in np.linspace(3.2, 7.4, 6):
        yy = 1.9 + (xx - 2.4) * (1.7 / 5.2)
        arrow(ax, (xx, yy + 0.05), (xx - 0.9, yy + 0.95), PINK, lw=2)
    ax.text(6.0, 1.3, "r-process: many neutrons at once,\nfar from stability; then β-decays\nback (diagonal arrows)", fontsize=17, color=PINK)
    x0 = 9.6
    ax.text(x0, 8.3, "Beyond iron, fusion costs energy:", fontsize=22)
    ax.text(x0, 7.7, "heavy nuclei are built by adding neutrons", fontsize=19, color=GREY)
    ax.text(x0, 6.6, "s (slow): ~1 capture per 1–1000 yr", fontsize=22, color=GREEN)
    ax.text(x0, 6.0, "   AGB stars → Sr, Y, Ba, La, Pb", fontsize=19, color=GREY)
    ax.text(x0, 5.4, "   (Ba stars: s-elements from a companion)", fontsize=17, color=GREY)
    ax.text(x0, 4.4, "r (rapid): > 10^20 neutrons/cm^3 for ~1 s", fontsize=22, color=PINK)
    ax.text(x0, 3.8, "   neutron-star mergers → Eu, Pt, Au, U", fontsize=19, color=GREY)
    ax.text(x0, 3.2, "   seen: kilonova of GW170817 (2017)", fontsize=17, color=GREY)
    ax.text(x0, 2.0, "Ba is mostly s, Eu almost only r:", fontsize=21)
    ax.text(x0, 1.4, "[Ba/Eu] tells which process dominated", fontsize=19, color=GREY)
    save(fig, "f4_neutron_captures")


# F0 ------------------------------------------------------------ overview table (clean)
def overview():
    plt.rcdefaults()
    mpl.rcParams.update({"figure.facecolor": BG, "savefig.facecolor": BG, "text.color": INK, "font.size": 17, "font.family": "DejaVu Sans"})
    rows = [("bb", "the young Universe", "first 3 minutes:\nprotons + neutrons fuse", "H, He, a little Li", "13.8 Gyr ago, once"),
            ("cr", "fast particles\nfrom supernovae", "fast protons break\nC, N, O in space", "Li, Be, B", "all the time"),
            ("ccsn", "massive star\n> 8 M☉", "shell burning + core\ncollapse explosion", "O, Ne, Mg, Si, S, Ca,\n~40% of Fe, half of C", "3–40 Myr\n(prompt)"),
            ("agb", "low/intermediate-\nmass star 1–8 M☉", "H/He shells, dredge-up,\ns-process", "C, N, Sr, Ba, Pb", "0.1–10 Gyr"),
            ("ia", "white dwarf in\na binary", "thermonuclear runaway\nof C/O", "~60% of Fe, Mn, Ni", "40 Myr–10+ Gyr\n(delayed)"),
            ("r", "two neutron stars\n(merging)", "r-process (rapid\nneutron capture)", "Eu, Pt, Au, U", "10 Myr–Gyr")]
    fig = plt.figure(figsize=(18, 8.4)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 18); ax.set_ylim(0, 8.4)
    cols = [0.9, 5.0, 8.5, 12.0, 15.3]
    for x, h in zip(cols, ["factory", "who explodes / dies", "what happens", "main products", "delay"]):
        ax.text(x, 7.9, h, fontsize=19, color=GREY, fontweight="bold")
    for i, (k, *cells) in enumerate(rows):
        y = 6.75 - i * 1.25
        ax.add_patch(Rectangle((0.3, y - 0.45), 0.4, 0.9, color=SOURCES[k][1]))
        ax.text(cols[0], y, SOURCES[k][0].replace(" ", "\n", 1) if len(SOURCES[k][0]) > 14 else SOURCES[k][0], va="center", fontsize=18, fontweight="bold", color=SOURCES[k][1] if k != "cr" else INK)
        for x, c in zip(cols[1:], cells):
            ax.text(x, y, c, va="center", fontsize=17)
        ax.plot([0.3, 17.7], [y - 0.62, y - 0.62], color="#3a3956", lw=1)
    save(fig, "f0_factories_table")


if __name__ == "__main__":
    overview(); massive_star(); agb_star(); sn_ia(); neutron_captures()
