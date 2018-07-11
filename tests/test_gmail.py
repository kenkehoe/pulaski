#!/usr/bin/env python3
import unittest

from os import environ
from os.path import join

from fire_coverage.gsuite.gmail import GMail

class TestMembers(unittest.TestCase):
    
    def test_construction(self):
        config_path = join(environ['HOME'], '.fire_coverage')
        credentials_path = join(config_path, 'nfv_gmail_credentials.json')
        secret_credentials_path = join(config_path, 'nfv_gmail_client_secret.json')
        scopes = GMail.Scopes.READONLY
        gmail = GMail(credentials_path, secret_credentials_path, scopes)
        print(gmail)
        
unittest.main()
