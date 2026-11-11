"""Figures for the Lecture 2 Slido answer slides (toy model + galevo runs).
Run: python make_l2_answer_figs.py  ->  slides_l2_answers/*.png
The same calculations are in notebooks/03_toy_chemical_evolution.ipynb (section "Slido answers").
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib.pyplot as plt
from stellarpops import run_one_zone
from stellarpops.style import use_slide_style, BLUE, ORANGE, GREEN, PINK, FG, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_l2_answers"); os.makedirs(OUT, exist_ok=True)
DATA = os.path.join(HERE, "..", "data", "galevo_runs")
use_slide_style(scale=1.15)
SIZE = (11.5, 7.2)


def knee(r, drop=0.05):
    """[Fe/H] where the gas [Mg/Fe] first falls `drop` dex below its plateau."""
    ok = np.isfinite(r["MgFe"]) & np.isfinite(r["FeH"]) & (r["sfr"] > 0)
    plateau = np.nanmax(r["MgFe"][ok])
    i = np.argmax(ok & (r["MgFe"] < plateau - drop) & (r["t"] > 0.04))
    return r["FeH"][i], r["MgFe"][i], plateau


def tracks(ax, runs):
    for lab, col, r in runs:
        ok = np.isfinite(r["FeH"]) & (r["sfr"] > 0) & (r["FeH"] > -3.4)
        ax.plot(r["FeH"][ok], r["MgFe"][ok], color=col, lw=4, label=lab)
    ax.set_xlim(-3.4, 0.5); ax.set_ylim(-0.3, 0.7)
    ax.set_xlabel("[Fe/H]"); ax.set_ylabel("[Mg/Fe]")
    ax.axhline(0, color=GREY, lw=1, ls=":"); ax.axvline(0, color=GREY, lw=1, ls=":")


# ---------------------------------------------------- knee: slow dwarf vs fast
GAL = [("elliptical: fast", ORANGE, dict(tau_sf=0.3, t_stop=0.5, eta=0.5)),
       ("Milky-Way disc", BLUE, dict(tau_sf=2.0, infall_tau=7.0, eta=1.0)),
       ("dwarf: slow, leaky", GREEN, dict(tau_sf=15.0, infall_tau=3.0, eta=10.0))]
runs = [(lab, col, run_one_zone(**p)) for lab, col, p in GAL]
fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
tracks(ax, runs)
for lab, col, r in runs:
    fk, mk, _ = knee(r)
    ax.plot(fk, mk, "o", ms=18, mfc="none", mec=col, mew=3)
    ax.annotate(f"knee\n[Fe/H] ≈ {fk:.1f}", (fk, mk), (fk - 0.05, mk - 0.33), color=col, fontsize=17,
                ha="center", arrowprops=dict(arrowstyle="-", color=col, lw=1.5))
    print(lab, "knee at [Fe/H] =", round(float(fk), 2))
ax.legend(loc="upper right")
fig.savefig(os.path.join(OUT, "ans_knee.png")); plt.close(fig)

# ---------------------------------------------------- plateau vs IMF
fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
for al, col, lab in ((1.9, PINK, "top-heavy, α = 1.9"), (2.3, BLUE, "Kroupa, α = 2.3"), (2.7, GREY, "top-light, α = 2.7")):
    r = run_one_zone(alpha_high=al, tau_sf=2.0, infall_tau=7.0, eta=1.0)
    ok = np.isfinite(r["FeH"]) & (r["FeH"] > -3.4)
    ax.plot(r["FeH"][ok], r["MgFe"][ok], color=col, lw=4, label=lab)
    pl = np.nanmax(r["MgFe"][r["t"] > 0.005])
    ax.text(-3.3, pl + 0.025, f"plateau +{pl:.2f}", color=col, fontsize=17)
    print("alpha", al, "plateau", round(float(pl), 2))
ax.set_xlim(-3.4, 0.5); ax.set_ylim(-0.3, 0.75)
ax.set_xlabel("[Fe/H]"); ax.set_ylabel("[Mg/Fe]")
ax.axhline(0, color=GREY, lw=1, ls=":"); ax.axvline(0, color=GREY, lw=1, ls=":")
ax.legend(loc="lower left")
fig.savefig(os.path.join(OUT, "ans_imf_plateau.png")); plt.close(fig)

# ---------------------------------------------------- galevo: tempo ranking
fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
labs, vals, cols = [], [], []
for k, lab, col in (("K_fast", "30 Myr", ORANGE), ("K_mid", "300 Myr", BLUE), ("K_slow", "3 Gyr", GREEN)):
    d = np.load(os.path.join(DATA, k + ".npz"))
    labs.append(lab); vals.append(float(d["stellar_Mg_over_Fe_list"][-1])); cols.append(col)
bars = ax.bar(labs, vals, color=cols, width=0.6)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + (0.02 if v >= 0 else -0.06), f"{v:+.2f}", ha="center", fontsize=22, color=FG)
ax.axhline(0, color=GREY, lw=1)
ax.set_ylabel("[Mg/Fe] of the stars"); ax.set_xlabel("same stellar mass formed in …")
ax.set_ylim(-0.3, 0.6)
print("galevo stars [Mg/Fe]:", dict(zip(labs, np.round(vals, 2))))
fig.savefig(os.path.join(OUT, "ans_tempo_galevo.png")); plt.close(fig)

# ---------------------------------------------------- ellipticals: duration
dts = np.geomspace(0.1, 13, 25)
mgfe = [run_one_zone(tau_sf=dt, t_stop=dt, eta=0.5)["star_MgFe"][-1] for dt in dts]
fig, ax = plt.subplots(figsize=SIZE, constrained_layout=True)
ax.plot(dts, mgfe, color=BLUE, lw=4, label="toy model (this course)")
ax.plot(dts, 0.2 - np.log10(dts) / 6, color=ORANGE, lw=3, ls="--", label="Thomas et al. 2005 (data)")
ax.axhline(0.3, color=PINK, lw=2, ls=":")
ax.text(9, 0.315, "massive ellipticals", color=PINK, fontsize=17, ha="right")
ax.set_xscale("log"); ax.set_xlabel("duration of star formation Δt [Gyr]"); ax.set_ylabel("[Mg/Fe] of the stars")
ax.set_ylim(-0.05, 0.6); ax.legend(loc="lower left")
print("toy: dt where stars [Mg/Fe]=0.3:", round(float(np.interp(-0.3, -np.array(mgfe), dts)), 2), "Gyr;",
      "Thomas05:", round(10 ** (6 * (0.2 - 0.3)), 2), "Gyr")
fig.savefig(os.path.join(OUT, "ans_duration.png")); plt.close(fig)
print("saved", OUT)
