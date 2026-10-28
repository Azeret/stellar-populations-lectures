"""A deliberately tiny one-zone ("bathtub") chemical evolution model.

It follows only two elements, Mg and Fe, to show *why* [Mg/Fe] is a clock:

* Core-collapse SNe (SN II, stars > 8 Msun) explode within ~40 Myr of star
  formation. We treat them as instantaneous. They make a lot of Mg and some Fe.
* Type Ia SNe (white dwarfs in binaries) explode with a delay-time
  distribution DTD ~ 1/t starting at 40 Myr. They make mostly Fe.

Gas: closed box, or with exponential infall. Star formation: SFR = M_gas / tau_sf
(a linear Schmidt law), optionally switched off at t_stop (a galactic wind /
quenching). A constant return fraction R gives gas back instantly.

The yields are *illustrative* (of the order of the values in e.g. Kobayashi et
al. 2006 for SN II and Iwamoto et al. 1999 for SN Ia), chosen to give
[Mg/Fe] ~ +0.4 from SN II alone with a Kroupa IMF. Use galevo for real models.
"""
import numpy as np
from .imf import _integral

# Solar mass fractions from Asplund et al. (2009)
SOLAR = dict(X=0.7381, Mg=7.14e-4, Fe=1.30e-3)

# Illustrative yields [Msun of element per supernova].
# SN II: Mg grows steeply with progenitor mass, Fe hardly does. This is what
# makes the [Mg/Fe] "plateau" depend on the high-mass IMF slope.
def mg_yield_ii(m):
    return 0.1 * (np.asarray(m) / 20.0) ** 1.5

def fe_yield_ii(m):
    return 0.07 + 0.0 * np.asarray(m)

YIELD_IA = dict(Mg=0.02, Fe=0.70)
N_IA_KROUPA = 1.3e-3   # SN Ia per Msun formed for a Kroupa IMF (Maoz & Mannucci 2012)


def _imf_numbers(alpha_high=2.3, m_max=100.0):
    """SN II and SN Ia numbers per Msun formed for a Kroupa-like IMF whose slope
    above 1 Msun is alpha_high, plus the IMF-averaged SN II yields."""
    b, a = [0.08, 0.5, 1.0, m_max], [1.3, 2.3, alpha_high]
    mtot = _integral(b, a, 0.08, m_max, 1)
    n_ii = _integral(b, a, 8.0, m_max, 0) / mtot
    mm = np.geomspace(8.0, m_max, 2000)
    w = mm ** (-alpha_high)
    y_ii = dict(Mg=np.trapezoid(w * mg_yield_ii(mm), mm) / np.trapezoid(w, mm),
                Fe=np.trapezoid(w * fe_yield_ii(mm), mm) / np.trapezoid(w, mm))
    n_ia_prog = _integral(b, a, 3.0, 8.0, 0) / mtot
    bk, ak = [0.08, 0.5, 1.0, m_max], [1.3, 2.3, 2.3]
    n_ia_prog_kroupa = _integral(bk, ak, 3.0, 8.0, 0) / _integral(bk, ak, 0.08, m_max, 1)
    n_ia = N_IA_KROUPA * n_ia_prog / n_ia_prog_kroupa
    return n_ii, n_ia, y_ii


