#!/usr/bin/env python2.7
#coding: utf8
from __future__ import print_function
from source_hfd_python.hfd_dat import Hfd
from source_hfd_python.makebas import Basis, ljblocks
from source_hfd_python.atom_strings import str2nlj
import sys
from scipy.linalg import inv
import scipy as sc
import source_hfd_python.hfd_in_out as hio
import source_hfd_python.electron_integrals as el

basfile, rc, corbs = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
basis = Basis.load_bas(basfile)
print("-"*10,"basis",'-'*10)
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
#  разложение орбиталей
coefs = {}
precoefs = {}
err = {}
for lj, orbnames, orbvals, smat in ljblocks(basis, nc):
    smat_inv = inv(smat)
    for orb in orbvals:
        pb, qb = orb[0:2]
        for s in vorb_names:
            n, lv, jv = str2nlj(s)
            if lv != lj[0] or jv != lj[1]:
                continue
            pv, qv, en = hfd[s]
            precoef = sc.trapz((pv[:nc]*pb[:nc]+
                                qv[:nc]*qb[:nc])*
                               basis.grid[1][:nc])*basis.grid[2]
            precoefs[s] = precoefs.get(s, []) + [precoef]
            err[s] = sc.trapz((pv[:nc]**2+qv[:nc]**2)*basis.grid[1][:nc])
            err[s] *= basis.grid[2]
    for s in vorb_names:
        n, lv, jv = str2nlj(s)
        if lv != lj[0] or jv != lj[1]:
            continue
        coefs[s] = sc.dot(smat_inv, precoefs[s])
        err[s] = (err[s] - sc.dot(coefs[s], precoefs[s]))/err[s]
        res = "\t".join([s]+map(str, coefs[s])+[str(err[s])])
        print(res.replace('.', ','))
# расчет энергий
print("-"*10)
for corb_str in corbs:
    res = 0e0
    for vorb_str in coefs:
        lv, jv = str2nlj(vorb_str)[1:]
        q = [aux['occ'] for aux in orb_prenames
             if aux['nl']+aux['j'] == vorb_str][0]
        # порядок матричных элементов задавался порядком orbvals как для
        # матричных элементов, так и для разложения. Поэтому они согласованны и
        # можно автомагически:
        res += q*sc.dot(coefs[vorb_str].T,
                        sc.dot(coulumbs[corb_str, lv, jv]-
                               exchanges[corb_str, lv, jv], coefs[vorb_str]))
    print("{}\t{}".format(corb_str, res).replace('.', ','))

