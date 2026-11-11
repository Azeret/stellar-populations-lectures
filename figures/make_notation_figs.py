"""Figures for the notation section and the 'which elements tell time' slide of Lecture 2.
Run: python make_notation_figs.py  ->  slides_elements/n*.png, ex*.png, t_clock.png
Solar abundances: Asplund et al. (2009, ARA&A 47, 481).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from stellarpops import run_one_zone
from stellarpops.origins import SOURCES
from stellarpops.style import use_slide_style, BG, FG, BLUE, ORANGE, PINK, GREEN, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_elements"); os.makedirs(OUT, exist_ok=True)
use_slide_style(scale=1.25)
plt.rcParams["font.family"] = "DejaVu Sans"
VIOLET = "#b39dff"
# log eps (Asplund+09) and atomic masses
A09 = {"H": (12.00, 1.008), "He": (10.93, 4.003), "C": (8.43, 12.011), "N": (7.83, 14.007), "O": (8.69, 15.999),
       "Ne": (7.93, 20.18), "Na": (6.24, 22.99), "Mg": (7.60, 24.305), "Al": (6.45, 26.98), "Si": (7.51, 28.085),
       "S": (7.12, 32.06), "Ar": (6.40, 39.95), "Ca": (6.34, 40.08), "Cr": (5.64, 52.0), "Fe": (7.50, 55.845),
       "Ni": (6.22, 58.69), "Ba": (2.18, 137.3), "Eu": (0.52, 152.0)}


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=110); plt.close(fig); print("saved", name)


# N1 ---------------------------------------------------------- the Sun by mass
def n1():
    m = {k: 10 ** (e - 12) * a for k, (e, a) in A09.items()}
    tot = sum(m.values()); X, Y = m["H"] / tot, m["He"] / tot; Z = 1 - X - Y
    met = {k: v / tot / Z for k, v in m.items() if k not in ("H", "He")}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 7.2), gridspec_kw=dict(width_ratios=[1, 1.5], wspace=0.35))
    fig.subplots_adjust(left=0.05, right=0.98, top=0.88, bottom=0.14)
    # left: X, Y, Z stacked bar
    y0 = 0
    for lab, v, c in (("X  hydrogen", X, BLUE), ("Y  helium", Y, GREEN), ("Z  'metals'", Z, ORANGE)):
        a1.bar(0, v, bottom=y0, color=c, width=0.6)
        if v > 0.05:
            a1.text(0.4, y0 + v * (0.3 if "helium" in lab else 0.5), f"{lab}\n{v:.3f}", va="center", fontsize=19, color=c)
        else:
            a1.annotate(f"{lab} {v:.4f}", (0.3, y0 + v / 2), (0.45, 0.94), fontsize=17, color=c,
                        arrowprops=dict(arrowstyle="->", color=c, lw=2))
        y0 += v
    a1.set_xlim(-0.4, 1.6); a1.set_ylim(0, 1.0); a1.set_xticks([]); a1.set_ylabel("mass fraction")
    a1.set_title("the Sun by mass", fontsize=20, color=GREY, pad=18)
    a1.spines["bottom"].set_visible(False)
    # right: what Z is made of
    keys = ["O", "C", "Fe", "Ne", "Si", "Mg", "N", "S", "rest"]
    vals = [met[k] for k in keys[:-1]]; vals.append(1 - sum(vals))
    cols = [BLUE if k in ("O", "Ne", "Mg", "Si", "S") else ORANGE if k == "Fe" else GREEN if k in ("C", "N") else GREY for k in keys]
    a2.barh(np.arange(len(keys))[::-1], np.array(vals) * 100, color=cols)
    for i, (k, v) in enumerate(zip(keys, vals)):
        a2.text(v * 100 + 0.8, len(keys) - 1 - i, f"{100 * v:.0f}%", va="center", fontsize=18)
    a2.set_yticks(np.arange(len(keys))[::-1]); a2.set_yticklabels(keys, fontsize=20)
    a2.set_xlabel("% of the metal mass Z"); a2.set_xlim(0, 52)
    a2.set_title("what the 1.3% of 'metals' is made of", fontsize=20, color=GREY)
    print("N1: X Y Z", round(X, 4), round(Y, 4), round(Z, 4), {k: round(100 * v) for k, v in zip(keys, vals)})
    save(fig, "n1_sun_composition")


# N2 ---------------------------------------------------------- log eps ladder
def n2():
    fig, ax = plt.subplots(figsize=(14, 7.6)); fig.subplots_adjust(left=0.1, right=0.97, top=0.95, bottom=0.08)
    show = [("H", 12.00, BLUE), ("He", 10.93, GREEN), ("O", 8.69, BLUE), ("C", 8.43, GREEN), ("Mg", 7.60, BLUE),
            ("Fe", 7.50, ORANGE), ("Ba", 2.18, GREEN), ("Eu", 0.52, PINK)]
    ax.set_ylim(-0.5, 12.8); ax.set_xlim(0, 10); ax.set_xticks([])
    ax.set_ylabel("log ε(X) = log₁₀(N_X / N_H) + 12")
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    xpos = {"H": 0.6, "He": 0.6, "O": 0.6, "C": 5.4, "Mg": 0.6, "Fe": 5.4, "Ba": 0.6, "Eu": 0.6}
    def per(n):
        if n < 1e6:
            return f"1 per {n:,.0f} H"
        ex = int(np.floor(np.log10(n))); return f"1 per {n / 10 ** ex:.0f} × 10^{ex} H"
    for k, e, c in show:
        x = xpos[k]
        if x < 2:
            ax.plot([0, x - 0.1], [e, e], color=c, lw=1.5, ls=":")
        ax.text(x, e, f"{k}  {e:.2f}", va="center", fontsize=20, color=c, fontweight="bold")
        ax.text(x + 1.9, e, "the reference" if k == "H" else per(10 ** (12 - e)), va="center", fontsize=16, color=GREY)
    ax.text(9.9, 5.6, "1 step down = 10× fewer atoms", ha="right", fontsize=17, color=FG)
    ax.annotate("", (9.5, 4.0), (9.5, 5.0), arrowprops=dict(arrowstyle="->", color=FG, lw=2))
    print("N2 done")
    save(fig, "n2_logeps_ladder")


# EX1 -------------------------------------------------------- the star on the plateau
def ex1():
    r = run_one_zone(tau_sf=2.0, infall_tau=7.0, eta=1.0)
    ok = np.isfinite(r["FeH"]) & (r["FeH"] > -3.4)
    fig, ax = plt.subplots(figsize=(11, 7.2)); fig.subplots_adjust(left=0.13, right=0.97, top=0.95, bottom=0.13)
    ax.plot(r["FeH"][ok], r["MgFe"][ok], color=BLUE, lw=4, label="toy Milky-Way model (notebook 03)")
    ax.plot(-1.5, 0.4, "*", ms=34, color=ORANGE, mec=FG, label="our star: [Fe/H] = −1.5, [Mg/Fe] = +0.4")
    ax.axhline(0, color=GREY, lw=1, ls=":"); ax.axvline(0, color=GREY, lw=1, ls=":")
    ax.text(-3.3, 0.5, "plateau: massive-star SNe only", fontsize=17, color=GREY)
    ax.text(-0.95, -0.15, "white dwarfs add iron\n→ [Mg/Fe] falls", fontsize=17, color=GREY)
    ax.set_xlim(-3.4, 0.5); ax.set_ylim(-0.3, 0.7)
    ax.set_xlabel("[Fe/H]"); ax.set_ylabel("[Mg/Fe]"); ax.legend(loc="lower left", fontsize=15)
    save(fig, "ex1_star_on_plateau")


# EX2 -------------------------------------------------------- alpha enhancement and Z
def ex2():
    zsun, fa = 0.0134, 0.638
    cases = [("solar mix\n[Fe/H] = −1", 0.0), ("α-enhanced\n[Fe/H] = −1, [α/Fe] = +0.4", 0.4)]
    fig, ax = plt.subplots(figsize=(11, 7.2)); fig.subplots_adjust(left=0.14, right=0.97, top=0.93, bottom=0.17)
    for i, (lab, ae) in enumerate(cases):
        a = zsun * 0.1 * fa * 10 ** ae; rest = zsun * 0.1 * (1 - fa)
        ax.bar(i, rest * 1e3, color=ORANGE, width=0.55, label="Fe-peak, C, N, … (unchanged)" if i == 0 else None)
        ax.bar(i, a * 1e3, bottom=rest * 1e3, color=BLUE, width=0.55, label="α elements: O, Ne, Mg, Si, S, Ca" if i == 0 else None)
        z = a + rest
        ax.text(i, z * 1e3 + 0.08, f"Z = {z:.4f}\n[M/H] = {np.log10(z / zsun):+.2f}", ha="center", fontsize=19)
    ax.set_xticks([0, 1]); ax.set_xticklabels([c[0] for c in cases], fontsize=17)
    ax.set_ylabel("metal mass fraction Z  [×10⁻³]"); ax.set_ylim(0, 3.6); ax.legend(loc="upper left", fontsize=15)
    save(fig, "ex2_alpha_Z")


# EX3 -------------------------------------------------------- averaging logs
def ex3():
    fig, ax = plt.subplots(figsize=(11, 7.2)); fig.subplots_adjust(left=0.08, right=0.97, top=0.9, bottom=0.2)
    pts = [(0, "cloud A\n(solar)", BLUE, 0.75), (-2, "cloud B", GREEN, 0.75), (-1, "WRONG:\naverage of\nthe logs", PINK, 0.3),
           (np.log10(0.505), "RIGHT:\nlog of the\naverage", ORANGE, 0.3)]
    ax.set_xlim(-2.6, 0.6); ax.set_ylim(0, 1); ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    for x, lab, c, y in pts:
        ax.plot([x, x], [0, y - 0.12], color=c, lw=3); ax.plot(x, 0.02, "o", ms=18, color=c, clip_on=False)
        ax.text(x, y, lab + f"\n{x:+.2f}", ha="center", va="bottom", fontsize=17, color=c)
    ax.set_xlabel("[Fe/H]")
    sec = ax.secondary_xaxis("top", functions=(lambda v: 10 ** v, lambda v: np.log10(np.clip(v, 1e-9, None))))
    sec.set_xticks([0.01, 0.1, 0.505, 1]); sec.set_xticklabels(["0.01", "0.1", "0.505", "1"]); sec.set_xlabel("iron per H relative to the Sun (linear)")
    save(fig, "ex3_averaging")


# T ----------------------------------------------------------- when each factory switches on
def t_clock():
    fig, ax = plt.subplots(figsize=(17, 7.6)); fig.subplots_adjust(left=0.24, right=0.97, top=0.9, bottom=0.14)
    rows = [("ccsn", "O, Mg, Si, Ca (α)", 3e-3, 4e-2), ("r", "Eu, Au, Pt (r-process)", 1e-2, 3.0),
            ("agb", "C, N, Sr, Ba, Pb (s-process)", 1e-1, 13.0), ("ia", "Fe, Mn, Ni (iron peak)", 4e-2, 13.0)]
    for i, (k, lab, a, b) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.barh(y, b - a, left=a, height=0.55, color=SOURCES[k][1])
        ax.text(2e-3 / 1.15, y, lab, ha="right", va="center", fontsize=19, color=SOURCES[k][1])
        ax.text(a * 1.15, y + 0.42, SOURCES[k][0], fontsize=15, color=GREY)
    ax.set_xscale("log"); ax.set_xlim(2e-3, 14); ax.set_ylim(-0.6, len(rows) - 0.2); ax.set_yticks([])
    ax.set_xticks([3e-3, 1e-2, 4e-2, 3e-1, 1, 10]); ax.set_xticklabels(["3 Myr", "10 Myr", "40 Myr", "300 Myr", "1 Gyr", "10 Gyr"])
    ax.set_xlabel("time after the stars are born")
    ax.axvline(4e-2, color=FG, lw=1.5, ls="--"); ax.text(4.3e-2, len(rows) - 0.35, "first white dwarfs explode", fontsize=15)
    ax.set_title("prompt / delayed:  [Mg/Fe], [Y/Mg], [Eu/Fe], [N/O] are all clocks", fontsize=19, color=GREY)
    save(fig, "t_clock")


if __name__ == "__main__":
    n1(); n2(); ex1(); ex2(); ex3(); t_clock()
