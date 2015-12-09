#!/usr/bin/env python
# coding: utf-8
import os
import sys
import os.path
import datetime
from propdb import *


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


def get_props_from_dir(pathname, name):
    props = {}
    for filename in filter(lambda t: os.path.isfile(pathname+'/'+t),
                           os.listdir(pathname)):
        res = get_prop_val(pathname+'/'+filename)
        if res is not None:
            assert(res[0] not in props)
            props[res[0]] = res[1]
    return props


def prop_as_tsv(props):
    res = '\n'.join(['{}\t{}'.format(pn, pv) for pn, pv in props.iteritems()
                    if pn != 'comp_name'])
    return res


initdb('props.db')
pathname = sys.argv[1]
name = sys.argv[2].upper()
current_time = datetime.datetime.strftime(datetime.datetime.now(),
                                          '%Y-%m-%d %H:%M')
print(current_time)
props = get_props_from_dir(pathname, name)
print (prop_as_tsv(props))
comps = get_comps()
print(comps)
comp_names = [comp[1] for comp in comps]

if name not in comp_names:
    comp_id = add_comp(name, current_time)
else:
    raise KeyError
print("---------")

for pn, pv in props.iteritems():
    prop_id = get_prop_id(pn)
    if prop_id is None:
        prop_id = add_prop(pn)
    add_propval(prop_id, comp_id, str(pv))
