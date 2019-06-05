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

from fire_coverage.hobo_db import HoboDB

filename = join(environ['HOME'], '.fire_coverage', 'members')
db = HoboDB(filename)

if args.add:
    db.members[args.email] = args.nickname
    
if args.remove:
    del db.members[args.email]

if args.pprint:
    print(str(db))

print("There are %d members in %s." % (len(db.members), filename))
