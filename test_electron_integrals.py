#! /usr/bin/env python2.7
import source_hfd_python.electron_integrals as el
import sys
from source_hfd_python.hfd_dat import Hfd
from scipy import trapz, exp, where

def str2nlj(s):
    n = int(s[0])
    l = 'spdfgh'.index(s[1])
    j = float(s[2:s.find('/')])/2e0
    return (n, l, j)

hfd = Hfd()
grid = (hfd.grid, hfd.weights, hfd.h)
nc = where(hfd.grid>0.5)[0][0]
testgrid = exp(-hfd.grid)
res = trapz(testgrid[:nc]*hfd.weights[:nc])*hfd.h
print("test grid")
print("{} - {} = {}\n".format(res, (1-exp(-0.5)), res-1.0+exp(-0.5)))
rc = 5e-1
csn = sys.argv[1]  # core shell
vsns = sys.argv[2:]  # valent shells
nc, lc, jc = str2nlj(csn)
p, q, en = hfd[csn]

core_orb = (p, q, lc, jc)

for v in vsns:
    nv, lv, jv = str2nlj(v)
    pv, qv, env = hfd[v]
    v_orb = (pv, qv, lv, jv)
    coul = el.coulumb(core_orb, v_orb, grid, rc)
    exc = el.exchange(core_orb, v_orb, grid, rc)
    out = "{} {}\t{:.6f}\t{:.6f}".format(csn, v, coul, exc)
    print out.replace('.',',')
