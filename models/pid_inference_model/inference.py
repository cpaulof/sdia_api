import torch 
from .hubconf import Detector
from PIL import Image
import numpy as np

class_names = ['bicycle', 'bus', 'car', 'motorcycle', 'person', 'truck']
model_path = './models/pid_inference_model/best_ckpt.pt'

IMG_SHAPE = (960, 960)

class Inference:
    def __init__(self, conf=0.6, iou=0.2):
        self.initialized = False
        self.detector = None
        self.conf = conf
        self.iou = iou
    
    def load(self):
        if not self.initialized:
            self.detector = Detector(model_path, class_names, 'cuda', conf_thres=self.conf, iou_thres=self.iou)
            #self.detector.model.half()
            self.initialized = True
            return True
        return False
    
    def unload(self):
        self.initialized = False
        del self.detector
        self.detector = None

    def from_filepath(self, path):
        img = Image.open(path)
        width, height = img.size
        img = img.resize((960, 960))
        img_array = torch.tensor(np.asarray(img))
        return self.from_image_array(img_array, (width, height))
    
    def from_image_array(self, array, img_shape):
        array = torch.tensor(array)
        array = array.permute(2, 0, 1)
        array = array.float()/255.
        return self._from_normalized_image(array, img_shape)
    
    def from_json(self, json):
        width = int(json['width'])
        height = int(json['height'])
        data = json['data']
        barray = list(bytes.fromhex(data))
        print('barray', len(barray))
        array = np.array(barray, np.uint8).reshape(height, width, 3)
        print('array', array.shape)
        img = Image.fromarray(array)
        img = img.resize((640, 640))
        img.save('asdasdasda.png')
        img_array = torch.tensor(np.asarray(img))
        return self.from_image_array(img_array, (width, height))
    
    def _from_normalized_image(self, array, img_shape):
        array = array[None]
        array = array.to('cuda')
        #print(array.shape)
        import time
        start = time.time()
        #print(img_shape)
        #print('Array', array.shape)
        detections = self.detector.forward(array, img_shape)
        #print('tempo', time.time()-start)

        return detections

    def from_normalized_image(self, array, img_shape):
        array = array[None]
        array = array.to('cuda')
        import time
        start = time.time()
        detections = self.detector.forward(array, img_shape)
        print('tempo', time.time()-start)

        keys = []
        values = []

        for key, value in detections.items():
            value_ = value.cpu().tolist()
            keys.append(key)
            values.append(value_)

        return dict(zip(keys, values))
    
inference = Inference()
    
if __name__ == '__main__':
    inference.load()
    print(inference.from_filepath('./test2.jpeg'))