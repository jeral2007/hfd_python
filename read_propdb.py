#!/usr/bin/env python

import propdb
import argparse


def print_comps(actions):
    for row in propdb.get_comps():
        print "\t".join(str(c) for c in row)


def print_props(actions):
    comp_match = "%"+actions[0]+"%"
    for row in propdb.get_props_for_given_comp_pattern(comp_match):
        print "\t".join(str(c) for c in row)

parser = argparse.ArgumentParser(
    description='display information from core properties database')
parser.add_argument('--dbfile', default='props.db',
                    help='the database filename')
parser.add_argument('actions', nargs='+',
                    help="""following actions are supported:
comps - print table with computations names and dates in the tsv format;

props comp_match - print table of properties values for computations that
                   match to the comp_match""")

args = parser.parse_args()
propdb.initdb(args.dbfile)
if "comps" == args.actions[0]:
    print_comps(args.actions[1:])
elif "props" == args.actions[0]:
    print_props(args.actions[1:])
else:
    parser.print_usage()
