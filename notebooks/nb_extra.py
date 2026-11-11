"""Extra notebooks (05-07) and the Slido-answers section of notebook 03.
Imported by build_notebooks.py. Raw strings: LaTeX backslashes are single."""

SETUP = r"""
import sys, os
sys.path.insert(0, os.path.abspath('..'))   # makes the small 'stellarpops' package importable
import numpy as np
import matplotlib.pyplot as plt
from stellarpops.style import use_slide_style
use_slide_style(dark=False, scale=0.7)       # dark=True gives the lecture-slide look
"""

# ============================================================== 03: Slido answers
NB03_SLIDO = [
("md", r"""
## 6. The Slido questions of Lecture 2, worked out

Each cell reproduces one answer from the lecture with the toy model (or the galevo runs of notebook 04). The answer slides in the lecture show the same numbers.
"""),
("md", r"""
### S2.3 — A star has 1/10 of the solar Fe/H. What is its [Fe/H]?
$[\mathrm{Fe/H}] = \log_{10}(N_\mathrm{Fe}/N_\mathrm{H})_\star - \log_{10}(N_\mathrm{Fe}/N_\mathrm{H})_\odot$: logarithmic **and** relative to the Sun.
"""),
("code", r"""
for ratio in (0.01, 0.1, 0.5, 1, 2):
    print(f'{ratio:>5} x the solar Fe/H  ->  [Fe/H] = {np.log10(ratio):+.2f}')
"""),
("md", r"""
### S2.5 and S2.8 — Where is the knee of a slowly star-forming dwarf?
We define the knee as the point where the gas [Mg/Fe] first drops 0.05 dex below the SN II plateau.
"""),
("code", r"""
def knee(r, drop=0.05):
    ok = np.isfinite(r['MgFe']) & np.isfinite(r['FeH']) & (r['sfr'] > 0)
    plateau = np.nanmax(r['MgFe'][ok])
    i = np.argmax(ok & (r['MgFe'] < plateau - drop) & (r['t'] > 0.04))
    return r['FeH'][i], r['t'][i]

galaxies = {'elliptical (fast)':   dict(tau_sf=0.3, t_stop=0.5, eta=0.5),
            'Milky-Way disc':      dict(tau_sf=2.0, infall_tau=7.0, eta=1.0),
            'dwarf (slow, leaky)': dict(tau_sf=15.0, infall_tau=3.0, eta=10.0)}
for name, p in galaxies.items():
    feh, t = knee(run_one_zone(**p))
    print(f'{name:22s} knee at [Fe/H] = {feh:+.2f}, reached after {t * 1000:.0f} Myr')
"""),
("md", r"""
The knee comes at a similar **time** in every galaxy (when SN Ia start to matter, ~0.1–1 Gyr), but at a very different **[Fe/H]**: a slow dwarf has made little iron by then.
So **S2.5: the knee sits at lower [Fe/H]**, and **S2.8: a knee at [Fe/H] ≈ −2 belongs to a dwarf spheroidal**.
"""),
("md", r"""
### S2.6 — Make the IMF top-heavy. What happens to the plateau?
"""),
("code", r"""
for alpha in (1.9, 2.3, 2.7):
    r = run_one_zone(alpha_high=alpha, tau_sf=2.0, infall_tau=7.0, eta=1.0)
    print(f'IMF slope above 1 Msun = {alpha}:  plateau [Mg/Fe] = {np.nanmax(r["MgFe"][r["t"] > 0.005]):+.2f}')
"""),
("md", r"""
**It goes up.** The plateau is pure SN II enrichment, and massive SN II make more Mg per Fe. That is the degeneracy: high [Mg/Fe] = fast star formation *or* a top-heavy IMF.
"""),
("md", r"""
### S2.7 — Rank by the [Mg/Fe] of their stars: the same mass formed in 30 Myr, 300 Myr, 3 Gyr
(galevo runs, Kroupa IMF; see notebook 04)
"""),
("code", r"""
for key, label in (('K_fast', '30 Myr'), ('K_mid', '300 Myr'), ('K_slow', '3 Gyr')):
    d = np.load(f'../data/galevo_runs/{key}.npz')
    print(f'{label:8s} [Mg/Fe] of the stars = {d["stellar_Mg_over_Fe_list"][-1]:+.2f}')
"""),
("md", r"""
### S2.9 — Massive ellipticals have [Mg/Fe] ≈ +0.3. How long did they form stars?
We let the toy galaxy form stars for a time $\Delta t$ and then stop (quench), and compare with the relation Thomas et al. (2005) derived from data, $[\alpha/\mathrm{Fe}] \approx 1/5 - 1/6\,\log(\Delta t/\mathrm{Gyr})$.
"""),
("code", r"""
dts = np.geomspace(0.1, 13, 20)
mgfe = np.array([run_one_zone(tau_sf=dt, t_stop=dt, eta=0.5)['star_MgFe'][-1] for dt in dts])
plt.semilogx(dts, mgfe, label='toy model')
plt.semilogx(dts, 0.2 - np.log10(dts) / 6, '--', label='Thomas et al. 2005')
plt.axhline(0.3, color='grey', ls=':')
plt.xlabel(r'duration of star formation $\Delta t$ [Gyr]'); plt.ylabel('[Mg/Fe] of the stars'); plt.legend()
print('toy model: [Mg/Fe] = +0.3 after', round(float(np.interp(-0.3, -mgfe, dts)), 2), 'Gyr;',
      'Thomas et al.:', round(10 ** (6 * (0.2 - 0.3)), 2), 'Gyr')
"""),
("md", r"""
**About 1 Gyr or less.** The exact number depends on the yields and the SN Ia delay-time distribution — and on the IMF: a top-heavy IMF raises the plateau and allows a longer $\Delta t$.
"""),
]

