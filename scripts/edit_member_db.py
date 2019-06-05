#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Edit member database (i.e. pickle file).')
parser.add_argument('--name', '-n', dest='name')
parser.add_argument('--email', '-e', dest='email')
parser.add_argument('--pprint', '-p', dest='pprint', action='store_true', default = False)
parser.add_argument('--add', '-a', dest='add', action='store_true', default = False)
parser.add_argument('--remove', '-r', dest='remove', action='store_true', default = False)
args = parser.parse_args()

from os import environ
from os.path import join

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['fire_coverage']

if args.add:
    member_collection = db['members']
    members = member_collection.insert_one({'name': args.name, 'email': args.email})
    
if args.remove:
    member_collection = db['members']
    if args.name:
        member = member_collection.remove({'name': args.name})
    elif args.email:
        member = member_collection.remove({'email': args.email})
                
print("There are %d members." % db.members.count_documents({}))
