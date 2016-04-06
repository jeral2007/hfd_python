#!/usr/bin/env python
import propdb
import argparse


def get_l(s):
    for l in 'spdfg':
        if l in s:
            return l.upper()


def take_orbs(dirac_output):
    import re
    en_pat = r"eigenvalue no. *(\d+): *(.*)"
    blank_pat = r"^[\s]*$"
    orbs = {}
    with open(dirac_output, 'r') as dfile:
        state = 0
        for line in dfile:
            if state == 0:
                gr = re.findall(en_pat, line)
                if gr is None or len(gr) == 0:
                    continue
                orb_num = int(gr[0][0])
                orb_energy = float(gr[0][1].replace('D', 'e'))
                if (orb_energy < 0e0):
                    state = 1
                    orbs[orb_num] = {'en': orb_energy}
            elif state == 1:
                if re.match(blank_pat, line):
                    state = 0
                    continue
                if '===' in line:
                    continue
                aux = line.split()
                atom = "".join(aux[2:4])
                key = '('+atom+')'+get_l(aux[4])
                if key not in orbs[orb_num]:
                    orbs[orb_num][key] = 0e0
                orbs[orb_num][key] += sum(float(c)**2 for c in aux[-4:])
    orbslist = []
    for n, orb in orbs.iteritems():
        norms = [k for k, v in orb.iteritems() if k != 'en'
                 and abs(v) > 1e-3]
        orbslist += [(n, str(orb['en']), " ".join(norms))]
        print "{}\t{}\t|{}|".format(*orbslist[-1])
    return orbslist


def put_orbs(args):
    orblist = take_orbs(args[0])
    comps = propdb.get_comps()
    comp_id = None
    for cid, cname, ctime in comps:
        if args[1].upper() == cname:
            comp_id = cid
            break
    if comp_id is None:
        raise KeyError("There is no such comp in database")
    for n, en, orbtype in orblist:
        propdb.add_orb(n, en, orbtype, comp_id)


def print_orbs(args):
    orbs = propdb.get_orbs_for_given_comp_pattern(args[0])
    for row in orbs:
        print("\t".join(map(str, row)))


parser = argparse.ArgumentParser(description='retrieve and put orbitals \
                                 information from core properties database')
parser.add_argument('--dbfile', default='props.db',
                    help='the database filename')
parser.add_argument('actions', nargs='+',
                    help="""following actions are supported:
show comp_match - print table of orbitals for computations that
                   match to the comp_match;
put output_file comp_name- takes orbital information from
dirac output file and puts it to the database""")

args = parser.parse_args()
propdb.initdb(args.dbfile)
if "put" == args.actions[0]:
    put_orbs(args.actions[1:])
elif "show" == args.actions[0]:
    print_orbs(args.actions[1:])
else:
    parser.print_usage()