# ============================================================== 05
NB05 = [
("md", r"""
# 05 — Spectral resolution, velocity dispersion and convolution

*Lecture 1: stellar populations — how real spectra are made*

A model spectrum is not what a telescope sees. The observed spectrum is

$$F_\mathrm{obs}(\lambda) = \Big[F_\mathrm{model} \ast \mathrm{LOSVD} \ast \mathrm{LSF}\Big] \ \text{sampled on pixels} \ + \ \text{noise}$$

* **LOSVD** — the line-of-sight velocity distribution of the stars (velocity dispersion $\sigma$ of the galaxy),
* **LSF** — the line-spread function of the spectrograph (its resolution, FWHM in Å or $R = \lambda/\Delta\lambda$),
* $\ast$ means **convolution**.

In this notebook you will convolve spectra by hand and see what resolution and velocity dispersion do to absorption lines — and to the line strengths we use to measure ages and metallicities.

FaSTAR spectra come at the resolution of the MILES library: **FWHM = 2.51 Å**, sampled at 0.9 Å per pixel, 3540–7400 Å.
"""),
("code", SETUP + r"""
from fastar import IntegratedSSPSynthesizer, imf
from stellarpops.spectra import (gaussian_kernel, convolve, degrade_resolution, log_rebin,
                                 broaden_velocity, lick_index, add_noise, normalise,
                                 C_KMS, FWHM_FASTAR, SIG2FWHM)

ssp = IntegratedSSPSynthesizer(imf_function=imf.kroupa)
wave = np.array(ssp.wave)
spec = normalise(wave, np.array(ssp.synthesize(age=10.0, met=0.0)))   # 10 Gyr, solar, Kroupa
print(f'{wave.min():.0f}-{wave.max():.0f} A, {np.median(np.diff(wave)):.2f} A per pixel, R = lambda/FWHM = {5000 / FWHM_FASTAR:.0f} at 5000 A')
"""),
("md", r"""
## 1. Convolution by hand

Convolution replaces every pixel by a weighted average of its neighbours; the weights are the **kernel** (here a Gaussian). It spreads each line out but keeps the total flux.
"""),
("code", r"""
sigma_pix = 5.0                       # kernel width in pixels
k = gaussian_kernel(sigma_pix)
print('kernel has', k.size, 'pixels and sums to', k.sum())

# a fake spectrum: flat continuum with two narrow absorption lines
x = np.arange(400)
toy = 1 - 0.8 * np.exp(-0.5 * ((x - 150) / 1.5) ** 2) - 0.8 * np.exp(-0.5 * ((x - 170) / 1.5) ** 2)
smooth = np.convolve(toy, k, mode='same')

plt.plot(x, toy, label='before'); plt.plot(x, smooth, label=f'convolved, sigma = {sigma_pix} px')
plt.xlim(100, 220); plt.legend(); plt.xlabel('pixel')
print('equivalent width before / after:', round(np.sum(1 - toy), 2), round(np.sum(1 - smooth[20:-20]), 2))
"""),
("md", r"""
**Question.** The two lines merge into one. How wide (in pixels) must the kernel be for two lines 20 px apart to blend? What stays the same (look at the equivalent width)?
"""),
("md", r"""
## 2. Instrumental resolution

Gaussians add **in quadrature**: to take a spectrum from FWHM$_\mathrm{in}$ to FWHM$_\mathrm{out}$, convolve with a Gaussian of
$\mathrm{FWHM}_\mathrm{kernel} = \sqrt{\mathrm{FWHM}_\mathrm{out}^2 - \mathrm{FWHM}_\mathrm{in}^2}$.
"""),
("code", r"""
fig, axs = plt.subplots(1, 2, figsize=(14, 4.5))
for fwhm in [FWHM_FASTAR, 5, 10, 25]:
    s = degrade_resolution(wave, spec, FWHM_FASTAR, fwhm)
    for ax, (lo, hi) in zip(axs, [(4800, 4920), (5130, 5350)]):
        sel = (wave > lo) & (wave < hi)
        ax.plot(wave[sel], s[sel], label=f'FWHM = {fwhm:g} A (R ~ {5000 / fwhm:.0f})')
axs[0].set_title(r'H$\beta$ (age-sensitive)'); axs[1].set_title('Mg b and Fe lines (metals)')
for ax in axs: ax.set_xlabel(r'wavelength [$\AA$]')
axs[1].legend(fontsize=9)
"""),
("md", r"""
For reference: MUSE ~2.5 Å, SDSS ~2.8 Å (R ≈ 2000), a low-resolution prism (e.g. JWST/NIRSpec PRISM) R ~ 100, i.e. FWHM of tens of Å in the optical rest frame.
"""),
("md", r"""
## 3. Velocity dispersion: why we rebin in ln(λ)

A Doppler shift moves a line by $\Delta\lambda = \lambda\,v/c$: the same velocity spreads a red line more (in Å) than a blue one. If we resample the spectrum onto a grid uniform in $\ln\lambda$, every pixel has the same width in **km/s**,
$\Delta v = c\,\Delta\ln\lambda$ (`velscale`), and the LOSVD becomes one fixed kernel.
"""),
("code", r"""
ln_lam, spec_log, velscale = log_rebin(wave, spec)
lam = np.exp(ln_lam)
print(f'velscale = {velscale:.1f} km/s per pixel')

fig, ax = plt.subplots(figsize=(10, 4.5))
sel = (lam > 5130) & (lam < 5350)
for sigma in [0, 100, 200, 300]:
    ax.plot(lam[sel], broaden_velocity(spec_log, velscale, sigma)[sel], label=f'sigma = {sigma} km/s')
ax.legend(); ax.set_xlabel(r'wavelength [$\AA$]')
print('sigma = 200 km/s at 5175 A corresponds to FWHM =', round(SIG2FWHM * 200 / C_KMS * 5175, 1), 'A')
"""),
("md", r"""
**Question.** A giant elliptical has $\sigma \approx 300$ km/s, a dwarf galaxy 20 km/s. Which one limits the resolution you need: the galaxy or the spectrograph?
"""),
("md", r"""
## 4. Line strengths depend on σ

Lick indices measure the equivalent width in a fixed window. If the line is broadened, part of it leaks out of the window: the index **drops** although the stars are the same. Index–σ corrections are needed before comparing galaxies.
"""),
("code", r"""
sigmas = np.arange(0, 401, 25)
fig, ax = plt.subplots(figsize=(8, 4.5))
for name in ['Hbeta', 'Mgb', 'Fe5270', 'Fe5335']:
    idx = [lick_index(lam, broaden_velocity(spec_log, velscale, s), name) for s in sigmas]
    ax.plot(sigmas, np.array(idx) / idx[0], label=name)
ax.set_xlabel(r'velocity dispersion $\sigma$ [km/s]'); ax.set_ylabel(r'index / index($\sigma$=0)'); ax.legend()
"""),
("md", r"""
## 5. Pixels and noise

A spectrum is sampled on pixels (Nyquist: at least ~2 pixels per FWHM) and every pixel has noise. Can you still see Hβ at S/N = 10?
"""),
("code", r"""
s200 = broaden_velocity(spec_log, velscale, 200)
fig, ax = plt.subplots(figsize=(10, 4.5))
sel = (lam > 4780) & (lam < 4940)
for i, snr in enumerate([100, 30, 10]):
    noisy, _ = add_noise(s200, snr, rng=i)
    ax.plot(lam[sel], noisy[sel] - 0.25 * i, label=f'S/N = {snr} per pixel')
ax.axvline(4861, color='grey', ls=':'); ax.legend(); ax.set_xlabel(r'wavelength [$\AA$]')
"""),
("md", r"""
## Exercises

1. Degrade the spectrum to R = 100 (prism). Which features survive? Can you still tell a 1 Gyr from a 10 Gyr population (try `ssp.synthesize(age=1.0, met=0.0)`)?
2. Make Figure 4 for a young (0.5 Gyr) population. Does Hβ respond to σ in the same way?
3. Your spectrograph has FWHM = 3 Å, the models 2.51 Å, the galaxy σ = 60 km/s. What Gaussian do you convolve the *models* with before comparing them with the galaxy (give σ in km/s at 5000 Å)?
4. Use `scipy.ndimage.gaussian_filter1d` instead of `convolve(...)` and check you get the same answer.
"""),
]

