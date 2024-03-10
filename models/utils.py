import cv2
import numpy as np




def rescale_boxes(boxes, width, height):
    boxes[..., 0] = boxes[..., 0]/640*width
    boxes[..., 1] = boxes[..., 1]/640*height
    boxes[..., 2] = boxes[..., 2]/640*width
    boxes[..., 3] = boxes[..., 3]/640*height
    return boxes


def draw_detections(image, boxes, scores):
    image = np.asarray(image)
    for i, box in enumerate(boxes):
        box = [int(i) for i in box]
        image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2, 0)
        score = round(float(scores[i]), 2)
        image = cv2.putText(image, str(score), (box[0], box[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
    return image






