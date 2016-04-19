#!/usr/bin/env python2.7
#coding:utf8

from __future__ import print_function
from source_hfd_python.hfd_dat import Hfd
from source_hfd_python.makebas import Basis
import sys
import os.path

basfile, orbs = sys.argv[1], sys.argv[2:]
hfd = Hfd()
if not os.path.isfile(basfile):
    bas = Basis(hfd)
else:
    bas = Basis.load_bas(basfile)

for orb in orbs:
    bas.add_orbital(hfd, orb)

print(str(bas))
bas.save_bas(basfile)
