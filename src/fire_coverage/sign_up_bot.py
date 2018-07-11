
from enum import Enum
from os.path import join
from os import environ

def get_volunteer_names_from_summary(event_summary):
    '''
    Expects a summary of the form "Night (<volunteer1>, <volunteer2>, ...)"
    This returns a list of strings, split on ',', for everything between the parentheses.
    '''
    start = event_summary.find('(')
    end = event_summary.find(')')
    volunteer_names = event_summary[start+1:end].strip()
    return [name for name in volunteer_names.split(',') if name]
        
def extract_email(string):
    '''
    Expects a string like 'Rando Volunteer <email>'
    '''
    email = None
    if '<' in string and '>' in string:
        begin = string.rfind('<')
        end = string.find('>')
        email = string[begin+1: end]
    else:
        email = string
    assert('@' in email)
    return email

class SignUpBot:

    def __init__(self,
                 gcal_name = 'Nederland Fire',
                 config_path = join(environ['HOME'], '.fire_coverage')):

        import logging
        from .members import Members
        from .gsuite.gmail import GMail
        from .gsuite.gcalendar import GCalendar

        self.logger = logging.getLogger(__name__)

        credentials_path = join(config_path, 'nfv_gmail_credentials.json')
        secret_credentials_path = join(config_path, 'nfv_gmail_client_secret.json')
        scopes = GMail.Scopes.READONLY
        self.gmail = GMail(credentials_path, secret_credentials_path, scopes)

        credentials_path = join(config_path, 'gcal_credentials.json')
        secret_credentials_path = join(config_path, 'gcal_client_secret.json')
        scopes = GCalendar.Scopes.MODIFY
        self.gcal = GCalendar(credentials_path, secret_credentials_path, scopes)        
        self.gcal.select_calendar(gcal_name)
                                     
        members_filename = join(config_path, 'members')
        self.members = Members(members_filename)
                        
    def check_email(self, test = False):

        import datetime
        
        self.logger.debug("checking email...")
        
        messages = self.gmail.messages_list(q = 'is:unread')

        emails = list()
        if messages and messages['resultSizeEstimate'] == 0 :
            self.logger.info('No responses found.')
        else:
            
            t = datetime.date.today()
            start_of_today = datetime.datetime(t.year, t.month, t.day)
            
            for message in messages['messages']:

                # Only need the header data for now.
                m = self.gmail.messages_get(id = message['id'], format = 'metadata')
                if not test:
                    # Mark this email as 'read' but only when live
                    self.gmail.messages_modify(id = m['id'], body = {'removeLabelIds': ['UNREAD']})
                
                date_received = datetime.datetime.fromtimestamp(int(m['internalDate'])/1e3)
                if date_received > start_of_today:                
                    for d in m['payload']['headers']:                
                        if d['name'] == 'From':
                            email = extract_email(d['value'])
                            if email != 'nedfire.vols@gmail.com':
                                emails.append(email)
                        
        return emails

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

    def update_calendar(self, email_list, test = False):

        night_shift = self.get_night_shift_event()        
        names = get_volunteer_names_from_summary(night_shift['summary'])
        start_size = len(names)

        names.extend([self.members.members[email] for email in email_list])
        if len(set(names)) > start_size:
            # we have new volunteers, so we need an update
            volunteers = [v+',' for v in set(names)]
            vlist = ''.join(volunteers).rstrip(',') # remove the last comma
            summary = 'Night (%s)' % vlist
            self.logger.debug('summary = %s' % summary)
            
            night_shift['colorId'] = GCalendar.ColorID.BASIL.value
            night_shift['summary'] = summary
            if not test:
                self.gcal.update_event(night_shift)
            return True
        return False
                        
    def go(self, frequency = 10):
        '''
        Check email every 'frequency' minutes.
        '''        
        import time

        self.logger.debug("go")
        
        while True:
            email_list = self.check_email()
            if email_list:
                self.update_calendar(email_list)
            time.sleep(frequency * 60)
