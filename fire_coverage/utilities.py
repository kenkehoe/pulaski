
def get_volunteer_names_from_summary(event_summary):
    '''
    Expects a summary of the form "Night (<volunteer1>, <volunteer2>, ...)"
    This returns a list of strings, split on ',', for everything between the parentheses.
    '''
    start = event_summary.find('(')
    end = event_summary.find(')')
    volunteer_names = event_summary[start+1:end].strip()
    return [name for name in volunteer_names.split(',') if name]


