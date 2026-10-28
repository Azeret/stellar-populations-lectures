"""Small teaching toolkit for the lectures
"Stellar populations, the IMF and chemical evolution of galaxies".

Everything here is deliberately simple and transparent, so students can read
the code. For research-grade models use FaSTAR (spectra) and galIMF/galevo
(chemical evolution), which the notebooks also call.
"""
from .imf import (kroupa_xi, powerlaw_imf_xi, sample_imf, mass_fraction,
                  number_fraction, KROUPA)
from .toy_gce import run_one_zone, SOLAR

__all__ = ["kroupa_xi", "powerlaw_imf_xi", "sample_imf", "mass_fraction",
           "number_fraction", "KROUPA", "run_one_zone", "SOLAR"]
