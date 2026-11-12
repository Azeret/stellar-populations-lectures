"""Two figures for the [Mg/Fe] plateau (Lecture 2):
p1_first_enrichment: from metal-free gas to the plateau (toy model tracks with time stamps + clouds enriched by a few SNe)
p2_topheavy_plateau: why a top-heavy IMF raises the plateau (per-SN Mg and Fe yields vs mass, and the IMF weights)
Yields: Kobayashi et al. 2006, Z = 0.0004, as tabulated in GalIMF (data/kobayashi06_Z0.0004_MgFe.json).
Run: python make_plateau_figs.py -> slides_elements/p*.png"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, matplotlib.pyplot as plt
from stellarpops import run_one_zone
from stellarpops.style import use_slide_style, BLUE, ORANGE, PINK, GREEN, FG, GREY, BG

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "slides_elements")
Y = json.load(open(os.path.join(HERE, "..", "data", "kobayashi06_Z0.0004_MgFe.json")))
M, MG, FE = (np.array(Y[k]) for k in ("mass", "Mg", "Fe"))
SUN = 7.14e-4 / 1.30e-3                      # solar Mg/Fe by mass (Asplund+09)
PAPER = np.array([13, 15, 18, 20, 25, 30, 40.])
mg = lambda m: np.interp(m, M, MG); fe = lambda m: np.interp(m, M, FE)


def plateau(alpha, lo=8, hi=100):
    g = np.linspace(lo, hi, 4000); w = g ** -alpha
    return np.log10(np.trapezoid(w * mg(g), g) / np.trapezoid(w * fe(g), g) / SUN)


def fig_topheavy():
    use_slide_style()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10.8, 7.6), sharex=True, gridspec_kw=dict(height_ratios=[1.15, 1], hspace=0.08))
    g = np.geomspace(8.05, 100, 400)
    a1.plot(g, mg(g), color=BLUE, lw=4, label="Mg made per supernova")
    a1.plot(g, fe(g), color=ORANGE, lw=4, label="Fe made per supernova")
    a1.plot(PAPER, mg(PAPER), "o", color=BLUE, ms=8); a1.plot(PAPER, fe(PAPER), "o", color=ORANGE, ms=8)
    a1.axvspan(40, 100, color=GREY, alpha=0.12); a1.text(63, 0.43, "extrapolated", color=GREY, fontsize=14, ha="center")
    a1.set_ylabel("M☉ per supernova"); a1.set_ylim(0, 0.55); a1.legend(loc="upper left", fontsize=16)
    a1.annotate("Mg: ×6 from 13 to 40 M☉\n(bigger O/Mg shells)", (30, mg(30)), (14.5, 0.30), color=BLUE, fontsize=15,
                arrowprops=dict(arrowstyle="->", color=BLUE))
    a1.text(9, 0.11, "Fe ≈ 0.07 M☉ for every mass\n(Ni-56 made next to the core)", color=ORANGE, fontsize=15)
    # IMF weights: share of all SN II per unit log mass
    for al, col, lab in [(2.3, BLUE, "Kroupa (α = 2.3)"), (1.9, PINK, "top-heavy (α = 1.9)")]:
        w = g ** (1 - al); w /= np.trapezoid(w, np.log10(g))
        f25 = np.trapezoid((g ** -al)[g >= 25], g[g >= 25]) / np.trapezoid(g ** -al, g)
        a2.plot(g, w, color=col, lw=4, ls="-" if al == 2.3 else "--",
                label=f"{lab}: {100 * f25:.0f}% of SNe above 25 M☉ → plateau {plateau(al):+.2f}")
    a2.set_xscale("log"); a2.set_xlim(8, 100); a2.set_ylim(0, None)
    a2.set_xticks([8, 10, 13, 20, 30, 40, 60, 100]); a2.set_xticklabels(["8", "10", "13", "20", "30", "40", "60", "100"])
    a2.set_xlabel("mass of the exploding star [M☉]"); a2.set_ylabel("how many SNe\n(per log mass)")
    a2.legend(loc="upper right", fontsize=14.5)
    fig.savefig(os.path.join(OUT, "p2_topheavy_plateau.png"), dpi=110, bbox_inches="tight", facecolor=BG); plt.close(fig)


def fig_first():
    use_slide_style()
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(figsize=(10.8, 7.2))
    # clouds of pristine gas polluted by a few SNe drawn from the IMF (8-100 Msun, alpha 2.3)
    u = rng.random(200000); a = 2.3
    masses = (8 ** (1 - a) + u * (100 ** (1 - a) - 8 ** (1 - a))) ** (1 / (1 - a)); k = 0
    for n, col in [(1, "#a9a9c8"), (3, ORANGE), (30, FG)]:
        xs, ys = [], []
        for _ in range(250):
            mm = masses[k:k + n]; k += n
            mdil = 10 ** rng.uniform(4.5, 6.0)                   # Msun of pristine gas mixed with the ejecta
            xs.append(np.log10(fe(mm).sum() / mdil / 1.30e-3)); ys.append(np.log10(mg(mm).sum() / fe(mm).sum() / SUN))
        ax.scatter(xs, ys, s={1: 10, 3: 16, 30: 26}[n], color=col, alpha={1: 0.5, 3: 0.6, 30: 0.9}[n], lw=0, zorder={1: 1, 3: 2, 30: 3}[n],
                   label={1: "cloud polluted by 1 SN", 3: "by 3 SNe", 30: "by 30 SNe"}[n])
    for name, col, p in [("Milky-Way-like", BLUE, dict(tau_sf=2.0, infall_tau=7.0, eta=1.0)),
                         ("slow dwarf", GREEN, dict(tau_sf=15.0, infall_tau=3.0, eta=10.0))]:
        r = run_one_zone(**p); ok = np.isfinite(r["FeH"]) & (r["t"] > 0.003)
        ax.plot(r["FeH"][ok], r["MgFe"][ok], color=col, lw=4, label=f"toy model: {name}", zorder=5)
        for tt, lab in [(0.01, "10 Myr"), (0.1, "100 Myr"), (1, "1 Gyr"), (10, "10 Gyr")]:
            i = np.argmin(abs(r["t"] - tt)); ax.plot(r["FeH"][i], r["MgFe"][i], "o", color=col, ms=11, mec=BG, mew=2, zorder=6)
            ax.text(r["FeH"][i], r["MgFe"][i] + (0.09 if col == BLUE else -0.13), lab, color=col, fontsize=13, ha="center", zorder=7, fontweight="bold")
    ax.axhline(0, color=GREY, lw=1, ls=":")
    ax.annotate("", (-4.9, 0.47), (-5.6, 0.47), arrowprops=dict(arrowstyle="-|>", color=PINK, lw=2.5))
    ax.text(-5.55, 0.98, "first 3 Myr: no supernova yet\ngas = Big Bang H + He\n[Fe/H] = −∞, [Mg/Fe] undefined",
            color=PINK, fontsize=14, va="top")
    ax.set_xlim(-5.6, 0.6); ax.set_ylim(-0.35, 1.05)
    ax.set_xlabel("[Fe/H]   (time and metals →)"); ax.set_ylabel("[Mg/Fe]")
    leg = ax.legend(loc="lower left", fontsize=13, ncol=2, markerscale=2.5)
    ax.text(-1.0, 0.95, "few SNe: [Mg/Fe] depends on which\nstars happened to explode (IMF sampling)", color=ORANGE, fontsize=13, ha="center", va="top")
    fig.savefig(os.path.join(OUT, "p1_first_enrichment.png"), dpi=110, bbox_inches="tight", facecolor=BG); plt.close(fig)


if __name__ == "__main__":
    for al in (2.7, 2.3, 1.9): print("plateau alpha", al, round(plateau(al), 2))
    fig_topheavy(); fig_first(); print("saved")
