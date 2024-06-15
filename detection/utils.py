import cv2
import numpy as np


def rescale_boxes(boxes, width, height, input_size):
    boxes[..., 0] = boxes[..., 0]/input_size*width
    boxes[..., 1] = boxes[..., 1]/input_size*height
    boxes[..., 2] = boxes[..., 2]/input_size*width
    boxes[..., 3] = boxes[..., 3]/input_size*height
    return boxes


def draw_detections(image, boxes, scores):
    image = np.asarray(image)
    for i, box in enumerate(boxes):
        box = [int(i) for i in box]
        image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2, 0)
        score = round(float(scores[i]), 2)
        image = cv2.putText(image, str(score), (box[0], box[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
    return image

def draw_detections_with_labels(image, boxes, labels, class_names):
    image = np.asarray(image)
    
    for i, box in enumerate(boxes):
        text = str(class_names[labels[i]])
        size, p = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1, 1)
        #print(size, (box[0], box[1]))
        box = [int(i) for i in box]
        image = cv2.rectangle(image, (box[0], box[1]-size[1]-1), (box[0]+size[0], box[1]), (0, 255, 0), -1, 0)
        image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 1, 0)
        image = cv2.putText(image, text, (box[0], box[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 1, cv2.LINE_AA)
    return image

def change_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img



