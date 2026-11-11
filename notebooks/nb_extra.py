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
### S2.3 — Four stars from four papers: which one is the most metal-poor?
A: [Fe/H] = +0.3, B: Z = 0.02, C: [M/H] = −0.5, D: [Fe/H] = −2.0. Put them all on one scale: $[\mathrm{M/H}] \approx \log_{10}(Z/Z_\odot)$ with today's $Z_\odot = 0.0134$ (for a solar-scaled mix $[\mathrm{M/H}] = [\mathrm{Fe/H}]$). Names used in papers (Beers & Christlieb 2005): metal-poor < −1, very < −2, extremely < −3, ultra < −4.
"""),
("code", r"""
Zsun = 0.0134
stars = {'A [Fe/H] = +0.3': 0.3, 'B Z = 0.02': np.log10(0.02 / Zsun), 'C [M/H] = -0.5': -0.5, 'D [Fe/H] = -2.0': -2.0}
for name, mh in sorted(stars.items(), key=lambda kv: kv[1]):
    print(f'{name:18s} -> [M/H] = {mh:+.2f},  Z = {Zsun * 10**mh:.5f},  {10**mh:.3g} x the Sun')
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

# IntegratedSSPSynthesizer = FaSTAR's model for a whole population (infinitely many stars):
#   it interpolates an isochrone (which stars are alive), weights them with the IMF and adds up
#   their spectra (predicted by a neural network trained on the MILES library). See notebook 02,
#   section 0, for the same calculation done step by step.
ssp = IntegratedSSPSynthesizer(imf_function=imf.kroupa)   # imf.kroupa: Kroupa (2001), 0.1-100 Msun
wave = np.array(ssp.wave)                                 # wavelengths [A], 3540-7410, 0.9 A/pixel
spec = ssp.synthesize(age=10.0, met=0.0)                  # age in Gyr, met = [M/H]; flux per Msun formed
spec = normalise(wave, np.array(spec))                    # divide by the median flux at 5400-5600 A
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
## 5. Convolution conserves the equivalent width — a proof

The **equivalent width** of an absorption line is the width of a rectangle of zero flux that removes the same light:

$$W = \int \Big(1 - \frac{F(\lambda)}{F_c}\Big)\, d\lambda \equiv \int D(\lambda)\, d\lambda ,$$

with $F_c$ the continuum and $D = 1 - F/F_c$ the line *depth*. Take a normalised spectrum ($F_c = 1$) and a kernel with unit area, $\int K(x)\,dx = 1$ (a Gaussian LSF or LOSVD).

**Step 1 — the continuum is untouched.** $(1 \ast K)(\lambda) = \int 1\cdot K(\lambda-\lambda')\,d\lambda' = 1$. So the depth of the convolved spectrum is the convolved depth:
$$1 - (F \ast K) = (1 - F)\ast K = D \ast K .$$

**Step 2 — swap the integrals (Fubini).**
$$W' = \int (D \ast K)(\lambda)\, d\lambda = \int\!\!\int D(\lambda')\,K(\lambda - \lambda')\, d\lambda'\, d\lambda
= \int D(\lambda') \underbrace{\Big[\int K(\lambda - \lambda')\, d\lambda\Big]}_{=\,1}\, d\lambda' = W . \qquad \blacksquare$$

**The same in one line with Fourier transforms:** the integral of a function is its Fourier transform at zero frequency, $W = \hat D(0)$. The convolution theorem gives $\widehat{D\ast K} = \hat D\,\hat K$, and $\hat K(0) = \int K = 1$, so $W' = \hat D(0)\hat K(0) = W$.

**What the proof assumes** (and where real measurements break it):
1. the kernel has unit area (it only *redistributes* light, it does not add or remove any);
2. the continuum is flat — or linear, because a symmetric kernel leaves a straight line unchanged;
3. you integrate over the **whole** broadened line. A fixed window (Lick bands!) misses the wings that spread outside it → the measured index drops (section 4), although the true $W$ is conserved;
4. in velocity space the same holds for $W$ measured in $\ln\lambda$ (km/s); $W_\lambda \approx \lambda\, W_{\ln\lambda}$.

Convolution is **linear** — so this holds for weak and saturated lines alike.
"""),
("code", r"""
# Numerical check 1: an isolated Gaussian absorption line, broadened more and more
x = np.arange(-400, 401) * 0.9                  # wavelength offset [A], 0.9 A pixels like FaSTAR
line = 1 - 0.7 * np.exp(-0.5 * (x / 1.2) ** 2)  # depth 0.7, sigma 1.2 A
W_true = np.trapezoid(1 - line, x)

kernel_sigmas_A = [0.5, 2, 5, 10, 20]
for s_A in kernel_sigmas_A:
    broad = convolve(line, gaussian_kernel(s_A / 0.9))
    W_all = np.trapezoid(1 - broad, x)                            # whole line
    win = np.abs(x) < 8                                           # a fixed 16 A window
    W_win = np.trapezoid(1 - broad[win], x[win])
    print(f'kernel sigma {s_A:4.1f} A:  W (all) = {W_all:.3f} A,  W (16 A window) = {W_win:.3f} A,  true {W_true:.3f} A')

fig, ax = plt.subplots(figsize=(9, 4))
for s_A in [0, 2, 5, 10]:
    y = line if s_A == 0 else convolve(line, gaussian_kernel(s_A / 0.9))
    ax.plot(x, y, label=f'kernel sigma = {s_A} A')
ax.axvspan(-8, 8, color='grey', alpha=0.15, label='fixed window')
ax.set_xlim(-60, 60); ax.set_xlabel(r'$\lambda - \lambda_0$ [$\AA$]'); ax.legend(fontsize=9)
ax.set_title('the line gets shallower and wider: the area (W) stays the same')
"""),
("code", r"""
# Numerical check 2: the real FaSTAR spectrum, Mg b region, broadened by velocity dispersion.
# W over a wide window (5100-5260 A) against a fixed continuum level stays (almost) the same;
# the Lick Mg b index in its fixed 32 A band drops.
def W_wide(lam_, f, lo=5100, hi=5260):
    sel = (lam_ > lo) & (lam_ < hi)
    cont = np.median(f[(lam_ > 5300) & (lam_ < 5330)])    # one continuum level for all
    return np.trapezoid(1 - f[sel] / cont, lam_[sel])

for sigma in [0, 100, 200, 300, 400]:
    b = broaden_velocity(spec_log, velscale, sigma)
    print(f'sigma = {sigma:3d} km/s:  W(5100-5260 A) = {W_wide(lam, b):6.2f} A,  Lick Mg b = {lick_index(lam, b, "Mgb"):5.2f} A')
