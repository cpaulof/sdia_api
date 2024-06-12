import socket
import time
import threading
import collections
import struct

import config

from server import pkt_parser, pkt_builder, codes

'''
Enviando um comando:
comandos sao enviados com client.send_cmd(code_name, *args),
em que code_name é o nome do codigo do comando ex:
'''
def _recv_until(skt, size, chunk_size=0xFFF):
    data = b''
    k = 0
    while k < size:
        recv_size = min(size-k, chunk_size)
        recv_data = skt.recv(recv_size)
        data+=recv_data
        k += recv_size
    return data

class Client:
    def __init__(self, skt):
        self.skt = skt
        self.running = True
        self.recv_thread = threading.Thread(target=self.recv_loop)
        self.send_queue = collections.deque(maxlen=200)
        self.is_sending = False
    
    def send_cmd(self, code_name, *args):
        self.send_queue.append((code_name, args))
    
    def run(self):
        self.recv_thread.start()
        while self.running:
            if len(self.send_queue) == 0:
                time.sleep(0.25)
                continue
            elif len(self.send_queue) >= self.send_queue.maxlen*0.7:
                print('Warning: send queue reaching 70% max length')
            
            code_name, args = self.send_queue.pop()
            code, pkt = codes.build_packet(code_name, *args)
            self.send_pkt(code, pkt)
    
    def send_pkt(self, code, pkt):
        payload = struct.pack('B', code) + pkt
        payload_length = len(payload)
        data = struct.pack(f">I", payload_length) + payload
        self.skt.sendall(data)

    def recv_loop(self):
        while self.running:           
            pkt = self.read()
            pkt_parser.parse_packet(pkt)
    
    def read(self):
        data_length = _recv_until(self.skt, 4)
        data_length, _ = struct.unpack('>I', data_length)
        data = _recv_until(self.skt, data_length)
        return data


class Listener:
    def __init__(self, host=config.SERVER_HOST, port=config.SERVER_PORT):
        self.skt = None
        self.host = host
        self.port = port
        self.listening = True
        self.start_server()

    def start_server(self):
        self.skt = socket.socket()
        self.skt.bind((self.host, self.port))
        self.skt.listen()
        self.listen_thread = threading.Thread(target=self.listen_loop)
        self.listen_thread.start()
    
    def close(self):
        self.listening = False
        self.client.running = False
        self.client_skt.close()
        self.skt.close()

    
    def listen_loop(self):
        while self.listening:
            try:
                client_skt, client_addr = self.skt.accept()
                self.client_skt = client_skt
                self.client_addr = client_addr
                new_client = Client(client_skt)
                self.client = new_client
                self.client.run()
                
            except Exception as err:
                print('Error:', err)
                
    def flush(self):
        for c in self.clients:
            if not c.is_alive():
                self.clients.remove(c)
        
