from datetime import datetime

from logger.base_logger import BaseLogger
import config


class ServerLogger(BaseLogger):
    def __init__(self, log_dir=config.SERVER_LOG_DIR):
        super(ServerLogger, self).__init__('LOG', 'txt', log_dir)
    
    def header_msg(self):
        return 'TIMESTAMP\tCODE_NAME\tSOURCE\tLENGTH\tMSG'
    
    def create_msg(self, *args)->str:
        # args -> [CODE_NAME, source, packet_length, msg]
        timestamp = str(datetime.now())
        code, source, length, msg = args
        return f'{timestamp}\t[{code}]\t{source}\t{length}\t{msg}'

