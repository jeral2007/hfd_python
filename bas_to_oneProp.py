#!/usr/bin/env python2.7
#coding: utf8
from __future__ import print_function
from source_hfd_python.hfd_dat import Hfd
from source_hfd_python.makebas import Basis, ljblocks
from source_hfd_python.atom_strings import str2nlj
import sys
import scipy as sc
import source_hfd_python.hfd_in_out as hio
import source_hfd_python.electron_integrals as el
# Forward and back


class ArgSortError(Exception):
    pass


def argsort(lst, cmp=None, key=None, reverse=False):
    if cmp is None and key is None:
        aux = sorted(enumerate(lst), reverse=reverse, key=lambda p: p[1])
    elif key is not None:
        aux = sorted(enumerate(lst), reverse=reverse, key=lambda p: key(p[1]))
    elif cmp is not None:
        aux = sorted(enumerate(lst), reverse=reverse,
                     cmp=lambda x, y: cmp(x[1], y[1]))
    else:
        raise ArgSortError("argsort called with argcmp and argkey together")
    return [p[0] for p in aux]


basfile, rc, corbs = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
basis = Basis.load_bas(basfile)
print("-"*10, "basis", '-'*10)
print(basis)
print("-"*25)
nc = sc.where(basis.grid[0] > rc)[0][0]+1
orb_prenames, en = hio.orbitals(open('hfd.res', 'r'))

vorb_names = [aux['nl']+aux['j'] for aux in orb_prenames
              if aux['kp'] < 0.5]
hfd = Hfd()
#  матричные элементы
exchanges = {}
coulumbs = {}
for lj, orb_names, orbvals, smat in ljblocks(basis, nc):
    for corb_str in corbs:
        ncc, lc, jc = str2nlj(corb_str)
        pc, qc, en = hfd[corb_str]
        c_orb = (pc, qc, lc, jc)
        N = len(orbvals)
        exmat = sc.zeros((N, N))
        coulmat = sc.zeros((N, N))
        for i in xrange(N):
            for j in xrange(i+1):
                exmat[i, j] = el.exchange_melem(c_orb,
                                                orbvals[i], orbvals[j],
                                                basis.grid, rc)
                coulmat[i, j] = el.coulumb_melem(c_orb,
                                                 orbvals[i], orbvals[j],
                                                 basis.grid, rc)
                exmat[j, i] = exmat[i, j]
                coulmat[j, i] = coulmat[i, j]
        exchanges[(corb_str, lj[0], lj[1])] = exmat
        coulumbs[(corb_str, lj[0], lj[1])] = coulmat

ls = []
js = []
mjs = []
orbns = []
for lj, orb_names, orbvals, smat in ljblocks(basis, nc):
    for orbn in orb_names:
        for mj in sc.arange(-lj[1], lj[1]+1):
            ls += [lj[0]]
            js += [lj[1]]
            mjs += [mj]
            orbns += [orbn]

# l,n, -j, m order
inds = argsort([100000*x+1000*int(z[0])+100*(10-y)+q for x, y, z, q in
                zip(ls, js, orbns, mjs)])
ls = [ls[i] for i in inds]
js = [js[i] for i in inds]
mjs = [mjs[i] for i in inds]
orbns = [orbns[i] for i in inds]
print(zip(orbns[0:20], mjs[0:20]))
N = len(ls)
cshs_file = open('chshs.txt', 'w')

for corb in corbs:
    chemshift = sc.zeros((N, N))
    for i in xrange(N):
        for j in xrange(N):
            if ls[i] != ls[j] or js[i] != js[j] or mjs[i] != mjs[j]:
                continue
            cmat = coulumbs[(corb, ls[i], js[i])]
            exmat = exchanges[(corb, ls[i], js[i])]
            orb_names = basis.ljblock[(ls[i], js[i])][0]

            mat_i = orb_names.index(orbns[i])
            mat_j = orb_names.index(orbns[j])
            chemshift[i, j] = cmat[mat_i, mat_j] - exmat[mat_i, mat_j]

    fmt = "        ".join(['{:.16f}']*N)+"\n"
    cshs_file.write("""  JRpropertyJML
title=ljm electron part of {} orbital energy shift
  dens=total
  {}
""".format(corb.replace('/', '_'), N))

    for i in xrange(N):
        cshs_file.write(fmt.format(*chemshift[i, :]))
