"""Builds the four student notebooks into repo/notebooks/."""
import nbformat as nbf
import os

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)


def nb(cells):
    n = nbf.v4.new_notebook()
    n.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    out = []
    for kind, src in cells:
        out.append(nbf.v4.new_markdown_cell(src.strip()) if kind == "md" else nbf.v4.new_code_cell(src.strip()))
    n.cells = out
    return n


SETUP = """
import sys, os
sys.path.insert(0, os.path.abspath('..'))   # makes the small 'stellarpops' package importable
import numpy as np
import matplotlib.pyplot as plt
from stellarpops.style import use_slide_style
use_slide_style(dark=False, scale=0.7)       # dark=True gives the lecture-slide look
"""

# ----------------------------------------------------------------------------- 01
nb01 = nb([
("md", """
# 01 — The stellar initial mass function (IMF)

*Galaxies course, Masaryk University — Lecture 1: stellar populations and the IMF*

The IMF $\\xi(m) = dN/dm$ tells us how many stars are born per unit mass interval. We write it as (multi-)power laws
$\\xi(m) \\propto m^{-\\alpha}$:

| IMF | slopes |
|---|---|
| Salpeter (1955) | $\\alpha = 2.35$ for all masses |
| Kroupa (2001) | $\\alpha_1 = 1.3$ for $0.08$–$0.5\\,M_\\odot$, $\\alpha_2 = 2.3$ above |

Remember: the IMF is not observed directly. It is a statistical construct (a *Hilfskonstrukt*) inferred from star counts after many corrections.

In this notebook you will **draw stars from the IMF**, see where the **number, mass and light** of a population sit, and find out why the **most massive star depends on the size of the cluster**.
"""),
("code", SETUP + "\nfrom stellarpops import sample_imf, kroupa_xi, number_fraction, mass_fraction\nfrom stellarpops.imf import powerlaw_imf_xi, KROUPA, SALPETER"),
("md", "## 1. Plot the IMF\nPlotting $\\xi(m)$ on log–log axes turns power laws into straight lines."),
("code", """
m = np.geomspace(0.08, 150, 500)
xi_k = powerlaw_imf_xi(m, **KROUPA)
xi_s = powerlaw_imf_xi(m, breaks=[0.08, 150], alphas=[2.35])
# normalise both to 1 Msun of stars formed
xi_k /= np.trapezoid(xi_k * m, m); xi_s /= np.trapezoid(xi_s * m, m)

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(m, xi_k, label='Kroupa (2001)')
ax.loglog(m, xi_s, '--', label='Salpeter (1955)')
ax.set_xlabel(r'$m$ [M$_\\odot$]'); ax.set_ylabel(r'$\\xi(m)$ per M$_\\odot$ formed'); ax.legend()
"""),
("md", "**Question:** where do the two IMFs differ, and by how much? Why was this region the hardest to measure for Salpeter in 1955?"),
("md", "## 2. Draw a star cluster (the dice game, in code)\n`sample_imf(N)` draws `N` random stellar masses from the IMF."),
("code", """
rng = np.random.default_rng(1)
for N in [30, 300, 3000, 30000]:
    stars = sample_imf(N, rng=rng)
    print(f"N = {N:6d}:  total mass = {stars.sum():8.1f} Msun,  most massive = {stars.max():6.1f} Msun,  stars > 8 Msun: {(stars > 8).sum()}")
"""),
("code", """
stars = sample_imf(3000, rng=2)
bins = np.geomspace(0.08, 150, 25)
plt.figure(figsize=(7, 5))
plt.hist(stars, bins=bins, histtype='stepfilled', alpha=0.6, label='3000 random stars')
plt.xscale('log'); plt.yscale('log'); plt.xlabel(r'$m$ [M$_\\odot$]'); plt.ylabel('number per bin'); plt.legend()
"""),
("md", "## 3. Where are the stars, the mass and the light?\nFor a Kroupa IMF at birth (zero-age main sequence). For the light we use a textbook piecewise main-sequence mass–luminosity relation: $L \\approx 0.23\\,m^{2.3}$ ($m<0.43$), $m^4$ ($0.43$–$2$), $1.4\\,m^{3.5}$ ($2$–$55$), $32000\\,m$ ($>55$), in solar units — good enough for a feeling, not for research."),
("code", """
edges = [0.08, 0.5, 1, 8, 150]
labels = ['0.08–0.5', '0.5–1', '1–8', '8–150']
num = [number_fraction(a, b) for a, b in zip(edges[:-1], edges[1:])]
mas = [mass_fraction(a, b) for a, b in zip(edges[:-1], edges[1:])]
mm = np.geomspace(0.08, 150, 4000); w = kroupa_xi(mm)
L = np.where(mm < 0.43, 0.23 * mm**2.3, np.where(mm < 2, mm**4, np.where(mm < 55, 1.4 * mm**3.5, 32000 * mm)))
lum = [np.trapezoid((w * L)[(mm >= a) & (mm < b)], mm[(mm >= a) & (mm < b)]) for a, b in zip(edges[:-1], edges[1:])]
lum = np.array(lum) / np.sum(lum)

x = np.arange(4); fig, ax = plt.subplots(figsize=(8, 5))
for i, (vals, name) in enumerate([(num, 'number'), (mas, 'mass'), (lum, 'light (at birth)')]):
    ax.bar(x + (i - 1) * 0.27, np.array(vals) * 100, width=0.27, label=name)
ax.set_xticks(x, labels); ax.set_xlabel(r'mass range [M$_\\odot$]'); ax.set_ylabel('% of total'); ax.legend()
for l, n, s, L in zip(labels, num, mas, lum):
    print(f"{l:>9} Msun:  {100*n:5.1f}% of stars, {100*s:5.1f}% of mass, {100*L:6.2f}% of light")
"""),
("md", """
**Questions**
1. Which stars dominate the *number*, which the *mass*, which the *light*?
2. A galaxy is 10 Gyr old. Stars above ~1 M$_\\odot$ have died. Who dominates its light now? (Hint: think of red giants.)
3. Why does this make measuring the low-mass IMF of a distant galaxy so hard?
"""),
("md", "## 4. Your turn: the most massive star vs the cluster mass\nDraw many clusters of different sizes and plot $m_{\\max}$ against the cluster mass $M_{\\rm cl}$. Is there a relation? (Observed young clusters follow a $m_{\\max}$–$M_{\\rm cl}$ relation, Weidner & Kroupa 2006 — is pure random sampling enough to explain it? This question is still debated.)"),
("code", """
Mcl, mmax = [], []
for N in np.geomspace(10, 30000, 300).astype(int):
    s = sample_imf(N)
    Mcl.append(s.sum()); mmax.append(s.max())
plt.figure(figsize=(7, 5))
plt.loglog(Mcl, mmax, '.', alpha=0.6)
plt.xlabel(r'cluster mass $M_{\\rm cl}$ [M$_\\odot$]'); plt.ylabel(r'$m_{\\max}$ [M$_\\odot$]')
"""),
("md", "**Extra:** change the IMF to a top-heavy one (`kroupa_xi` / `powerlaw_imf_xi` with a flatter high-mass slope, e.g. `alphas=[1.3, 1.9]`) and redo sections 3 and 4. What changes?"),
])

