import cv2

def encode_image(frame):
    if frame is None: return
    ret, encoded = cv2.imencode('.jpg', frame)
    return encoded.tobytes()








