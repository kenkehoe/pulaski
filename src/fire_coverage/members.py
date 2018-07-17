import pickle

class Members:

    from os.path import exists
    
    def __init__(self, filename):
        import logging
        from os.path import exists
        
        self.logger = logging.getLogger(__name__)
        self.filename = filename
        self.members = dict()
        
        if exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.members = pickle.load(f)
        else:
            self.logger.warning("File %s does not exist.  A new file will be created." % self.filename)

    def add_member(self, email, entry):
        assert('@' in email)
        self.members[email] = entry
                
    def remove_member(self, email):
        del self.members[email]

    def __str__(self):
        result = ''
        for kv_pair in self.members.items():
            result += '%s : %s\n' % kv_pair
        return result
        
    def __del__(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.members, f)
            
