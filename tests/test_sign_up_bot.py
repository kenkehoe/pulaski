#!/usr/bin/env python3
import unittest

from fire_coverage.sign_up_bot import SignUpBot


class TestSignUpBot(unittest.TestCase):

    def test_check_email(self):
        bot = SignUpBot(test = True)
        result = bot.check_email()
        self.assertTrue(isinstance(result, list))

    def test_get_night_shift_event(self):
        bot = SignUpBot(test = True)
        result = bot.get_night_shift_event()
        self.assertTrue(result)

    def test_update_calendar(self):
        bot = SignUpBot(test = True)
        updated = bot.update_calendar(['alex.r.olivas@gmail.com'])
        self.assertTrue(updated)
        
unittest.main()
