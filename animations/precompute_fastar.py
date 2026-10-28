"""Pre-compute FaSTAR spectra and M/L ratios used by animations a2-a5.
Saves out/fastar_grid.npz (takes a few minutes on a laptop).

FaSTAR: Martin-Navarro et al. 2026, A&A 711, A282/A283 — pip install fastar-astro
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import jax
from fastar import IntegratedSSPSynthesizer, SemiresolvedSSPSynthesizer, imf
from stellarpops.remnants import living_plus_remnant_mass
from stellarpops import kroupa_xi

OUT = os.path.join(os.path.dirname(__file__), "out"); os.makedirs(OUT, exist_ok=True)
t0 = time.time()
kro = IntegratedSSPSynthesizer(imf_function=imf.kroupa)
spl = IntegratedSSPSynthesizer(imf_function=imf.single_power_law)
wave = np.array(kro.wave)


def ml_star_remnant(ssp, age, met, xi, imf_params=None):
    """V-band (living stars + remnants)/L, using FaSTAR's luminosity per Msun formed."""
    ml_birth = float(ssp.mass_to_light_ratio(age=age, met=met, imf_params=imf_params)["total"])
    return ml_birth * living_plus_remnant_mass(age, xi), ml_birth


# 1) ageing at solar metallicity, Kroupa IMF
ages = np.geomspace(0.03, 13.0, 60)
spec_age, ml_age, mlb_age = [], [], []
for a in ages:
    spec_age.append(np.array(kro.synthesize(age=a, met=0.0)))
    m1, m2 = ml_star_remnant(kro, a, 0.0, kroupa_xi)
    ml_age.append(m1); mlb_age.append(m2)
print("ages done", round(time.time() - t0))

# 2) metallicity at 10 Gyr
mets = np.linspace(-2.2, 0.25, 40)
spec_met = [np.array(kro.synthesize(age=10.0, met=z)) for z in mets]
print("mets done", round(time.time() - t0))

# 3) high-mass + low-mass slope: single power law 0.1-100 Msun, 10 Gyr, solar
alphas = np.linspace(1.3, 3.3, 41)
spec_alpha, ml_alpha, mlb_alpha = [], [], []
for al in alphas:
    p = {"alpha": float(al)}
    spec_alpha.append(np.array(spl.synthesize(age=10.0, met=0.0, imf_params=p)))
    xi = lambda m, al=al: np.asarray(m) ** (-al)
    m1, m2 = ml_star_remnant(spl, 10.0, 0.0, xi, p)
    ml_alpha.append(m1); mlb_alpha.append(m2)
print("alphas done", round(time.time() - t0))

# 4) stochastic sampling (semi-resolved models), young and old
semi = SemiresolvedSSPSynthesizer(imf_function=imf.kroupa)
key = jax.random.PRNGKey(7)
nstars = [50, 500, 5000]
nreal = 12
semi_specs = {}
for age in (0.1, 10.0):
    ref = np.array(kro.synthesize(age=age, met=0.0))
    semi_specs[f"ref_{age}"] = ref
    for n in nstars:
        arr = []
        for k in jax.random.split(jax.random.fold_in(key, n), nreal):
            s, _ = semi.synthesize(age=age, met=0.0, num_stars=n, key=k)
            arr.append(np.array(s))
        semi_specs[f"semi_{age}_{n}"] = np.array(arr)
    print("semi", age, "done", round(time.time() - t0))

np.savez(os.path.join(OUT, "fastar_grid.npz"), wave=wave,
         ages=ages, spec_age=np.array(spec_age), ml_age=np.array(ml_age), mlb_age=np.array(mlb_age),
         mets=mets, spec_met=np.array(spec_met),
         alphas=alphas, spec_alpha=np.array(spec_alpha), ml_alpha=np.array(ml_alpha), mlb_alpha=np.array(mlb_alpha),
         nstars=np.array(nstars), **semi_specs)
print("saved in", round(time.time() - t0), "s")
