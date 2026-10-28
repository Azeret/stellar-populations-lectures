"""Hand-drawn line-art sketches for the slides (white lines, transparent background).
They are meant as drafts: redraw any of them as Canva sketches if you prefer.
Run: python make_sketches.py  -> sketches/*.png
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, Ellipse, Rectangle, Polygon
from stellarpops import kroupa_xi, number_fraction, mass_fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sketches"); os.makedirs(OUT, exist_ok=True)
FONT = os.environ.get("XKCD_FONT", "/home/claude/ext/fonts/xkcd-font/xkcd-script/font/xkcd-script.ttf")
if os.path.exists(FONT):
    font_manager.fontManager.addfont(FONT)
INK, BLUE, ORANGE, PINK, GREEN, GREY = "#f4f4f6", "#1e8fd5", "#f5a623", "#ef5d8f", "#5cc8a1", "#9a9ab5"


def sketch_fig(w=16, h=9):
    plt.xkcd(scale=1.2, length=120, randomness=2)
    mpl.rcParams.update({"font.family": "xkcd Script" if os.path.exists(FONT) else "sans-serif",
                         "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
                         "xtick.color": INK, "ytick.color": INK, "path.effects": [],
                         "font.size": 26, "savefig.transparent": True})
    fig = plt.figure(figsize=(w, h))
    return fig


def arrow(ax, a, b, col=INK, lw=3, rad=0.0, ms=30):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=col,
                                 connectionstyle=f"arc3,rad={rad}"))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=120, transparent=True)
    plt.close(fig); plt.rcdefaults()


# 1 ---------------------------------------------------------------- SSP recipe
def ssp_recipe():
    fig = sketch_fig(); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")
    # isochrone
    t = np.linspace(0, 1, 100)
    ax.plot(1 + 2.4 * t ** 0.5, 2.2 + 3.6 * t ** 1.6, color=INK, lw=3)
    ax.plot([3.4, 3.0, 2.2], [5.8, 6.4, 7.1], color=ORANGE, lw=3)
    ax.text(2.3, 1.2, "isochrone\n(which stars\nare alive at t, Z)", ha="center", fontsize=22)
    ax.text(4.6, 4.6, "+", fontsize=60, ha="center")
    # IMF
    m = np.geomspace(0.1, 50, 50); y = np.log10(kroupa_xi(m) + 1e-9)
    ax.plot(5.6 + 1.0 * np.log10(m / 0.1), 4.2 + 0.5 * (y - y.min()) / 2, color=BLUE, lw=3)
    ax.text(7.2, 1.2, "IMF\n(how many\nof each mass)", ha="center", fontsize=22)
    ax.text(9.3, 4.6, "+", fontsize=60, ha="center")
    # star spectra
    w = np.linspace(0, 1, 200)
    for k, c in zip(range(3), [BLUE, INK, ORANGE]):
        s = 6.6 - k * 0.9 + 0.5 * np.exp(-((w - 0.2 - 0.25 * k) / 0.25) ** 2)
        s -= 0.25 * np.exp(-((w - 0.55) / 0.01) ** 2)
        ax.plot(10.0 + 2.0 * w, s - 1.6, color=c, lw=2.5)
    ax.text(11.0, 1.2, "spectra of\nthe stars", ha="center", fontsize=22)
    ax.text(12.9, 4.6, "=", fontsize=60, ha="center")
    s = 5.4 + 0.6 * np.exp(-((w - 0.5) / 0.4) ** 2) - 0.35 * np.exp(-((w - 0.55) / 0.012) ** 2) - 0.2 * np.exp(-((w - 0.3) / 0.01) ** 2)
    ax.plot(13.5 + 2.0 * w, s - 0.8, color=GREEN, lw=4)
    ax.text(14.5, 1.2, "spectrum of\nthe population\n(SSP)", ha="center", fontsize=22, color=GREEN)
    save(fig, "s1_ssp_recipe")


# 2 ---------------------------------------------------------------- bathtub
def bathtub():
    fig = sketch_fig(); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")
    tub = np.array([[4.5, 5.5], [5.0, 1.8], [11.0, 1.8], [11.5, 5.5]])
    ax.plot(tub[:, 0], tub[:, 1], color=INK, lw=4)
    ax.fill_between([4.85, 11.15], [1.85, 1.85], [3.9, 3.9], color=BLUE, alpha=0.35, lw=0)
    ax.plot([4.75, 11.25], [3.9, 3.9], color=BLUE, lw=3)
    ax.text(8, 2.7, "gas", ha="center", fontsize=34, color=INK)
    # tap / inflow
    ax.plot([2.0, 3.6, 3.6], [7.6, 7.6, 6.9], color=INK, lw=6)
    for x in (3.5, 3.65, 3.8):
        ax.plot([x, x + 0.3], [6.7, 4.2], color=BLUE, lw=2)
    ax.text(1.0, 8.1, "inflow of fresh gas", fontsize=24)
    # stars forming at the bottom (drain)
    arrow(ax, (8.0, 1.75), (8.0, 0.55), col=ORANGE, lw=4)
    ax.text(8.4, 0.6, "star formation  SFR = M_gas / τ", fontsize=24, color=ORANGE)
    # stars return enriched gas
    for x0 in (12.8, 13.4, 14.0):
        ax.plot(x0, 1.0, marker="*", ms=26, color=ORANGE)
    arrow(ax, (13.4, 1.6), (11.3, 4.4), col=PINK, lw=3, rad=0.3)
    ax.text(13.6, 2.6, "supernovae\nreturn metals", fontsize=22, color=PINK)
    # outflow
    arrow(ax, (9.5, 4.2), (12.5, 7.8), col=GREEN, lw=3, rad=-0.2)
    ax.text(12.0, 8.2, "galactic wind  (η × SFR)", fontsize=24, color=GREEN)
    ax.text(0.4, 4.0, "one zone:\nperfectly\nmixed", fontsize=22, color=GREY)
    save(fig, "s2_bathtub")


# 3 ---------------------------------------------------------------- two kinds of SNe
def sn_timeline():
    fig = sketch_fig(); ax = fig.add_axes([0.08, 0.2, 0.86, 0.7])
    t = np.geomspace(0.003, 13, 400)
    ii = np.where(t < 0.04, 1.0, 0.0)
    ia = np.where(t > 0.04, 0.04 / t, 0.0)
    ax.fill_between(t, ii, color=PINK, alpha=0.5, lw=0)
    ax.plot(t, ia, color=INK, lw=4)
    ax.set_xscale("log"); ax.set_xlim(0.003, 13); ax.set_ylim(0, 1.15); ax.set_yticks([])
    ax.set_xticks([0.01, 0.1, 1, 10]); ax.set_xticklabels(["10 Myr", "100 Myr", "1 Gyr", "10 Gyr"])
    ax.set_xlabel("time after a burst of star formation")
    ax.set_ylabel("supernova rate")
    ax.text(0.0045, 0.75, "SN II\nm > 8 Msun\nMg + O + some Fe", color=PINK, fontsize=24)
    ax.text(0.3, 0.45, "SN Ia: white dwarfs in binaries\nmostly Fe,  delay ~ 1/t", color=INK, fontsize=24)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "s3_sn_timeline")


# 4 ---------------------------------------------------------------- the knee
def knee():
    fig = sketch_fig(); ax = fig.add_axes([0.1, 0.17, 0.85, 0.75])
    fe = np.linspace(-3, 0.4, 200)
    def track(k):  # plateau then decline after knee k
        return 0.42 - 0.5 * np.log1p(np.exp(3.5 * (fe - k))) / 3.5 * 1.3
    ax.plot(fe, track(-0.6), color=ORANGE, lw=4)
    ax.plot(fe, track(-1.1), color=BLUE, lw=4)
    ax.plot(fe, track(-2.0), color=GREEN, lw=4)
    ax.axhline(0, color=GREY, lw=1.5, ls="--")
    ax.set_xlim(-3, 0.5); ax.set_ylim(-0.3, 0.6)
    ax.set_xlabel("[Fe/H]  (time → more iron)"); ax.set_ylabel("[Mg/Fe]")
    ax.text(-2.9, 0.48, "plateau: only SN II so far", fontsize=24)
    ax.annotate("knee: SN Ia\nkick in", xy=(-1.1, 0.38), xytext=(-1.6, 0.05), fontsize=24,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.5))
    ax.text(-0.45, 0.43, "fast", color=ORANGE, fontsize=26)
    ax.text(-1.0, 0.43, "", color=BLUE)
    ax.text(-2.75, -0.2, "slow", color=GREEN, fontsize=26)
    ax.text(-0.9, -0.12, "Milky Way", color=BLUE, fontsize=26)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "s4_knee_schematic")


# 5 ---------------------------------------------------------------- number / mass / light
def budget():
    fig = sketch_fig(); ax = fig.add_axes([0.1, 0.18, 0.86, 0.72])
    edges = [0.08, 0.5, 1, 8, 150]; labels = ["0.08-0.5", "0.5-1", "1-8", "8-150"]
    num = [number_fraction(a, b) for a, b in zip(edges[:-1], edges[1:])]
    mas = [mass_fraction(a, b) for a, b in zip(edges[:-1], edges[1:])]
    mm = np.geomspace(0.08, 150, 4000); w = kroupa_xi(mm)
    L = np.where(mm < 0.43, 0.23 * mm ** 2.3, np.where(mm < 2, mm ** 4, np.where(mm < 55, 1.4 * mm ** 3.5, 32000 * mm)))
    lum = np.array([np.trapezoid((w * L)[(mm >= a) & (mm < b)], mm[(mm >= a) & (mm < b)]) for a, b in zip(edges[:-1], edges[1:])])
    lum /= lum.sum()
    x = np.arange(4)
    for i, (v, c, n) in enumerate([(num, BLUE, "number"), (mas, ORANGE, "mass"), (lum, PINK, "light (newborn)")]):
        ax.bar(x + (i - 1) * 0.27, np.array(v) * 100, width=0.25, color=c, label=n)
    ax.set_xticks(x, labels); ax.set_xlabel("stellar mass [Msun]"); ax.set_ylabel("% of total")
    ax.legend(frameon=False, fontsize=24, loc="upper center")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "s5_number_mass_light")
    return num, mas, lum


# 6 ---------------------------------------------------------------- light -> mass
def light_to_mass():
    fig = sketch_fig(); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")
    ax.add_patch(Ellipse((2.5, 4.8), 3.6, 1.6, angle=20, fill=False, lw=3, color=INK))
    ax.add_patch(Ellipse((2.5, 4.8), 1.2, 0.6, angle=20, fill=True, color=ORANGE, alpha=0.6))
    ax.text(2.5, 2.8, "light L", ha="center", fontsize=30)
    ax.text(5.6, 4.6, "×", fontsize=60, ha="center")
    ax.text(8.0, 4.6, "M/L", ha="center", fontsize=54, color=BLUE)
    ax.text(8.0, 2.8, "from a model:\nage, Z, IMF", ha="center", fontsize=24, color=BLUE)
    ax.text(10.6, 4.6, "=", fontsize=60, ha="center")
    ax.text(13.3, 4.6, "M*", ha="center", fontsize=60, color=GREEN)
    ax.text(13.3, 2.8, "stellar mass", ha="center", fontsize=26, color=GREEN)
    ax.text(8.0, 7.5, "the IMF hides in here", ha="center", fontsize=26, color=PINK)
    arrow(ax, (8.0, 7.2), (8.0, 5.7), col=PINK)
    save(fig, "s6_light_to_mass")


if __name__ == "__main__":
    ssp_recipe(); bathtub(); sn_timeline(); knee(); out = budget(); light_to_mass()
    print("done", [round(100 * v, 1) for v in out[2]])


# 7 ---------------------------------------------------------------- IMF shapes
def imf_shapes():
    from stellarpops.imf import powerlaw_imf_xi
    fig = sketch_fig(); ax = fig.add_axes([0.12, 0.17, 0.83, 0.75])
    m = np.geomspace(0.08, 100, 300)
    def nrm(x): return x / np.trapezoid(x * m, m)
    sal = nrm(powerlaw_imf_xi(m, [0.08, 100], [2.35]))
    kro = nrm(powerlaw_imf_xi(m, [0.08, 0.5, 100], [1.3, 2.3]))
    chab = nrm(np.where(m < 1, np.exp(-(np.log10(m) - np.log10(0.079)) ** 2 / (2 * 0.69 ** 2)) / m,
                        np.exp(-(np.log10(1) - np.log10(0.079)) ** 2 / (2 * 0.69 ** 2)) * m ** -2.3))
    ax.loglog(m, sal, color=GREY, lw=3, ls="--"); ax.loglog(m, kro, color=BLUE, lw=4); ax.loglog(m, chab, color=ORANGE, lw=3)
    ax.text(0.09, sal[0] * 1.3, "Salpeter 1955", color=GREY, fontsize=24)
    ax.text(0.3, kro[60] * 0.15, "Kroupa 2001", color=BLUE, fontsize=24)
    ax.text(0.09, chab[0] * 0.25, "Chabrier 2003", color=ORANGE, fontsize=24)
    ax.text(8, sal[200] * 6, "slope -2.3 above ~0.5-1 Msun\n(almost everyone agrees)", fontsize=22)
    ax.text(0.09, 2e-3, "the low-mass end:\nthe hard part", fontsize=24, color=PINK)
    ax.set_xlabel("stellar mass [Msun]"); ax.set_ylabel("dN/dm  (per Msun formed)")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "s7_imf_shapes")


if __name__ == "__main__":
    imf_shapes()
