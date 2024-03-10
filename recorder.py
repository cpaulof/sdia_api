import os
import datetime

import cv2

SAVE_DIR = "./recorded"


def _get_new_filename():
    return str(datetime.datetime.now())

class Recorder:
    def __init__(self, video_feed, log_client):
        self.video_feed = video_feed
        self.log_client = log_client

        self.video_writer = None
        self.log_writer = None

        self.is_recording = False
    
    def start_recording(self):
        if self.is_recording: return
        self.is_recording = True
        
        base_filename = _get_new_filename()
        video_filename = base_filename+'.mp4'
        log_filename = base_filename+'.txt'

        frame_rate = self.video_feed.capture.frame_rate
        print(self.video_feed.size)
        self.video_writer = cv2.VideoWriter(os.path.join(SAVE_DIR, video_filename), cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, self.video_feed.size)
        self.log_writer = open(os.path.join(SAVE_DIR, log_filename), 'w')

    
    def track(self):
        if not self.is_recording or None in (self.log_writer, self.video_writer): return
        self.video_writer.write(self.video_feed.last_frame)
        #cv2.imwrite(str(datetime.datetime.now())+'.png', self.video_feed.last_frame)
        data = [datetime.datetime.now()]
        if self.log_client.last_data is not None:
            data.extend(self.log_client.last_data)
        self.log_writer.write(",".join([str(i) for i in data]))
        self.log_writer.write('\n')
    
    def stop_recording(self):
        if not self.is_recording: return
        self.is_recording = False
        self.video_writer.release()
        self.log_writer.close()




