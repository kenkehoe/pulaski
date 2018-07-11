
def _setup_service(credentials_path, secret_credentials_path, scopes_url, *args):
    from apiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file, client, tools

    # Setup the Calendar API
    storage = file.Storage(credentials_path)
    credentials = storage.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secret_credentials_path, scopes_url)
        credentials = tools.run_flow(flow, storage)
    return build(*args, http = credentials.authorize(Http()))

def setup_calendar_service(credentials_path, secret_credentials_path, scopes):    
    return _setup_service(credentials_path, secret_credentials_path, scopes.value,
                          'calendar', 'v3')                

def setup_mail_service(credentials_path, secret_credentials_path, scopes):    
    return _setup_service(credentials_path, secret_credentials_path, scopes.value,
                          'gmail', 'v1')
