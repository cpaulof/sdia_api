import socket
import time
import threading

from . import config
from . import client_utils


class Client:
    def __init__(self, host=config.HOST, port=config.PORT):
        self.address = (host, port)
        self.socket = None
        self.thread = None
        self.connected = False
        self.stop = False
        self.last_data = None
    
    def start_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop_thread(self):
        self.stop = True

    def connect(self):
        try:
            self.socket = socket.create_connection(self.address)
            self.connected = True
        except ConnectionRefusedError:
            self.connected = False
        return self.connected
    
    def disconnect(self):
        self.connected = False
        try:
            self.socket.close()
        except:
            pass
        self.socket = None
    
    def run(self):
        print("Thread started", self.thread)
        while not self.stop:
            if not self.connected:
                print("Connecting to ", self.address)
                ret = self.connect()
                if not ret:
                    print("Error connecting, retrying in {} seconds".format(config.RETRYING_CONNECTION_WAIT))
                    time.sleep(config.RETRYING_CONNECTION_WAIT)
                    continue
                print("successfuly connected!")
            
            try:
                client_utils.get_data(self.socket)
                self.last_data = client_utils.save_state()
            except Exception as e:
                print("[TELEMETRY] Error! ", e)
                self.disconnect()
                time.sleep(config.RETRYING_CONNECTION_WAIT)

