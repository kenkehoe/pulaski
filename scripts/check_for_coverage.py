#!/usr/bin/env python3

import logging, datetime
from fire_coverage.alerts import NightCoverageAlerts

# silence annoying output from google
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

now = datetime.datetime.now()

format_h = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_h = logging.FileHandler('/home/olivas/.fire_coverage/logs/check_for_coverage_%s.log' %
                             str(now).replace(' ', '_'))
file_h.setFormatter(format_h)

alert = NightCoverageAlerts()
alert.logger.addHandler(file_h)
alert.logger.setLevel(logging.DEBUG)
alert.go()
