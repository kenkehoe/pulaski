import pickle

from os import makedirs
from os import environ
from os.path import exists
from os.path import dirname
from os.path import join

class HoboDB:
    
    def __init__(self, filename = join(environ["HOME"], '.fire_coverage', 'hobo_db')):
        import logging
        from os.path import exists
        
        self.logger = logging.getLogger(__name__)
        self.filename = filename
        self.members = dict()
        
        if exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.members = pickle.load(f)
                print(self.members)
        else:
            self.logger.warning("File %s does not exist.  A new file will be created." % self.filename)
            makedirs(dirname(self.filename))

    def write(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.members, f)
        
    def __str__(self):
        result = ''
        for kv_pair in self.members.items():
            result += '%s : %s\n' % kv_pair
        return result
        
    def __del__(self):
        self.write()            
