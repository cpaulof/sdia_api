import sys
import os

cwd = sys.path[0]
sys.path.append(os.path.join(cwd, 'models/pid_inference_model'))
sys.path.append(os.path.join(cwd, 'models/face_inference_model'))