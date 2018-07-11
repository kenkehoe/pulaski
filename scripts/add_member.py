#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Add a new member.')
parser.add_argument('nickname', help='Short member nickname...not their full name.')                    
parser.add_argument('email', help="Member's email address.")
args = parser.parse_args()

from os import environ
from os.path import join

from fire_coverage.members import Members

filename = join(environ['HOME'], '.fire_coverage', 'members')
m = Members(filename)
m.add_member(args.email, args.nickname)
print("There are %d members in %s." % (len(m.members), filename))
