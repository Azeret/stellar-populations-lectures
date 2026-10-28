"""Animation 8: galevo (GalIMF) chemical evolution, same stellar mass formed
over 30 Myr / 300 Myr / 3 Gyr, Kroupa IMF (solid) vs IGIMF (dashed).
Reads ../data/galevo_runs/*.npz (made with run_galevo.py).
Run: python a8_galevo.py  ->  out/a8_galevo_tracks.mp4
"""
import os, sys, glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from stellarpops.style import use_slide_style, BLUE, ORANGE, GREEN, FG, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); DATA = os.path.join(HERE, "..", "data", "galevo_runs")
use_slide_style()
WRITER = dict(fps=30, codec="libx264", extra_args=["-preset", "veryfast", "-pix_fmt", "yuv420p", "-crf", "20"])
STYLE = {"K_fast": (ORANGE, "-", "30 Myr, Kroupa"), "K_mid": (BLUE, "-", "300 Myr, Kroupa"),
         "K_slow": (GREEN, "-", "3 Gyr, Kroupa"), "I_fast": (ORANGE, "--", "30 Myr, IGIMF"), "I_mid": (BLUE, "--", "300 Myr, IGIMF"),
         "I_slow": (GREEN, "--", "3 Gyr, IGIMF")}
runs = {k: np.load(f) for k in STYLE for f in glob.glob(os.path.join(DATA, k + ".npz"))}
print("runs:", list(runs))


def track(d):
    t = 10 ** d["time_axis"] / 1e9                     # Gyr
    fe, mg = d["Fe_over_H_list"], d["Mg_over_Fe_list"]
    ok = fe > -4.5
    return t[ok], fe[ok], mg[ok]


fig = plt.figure(figsize=(19.2, 10.8))
ax = fig.add_axes([0.07, 0.13, 0.55, 0.72]); axs = fig.add_axes([0.70, 0.45, 0.27, 0.38])
fig.text(0.5, 0.93, "galevo: same stellar mass, different tempo", ha="center", fontsize=32, weight="bold", color=FG)
clock = fig.text(0.07, 0.87, "", fontsize=26, color=FG)
note = fig.text(0.07, 0.008, "lines: gas abundances; solid Kroupa IMF, dashed IGIMF (variable galaxy-wide IMF); "
                "3×10⁹ M$_\\odot$ formed with a flat SFH", fontsize=16, color=GREY)
axb = fig.add_axes([0.70, 0.13, 0.27, 0.2])
times = np.concatenate([np.geomspace(0.003, 10, 300), np.full(75, 10)])


def draw(tn):
    ax.cla()
    for k, d in runs.items():
        col, ls, lab = STYLE[k]
        t, fe, mg = track(d)
        sel = t <= tn
        ax.plot(fe[sel], mg[sel], ls, color=col, lw=3.5, label=lab)
        if sel.any():
            ax.plot(fe[sel][-1], mg[sel][-1], "o", color=col, ms=12)
    ax.set_xlim(-4, 0.5); ax.set_ylim(-0.6, 0.7)
    ax.axhline(0, color=GREY, lw=1, ls=":"); ax.axvline(0, color=GREY, lw=1, ls=":")
    ax.set_xlabel("gas [Fe/H]"); ax.set_ylabel("gas [Mg/Fe]"); ax.legend(loc="lower left", fontsize=16)
    axs.cla()
    for k, dur in (("K_fast", 0.03), ("K_mid", 0.3), ("K_slow", 3.0)):
        col = STYLE[k][0]
        tt = np.geomspace(0.001, 10, 400); sfr = np.where(tt < dur, 3.0 / dur, 0)
        axs.plot(tt[tt <= tn], sfr[tt <= tn], color=col, lw=3)
    axs.set_xscale("log"); axs.set_yscale("log"); axs.set_xlim(0.001, 10); axs.set_ylim(0.5, 200)
    axs.set_xlabel("time [Gyr]"); axs.set_ylabel("SFR [M$_\\odot$/yr]")
    axb.cla()
    keys = [k for k in STYLE if k in runs]
    vals = [runs[k]["stellar_Mg_over_Fe_list"][-1] if tn >= 3 else np.nan for k in keys]
    axb.bar(range(len(keys)), np.nan_to_num(vals), color=[STYLE[k][0] for k in keys],
            hatch=None, alpha=0.9, edgecolor=FG, linewidth=[2 if STYLE[k][1] == "--" else 0 for k in keys])
    axb.set_xticks(range(len(keys)), [STYLE[k][2].replace(", ", "\n") for k in keys], fontsize=12)
    axb.set_ylim(-0.25, 0.55); axb.set_ylabel("stars' [Mg/Fe]", fontsize=16); axb.axhline(0, color=GREY, lw=1)
    clock.set_text(f"t = {tn*1000:,.0f} Myr" if tn < 1 else f"t = {tn:.1f} Gyr")


if os.environ.get("PREVIEW"):
    draw(10); fig.savefig(os.path.join(OUT, "a8_preview.png")); sys.exit()
FuncAnimation(fig, lambda k: draw(times[k]), frames=len(times)).save(
    os.path.join(OUT, "a8_galevo_tracks.mp4"), writer=FFMpegWriter(**WRITER))
draw(10); fig.savefig(os.path.join(OUT, "a8_galevo_tracks_final.png"))
print("done")
