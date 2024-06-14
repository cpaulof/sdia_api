from datetime import datetime

from logger.base_logger import BaseLogger
import config


class FlightLogger(BaseLogger):
    def __init__(self, log_dir=config.FLIGHT_LOG_DIR):
        super(FlightLogger, self).__init__('LOG', 'txt', log_dir)
    
    def header_msg(self):
        return 'TIMESTAMP LATITUDE LONGITUDE ALTITUDE YAW ROLL PITCH VELOCITY_X VELOCITY_Y VELOCITY_Z FLY_TIME'.replace(' ', '\t')
    
    def create_msg(self, *args)->str:
        # args -> [LATITUDE LONGITUDE ALTITUDE YAW ROLL PITCH VELOCITY_X VELOCITY_Y VELOCITY_Z FLY_TIME]
        timestamp = str(datetime.now())
        lat, lng, alt, yaw, roll, pitch, vx, vy, vz, fly = args
        return f'{timestamp}\t{lat}\t{lng}\t{alt}\t{yaw}\t{roll}\t{pitch}\t{vx}\t{vy}\t{vz}\t{fly}'

