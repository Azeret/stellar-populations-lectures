"""Animation 1: building a star cluster by drawing stars from the IMF.

Left: the 'cluster' (dot size ~ mass, colour = mass). Right: the histogram
dN/dlog m filling up, compared with the Kroupa IMF expectation.
Run:  python a1_imf_sampling.py   ->  out/a1_imf_sampling.mp4
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from stellarpops import sample_imf, kroupa_xi
from stellarpops.style import use_slide_style, BLUE, ORANGE, FG, GREY

OUT = os.path.join(os.path.dirname(__file__), "out"); os.makedirs(OUT, exist_ok=True)
use_slide_style()
rng = np.random.default_rng(42)
NMAX = 100_000
m = sample_imf(NMAX, rng=rng)
# positions: Plummer-like sphere projected
r = 1.0 / np.sqrt(rng.random(NMAX) ** (-2 / 3) - 1)
r = np.where(r > 4.6, rng.random(NMAX) * 4.6, r)  # keep everyone inside the frame
phi = rng.random(NMAX) * 2 * np.pi
x, y = r * np.cos(phi), r * np.sin(phi)

bins = np.logspace(np.log10(0.08), np.log10(150), 25)
centers = np.sqrt(bins[1:] * bins[:-1]); dlogm = np.diff(np.log10(bins))
mm = np.geomspace(0.08, 150, 400)
xi = kroupa_xi(mm)
# expected dN/dlogm per star = m*xi(m)*ln10 / int(xi)
norm = np.trapezoid(xi, mm)
expect_per_star = mm * xi * np.log(10) / norm

fig = plt.figure(figsize=(19.2, 10.8))
axc = fig.add_axes([0.05, 0.02, 0.40, 0.72]); axc.set_aspect("equal"); axc.axis("off")
axh = fig.add_axes([0.55, 0.14, 0.42, 0.68])
title = fig.text(0.5, 0.93, "", ha="center", fontsize=34, weight="bold", color=FG)
info = fig.text(0.05, 0.86, "", fontsize=22, color=FG, va="top", linespacing=1.4)

nframes, hold = 270, 75
Ns = np.unique(np.round(np.logspace(1, np.log10(NMAX), nframes)).astype(int))
frames = list(Ns) + [Ns[-1]] * hold
cmap = plt.get_cmap("RdYlBu")


def draw(N):
    axc.cla(); axc.axis("off"); axc.set_xlim(-5, 5); axc.set_ylim(-5, 5)
    mi = m[:N]
    order = np.argsort(mi)
    shrink = min(1.0, (300 / N) ** 0.35)
    sizes = (6 + 40 * mi[order] ** 0.6) * shrink
    alpha = 0.9 if N < 3000 else max(0.35, 0.9 * (3000 / N) ** 0.3)
    axc.scatter(x[:N][order], y[:N][order], s=sizes, c=np.log10(mi[order]), cmap=cmap,
                vmin=-1, vmax=1.7, alpha=alpha, linewidths=0)
    axh.cla()
    h, _ = np.histogram(mi, bins)
    dens = h / dlogm
    ok = h > 0
    axh.bar(centers[ok], dens[ok], width=np.diff(bins)[ok] * 0.9, color=BLUE, alpha=0.85,
            label="stars drawn")
    axh.plot(mm, N * expect_per_star, color=ORANGE, lw=3, label="Kroupa IMF (expected)")
    axh.set_xscale("log"); axh.set_yscale("log")
    axh.set_xlim(0.07, 200); axh.set_ylim(0.5, 3e5)
    axh.set_xlabel(r"stellar mass  $m$  [M$_\odot$]")
    axh.set_ylabel(r"$dN / d\log m$")
    axh.legend(loc="lower left")
    axh.axvline(8, color=GREY, ls=":", lw=2)
    axh.text(9.5, 3e4, "SN II\nprogenitors", color=GREY, fontsize=16)
    title.set_text("Drawing stars from the IMF")
    info.set_text(f"N = {N:,} stars     M = {mi.sum():,.0f} M$_\\odot$\n"
                  f"most massive: {mi.max():.1f} M$_\\odot$     stars > 8 M$_\\odot$: {(mi > 8).sum():,}")


if os.environ.get("PREVIEW"):          # PREVIEW=1 python ... -> only still frames
    for N in (30, 3000, NMAX):
        draw(N); fig.savefig(os.path.join(OUT, f"a1_preview_{N}.png"))
    sys.exit()
anim = FuncAnimation(fig, lambda i: draw(frames[i]), frames=len(frames))
anim.save(os.path.join(OUT, "a1_imf_sampling.mp4"),
          writer=FFMpegWriter(fps=30, codec="libx264", extra_args=["-preset", "veryfast", "-pix_fmt", "yuv420p", "-crf", "20"]))
draw(frames[-1]); fig.savefig(os.path.join(OUT, "a1_imf_sampling_final.png"))
print("done")
