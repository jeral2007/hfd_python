#!/usr/bin/env python
#coding: utf8

from __future__ import print_function
from source_hfd_python.dirac_parse import dirac_total_energies

print("test on correct output file")
dout = open('correct.out')
print(dirac_total_energies(dout))
dout.close()
print("test on invalid file")
dout = open('invalid.out')
print(dirac_total_energies(dout))
dout.close()

