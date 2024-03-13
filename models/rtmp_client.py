import cv2
import time
import threading


class CaptureClient:
    def __init__(self, url='rtmp://127.0.0.1:1935/live/test', wait_for_frame_time=True):
        self.url = url
        self.thread_running = False

        self.current_frame = None # keep only the last frame instead of queuing them.
        self.last_frame = None
        self.wait_for_frame_time = wait_for_frame_time

        self.start_thread = threading.Thread(target=self.start)
        self.start_thread.start()
    
    def start(self):
        self.thread_running = True
        self.cap = cv2.VideoCapture(self.url)
        self.frame_index = 0
        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        print(self.frame_rate)
        frame_time = 1/self.frame_rate
        initial_time = time.time()
        while self.thread_running:
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    #frame = cv2.resize(frame, (1280, 720))
                    self.current_frame = frame
                    current_time = time.time() 
                    wait_time = frame_time - (current_time-initial_time)
                    
                    if wait_time> 0 and self.wait_for_frame_time:
                        time.sleep(wait_time*2)
                    initial_time = current_time
                    self.frame_index+=1
                    
            else:
                self.thread_running = False
                self.cap = None
                return
    
    def stop(self):
        self.thread_running = False
        if self.cap is not None:
            self.cap.release()
    
    def get_frame_index(self):
        return self.frame_index
    
    def retrieve_frame(self):
        return self.current_frame

