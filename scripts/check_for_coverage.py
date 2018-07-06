#!/usr/bin/env python3
"""

"""

from fire_coverage.alerts import NightCoverageAlerts

alert = NightCoverageAlerts()
alert.go(test=True)
