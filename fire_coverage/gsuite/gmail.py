
class GMail:

    from enum import Enum
    class Scopes(Enum):
        READONLY = 'https://www.googleapis.com/auth/gmail.readonly'
        COMPOSE = 'https://www.googleapis.com/auth/gmail.compose'
        SEND = 'https://www.googleapis.com/auth/gmail.send'
        INSERT = 'https://www.googleapis.com/auth/gmail.insert'
        LABELS = 'https://www.googleapis.com/auth/gmail.labels'
        MODIFY = 'https://www.googleapis.com/auth/gmail.modify'
        METADATA = 'https://www.googleapis.com/auth/gmail.metadata'
        SETTINGS_BASIC = 'https://www.googleapis.com/auth/gmail.settings.basic'
        SETTINGS_SHARING = 'https://www.googleapis.com/auth/gmail.setttings.sharing'    
    
    def __init__(self, credentials_path, secret_credentials_path, scopes):

        import logging
        from .utilities import setup_mail_service 
        self.service = setup_mail_service(credentials_path, secret_credentials_path, scopes)
        self.logger = logging.getLogger(__name__)                
        
    def send_message(self, to, subject, body):

        import base64
        from email.mime.text import MIMEText        
        from apiclient import errors
        
        message = MIMEText(body)
        message['to'] = to 
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())

        try:
            email = self.service.users().messages().send(userId = "me", body = {'raw': raw.decode()} ).execute()
            self.logger.info('Message Id: %s' % email['id'])
        except errors.HttpError as error:
            self.logger.error('An error occurred: %s' % error)

    def __execute(self, method, **kwargs):
        from apiclient import errors
        messages = dict()
        try:
            if method == 'get':
                messages = self.service.users().messages().get(userId='me', **kwargs).execute()
            if method == 'modify':
                messages = self.service.users().messages().modify(userId='me', **kwargs).execute()
            if method == 'list':
                messages = self.service.users().messages().list(userId='me', **kwargs).execute()
        except Exception as error:
            self.logger.error(str(error))
        finally:
            return messages
                            
    def messages_get(self, **kwargs):
        return self.__execute('get', **kwargs)
        
    def messages_modify(self, **kwargs):
        return self.__execute('modify', **kwargs)
        
    def messages_list(self, **kwargs):
        return self.__execute('list', **kwargs)
            
