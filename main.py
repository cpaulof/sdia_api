import copy

from capture.capture import Capture
from capture.recorder import Recorder
import capture.utils as cap_utils

from mission_control.database import Database as MissionDatabase, URI

from detection.detector import Detector
from detection.class_names import pid_class_names, face_class_names

from server_events import ServerEvents

import api

import config

class Main:
    def __init__(self):
        print('init modules')
        self.mission_database = MissionDatabase(URI)
        self.server_events = ServerEvents()
        self.server_events.start_server()
        # self.server_events.initialize_default_listeners()

        self.capture = Capture(config.CAPTURE_URL)
        self.recorder = Recorder()

        self.face_detection = Detector('./detection/checkpoints/face_model.pt', face_class_names, self.capture.retrieve)
        self.pid_detection = Detector('./detection/checkpoints/pid_model.pt', pid_class_names, self.capture.retrieve)
        print('modules loaded')

        #self.start_capture()

        ##
        self.current_detection_model = None
    
    def change_detection_mode(self, mode):
        m = self.current_detection_model
        if m == mode: return # no change, do nothing
        if mode == 'face':
            if m == 'pid': # stop pid first
                self.pid_detection.stop()
            self.face_detection.start()
            self.current_detection_model = 'face'

        elif mode == 'pid':
            if m == 'face': # stop face first
                self.face_detection.stop()
            self.pid_detection.start()
            self.current_detection_model = 'pid'
        else:
            self.face_detection.stop()
            self.pid_detection.stop()
            self.current_detection_model = None
            

    
    def start_capture(self):
        return self.capture.start()
    
    def stop_capture(self):
        return self.capture.stop()
    
    def get_detection(self):
        m = self.current_detection_model
        if m == 'face':
            frame = self.face_detection.run()
        elif m == 'pid':
            frame = self.pid_detection.run()
        else:
            frame = self.capture.retrieve()
        
        r = cap_utils.encode_image(frame)
        return r

    
    def get_frame(self):
        frame = self.capture.retrieve()
        r = cap_utils.encode_image(frame)
        return r

    @property
    def server_status(self):
        server_running = ('' if self.server_events.server.listening else 'not ')+'running'
        client_conn = None
        client_ping = -1
        try:
            client_ping = self.server_events.server.client.heart_beat.heart_beat_duration
        except: pass

        if self.server_events.server.client is not None:
            client_conn = self.server_events.server.client_addr
        return {
            'mission_database': str(self.mission_database.engine),
            'server': {'server': server_running, 'client':client_conn, 'client_ping':client_ping},
            'camera': str(self.capture.running),
            'recording': self.is_recording,
            'current_detection_model': self.current_detection_model,
        }

    @property
    def is_recording(self):
        return self.recorder.recording
    
    @property
    def telemetry_data(self):
        return copy.deepcopy(self.server_events.telemetry_data)
    
    def create_mission(self, params):
        r = self.mission_database.add_waypoint_mission(params)
        return r
    
    def get_missions(self, amount, page):
        missions = self.mission_database.get_mission_list(amount, page)
        return self.mission_database.serialize(missions)
    
    #mission exec
    def load_mission(self, mission_id):
        m = self.mission_database.get_mission_by_id(mission_id)
        if m is None: return
        
    
    

    
     


main = Main()

api.set_main_instance(main)

# # test #
# from client_mock import _Client
# client = _Client(config.SERVER_HOST, config.SERVER_PORT)
# ########

api.start()

