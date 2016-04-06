#!/usr/bin/env python

import sys
import hfd_in_out

def data_shell(orbs, shells):
    for shell in shells:
        nl, j = shell[0:2], shell[2:]
        for orb in orbs:
            if orb['nl'] == nl and orb['j'] == j:
                yield orb


hfdres, shells = sys.argv[1], sys.argv[2:]
orbs, en = hfd_in_out.orbitals(open(hfdres, 'r'))
for data in data_shell(orbs, shells):
    print("{}{}\t{}".format(data['nl'], data['j'],
                            str(data['en']).replace('.', ',')))
