import torch 
from .hubconf import Detector

import config

#model_path = './models/face_inference_model/model_ckpt.pt'
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class Inference:
    def __init__(self, ckpt, class_names, conf=0.4, iou=0.2):
        self.initialized = False
        self.detector = None
        self.conf = conf
        self.iou = iou
        self.ckpt = ckpt
        self.class_names = class_names
    
    def load(self):
        if not self.initialized:
            self.detector = Detector(self.ckpt, self.class_names , device, conf_thres=self.conf, iou_thres=self.iou)
            #self.detector.model.half()
            self.initialized = True
            return True
        return False
    
    def unload(self):
        self.initialized = False
        del self.detector
        self.detector = None
    
    def from_frame(self, frame, img_size):
        # 1 - 255 -> -1 - 1
        #frame = torch.tensor(frame/127.5-1.).unsqueeze(0)
        frame = frame.to(device)
        detections = self.detector.forward(frame, img_size)
        return detections

    # def from_filepath(self, path):
    #     img = Image.open(path).convert('RGB')
    #     width, height = img.size
    #     img = img.resize((640, 640))
    #     img_array = torch.tensor(np.asarray(img))
    #     return self.from_image_array(img_array, (width, height))
    
    # def from_image_array(self, array, img_shape):
    #     array = torch.tensor(array)
    #     array = array.permute(2, 0, 1)
    #     array = array.float()/255.
    #     return self._from_normalized_image(array, img_shape)
    
    # def from_json(self, json):
    #     width = int(json['width'])
    #     height = int(json['height'])
    #     data = json['data']
    #     barray = list(bytes.fromhex(data))
    #     print('barray', len(barray))
    #     array = np.array(barray, np.uint8).reshape(height, width, 3)
    #     print('array', array.shape)
    #     img = Image.fromarray(array)
    #     img = img.resize((640, 640))
    #     img.save('asdasdasda.png')
    #     img_array = torch.tensor(np.asarray(img))
    #     return self.from_image_array(img_array, (width, height))
    
    # def _from_normalized_image(self, array, img_shape):
    #     array = array[None]
    #     array = array.to(device)
    #     #print(array.shape)
    #     import time
    #     start = time.time()
    #     #print(img_shape)

    #     detections = self.detector.forward(array, img_shape)
    #     #print('tempo', time.time()-start)

    #     return detections

    # def from_normalized_image(self, array, img_shape):
    #     array = array[None]
    #     array = array.to(device)
    #     import time
    #     start = time.time()
    #     detections = self.detector.forward(array, img_shape)
    #     print('tempo', time.time()-start)

    #     keys = []
    #     values = []

    #     for key, value in detections.items():
    #         value_ = value.cpu().tolist()
    #         keys.append(key)
    #         values.append(value_)

    #     return dict(zip(keys, values))