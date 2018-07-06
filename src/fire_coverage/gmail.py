from enum import Enum
from os.path import join
from os import environ

class AlertLevel(Enum):
    NO_ALERT = 0
    WARNING = 1
    SEVERE = 2

class GMail:

    def __init__(self, config_path = join(environ['HOME'], '.fire_coverage')):
                 
        from apiclient.discovery import build
        from httplib2 import Http
        from oauth2client import file, client, tools
        
        # Setup the GMail API
        SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
        store = file.Storage(join(config_path, 'gmail_credentials.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(join(config_path,'gmail_client_secret.json'), SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))

        member_list_path = join(config_path, 'member_list')
        self.member_email_dict = dict()
        with open(member_list_path) as f:
            for line in f.readlines():
                name = line.split(':')[0]
                email = line.split(':')[1].strip()
                self.member_email_dict[name] = email
                
    def _create_message(self, body, to, subject):

        import base64
        from email.mime.text import MIMEText        
        
        message = MIMEText(body)
        message['to'] = to 
        #message['from'] = 'nedfire.vols@gmail.com'
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw.decode()}
    
    def send_alert(self, alert_level, body):

        from apiclient import errors
        
        if alert_level == AlertLevel.NO_ALERT:
            # send an email to myself, just to know the system is running
            body = "All is good."
            to = 'alex.r.olivas@gmail.com'
            subject = 'NFPD is covered tonight'
            message = self._create_message(body, to, subject)
        else:
            email_list = [v+',' for k,v in self.member_email_dict.items()]
            to = ''.join(email_list)

            if alert_level == AlertLevel.WARNING:            
                body = "All is not good."
                subject = 'NedFire Volunteers - Please help out tonight. '
                message = self._create_message(body, to, subject)
                
            if alert_level == AlertLevel.SEVERE:            
                body = "All is really not good."
                subject = 'NedFire Volunteers - PLEEEAAASE help out tonight. Pretty please?'
                message = self._create_message(body, to, subject)            

        try:
            email = self.service.users().messages().send(userId = "me", body = message).execute()
            print('Message Id: %s' % email['id'])
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            
                       
