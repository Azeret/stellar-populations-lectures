"""Metal-poor / metal-rich scale as used in papers: [Fe/H] or [M/H], Z/Zsun and Z on one ruler,
with the standard names (Beers & Christlieb 2005).  Writes slides_elements/n3_metal_scale*.png
Run: python make_metal_scale.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from stellarpops.style import BG, FG, BLUE, ORANGE, PINK, GREEN, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_elements"); os.makedirs(OUT, exist_ok=True)
ZSUN = 0.0134          # Asplund et al. 2009 (present-day photosphere ~0.0134)

# (lo, hi, name, colour) -- Beers & Christlieb (2005) naming
BANDS = [(-5.3, -5, "HMP\nhyper", "#7a2e4f"), (-5, -4, "UMP\nultra\nmetal-poor", "#a8395f"),
         (-4, -3, "EMP\nextremely\nmetal-poor", "#c9476d"), (-3, -2, "VMP\nvery\nmetal-poor", "#e0607f"),
         (-2, -1, "MP\nmetal-poor", "#e98aa0"), (-1, 0, "mildly\nmetal-poor", "#6f6f8f"),
         (0, 0.5, "metal-\nrich", "#2f86c9"), (0.5, 0.8, "super\nrich", "#1b5f99")]


def zstr(x):
    z = ZSUN * 10 ** x
    return f"{z:.2g}" if z >= 1e-4 else f"{z:.1e}".replace("e-0", "e-")


def ratio_str(x):
    r = 10 ** x
    return {0: "1"}.get(x, f"1/{int(round(1 / r)):,}".replace(",", " ") if r < 1 else f"{r:.0f}")


def draw(quiz=False):
    plt.rcdefaults()
    mpl.rcParams.update({"figure.facecolor": BG, "savefig.facecolor": BG, "text.color": FG, "font.family": "DejaVu Sans"})
    top = 12.2 if quiz else 9.3
    fig = plt.figure(figsize=(11.2, 6.8 if not quiz else 7.6)); ax = fig.add_axes([0.01, 0.02, 0.98, 0.96])
    ax.set_xlim(-6.75, 0.85); ax.set_ylim(0.2, top); ax.axis("off")

    # name bands
    for lo, hi, name, c in BANDS:
        ax.add_patch(Rectangle((lo, 7.0), hi - lo, 2.0, color=c, ec=BG, lw=2))
        fs = 12 if hi - lo >= 1 else 9.5
        ax.text((lo + hi) / 2, 8.0, name, ha="center", va="center", fontsize=fs, color="white", fontweight="bold", linespacing=1.05)
    ax.text(-6.7, 8.0, "what papers\ncall it", fontsize=13, color=GREY, va="center")

    # main axis
    y0 = 6.5
    ax.plot([-5.3, 0.8], [y0, y0], color=FG, lw=2)
    for x in range(-5, 1):
        ax.plot([x, x], [y0 - 0.15, y0 + 0.15], color=FG, lw=2)
        ax.text(x, y0 - 0.55, f"{x:+d}".replace("+0", "0").replace("-", "−"), ha="center", fontsize=17, fontweight="bold")
    ax.plot([0.3, 0.3], [y0 - 0.1, y0 + 0.1], color=FG, lw=1.5); ax.text(0.3, y0 - 0.5, "+0.3", ha="center", fontsize=11, color=GREY)
    ax.text(-6.7, y0 - 0.4, "[Fe/H] or [M/H]\n(dex)", fontsize=13, color=ORANGE, va="center", fontweight="bold")

    # Z / Zsun and Z rows
    for x in range(-5, 1):
        ax.text(x, 4.75, ratio_str(x), ha="center", fontsize=12.5, color=GREEN)
        ax.text(x, 3.55, zstr(x), ha="center", fontsize=12.5, color=BLUE)
    ax.text(0.3, 4.75, "2", ha="center", fontsize=12.5, color=GREEN)
    ax.text(-6.7, 4.85, "Z / Z☉\n(× the Sun)", fontsize=13, color=GREEN, va="center", fontweight="bold")
    ax.text(-6.7, 3.65, "Z\n(mass fraction)", fontsize=13, color=BLUE, va="center", fontweight="bold")

    # how to convert + trap
    ax.text(-6.7, 2.25, "convert:   Z / Z☉ = 10^[M/H]      Z = 0.0134 × 10^[M/H]      [M/H] = log₁₀(Z / 0.0134)", fontsize=13.5, color=FG)
    ax.text(-6.7, 1.35, "trap: older papers and isochrones call Z = 0.02 \"solar\"; today Z☉ ≈ 0.013–0.014, so Z = 0.02 is [M/H] ≈ +0.17",
            fontsize=12, color=GREY)
    ax.text(-6.7, 0.55, "names: Beers & Christlieb (2005);  Z☉ = 0.0134: Asplund et al. (2009)", fontsize=10.5, color=GREY)

    if quiz:
        # (x on the scale, letter, value, colour, letter x, letter y)
        opts = [(0.3, "A", "[Fe/H] = +0.3", FG, 0.6, 9.9), (np.log10(0.02 / ZSUN), "B", "Z = 0.02  → [M/H] = +0.17", FG, -0.15, 9.9),
                (-0.5, "C", "[M/H] = −0.5", FG, -0.5, 9.9), (-2.0, "D", "[Fe/H] = −2.0  ← most metal-poor", PINK, -2.0, 9.9)]
        for i, (x, L, val, c, tx, ty) in enumerate(opts):
            ax.plot([x, x], [y0, 7.0], color=c, lw=2, ls=":", zorder=1)
            ax.plot(x, y0, "o", ms=12, color=c, mec=BG, mew=2, zorder=5)
            ax.annotate(L, xy=(x, 9.05), xytext=(tx, ty), ha="center", va="center", fontsize=16, color=c, fontweight="bold",
                        bbox=dict(boxstyle="circle,pad=0.2", fc=BG, ec=c, lw=1.8),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8, shrinkA=0, shrinkB=0))
            ax.text(-6.7, 11.75 - i * 0.55, f"{L}   {val}", fontsize=14.5, color=c, fontweight="bold", va="center")
    name = "n3_metal_scale_quiz" if quiz else "n3_metal_scale"
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=150); plt.close(fig); print("saved", name)


if __name__ == "__main__":
    print("Z=0.02 ->", round(np.log10(0.02 / ZSUN), 3), "  [M/H]=-0.5 -> Z =", round(ZSUN * 10 ** -0.5, 5))
    draw(False); draw(True)
