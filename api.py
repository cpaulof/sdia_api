from flask import Flask, render_template, Response, jsonify

from flask_cors import CORS, cross_origin

from video_feed import VideoCamera
from _mock import DroneData



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


drone_data = DroneData()

@app.route('/')
def index():
    return render_template('index.js')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@cross_origin()
@app.route("/drone_data")
def get_drone_data():
    drone_data.update_data()
    data = drone_data.get_data()
    return jsonify(data)

@cross_origin()
@app.route("/face_detection")
def activate_face_detection():
    return jsonify({"result": True})

@cross_origin()
@app.route("/pid")
def activate_pid():
    return jsonify({"result": True})

@cross_origin()
@app.route("/get-next-pid")
def get_next_pid():
    return jsonify({"result": True})

@cross_origin()
@app.route("/pid-frame/<int:frame_id>")
def get_pid_frame(frame_id):
    return jsonify({"result": frame_id})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)