# ----------------------------------------------------------------------------- 02
nb02 = nb([
("md", """
# 02 — Simple stellar populations with FaSTAR

*Lecture 1: stellar populations and the IMF*

A **simple stellar population (SSP)** is a group of stars born at the same time with the same chemistry. Its spectrum is

$$F_\\lambda(t, Z) = \\int_{m_{\\min}}^{m_{\\rm TO}(t)} \\xi(m)\\, f_\\lambda\\big(m, t, Z\\big)\\, dm ,$$

i.e. the IMF $\\xi(m)$ weights the spectra $f_\\lambda$ of the stars that are still alive on the isochrone.

We use **FaSTAR** (Martín-Navarro et al. 2026, A&A 711, A282 and A283), a fast, differentiable SSP code:
`pip install fastar-astro` — docs: https://fastar.readthedocs.io

Valid range: ages 0.02–14 Gyr, [M/H] from −2.5 to +0.3. The first call takes ~10 s (it loads a neural network); afterwards a spectrum takes ~1 s.
"""),
("code", SETUP + "\nfrom fastar import IntegratedSSPSynthesizer, SemiresolvedSSPSynthesizer, imf\nfrom stellarpops.remnants import living_plus_remnant_mass\nfrom stellarpops import kroupa_xi\n\nssp = IntegratedSSPSynthesizer(imf_function=imf.kroupa)\nwave = np.array(ssp.wave)\n\ndef norm(s, lo=5400, hi=5600):\n    s = np.array(s); sel = (wave > lo) & (wave < hi)\n    return s / np.median(s[sel])"),
("md", "## 1. Age\nSame IMF, same metallicity, different ages. Prediction first: what happens to the blue part of the spectrum and to the total brightness?"),
("code", """
fig, ax = plt.subplots(figsize=(10, 5))
for age in [0.05, 0.3, 1, 3, 10]:
    ax.plot(wave, np.array(ssp.synthesize(age=age, met=0.0)), lw=1, label=f'{age} Gyr')
ax.set_yscale('log'); ax.set_xlabel('wavelength [Å]'); ax.set_ylabel(r'flux per M$_\\odot$ formed'); ax.legend()
"""),
("md", "## 2. Mass-to-light ratio\nFaSTAR gives the luminosity per solar mass *formed*. We add up the mass still in living stars and remnants (white dwarfs, neutron stars, black holes) to get the usual $M_*/L_V$."),
("code", """
ages = np.geomspace(0.03, 13, 15)
ml = [float(ssp.mass_to_light_ratio(age=a, met=0.0)['total']) * living_plus_remnant_mass(a, kroupa_xi) for a in ages]
plt.figure(figsize=(7, 5)); plt.loglog(ages, ml, 'o-')
plt.xlabel('age [Gyr]'); plt.ylabel(r'$M_*/L_V$ (stars + remnants)')
"""),
("md", "**Question:** you measure the V-band luminosity of a galaxy. How wrong is its stellar mass if you assume 10 Gyr but it is really 1 Gyr old?"),
("md", "## 3. Metallicity\nSame age (10 Gyr), different [M/H]. Look at the Mg b lines (~5175 Å) and the overall slope."),
("code", """
fig, ax = plt.subplots(figsize=(10, 5))
for met in [-2.0, -1.0, 0.0, 0.25]:
    ax.plot(wave, norm(ssp.synthesize(age=10.0, met=met)), lw=1, label=f'[M/H] = {met:+.2f}')
ax.set_xlabel('wavelength [Å]'); ax.set_ylabel('normalised flux'); ax.legend()
"""),
("md", "**Your turn — the age–metallicity degeneracy:** find a *younger, more metal-rich* population whose spectrum shape (normalised) looks similar to a 10 Gyr, [M/H] = −0.5 one. Worthey's (1994) \"3/2 rule\": a population 3× older looks almost the same as one 2× more metal-rich, i.e. Δlog t ≈ −(3/2) Δlog Z along lines of constant colour."),
("code", "# your code here\n"),
("md", "## 4. The IMF\nNow vary the slope of a single power law (Salpeter = 2.35). Compare the spectra *and* the mass-to-light ratios."),
("code", """
spl = IntegratedSSPSynthesizer(imf_function=imf.single_power_law)
alphas = np.linspace(1.3, 3.3, 11)
ml_a, specs = [], []
for a in alphas:
    p = {'alpha': float(a)}
    specs.append(norm(spl.synthesize(age=10.0, met=0.0, imf_params=p), 6000, 6200))
    xi = lambda m, a=a: np.asarray(m) ** (-a)
    ml_a.append(float(spl.mass_to_light_ratio(age=10.0, met=0.0, imf_params=p)['total']) * living_plus_remnant_mass(10.0, xi))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
ref = specs[5]   # alpha = 2.3
for a, s in zip(alphas[::2], specs[::2]):
    ax1.plot(wave, s / ref, lw=1, label=f'α = {a:.1f}')
ax1.set_ylim(0.85, 1.15); ax1.set_xlabel('wavelength [Å]'); ax1.set_ylabel('spectrum / α=2.3'); ax1.legend(fontsize=9)
ax2.plot(alphas, ml_a, 'o-'); ax2.set_xlabel('IMF slope α'); ax2.set_ylabel(r'$M_*/L_V$ at 10 Gyr')
"""),
("md", """
**Questions**
1. Why is the M/L high for *both* very flat and very steep IMFs? (Which kind of object carries the mass in each case?)
2. The spectrum changes by only a few per cent. Which features change? Why are Na D and TiO sensitive to low-mass dwarfs?
3. Compare: changing α from 2.3 to 3.0 changes the spectrum by ~2–5 %, but the mass by a factor ~2. What does this mean for measuring galaxy masses?
"""),
("md", "## 5. Few stars: stochastic sampling\nA real star cluster or a small patch of a galaxy has a *finite* number of stars. FaSTAR's semi-resolved models draw them randomly. (Memory grows with the number of stars: keep it ≤ 5000 on a laptop.)"),
("code", """
import jax
semi = SemiresolvedSSPSynthesizer(imf_function=imf.kroupa)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(wave, norm(ssp.synthesize(age=0.1, met=0.0)), 'k--', lw=2, label='infinitely many stars')
for i, key in enumerate(jax.random.split(jax.random.PRNGKey(0), 5)):
    s, mass = semi.synthesize(age=0.1, met=0.0, num_stars=300, key=key)
    ax.plot(wave, norm(s), lw=1, label=f'300 stars, draw {i+1}')
ax.set_xlabel('wavelength [Å]'); ax.set_ylabel('normalised flux'); ax.legend(fontsize=9)
"""),
("md", "**Your turn:** repeat for 30 and 3000 stars, and for an old (10 Gyr) population. When can you trust an SSP fit to a small cluster?"),
])

