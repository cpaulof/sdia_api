import cv2
import numpy as np


from .face_inference_model.inference import inference

from . import utils

class FaceModel:
    def __init__(self, capture):
        self.capture = capture
    
    def start(self):
        inference.load()
    
    def stop(self):
        inference.unload()
    
    def run(self):
        frame = self.capture.retrieve_frame()
        if not inference.initialized: return frame
        h,w = frame.shape[:2]
        image = cv2.resize(frame, (640, 640))
        image_input = cv2.cvtColor(np.copy(image), cv2.COLOR_BGR2RGB)
        detections = inference.from_image_array(image_input, (h, w))
        boxes = detections['boxes']
        scores = detections['scores']
        boxes = utils.rescale_boxes(boxes, w, h)
        final_image = utils.draw_detections(frame, boxes, scores)
        return final_image

