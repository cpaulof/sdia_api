'''
Mock para simulação básica do client para testes.
'''

import random
import socket
import threading
import struct
import time
from server.pkt_builder import BUILD_CODES

from icecream import ic
MAX_POSSIBLE_LENGTH = 0xFFF

class _Client:
    def __init__(self, host, port):
        self.skt = socket.create_connection((host, port))
        self.skt.settimeout(5.0)
        #self.skt.send(b'\x00\x00\x00\x05\x01ABCD')
        self.start_time = time.time()
        self.running = True
        threading.Thread(target=self.run).start()

    
    def send(self, data):
        self.skt.sendall(data)
    
    def recv(self):
        length = self.skt.recv(4)
        assert len(length) == 4
        length,  = struct.unpack('>I', length)
        assert length < MAX_POSSIBLE_LENGTH
        data = self.skt.recv(length)
        return data
    
    def takeoff(self):
        code_name = 'START_TAKEOFF'
        code, _ = BUILD_CODES[code_name]
        data = struct.pack('>B', code)
        pkt = struct.pack('>I', len(data)) + data
        self.send(pkt)
    
    def land(self):
        code_name = 'START_LANDING'
        code, _ = BUILD_CODES[code_name]
        data = struct.pack('>B', code)
        pkt = struct.pack('>I', len(data)) + data
        self.send(pkt)

    def run(self):
        while self.running:
            pkt = self.create_random_telemetry_data()
            self.send(pkt)
            ic(time.sleep(1.25))
    
    def create_random_telemetry_data(self):
        lat = random.uniform(-90, 90)
        lng = random.uniform(-180, 180)
        alt = random.uniform(10, 30)
        yaw = random.uniform(-25, 25)
        roll = random.uniform(-.5, .5)
        pitch = random.uniform(-15, 0.5)
        vel_x = random.uniform(5.5, 15.)
        vel_y = random.uniform(5.5, 15.)
        vel_z = random.uniform(5.5, 15.)
        time_ = int(time.time() - self.start_time)

        code_name = 'FLIGHT_RECORD'
        code, _ = BUILD_CODES[code_name]

        data = struct.pack('>B9fI', code, lat, lng, alt, yaw, roll, pitch, vel_x, vel_y, vel_z, time_)
        pkt = struct.pack('>I', len(data)) + data
        return pkt

