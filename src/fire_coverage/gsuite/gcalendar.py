from enum import Enum

class GCalendar:

    class ColorID(Enum):
        BANANA = 5
        TANGERINE = 6
        BASIL = 10
        TOMATO = 11
    
    class Scopes(Enum):
        READONLY = 'https://www.googleapis.com/auth/calendar.readonly'
        MODIFY = 'https://www.googleapis.com/auth/calendar'
    
    def __init__(self, credentials_path, secret_credentials_path, scopes):

        import logging
        from .utilities import setup_calendar_service
        
        self.logger = logging.getLogger(__name__)        
        self.gcal_id = 'primary'        
        self.service = setup_calendar_service(credentials_path, secret_credentials_path, scopes)

    def select_calendar(self, calendar_name):
        '''
        Sets self.gcal_id to the ID matching self.gcal_name
        '''
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry['summary'] == calendar_name:          
                    self.gcal_id = calendar_list_entry['id']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    def events(self, **kwargs):
        results =  self.service.events().list(calendarId = self.gcal_id, **kwargs). execute()
        return results.get('items', [])

    def update_event(self, event):
        self.service.events().update(calendarId = self.gcal_id,
                                     eventId = event['id'],
                                     body = event).execute()
    
