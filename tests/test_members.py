#!/usr/bin/env python3
import unittest

from fire_coverage.members import Members

class TestMembers(unittest.TestCase):
    
    def test_add_members(self):
        m = Members('deleteme') # brand new file
        m.add_member('testuser1@gmail.com', 'testuser1')
        m.add_member('testuser2@gmail.com', 'testuser2')
        m.add_member('testuser3@gmail.com', 'testuser3')
        self.assertEqual(len(m.members), 3)

    def test_add_new_member(self):
        m = Members('deleteme') # open file from previous test
        m.add_member('testuser4@gmail.com', 'testuser4')
        self.assertEqual(len(m.members), 4)

    def test_print(self):
        m = Members('deleteme') # open file from previous test
        self.assertEqual(len(str(m)), 128)

    def test_remove_member(self):
        m = Members('deleteme') # open file from previous test
        m.remove_member('testuser2@gmail.com')
        self.assertEqual(len(m.members), 3)    
        
    @classmethod
    def tearDownClass(self):
        import os
        os.unlink('deleteme')
        
unittest.main()