"""),
("md", r"""
**Questions.**
1. In check 2 the wide-window $W$ is conserved to a few per cent only. Which assumption of the proof is (slightly) violated? *(Hint: lines near the window edges; is the continuum flat?)*
2. Why do people still use fixed windows (Lick indices) if they are not conserved? *(Comparability between instruments/galaxies, and blends: a "whole line" does not exist in a crowded spectrum.)*
3. Show that convolving with a kernel of area 0.9 instead of 1 changes $W$. By how much — and why can a real LSF never do that?
"""),
("md", r"""
## 6. Pixels and noise

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
        # 1. FaSTAR: isochrone at (age, met) -> IMF weights -> sum of stellar spectra (notebook 02, section 0)
        s = np.array(ssp.synthesize(age=float(age), met=float(met)))
        # 2. resample to the ln(lambda) grid, where a velocity dispersion is a single kernel (notebook 05)
        s = np.interp(ln_lam, np.log(wave), s)
        # 3. normalise (the fit solves for the amplitude anyway) and broaden by sigma [km/s]
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

**The physics in one equation.** A galaxy is a sum of simple stellar populations (SSPs). Every generation of stars, born at lookback time $t_i$ with metallicity $Z_i$, adds its spectrum weighted by the **mass it formed**, $M_i$:

$$F_\mathrm{gal}(\lambda) = \Big[\sum_{i} M_i\, F_\mathrm{SSP}(\lambda;\, t_i, Z_i)\Big] \ast \mathrm{LOSVD} \;+\; \text{noise}.$$

* $F_\mathrm{SSP}(\lambda; t, Z)$ — the light of 1 M$_\odot$ of stars formed $t$ ago: the IMF-weighted sum of all stars still alive on the isochrone (notebook 02, section 0).
* $\ast\,\mathrm{LOSVD}$ — the stars move: their lines are Doppler-broadened by the velocity dispersion $\sigma$ (notebook 05).
* The list $\{M_i\}$ **is** the star-formation history (SFH): $\mathrm{SFR}(t_i) \approx M_i/\Delta t_i$.

**The inverse problem.** Given $F_\mathrm{gal}$, find $M_i \ge 0$. For fixed $\sigma$ this is *linear* in the $M_i$ (non-negative least squares). It is **ill-posed**: old populations of similar age look almost identical, so many SFHs fit equally well. Adding **regularisation** (prefer smooth SFHs) picks a sensible one.

**Which stars make which features** (section 2 below shows them):

| feature | λ [Å] | made mostly by | tells you about |
|---|---|---|---|
| Balmer lines Hδ, Hγ, Hβ, Hα | 4102, 4340, 4861, 6563 | A stars (T ≈ 8000–10000 K, 1.5–3 M$_\odot$ on the main sequence): strongest at 0.3–1 Gyr | **age** (recent star formation) |
| 4000 Å break, Ca II H&K | 3934, 3969 | cool stars (G, K): metal opacity in their atmospheres | age + metallicity |
| G band (CH) | 4300 | G and K stars | age/metallicity, C |
| Mg b | 5167–5184 | K giants and dwarfs | **Mg** (α elements, SN II) |
| Fe 5270, Fe 5335 | | G, K stars | **Fe** (SN Ia) |
| Na D | 5890, 5896 | cool dwarfs (and interstellar gas) | low-mass stars → IMF |
| TiO bands | 6200, 7100 | M dwarfs and M giants (T < 4000 K) | low-mass stars, cool giants |

**Tools.** `pip install ppxf` — pPXF (Cappellari & Emsellem 2004; Cappellari 2017, 2023), the standard full-spectrum fitting code; and `pip install fastar-astro` for the SSP templates. Alternatives you will meet: Prospector, BAGPIPES, FAST, STARLIGHT, FIREFLY, pyPipe3D.

⏱ The template grid takes ~1 minute, each fit a few seconds.
"""),
("code", SETUP + r"""
import jax.numpy as jnp
from fastar import IntegratedSSPSynthesizer, imf   # FaSTAR: SSP spectra (a neural network trained on MILES)
from ppxf.ppxf import ppxf                         # pPXF: penalised pixel fitting (Cappellari)
from scipy.optimize import nnls                    # non-negative least squares, to do it by hand
from stellarpops.spectra import log_rebin, broaden_velocity, add_noise

# One SSP model with a Kroupa IMF between 0.1 and 100 Msun.
ssp = IntegratedSSPSynthesizer(imf_function=imf.kroupa)
wave = np.array(ssp.wave)          # 3540-7410 A, 0.9 A per pixel, resolution FWHM = 2.51 A
"""),
("md", r"""
## 1. Which stars make which lines?

FaSTAR can also give the spectrum of a **single star** from its surface gravity $\log g$, effective temperature $T_\mathrm{eff}$ and metallicity (`ssp.predict_spectrum`). These are the building blocks of every SSP.
"""),
("code", r"""
# (log g [cgs], T_eff [K]) of typical stars. log g ~ 4-5: dwarfs (main sequence), log g ~ 1-3: giants.
stars = {'A0 V  (2.5 Msun, 9500 K)':  (4.0, 9500),
         'F5 V  (1.3 Msun, 6500 K)':  (4.3, 6500),
         'G2 V  (the Sun, 5770 K)':   (4.44, 5772),
         'K2 III (giant, 4500 K)':    (2.5, 4500),
         'M0 III (giant, 3800 K)':    (1.5, 3800),
         'M2 V  (0.4 Msun, 3500 K)':  (4.8, 3500)}
FEATURES = {'Ca H&K': 3950, r'H$\delta$': 4102, 'G band': 4300, r'H$\gamma$': 4340, r'H$\beta$': 4861,
            'Mg b': 5175, 'Fe': 5270, 'Na D': 5893, 'TiO': 6200, r'H$\alpha$': 6563, 'TiO ': 7100}

fig, ax = plt.subplots(figsize=(12, 7))
for k, (name, (logg, teff)) in enumerate(stars.items()):
    # predict_spectrum wants arrays of log g, log10(T_eff) and [Fe/H]; it returns spectra normalised to mean flux 1
    f = np.array(ssp.predict_spectrum(jnp.array([logg]), jnp.array([np.log10(teff)]), jnp.array([0.0])))[0]
    ax.plot(wave, f / np.median(f) + 1.2 * k, lw=0.8, label=name)
for lab, x in FEATURES.items():
    ax.axvline(x, color='grey', lw=0.6, ls=':'); ax.text(x, 7.4, lab, rotation=90, ha='center', va='bottom', fontsize=9)
ax.set_xlabel(r'wavelength [$\AA$]'); ax.set_ylabel('normalised flux + offset'); ax.set_ylim(0, 8.3)
ax.legend(loc='upper right', fontsize=8)
"""),
("md", r"""
**Look for:** deep Balmer lines only in the A and F stars; Ca H&K, the G band, Mg b and Fe growing as stars get cooler; Na D and TiO in the M stars. A galaxy spectrum is a mix of all of these, weighted by how many of each star exist (IMF) and how bright they are (isochrone).
"""),
("md", r"""
## 2. Templates: a grid of SSPs

