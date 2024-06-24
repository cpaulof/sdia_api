import socket
import struct
from typing import List

import av

import config

def _recv_until(skt, size, chunk_size=0xFFF):
    data = b''
    k = 0
    while k < size:
        recv_size = min(size-k, chunk_size)
        recv_data = skt.recv(recv_size)
        if not recv_data: return b''
        data+=recv_data
        k += recv_size
    return data

class Decoder:
    def __init__(self):
        self.codec = av.Codec('h264', 'w')
        self.context = self.codec.create()
        self.context.width = 1280
        self.context.height = 720
        self.context.pix_fmt = 'yuv420p'
        self.context.rate = 24

        self.context.open()
        self.last_frame = None

    def parse(self, packet):
        packets = self.context.parse(packet)
        for pkt in packets:
            frames:List['av.VideoFrame'] = self.context.decode(pkt)
            for frame in frames:
                self.last_frame = frame.to_rgb().to_ndarray()

class Server:
    def __init__(self, host=config.SERVER_HOST, port=config.SERVER_VIDEO_FEED_PORT):
        self.host = host
        self.port = port
        self.skt = socket.Socket()
        self.skt.bind((host, port))
        self.skt.listen(1)

        self.decoder = None

        self.listening = True
    
    def run(self):
        while self.listening:
            self.client, self.client_addr = self.skt.accept()
            print('[VideoFeedServer] Connected:', self.client_addr)
            self.decoder = Decoder()
            while True: #1 client // recv only
                try:
                    packet_length = _recv_until(self.client, 4)
                    assert len(packet_length) == 4
                    packet_length, = struct.unpack('>I', packet_length)
                    packet = _recv_until(self.client, packet_length)
                    self.decoder.parse(packet)
                    print('Decoder Frame:', self.decoder.last_frame)
                except Exception as err:
                    print('[VideoFeedServer] Erro:', err)
