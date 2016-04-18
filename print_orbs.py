#!/usr/bin/env python

import sys
import hfd_in_out


def data_shell(orbs):
    return [orb for orb in orbs if orb['kp'] < 0.5]  # unfrozen shells only

hfdres, shells = sys.argv[1], sys.argv[2:]
orbs, en = hfd_in_out.orbitals(open(hfdres, 'r'))

unfrozen = data_shell(orbs)
print len(unfrozen)

for data in data_shell(orbs):
    print("{}{}\t{}".format(data['nl'], data['j'],
                            str(data['en']).replace('.', ',')))
print(en)