We now build SSPs on a grid of ages and metallicities. These will be (a) the ingredients of our synthetic galaxies and (b) the **templates** we fit them with.
"""),
("code", r"""
ages = np.geomspace(0.06, 13.0, 14)               # 14 ages from 60 Myr to 13 Gyr, log-spaced (Gyr)
mets = np.array([-1.5, -1.0, -0.5, 0.0, 0.25])    # 5 metallicities [M/H]

# One FaSTAR SSP per (age, [M/H]) pair: 14 x 5 = 70 spectra, ~0.2 s each.
# Each is the spectrum of 1 Msun of stars FORMED (the IMF in FaSTAR is normalised to 1 Msun
# between 0.1 and 100 Msun), so a weight w_i in the fit = mass formed in that age/metallicity bin.
grid = np.array([[np.array(ssp.synthesize(age=float(a), met=float(m))) for m in mets] for a in ages])
SCALE = np.median(grid)                           # one common number, keeps the weights near 1

# pPXF works on a ln(lambda) grid: there a velocity dispersion is one fixed kernel (notebook 05).
ln_lam, _, velscale = log_rebin(wave, grid[0, 0])
templates = np.array([[np.interp(ln_lam, np.log(wave), grid[i, j]) for j in range(mets.size)]
                      for i in range(ages.size)]) / SCALE
templates = np.moveaxis(templates, -1, 0)         # pPXF wants the shape (n_pixels, n_ages, n_mets)
print('templates:', templates.shape, f' velscale = {velscale:.1f} km/s per pixel')
"""),
("code", r"""
# How does 1 Msun of stars FADE and REDDEN with age? (same metallicity, absolute flux per Msun formed)
fig, ax = plt.subplots(figsize=(11, 4.5))
lam_t = np.exp(ln_lam)
for i in range(0, ages.size, 3):
    ax.plot(lam_t, templates[:, i, 3], lw=0.8, label=f'{ages[i]:.2f} Gyr')
ax.set_yscale('log'); ax.set_xlabel(r'wavelength [$\AA$]'); ax.set_ylabel('flux per Msun formed (scaled)')
ax.legend(fontsize=9, ncol=2)
"""),
("md", r"""
A young SSP is ~100× brighter per unit mass than an old one: **light is dominated by the youngest stars, mass by the oldest**. That is why a small young burst can hide a big old population — and why we compare *mass-weighted* and *light-weighted* ages.
"""),
("md", r"""
## 3. Four synthetic galaxies

We build each galaxy from a **finer** set of ages than the template grid (fitting with exactly the same templates that made the mock would be cheating — the "inverse crime").
"""),
("code", r"""
def make_galaxy(sfh, zfun, sigma, snr, seed=0, t_max=13.0, n=60):
    # sfh(t):  star-formation rate at lookback time t [Gyr] (arbitrary units; only the shape matters)
    # zfun(t): [M/H] of the stars born at lookback time t (an age-metallicity relation)
    # sigma:   velocity dispersion of the stars [km/s] -> broadens all lines
    # snr:     signal-to-noise ratio per pixel
    t = np.geomspace(0.05, t_max, n)          # 60 birth times between 50 Myr and 13 Gyr ago
    dt = np.gradient(t)                       # width of each time bin [Gyr]
    mass = sfh(t) * dt                        # mass formed in each bin = SFR x duration
    # the galaxy spectrum = sum over generations of (mass formed) x (SSP spectrum per Msun formed)
    spec = sum(m * np.array(ssp.synthesize(age=float(a), met=float(np.clip(zfun(a), -2.4, 0.29))))
               for a, m in zip(t, mass) if m > 0) / SCALE
    lnl, s, _ = log_rebin(wave, spec, velscale)   # to ln(lambda), same pixels as the templates
    s = broaden_velocity(s, velscale, sigma)      # the stars move: Doppler broadening
    s, noise = add_noise(s, snr, rng=seed)        # photon noise
    return dict(t=t, mass=mass / mass.sum(), z=zfun(t), lam=np.exp(lnl), flux=s, noise=noise, sigma=sigma)

galaxies = {
  # one early burst ~11.5 Gyr ago lasting ~1 Gyr, slightly metal-rich, large sigma (massive)
  'old elliptical':  make_galaxy(lambda t: np.exp(-0.5 * ((t - 11.5) / 0.7) ** 2), lambda t: 0.1 + 0 * t, sigma=250, snr=60),
  # constant SFR for 11 Gyr; old stars are metal-poor, young ones metal-rich (chemical enrichment)
  'Milky-Way disc':  make_galaxy(lambda t: (t < 11) * 1.0, lambda t: 0.1 - 0.08 * t, sigma=100, snr=60),
  # old population + a strong burst 0.6 Gyr ago that then stopped (quenched)
  'post-starburst':  make_galaxy(lambda t: np.exp(-0.5 * ((t - 11) / 1) ** 2) + 3 * np.exp(-0.5 * ((t - 0.6) / 0.1) ** 2),
                                 lambda t: 0.0 + 0 * t, sigma=150, snr=60),
  # two bursts (9 and 1.5 Gyr ago), metal-poor, small sigma (low mass)
  'bursty dwarf':    make_galaxy(lambda t: np.exp(-0.5 * ((t - 9) / 0.8) ** 2) + 0.6 * np.exp(-0.5 * ((t - 1.5) / 0.3) ** 2),
                                 lambda t: np.where(t > 4, -1.0, -0.6), sigma=40, snr=60),
}

fig, ax = plt.subplots(figsize=(12, 6))
for k, (name, g) in enumerate(galaxies.items()):
    sel = (g['lam'] > 3800) & (g['lam'] < 7200)
    ax.plot(g['lam'][sel], g['flux'][sel] / np.median(g['flux'][sel]) + 0.6 * k, lw=0.6, label=name)
for lab, x in FEATURES.items():
    ax.axvline(x, color='grey', lw=0.6, ls=':'); ax.text(x, 3.05, lab, rotation=90, ha='center', va='bottom', fontsize=9)
ax.set_ylim(0, 3.6); ax.set_xlabel(r'wavelength [$\AA$]'); ax.legend(fontsize=9, loc='lower right')
"""),
("md", r"""
**Read the spectra like a detective.** The post-starburst has the deepest Balmer lines (A stars from the 0.6 Gyr burst). The old elliptical has the strongest Mg b and Fe, a deep 4000 Å break and smeared-out lines ($\sigma$ = 250 km/s). The dwarf has weak metal lines (low [M/H]) but sharp ones ($\sigma$ = 40 km/s).
"""),
("md", r"""
## 4. Who makes the light? Split a galaxy into its generations

