import os
from datetime import datetime
import cv2
import config



''' Recebe um callable e inicia uma gravação
a partir disso'''
class Recorder:
    def __init__(self, rec_dir=config.RECORDER_DIR, mode=config.RECODER_MODE):
        self.rec_dir = os.path.join(config.BASEPATH, rec_dir)
        self.mode = mode
        self.recording = False
        self.retrive_frame = None
        self.writer = None

    def start_record(self, size, fps, func):
        if self.recording: return
        self.retrive_frame = func
        self.recording = True
        filename = str(datetime.now()).replace(':', '.')+'.mp4'
        self.writer = cv2.VideoWriter(os.path.join(self.rec_dir, filename), cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    
    def record(self):
        if self.retrive_frame is None or not self.recording or self.writer is None: return
        frame = self.retrive_frame()
        self.writer(frame)
    
    def stop_record(self):
        if self.writer is not None:
            try:
                self.writer.release()
            except: pass
        self.recording = False
        self.retrive_frame = None
        self.writer = None

