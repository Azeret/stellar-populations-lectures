# Stellar populations, the IMF and chemical evolution of galaxies

Hands-on material for two lectures in the *Galaxies* course at Masaryk University (Dr. Tereza Jeřábková, ÚTFA).

## 🎲 Class games (phone or laptop, nothing to install)

**https://azeret.github.io/stellar-populations-lectures/**

1. **Build a star cluster** — give birth to stars drawn from the Kroupa IMF and see where the mass sits (Lecture 1).
2. **Galaxy clock** — set when your galaxy forms its stars, watch SN II and SN Ia fill the gas with Mg and Fe, and race to an [Mg/Fe] target (Lecture 2).

## 💬 Class Slido

| Lecture | Join (students) | Code |
|---|---|---|
| 1 · Stellar populations & the IMF | https://app.sli.do/event/fAi3QWgSvPf3EnTHoNAEUi | slido.com **#2458698** |
| 2 · Chemical evolution & the [Mg/Fe] clock | https://app.sli.do/event/s76TJyV1cGRxvwUWRgkj4F | slido.com **#1642685** |

## Notebooks (click the badge to run in your browser with Google Colab)

| Notebook | Lecture | What you do | Run |
|---|---|---|---|
| `01_IMF.ipynb` | 1 | Draw stars from the IMF; where are the number, mass and light; most massive star vs cluster mass | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Azeret/stellar-populations-lectures/blob/main/notebooks/01_IMF.ipynb) |
| `02_SSP_with_FaSTAR.ipynb` | 1 | Spectra and M/L of simple stellar populations vs age, metallicity and IMF; stochastic sampling | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Azeret/stellar-populations-lectures/blob/main/notebooks/02_SSP_with_FaSTAR.ipynb) |
| `03_toy_chemical_evolution.ipynb` | 2 | A 100-line one-zone model: why [Mg/Fe] is a clock, how the IMF moves the plateau, and the kitchen game in code | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Azeret/stellar-populations-lectures/blob/main/notebooks/03_toy_chemical_evolution.ipynb) |
| `04_galevo_chemical_evolution.ipynb` | 2 | Real chemical-evolution runs with galevo (GalIMF), Kroupa IMF vs IGIMF | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Azeret/stellar-populations-lectures/blob/main/notebooks/04_galevo_chemical_evolution.ipynb) |
| `05_spectral_resolution.ipynb` | 1 (practice) | Convolution by hand, instrumental resolution, velocity dispersion, why line strengths drop with σ, noise | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Azeret/stellar-populations-lectures/blob/main/notebooks/05_spectral_resolution.ipynb) |
| `06_fitting_an_SSP_with_FaSTAR.ipynb` | 1 (practice) | Fit age and metallicity of a mock spectrum: χ² grid, posterior, the age–metallicity degeneracy, S/N | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Azeret/stellar-populations-lectures/blob/main/notebooks/06_fitting_an_SSP_with_FaSTAR.ipynb) |
| `07_SFH_of_synthetic_galaxies.ipynb` | 1 → 2 | Build four synthetic galaxies and recover their star-formation histories with pPXF; regularisation; NNLS by hand | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Azeret/stellar-populations-lectures/blob/main/notebooks/07_SFH_of_synthetic_galaxies.ipynb) |

In Colab, run the first code cell: it fetches this repository and installs what the notebook needs (FaSTAR for 02 and 05–07, pPXF for 07). You need a Google account; nothing is installed on your computer.

## Getting started on your own computer

```bash
git clone https://github.com/Azeret/stellar-populations-lectures.git
cd stellar-populations-lectures
python -m venv .venv && source .venv/bin/activate     # or a conda environment
pip install -r requirements.txt
jupyter lab
```

* Notebooks 01 and 03 need only numpy/matplotlib and run in seconds.
* Notebook 02 uses **FaSTAR** (`pip install fastar-astro`, Martín-Navarro et al. 2026, A&A 711, A282 and A283). The first spectrum takes ~10 s, then ~1 s each. Semi-resolved models need a lot of memory beyond ~5000 stars.
* Notebooks 05–07 use FaSTAR; 07 also needs **pPXF** (`pip install ppxf`; Cappellari 2017, MNRAS 466, 798; Cappellari 2023, MNRAS 526, 3273). 06 and 07 take a few minutes (they compute many model spectra).
* Notebook 04 clones **GalIMF** (https://github.com/Azeret/galIMF; Yan, Jeřábková & Kroupa 2017) next to this repository. Pre-computed runs are in `data/galevo_runs/` so you can plot before you run (a 3 Gyr run takes tens of minutes).

## What else is here

* `stellarpops/` — the small teaching package used by the notebooks: multi-power-law IMFs and sampling (`imf.py`), the toy one-zone model (`toy_gce.py`), spectra tools: convolution, log-rebinning, Lick indices (`spectra.py`), remnant masses for M/L (`remnants.py`), plot style (`style.py`).
* `animations/` — scripts for the lecture animations (`a1`–`a8`); `precompute_fastar.py` must run before `a2_a5_fastar.py`. Output goes to `animations/out/`.
* `figures/make_sketches.py` — the hand-drawn line-art diagrams used on the slides.
* `data/run_galevo.py` — how the galevo runs in `data/galevo_runs/` were made.

## Caveats

The toy model uses illustrative yields and a simple 1/t delay-time distribution for SN Ia; it is built to show the mechanism, not to fit data. The M/L "stars + remnants" uses a simple initial–final mass relation. For research, use the full codes and cite the original papers.
