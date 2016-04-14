#coding: utf8
from w3js0_table import w3js0
import scipy as sc
from scipy.integrate import cumtrapz
__doc__ = u"""
#модуль для вычисления прямых и обменных кулоновских интегралов

Содержит следующие функции:
- coulumb(a, b, grid, end_point=-1)
- exchange(a, b, grid, end_point=-1)
- coulumb_melem(a, b, c, grid, end_point=-1)
- exchange_melem(a, b, c, grid, end_point=-1)

Для функций coulumb и exchange выполняются следующие инварианты:

1. coulumb(a, b, grid, end_point) = coulumb_melem(a, b, b, grid, end_point)
2. exchange(a, b, grid, end_point) = exchange_melem(a, b, b, grid, end_point)
3. coulumb(a, a, grid, end_point) = 0.5*exchange(a, a, grid, end_point)

## формат задания орбиталей
В функциях модуля используется унифицированный формат задания орбиталей как
аргументов функций:
орбиталь a задается в виде кортежа (abc, asc, al, aj), где
- abc -- numpy массив со значениями большой компоненты на сетке
- asc -- numpy массив со значениями малой компоненты на сетке
- al -- целое число, орбитальный момент
- aj -- число с плавающей точкой, кратное 0.5, полный момент

## формат задания сетки
В функциях модуля используется унифицированный формат задания сетки для передачи
в функции:
сетка grid задается в виде кортежа: (ro, w, h), где
- ro -- numpy массив, значения координат узлов сетки
- w -- numpy массив, значения весовых коэффициентов для интегрирования. w[i] --
весовой коэффициент для узла r[i].

## coulumb(a, b, grid, end_point=-1)
вычисляет кулоновский прямой интеграл с радиусом обрезания end_point, если
последний не задан интегрирование ведется до бесконечности.
- a -- `` остовная орбиталь''
- b -- `` валентная орбиталь''
- grid -- сетка
- end_point --радиус обрезания.
описание форматов орбиталей и сетки см. в соответствующих разделах.

## exchange(a, b, grid, end_point=-1)
вычисляет кулоновский обменный интеграл с радиусом обрезания end_point, если
последний не задан интегрирование ведется до бесконечности.
- a -- `` остовная орбиталь''
- b -- `` валентная орбиталь''
- grid -- сетка
- end_point --радиус обрезания.
описание форматов орбиталей и сетки см. в соответствующих разделах.

## coulumb_melem(a, b, c, grid, end_point=-1)
вычисляет матричный элемент между орбиталями b и c, соответствующий
кулоновскому прямому интегралу с радиусом обрезания end_point, если
последний не задан интегрирование ведется до бесконечности.
- a -- `` остовная орбиталь''
- b -- `` валентная орбиталь 1''
- с -- `` валентная орбиталь 2''
- grid -- сетка
- end_point --радиус обрезания.
описание форматов орбиталей и сетки см. в соответствующих разделах.

## exchange_melem(a, b, c, grid, end_point=-1)
вычисляет матричный элемент между орибталями b и c, соответствующий кулоновскому
обменному интегралу с радиусом обрезания end_point, если
последний не задан интегрирование ведется до бесконечности.
- a -- `` остовная орбиталь''
- b -- `` валентная орбиталь 1''
- c -- `` валентная орбиталь 2''
- grid -- сетка
- end_point -- радиус обрезания.
описание форматов орбиталей и сетки см. в соответствующих разделах.
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


def coulumb_melem(a, b, c, grid, end_point=-1):
    abc, asc, al, aj = a  # radial and angular for a
    bbc, bsc, bl, bj = b  # radial and angular for b
    cbc, csc, cl, cj = c  # radial and angular for c
    if (cl != bl or cj != bj):
        return 0e0        # operator diagonal for angular variables
    ro, w, h = grid  # radial grid and weights
    end_ind = end_point < 0 and len(ro) or (sc.where(ro > end_point)[0][0]+1)
    cro = ro[:end_ind]
    cw = w[:end_ind]
    cabc = abc[:end_ind]
    casc = asc[:end_ind]
    cbbc = bbc[:end_ind]
    cbsc = bsc[:end_ind]
    ccbc = cbc[:end_ind]
    ccsc = csc[:end_ind]
    bdens = cbbc*ccbc + ccsc*cbsc
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


def exchange_melem(a, b, c, grid, end_point=-1):
    abc, asc, al, aj = a  # radial and angular for a
    bbc, bsc, bl, bj = b  # radial and angular for b
    cbc, csc, cl, cj = c  # radial and angular for c
    if (cj != bj or cl != bl):
        return 0e0  # only angle-diagonal elements are nonzero

    jmax, jmin = max(aj, bj), min(aj, bj)
    ro, w, h = grid  # radial grid and weights
    end_ind = end_point < 0 and len(ro) or (sc.where(ro > end_point)[0][0]+1)
    cabc = abc[:end_ind]
    casc = asc[:end_ind]
    cbbc = bbc[:end_ind]
    cbsc = bsc[:end_ind]
    ccbc = cbc[:end_ind]
    ccsc = csc[:end_ind]
    cro = ro[:end_ind]
    cw = w[:end_ind]
    k = jmax - jmin
    if (k+al+bl) % 2 != 0:
        k += 1
    dens0b = cabc*cbbc+casc*cbsc
    dens0c = cabc*ccbc+casc*ccsc
    dens_kgb = dens0b/cro**(k+1)
    dens_klb = dens0b*cro**k
    dens_kgc = dens0c/cro**(k+1)
    dens_klc = dens0c*cro**k
    res = 0e0
    while (k <= (jmax+jmin)):
        dens_g_int = cumtrapz(dens_kgc*cw, initial=0e0)*h
        # внешнее интегрирование от r до бесконечности
        dens_g_int = dens_g_int[-1] - dens_g_int
        dens_l_int = cumtrapz(dens_klc*cw, initial=0e0)*h
        res_k = sc.trapz((dens_kgb*dens_l_int+dens_klb*dens_g_int)*cw)*h
        res += res_k*w3js0[(jmax, jmin, k)]
        k += 2
        dens_kgb = dens_kgb/cro**2
        dens_klb = dens_klb*cro**2
        dens_kgc = dens_kgc/cro**2
        dens_klc = dens_klc*cro**2
    return res
