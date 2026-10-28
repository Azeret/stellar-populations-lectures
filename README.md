# Stellar populations, the IMF and chemical evolution of galaxies

Hands-on material for two lectures in the *Galaxies* course at Masaryk University (Dr. Tereza Jeřábková, ÚTFA).

| Notebook | Lecture | What you do |
|---|---|---|
| `notebooks/01_IMF.ipynb` | 1 | Draw stars from the IMF; where are the number, mass and light; most massive star vs cluster mass |
| `notebooks/02_SSP_with_FaSTAR.ipynb` | 1 | Spectra and M/L of simple stellar populations vs age, metallicity and IMF; stochastic sampling |
| `notebooks/03_toy_chemical_evolution.ipynb` | 2 | A 100-line one-zone model: why [Mg/Fe] is a clock, and how the IMF moves the plateau |
| `notebooks/04_galevo_chemical_evolution.ipynb` | 2 | Real chemical-evolution runs with galevo (GalIMF), Kroupa IMF vs IGIMF |

## Getting started

```bash
git clone https://github.com/Azeret/stellar-populations-lectures.git
cd stellar-populations-lectures
python -m venv .venv && source .venv/bin/activate     # or a conda environment
pip install -r requirements.txt
jupyter lab
```

* Notebooks 01 and 03 need only numpy/matplotlib and run in seconds.
* Notebook 02 uses **FaSTAR** (`pip install fastar-astro`, Martín-Navarro et al. 2026, A&A 711, A282 and A283). The first spectrum takes ~10 s, then ~1 s each. Semi-resolved models need a lot of memory beyond ~5000 stars.
* Notebook 04 clones **GalIMF** (https://github.com/Azeret/galIMF; Yan, Jeřábková & Kroupa 2017) next to this repository. Pre-computed runs are in `data/galevo_runs/` so you can plot before you run (a 3 Gyr run takes tens of minutes).

## What else is here

* `stellarpops/` — the small teaching package used by the notebooks: multi-power-law IMFs and sampling (`imf.py`), the toy one-zone model (`toy_gce.py`), remnant masses for M/L (`remnants.py`), plot style (`style.py`).
* `animations/` — scripts for the lecture animations (`a1`–`a8`); `precompute_fastar.py` must run before `a2_a5_fastar.py`. Output goes to `animations/out/`.
* `figures/make_sketches.py` — the hand-drawn line-art diagrams used on the slides.
* `data/run_galevo.py` — how the galevo runs in `data/galevo_runs/` were made.

## Caveats

The toy model uses illustrative yields and a simple 1/t delay-time distribution for SN Ia; it is built to show the mechanism, not to fit data. The M/L "stars + remnants" uses a simple initial–final mass relation. For research, use the full codes and cite the original papers.