# ----------------------------------------------------------------------------- 03
nb03 = nb([
("md", """
# 03 — A toy model of chemical evolution: the [Mg/Fe] clock

*Lecture 2: chemical evolution*

A **one-zone ("bathtub") model**: gas flows in, stars form, massive stars return enriched gas, a wind blows some gas out.
We follow only magnesium and iron:

* **SN II** (core collapse, $m > 8\\,M_\\odot$) explode within ~40 Myr: lots of **Mg**, some Fe.
* **SN Ia** (white dwarfs in binaries) explode with a delay-time distribution $\\propto 1/t$ after ~40 Myr: mostly **Fe**.

Notation: $[X/H] = \\log_{10}(X/H) - \\log_{10}(X/H)_\\odot$ and $[\\mathrm{Mg/Fe}] = [\\mathrm{Mg/H}] - [\\mathrm{Fe/H}]$.

The code is in `stellarpops/toy_gce.py` — about 100 lines, read it! The yields are illustrative; for real models see notebook 04 (galevo).
"""),
("code", SETUP + "\nfrom stellarpops import run_one_zone"),
("md", "## 1. A Milky-Way-like disc"),
("code", """
r = run_one_zone(tau_sf=2.0, infall_tau=7.0, eta=1.0)
fig, axs = plt.subplots(1, 3, figsize=(15, 4.2))
axs[0].plot(r['t'], r['sfr']); axs[0].set_xlabel('t [Gyr]'); axs[0].set_ylabel('SFR (arb.)')
axs[1].plot(r['t'], r['rate_ii'], label='SN II'); axs[1].plot(r['t'], r['rate_ia'], label='SN Ia')
axs[1].set_xscale('log'); axs[1].set_xlabel('t [Gyr]'); axs[1].set_ylabel('SN rate (arb.)'); axs[1].legend()
axs[2].plot(r['FeH'], r['MgFe']); axs[2].set_xlim(-3, 0.5); axs[2].set_xlabel('[Fe/H]'); axs[2].set_ylabel('[Mg/Fe]')
plt.tight_layout()
"""),
("md", "**Questions:** where is the *plateau* and what sets its height? Where is the *knee* and what happens there?"),
("md", "## 2. Fast vs slow star formation"),
("code", """
models = {'elliptical: fast, quenched at 0.5 Gyr': dict(tau_sf=0.3, t_stop=0.5, eta=0.5),
          'Milky-Way-like disc': dict(tau_sf=2.0, infall_tau=7.0, eta=1.0),
          'dwarf: slow and leaky': dict(tau_sf=15.0, infall_tau=3.0, eta=10.0)}
plt.figure(figsize=(8, 5.5))
for name, p in models.items():
    r = run_one_zone(**p)
    act = r['sfr'] > 0                  # only while stars still form
    plt.plot(r['FeH'][act], r['MgFe'][act], label=name)
    print(f"{name:40s} mass-weighted stellar [Fe/H] = {r['star_FeH'][-1]:+.2f}, [Mg/Fe] = {r['star_MgFe'][-1]:+.2f}")
plt.xlim(-3, 0.5); plt.xlabel('[Fe/H]'); plt.ylabel('[Mg/Fe]'); plt.legend()
"""),
("md", "**Your turn:** find a star-formation time scale `tau_sf` and quenching time `t_stop` that give a mass-weighted stellar [Mg/Fe] ≈ +0.3 (a massive elliptical, Thomas et al. 2005). How short must star formation be?"),
("code", "# your code here\n"),
("md", "## 3. The IMF moves the plateau\n`alpha_high` is the IMF slope above 1 M$_\\odot$ (Kroupa = 2.3). More massive SN II progenitors produce more Mg per Fe."),
("code", """
plt.figure(figsize=(8, 5.5))
for a in [1.9, 2.3, 2.7]:
    r = run_one_zone(tau_sf=2.0, infall_tau=7.0, eta=1.0, alpha_high=a)
    plt.plot(r['FeH'], r['MgFe'], label=f'α = {a}')
plt.xlim(-3, 0.5); plt.xlabel('[Fe/H]'); plt.ylabel('[Mg/Fe]'); plt.legend()
"""),
("md", """
**The degeneracy:** a high [Mg/Fe] can mean *fast* star formation **or** a *top-heavy* IMF. How could you tell them apart? (Hints: metallicity, other elements, the mass-to-light ratio from notebook 02.)

## 4. Galaxy chef: the cosmic-kitchen game, now with orders to fill
In the lecture you played one recipe on paper. Here you are the chef and the customers are picky.

**Kitchen rules (same as on paper):** you have **8 units** of star formation to spend over **8 rounds** (1 round ≈ 250 Myr).
Each unit makes **3 Mg + 1 Fe at once** (SN II) and books SN Ia iron for later: **+1 Fe** one round later, **+1** two rounds later, **+1** four rounds later.
The stars formed in a round get the [Mg/Fe] of the pot at that moment, so what the customer receives is the mass-weighted [Mg/Fe] of all your stars.

Run the next cell once, then try to fill the four orders below (the recipes given are starting guesses that fail). One order is impossible in this kitchen: find out which and **why**. In class: first team to fill A–C wins; lowest [Mg/Fe] for order B goes on the board.
"""),
("code", """
def kitchen(recipe, mg_per_unit=3, rounds=8, show=True):
    \"\"\"Play a recipe = list of star-formation units per round. Returns the stars' mass-weighted [Mg/Fe].\"\"\"
    recipe = list(recipe) + [0] * (rounds - len(recipe))
    mg = fe = 0.0
    due = np.zeros(rounds + 10)
    star_units, star_ratio = [], []
    if show:
        print('round  units   Mg    Fe   pot [Mg/Fe]')
    for r in range(rounds):
        fe += due[r]                         # 1. SN Ia deliveries
        u = recipe[r]
        mg += mg_per_unit * u; fe += u       # 2. form stars -> SN II at once
        for delay in (1, 2, 4):              #    ... and book their SN Ia
            due[r + delay] += u
        ratio = mg / fe if fe > 0 else np.nan
        if u > 0:
            star_units.append(u); star_ratio.append(ratio)
        if show:
            print(f'{r+1:5d} {u:6d} {mg:5.0f} {fe:5.0f}   {np.log10(ratio):+.2f}' if fe > 0 else f'{r+1:5d} {u:6d}   (empty pot)')
    if not star_units:
        return np.nan
    stars = np.log10(np.average(star_ratio, weights=star_units))
    if show:
        print(f'-> your stars: [Mg/Fe] = {stars:+.2f}')
    return stars


ORDERS = {
    'A. Giant elliptical': ('all 8 units used, stars [Mg/Fe] >= +0.42',
                            lambda rec, x: sum(rec) == 8 and x >= 0.42),
    'B. Milky-Way disc':   ('all 8 units, star formation in at least 6 rounds, stars [Mg/Fe] <= +0.17 (the steady 1-per-round recipe gives +0.18: beat it)',
                            lambda rec, x: sum(rec) == 8 and sum(u > 0 for u in rec) >= 6 and x <= 0.17),
    'C. Iron-rich today':  ('all 8 units, some stars form in round 8, and those round-8 stars have [Mg/Fe] <= 0',
                            None),   # checked below: needs the pot of round 8
    'D. Super-alpha':      ('all 8 units used, stars [Mg/Fe] >= +0.55',
                            lambda rec, x: sum(rec) == 8 and x >= 0.55),
}


def serve(order, recipe, mg_per_unit=3):
    rec = list(recipe) + [0] * (8 - len(recipe))
    text, check = ORDERS[order]
    print(f'ORDER {order}: {text}')
    x = kitchen(rec, mg_per_unit=mg_per_unit)
    if check is None:     # order C: look at the pot when the round-8 stars form
        mg = fe = 0.0; due = np.zeros(20)
        for r in range(8):
            fe += due[r]; mg += mg_per_unit * rec[r]; fe += rec[r]
            for d in (1, 2, 4): due[r + d] += rec[r]
        ok = sum(rec) == 8 and rec[7] > 0 and np.log10(mg / fe) <= 0
    else:
        ok = check(rec, x)
    print('ORDER FILLED \u2705' if ok else 'Customer sends it back \u274c  - try again')


for name, (text, _) in ORDERS.items():
    print(f'{name}: {text}')
"""),
("code", """
# Your turn: change the recipes until every order you think is possible is filled.
serve('A. Giant elliptical', [4, 4, 0, 0, 0, 0, 0, 0])
"""),
("code", """
serve('B. Milky-Way disc', [1, 1, 1, 1, 1, 1, 1, 1])
"""),
("code", """
serve('C. Iron-rich today', [0, 0, 0, 0, 0, 0, 0, 8])
"""),
("md", """
**Order D.** Try any recipe you like for the super-alpha galaxy. When you are convinced it cannot be done with this kitchen, explain why in one sentence — what sets the ceiling?

Then change the *kitchen*, not the recipe: a top-heavy IMF means more very massive SN II, i.e. more Mg per unit. Try `serve('D. Super-alpha', your_recipe, mg_per_unit=4)`.
This is the degeneracy from the lecture: a high [Mg/Fe] can mean *fast* star formation **or** a *top-heavy* IMF.

**Order C:** why does putting all 8 units into round 8 fail, even though that is the latest possible moment? What do you need to do earlier, and why?
"""),
("code", """
serve('D. Super-alpha', [8], mg_per_unit=3)
"""),
])