# ============================================================== 06
NB06 = [
("md", r"""
# 06 — Measuring age and metallicity: fitting one SSP with FaSTAR

*Lecture 1: stellar populations*

We make a **mock galaxy spectrum** with known age and metallicity, add the effects from notebook 05 (velocity dispersion, noise), and try to get the parameters back by comparing it with FaSTAR models:

$$\chi^2(t, Z) = \sum_\mathrm{pixels} \left(\frac{F_\mathrm{obs} - A\,F_\mathrm{model}(t, Z)}{\sigma_\mathrm{noise}}\right)^2 .$$

The amplitude $A$ (the galaxy's mass and distance) is solved for exactly at each step (it is linear). You will meet the **age–metallicity degeneracy** of the lecture in numbers — and see why spectra beat colours.

Tools: FaSTAR, numpy, scipy (`scipy.optimize.minimize`). A model takes ~0.2 s; the whole notebook runs in ~5 minutes.
"""),
("code", SETUP + r"""
from scipy.optimize import minimize
from fastar import IntegratedSSPSynthesizer, imf
from stellarpops.spectra import log_rebin, broaden_velocity, add_noise

ssp = IntegratedSSPSynthesizer(imf_function=imf.kroupa)
wave = np.array(ssp.wave)
ln_lam, _, velscale = log_rebin(wave, np.ones_like(wave))
lam = np.exp(ln_lam)
FIT = (lam > 3800) & (lam < 7200)          # pixels used in the fit

_cache = {}
def model(age, met, sigma):
    # FaSTAR SSP, log-rebinned and broadened to the galaxy's velocity dispersion (cached)
    key = (round(float(age), 5), round(float(met), 5), sigma)
    if key not in _cache:
        s = np.array(ssp.synthesize(age=float(age), met=float(met)))
        s = np.interp(ln_lam, np.log(wave), s)
        _cache[key] = broaden_velocity(s / np.median(s), velscale, sigma)
    return _cache[key]
"""),
("md", r"""
## 1. A mock galaxy
"""),
("code", r"""
TRUE = dict(age=5.0, met=-0.3)
SIGMA = 150.0          # km/s, assumed known (pPXF measures it, notebook 07)
SNR = 20               # per pixel

clean = model(TRUE['age'], TRUE['met'], SIGMA)
obs, err = add_noise(clean, SNR, rng=42)

plt.figure(figsize=(11, 4))
plt.plot(lam[FIT], obs[FIT], lw=0.6, label=f'mock: {TRUE["age"]} Gyr, [M/H] = {TRUE["met"]}, S/N = {SNR}')
plt.xlabel(r'wavelength [$\AA$]'); plt.legend()
"""),
("md", r"""
## 2. χ² with the best amplitude

For fixed $(t, Z)$ the best amplitude is $A = \sum (F_\mathrm{obs} F_\mathrm{mod}/\sigma^2) / \sum (F_\mathrm{mod}^2/\sigma^2)$ — a one-line linear fit.
"""),
("code", r"""
def chi2(age, met, data=obs, noise=err, sigma=SIGMA, mask=FIT):
    m = model(age, met, sigma)[mask]
    d, e = data[mask], noise[mask]
    A = np.sum(d * m / e**2) / np.sum(m**2 / e**2)
    return np.sum(((d - A * m) / e) ** 2)

print('chi2 at the truth:', round(chi2(**TRUE)), 'for', FIT.sum(), 'pixels  (expect about the number of pixels)')
print('chi2 at 10 Gyr, solar:', round(chi2(10.0, 0.0)))
"""),
("md", r"""
## 3. The χ² landscape: a diagonal valley

We evaluate χ² on a grid. The colours show how much worse than the best model each point is (log scale).
"""),
("code", r"""
ages = np.geomspace(1.0, 13.5, 22)
mets = np.linspace(-1.0, 0.3, 14)
chi = np.array([[chi2(a, m) for m in mets] for a in ages])

fig, ax = plt.subplots(figsize=(7, 5.5))
cs = ax.contourf(mets, np.log10(ages), np.log10(chi - chi.min() + 1), levels=20, cmap='viridis_r')
plt.colorbar(cs, label=r'log$_{10}(\Delta\chi^2 + 1)$')
ax.plot(TRUE['met'], np.log10(TRUE['age']), 'r*', ms=18, label='truth')
i, j = np.unravel_index(chi.argmin(), chi.shape)
ax.plot(mets[j], np.log10(ages[i]), 'wx', ms=12, mew=3, label='best grid point')
ax.set_xlabel('[M/H]'); ax.set_ylabel('log age [Gyr]'); ax.legend()
"""),
("md", r"""
**Question.** Which way does the valley of good fits run? Relate it to the "older or more metal-rich?" slide: older *and* more metal-poor (or younger and more metal-rich) look alike.
"""),
("md", r"""
## 4. A proper minimisation and the uncertainty

Starting from the best grid point, `scipy.optimize.minimize` (Nelder–Mead, no derivatives) finds the minimum in $(\log t, [M/H])$.
Then we map $\Delta\chi^2$ on a fine grid around it: $\Delta\chi^2 = 2.3$ and $6.2$ enclose the 68% and 95% regions for two parameters.
"""),
("code", r"""
def f(p):
    la, met = p
    if not (np.log10(0.05) < la < np.log10(13.9) and -2.4 < met < 0.29):
        return 1e30
    return chi2(10 ** la, met)

res = minimize(f, x0=[np.log10(ages[i]), mets[j]], method='Nelder-Mead', options=dict(xatol=1e-3, fatol=0.5))
la0, m0 = res.x
print(f'best fit: age = {10 ** la0:.2f} Gyr, [M/H] = {m0:+.3f}   (truth {TRUE["age"]} Gyr, {TRUE["met"]}),  {res.nfev} models')

dla, dm = np.linspace(-0.04, 0.04, 11), np.linspace(-0.04, 0.04, 11)
fine = np.array([[f([la0 + a, m0 + b]) for b in dm] for a in dla])
fig, ax = plt.subplots(figsize=(6.5, 5.5))
ax.contour(m0 + dm, la0 + dla, fine - fine.min(), levels=[2.3, 6.2, 11.8], colors=['k', 'grey', 'lightgrey'])
ax.plot(TRUE['met'], np.log10(TRUE['age']), 'r*', ms=16, label='truth')
ax.plot(m0, la0, 'kx', ms=12, mew=3, label='best fit')
ax.set_xlabel('[M/H]'); ax.set_ylabel('log age [Gyr]'); ax.legend(); ax.set_title(r'$\Delta\chi^2$ = 2.3, 6.2, 11.8')
"""),
("md", r"""
The ellipse is **tilted** — that is the degeneracy — but tiny: a full spectrum with perfect models pins down age and metallicity to a few per cent. In real life the error budget is dominated by the *models* (stellar libraries, isochrones, the IMF, α-enhancement), not by the noise.
"""),
("md", r"""
## 5. Repeat with new noise

Fit 5 noise realisations at three S/N values (a few minutes). The scatter of the results is the real statistical uncertainty.
"""),
("code", r"""
results = {}
for snr in [5, 20, 80]:
    out = []
    for seed in range(5):
        d, e = add_noise(clean, snr, rng=100 + seed)
        g = lambda p: 1e30 if not (-1.3 < p[0] < 1.14 and -2.4 < p[1] < 0.29) else chi2(10 ** p[0], p[1], data=d, noise=e)
        out.append(minimize(g, x0=[np.log10(TRUE['age']), TRUE['met']], method='Nelder-Mead',
                            options=dict(xatol=2e-3, fatol=0.5)).x)
    results[snr] = np.array(out)

fig, ax = plt.subplots(figsize=(7, 5.5))
for snr, r in results.items():
    ax.plot(r[:, 1], r[:, 0], 'o', ms=9, label=f'S/N = {snr}')
ax.plot(TRUE['met'], np.log10(TRUE['age']), 'k*', ms=18, label='truth')
ax.set_xlabel('[M/H]'); ax.set_ylabel('log age [Gyr]'); ax.legend()
"""),
("md", r"""
## 6. Colours only

Now throw the lines away: measure the mean flux in six broad bands (like photometry) with 2% errors, and fit those. Compare the allowed region with the full-spectrum one.
"""),
("code", r"""
BANDS = [(3800, 4300), (4300, 4800), (4800, 5300), (5300, 5800), (5800, 6400), (6400, 7200)]
def bandflux(s):
    f = np.array([s[(lam > lo) & (lam < hi)].mean() for lo, hi in BANDS])
    return f / f[3]                              # normalise: only the shape (colours) matters

phot = bandflux(clean)
ephot = 0.02 * phot
def chi2_phot(age, met):
    return np.sum(((phot - bandflux(model(age, met, SIGMA))) / ephot) ** 2)

chi_p = np.array([[chi2_phot(a, m) for m in mets] for a in ages])     # reuses the cached models
fig, ax = plt.subplots(figsize=(7, 5.5))
ax.contourf(mets, np.log10(ages), chi_p - chi_p.min(), levels=[0, 2.3, 6.2], colors=['C1', 'moccasin'])
ax.contour(m0 + dm, la0 + dla, fine - fine.min(), levels=[2.3], colors='k')
ax.plot(TRUE['met'], np.log10(TRUE['age']), 'r*', ms=18)
ax.set_xlabel('[M/H]'); ax.set_ylabel('log age [Gyr]')
ax.set_title('orange: six colours (2% errors), black: full spectrum')
"""),
("md", r"""
**This is the degeneracy of the lecture:** with colours alone, a whole diagonal band of (age, metallicity) is allowed. Absorption lines (Hβ for age, Mg b and Fe for metals) break it.
"""),
("md", r"""
## Exercises

1. Fit with the wrong velocity dispersion (e.g. `sigma=100` in `chi2`). Which parameter is biased, and why?
2. Make the mock with a bottom-heavy IMF: `IntegratedSSPSynthesizer(imf_function=imf.single_power_law)` with `imf_params={'alpha': 3.0}`, and fit it with Kroupa models. Is the fit bad? Are age and metallicity biased?
3. Mask everything except Hβ, Mg b and Fe5270/5335 (`mask=` argument of `chi2`). How much precision do you lose?
4. Add dust to the mock (multiply by $(\lambda/5500\,\AA)^{0.3}$) and fit the colours again. Which way does the answer move?
5. Real galaxies are not one SSP — that is notebook 07.
"""),
]

