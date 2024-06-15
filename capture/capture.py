import threading
import cv2
import time

from icecream import ic

class Capture:
    def __init__(self, url):
        self.url = url
        self.cap = None
        self.running = False
        self.last_capture_time = None
        self.frame_rate = 0
        self.frame = None
    
    def start(self):
        self.running = True # START
        ic('\nSTART CAPTURE')
        self.cap = cv2.VideoCapture(self.url)
        self.last_capture_time = time.time()

        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    def retrieve(self):
        return self.frame
    
    def capture(self):
        if self.cap is None and self.cap.isOpened(): return None
        now = time.time()
        self.frame_rate = int(1./max(now - self.last_capture_time, 0.0001))
        self.last_capture_time = now
        frame, _ = self.cap.read()
        return frame

    def run(self):
        while self.running:
            self.frame = self.capture()
            if self.frame is None:
                self.stop()
        
        self.cap = None
    
    def stop(self):
        self.running = False
        ic('\nSTOP CAPTURE')