# ----------------------------------------------------------------------------- 04
nb04 = nb([
("md", """
# 04 — Real chemical evolution with galevo (GalIMF)

*Lecture 2: chemical evolution*

**galevo** is the galaxy chemical-evolution module of the open-source **GalIMF** code (Yan, Jeřábková & Kroupa 2017; Yan et al. 2019):
https://github.com/Azeret/galIMF

Compared with the toy model it follows stellar lifetimes, metallicity-dependent yields of many elements, SN Ia from a delay-time distribution — and it can use a **variable, galaxy-wide IMF** computed from the IGIMF theory (`imf='igimf'`), which becomes top-heavy at high star-formation rates.

We compare three galaxies that form the **same total stellar mass** ($3\\times10^9\\,M_\\odot$) with a flat star-formation history lasting 30 Myr, 300 Myr or 3 Gyr.

⏱ A run takes from ~30 s (30 Myr) to tens of minutes (3 Gyr). Pre-computed results are in `../data/galevo_runs/`, so you can plot first and run later.
"""),
("code", SETUP),
("md", "## 1. Plot the pre-computed runs"),
("code", """
import glob
runs = {os.path.basename(f)[:-4]: np.load(f) for f in sorted(glob.glob('../data/galevo_runs/*.npz'))}
names = {'K_fast': 'Kroupa IMF, 30 Myr', 'K_mid': 'Kroupa IMF, 300 Myr', 'K_slow': 'Kroupa IMF, 3 Gyr',
         'I_fast': 'IGIMF, 30 Myr', 'I_mid': 'IGIMF, 300 Myr', 'I_slow': 'IGIMF, 3 Gyr'}
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
for k, d in runs.items():
    ls = '--' if k.startswith('I') else '-'
    t = 10 ** d['time_axis'] / 1e9
    ok = d['Fe_over_H_list'] > -5
    ax1.plot(d['Fe_over_H_list'][ok], d['Mg_over_Fe_list'][ok], ls, label=names.get(k, k))
    ax2.plot(t[ok], d['Mg_over_Fe_list'][ok], ls, label=names.get(k, k))
ax1.set_xlabel('gas [Fe/H]'); ax1.set_ylabel('gas [Mg/Fe]'); ax1.set_xlim(-4, 0.5); ax1.legend(fontsize=9)
ax2.set_xscale('log'); ax2.set_xlabel('time [Gyr]'); ax2.set_ylabel('gas [Mg/Fe]')
for k, d in runs.items():
    print(f"{names.get(k, k):22s} final mass-weighted stellar [Fe/H] = {d['stellar_Fe_over_H_list'][-1]:+.2f}, [Mg/Fe] = {d['stellar_Mg_over_Fe_list'][-1]:+.2f}")
"""),
("md", """
**Questions**
1. Rank the three Kroupa-IMF galaxies by the [Mg/Fe] of their stars. Does it match the toy model?
2. Why does the gas [Mg/Fe] keep falling after star formation has stopped?
3. Compare Kroupa and IGIMF for the fast galaxy. Why does a high star-formation rate change the IMF in the IGIMF theory, and what does this do to [Mg/Fe]?
"""),
("md", "## 2. Run galevo yourself\nThis clones GalIMF next to the repo (once) and runs one model. Change `log_SFR` and `SFEN` (duration in units of 10 Myr; keep `log_SFR + log10(SFEN)` fixed to keep the total mass)."),
("code", """
import subprocess
here = os.getcwd()
gal = os.path.abspath('../../galIMF')
if not os.path.isdir(gal):
    subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/Azeret/galIMF.git', gal], check=True)
os.chdir(gal); sys.path.insert(0, gal)
import galevo

log_SFR, SFEN, IMF = 2.0, 3, 'Kroupa'      # try IMF = 'igimf'
galevo.generate_SFH('flat', log_SFR, SFEN, 0, 10, 0)
galevo.galaxy_evol(imf=IMF, STF=0.3, SFEN=SFEN, Z_0=0.00000001886, solar_mass_component='Anders1989_mass',
                   str_yield_table='portinari98', IMF_name='Kroupa', steller_mass_upper_bound=150,
                   time_resolution_in_Myr=1, mass_boundary_observe_low=1.5, mass_boundary_observe_up=8,
                   SFH_model='provided', SNIa_ON=True, high_time_resolution=None,
                   plot_show=None, plot_save=None, outflow=None, check_igimf=False)
os.chdir(here)
plt.figure(figsize=(7, 5))
ok = np.array(galevo.Fe_over_H_list) > -5
plt.plot(np.array(galevo.Fe_over_H_list)[ok], np.array(galevo.Mg_over_Fe_list)[ok])
plt.xlabel('gas [Fe/H]'); plt.ylabel('gas [Mg/Fe]')
"""),
])

