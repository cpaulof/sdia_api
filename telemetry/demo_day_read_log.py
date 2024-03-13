import time
import math

feet_meters = 0.3048

class LogReader:
    def __init__(self):
        file = open("12-03/log.txt")
        self.data = file.readlines()
        self.current_index = 332
        #self.readline()

        self.first = True
        self.initial_time = None
    
    def read(self, frame_index, frame_rate):
        if self.first:
            self.initial_time = time.time()
            self.first = False
        
        cur_time = time.time()
        #index = math.ceil((cur_time-self.initial_time)/0.1) -35
        index = math.ceil((frame_index/frame_rate)/0.1) -42
        #print(index, cur_time, self.initial_time)
        if index < 1: self.last_line = None
        else:
            self.last_line = self.read_index(index)
        

    
    def read_index(self, idx):
        line = self.data[idx]
        line = line.replace('\n', '').split('\t')
        
        _,_,_,flght_time,lat, lng, alt, pitch,roll,yaw,bearing, _, _, _, _, _,_ = line
        alt = float(alt)*feet_meters
        line = flght_time,lat, lng, alt, pitch,roll,yaw,bearing
        return line
    
    def get_data(self):
        if self.last_line is None:
            flght_time,lat, lng, alt, pitch,roll,yaw,bearing = 0, -2.4, -44.2, 0.0, 0.0, 0.0, 0.0, 0.0
        else:
            flght_time,lat, lng, alt, pitch,roll,yaw,bearing = self.last_line
        return {
            'lat': float(lat),
            'lng': float(lng),
            'alt': round(alt, 1),
            'vel_x': 0,
            'vel_y': 0,
            'vel_z': 0,
            'pitch': float(pitch),
            'roll': float(roll),
            'yaw': float(yaw)
        }


log_reader = LogReader()
