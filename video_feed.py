import cv2
import numpy as np
import threading
import sys
import time

sys.path.append("./models/face_inference_model")
sys.path.append("./models/pid_inference_model")

sys.path.append('./models/face_inference_model/yolov6')
sys.path.append('./models/pid_inference_model/yolov6')

from models.rtmp_client import CaptureClient
from models.face_model import FaceModel
from models.pid_model import PIDModel

class VideoFeeder:
    def __init__(self, url, mode, delay_to_frame_rate=False):
        self.url = url
        self.mode = mode

        self.delay_to_frame_rate = delay_to_frame_rate

        self.capture = CaptureClient(url)
        self.face_model = FaceModel(self.capture)
        self.pid_model = PIDModel(self.capture)

        self.last_frame = None

        if self.mode == 2:
            self.face_model.start()
        elif self.mode == 3:
            self.pid_model.start()
    
    def encode(self, frame):
        if frame is not None:
            ret, encoded = cv2.imencode('.jpg', frame)
            return encoded.tobytes()
        ret, encoded = cv2.imencode('.jpg', np.zeros(10, 10, 3))
        return encoded.tobytes()
    
    def retrieve(self):

        frame_rate = self.capture.frame_rate
        frame_time = 1/frame_rate

        start_time = time.time()

        if self.mode == 1: # just video feed
            self.last_frame = self.capture.retrieve_frame()
            encoded = self.encode(self.last_frame)
        elif self.mode == 2: # face model
            self.last_frame = self.face_model.run()
            encoded = self.encode(self.last_frame )
        else: # pid model
            self.last_frame = self.pid_model.run()
            encoded = self.encode(self.last_frame )
        
        if self.last_frame is not None:
            self.size = self.last_frame.shape[:2][::-1]
        
        spent_time = time.time() - start_time

        if(self.delay_to_frame_rate):
            wait_time = frame_time - spent_time
            print(wait_time, frame_time, spent_time)
            if wait_time > 0:
                time.sleep(wait_time)
        
        return encoded

        

    
    def change_mode(self, new_mode):
        if new_mode == self.mode: return
        self.mode = new_mode

        if new_mode == 1:
            self.pid_model.stop()
            self.face_model.stop()

        if new_mode == 2:
            self.pid_model.stop()
            self.face_model.start()
        
        if new_mode == 3:
            self.face_model.stop()
            self.pid_model.start()
          


video_feed = VideoFeeder(0, 2)

def _thread():
    import time
    time.sleep(10)
    video_feed.change_mode(1)
    time.sleep(3)
    video_feed.change_mode(3)

#threading.Thread(target=(_thread)).start()
