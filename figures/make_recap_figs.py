"""Figures for the Lecture 1 recap at the start of Lecture 2 (one figure per recap question).
Run: python make_recap_figs.py  ->  slides_recap/*.png
Uses stellarpops (IMF integrals, remnants) and the FaSTAR grid in animations/out/fastar_grid.npz
(made by animations/precompute_fastar.py). r5 needs FaSTAR itself (3 extra spectra).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib.pyplot as plt
from stellarpops import number_fraction, mass_fraction, kroupa_xi, sample_imf
from stellarpops.remnants import turnoff_mass, remnant_mass
from stellarpops.style import use_slide_style, BG, FG, BLUE, ORANGE, PINK, GREEN, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_recap"); os.makedirs(OUT, exist_ok=True)
GRID = os.path.join(HERE, "..", "animations", "out", "fastar_grid.npz")
use_slide_style(scale=1.2)
SIZE = (11, 7.4)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=110)
    plt.close(fig); print("saved", name)


# R1 ---------------------------------------------------- number vs mass at birth
def r1():
    bins = [("below 1 M☉", 0.08, 1), ("1–8 M☉", 1, 8), ("above 8 M☉", 8, 150)]
    num = [100 * number_fraction(a, b) for _, a, b in bins]
    mas = [100 * mass_fraction(a, b) for _, a, b in bins]
    fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
    y = np.arange(3)[::-1]
    ax.barh(y + 0.2, num, 0.38, color=BLUE, label="share of the NUMBER of stars")
    ax.barh(y - 0.2, mas, 0.38, color=ORANGE, label="share of the MASS")
    for yy, n, m in zip(y, num, mas):
        ax.text(n + 1.5, yy + 0.2, f"{n:.1f}%" if n < 1 else f"{n:.0f}%", va="center", color=BLUE, fontsize=22)
        ax.text(m + 1.5, yy - 0.2, f"{m:.0f}%", va="center", color=ORANGE, fontsize=22)
    ax.set_yticks(y); ax.set_yticklabels([b[0] for b in bins], fontsize=22)
    ax.set_xlim(0, 112); ax.set_xlabel("% of all newborn stars (Kroupa IMF, 0.08–150 M☉)")
    ax.legend(loc="lower right", fontsize=17)
    save(fig, "r1_number_mass")


# R2 ---------------------------------------------------- where the mass is after 10 Gyr
def r2():
    m = np.geomspace(0.08, 150, 20000); w = kroupa_xi(m); M = np.trapezoid(w * m, m)
    mto = float(turnoff_mass(10.0))
    def part(sel, val): return 100 * np.trapezoid(np.where(sel, val, 0) * w, m) / M
    alive_lo = part(m <= 0.5, m); alive_hi = part((m > 0.5) & (m <= mto), m)
    wd = part((m > mto) & (m < 8), remnant_mass(m)); ns_bh = part(m >= 8, remnant_mass(m))
    gas = 100 - alive_lo - alive_hi - wd - ns_bh
    parts = [("living stars\n< 0.5 M☉", alive_lo, BLUE), (f"living stars\n0.5–{mto:.1f} M☉", alive_hi, GREEN),
             ("white dwarfs", wd, GREY), ("neutron stars\n+ black holes", ns_bh, PINK), ("returned to gas\n(winds, SNe)", gas, ORANGE)]
    fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
    for i, (lab, v, c) in enumerate(parts):
        ax.bar(i, v, color=c, width=0.7)
        ax.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=24)
    ax.set_xticks(range(5)); ax.set_xticklabels([p[0] for p in parts], fontsize=15)
    ax.set_ylabel("M☉ out of every 100 M☉ formed"); ax.set_ylim(0, max(p[1] for p in parts) * 1.2)
    ax.set_title("10 Gyr after a burst (Kroupa IMF)", fontsize=20, color=GREY)
    print("R2:", {p[0].split()[0] + p[0].split()[-1]: round(p[1], 1) for p in parts})
    save(fig, "r2_mass_10gyr")


# R3 ---------------------------------------------------- M/L U-shape
def r3():
    G = np.load(GRID); al, ml = G["alphas"], G["ml_alpha"]
    fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
    ax.plot(al, ml, color=FG, lw=4)
    for a, c, lab in ((1.3, PINK, "top-heavy\nα = 1.3"), (2.35, BLUE, "Salpeter\nα = 2.35"), (3.0, ORANGE, "bottom-heavy\nα = 3")):
        v = np.interp(a, al, ml); ax.plot(a, v, "o", ms=20, color=c)
        ax.text(a, v + 1.6, f"{lab}\nM/L = {v:.0f}", ha="center", color=c, fontsize=18)
    ax.text(1.45, 3.0, "extra mass in dark\nremnants (WD, NS, BH)", color=PINK, fontsize=17)
    ax.text(3.25, 3.0, "extra mass in\nfaint red dwarfs", color=ORANGE, fontsize=17, ha="right")
    ax.set_xlabel("IMF slope α over 0.1–100 M☉  (dN/dm ∝ m^−α)"); ax.set_ylabel("M/L in the V band at 10 Gyr  [M☉/L☉]")
    ax.set_ylim(0, ml.max() * 1.15)
    ax.set_title("FaSTAR, solar metallicity, stars + remnants", fontsize=18, color=GREY)
    save(fig, "r3_ml_imf")


# R4 ---------------------------------------------------- fading
def r4():
    G = np.load(GRID); a = G["ages"]; L = 1 / G["mlb_age"]
    L = L / np.interp(0.1, a, L)
    fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
    ax.loglog(a, L, color=FG, lw=4)
    l10 = np.interp(10, a, L)
    ax.plot([0.1, 10], [1, l10], "o", ms=18, color=ORANGE)
    ax.annotate("", (10, l10), (10, 1), arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=3))
    ax.axhline(1, color=GREY, lw=1, ls=":")
    ax.text(7.5, np.sqrt(l10), f"{1 / l10:.0f}× fainter", color=ORANGE, fontsize=24, ha="right", va="center")
    ax.text(0.12, 0.45, "100 Myr: light from\n3–5 M☉ stars\n(L ∝ m³·⁵: very bright)", color=BLUE, fontsize=17, va="top")
    ax.text(6.0, l10 * 1.6, "10 Gyr: those are dead;\nlight from ~1 M☉ giants", color=PINK, fontsize=17, va="bottom", ha="right")
    ax.set_xlabel("age [Gyr]"); ax.set_ylabel("V-band light per M☉ formed\n(relative to 100 Myr)")
    ax.set_title("FaSTAR, Kroupa IMF, solar metallicity", fontsize=18, color=GREY)
    print("R4: fading factor", round(1 / l10, 1))
    save(fig, "r4_fading")


# R5 ---------------------------------------------------- colour degeneracy
def r5():
    G = np.load(GRID); w = G["wave"]
    S = np.load(os.path.join(HERE, "..", "data", "recap_colour_spectra_all.npz"))
    def norm(f): return f / np.median(f[(w > 5400) & (w < 5600)])
    def colour(f): return -2.5 * np.log10(np.mean(f[(w > 4350) & (w < 4650)]) / np.mean(f[(w > 5900) & (w < 6200)]))
    base = norm(S["base"])
    # Calzetti-like attenuation k(λ) for 0.12-0.63 micron (Calzetti et al. 2000), R_V = 4.05
    x = w / 1e4; k = 2.659 * (-2.156 + 1.509 / x - 0.198 / x ** 2 + 0.011 / x ** 3) + 4.05
    target = colour(norm(S["age3"])) - colour(base)
    av = np.interp(target, [colour(base * 10 ** (-0.4 * a * k / 4.05)) - colour(base) for a in np.linspace(0, 1, 101)], np.linspace(0, 1, 101))
    dusty = norm(base * 10 ** (-0.4 * av * k / 4.05))
    sp = [("your model: 2 Gyr, [M/H] = −0.4", base, GREY), ("1.5× older (3 Gyr)", norm(S["age3"]), ORANGE),
          ("4× more metals ([M/H] = +0.2)", norm(S["met0.2"]), BLUE), (f"a little dust (A_V = {av:.2f} mag)", dusty, PINK)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 7.4), gridspec_kw=dict(width_ratios=[1.6, 1]), constrained_layout=True)
    sm = lambda f: np.convolve(f, np.ones(25) / 25, mode="same")
    for lab, f, c in sp:
        a1.plot(w[15:-15], sm(f)[15:-15], color=c, lw=2.5, label=f"{lab}:  redder by {colour(f) - colour(base):.2f} mag" if f is not base else lab)
    a1.set_xlabel("wavelength [Å]"); a1.set_ylabel("flux (normalised at 5500 Å, smoothed)")
    a1.axvspan(4350, 4650, color=BLUE, alpha=0.12); a1.axvspan(5900, 6200, color=ORANGE, alpha=0.12)
    a1.legend(fontsize=13, loc="lower right"); a1.set_title("the continuum (colour): all three look alike", fontsize=17, color=GREY)
    from stellarpops.spectra import lick_index
    names = ["model", "older", "metals", "dust"]
    hb = [lick_index(w, f, "Hbeta") for _, f, _ in sp]; mg = [lick_index(w, f, "Mgb") for _, f, _ in sp]
    x = np.arange(4); cols = [c for _, _, c in sp]
    a2.bar(x - 0.2, hb, 0.38, color=cols, edgecolor=FG, lw=1.5, hatch="//")
    a2.bar(x + 0.2, mg, 0.38, color=cols, edgecolor=FG, lw=1.5)
    a2.set_xticks(x); a2.set_xticklabels(names, fontsize=15)
    a2.set_ylabel("line strength (equivalent width) [Å]")
    a2.text(0.02, 0.97, "hatched: Hβ   plain: Mg b\nolder: Hβ drops most\nmore metals: Mg b rises most\ndust: changes neither", transform=a2.transAxes, fontsize=13, va="top")
    a2.set_ylim(0, max(max(hb), max(mg)) * 1.45)
    a2.set_title("the lines tell them apart", fontsize=17, color=GREY)
    print("R5 Hb", np.round(hb, 2), "Mgb", np.round(mg, 2))
    print("R5: colour shifts", [round(colour(f) - colour(base), 3) for _, f, _ in sp], "A_V", round(av, 2))
    save(fig, "r5_colour")


# R6 ---------------------------------------------------- stochastic sampling
def r6():
    rng = np.random.default_rng(3)
    counts = []
    for _ in range(3000):
        m = sample_imf(300, rng=rng)
        counts.append(np.sum((m > 0.9) & (m < 1.0)))
    counts = np.array(counts)
    fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
    k = np.arange(0, counts.max() + 1)
    ax.bar(k, [100 * np.mean(counts == i) for i in k], color=GREEN, width=0.75)
    ax.set_xlabel("number of stars with 0.9–1.0 M☉ in a 300-star cluster\n(at 10 Gyr these are the giants that make ~half the light)")
    ax.set_ylabel("% of clusters"); ax.set_xticks(k)
    ax.set_title(f"3000 random clusters of 300 stars: mean {counts.mean():.1f}, but often 0–2 or 7+", fontsize=17, color=GREY)
    print("R6: mean", counts.mean(), "P(<=2)", np.mean(counts <= 2), "P(>=7)", np.mean(counts >= 7))
    save(fig, "r6_stochastic")


# R7 ---------------------------------------------------- H-alpha SFR
def r7():
    m = np.geomspace(0.08, 150, 20000)
    vals = []
    for ah in (2.3, 1.9):
        w = kroupa_xi(m, alpha_high=ah); M = np.trapezoid(w * m, m)
        vals.append(1000 * np.trapezoid(w[m > 15], m[m > 15]) / M)
    fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
    b = ax.bar(["Kroupa\n(α = 2.3 above 1 M☉)", "top-heavy\n(α = 1.9 above 1 M☉)"], vals, color=[BLUE, PINK], width=0.55)
    for bb, v in zip(b, vals):
        ax.text(bb.get_x() + bb.get_width() / 2, v + 0.2, f"{v:.1f}", ha="center", fontsize=26)
    ax.set_ylabel("stars above 15 M☉ per 1000 M☉ formed\n(they make the ionising photons → Hα)")
    ax.set_ylim(0, max(vals) * 1.25)
    ax.set_title(f"top-heavy: {vals[1] / vals[0]:.1f}× more Hα per M☉ formed", fontsize=19, color=GREY)
    print("R7:", [round(v, 2) for v in vals], "ratio", round(vals[1] / vals[0], 2))
    save(fig, "r7_halpha")


if __name__ == "__main__":
    r1(); r2(); r3(); r4(); r5(); r6(); r7()
