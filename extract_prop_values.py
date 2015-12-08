#!/usr/bin/env python
# coding: utf-8
import os, sys
import os.path
import math


def get_prop_val(filename):
    import re
    pat_re = r"value Re \(([^)]+)\) = +(.*)"
    pat_im = r"value Im \(([^)]+)\) = +(.*)"
    with open(filename, 'r') as fs:
        line = fs.readline()
        if '------' not in line:
            return
        line = fs.readline()
        gr = re.findall(pat_re, line)
        if gr is None:
            return
        prop_name = gr[0][0]
        reval = gr[0][1]
        line = fs.readline()
        gr = re.findall(pat_im, line)
        if gr is None:
            return
        if prop_name != gr[0][0]:
            return
        imval = gr[0][1]
        if abs(float(imval)/(float(reval)+1e-10)) > 1e-10:
            return (prop_name, float(reval) + 1j*float(imval))
        else:
            return (prop_name, float(reval))


pathname = sys.argv[1]
name = sys.argv[2]
props = {'comp_name': name}
for filename in filter(os.path.isfile, os.listdir(pathname)):
    res = get_prop_val(pathname+'/'+filename)
    if res is not None:
        assert(res[0] not in props)
        props[res[0]] = res[1]

print props
