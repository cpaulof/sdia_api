
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
        self.KEYS = {}
        self.listeners = []
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
        lat, lng, alt = data
        pitch = self.KEYS.get('ATTITUDE_PITCH', None)
        yaw = self.KEYS.get('ATTITUDE_YAW', None)
        roll = self.KEYS.get('ATTITUDE_ROLL', None)
        vel_x = self.KEYS.get('VELOCITY_X', None)
        vel_y = self.KEYS.get('VELOCITY_Y', None)
        vel_z = self.KEYS.get('VELOCITY_Z', None)
        time_ = self.KEYS.get('FLY_TIME_IN_SECONDS', None)
        if self.telemetry_logger:
            self.telemetry_logger.write(lat, lng, alt, pitch, yaw, roll, vel_x, vel_y, vel_z, time_, new_file=self.telemetry_logger_header)
            self.telemetry_logger_header = False

    # def telemetry_listener(self):
    #     keys = ['lat', 'lng', 'alt', 'yaw', 'row', 'pitch', 'vel_x', 'vel_y', 'vel_z', 'time']
    #     listener = self.create_dict_updater_listener('telemetry_data', keys)
    #     self.add_listener('FLIGHT_RECORD', listener)
    #     self.add_listener('FLIGHT_RECORD', self.telemetry_log_writer)

    def initialize_default_listeners(self):
        ic('-------------- INIT LISTENERS --------------')
        if len(self.listeners) > 0:
            self.remove_all_listeners()

        #self.telemetry_listener()
        self.add_listener('AIRCRAFT_LOCATION', lambda data:self.KEYS.update([('AIRCRAFT_LOCATION', data)]))
        self.add_listener('AIRCRAFT_LOCATION', self.telemetry_log_writer)
        self.add_listener('VELOCITY_X', lambda data:self.KEYS.update([('VELOCITY_X', data[0])]))
        self.add_listener('VELOCITY_Y', lambda data:self.KEYS.update([('VELOCITY_Y', data[0])]))
        self.add_listener('VELOCITY_Z', lambda data:self.KEYS.update([('VELOCITY_Z', data[0])]))

        self.add_listener('IS_FLYING', lambda data:self.KEYS.update([('IS_FLYING', data[0])]))

        self.add_listener('ATTITUDE_PITCH', lambda data:self.KEYS.update([('ATTITUDE_PITCH', data[0])]))
        self.add_listener('ATTITUDE_YAW', lambda data:self.KEYS.update([('ATTITUDE_YAW', data[0])]))
        self.add_listener('ATTITUDE_ROLL', lambda data:self.KEYS.update([('ATTITUDE_ROLL', data[0])]))
        self.add_listener('FLY_TIME_IN_SECONDS', lambda data:self.KEYS.update([('FLY_TIME_IN_SECONDS', data[0])]))


        self.add_listener('START_TAKEOFF', lambda _:self.drone_status.update([('FLYING', True)]))
        self.add_listener('START_LANDING', lambda _:self.drone_status.update([('FLYING', False)]))
        self.add_listener('START_LANDING', lambda _:setattr(self, 'telemetry_logger_header', True))

        def _list_key_updater(key, data):
            l = self.KEYS.get(key, [])
            l.append(data)
            self.KEYS.update([(key, l)])

        self.add_listener('WAYPOINT_MISSION_STATUS', lambda data:_list_key_updater('WAYPOINT_MISSION_STATUS', data))
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
        self.server = server.Listener(self)
    

    def get_value(self, key):
        pass

    def remove_all_listeners(self):
        for code_name, func in self.listeners:
            self.remove_listener(code_name, func)

    def add_listener(self, code_name, callback):
        code, _ = pkt_builder.BUILD_CODES.get(code_name, None)
        if code is None: return
        pkt_parser.add_handler(code, callback)
        self.listeners.append((code_name, callback))
    
    def remove_listener(self, code_name, callback):
        code, _ = pkt_builder.BUILD_CODES.get(code_name, None)
        if code is None: return
        try:
            pkt_parser.HANDLERS[code].remove(callback)
        except ValueError: pass



