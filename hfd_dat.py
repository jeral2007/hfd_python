#coding: utf8
import orbs_python as o
import scipy as sc
__doc__ = """
## hfd.dat

модуль для работы с hfd.dat файлами
Содержит класс Hfd()
"""

def _isdigit_(c):
    return c in '0123456789'


def _ismoment_(c):
    return c in 'spdfghiklmn'


def _isslash_(c):
    return c == '/'


def _str2orb_(orbspec):
    state = 0
    nstr, jjstr = '', ''
    for c in orbspec:
        if state == 0:  # wait digit
            if _isdigit_(c):
                nstr += c
            elif _ismoment_(c):
                n = int(nstr)
                l = "spdfghiklmn".find(c)
                state = 1
                continue
            else:
                raise ValueError("incorrect orbital")
        if state == 1:
            if _isdigit_(c):
                jjstr += c
            elif _isslash_(c):
                break
            else:
                raise ValueError("incorrect orbital {}, c={}".format(orbspec,
                                                                     c))
            j = int(jjstr)
    return n, l, j


class Hfd():
    """ master class for processing hfd.dat files
Usage:
    hfd_dat = Hfd('hfd.dat', maxii) where the hfd.dat
    is the actual name of the file of interest, maxii
    is number of elements in record and equals to 512 by default

Methods and Variables:
    - self.getorb_by_number(n) returns the radial parts of the
    large and small components of orbital with number n
    - self.__getitem__(orb_spec) returns orbital with given specification
        orbspec
        for example hfd_dat['5s1/2'] or hfd_dat[(5,0,1)] will return tuple
        (p, q, en), where p is the large component of 5s1/2 orbital,
        q is the small component, and en is the orbital energy.
    - self.__getgrid__() is the method that loads grid and weights from hfd.dat
    - self.grid is the scipy 1d-array of the nodes of grid
    - self.h * self.wieghts is the scipy 1d-array of the weights of grid
    - self.ns is the total number of shells in the hfd.dat file
    - self.ll[0:self.ns] is the scipy 1d-array
        of orbital moments of the orbitals
    - self.jj[0:self.ns] is the scipy 1d-array of
        the full moments of the orbitals
    - self.qq[0:self.ns] is the scipy 1d-array of the occupation numbers of
        the orbitals
    """
    def __init__(self, filename="hfd.dat", maxii=512):
        """ see entire class documentation"""
        (nn, ll, jj,
         qq, h, ns) = o.orbs_python.get_atom_infofrom(filename, maxii)
        self.h = h
        self.ns = ns
        self.nn = sc.array(nn[:ns], dtype='int')
        self.ll = sc.array(ll[:ns], dtype='int')
        self.jj = sc.array(jj[:ns], dtype='int')
        self.qq = sc.array(qq[:ns])
        self.maxii = maxii
        self.filename = filename
        self.__getgrid__()

    def __getitem__(self, orb_spec):
        """ see entire class documentation"""
        if type(orb_spec) is str:
            n, l, j = _str2orb_(orb_spec)
        else:
            n, l, j = orb_spec
        ns = 0
        ok = False
        for (n1, l1, j1) in zip(self.nn, self.ll, self.jj):
            if n == n1 and l == l1 and j == j1:
                ok = True
                break
            ns += 1
        if not ok:
            raise ValueError("{} not in {}".format(orb_spec,self.filename))
        return self.getorb_by_number(ns)

    def occ(self, orb_spec):
        if type(orb_spec) is str:
            n, l, j = _str2orb_(orb_spec)
        else:
            n, l, j = orb_spec
        ns = 0
        ok = False
        for (n1, l1, j1) in zip(self.nn, self.ll, self.jj):
            if n == n1 and l == l1 and j == j1:
                ok = True
                break
            ns += 1
        if not ok:
            raise ValueError
        return self.qq[ns]

    def getorb_by_number(self, num):
        """ see entire class documentation"""
        p, q = o.orbs_python(self.filename, num+1, self.maxii)
        return (p[:self.imax], q[:self.imax], p[self.imax])

    def __getgrid__(self):
        """ see entire class documentation"""
        grid, weights, iimax =\
            o.orbs_python.getgridfrom(self.filename, self.maxii)
        self.grid = grid[:iimax]
        self.weights = weights[:iimax]
        self.imax = iimax

    def make_integrate(self):
        def integrate(func_vals):
            return sc.trapz(func_vals, self.grid)
        return integrate


def _get_nc(rc, r):
    if rc >= r[-1]:
        return -1
    else:
        return sc.where(rc<r)[0][0]+1

def gr_trapz(f, hfd, rc=1e15):
    """ Интегрирование на сетке заданной в hfd.dat

### Аргументы
- f - numpy-1d массив содержащий значения функции на сетке
- rc=1e15 - верхний предел интеграла
- hfd - экземпляр Hfd, hfd.grid - узлы сетки, hfd.weights - веса в них

### Пример использования
~~~
res = gr_trapz(hfd.grid**2, rc=1.0, hfd)
~~~
"""
    r, w, h = hfd.grid, hfd.weights, hfd.h
    nc = _get_nc(rc, r)
    return sc.trapz(f[:nc]*w[:nc])*h
