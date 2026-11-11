"""[Mg/Fe] of the stars vs duration of star formation, from the Galaxy clock game (docs/index.html).
Grid made by running the game's own JS model (data/galaxy_clock_grid.json). -> slides_elements/g_clock_duration.png"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, matplotlib.pyplot as plt
from stellarpops.style import use_slide_style, BLUE, ORANGE, PINK, GREEN, FG, GREY
HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "..", "data", "galaxy_clock_grid.json")))
use_slide_style()
fig, ax = plt.subplots(figsize=(10.8, 7.2))
ax.plot(g["d"], g["k"], color=BLUE, lw=4, label="Kroupa IMF")
ax.plot(g["d"], g["t"], color=PINK, lw=3, ls="--", label="top-heavy IMF")
ax.set_xscale("log"); ax.set_xlim(0.05, 10); ax.set_ylim(0.1, 0.62)
ax.axhline(0.30, color=GREEN, lw=1.5, ls=":"); ax.text(0.055, 0.31, "round 2 target +0.30", color=GREEN, fontsize=17)
ax.plot(0.05, g["k"][0], "o", color=ORANGE, ms=14); ax.text(0.062, g["k"][0] + 0.015, "round 1 winner +0.46", color=ORANGE, fontsize=17)
d = np.array(g["d"]); k = np.array(g["k"]); x30 = np.interp(0.30, k[::-1], d[::-1])
ax.plot(x30, 0.30, "o", color=GREEN, ms=12); ax.annotate(f"≈ {x30:.1f} Gyr", (x30, 0.30), (x30 * 1.4, 0.36), color=GREEN, fontsize=17, arrowprops=dict(arrowstyle="->", color=GREEN))
t = np.array(g["t"]); ax.annotate("top-heavy + 10 Gyr\n= Kroupa + 1 Gyr", (10, t[-1]), (2.2, 0.47), color=PINK, fontsize=15, ha="center", arrowprops=dict(arrowstyle="->", color=PINK))
ax.set_xlabel("how long the galaxy formed stars [Gyr]"); ax.set_ylabel("[Mg/Fe] of all its stars")
ax.set_xticks([0.05, 0.1, 0.3, 1, 3, 10]); ax.set_xticklabels(["0.05", "0.1", "0.3", "1", "3", "10"])
ax.legend(loc="lower left", fontsize=16)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "slides_elements", "g_clock_duration.png"), dpi=110); print("x30", x30)