Because the galaxy is a *sum*, we can plot each part separately: here the post-starburst, split into stars younger and older than 2 Gyr.
"""),
("code", r"""
g = galaxies['post-starburst']
young = g['t'] < 2.0
def part(mask):
    s = sum(m * np.array(ssp.synthesize(age=float(a), met=0.0)) for a, m, ok in zip(g['t'], g['mass'], mask) if ok)
    return np.interp(ln_lam, np.log(wave), s)
f_young, f_old = part(young), part(~young)
print(f'mass fraction in stars < 2 Gyr: {g["mass"][young].sum():.0%}   '
      f'light fraction at 5500 A: {np.interp(5500, lam_t, f_young) / np.interp(5500, lam_t, f_young + f_old):.0%}')

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(lam_t, f_young + f_old, 'k', lw=0.8, label='total')
ax.plot(lam_t, f_young, lw=0.8, label='stars < 2 Gyr (the burst)')
ax.plot(lam_t, f_old, lw=0.8, label='stars > 2 Gyr')
for lab, x in FEATURES.items():
    ax.axvline(x, color='grey', lw=0.6, ls=':')
ax.set_xlim(3800, 7200); ax.set_xlabel(r'wavelength [$\AA$]'); ax.set_ylabel('flux'); ax.legend()
"""),
("md", r"""
The young stars carry a small fraction of the **mass** but a large fraction of the **light**, especially in the blue, and they make the deep Balmer lines. The old stars make the red continuum, Mg b, Fe and TiO.
"""),
("md", r"""
## 5. Fit one galaxy with pPXF

What pPXF does: for trial kinematics (V, σ) it broadens all templates, then finds the non-negative weights that best reproduce the galaxy, and iterates on (V, σ).

* `start=[V, sigma]` — first guess of the kinematics (km/s); `moments=2` fits V and σ.
* `degree=-1` — no additive polynomial (it would mimic a featureless continuum and bias the ages).
* `mdegree=8` — a multiplicative polynomial: absorbs flux-calibration errors and dust (changes the continuum shape, not the lines).
* `regul` — regularisation strength (0 = plain non-negative least squares).
* `reg_dim` — the template grid shape (n_ages, n_mets), so pPXF knows which weights are neighbours.
"""),
("code", r"""
def fit(g, regul=0, mdegree=8, plot=False):
    sel = (g['lam'] > 3800) & (g['lam'] < 7200)          # fit range: avoid the ends of the model spectra
    pp = ppxf(templates,                                  # (n_pix, n_ages, n_mets) SSPs per Msun formed
              g['flux'][sel], g['noise'][sel],            # the data and its 1-sigma errors
              velscale, start=[0, 100], moments=2,        # fit V and sigma, starting from 0 and 100 km/s
              degree=-1, mdegree=mdegree,                 # polynomials (see above)
              lam=g['lam'][sel], lam_temp=np.exp(ln_lam), # wavelengths: pPXF works out the offsets itself
              regul=regul, reg_dim=templates.shape[1:],   # smoothness penalty on the weight grid
              quiet=True, plot=plot)
    w = pp.weights.reshape(ages.size, mets.size)          # mass formed in each (age, [M/H]) bin
    return pp, w / w.sum()                                # normalise: fractions of the total mass formed

g = galaxies['post-starburst']
pp, w = fit(g, regul=0, plot=True)
print(f'sigma: fitted {pp.sol[1]:.0f} km/s, true {g["sigma"]} km/s;  chi2/pixel = {pp.chi2:.2f}')
"""),
("md", r"""
In the plot: black = data, red = best fit, green = residuals (offset). χ²/pixel ≈ 1 means the fit is as good as the noise allows.
"""),
("md", r"""
## 6. Recovered vs true star-formation history

We compare the **cumulative** mass formed (from the oldest stars to today), which is much more robust than the mass in single age bins, and the mass-weighted mean age and [M/H].
"""),
("code", r"""
def compare(name, regul_values=(0, 30, 300)):
    g = galaxies[name]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 4.5))
    order = np.argsort(g['t'])[::-1]                                    # oldest first
    a2.plot(g['t'][order], np.cumsum(g['mass'][order]), 'k', lw=4, label='truth')
    for regul in regul_values:
        pp, w = fit(g, regul=regul)
        m_age = w.sum(axis=1)                                           # sum over metallicity -> mass per age
        a1.plot(ages, m_age, 'o-', label=f'regul = {regul}')
        a2.plot(ages[::-1], np.cumsum(m_age[::-1]), 'o-', label=f'regul = {regul}')
        mw_age = 10 ** (m_age @ np.log10(ages))                         # mass-weighted (log) age
        mw_z = w.sum(axis=0) @ mets                                     # mass-weighted [M/H]
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
## 7. What pPXF does, by hand

With the kinematics fixed, the problem is **non-negative least squares**: find $w_i \ge 0$ minimising $\|(\mathbf{T} w - F)/\sigma\|^2$, where the columns of $\mathbf{T}$ are the broadened templates. `scipy.optimize.nnls` solves it in one line.
"""),
("code", r"""
g = galaxies['post-starburst']
sel = (g['lam'] > 3800) & (g['lam'] < 7200)
# columns of T: every template, broadened with the true sigma, on the galaxy's pixels
T = np.array([broaden_velocity(templates[:, i, j], velscale, g['sigma'])
              for i in range(ages.size) for j in range(mets.size)]).T
T = np.array([np.interp(np.log(g['lam'][sel]), ln_lam, T[:, k]) for k in range(T.shape[1])]).T
A = T / g['noise'][sel, None]            # divide each row by the noise: chi2 = |A w - b|^2
b = g['flux'][sel] / g['noise'][sel]
w_nnls, _ = nnls(A, b)                   # the whole fit: one line
w_nnls = w_nnls.reshape(ages.size, mets.size); w_nnls /= w_nnls.sum()
print('templates used (weight > 1%):', int((w_nnls > 0.01).sum()), 'of', w_nnls.size)
plt.plot(ages, w_nnls.sum(1), 'o-', label='scipy nnls'); plt.plot(ages, fit(g, regul=0)[1].sum(1), 's--', label='pPXF, regul=0')
plt.xscale('log'); plt.xlabel('age [Gyr]'); plt.ylabel('fraction of mass formed'); plt.legend()
"""),
("md", r"""
## Exercises

1. Lower the S/N of the post-starburst to 15 (`make_galaxy(..., snr=15)`). Is the young burst still found? Its mass? Its age?
2. Make the burst **older** (t = 2 Gyr instead of 0.6 Gyr). Why is it harder to recover? *(Hint: section 1 — which stars make the Balmer lines, and how long do they live?)*
3. Add dust: multiply the galaxy by a smooth slope, `g['flux'] *= (g['lam'] / 5500) ** 0.5`. Fit with `mdegree=0` and `mdegree=8`. What happens?
4. Build templates with a top-heavy or bottom-heavy IMF (`imf.single_power_law`, `imf_params={'alpha': ...}`) and fit the Milky-Way disc. How much does the inferred SFH depend on the IMF you assume?
5. Lecture 2 link: the SFH of the old elliptical gives its star-formation **duration**. Compare with the [Mg/Fe] ≈ +0.3 argument (Slido S2.9).
"""),
]

# ============================================================== 02: open the box
NB02_INSIDE = [
("md", r"""
## 0. Open the box: what `ssp.synthesize(age, met)` actually does

