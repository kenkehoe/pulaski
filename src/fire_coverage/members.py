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
        self.members[email] = entry
                
    def __del__(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.members, f)
            
