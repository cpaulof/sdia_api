import cv2
import numpy as np
from PIL import Image
import sys
import time
import collections
import threading


from face_inference_model.inference import inference

inference.load()

cap = cv2.VideoCapture()
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
cap.open('rtmp://127.0.0.1:1935/live/test')

def draw_detection(image, boxes, scores):
    image = np.asarray(image)
    for i, box in enumerate(boxes):
        box = [int(i) for i in box]
        image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2, 0)
        score = round(float(scores[i]), 2)
        image = cv2.putText(image, str(score), (box[0], box[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
    return image


class Detection:
    def __init__(self):
        self.queue = collections.deque(maxlen=100)
        self.running = True
        self.out_queue = collections.deque(maxlen=100)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def append(self, obj):
        self.queue.append(obj)
    
    def pop(self):
        return self.queue.pop()
    
    def run(self):
        while self.running:
            if len(self.queue) == 0:
                time.sleep(0.250)
                continue
            frame = self.pop()
            image = Image.fromarray(frame).resize((640,640))
            image = np.asarray(image, np.float32)
            detections = inference.from_image_array(image, (640, 640))
            #print(detections['boxes'])
            boxes = detections['boxes']
            h,w = frame.shape[:2]
            #boxes[..., 1] = boxes[..., 1]/
            print(boxes)

            final_image = draw_detection(image, boxes)
            self.out_queue.append(final_image)
            #cv2.imshow('Image', final_image/255.)

#detector = Detection()

c = 0

class StreamReader:
    def __init__(self):
        self.running = True
        self.frame = None
        threading.Thread(target=self.run).start()
    
    def run(self):
        while self.running:
            ret, frame = cap.read()
            self.frame = frame
        




stream_reader = StreamReader()

while True:
    t = stream_reader.frame
    if t is not None:
        h,w = t.shape[:2]
        
        
        #image = Image.fromarray(cv2.cvtColor(t, cv2.COLOR_BGR2RGB)).resize((640,640))
        image = cv2.resize(t, (640, 640))
        image_input = cv2.cvtColor(np.copy(image), cv2.COLOR_BGR2RGB)
        #image = np.asarray(image, np.float32)
        detections = inference.from_image_array(image_input, (h, w))
        boxes = detections['boxes']
        scores = detections['scores']
        boxes[..., 0] = boxes[..., 0]/640*w
        boxes[..., 1] = boxes[..., 1]/640*h
        boxes[..., 2] = boxes[..., 2]/640*w
        boxes[..., 3] = boxes[..., 3]/640*h
        final_image = draw_detection(t, boxes, scores)
        cv2.imshow("img", final_image/255)

        cv2.waitKey(1)