Before using FaSTAR as a black box, we rebuild one SSP **by hand** from its four ingredients and check that we get the same spectrum. The physics is the integral above:

$$F_\lambda(t, Z) = \int \underbrace{\xi(m)}_{\text{IMF}}\; \underbrace{L_\lambda\big(m \mid t, Z\big)}_{\text{star on the isochrone}}\; dm .$$

1. **Isochrone** — which stars are still alive at age $t$, and their $T_\mathrm{eff}$, $\log g$, luminosity $L$ (BaSTI-IAC isochrones, interpolated in age and [M/H]).
2. **IMF** — how many stars of each initial mass $m$ were born per 1 M$_\odot$ formed (Kroupa: $\xi \propto m^{-1.3}$ below 0.5 M$_\odot$, $m^{-2.3}$ above; normalised so that $\int m\,\xi\,dm = 1$ M$_\odot$ between 0.1 and 100 M$_\odot$).
3. **Stellar spectra** — the *shape* of each star's spectrum from $(T_\mathrm{eff}, \log g, [M/H])$: a neural network trained on the MILES (+BOSZ) stellar libraries returns a spectrum with mean flux 1.
4. **Scaling** — each shape is scaled to the star's true brightness, using its luminosity and a bolometric correction to the V band.

Then the integral over mass is a trapezoid sum along the isochrone.
"""),
("code", r"""
import jax.numpy as jnp
from fastar.interpolate.color import color_interpolation

age, met = 10.0, 0.0      # Gyr, [M/H]

# 1. ISOCHRONE: 2100 points along the isochrone, ordered by initial mass.
#    m = initial mass [Msun], logT = log10(Teff [K]), logg = surface gravity [cgs], logL = log10(L/Lsun)
m, logT, logg, logL = [np.array(x) for x in ssp._get_isochrone(age, met)]
print(f'{m.size} isochrone points, initial masses {m.min():.2f}-{m.max():.3f} Msun (heavier stars are dead)')

# 2. IMF: number of stars per unit initial mass, per 1 Msun formed
xi = np.array(ssp.imf_function(jnp.array(m), {}))

# 3. STELLAR SPECTRA: one normalised spectrum (mean flux 1) per isochrone point -> array (2100, 4300)
feh = jnp.full(m.size, met)
shapes = np.array(ssp.predict_spectrum(jnp.array(logg), jnp.array(logT), feh))

# 4. SCALING to the true brightness of each star:
#    V magnitude the star should have:  M_V = -2.5 log10(L/Lsun) - BC_V + M_V(Sun)
#    V magnitude of the normalised shape: computed by integrating it through the V filter
bc_v = np.array(color_interpolation(jnp.array(logg), jnp.array(logT), feh,
                                    ssp.logg_array, ssp.teff_log10_array, ssp.fmet_array, ssp.bcv_grid))
mv_true = -2.5 * logL - bc_v + float(ssp.sun_vmag)
mv_shape = np.array(ssp._compute_ab_magnitudes(jnp.array(shapes)))
scale = 10 ** (-0.4 * (mv_true - mv_shape))     # flux factor that turns each shape into the real star

# THE INTEGRAL over initial mass: sum of (number of stars) x (spectrum of one star)
my_ssp = np.trapezoid(shapes * (xi * scale)[:, None], m, axis=0)

fastar_ssp = np.array(ssp.synthesize(age=age, met=met))
print('largest relative difference to ssp.synthesize:', f'{np.max(np.abs(my_ssp / fastar_ssp - 1)):.1e}')
"""),
("code", r"""
# WHICH STARS MAKE THE LIGHT? Contribution of each piece of the isochrone to the flux at 5500 A.
i55 = np.argmin(np.abs(wave - 5500))
f55 = shapes[:, i55] * xi * scale                              # flux at 5500 A per unit mass along the isochrone
dF = 0.5 * (f55[1:] + f55[:-1]) * np.diff(m)                   # trapezoid: light from each piece
dN = 0.5 * (xi[1:] + xi[:-1]) * np.diff(m)                     # number of stars in each piece
giant = logg[1:] < 3.5                                          # giants: low surface gravity
print(f'giants (log g < 3.5): {dN[giant].sum() / dN.sum():.2%} of the stars, '
      f'{dF[giant].sum() / dF.sum():.0%} of the V-band light, initial masses {m[1:][giant].min():.3f}-{m[1:][giant].max():.3f} Msun')

fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5))
sc = a1.scatter(logT, logL, c=np.log10(m), s=6, cmap='viridis')
a1.invert_xaxis(); a1.set_xlabel(r'log $T_\mathrm{eff}$'); a1.set_ylabel(r'log $L/L_\odot$')
a1.set_title(f'isochrone, {age} Gyr, [M/H] = {met}'); plt.colorbar(sc, ax=a1, label=r'log initial mass [M$_\odot$]')
a2.plot(np.arange(dF.size), np.cumsum(dF) / dF.sum(), label='cumulative V light')
a2.plot(np.arange(dN.size), np.cumsum(dN) / dN.sum(), label='cumulative number of stars')
a2.set_xlabel('position along the isochrone (point index: main sequence → turnoff → giants)')
a2.set_ylabel('cumulative fraction'); a2.legend()
"""),
("md", r"""
**Read the plot.** Almost all *stars* are faint dwarfs on the lower main sequence, but about half of the *V-band light* comes from giants — stars with initial masses within a few per cent of the turnoff mass. This is why the IMF *shape* barely changes the spectrum (notebook section 4), while it changes the *mass* a lot.

From now on we use `ssp.synthesize(...)`: it does exactly the steps above (plus compiles them with JAX, so it is fast).
"""),
]

# ============================================================== 03 (full)
NB03_FULL = [
("md", r"""
# 03 — A toy model of chemical evolution: the [Mg/Fe] clock

*Lecture 2: chemical evolution*

A **one-zone ("bathtub") model**: one well-mixed reservoir of gas. Gas flows in, stars form from it, dying stars put enriched gas back, a wind blows some gas out. We follow only two elements, **magnesium** and **iron**, because their ratio is a clock:

