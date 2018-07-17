#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Edit member database (i.e. pickle file).')
parser.add_argument('--nickname', '-n', dest='nickname')
parser.add_argument('--email', '-e', dest='email')
parser.add_argument('--pprint', '-p', dest='pprint', action='store_true', default = False)
parser.add_argument('--add', '-a', dest='add', action='store_true', default = False)
parser.add_argument('--remove', '-r', dest='remove', action='store_true', default = False)
args = parser.parse_args()

from os import environ
from os.path import join

from fire_coverage.members import Members

filename = join(environ['HOME'], '.fire_coverage', 'members')
m = Members(filename)

if args.add:
    m.add_member(args.email, args.nickname)
    
if args.remove:
    m.remove_member(args.email)

if args.pprint:
    print(str(m))

print("There are %d members in %s." % (len(m.members), filename))
