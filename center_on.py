#!/usr/bin/env python
import sys
try:
    file_in, center_num = sys.argv[1:]
    center_num = int(center_num)
except Exception:
    sys.stderr.write('usage: {} in_file \
 number of the center atom\n'.format(
        sys.argv[0]))
    sys.exit(0)

inf = open(file_in, 'r')
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

coords[center_num][0:3] = [0, 0, 0]

fmt_str = "    {:.14f}" * 3 + "    {}"
print('$coord')

for c in coords:
    print(fmt_str.format(*c))

print('$end')
