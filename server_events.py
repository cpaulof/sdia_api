
from server import server, pkt_parser, pkt_builder
from logger.flight_logger import FlightLogger
from logger.server_logger import ServerLogger

from icecream import ic

## init loggers ####
loggers = {
    'telemetry': FlightLogger(),
    'server': ServerLogger() 
}
def get_logger(service):
    return loggers.get(service, None)

class ServerEvents:
    def __init__(self):
        self.server = None
        self.telemetry_data = {
            'lat': None,
            'lng': None,
            'alt': None,
            'yaw': None,
            'row': None,
            'pitch': None,
            'vel_x': None,
            'vel_y': None,
            'vel_z': None,
            'time': None,
        }

        self.drone_status = {
            'GPS_SIGNAL': 0,
            'ATTITUDE': 0,
            'FLYING': False,
        }

        self.telemetry_logger = get_logger('telemetry')
        self.telemetry_logger_header = True
    ############## listeners
    def create_dict_updater_listener(self, dict_name, keys):
        def listener(values):
            dict_obj = getattr(self, dict_name)
            dict_obj.update(zip(keys, values))
        return listener
    
    def telemetry_log_writer(self, data):
        # ic(self.telemetry_data)
        if self.telemetry_logger and self.drone_status['FLYING']:
            self.telemetry_logger.write(*data, new_file=self.telemetry_logger_header)
            self.telemetry_logger_header = False

    def telemetry_listener(self):
        keys = ['lat', 'lng', 'alt', 'yaw', 'row', 'pitch', 'vel_x', 'vel_y', 'vel_z', 'time']
        listener = self.create_dict_updater_listener('telemetry_data', keys)
        self.add_listener('FLIGHT_RECORD', listener)
        self.add_listener('FLIGHT_RECORD', self.telemetry_log_writer)

    def initialize_default_listeners(self):
        self.telemetry_listener()
        self.add_listener('START_TAKEOFF', lambda _:self.drone_status.update([('FLYING', True)]))
        self.add_listener('START_LANDING', lambda _:self.drone_status.update([('FLYING', False)]))
        self.add_listener('START_LANDING', lambda _:setattr(self, 'telemetry_logger_header', True))
    ################
    def check_server_status(self):
        if self.server is None:
            s = -1
        elif self.server.running:
            s = 1
        else:
            s = 0
        return s
    
    def stop_server(self):
        if self.server:
            self.server.close()

    def start_server(self):
        if self.check_server_status() == 1:
            self.stop_server()
        self.server = server.Listener()
    

    def get_value(self, key):
        pass

    def add_listener(self, code_name, callback):
        code, _ = pkt_builder.BUILD_CODES.get(code_name, None)
        if code is None: return
        pkt_parser.add_handler(code, callback)
    
    def remove_listener(self, code_name, callback):
        code, _ = pkt_builder.BUILD_CODES.get(code_name, None)
        if code is None: return
        try:
            pkt_parser.HANDLERS[code].remove(callback)
        except ValueError: pass



