import unittest
import socket, struct, time

from server import server

from icecream import ic

MAX_POSSIBLE_LENGTH = 0xFFF

class _Client:
    def __init__(self, host, port):
        self.skt = socket.create_connection((host, port))
        self.skt.settimeout(5.0)
        #self.skt.send(b'\x00\x00\x00\x05\x01ABCD')

    
    def send(self, data):
        self.skt.sendall(data)
    
    def recv(self):
        length = self.skt.recv(4)
        assert len(length) == 4
        length,  = struct.unpack('>I', length)
        assert length < MAX_POSSIBLE_LENGTH
        data = self.skt.recv(length)
        return data
    


class TestServer(unittest.TestCase):
    
    def test_connect(self):
        host, port = '127.0.0.1', 8875
        listener = server.Listener(host, port)
        client = _Client(host, port)
        time.sleep(0.1)
        listener.close()
        self.assertIsNotNone(listener.client)


    def test_reconect_client(self):
        ic.enable()
        host, port = '127.0.0.1', 8875
        listener = server.Listener(host, port)
        client = _Client(host, port)
        ic(client)
        time.sleep(0.1)
        self.assertIsNotNone(listener.client)
        client.skt.close()
        time.sleep(0.1)

        client = _Client(host, port)
        ic(client)
        time.sleep(0.1)
        self.assertIsNotNone(listener.client)
        listener.close()
        ic.disable()


    def test_restart_server(self):
        ic.enable()
        host, port = '127.0.0.1', 8875
        listener = server.Listener(host, port)
        listener.close()
        listener.start_server()
        time.sleep(0.1)
        client = _Client(host, port)
        ic(client)
        time.sleep(0.1)
        self.assertIsNotNone(listener.client)
        ic.disable()
        listener.close()
    
    def test_heart_beat(self):
        ic.enable()
        host, port = '127.0.0.1', 8879
        listener = server.Listener(host, port)
        client = _Client(host, port)
        ic(client)
        
        time.sleep(0.1)
        self.assertIsNotNone(listener.client)

        ic(listener.client.heart_beat.heart_beat_duration)
        ###
        data = client.recv()
        time.sleep(0.25)
        ic(data)
        client.send(b'\x00\x00\x00\x05'+data)
        time.sleep(0.2)
        ic(listener.client.heart_beat.heart_beat_duration)
        ###
        ic.disable()
        listener.close()
