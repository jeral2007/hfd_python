import orbs_python as o
import scipy as sc


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
    def __init__(self, filename="hfd.dat", maxii=512):
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
        return self.getorb_by_number(ns)

    def getorb_by_number(self, num):
        p, q = o.orbs_python(self.filename, num+1, self.maxii)
        return (p[:self.imax], q[:self.imax], p[self.imax])

    def __getgrid__(self):
        grid, weights, iimax =\
            o.orbs_python.getgridfrom(self.filename, self.maxii)
        self.grid = grid[:iimax]
        self.weights = weights[:iimax]
        self.imax = iimax

    def make_integrate(self):
        def integrate(func_vals):
            return sc.trapz(func_vals, self.grid)
        return integrate


