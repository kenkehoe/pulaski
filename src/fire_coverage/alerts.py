
def get_volunteer_names(event_summary):
    '''
    Expects a summary of the form "Night (<volunteer1>, <volunteer2>, ...)"
    This returns a list of strings, split on ',', for everything between the parentheses.
    '''
    start = event_summary.find('(')
    end = event_summary.find(')')
    volunteer_names = event_summary[start+1:end].strip()
    return [name for name in volunteer_names.split(',') if name]

gcal_color_map = {'yellow': 5,
                  'orange': 6,
                  'green': 10,
                  'red': 11}


from os.path import join
from os import environ

class NightCoverageAlerts:

    def __init__(self,
                 gcal_name = 'Nederland Fire',
                 config_path = join(environ['HOME'], '.fire_coverage')):

        from apiclient.discovery import build
        from httplib2 import Http
        from oauth2client import file, client, tools
        import logging
        
        self.gcal_name = gcal_name
        self.logger = logging.getLogger(__name__)
        
        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage(join(config_path, 'gcal_credentials.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(join(config_path,'gcal_client_secret.json'), SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('calendar', 'v3', http=creds.authorize(Http()))

        self.__set_gcal_id()
        assert(self.gcal_id)        
                
    def __send_alert(self, alert_level):
        from fire_coverage.gmail import GMail        
        email_client = GMail()        
        email_client.send_alert(alert_level, 'Test')
        
    def __set_gcal_id(self):
        '''
        Sets self.gcal_id to the ID matching self.gcal_name
        '''
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry['summary'] == self.gcal_name:          
                    self.gcal_id = calendar_list_entry['id']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    def go(self, test = False):

        import datetime
        from fire_coverage.gmail import AlertLevel        
        
        now = datetime.datetime.utcnow()
        one_microsecond = datetime.timedelta(microseconds=1)
        # one microsecond before the stroke of midnight
        end_of_today = datetime.datetime(now.year, now.month, now.day + 1) - one_microsecond
        
        events_result = self.service.events().list(calendarId = self.gcal_id,
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
        if volunteers:
            self.logger.debug("The following are signed up for tonight:")
            for vol in volunteers:
                self.logger.debug("   %s" % vol)
                self.__send_alert(AlertLevel.NO_ALERT)
                event_color = 'green'                    
        else:
            today = datetime.datetime.today()
            noon = datetime.datetime(today.year, today.month, today.day, 11, 59)
            eightpm = datetime.datetime(today.year, today.month, today.day, 19, 59)            
            now = datetime.datetime.now()
            
            self.logger.debug('No coverage.')
            if now < noon:
                event_color = 'yellow'
                self.__send_alert(AlertLevel.CAUTION)
            if now > noon and now < eightpm:
                event_color = 'orange'
                self.__send_alert(AlertLevel.WARNING)
            if now > eightpm:
                event_color = 'red'
                self.__send_alert(AlertLevel.SEVERE)
                
        night_shift['colorId'] = gcal_color_map[event_color]
        self.service.events().update(calendarId = self.gcal_id,
                                     eventId = night_shift['id'],
                                     body = night_shift).execute()
 