* **SN II** (core-collapse supernovae of stars with $m > 8\,M_\odot$) explode within ~40 Myr of star formation — essentially *immediately*. Each makes ~0.1 M$_\odot$ of Mg and ~0.07 M$_\odot$ of Fe (more Mg for more massive stars).
* **SN Ia** (thermonuclear explosions of white dwarfs in binaries) explode with a **delay-time distribution** (DTD) $\propto 1/t$, from ~40 Myr to a Hubble time. Each makes ~0.7 M$_\odot$ of Fe and almost no Mg.

So early on, the gas has the SN II ratio (high Mg/Fe: the **plateau**); once SN Ia catch up, Fe rises faster than Mg and [Mg/Fe] falls (the **knee**).

**Notation.** $[X/H] = \log_{10}(X/H) - \log_{10}(X/H)_\odot$ (here with mass fractions), $[\mathrm{Mg/Fe}] = [\mathrm{Mg/H}] - [\mathrm{Fe/H}]$. Solar values: Asplund et al. (2009).

The code is in `stellarpops/toy_gce.py` — about 100 lines, read it! The yields are illustrative; for real models see notebook 04 (galevo).
"""),
("md", r"""
### The equations the code solves (one time step $dt$ = 2 Myr)

| quantity | equation | physics |
|---|---|---|
| star-formation rate | $\psi = M_\mathrm{gas}/\tau_\mathrm{sf}$ (0 after `t_stop`) | linear Schmidt law; $\tau_\mathrm{sf}$ = gas depletion time |
| SN II rate | $R_\mathrm{II} = N_\mathrm{II}\,\psi$ | $N_\mathrm{II} \approx 0.011$ per M$_\odot$ formed (Kroupa IMF, $m > 8$ M$_\odot$); instantaneous |
| SN Ia rate | $R_\mathrm{Ia}(t) = \int_0^t \psi(t')\,\mathrm{DTD}(t - t')\,dt'$ | the past SFR convolved with the DTD; $\int \mathrm{DTD} = N_\mathrm{Ia} = 1.3\times10^{-3}$ per M$_\odot$ (Maoz & Mannucci 2012) |
| gas mass | $\dot M_\mathrm{gas} = \dot M_\mathrm{in} - (1-R)\,\psi - \eta\,\psi$ | infall; locked in long-lived stars ($R = 0.3$ returned at once); wind with mass loading $\eta$ |
| element X (Mg, Fe) | $\dot M_X = -\big[(1-R)\psi + \eta\psi\big] \frac{M_X}{M_\mathrm{gas}} + R_\mathrm{II}\,y^\mathrm{II}_X + R_\mathrm{Ia}\,y^\mathrm{Ia}_X$ | removed with the gas that forms stars / is blown out; added by supernova yields $y$ |

Stars born at time $t$ inherit the gas abundances at $t$. "Stellar [Mg/Fe]" = mass-weighted average over all stars formed so far — roughly what an integrated galaxy spectrum measures.

**Parameters of `run_one_zone`:** `tau_sf` (Gyr; small = efficient), `infall_tau` (Gyr; gas arrives as $e^{-t/\tau}$; `None` = all gas there at $t = 0$, closed box), `eta` (wind mass loading), `t_stop` (Gyr; quench star formation), `alpha_high` (IMF slope above 1 M$_\odot$), `ia` (switch SN Ia on/off).
"""),
("code", SETUP + r"""
from stellarpops import run_one_zone, SOLAR
"""),
("md", r"""
## 1. A Milky-Way-like disc
"""),
("code", r"""
# tau_sf = 2 Gyr: the gas would be used up in ~2 Gyr without infall
# infall_tau = 7 Gyr: fresh (metal-free) gas keeps arriving for ~7 Gyr
# eta = 1: the wind removes as much gas as goes into stars
r = run_one_zone(tau_sf=2.0, infall_tau=7.0, eta=1.0)

fig, axs = plt.subplots(1, 3, figsize=(15, 4.2))
axs[0].plot(r['t'], r['sfr'])                                   # SFR(t) = gas / tau_sf
axs[0].set_xlabel('t [Gyr]'); axs[0].set_ylabel('SFR (arb.)')
axs[1].plot(r['t'], r['rate_ii'], label='SN II (follows the SFR)')
axs[1].plot(r['t'], r['rate_ia'], label='SN Ia (SFR convolved with the DTD)')
axs[1].set_xscale('log'); axs[1].set_xlabel('t [Gyr]'); axs[1].set_ylabel('SN rate (arb.)'); axs[1].legend(fontsize=9)
axs[2].plot(r['FeH'], r['MgFe'])                                # the chemical track of the gas (= newborn stars)
axs[2].set_xlim(-3, 0.5); axs[2].set_xlabel('[Fe/H]'); axs[2].set_ylabel('[Mg/Fe]')
plt.tight_layout()
"""),
("md", r"""
**Questions:** where is the *plateau* and what sets its height? Where is the *knee* and what happens there? (Middle panel: when does the SN Ia rate become comparable to the SN II rate?)
"""),
("md", r"""
## 2. The plateau, from the yields alone

Before any SN Ia explodes, the gas has exactly the Mg/Fe of the SN II ejecta. So the plateau is

$$[\mathrm{Mg/Fe}]_\mathrm{plateau} = \log_{10}\frac{\langle y_\mathrm{Mg}\rangle_\mathrm{II} / \langle y_\mathrm{Fe}\rangle_\mathrm{II}}{(\mathrm{Mg/Fe})_\odot},$$

where $\langle\,\rangle$ is the average over the IMF of stars above 8 M$_\odot$. And if *all* supernovae of a population have exploded (SN II + all SN Ia), the ratio is the total-yield ratio.
"""),
("code", r"""
y = r['yields_ii']                                 # IMF-averaged SN II yields [Msun per SN]
mgfe_sun = SOLAR['Mg'] / SOLAR['Fe']               # solar Mg/Fe mass ratio
print(f"SN II per Msun formed: {r['n_ii']:.4f},  SN Ia per Msun formed: {r['n_ia']:.4f}")
print(f"<y_Mg>_II = {y['Mg']:.3f} Msun,  <y_Fe>_II = {y['Fe']:.3f} Msun")
print(f"plateau:   [Mg/Fe] = log10({y['Mg']:.3f}/{y['Fe']:.3f} / {mgfe_sun:.3f}) = {np.log10(y['Mg'] / y['Fe'] / mgfe_sun):+.2f}")

mg_all = r['n_ii'] * y['Mg'] + r['n_ia'] * 0.02    # SN Ia yields: 0.02 Msun Mg, 0.70 Msun Fe
fe_all = r['n_ii'] * y['Fe'] + r['n_ia'] * 0.70
print(f"all SN II + all SN Ia of one population: [Mg/Fe] = {np.log10(mg_all / fe_all / mgfe_sun):+.2f};"
      f" SN Ia make {r['n_ia'] * 0.70 / fe_all:.0%} of the iron")
