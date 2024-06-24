import threading
import cv2
import time
from copy import deepcopy

from icecream import ic

class Capture:
    def __init__(self, url):
        self.url = url
        self.cap = None
        self.running = False
        self.last_capture_time = None
        self.frame_time = 0
        self.frame = None
        self.frame_rate = 30
        self.freezed_frame = None
    
    def start(self):
        if self.running == True:
            return ic('\nalready running, call stop first')
        self.running = True # START
        self.cap = cv2.VideoCapture(self.url)
        self.last_capture_time = time.time()
        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        return ic('\nSTART CAPTURE')
    
    def retrieve(self):
        return deepcopy(self.frame)
    
    def capture(self):
        if self.cap is None or not self.cap.isOpened(): return None
        now = time.time()
        self.frame_time = int(1./max(now - self.last_capture_time, 0.0001))
        self.last_capture_time = now
        _, frame = self.cap.read()
        diff = 1/self.frame_rate - (time.time()-self.last_capture_time)
        diff = max(0, diff)
        diff = min(1/self.frame_rate, diff)
        if diff > 0:
            time.sleep(diff)
        return frame

    def run(self):
        while self.running:
            self.frame = self.capture()
            if self.frame is None:
                self.stop()
        
        self.cap = None
        self.frame = self.freezed_frame
    
    def stop(self):
        self.running = False
        self.freezed_frame = deepcopy(self.frame)
        return ic('\nSTOP CAPTURE')


