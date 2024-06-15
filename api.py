from flask import Flask, render_template, Response, jsonify, request

from flask_cors import CORS, cross_origin

# from video_feed import video_feed
# from telemetry.client import Client
# from recorder import Recorder
# from _mock import DroneData

# log_client = Client()

import config #

# recorder = Recorder(video_feed,log_client)
# from telemetry.demo_day_read_log import log_reader

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

main_instance = None

def set_main_instance(o):
    globals()['main_instance'] = o


# drone_data = DroneData()


@app.route('/')
def index():
    return str(main_instance)

@app.route('/status')
def status():
    return main_instance.server_status

@app.route('/missions/')
def missions():
    amount = 10
    page = 0
    try:
        amount = int(request.args.get('amount', 10))
        page = int(request.args.get('page', 0))
    except: pass
    return main_instance.get_missions(amount, page)

@app.route('/telemetry/')
def telemetry():
    return main_instance.telemetry_data

# def gen(feed):
#     while True:
#         frame = feed.retrieve()
#         recorder.track()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
# @cross_origin()        
# @app.route('/video_feed')
# def video_feeder():
#     return Response(gen(video_feed),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @cross_origin()
# @app.route("/drone_data")
# def get_drone_data():
#     #drone_data.update_data()
#     #data = drone_data.get_data()
#     #################################
#     # DEMONSTRACAO//
#     # EXECUTA API COM UM ARQUIVO DE VIDEO E LOG DE VOO SIMULANDO A
#     # COMUNICAÇÃO COM O DRONE.
    
#     # log_reader.read(video_feed.capture.frame_index, video_feed.capture.frame_rate)
#     # data = log_reader.get_data()
#     data = {}
#     ######################################
#     return jsonify(data)

# @cross_origin()
# @app.route("/face_detection")
# def activate_face_detection():
#     return jsonify({"result": True})

# @cross_origin()
# @app.route("/pid")
# def activate_pid():
#     return jsonify({"result": True})

# @cross_origin()
# @app.route("/get-next-pid")
# def get_next_pid():
#     return jsonify({"result": True})

# @cross_origin()
# @app.route("/pid-frame/<int:frame_id>")
# def get_pid_frame(frame_id):
#     return jsonify({"result": frame_id})


# @cross_origin()
# @app.route("/start_record")
# def start_record():
#     if recorder.is_recording:
#         return jsonify({"result": "already recording"})
    
#     recorder.start_recording()
#     return jsonify({"result": "started recording"})

# @cross_origin()
# @app.route("/stop_record")
# def stop_record():
#     if not recorder.is_recording:
#         return jsonify({"result": "not recording"})
#     recorder.stop_recording()
#     return jsonify({"result": "stoped recording"})





def start():
    if main_instance is not None:
        app.run(host=config.API_HOST, port=config.API_PORT, threaded=True, use_reloader=False)
    else:
        print('manager instance not set')