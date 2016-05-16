#!/usr/bin/env python2.7
# coding:utf8
from __future__ import print_function
from source_hfd_python.makebas import Basis
import sys
__doc__ = """
##del_basfun.py
является частью source_hfd_python.
Удаляет функцию из файла с базисом, после чего перезаписывает его

Использование:
{progname} bas_file functions_to_delete

-bas_file -- имя файла с базисом
-functions_to_delete -- список орбиталей для удаления через пробел.

Пример:
~~~
{progname} basis.dat 4s1/2 5s1/2 5p3/2
~~~
эта команда удалит из basis.dat орбитали 4s1/2, 5s1/2 и 5p3/2

"""


def delete_orb(orb, basis):
    for lj in basis.ljblock:
        if orb in basis.ljblock[lj][0]:
            ind = basis.ljblock[lj][0].index(orb)
            basis.ljblock[lj][0].pop(ind)
            basis.ljblock[lj][1].pop(ind)
            return
try:
    basfile, orbs_to_delete = sys.argv[1], sys.argv[2:]
    basis = Basis.load_bas(basfile)
    for orb in orbs_to_delete:
        delete_orb(orb, basis)
except Exception:
    sys.stderr.write(__doc__.format(progname=sys.argv[0]))
    exit()
print(str(basis))
basis.save_bas(basfile)

