#!/usr/bin/env python3
import unittest

from fire_coverage.members import Members

class TestMembers(unittest.TestCase):
    
    def test_add_members(self):
        m = Members('deleteme') # brand new file
        m.add_member('testuser1', 'testuser1@gmail.com')
        m.add_member('testuser2', 'testuser2@gmail.com')
        m.add_member('testuser3', 'testuser3@gmail.com')
        self.assertEqual(len(m.members), 3)

    def test_add_new_member(self):
        m = Members('deleteme') # open file from previous test
        m.add_member('testuser4', 'testuser4@gmail.com')
        self.assertEqual(len(m.members), 4)
        
    @classmethod
    def tearDownClass(self):
        import os
        os.unlink('deleteme')
        
unittest.main()
