import os
from datetime import datetime

import config

class BaseLogger:
    def __init__(self, prefix, suffix, log_dir):
        self.prefix = prefix
        self.suffix = suffix
        self.abs_log_dir = os.path.join(config.BASEPATH, log_dir)
        if not os.path.exists(self.abs_log_dir):
            os.makedirs(self.abs_log_dir, exist_ok=True)
    
    def get_new_file(self):
        timestamp = str(datetime.now()).replace(':', '.')
        filename = f"{self.prefix}_{timestamp}.{self.suffix}"
        return open(os.path.join(self.abs_log_dir, filename), 'a')
    
    def get_last_file(self, create_new):
        filenames = os.listdir(self.abs_log_dir)
        if len(filenames) == 0 or create_new: 
            return self.get_new_file()
        filenames = [os.path.join(self.abs_log_dir, i) for i in filenames]
        filenames.sort(key=os.path.getmtime)
        filename = filenames[-1]
        return open(filename, 'a')
    
    def header_msg(self):
        raise NotImplementedError()
    def create_msg(self, *args):
        raise NotImplementedError()
    
    def write(self, *data, new_file=False):
        file_ = self.get_last_file(new_file)
        msg = self.create_msg(*data)
        if new_file: # write header to new file
            file_.write(self.header_msg())
            file_.write('\n')
        file_.write(msg)
        file_.write('\n')
        file_.close()
        