"""),
("md", r"""
## 3. Fast vs slow star formation
"""),
("code", r"""
models = {'elliptical: fast, quenched at 0.5 Gyr': dict(tau_sf=0.3, t_stop=0.5, eta=0.5),   # efficient, then stops
          'Milky-Way-like disc': dict(tau_sf=2.0, infall_tau=7.0, eta=1.0),
          'dwarf: slow and leaky': dict(tau_sf=15.0, infall_tau=3.0, eta=10.0)}            # inefficient, strong wind
plt.figure(figsize=(8, 5.5))
for name, p in models.items():
    r = run_one_zone(**p)
    act = r['sfr'] > 0                  # plot only while stars still form (afterwards nobody records the gas)
    plt.plot(r['FeH'][act], r['MgFe'][act], label=name)
    # star_FeH / star_MgFe: mass-weighted averages over ALL stars formed (what a spectrum of the galaxy sees)
    print(f"{name:40s} mass-weighted stellar [Fe/H] = {r['star_FeH'][-1]:+.2f}, [Mg/Fe] = {r['star_MgFe'][-1]:+.2f}")
plt.xlim(-3, 0.5); plt.xlabel('[Fe/H]'); plt.ylabel('[Mg/Fe]'); plt.legend()
"""),
("md", r"""
All three start on the same plateau (same IMF, same yields). The **knee** comes at a similar *time* (when SN Ia start, ~0.1–0.3 Gyr) but at very different **[Fe/H]**: the elliptical has already made a lot of iron by then, the dwarf very little. The elliptical stops forming stars before SN Ia dominate, so its stars stay α-rich.

**Your turn:** find a star-formation time scale `tau_sf` and quenching time `t_stop` that give a mass-weighted stellar [Mg/Fe] ≈ +0.3 (a massive elliptical, Thomas et al. 2005). How short must star formation be?
"""),
("code", "# your code here\n"),
("md", r"""
## 4. The IMF moves the plateau

`alpha_high` is the IMF slope above 1 M$_\odot$ (Kroupa = 2.3). In the code it changes (i) the number of SN II per M$_\odot$ formed, (ii) the IMF-averaged SN II yields — more massive progenitors make more Mg per Fe, $y_\mathrm{Mg} \propto m^{1.5}$ here — and (iii) the number of SN Ia progenitors (3–8 M$_\odot$).
"""),
("code", r"""
plt.figure(figsize=(8, 5.5))
for a in [1.9, 2.3, 2.7]:
    r = run_one_zone(tau_sf=2.0, infall_tau=7.0, eta=1.0, alpha_high=a)
    y = r['yields_ii']
    plt.plot(r['FeH'], r['MgFe'], label=f"α = {a}:  N_II = {r['n_ii']:.3f}/Msun, <y_Mg/y_Fe>_II = {y['Mg'] / y['Fe']:.2f}")
plt.xlim(-3, 0.5); plt.xlabel('[Fe/H]'); plt.ylabel('[Mg/Fe]'); plt.legend(fontsize=9)
"""),
("md", r"""
**The degeneracy:** a high [Mg/Fe] can mean *fast* star formation **or** a *top-heavy* IMF. How could you tell them apart? (Hints: metallicity, other elements, the mass-to-light ratio from notebook 02.)

## 5. Bonus: the kitchen game, a round-by-round version of the Galaxy clock
In class we played the *Galaxy clock* on the games page (azeret.github.io/stellar-populations-lectures, tab 2). This kitchen is the same physics in 8 coarse rounds, with picky customers.

**Kitchen rules (same as on paper):** you have **8 units** of star formation to spend over **8 rounds** (1 round ≈ 250 Myr).
Each unit makes **3 Mg + 1 Fe at once** (SN II) and books SN Ia iron for later: **+1 Fe** one round later, **+1** two rounds later, **+1** four rounds later (a coarse $1/t$ DTD).
The stars formed in a round get the [Mg/Fe] of the pot at that moment, so what the customer receives is the mass-weighted [Mg/Fe] of all your stars.
In these units the pot's [Mg/Fe] = log10(Mg/Fe): pure SN II gives log10(3) = +0.48 — the plateau.

Run the next cell once, then try to fill the four orders below (the recipes given are starting guesses that fail). One order is impossible in this kitchen: find out which and **why**. In class: first team to fill A–C wins; lowest [Mg/Fe] for order B goes on the board.
"""),
]
NB03_FULL += [c for c in []]   # the kitchen cells are appended in build_notebooks.py

# ============================================================== 04 (full)
NB04_FULL = [
("md", r"""
# 04 — Real chemical evolution with galevo (GalIMF)

*Lecture 2: chemical evolution*

**galevo** is the galaxy chemical-evolution module of the open-source **GalIMF** code (Yan, Jeřábková & Kroupa 2017; Yan et al. 2019): https://github.com/Azeret/galIMF

### What galevo does that the toy model does not

| | toy model (notebook 03) | galevo |
|---|---|---|
| stellar lifetimes | SN II instantly, everything else ignored | mass- and metallicity-dependent lifetimes: every star returns its gas when it dies |
| yields | 2 elements, fixed numbers | H, He, C, N, O, Ne, Mg, Si, S, Ca, Fe; metallicity-dependent yields of massive and intermediate-mass stars (Portinari et al. 1998), SN Ia yields (Thielemann et al. 1993) |
| SN Ia | $1/t$ DTD, fixed number | $1/t$ DTD after 40 Myr, normalised to the observed rate (Maoz & Mannucci 2012), scaled with the number of 1.5–8 M$_\odot$ progenitors of the actual IMF |
| IMF | fixed (slope can be changed) | fixed (Kroupa) **or** the **IGIMF**: a galaxy-wide IMF computed every 10 Myr from the star-formation rate |
| time step | 2 Myr | star formation in 10 Myr epochs; enrichment followed with 1 Myr resolution early on |

### The IGIMF in two sentences
Stars form in embedded clusters; the most massive cluster a galaxy can form grows with its SFR, and the most massive star a cluster can form grows with the cluster mass. Adding up the IMFs of all clusters gives a galaxy-wide IMF that is **top-light** at low SFR and **top-heavy** at high SFR (Kroupa & Weidner 2003; Jeřábková et al. 2018).

### The experiment
Three galaxies form the **same total stellar mass** ($3\times10^9\,M_\odot$) with a flat star-formation history lasting **30 Myr, 300 Myr or 3 Gyr** — the SFR is 100, 10 or 1 M$_\odot$/yr. Same mass, different tempo: what happens to [Mg/Fe]?

⏱ A run takes from ~30 s (30 Myr) to tens of minutes (3 Gyr). Pre-computed results are in `../data/galevo_runs/` (made with `../data/run_galevo.py`), so you can plot first and run later.
"""),
("code", SETUP),
("md", r"""
## 1. Plot the pre-computed runs