def run_one_zone(tau_sf=2.0, t_stop=None, infall_tau=None, alpha_high=2.3,
                 eta=1.0, t_end=13.0, dt=0.002, R=0.3, ia=True, gas0=1.0):
    """Run the toy model. Times in Gyr. Returns a dict of arrays.

    tau_sf      gas depletion time (Gyr): small = fast, efficient star formation
    t_stop      stop star formation at this time (Gyr), e.g. 1 for an elliptical
    infall_tau  if given, gas falls in as exp(-t/infall_tau) instead of a closed box
    alpha_high  IMF slope above 1 Msun (2.3 = Kroupa; 1.9 top-heavy; 2.7 top-light)
    eta         outflow mass-loading: gas is blown out at eta * SFR
    ia          switch Type Ia supernovae on/off

    Returned gas abundances FeH, MgH, MgFe describe the gas (= newly born stars);
    star_FeH, star_MgFe are mass-weighted averages over all stars formed so far
    (what you would measure in an old galaxy's integrated spectrum, roughly).
    """
    n = int(round(t_end / dt)) + 1
    t = np.arange(n) * dt
    n_ii, n_ia, y_ii = _imf_numbers(alpha_high)

    # SN Ia delay-time distribution ~ 1/t between 0.04 and 13.8 Gyr, normalised to n_ia
    td = t.copy(); td[0] = dt
    dtd = np.where((td >= 0.04) & (td <= 13.8), 1.0 / td, 0.0)
    dtd *= n_ia / (dtd.sum() * dt)          # SN Ia per Msun formed per Gyr

    gas = np.zeros(n); mg = np.zeros(n); fe = np.zeros(n); sfr = np.zeros(n)
    rate_ia = np.zeros(n); rate_ii = np.zeros(n)
    g, m_mg, m_fe = (0.0 if infall_tau else gas0), 0.0, 0.0
    infall_norm = gas0 / infall_tau if infall_tau else 0.0
    sfr_hist = np.zeros(n)
    st_mass = st_mg = st_fe = 0.0
    star_mg = np.zeros(n); star_fe = np.zeros(n); star_m = np.zeros(n)
    for i in range(n):
        s = g / tau_sf if (t_stop is None or t[i] < t_stop) else 0.0
        sfr_hist[i] = s
        # SN Ia rate now = sum over past SFR * DTD(delay)
        r_ia = (np.dot(sfr_hist[:i + 1][::-1], dtd[:i + 1]) * dt) if ia else 0.0
        r_ii = s * n_ii
        zmg = m_mg / g if g > 0 else 0.0
        zfe = m_fe / g if g > 0 else 0.0
        inflow = infall_norm * np.exp(-t[i] / infall_tau) if infall_tau else 0.0
        out = eta * s
        # stars born now inherit the gas composition
        st_mass += s * (1 - R) * dt; st_mg += s * (1 - R) * zmg * dt; st_fe += s * (1 - R) * zfe * dt
        # update reservoir: locked into long-lived stars + blown out by the wind
        g += (inflow - s * (1 - R) - out) * dt
        m_mg += (-(s * (1 - R) + out) * zmg + r_ii * y_ii["Mg"] + r_ia * YIELD_IA["Mg"]) * dt
        m_fe += (-(s * (1 - R) + out) * zfe + r_ii * y_ii["Fe"] + r_ia * YIELD_IA["Fe"]) * dt
        g = max(g, 1e-12); m_mg = max(m_mg, 0.0); m_fe = max(m_fe, 0.0)
        star_m[i], star_mg[i], star_fe[i] = st_mass, st_mg, st_fe
        gas[i], mg[i], fe[i], sfr[i], rate_ia[i], rate_ii[i] = g, m_mg, m_fe, s, r_ia, r_ii

    with np.errstate(divide="ignore", invalid="ignore"):
        feh = np.log10(fe / gas / SOLAR["Fe"])
        mgh = np.log10(mg / gas / SOLAR["Mg"])
        mgfe = mgh - feh
        s_feh = np.log10(star_fe / star_m / SOLAR["Fe"])
        s_mgfe = np.log10(star_mg / star_m / SOLAR["Mg"]) - s_feh
    return dict(t=t, gas=gas, sfr=sfr, rate_ii=rate_ii, rate_ia=rate_ia,
                FeH=feh, MgH=mgh, MgFe=mgfe, star_FeH=s_feh, star_MgFe=s_mgfe,
                stellar_mass=star_m, n_ii=n_ii, n_ia=n_ia, yields_ii=y_ii)