REPO = "Azeret/stellar-populations-lectures"


def colab_cells(name, extra_pip=""):
    badge = (f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
             f"(https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{name})  "
             "\u2190 run this notebook in your browser, nothing to install")
    pkgs = ", ".join(repr(x) for x in extra_pip.split())
    pip = (f"\n    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', {pkgs}], check=True)"
           if extra_pip else "")
    code = f"""# Running in Google Colab? This cell fetches the course code{' and installs ' + extra_pip if extra_pip else ''}.
# On your own computer it does nothing.
import sys, os, subprocess
if 'google.colab' in sys.modules:
    if not os.path.isdir('/content/stellar-populations-lectures'):
        subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/{REPO}.git',
                        '/content/stellar-populations-lectures'], check=True)
    os.chdir('/content/stellar-populations-lectures/notebooks'){pip}"""
    return nbf.v4.new_markdown_cell(badge), nbf.v4.new_code_cell(code)


import sys as _sys
from nb_extra import NB03_SLIDO, NB05, NB06, NB07
nb03.cells += nb(NB03_SLIDO).cells
nb05, nb06, nb07 = nb(NB05), nb(NB06), nb(NB07)
ONLY = _sys.argv[1:]          # e.g. python build_notebooks.py 03 05  -> only those notebooks
for name, n, pip in [("01_IMF.ipynb", nb01, ""), ("02_SSP_with_FaSTAR.ipynb", nb02, "fastar-astro"),
                     ("03_toy_chemical_evolution.ipynb", nb03, ""), ("04_galevo_chemical_evolution.ipynb", nb04, ""),
                     ("05_spectral_resolution.ipynb", nb05, "fastar-astro"),
                     ("06_fitting_an_SSP_with_FaSTAR.ipynb", nb06, "fastar-astro"),
                     ("07_SFH_of_synthetic_galaxies.ipynb", nb07, "fastar-astro ppxf")]:
    if ONLY and name[:2] not in ONLY:
        continue
    md, code = colab_cells(name, pip)
    n.cells = [n.cells[0], md, code] + n.cells[1:]
    nbf.write(n, os.path.join(OUT, name))
print("written")
