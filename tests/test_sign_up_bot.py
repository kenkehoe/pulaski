#!/usr/bin/env python3
import unittest

from fire_coverage.sign_up_bot import SignUpBot


class TestSignUpBot(unittest.TestCase):

    def test_check_email(self):
        bot = SignUpBot()
        result = bot.check_email(test = True)
        self.assertTrue(isinstance(result, list))

    def test_get_night_shift_event(self):
        bot = SignUpBot()
        result = bot.get_night_shift_event()
        self.assertTrue(result)

    def test_update_calendar(self):
        bot = SignUpBot()
        updated = bot.update_calendar(['alex.r.olivas@gmail.com'], test = True)
        self.assertTrue(result)
        
unittest.main()
