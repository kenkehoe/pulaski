import logging

from enum import Enum
from os.path import join
from os import environ

def get_volunteer_names(event_summary):
    '''
    Expects a summary of the form "Night (<volunteer1>, <volunteer2>, ...)"
    This returns a list of strings, split on ',', for everything between the parentheses.
    '''
    start = event_summary.find('(')
    end = event_summary.find(')')
    volunteer_names = event_summary[start+1:end].strip()
    return [name for name in volunteer_names.split(',') if name]

def is_today(date):
    '''
    Date from gmail is of the form 'Thu, 5 Jul 2018 20:04:33 -0600'
    '''
    import datetime
    today = datetime.date.today()
    
    labels = ['jan','feb','mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    _month = {k:v+1 for v,k in enumerate(labels)} 
    
    ds = date.split()
    year = int(ds[3])
    month = _month[ds[2].lower()]
    day = int(ds[1])

    return bool(datetime.date(year, month, day) == today)
    
    
def parse_volunteer_list(volunteers):
    '''
    Expects a list of 'Rando Volunteer <email>'
    '''
    result = list()
    for v in volunteers:
        if '<' in v and '>' in v:
            begin = v.rfind('<')
            end = v.find('>')
            email = v[begin+1: end]
        else:
            email = v
        assert('@' in email)
        result.append(email)
    return result                      

gcal_color_map = {'yellow': 5,
                  'orange': 6,
                  'green': 10,
                  'red': 11}

class SignUpBot:

    def __init__(self,
                 gcal_name = 'Nederland Fire',
                 config_path = join(environ['HOME'], '.fire_coverage')):
                 
        from apiclient.discovery import build
        from httplib2 import Http
        from oauth2client import file, client, tools

        self.gcal_name = gcal_name
        self.logger = logging.getLogger(__name__)
        
        # Setup the GMail API
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        store = file.Storage(join(config_path, 'nfv_gmail_credentials.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(join(config_path,'nfv_gmail_client_secret.json'), SCOPES)
            creds = tools.run_flow(flow, store)
        self.gmail_service = build('gmail', 'v1', http=creds.authorize(Http()))
                             

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage(join(config_path, 'gcal_credentials.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(join(config_path,'gcal_client_secret.json'), SCOPES)
            creds = tools.run_flow(flow, store)
        self.gcal_service = build('calendar', 'v3', http=creds.authorize(Http()))


        self.__set_gcal_id()
        assert(self.gcal_id)        
                             
        member_list_path = join(config_path, 'member_list')
        self.member_email_dict = dict()
        with open(member_list_path) as f:
            for line in f.readlines():
                if not line :
                    continue
                name = line.split(':')[0]
                email = line.split(':')[1].strip()
                nickname = line.split(':')[2].strip()
                self.member_email_dict[email] = nickname
                
        self.volunteers = set()

    def __set_gcal_id(self):
        '''
        Sets self.gcal_id to the ID matching self.gcal_name
        '''
        page_token = None
        while True:
            calendar_list = self.gcal_service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry['summary'] == self.gcal_name:          
                    self.gcal_id = calendar_list_entry['id']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        
    def check_email(self):

        self.logger.debug("checking email...")
        
        from apiclient import errors
        import datetime
        today = datetime.date.today()

        try:
            # Apparently in google's world yesterday is still *after* today...go figure.
            # This does still limit the number of responses however.  I'll file a bug report 
            # at some point.  I'm sure this is not intended behavior
            query = 'subject:NedFire Volunteers AND after:%s' % str(today)
            response  = self.gmail_service.users().messages().list(userId='me', q = query).execute()
        except errors.HttpError as error:
            print('An error occured: %s' % error)
            
        if response['resultSizeEstimate'] == 0 :
            self.logger.info('No responses found.')
        else:
            
            start_size = len(self.volunteers)
            volunteers = list()

            for message in response['messages']:
                m = self.gmail_service.users().messages().get(userId='me', id = message['id']).execute()
                print('\n',m['payload'], '\n')
                vname = None
                sent_today = False
                for d in m['payload']['headers']:                
                    if d['name'] == 'From':
                        vname = d['value']
                    if d['name'] == 'Date':
                        self.logger.debug('*** date = %s' % d['value'])
                        self.logger.debug('    is_today = %s' % is_today(d['value']))
                        sent_today = is_today(d['value'])
                if sent_today and vname:
                    volunteers.append(vname)
                    
            volunteers.extend(self.volunteers)
            self.volunteers = set(volunteers)

            if len(self.volunteers) > start_size:
                self.update_calendar()

    def update_calendar(self):

        import datetime
        
        now = datetime.datetime.utcnow()
        one_microsecond = datetime.timedelta(microseconds=1)
        # one microsecond before the stroke of midnight
        end_of_today = datetime.datetime(now.year, now.month, now.day + 1) - one_microsecond
        
        events_result = self.gcal_service.events().list(calendarId = self.gcal_id,
                                                        timeMin = now.isoformat() + 'Z',
                                                        timeMax = end_of_today.isoformat() + 'Z',
                                                        maxResults = 20,
                                                        singleEvents=True,
                                                        orderBy = 'startTime').execute()

        # these should be sorted in order
        events = events_result.get('items', [])
        
        coverage = False
        night_shift = None
        for event in events:
            if 'Night' in event['summary']:
                night_shift = event
                break

        volunteers = get_volunteer_names(night_shift['summary'])
        start_size = len(volunteers)
        print(parse_volunteer_list(self.volunteers))
        volunteers.extend([self.member_email_dict[e] for e in parse_volunteer_list(self.volunteers)])
        if len(set(volunteers)) > start_size:
            # we need an update
            # we have new volunteers                
            volunteers = [v+',' for v in set(volunteers)]
            vlist = ''.join(volunteers).rstrip(',')
            summary = 'Night (%s)' % vlist
            self.logger.debug('summary = %s' % summary)
            
            night_shift['colorId'] = gcal_color_map['green']
            night_shift['summary'] = summary
            self.gcal_service.events().update(calendarId = self.gcal_id,
                                              eventId = night_shift['id'],
                                              body = night_shift).execute()
                        
    def go(self, frequency = 10):
        '''
        Check email every 'frequency' minutes.
        '''        
        import time

        self.logger.debug("go")
        
        while True:
            self.check_email()
            time.sleep(frequency * 60)
