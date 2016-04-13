from w3js0_table import w3js0
import scipy as sc
from scipy.integrate import cumtrapz
__doc__ = """
модуль для вычисления прямых и обменных кулоновских интегралов
"""


def coulumb(a, b, grid, end_point=-1):
    abc, asc, al, aj = a  # radial and angular for a
    bbc, bsc, bl, bj = b  # radial and angular for b
    if (al+bl) % 2 != 0:  # parity check
        return 0.0
    ro, w, h = grid  # radial grid and weights
    end_ind = end_point < 0 and len(ro) or (sc.where(ro > end_point)[0][0] - 1)
    ro = ro[:end_ind]
    w = w[:end_ind]
    abc = abc[:end_ind]
    asc = asc[:end_ind]
    bbc = bbc[:end_ind]
    bsc = bsc[:end_ind]
    bdens = bbc**2 + bsc**2
    inner = 1./ro*cumtrapz(bdens*w, initial=0e0)*h
    outer = cumtrapz(bdens/ro*w, initial=0e0)*h
    outer = outer[:-1] - outer  # внешнее интегрирование от r до бесконечности
    adens = abc**2 + asc**2
    res = sc.trapz(adens*(inner+outer)*w[1:])*h
    return res*w3js0[(aj, aj, 0)]*w3js0[(bj, bj, 0)]


def exchange(a, b, grid, end_point=-1):
    abc, asc, al, aj = a  # radial and angular for a
    bbc, bsc, bl, bj = b  # radial and angular for b
    jmax, jmin = max(aj, bj), min(aj, bj)
    ro, w, h = grid  # radial grid and weights
    end_ind = end_point < 0 and len(ro) or (sc.where(ro > end_point)[0][0] - 1)
    abc = abc[:end_ind]
    asc = asc[:end_ind]
    bbc = bbc[:end_ind]
    bsc = bsc[:end_ind]
    ro = ro[:end_ind]
    w = w[:end_ind]
    k = jmax-jmin
    if (k+al+bl) % 2 != 0:
        k += 1
    dens0 = abc*bbc+asc*bsc

    dens_kg = dens0/ro**(k+1)
    dens_kl = dens0*ro**k
    res = 0e0
    while (k <= (jmax+jmin)):
        dens_g_int = cumtrapz(dens_kg*w, initial=0e0)
        # внешнее интегрирование от r до бесконечности
        dens_g_int = dens_g_int[:-1] - dens_g_int
        dens_l_int = cumtrapz(dens_kl*w, initial=0e0)*h
        res_k = sc.trapz((dens_kg*dens_l_int+dens_kl*dens_g_int)*w)*h
        res += res_k*w3js0[(jmax, jmin, k)]**2
        k += 2
