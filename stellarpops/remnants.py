"""Mass locked in living stars + stellar remnants, per Msun formed.

Used to turn FaSTAR's luminosity into the classic (stars + remnants) M/L.
Very simple ingredients, good enough for teaching:
  * main-sequence lifetime  t_MS ~ 10 Gyr (m/Msun)^-2.5  -> turn-off mass
  * white dwarfs (m < 8):   M_WD = 0.109 m + 0.394          (Kalirai et al. 2008)
  * neutron stars (8-25):   1.4 Msun
  * black holes (> 25):     0.5 m  (crude; strongly model dependent)
"""
import numpy as np


def turnoff_mass(age_gyr):
    return (np.asarray(age_gyr) / 10.0) ** (-1.0 / 2.5)


def remnant_mass(m):
    m = np.asarray(m, float)
    return np.where(m < 8, 0.109 * m + 0.394, np.where(m < 25, 1.4, 0.5 * m))


def living_plus_remnant_mass(age_gyr, xi, m_min=0.1, m_max=100.0, n=4000):
    """Mass in living stars + remnants per 1 Msun formed, for IMF xi(m) (any normalisation)."""
    m = np.geomspace(m_min, m_max, n)
    w = xi(m)
    mtot = np.trapezoid(w * m, m)
    mto = turnoff_mass(age_gyr)
    alive = np.where(m <= mto, m, remnant_mass(m))
    return np.trapezoid(w * alive, m) / mtot
