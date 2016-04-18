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
nc = where(hfd.grid > 0.5)[0][0]
print(nc)
testgrid = exp(-hfd.grid)
res = trapz(testgrid[:nc]*hfd.weights[:nc])*hfd.h
print("test grid")
print("{} - {} = {}\n".format(res, (1-exp(-0.5)), res-1.0+exp(-0.5)))
rc = 5e-1
csn = sys.argv[1]  # core shell
vsns = sys.argv[2:]  # valent shells
ncc, lc, jc = str2nlj(csn)
p, q, en = hfd[csn]
print("norm function")
core_orb = (p, q, lc, jc)
norm2rc = trapz((p[:nc]**2+q[:nc]**2)*hfd.weights[:nc])*hfd.h
norm2 = trapz((p**2+q**2)*hfd.weights[:hfd.imax])*hfd.h
print("||{}||^2  = {}\t{}".format(csn, norm2rc, norm2))
v_orbs = []
for v in vsns:
    nv, lv, jv = str2nlj(v)
    pv, qv, env = hfd[v]
    v_orb = (pv, qv, lv, jv)
    v_orbs += [v_orb]
    coul = el.coulumb(core_orb, v_orb, grid, rc)
    exc = -el.exchange(core_orb, v_orb, grid, rc)
    out = "{} {}\t{:.6f}\t{:.6f}".format(csn, v, coul, exc)
    print out.replace('.', ',')
# grid info
with open('grid.txt', 'w') as outp:
    for i, r in enumerate(hfd.grid):
        outp.write("{} {}\n".format(i, r))
# orb info
with open('orbs.txt', 'w') as outp:
    r = grid[0]
    for i in xrange(hfd.imax):
        res = "\t".join(str(v_orb[0][i]) for v_orb in v_orbs)
        outp.write("{}\t{}\n".format(r[i], res))

print("electron_melem_test")


def test_with_orb(corb, vorb, v, grid, rc):

    res = "{}\t{}\t{}\t{}\t{}".format(v, el.coulumb(core_orb, v_orb, grid, rc),
                                      el.coulumb_melem(core_orb, v_orb, v_orb,
                                                       grid, rc),
                                      el.exchange(core_orb, v_orb, grid, rc),
                                      el.exchange_melem(core_orb, v_orb, v_orb,
                                                        grid, rc))
    print(res.replace('.', ','))

for v in vsns:
    nv, lv, jv = str2nlj(v)
    pv, qv, env = hfd[v]
    v_orb = (pv, qv, lv, jv)
    test_with_orb(core_orb, v_orb, v, grid, rc)
