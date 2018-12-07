#!/usr/bin/env python
#coding: utf8

import sys
from source_hfd_python.dirac_parse import subst_ind
dirac_out_filename, inv_end = sys.argv[1:]
total = {}
with open(dirac_out_filename, 'r') as dout:
    for orb_num, inds in subst_ind(dout, inv_end).iteritems():
        for k, inds_set in enumerate(inds):
            total[k] = total.get(k, set()).union(inds_set)

for iset in total.values():
    print("\n".join(str(ind) for ind in sorted(iset)))
