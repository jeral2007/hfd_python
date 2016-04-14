#coding: utf8
from w3js0_table import w3js0
import scipy as sc
from scipy.integrate import cumtrapz
__doc__ = u"""
модуль для вычисления прямых и обменных кулоновских интегралов
"""


def coulumb(a, b, grid, end_point=-1):
    abc, asc, al, aj = a  # radial and angular for a
    bbc, bsc, bl, bj = b  # radial and angular for b
    ro, w, h = grid  # radial grid and weights
    end_ind = end_point < 0 and len(ro) or (sc.where(ro > end_point)[0][0]+1)
    cro = ro[:end_ind]
    cw = w[:end_ind]
    cabc = abc[:end_ind]
    casc = asc[:end_ind]
    cbbc = bbc[:end_ind]
    cbsc = bsc[:end_ind]
    bdens = cbbc**2 + cbsc**2
    inner = 1./cro*cumtrapz(bdens*cw, initial=0e0)*h
    outer = cumtrapz(bdens/cro*cw, initial=0e0)*h
    outer = outer[-1] - outer  # внешнее интегрирование от r до бесконечности
    adens = cabc**2 + casc**2
    res = sc.trapz(adens*(inner+outer)*cw)*h
    return res


def exchange(a, b, grid, end_point=-1):
    abc, asc, al, aj = a  # radial and angular for a
    bbc, bsc, bl, bj = b  # radial and angular for b
    jmax, jmin = max(aj, bj), min(aj, bj)
    ro, w, h = grid  # radial grid and weights
    end_ind = end_point < 0 and len(ro) or (sc.where(ro > end_point)[0][0]+1)
    cabc = abc[:end_ind]
    casc = asc[:end_ind]
    cbbc = bbc[:end_ind]
    cbsc = bsc[:end_ind]
    cro = ro[:end_ind]
    cw = w[:end_ind]
    k = jmax - jmin
    if (k+al+bl) % 2 != 0:
        k += 1
    dens0 = cabc*cbbc+casc*cbsc

    dens_kg = dens0/cro**(k+1)
    dens_kl = dens0*cro**k
    res = 0e0
    while (k <= (jmax+jmin)):
        dens_g_int = cumtrapz(dens_kg*cw, initial=0e0)*h
        # внешнее интегрирование от r до бесконечности
        dens_g_int = dens_g_int[-1] - dens_g_int
        dens_l_int = cumtrapz(dens_kl*cw, initial=0e0)*h
        res_k = sc.trapz((dens_kg*dens_l_int+dens_kl*dens_g_int)*cw)*h
        res += res_k*w3js0[(jmax, jmin, k)]
        k += 2
        dens_kg = dens_kg/cro**2
        dens_kl = dens_kl*cro**2
    return res
