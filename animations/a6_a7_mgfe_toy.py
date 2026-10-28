"""Animations 6 and 7 with the toy one-zone model (stellarpops.toy_gce).

A6: [Mg/Fe] vs [Fe/H] tracks drawn as time runs, for an elliptical (fast,
    quenched), a Milky-Way-like disc and a slow dwarf, with the SN II / SN Ia
    rates of the Milky-Way model underneath.
A7: the Milky-Way model while the high-mass IMF slope slides from 1.9 to 2.7.
Run: python a6_a7_mgfe_toy.py  ->  out/a6_mgfe_clock.mp4, out/a7_mgfe_imf.mp4
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from stellarpops import run_one_zone
from stellarpops.style import use_slide_style, BLUE, ORANGE, GREEN, PINK, FG, GREY

OUT = os.path.join(os.path.dirname(__file__), "out"); os.makedirs(OUT, exist_ok=True)
use_slide_style()
WRITER = dict(fps=30, codec="libx264", extra_args=["-preset", "veryfast", "-pix_fmt", "yuv420p", "-crf", "20"])

GALAXIES = [  # label, colour, model parameters
    ("Elliptical: fast, then quenched", ORANGE, dict(tau_sf=0.3, t_stop=0.5, eta=0.5)),
    ("Milky-Way-like disc", BLUE, dict(tau_sf=2.0, infall_tau=7.0, eta=1.0)),
    ("Dwarf: slow, leaky", GREEN, dict(tau_sf=15.0, infall_tau=3.0, eta=10.0)),
]
runs = [run_one_zone(**p) for _, _, p in GALAXIES]
t = runs[0]["t"]


def setup_track_axes(ax):
    ax.set_xlim(-3.2, 0.6); ax.set_ylim(-0.35, 0.65)
    ax.set_xlabel("[Fe/H]   (more iron →)"); ax.set_ylabel("[Mg/Fe]")
    ax.axhline(0, color=GREY, lw=1, ls=":"); ax.axvline(0, color=GREY, lw=1, ls=":")
    ax.text(0.03, 0.03, "Sun", color=GREY, fontsize=15)


# ---------------------------------------------------------------- A6
def make_a6(preview=False):
    fig = plt.figure(figsize=(19.2, 10.8))
    ax = fig.add_axes([0.07, 0.11, 0.52, 0.74])
    axs = fig.add_axes([0.67, 0.53, 0.30, 0.30])
    axr = fig.add_axes([0.67, 0.11, 0.30, 0.30])
    fig.text(0.5, 0.93, "[Mg/Fe] is a clock: SN II first, SN Ia later", ha="center",
             fontsize=32, weight="bold", color=FG)
    clock = fig.text(0.07, 0.87, "", fontsize=26, color=FG)
    times = np.concatenate([np.geomspace(0.01, 13.0, 330), np.full(80, 13.0)])
    mw = runs[1]
    rmax = max(mw["rate_ii"].max(), 1e-12)

    def draw(tnow):
        i = min(np.searchsorted(t, tnow), len(t) - 1)
        ax.cla(); setup_track_axes(ax)
        for (lab, col, _), r in zip(GALAXIES, runs):
            act = r["sfr"][: i + 1] > 0
            fe, mg = r["FeH"][: i + 1][act], r["MgFe"][: i + 1][act]
            ok = np.isfinite(fe) & (fe > -3.2)
            ax.plot(fe[ok], mg[ok], color=col, lw=3.5, label=lab)
            if ok.any():
                ax.plot(fe[ok][-1], mg[ok][-1], "o", color=col, ms=14)
                if not act[-1]:
                    ax.text(fe[ok][-1] - 0.05, mg[ok][-1] - 0.07, "star formation stopped", color=col, fontsize=15, ha="right")
        ax.legend(loc="lower left")
        # SFR panel
        axs.cla()
        for (lab, col, _), r in zip(GALAXIES, runs):
            axs.plot(t[: i + 1], r["sfr"][: i + 1] / r["sfr"].max(), color=col)
        axs.set_xscale("log"); axs.set_xlim(0.01, 13); axs.set_ylim(0, 1.1)
        axs.set_ylabel("star formation\n(scaled)"); axs.set_xticklabels([])
        # SN rates panel (MW model)
        axr.cla()
        axr.plot(t[: i + 1], mw["rate_ii"][: i + 1] / rmax, color=PINK, label="SN II (Mg + some Fe)")
        axr.plot(t[: i + 1], mw["rate_ia"][: i + 1] / rmax * 5, color=FG, label="SN Ia ×5 (mostly Fe)")
        axr.set_xscale("log"); axr.set_xlim(0.01, 13); axr.set_ylim(0, 1.15)
        axr.set_xlabel("time [Gyr]"); axr.set_ylabel("SN rate, MW\n(scaled)")
        axr.legend(loc="upper left", fontsize=14)
        clock.set_text(f"t = {tnow*1000:,.0f} Myr" if tnow < 1 else f"t = {tnow:.1f} Gyr")

    if preview:
        for tn in (0.03, 0.3, 13.0):
            draw(tn); fig.savefig(os.path.join(OUT, f"a6_preview_{tn}.png"))
        return
    FuncAnimation(fig, lambda k: draw(times[k]), frames=len(times)).save(
        os.path.join(OUT, "a6_mgfe_clock.mp4"), writer=FFMpegWriter(**WRITER))
    draw(13.0); fig.savefig(os.path.join(OUT, "a6_mgfe_clock_final.png"))


# ---------------------------------------------------------------- A7
def make_a7(preview=False):
    alphas = np.linspace(1.9, 2.7, 41)
    seq = np.concatenate([np.full(20, 2.3), np.linspace(2.3, 1.9, 60), np.full(20, 1.9),
                          np.linspace(1.9, 2.7, 120), np.full(20, 2.7), np.linspace(2.7, 2.3, 60), np.full(40, 2.3)])
    p = GALAXIES[1][2]
    tracks = {round(a, 3): run_one_zone(alpha_high=a, **p) for a in alphas}
    ref = tracks[2.3]
    fig = plt.figure(figsize=(19.2, 10.8))
    ax = fig.add_axes([0.07, 0.11, 0.55, 0.74])
    axi = fig.add_axes([0.70, 0.40, 0.27, 0.40])
    fig.text(0.5, 0.93, "A different IMF moves the [Mg/Fe] plateau", ha="center", fontsize=32, weight="bold", color=FG)
    lab = fig.text(0.70, 0.30, "", fontsize=26, color=FG)
    note = fig.text(0.70, 0.16, "", fontsize=20, color=GREY)
    mm = np.geomspace(1, 100, 200)

    def draw(a):
        a = alphas[np.argmin(abs(alphas - a))]
        r = tracks[round(a, 3)]
        ax.cla(); setup_track_axes(ax); ax.set_xlim(-3.2, 0.5)
        ax.plot(ref["FeH"], ref["MgFe"], color=GREY, lw=2, ls="--", label="Kroupa (α = 2.3)")
        ax.plot(r["FeH"], r["MgFe"], color=BLUE, lw=4, label=f"α = {a:.2f}")
        ax.legend(loc="lower left")
        axi.cla()
        axi.loglog(mm, mm ** -2.3, color=GREY, ls="--"); axi.loglog(mm, mm ** -a, color=BLUE, lw=3)
        axi.set_xlabel("m [M$_\\odot$]"); axi.set_ylabel("ξ(m), m > 1 M$_\\odot$")
        axi.axvspan(8, 100, color=PINK, alpha=0.15); axi.text(9, 3e-1, "SN II", color=PINK, fontsize=16)
        lab.set_text(f"high-mass slope α = {a:.2f}")
        note.set_text("top-heavy" if a < 2.2 else ("top-light" if a > 2.4 else "canonical"))

    if preview:
        for a in (1.9, 2.3, 2.7):
            draw(a); fig.savefig(os.path.join(OUT, f"a7_preview_{a}.png"))
        return
    FuncAnimation(fig, lambda k: draw(seq[k]), frames=len(seq)).save(
        os.path.join(OUT, "a7_mgfe_imf.mp4"), writer=FFMpegWriter(**WRITER))
    draw(1.9); fig.savefig(os.path.join(OUT, "a7_mgfe_imf_final.png"))


if __name__ == "__main__":
    pv = bool(os.environ.get("PREVIEW"))
    make_a6(pv); make_a7(pv)
    print("done")
