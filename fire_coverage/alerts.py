
from enum import Enum
from os.path import join
from os import environ

class NightCoverageAlerts:

    class AlertLevel(Enum):
        NO_ALERT = 0
        CAUTION = 1
        WARNING = 2
        SEVERE = 3
    
    def __init__(self,
                 gcal_name = 'Nederland Fire',
                 config_path = join(environ['HOME'], '.fire_coverage'),
                 test = False):

        import logging
        
        from fire_coverage.hobo_db import DB
        from fire_coverage.gsuite.gmail import GMail
        from fire_coverage.gsuite.gcalendar import GCalendar

        self.logger = logging.getLogger(__name__)
        self.test = test
        self.logger.info("%s" % "Test" if self.test else "Production")
        
        credentials_path = join(config_path, 'nfv_gmail_credentials.json')
        secret_credentials_path = join(config_path, 'nfv_gmail_client_secret.json')
        scopes = GMail.Scopes.READONLY
        self.gmail = GMail(credentials_path, secret_credentials_path, scopes)

        credentials_path = join(config_path, 'gcal_credentials.json')
        secret_credentials_path = join(config_path, 'gcal_client_secret.json')
        scopes = GCalendar.Scopes.MODIFY
        self.gcal = GCalendar(credentials_path, secret_credentials_path, scopes)        
        self.gcal.select_calendar(gcal_name)
                                     
        self.members = HoboDB().members
                
    def __send_alert(self, alert_level):
        
        if alert_level == self.AlertLevel.NO_ALERT:
            to = 'alex.r.olivas@gmail.com'
            body = "All is good." 
            subject = '[NedFire Volunteers] NFPD is covered tonight' 

        if alert_level == self.AlertLevel.CAUTION:
            to = 'alex.r.olivas@gmail.com'
            body = 'I hope someone signs up today.'
            subject = '[NedFire Volunteers] No coverage tonight yet.'

        if alert_level == self.AlertLevel.WARNING:
            to = ','.join(self.members.members.keys())
            body = "To sign up for tonight's shift, simply respond to this email."
            subject = '[NedFire Volunteers] Please help out tonight. '
                
        if alert_level == self.AlertLevel.SEVERE:
            to = ','.join(self.members.members.keys())
            body = "To sign up for tonight's shift, simply respond to this email."
            subject = '[NedFire Volunteers] PLEEEAAASE help out tonight. Pretty please?'

        if not self.test:
            self.gmail.send_message(to, subject, body)
            
    def get_night_shift_event(self):

        import datetime
        
        now = datetime.datetime.utcnow()
        one_microsecond = datetime.timedelta(microseconds=1)
        # one microsecond before the stroke of midnight
        end_of_today = datetime.datetime(now.year, now.month, now.day + 1) - one_microsecond

        events = self.gcal.events(timeMin = now.isoformat() + 'Z',
                                  timeMax = end_of_today.isoformat() + 'Z',
                                  maxResults = 20,
                                  singleEvents=True,
                                  orderBy = 'startTime')
        
        for event in events:
            if 'Night' in event['summary']:
                return event

        
    def go(self):

        import datetime

        from .utilities import get_volunteer_names_from_summary
        from .gsuite.gcalendar import GCalendar
        
        night_shift = self.get_night_shift_event()
        
        volunteers = get_volunteer_names_from_summary(night_shift['summary'])
        if volunteers:
            self.logger.debug("The following are signed up for tonight:")
            for v in volunteers:
                self.logger.debug("   %s" % v)
                self.__send_alert(self.AlertLevel.NO_ALERT)
                event_color_id = GCalendar.ColorID.BASIL
        else:
            today = datetime.datetime.today()
            noon = datetime.datetime(today.year, today.month, today.day, 11, 59)
            eightpm = datetime.datetime(today.year, today.month, today.day, 19, 59)            
            now = datetime.datetime.now()
            
            self.logger.debug('No coverage.')
            if now < noon:
                event_color_id = GCalendar.ColorID.BANANA
                self.__send_alert(self.AlertLevel.CAUTION)
            if now > noon and now < eightpm:
                event_color_id = GCalendar.ColorID.TANGERINE
                self.__send_alert(self.AlertLevel.WARNING)
            if now > eightpm:
                event_color_id = GCalendar.ColorID.TOMATO
                self.__send_alert(self.AlertLevel.SEVERE)
                
        night_shift['colorId'] = event_color_id.value
        if not self.test:
            self.gcal.update_event(night_shift)
 