# ============================================================== 07
NB07 = [
("md", r"""
# 07 — Synthetic galaxies and their star-formation histories

*Lecture 1 (stellar populations) → Lecture 2 (star-formation histories, the [Mg/Fe] clock)*

A galaxy is a **sum of SSPs**: every generation of stars, with its own age and metallicity, adds its spectrum weighted by the **mass it formed**:

$$F_\mathrm{gal}(\lambda) = \Big[\sum_{i} M_i\, F_\mathrm{SSP}(\lambda;\, t_i, Z_i)\Big] \ast \mathrm{LOSVD} + \text{noise}.$$

Recovering the weights $M_i \ge 0$ is a **linear** problem with a positivity constraint (non-negative least squares). It is ill-posed: many SFHs fit the data equally well, so we add **regularisation** (prefer smooth solutions).

We use **pPXF** (Cappellari & Emsellem 2004; Cappellari 2017, 2023) — the standard tool for this — with FaSTAR templates.

**Extra packages:** `pip install ppxf` (pPXF; numpy/scipy/matplotlib only) and `pip install fastar-astro`.
Alternatives you may meet: Prospector, FAST, BAGPIPES, STARLIGHT, FIREFLY, pyPipe3D.

⏱ The template grid takes ~1 minute, each fit a few seconds.
"""),
("code", SETUP + r"""
from fastar import IntegratedSSPSynthesizer, imf
from ppxf.ppxf import ppxf
from scipy.optimize import nnls
from stellarpops.spectra import log_rebin, broaden_velocity, add_noise

ssp = IntegratedSSPSynthesizer(imf_function=imf.kroupa)
wave = np.array(ssp.wave)
"""),
("md", r"""
## 1. Templates: a grid of SSPs

FaSTAR spectra are *per solar mass formed*, so the pPXF weights will be **masses formed**. We log-rebin all templates (notebook 05).
"""),
("code", r"""
ages = np.geomspace(0.06, 13.0, 14)               # Gyr
mets = np.array([-1.5, -1.0, -0.5, 0.0, 0.25])    # [M/H]
grid = np.array([[np.array(ssp.synthesize(age=float(a), met=float(m))) for m in mets] for a in ages])
SCALE = np.median(grid)                           # keep numbers near 1

ln_lam, _, velscale = log_rebin(wave, grid[0, 0])
templates = np.array([[np.interp(ln_lam, np.log(wave), grid[i, j]) for j in range(mets.size)]
                      for i in range(ages.size)]) / SCALE
templates = np.moveaxis(templates, -1, 0)         # pPXF wants (n_pixels, n_ages, n_mets)
print('templates:', templates.shape, f' velscale = {velscale:.1f} km/s')
"""),
("md", r"""
## 2. Four synthetic galaxies

We build them from a **finer** set of ages than the template grid (fitting with exactly the same templates that made the mock would be cheating — the "inverse crime").
"""),
("code", r"""
def make_galaxy(sfh, zfun, sigma, snr, seed=0, t_max=13.0, n=60):
    # sfh(t): star-formation rate at lookback time t [Gyr]; zfun(t): [M/H] of stars born then
    t = np.geomspace(0.05, t_max, n)
    dt = np.gradient(t)
    mass = sfh(t) * dt
    spec = sum(m * np.array(ssp.synthesize(age=float(a), met=float(np.clip(zfun(a), -2.4, 0.29))))
               for a, m in zip(t, mass) if m > 0) / SCALE
    lnl, s, _ = log_rebin(wave, spec, velscale)
    s = broaden_velocity(s, velscale, sigma)
    s, noise = add_noise(s, snr, rng=seed)
    return dict(t=t, mass=mass / mass.sum(), z=zfun(t), lam=np.exp(lnl), flux=s, noise=noise, sigma=sigma)

galaxies = {
  'old elliptical':  make_galaxy(lambda t: np.exp(-0.5 * ((t - 11.5) / 0.7) ** 2), lambda t: 0.1 + 0 * t, sigma=250, snr=60),
  'Milky-Way disc':  make_galaxy(lambda t: (t < 11) * 1.0, lambda t: 0.1 - 0.08 * t, sigma=100, snr=60),
  'post-starburst':  make_galaxy(lambda t: np.exp(-0.5 * ((t - 11) / 1) ** 2) + 3 * np.exp(-0.5 * ((t - 0.6) / 0.1) ** 2),
                                 lambda t: 0.0 + 0 * t, sigma=150, snr=60),
  'bursty dwarf':    make_galaxy(lambda t: np.exp(-0.5 * ((t - 9) / 0.8) ** 2) + 0.6 * np.exp(-0.5 * ((t - 1.5) / 0.3) ** 2),
                                 lambda t: np.where(t > 4, -1.0, -0.6), sigma=40, snr=60),
}
fig, ax = plt.subplots(figsize=(11, 4.5))
for k, (name, g) in enumerate(galaxies.items()):
    sel = (g['lam'] > 3800) & (g['lam'] < 7200)
    ax.plot(g['lam'][sel], g['flux'][sel] / np.median(g['flux'][sel]) + 0.6 * k, lw=0.6, label=name)
ax.set_xlabel(r'wavelength [$\AA$]'); ax.legend(fontsize=9, loc='upper right')
"""),
("md", r"""
## 3. Fit one galaxy with pPXF

* `start=[V, sigma]` — first guess of the kinematics (km/s); `moments=2` fits V and σ.
* `degree=-1, mdegree=8` — no additive polynomial; a multiplicative one absorbs flux-calibration errors and dust.
* `regul` — regularisation strength (0 = plain non-negative least squares).
"""),
("code", r"""
def fit(g, regul=0, mdegree=8, plot=False):
    sel = (g['lam'] > 3800) & (g['lam'] < 7200)
    pp = ppxf(templates, g['flux'][sel], g['noise'][sel], velscale, start=[0, 100], moments=2,
              degree=-1, mdegree=mdegree, lam=g['lam'][sel], lam_temp=np.exp(ln_lam),
              regul=regul, reg_dim=templates.shape[1:], quiet=True, plot=plot)
    w = pp.weights.reshape(ages.size, mets.size)
    return pp, w / w.sum()

g = galaxies['post-starburst']
pp, w = fit(g, regul=0, plot=True)
print(f'sigma: fitted {pp.sol[1]:.0f} km/s, true {g["sigma"]} km/s;  chi2/pixel = {pp.chi2:.2f}')
"""),
("md", r"""
## 4. Recovered vs true star-formation history

We compare the **cumulative** mass formed (from the oldest stars to today), which is much more robust than the mass in single age bins.
"""),
("code", r"""
def compare(name, regul_values=(0, 30, 300)):
    g = galaxies[name]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 4.5))
    order = np.argsort(g['t'])[::-1]
    a2.plot(g['t'][order], np.cumsum(g['mass'][order]), 'k', lw=4, label='truth')
    for regul in regul_values:
        pp, w = fit(g, regul=regul)
        m_age = w.sum(axis=1)
        a1.plot(ages, m_age, 'o-', label=f'regul = {regul}')
        a2.plot(ages[::-1], np.cumsum(m_age[::-1]), 'o-', label=f'regul = {regul}')
        mw_age = 10 ** (m_age @ np.log10(ages)); mw_z = w.sum(axis=0) @ mets
        print(f'regul={regul:4d}: mass-weighted age {mw_age:5.2f} Gyr, [M/H] {mw_z:+.2f}  (chi2/pix {pp.chi2:.2f})')
    print(f'truth     : mass-weighted age {10 ** (g["mass"] @ np.log10(g["t"])):5.2f} Gyr, [M/H] {g["mass"] @ g["z"]:+.2f}')
    for ax in (a1, a2):
        ax.set_xscale('log'); ax.set_xlabel('lookback time (age) [Gyr]')
    a1.set_ylabel('fraction of mass formed'); a2.set_ylabel('cumulative mass fraction (oldest first)')
    a1.set_title(name); a2.legend(fontsize=9)

compare('post-starburst')
"""),
("code", r"""
compare('old elliptical')
"""),
("code", r"""
compare('Milky-Way disc')
"""),
("code", r"""
compare('bursty dwarf')
"""),
("md", r"""
**How much regularisation?** Too little gives spiky, noise-driven solutions; too much smears real bursts out (look at regul = 300 for the post-starburst, and at its higher χ²). A classic recipe (Press et al.; Cappellari 2017): increase `regul` until χ² has grown by $\sqrt{2N_\mathrm{pix}}$ above the unregularised fit.

**Questions.**
* Without regularisation (`regul=0`) the solution is spiky: why does a least-squares fit love a few templates?
* Which features are recovered robustly: the young burst, the old bulk, the exact ages?
* Compare the mass-weighted [M/H] with the truth. Where does the age–metallicity degeneracy show up?
"""),
("md", r"""
## 5. What pPXF does, by hand

With the kinematics fixed, the problem is **non-negative least squares**: find $w_i \ge 0$ minimising $\|(\mathbf{T} w - F)/\sigma\|^2$. `scipy.optimize.nnls` solves it in one line.
"""),
("code", r"""
g = galaxies['post-starburst']
sel = (g['lam'] > 3800) & (g['lam'] < 7200)
# templates on the galaxy's wavelength pixels, broadened with the true sigma
T = np.array([broaden_velocity(templates[:, i, j], velscale, g['sigma'])
              for i in range(ages.size) for j in range(mets.size)]).T
T = np.array([np.interp(np.log(g['lam'][sel]), ln_lam, T[:, k]) for k in range(T.shape[1])]).T
A = T / g['noise'][sel, None]; b = g['flux'][sel] / g['noise'][sel]
w_nnls, _ = nnls(A, b)
w_nnls = w_nnls.reshape(ages.size, mets.size); w_nnls /= w_nnls.sum()
print('templates used (weight > 1%):', int((w_nnls > 0.01).sum()), 'of', w_nnls.size)
plt.plot(ages, w_nnls.sum(1), 'o-', label='scipy nnls'); plt.plot(ages, fit(g, regul=0)[1].sum(1), 's--', label='pPXF, regul=0')
plt.xscale('log'); plt.xlabel('age [Gyr]'); plt.ylabel('fraction of mass formed'); plt.legend()
"""),
("md", r"""
## Exercises

1. Lower the S/N of the post-starburst to 15 (`make_galaxy(..., snr=15)`). Is the young burst still found? Its mass? Its age?
2. Make the burst **older** (t = 2 Gyr instead of 0.6 Gyr). Why is it harder to recover?
3. Add 30% more "dust": multiply the galaxy by a smooth slope, `g['flux'] *= (g['lam'] / 5500) ** 0.5`. Fit with `mdegree=0` and `mdegree=8`. What happens?
4. Build templates with a top-heavy or bottom-heavy IMF (`imf.single_power_law`, `imf_params={'alpha': ...}`) and fit the Milky-Way disc. How much does the inferred SFH depend on the IMF you assume?
5. Lecture 2 link: the SFH of the old elliptical tells you its star-formation **duration**. Compare it with the [Mg/Fe] ≈ +0.3 argument (Slido S2.9).
"""),
]