Each `.npz` file holds the arrays galevo produces (one value per output time):
* `time_axis` — log10(time / yr)
* `Fe_over_H_list`, `Mg_over_Fe_list` — [Fe/H] and [Mg/Fe] of the **gas** (= of the stars being born at that moment)
* `stellar_Fe_over_H_list`, `stellar_Mg_over_Fe_list` — mass-weighted averages over **all stars formed so far** (what an integrated spectrum measures)
* `total_star_formed` — cumulative stellar mass formed [M$_\odot$]
"""),
("code", r"""
import glob
runs = {os.path.basename(f)[:-4]: np.load(f) for f in sorted(glob.glob('../data/galevo_runs/*.npz'))}
# K_ = Kroupa IMF, I_ = IGIMF;  fast / mid / slow = 30 Myr / 300 Myr / 3 Gyr of star formation
names = {'K_fast': 'Kroupa IMF, 30 Myr', 'K_mid': 'Kroupa IMF, 300 Myr', 'K_slow': 'Kroupa IMF, 3 Gyr',
         'I_fast': 'IGIMF, 30 Myr', 'I_mid': 'IGIMF, 300 Myr', 'I_slow': 'IGIMF, 3 Gyr'}
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
for k, d in runs.items():
    ls = '--' if k.startswith('I') else '-'          # dashed: IGIMF
    t = 10 ** d['time_axis'] / 1e9                   # time in Gyr
    ok = d['Fe_over_H_list'] > -5                     # skip the first, metal-free steps
    ax1.plot(d['Fe_over_H_list'][ok], d['Mg_over_Fe_list'][ok], ls, label=names.get(k, k))
    ax2.plot(t[ok], d['Mg_over_Fe_list'][ok], ls, label=names.get(k, k))
ax1.set_xlabel('gas [Fe/H]'); ax1.set_ylabel('gas [Mg/Fe]'); ax1.set_xlim(-4, 0.5); ax1.legend(fontsize=9)
ax2.set_xscale('log'); ax2.set_xlabel('time [Gyr]'); ax2.set_ylabel('gas [Mg/Fe]')
for k, d in runs.items():
    print(f"{names.get(k, k):22s} final mass-weighted stellar [Fe/H] = {d['stellar_Fe_over_H_list'][-1]:+.2f}, "
          f"[Mg/Fe] = {d['stellar_Mg_over_Fe_list'][-1]:+.2f},  stars formed = {np.ravel(d['total_star_formed'])[-1]:.1e} Msun")
"""),
("md", r"""
**How to read it.** Left: the gas track in the [Mg/Fe]–[Fe/H] plane (the toy model's diagram). Right: the same against time — the knee is a *time*, set by when SN Ia start to matter; where it falls in [Fe/H] depends on how much iron was made before then (i.e. on the SFR).

**Questions**
1. Rank the three Kroupa-IMF galaxies by the [Mg/Fe] of their stars. Does it match the toy model (notebook 03, section 6) and the Slido answer S2.7?
2. Why does the gas [Mg/Fe] keep falling after star formation has stopped? (Who is still exploding?)
3. Compare Kroupa and IGIMF for the fast galaxy (SFR = 100 M$_\odot$/yr). Why does a high star-formation rate make the IGIMF top-heavy, and what does that do to [Mg/Fe] and [Fe/H]?
"""),
("md", r"""
## 2. Run galevo yourself

This clones GalIMF next to the repository (once) and runs one model. The two steps are:

1. `generate_SFH('flat', log_SFR, SFEN, ...)` writes `SFH.txt`: one line per 10 Myr epoch with the SFR in M$_\odot$/yr — here `SFEN` epochs at $10^{\mathrm{log\_SFR}}$ M$_\odot$/yr, then zeros up to 13 Gyr.
2. `galaxy_evol(...)` evolves the galaxy. The arguments we use:

| argument | value | meaning |
|---|---|---|
| `imf` | `'Kroupa'` or `'igimf'` | fixed canonical IMF, or the SFR-dependent galaxy-wide IMF |
| `STF` | 0.3 | star-transformation fraction: total stars formed / initial gas mass (sets the gas reservoir; closed box) |
| `SFEN` | e.g. 3 | number of 10 Myr star-formation epochs (must match the SFH) |
| `Z_0` | 1.9×10⁻⁸ | initial metallicity of the gas (≈ primordial) |
| `solar_mass_component` | `'Anders1989_mass'` | solar abundances used for the bracket notation |
| `str_yield_table` | `'portinari98'` | stellar yields of massive and intermediate-mass stars |
| `steller_mass_upper_bound` | 150 | most massive star allowed [M$_\odot$] |
| `time_resolution_in_Myr` | 1 | time step of the enrichment calculation |
| `SNIa_ON` | `True` | switch SN Ia on (try `False`: the plateau never ends!) |
| `mass_boundary_observe_low/up` | 1.5, 8 | kept at the default values |
| `SFH_model` | `'provided'` | read the SFH from `SFH.txt` |

Change `log_SFR` and `SFEN` together, keeping `log_SFR + log10(SFEN)` fixed, to keep the total mass the same.
"""),
("code", r"""
import subprocess
here = os.getcwd()
gal = os.path.abspath('../../galIMF')
if not os.path.isdir(gal):                     # clone GalIMF once (needs internet)
    subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/Azeret/galIMF.git', gal], check=True)
os.chdir(gal); sys.path.insert(0, gal)         # galevo reads/writes its tables relative to its own folder
import galevo

log_SFR, SFEN, IMF = 2.0, 3, 'Kroupa'          # 100 Msun/yr for 3 x 10 Myr = 3e9 Msun. Try IMF = 'igimf'
galevo.generate_SFH('flat', log_SFR, SFEN, 0, 10, 0)   # the last three numbers are only used by other SFH shapes
galevo.galaxy_evol(imf=IMF, STF=0.3, SFEN=SFEN, Z_0=0.00000001886, solar_mass_component='Anders1989_mass',
                   str_yield_table='portinari98', IMF_name='Kroupa', steller_mass_upper_bound=150,
                   time_resolution_in_Myr=1, mass_boundary_observe_low=1.5, mass_boundary_observe_up=8,
                   SFH_model='provided', SNIa_ON=True, high_time_resolution=None,
                   plot_show=None, plot_save=None, outflow=None, check_igimf=False)
os.chdir(here)

# galevo keeps its results as module-level lists
plt.figure(figsize=(7, 5))
ok = np.array(galevo.Fe_over_H_list) > -5
plt.plot(np.array(galevo.Fe_over_H_list)[ok], np.array(galevo.Mg_over_Fe_list)[ok])
plt.xlabel('gas [Fe/H]'); plt.ylabel('gas [Mg/Fe]')
print('final gas [Fe/H] = %.2f, [Mg/Fe] = %.2f' % (galevo.Fe_over_H_list[-1], galevo.Mg_over_Fe_list[-1]))
"""),
]
