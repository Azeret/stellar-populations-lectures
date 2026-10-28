"""Multi-power-law IMFs and random sampling.

Convention: xi(m) = dN/dm  propto  m^(-alpha_i)  in segment i.
Salpeter (1955): alpha = 2.35 for all masses.
Kroupa (2001):   alpha = 1.3 (0.08-0.5 Msun), 2.3 (> 0.5 Msun).
"""
import numpy as np

# (mass breaks, slopes) for the canonical Kroupa (2001) IMF
KROUPA = dict(breaks=[0.08, 0.5, 150.0], alphas=[1.3, 2.3])
SALPETER = dict(breaks=[0.1, 150.0], alphas=[2.35])


def _segments(breaks, alphas):
    """Continuity coefficients k_i so that xi is continuous at the breaks."""
    k = [1.0]
    for i in range(1, len(alphas)):
        mb = breaks[i]
        k.append(k[-1] * mb ** (-alphas[i - 1]) / mb ** (-alphas[i]))
    return np.array(k)


def powerlaw_imf_xi(m, breaks=KROUPA["breaks"], alphas=KROUPA["alphas"]):
    """Un-normalised multi-power-law IMF dN/dm evaluated at masses m."""
    m = np.atleast_1d(np.asarray(m, float))
    k = _segments(breaks, alphas)
    xi = np.zeros_like(m)
    for i, a in enumerate(alphas):
        sel = (m >= breaks[i]) & (m < breaks[i + 1])
        xi[sel] = k[i] * m[sel] ** (-a)
    return xi


def kroupa_xi(m, alpha_high=2.3, m_max=150.0):
    """Kroupa IMF with an adjustable high-mass slope (alpha_3 for m > 1 Msun)."""
    return powerlaw_imf_xi(m, [0.08, 0.5, 1.0, m_max], [1.3, 2.3, alpha_high])


def _integral(breaks, alphas, lo, hi, power):
    """Integral of m^power * xi(m) dm between lo and hi (analytic)."""
    k = _segments(breaks, alphas)
    tot = 0.0
    for i, a in enumerate(alphas):
        a0, a1 = max(lo, breaks[i]), min(hi, breaks[i + 1])
        if a1 <= a0:
            continue
        p = power - a + 1.0
        tot += k[i] * (np.log(a1 / a0) if abs(p) < 1e-12 else (a1 ** p - a0 ** p) / p)
    return tot


def number_fraction(lo, hi, breaks=KROUPA["breaks"], alphas=KROUPA["alphas"]):
    """Fraction of all stars (by number) born with lo <= m < hi."""
    return _integral(breaks, alphas, lo, hi, 0) / _integral(breaks, alphas, breaks[0], breaks[-1], 0)


def mass_fraction(lo, hi, breaks=KROUPA["breaks"], alphas=KROUPA["alphas"]):
    """Fraction of the total birth mass locked in stars with lo <= m < hi."""
    return _integral(breaks, alphas, lo, hi, 1) / _integral(breaks, alphas, breaks[0], breaks[-1], 1)


def sample_imf(n, breaks=KROUPA["breaks"], alphas=KROUPA["alphas"], rng=None):
    """Draw n stellar masses from a multi-power-law IMF (inverse-CDF sampling)."""
    rng = np.random.default_rng(rng)
    k = _segments(breaks, alphas)
    # probability of each segment
    w = np.array([_integral(breaks, alphas, breaks[i], breaks[i + 1], 0) for i in range(len(alphas))])
    w /= w.sum()
    seg = rng.choice(len(alphas), size=n, p=w)
    u = rng.random(n)
    m = np.empty(n)
    for i, a in enumerate(alphas):
        s = seg == i
        lo, hi, p = breaks[i], breaks[i + 1], 1.0 - a
        if abs(p) < 1e-12:
            m[s] = lo * (hi / lo) ** u[s]
        else:
            m[s] = (lo ** p + u[s] * (hi ** p - lo ** p)) ** (1.0 / p)
    return m
