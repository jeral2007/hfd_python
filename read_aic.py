#!/usr/bin/env python
import glob
import sys
import cPickle

def parse_prop_file(pfile):
    for line in pfile:
        if 'value Re' not in line or any(sym*2 in line for sym in 'SPDFGH'):
            continue
        aux = line.split('=')
        val = aux[1]
        pname = aux[0].split('(')[1][:-1]
        return pname, val


try:
    prop_path, dump_file = sys.argv[1:]
except Exception:
    sys.stderr.write("""\
Usage:
    {} folder dump
folder is  folder of OneProp output (log/JReduced0.55 for example)\n
dump is dump file with props\n""".format(sys.argv[0]))

    sys.exit(1)

prop_prefix = "JRed_prop_ljm"
props = []
for prop_fname in glob.glob(prop_path + '/' + prop_prefix + '*'):
    with open(prop_fname, 'r') as pfile:
        props += [parse_prop_file(pfile)]

dumpf = open(dump_file, 'w')
cPickle.dump(props, dumpf)
print props
