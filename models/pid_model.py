import cv2
import numpy as np


from .pid_inference_model.inference import inference

from . import utils

class_names = ['bicicleta', 'onibus', 'carro', 'moto', 'pessoa', 'caminhao']

#INPUT_SIZE = 640
INPUT_SIZE = 960

def change_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

class PIDModel:
    def __init__(self, capture):
        self.capture = capture
    
    def start(self):
        inference.load()
    
    def stop(self):
        inference.unload()
    
    def run(self):
        frame = self.capture.retrieve_frame()
        frame = change_brightness(frame, -100)
        if not inference.initialized: return frame
        h,w = frame.shape[:2]
        image = cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE))
        image_input = cv2.cvtColor(np.copy(image), cv2.COLOR_BGR2RGB)
        detections = inference.from_image_array(image_input, (h, w))
        boxes = detections['boxes']
        labels = detections['labels']
        boxes = utils.rescale_boxes(boxes, w, h, INPUT_SIZE)
        final_image = utils.draw_detections_with_labels(frame, boxes, labels, class_names)
        return final_image

