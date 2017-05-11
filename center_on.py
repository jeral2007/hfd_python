#!/usr/bin/env python
import sys
try:
    file_in, file_out, center_num = sys.argv[1:]
    center_num = int(center_num)
except Exception:
    sys.stderr('usage: {} in_file out_file number of the center atom\n'.format(
        sys.argv[0]))

inf = open(file_in, 'r')
outf = open(file_out, 'w')
coords = []

for line in inf:
    if '$coord' in line:
        continue
    if '$end' in line:
        break
    coords += [line.split()]
    coords[-1][0:3] = [float(c) for c in coords[-1][0:3]]

for ii in xrange(len(coords)):
    if ii != center_num:
        for jj in xrange(3):
            coords[ii][jj] -= coords[center_num][jj]

print(coords)
