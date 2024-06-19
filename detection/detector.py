import cv2
import torch
import os

from detection.model import inference
from detection import utils

import config


class Detector:
    def __init__(self, ckpt, class_names, frame_retriever):
        self.ckpt = ckpt
        self.class_names = class_names
        self.frame_retriever = frame_retriever
        self.inference_model = inference.Inference(ckpt, class_names, conf=config.DETECTION_CONF, iou=config.DETECTION_IOU)
        
    def start(self):
        self.inference_model.load()
    
    def stop(self):
        self.inference_model.unload()
    
    def run(self):
        frame = self.frame_retriever()
        if frame is None: return frame
        #frame = utils.change_brightness(frame, -100)
        if not self.inference_model.initialized: return frame
        h, w = frame.shape[:2]
        image = cv2.resize(frame, config.DETECTION_IMAGE_SIZE)
        image_input = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_input = torch.tensor(image_input, dtype=torch.float32)/255.
        image_input = image_input.unsqueeze(0)
        image_input = image_input.permute(0, 3, 1, 2)
        detections = self.inference_model.from_frame(image_input, (h, w))
        boxes = detections['boxes']
        labels = detections['labels']
        boxes = utils.rescale_boxes(boxes, w, h, config.DETECTION_IMAGE_SIZE[0])
        final_image = utils.draw_detections_with_labels(frame, boxes, labels, self.class_names)
        return cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)

def main():
    from PIL import Image
    import numpy as np
    from detection.class_names import face_class_names, pid_class_names

    def _get_img():
        s = Image.open('test2.png').convert('RGB')
        s = np.asarray(s)
        s = cv2.cvtColor(s, cv2.COLOR_BGR2RGB)
        return s
    
    det = Detector('detection/checkpoints/face_model.pt', face_class_names, _get_img)
    #det = Detector('detection/checkpoints/pid_model.pt', pid_class_names, _get_img)
    det.start()
    img = det.run()
    f = Image.fromarray(img)
    f.save('result2.png')
    print('done')