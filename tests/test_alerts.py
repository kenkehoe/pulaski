#!/usr/bin/env python3
import unittest

from fire_coverage.alerts import NightCoverageAlerts

class TestNightCoverageAlerts(unittest.TestCase):

    def test_get_night_shift_event(self):
        alert = NightCoverageAlerts(test = True)
        result = alert.get_night_shift_event()
        self.assertTrue(result)

    def test_go(self):
        alert = NightCoverageAlerts(test = True)
        alert.go()
        
unittest.main()
