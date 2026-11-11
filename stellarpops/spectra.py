"""Small, readable tools for working with spectra (notebooks 05-07).

Everything is plain numpy so students can read it. pPXF (Cappellari 2017,
2023; `pip install ppxf`) does the same things faster and more carefully.
"""
import numpy as np

C_KMS = 299792.458                  # speed of light [km/s]
FWHM_FASTAR = 2.51                  # FaSTAR / MILES spectral resolution, FWHM [Angstrom]
SIG2FWHM = 2 * np.sqrt(2 * np.log(2))   # = 2.355

# Lick/IDS index definitions (Worthey et al. 1994; Trager et al. 1998), Angstrom
LICK = {
    "Hbeta":  ((4847.875, 4876.625), (4827.875, 4847.875), (4876.625, 4891.625)),
    "Mgb":    ((5160.125, 5192.625), (5142.625, 5161.375), (5191.375, 5206.375)),
    "Fe5270": ((5245.650, 5285.650), (5233.150, 5248.150), (5285.650, 5318.150)),
    "Fe5335": ((5312.125, 5352.125), (5304.625, 5315.875), (5353.375, 5363.375)),
    "NaD":    ((5876.875, 5909.375), (5860.625, 5875.625), (5922.125, 5948.125)),
}


def gaussian_kernel(sigma_pix, half_width=5):
    """Normalised Gaussian kernel sampled on pixels (sigma in pixels)."""
    n = max(int(np.ceil(half_width * sigma_pix)), 1)
    x = np.arange(-n, n + 1)
    k = np.exp(-0.5 * (x / sigma_pix) ** 2)
    return k / k.sum()


def convolve(flux, kernel):
    """Convolve, padding with the edge values so the ends do not drop to zero."""
    n = len(kernel) // 2
    padded = np.concatenate([np.full(n, flux[0]), flux, np.full(n, flux[-1])])
    return np.convolve(padded, kernel, mode="valid")


def degrade_resolution(wave, flux, fwhm_in, fwhm_out):
    """Lower the resolution of a linearly sampled spectrum from FWHM fwhm_in to
    fwhm_out (both in Angstrom). Gaussians add in quadrature, so the kernel
    has FWHM = sqrt(fwhm_out^2 - fwhm_in^2)."""
    if fwhm_out <= fwhm_in:
        return flux.copy()
    dlam = np.median(np.diff(wave))
    sigma_pix = np.sqrt(fwhm_out ** 2 - fwhm_in ** 2) / SIG2FWHM / dlam
    return convolve(flux, gaussian_kernel(sigma_pix))


def log_rebin(wave, flux, velscale=None):
    """Resample a spectrum onto a grid uniform in ln(lambda): then every pixel
    has the same width in velocity, velscale = c * d(ln lambda) [km/s].
    Simple linear interpolation (fine for well-sampled spectra)."""
    ln = np.log(wave)
    if velscale is None:
        velscale = C_KMS * np.min(np.diff(ln))
    dln = velscale / C_KMS
    ln_new = np.arange(ln[0], ln[-1], dln)
    return ln_new, np.interp(ln_new, ln, flux), velscale


def broaden_velocity(flux_log, velscale, sigma_kms, v_kms=0.0):
    """Line-of-sight velocity distribution: shift by v and convolve with a Gaussian
    of dispersion sigma (km/s). flux_log must be log-rebinned with velscale."""
    out = flux_log
    if sigma_kms > 0:
        out = convolve(out, gaussian_kernel(sigma_kms / velscale))
    if v_kms != 0:
        x = np.arange(len(out))
        out = np.interp(x - v_kms / velscale, x, out)
    return out


def lick_index(wave, flux, name):
    """Equivalent width [Angstrom] in a Lick band with a straight pseudo-continuum."""
    band, blue, red = LICK[name]

    def mean(a, b):
        sel = (wave > a) & (wave < b)
        return wave[sel].mean(), flux[sel].mean()

    (wb, fb), (wr, fr) = mean(*blue), mean(*red)
    sel = (wave > band[0]) & (wave < band[1])
    cont = fb + (fr - fb) * (wave[sel] - wb) / (wr - wb)
    return np.trapezoid(1 - flux[sel] / cont, wave[sel])


def add_noise(flux, snr, rng=None):
    """Gaussian noise with a constant signal-to-noise ratio per pixel.
    Returns (noisy flux, 1-sigma noise array)."""
    rng = np.random.default_rng(rng)
    noise = np.abs(flux) / snr
    return flux + rng.normal(0, 1, flux.size) * noise, noise


def normalise(wave, flux, lo=5400, hi=5600):
    sel = (wave > lo) & (wave < hi)
    return flux / np.median(flux[sel])
