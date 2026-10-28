"""Animations 2-5 from FaSTAR spectra (run precompute_fastar.py first).

A2  an SSP ageing from 30 Myr to 13 Gyr: spectrum per Msun formed + M/L_V
A3  metallicity from [M/H] = -2.2 to +0.25 at 10 Gyr
A4  IMF slope from 1.3 to 3.3: IMF shape, spectral change, M/L U-shape
A5  stochastic IMF sampling: 50 / 500 / 5000 stars vs the smooth model
Run: python a2_a5_fastar.py [a2 a3 a4 a5]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from stellarpops.style import use_slide_style, BLUE, ORANGE, PINK, GREEN, FG, GREY

OUT = os.path.join(os.path.dirname(__file__), "out")
use_slide_style()
WRITER = dict(fps=30, codec="libx264", extra_args=["-preset", "veryfast", "-pix_fmt", "yuv420p", "-crf", "20"])
G = np.load(os.path.join(OUT, "fastar_grid.npz"))
wave = G["wave"]
PREVIEW = bool(os.environ.get("PREVIEW"))
FEATURES = [(3950, "Ca H+K"), (4102, "Hδ"), (4340, "Hγ"), (4861, "Hβ"),
            (5175, "Mg b"), (5270, "Fe"), (5893, "Na D"), (6563, "Hα"), (7050, "TiO")]


def norm(s, lo=5400, hi=5600):
    sel = (wave > lo) & (wave < hi)
    return s / np.median(s[sel])


def mark_features(ax, y, which=None, size=15):
    for w, name in FEATURES:
        if which and name not in which:
            continue
        ax.axvline(w, color=GREY, lw=1, ls=":", zorder=0)
        ax.text(w, y, name, color=GREY, fontsize=size, ha="center", va="bottom", transform=ax.get_xaxis_transform())


def save(fig, draw, seq, name, stills):
    if PREVIEW:
        for v in stills:
            draw(v); fig.savefig(os.path.join(OUT, f"{name}_preview_{v:.3g}.png"))
        return
    FuncAnimation(fig, lambda k: draw(seq[k]), frames=len(seq)).save(
        os.path.join(OUT, f"{name}.mp4"), writer=FFMpegWriter(**WRITER))
    draw(seq[-1]); fig.savefig(os.path.join(OUT, f"{name}_final.png"))


# ------------------------------------------------------------------ A2
def a2():
    ages, specs, ml = G["ages"], G["spec_age"], G["ml_age"]
    cmap = plt.get_cmap("RdYlBu_r")
    col = lambda a: cmap((np.log10(a) - np.log10(0.03)) / (np.log10(13) - np.log10(0.03)))
    fig = plt.figure(figsize=(19.2, 10.8))
    ax = fig.add_axes([0.07, 0.11, 0.56, 0.72]); axm = fig.add_axes([0.71, 0.11, 0.26, 0.72])
    fig.text(0.5, 0.93, "One stellar population, getting older", ha="center", fontsize=32, weight="bold", color=FG)
    lab = fig.text(0.07, 0.87, "", fontsize=26, color=FG)
    seq = np.concatenate([np.full(20, 0), np.repeat(np.arange(len(ages)), 5), np.full(60, len(ages) - 1)])

    def draw(k):
        k = int(k)
        ax.cla()
        for j in range(0, k, 6):
            ax.plot(wave, specs[j] * 1e12, color=col(ages[j]), lw=1, alpha=0.35)
        ax.plot(wave, specs[k] * 1e12, color=col(ages[k]), lw=2.5)
        ax.set_yscale("log"); ax.set_ylim(specs.min() * 1e12 * 0.5, specs.max() * 1e12 * 1.5)
        ax.set_xlim(wave[0], wave[-1]); ax.set_xlabel("wavelength [Å]")
        ax.set_ylabel("flux per M$_\\odot$ formed (arbitrary units)")
        mark_features(ax, 1.01, ["Ca H+K", "Hδ", "Hβ", "Mg b", "Na D", "TiO"])
        axm.cla()
        axm.plot(ages[: k + 1], ml[: k + 1], color=FG, lw=2)
        axm.plot(ages[k], ml[k], "o", color=col(ages[k]), ms=16)
        axm.set_xscale("log"); axm.set_yscale("log"); axm.set_xlim(0.025, 16); axm.set_ylim(0.04, 8)
        axm.set_xlabel("age [Gyr]"); axm.set_ylabel("M/L$_V$  (stars + remnants)")
        a = ages[k]
        lab.set_text(f"age = {a*1000:,.0f} Myr" if a < 1 else f"age = {a:.1f} Gyr")

    save(fig, draw, seq, "a2_ssp_ageing", [0, 30, len(ages) - 1])


# ------------------------------------------------------------------ A3
def a3():
    mets, specs = G["mets"], G["spec_met"]
    cmap = plt.get_cmap("viridis")
    fig = plt.figure(figsize=(19.2, 10.8))
    ax = fig.add_axes([0.07, 0.11, 0.56, 0.72]); axz = fig.add_axes([0.71, 0.11, 0.26, 0.72])
    fig.text(0.5, 0.93, "Same age (10 Gyr), more metals", ha="center", fontsize=32, weight="bold", color=FG)
    lab = fig.text(0.07, 0.87, "", fontsize=26, color=FG)
    seq = np.concatenate([np.full(20, 0), np.repeat(np.arange(len(mets)), 6), np.full(60, len(mets) - 1)])
    zoom = (wave > 5050) & (wave < 5450)

    def draw(k):
        k = int(k); c = cmap(k / (len(mets) - 1))
        ax.cla()
        ax.plot(wave, norm(specs[0]), color=GREY, lw=1, label="[M/H] = −2.2")
        ax.plot(wave, norm(specs[k]), color=c, lw=2)
        ax.set_xlim(wave[0], wave[-1]); ax.set_ylim(0, 1.6); ax.set_xlabel("wavelength [Å]")
        ax.set_ylabel("flux (normalised at 5500 Å)"); ax.legend(loc="lower right")
        mark_features(ax, 1.01, ["Ca H+K", "Hβ", "Mg b", "Na D", "TiO"])
        axz.cla()
        axz.plot(wave[zoom], norm(specs[0])[zoom], color=GREY, lw=1.5)
        axz.plot(wave[zoom], norm(specs[k])[zoom], color=c, lw=2.5)
        axz.set_ylim(0.55, 1.2); axz.set_xlabel("wavelength [Å]"); axz.set_title("zoom: Mg b and Fe lines", fontsize=20)
        lab.set_text(f"[M/H] = {mets[k]:+.2f}")

    save(fig, draw, seq, "a3_ssp_metallicity", [0, len(mets) - 1])


# ------------------------------------------------------------------ A4
def a4():
    al, specs, ml = G["alphas"], G["spec_alpha"], G["ml_alpha"]
    i0 = int(np.argmin(abs(al - 2.3)))
    ref = norm(specs[i0], 6000, 6200)
    idx = np.concatenate([np.full(30, i0), np.linspace(i0, 0, 50), np.full(25, 0),
                          np.linspace(0, len(al) - 1, 120), np.full(25, len(al) - 1),
                          np.linspace(len(al) - 1, i0, 60), np.full(40, i0)]).round().astype(int)
    fig = plt.figure(figsize=(19.2, 10.8))
    axi = fig.add_axes([0.06, 0.53, 0.25, 0.30]); axr = fig.add_axes([0.06, 0.11, 0.55, 0.30])
    axm = fig.add_axes([0.70, 0.11, 0.27, 0.72])
    fig.text(0.5, 0.93, "Change the IMF: the spectrum barely moves, the mass does", ha="center",
             fontsize=30, weight="bold", color=FG)
    lab = fig.text(0.36, 0.70, "", fontsize=28, color=FG)
    note = fig.text(0.36, 0.62, "", fontsize=20, color=GREY)
    m = np.geomspace(0.1, 100, 300)

    def draw(k):
        k = int(k); a = al[k]
        axi.cla()
        for aa, cc, ls in ((2.3, GREY, "--"), (a, BLUE, "-")):
            xi = m ** (-aa); xi /= np.trapezoid(xi * m, m)
            axi.loglog(m, xi, color=cc, ls=ls, lw=2.5)
        axi.set_xlabel("m [M$_\\odot$]"); axi.set_ylabel("ξ(m) per M$_\\odot$"); axi.set_ylim(1e-7, 1e2)
        axr.cla()
        axr.plot(wave, norm(specs[k], 6000, 6200) / ref, color=BLUE, lw=1.8)
        axr.axhline(1, color=GREY, ls="--", lw=1)
        axr.set_xlim(wave[0], wave[-1]); axr.set_ylim(0.85, 1.15)
        axr.set_xlabel("wavelength [Å]"); axr.set_ylabel("spectrum / Kroupa-like")
        mark_features(axr, 1.02, ["Ca H+K", "Mg b", "Na D", "TiO"], size=14)
        axm.cla()
        axm.plot(al, ml, color=FG, lw=2)
        axm.plot(a, ml[k], "o", color=ORANGE, ms=16)
        axm.set_xlabel("IMF slope α  (dN/dm ∝ m$^{-\\alpha}$)"); axm.set_ylabel("M/L$_V$ at 10 Gyr (stars + remnants)")
        axm.text(1.35, ml.max() * 0.93, "top-heavy:\nremnants", color=GREY, fontsize=17, va="top")
        axm.text(3.25, ml.max() * 0.93, "bottom-heavy:\ndwarfs", color=GREY, fontsize=17, va="top", ha="right")
        axm.set_ylim(0, ml.max() * 1.05)
        lab.set_text(f"α = {a:.2f}")
        note.set_text("Salpeter = 2.35" if abs(a - 2.35) < 0.06 else ("top-heavy" if a < 2.2 else ("bottom-heavy" if a > 2.5 else "")))

    save(fig, draw, idx, "a4_ssp_imf", [0, i0, len(al) - 1])


# ------------------------------------------------------------------ A5
def a5(age=0.1):
    ns = [int(n) for n in G["nstars"]]
    ref = norm(G[f"ref_{age}"])
    cols = [PINK, ORANGE, GREEN]
    fig = plt.figure(figsize=(19.2, 10.8))
    fig.text(0.5, 0.93, f"Few stars, noisy light: stochastic IMF sampling ({age*1000:.0f} Myr)" if age < 1 else f"Few stars, noisy light ({age:.0f} Gyr)", ha="center",
             fontsize=30, weight="bold", color=FG)
    axes = [fig.add_axes([0.08, 0.64 - 0.265 * i, 0.88, 0.2]) for i in range(3)]
    nreal = G[f"semi_{age}_{ns[0]}"].shape[0]
    seq = np.repeat(np.arange(nreal), 15)

    def draw(k):
        k = int(k)
        for ax, n, c in zip(axes, ns, cols):
            ax.cla()
            ax.plot(wave, ref, color=GREY, lw=1.5, ls="--")
            ax.plot(wave, norm(G[f"semi_{age}_{n}"][k]), color=c, lw=1.6)
            ax.set_xlim(wave[0], wave[-1]); ax.set_ylim(0, 2.2)
            ax.text(0.0, 1.02, f"{n:,} stars   (realisation {k + 1})", transform=ax.transAxes, fontsize=20, color=c, va="bottom")
            if ax is not axes[-1]:
                ax.set_xticklabels([])
        axes[-1].set_xlabel("wavelength [Å]")
        axes[1].set_ylabel("flux (normalised)")
        axes[0].text(1.0, 1.02, "dashed: infinitely many stars", transform=axes[0].transAxes,
                     fontsize=17, color=GREY, ha="right", va="bottom")

    save(fig, draw, seq, f"a5_stochastic_{age:g}Gyr", [0, 5])


if __name__ == "__main__":
    which = sys.argv[1:] or ["a2", "a3", "a4", "a5"]
    for w in which:
        globals()[w]()
        if w == "a5":
            a5(10.0)     # the old version too
    print("done", which)
