#!/usr/bin/env python3

import logging, datetime
from fire_coverage.sign_up_bot import SignUpBot

# silence annoying output from google
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

now = datetime.datetime.now()

format_h = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_h = logging.FileHandler('/home/olivas/.fire_coverage/logs/launch_sign_up_bot_%s.log' %
                             str(now).replace(' ', '_'))
file_h.setFormatter(format_h)

sign_up_bot = SignUpBot()
sign_up_bot.logger.addHandler(file_h)
sign_up_bot.logger.setLevel(logging.DEBUG)
try:
    sign_up_bot.go()
except Exception as error:
    sign_up_bot.logger.error(str(error))

