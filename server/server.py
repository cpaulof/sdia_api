import socket
import time
import threading
import collections
import struct
import random

from icecream import ic

import config

from server import pkt_parser, pkt_builder
from logger.server_logger import ServerLogger
import server_events

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
        ic(recv_data)
        if not recv_data: return b''
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
        self.heart_beat = HeartBeat(self)
        self.heart_beat_thread = threading.Thread(target=self.heart_beat.run)
        self.logger:ServerLogger = server_events.get_logger('server')
        self.logger_first = True

    def send_cmd(self, code_name, *args):
        self.send_queue.append((code_name, args))
    
    def close(self):
        self.running = False
        try: self.skt.close()
        except: pass
    
    def run(self):
        self.recv_thread.start()
        self.heart_beat_thread.start()
        while self.running:
            if len(self.send_queue) == 0:
                time.sleep(0.25)
                continue
            elif len(self.send_queue) >= self.send_queue.maxlen*0.7:
                print('Warning: send queue reaching 70% max length')
            
            code_name, args = self.send_queue.pop()
            code, pkt = pkt_builder.build_packet(code_name, *args)
            self.send_pkt(code, pkt)
            if self.logger:
                self.logger.write(code_name, 'SERVER', len(pkt), 'N/A', new_file=self.logger_first)
                self.logger_first = False
    
    def send_pkt(self, code, pkt):
        payload = struct.pack('B', code) + pkt
        payload_length = len(payload)
        data = struct.pack(f">I", payload_length) + payload
        self.skt.sendall(data)

    def recv_loop(self):
        while self.running:           
            pkt = self.read()
            ic(pkt)
            if pkt is None: break
            try:
                code, length = pkt_parser.parse_packet(pkt)
                if self.logger:
                    self.logger.write(code, 'CLIENT', length, '-', new_file=self.logger_first)
            except Exception as err:
                msg = "Error RECV_LOOP: "+repr(err)
                if self.logger:
                    self.logger.write(-1, 'CLIENT', 0, msg, new_file=self.logger_first)
                ic(msg)
            self.logger_first = False

    
    def read(self):
        try:
            data_length = _recv_until(self.skt, 4)
            data_length,  = struct.unpack('>I', data_length)
            data = _recv_until(self.skt, data_length)
            return data
        except OSError: # closed by server
            self.close()
        except struct.error: # closed by client
            self.close()


class HeartBeat:
    def __init__(self, client: Client, delay=5):
        self.client = client
        self.delay = delay
        self.heart_beat_duration = 0
        self.current_time = time.time()
    
    def gen_check(self):
        check = struct.pack('>I', random.randint(0, 0xFFFFFFFF))
        return check
    
    def run(self):
        pkt_parser.add_handler(1, self.heart_beat_handler)
        ic("added heart beat in handlers")
        while self.client.running:
            check = self.gen_check()
            self.current_time = time.time()
            self.client.send_cmd('HEART_BEAT', check)
            time.sleep(self.delay)
    
    def heart_beat_handler(self, data):
        self.heart_beat_duration = time.time() - self.current_time
        

class Listener:
    def __init__(self, server_ev, host=config.SERVER_HOST, port=config.SERVER_PORT):
        self.skt = None
        self.host = host
        self.port = port
        self.listening = True
        self.client = None
        self.events = server_ev
        self.start_server()
        
    def start_server(self):
        self.skt = socket.socket()
        self.skt.bind((self.host, self.port))
        self.skt.listen(1)
        self.listening = True
        self.listen_thread = threading.Thread(target=self.listen_loop)
        self.listen_thread.start()
    
    def close(self):
        self.listening = False
        if self.client:
            self.client.running = False
            self.client_skt.close()
        self.skt.close()

    def remove_old_listeners(self):
        try:
            func = self.client.heart_beat.heart_beat_handler
            code, _ = pkt_builder.BUILD_CODES.get('HEART_BEAT', None)
            if code is None: return
            try:
                pkt_parser.HANDLERS[code].remove(func)
            except ValueError: pass
            self.events.initialize_default_listeners()
        except: pass

    def listen_loop(self):
        while self.listening:
            try:
                client_skt, client_addr = self.skt.accept()
                # remove old listeners
                old_client = self.client
                ic(client_skt)
                self.client_skt = client_skt
                self.client_addr = client_addr
                new_client = Client(client_skt)
                self.client = new_client
                self.remove_old_listeners(old_client)
                self.client.run()
                
            except Exception as err:
                print('Error:', err)
                
    def flush(self):
        for c in self.clients:
            if not c.is_alive():
                self.clients.remove(c)
        
