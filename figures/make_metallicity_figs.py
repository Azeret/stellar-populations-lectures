"""Two slide figures on metallicity, from FaSTAR's BaSTI-IAC isochrones and SSP models.

1. fig_z_stars.png       — the same star with fewer metals: hotter and brighter, but
                           differently for low- and high-mass stars.
2. fig_z_degeneracy.png  — older or more metal-rich? Two look-alike SSPs and how
                           Hbeta vs Mg b separates them.
Run: python make_metallicity_figs.py   (needs `pip install fastar-astro`, ~1 min)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import fastar
from fastar import IntegratedSSPSynthesizer, imf
from stellarpops.style import use_slide_style, BLUE, ORANGE, FG, GREY, GREEN

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_metallicity"); os.makedirs(OUT, exist_ok=True)
use_slide_style()
POOR, RICH = BLUE, ORANGE

# ----------------------------------------------------------------- isochrones
iso = h5py.File(os.path.join(os.path.dirname(fastar.__file__), "assets", "BASTI-IAC_isochrones.hdf5"))
AGES, METS = np.array(iso["ages"], float), np.array(iso["mets"], float)        # Myr, [Fe/H]
M, T, L = (np.array(iso[k]) for k in ("mass_ini", "teff_out", "lumi_out"))     # Msun, log Teff, log L
I_POOR, I_RICH = int(np.argmin(abs(METS + 1.7))), int(np.argmin(abs(METS - 0.06)))


def iso_at(age_myr, im):
    ia = int(np.argmin(abs(AGES - age_myr)))
    return M[:, ia, im], T[:, ia, im], L[:, ia, im]


def star(mass, age_myr, im):
    """log Teff, log L of a star of initial mass `mass` on the isochrone (main-sequence part)."""
    m, t, l = iso_at(age_myr, im)
    k = np.searchsorted(m, mass) + 2
    return np.interp(mass, m[:k], t[:k]), np.interp(mass, m[:k], l[:k])


def mid_ms_age(mass):
    """An age (Myr) at which a star of this mass sits in the middle of its main sequence."""
    return float(np.clip(0.25e4 * mass ** -2.5, 20, 4000))


def lifetime(mass, im):
    """Total lifetime [Gyr]: the age at which `mass` is the most massive star still alive."""
    mmax = M[:, :, im].max(axis=0)
    return np.interp(-np.asarray(mass), -mmax, AGES) / 1e3


def turnoff_mass(age_myr, im):
    m, t, _ = iso_at(age_myr, im)
    sel = m < 1.5
    return m[sel][np.argmax(t[sel])]


# ============================================================ figure 1: stars
masses = np.array([0.3, 0.5, 0.7, 1.0, 1.3, 2.0, 3.0, 5.0, 8.0])
poor = np.array([star(m, mid_ms_age(m), I_POOR) for m in masses])
rich = np.array([star(m, mid_ms_age(m), I_RICH) for m in masses])
dlogL = poor[:, 1] - rich[:, 1]
dT = 10 ** (poor[:, 0] - rich[:, 0])

fig = plt.figure(figsize=(19.2, 10.8))
ax = fig.add_axes([0.06, 0.10, 0.50, 0.82])
for im, col, lab in ((I_POOR, POOR, "[Fe/H] = −1.7"), (I_RICH, RICH, "[Fe/H] = +0.06 (≈ solar)")):
    m, t, l = iso_at(10000, im)
    ok = l < 2.6
    ax.plot(t[ok], l[ok], color=col, lw=2, alpha=0.45, ls="--")
    top = np.argmax(np.where(ok & (m > 0.5), l, -9))
    ax.text(t[top], 2.72, "10 Gyr\ngiants", color=col, fontsize=14, ha="center", va="bottom", alpha=0.9)
for (tp, lp), (tr, lr), m in zip(poor, rich, masses):
    ax.add_patch(FancyArrowPatch((tr, lr), (tp, lp), arrowstyle="-|>", mutation_scale=22, lw=2, color=GREY))
    ax.plot(tr, lr, "o", color=RICH, ms=15, zorder=5)
    ax.plot(tp, lp, "o", color=POOR, ms=15, zorder=5)
    ax.text(tr + 0.012, lr - 0.06, f"{m:g} M$_\\odot$", fontsize=16, color=FG, ha="right", va="top")
ax.plot([], [], "o", color=RICH, ms=12, label="metal-rich, [Fe/H] = +0.06")
ax.plot([], [], "o", color=POOR, ms=12, label="metal-poor, [Fe/H] = −1.7")
ax.plot([], [], "--", color=GREY, lw=2, label="10 Gyr isochrones (turnoff + giants)")
ax.set_xlim(4.5, 3.48); ax.set_ylim(-2.45, 4.1)
ax.set_xlabel(r"log $T_\mathrm{eff}$ [K]   (hot ← → cool)")
ax.set_ylabel(r"log $L$ [L$_\odot$]")
ax.legend(loc="upper right", fontsize=15)
ax.text(4.47, -2.3, "each pair: same initial mass, middle of its main sequence", fontsize=14, color=GREY)

axl = fig.add_axes([0.66, 0.58, 0.31, 0.32])
axl.bar(range(len(masses)), 10 ** dlogL, color=POOR, alpha=0.9)
axl.axhline(1, color=GREY, lw=1)
axl.set_xticks(range(len(masses)), [f"{m:g}" for m in masses], fontsize=15)
axl.set_ylabel("× brighter", fontsize=18)
axl.set_title("metal-poor twin: luminosity", fontsize=19)
axl.set_ylim(0, 3.4)
axt = fig.add_axes([0.66, 0.12, 0.31, 0.32])
lm = masses[masses >= 1.0]
ratio = lifetime(lm, I_POOR) / lifetime(lm, I_RICH)
k0 = len(masses) - len(lm)
axt.bar(range(k0, len(masses)), ratio, color=POOR, alpha=0.9)
axt.axhline(1, color=GREY, lw=1)
axt.text(1, 0.5, "< 1 M$_\\odot$:\nboth outlive\nthe Universe", ha="center", va="center", fontsize=14, color=GREY)
axt.set_xticks(range(len(masses)), [f"{m:g}" for m in masses], fontsize=15)
axt.set_xlim(-0.6, len(masses) - 0.4)
axt.set_ylabel("× the lifetime", fontsize=18)
axt.set_xlabel(r"initial mass [M$_\odot$]", fontsize=18)
axt.set_title("metal-poor twin: lifetime", fontsize=19)
axt.set_ylim(0, 1.15)
fig.savefig(os.path.join(OUT, "fig_z_stars.png"))
plt.close(fig)

tom_poor, tom_rich = turnoff_mass(10000, I_POOR), turnoff_mass(10000, I_RICH)
print("figure 1: luminosity ratio", dict(zip(masses, np.round(10 ** dlogL, 2))))
print("          % hotter       ", dict(zip(masses, np.round(100 * (dT - 1)))))
print(f"          10 Gyr turnoff mass: {tom_poor:.2f} (poor) vs {tom_rich:.2f} (rich) Msun")

# ======================================================= figure 2: degeneracy
ssp = IntegratedSSPSynthesizer(imf_function=imf.kroupa)
w = np.array(ssp.wave)


def spec(age, met):
    s = np.array(ssp.synthesize(age=age, met=met))
    return s / np.median(s[(w > 5450) & (w < 5550)])


def index(s, band, blue, red):
    """Lick-style equivalent width [A] with a straight pseudo-continuum."""
    def mean(a, b):
        sel = (w > a) & (w < b)
        return w[sel].mean(), s[sel].mean()
    (wb, fb), (wr, fr) = mean(*blue), mean(*red)
    sel = (w > band[0]) & (w < band[1])
    cont = fb + (fr - fb) * (w[sel] - wb) / (wr - wb)
    return np.trapezoid(1 - s[sel] / cont, w[sel])


HB = ((4847.875, 4876.625), (4827.875, 4847.875), (4876.625, 4891.625))
MGB = ((5160.125, 5192.625), (5142.625, 5161.375), (5191.375, 5206.375))


def smooth(s, n=101):
    return np.convolve(s, np.ones(n) / n, "same")


# the young metal-rich population, and the 3x older population whose continuum matches best
A_YOUNG, Z_YOUNG, A_OLD = 4.0, 0.0, 12.0
ref = spec(A_YOUNG, Z_YOUNG)
ztry = np.arange(-0.9, 0.01, 0.025)
rms = [np.sqrt(np.mean((smooth(spec(A_OLD, z)) - smooth(ref))[100:-100] ** 2)) for z in ztry]
Z_OLD = float(ztry[int(np.argmin(rms))])
old = spec(A_OLD, Z_OLD)
print(f"figure 2: {A_OLD:g} Gyr needs [M/H] = {Z_OLD:+.3f} to mimic {A_YOUNG:g} Gyr solar")

fig = plt.figure(figsize=(19.2, 10.8))
ax = fig.add_axes([0.06, 0.40, 0.60, 0.52])
ax.plot(w, ref, color=RICH, lw=1.6, label=f"{A_YOUNG:g} Gyr, solar metallicity")
ax.plot(w, old, color=POOR, lw=1.6, alpha=0.85, label=f"{A_OLD:g} Gyr (3× older), [M/H] = {Z_OLD:+.2f}")
ax.set_xlim(w.min(), w.max()); ax.set_ylim(0.2, 1.35)
ax.set_xlabel("wavelength [Å]"); ax.set_ylabel("flux (normalised at 5500 Å)")
ax.legend(loc="lower right", fontsize=16)
for x, lab in ((4861, "Hβ"), (5175, "Mg b")):
    ax.axvline(x, color=GREY, ls=":", lw=1.2); ax.text(x, 1.30, lab, color=FG, ha="center", fontsize=16)
ax.text(5320, 1.22, "same colour, same continuum shape", fontsize=20, color=FG)

for k, (lo, hi, lab) in enumerate(((4820, 4900, "Hβ: age"), (5140, 5210, "Mg b: metals"))):
    axz = fig.add_axes([0.06 + 0.32 * k, 0.08, 0.27, 0.22])
    sel = (w > lo) & (w < hi)
    axz.plot(w[sel], ref[sel], color=RICH, lw=2.5)
    axz.plot(w[sel], old[sel], color=POOR, lw=2.5)
    axz.set_title(lab, fontsize=18); axz.tick_params(labelsize=13)

# index-index grid
ga = [2, 3, 4, 6, 9, 13]; gz = [-1.0, -0.5, 0.0, 0.25]
grid = np.array([[(index(spec(a, z), *MGB), index(spec(a, z), *HB)) for z in gz] for a in ga])
axg = fig.add_axes([0.73, 0.12, 0.25, 0.78])
for j, z in enumerate(gz):
    axg.plot(grid[:, j, 0], grid[:, j, 1], color=GREY, lw=1.5)
    axg.text(grid[-1, j, 0] + 0.05, grid[-1, j, 1] - 0.07, "0" if z == 0 else f"{z:+g}",
             color=GREY, fontsize=14, ha="left", va="top")
axg.text(grid[-1, -1, 0] + 0.05, grid[-1, -1, 1] - 0.22, "[M/H]", color=GREY, fontsize=14, ha="left", va="top")
for i, a in enumerate(ga):
    axg.plot(grid[i, :, 0], grid[i, :, 1], color=GREY, lw=1.5, ls="--")
    axg.text(grid[i, 0, 0] - 0.08, grid[i, 0, 1], f"{a} Gyr", color=GREY, fontsize=14, ha="right", va="center")
axg.plot(index(ref, *MGB), index(ref, *HB), "o", color=RICH, ms=18, zorder=5)
axg.plot(index(old, *MGB), index(old, *HB), "o", color=POOR, ms=18, zorder=5)
axg.set_xlabel("Mg b [Å]  → more metals"); axg.set_ylabel("Hβ [Å]  → younger")
axg.set_title("break the degeneracy", fontsize=20)
x0, x1 = grid[..., 0].min(), grid[..., 0].max()
axg.set_xlim(x0 - 0.9, x1 + 0.8)
axg.set_ylim(grid[..., 1].min() - 0.45, grid[..., 1].max() + 0.15)
fig.savefig(os.path.join(OUT, "fig_z_degeneracy.png"))
plt.close(fig)
print("saved to", OUT)
