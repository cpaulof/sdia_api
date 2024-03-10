from flask import Flask, jsonify, request
from inference import inference


app = Flask(__name__)

@app.route("/")
def hello_world():
    result = inference.load()

    r = '''
<p>Inference Model API</p>

<br/> Model loading tfor tssssse fsirst time: {}

'''.format(result)
    return r

@app.route('/test_model')
def test_model():
    r = inference.from_filepath('./inference_model/test2.jpeg')
    return jsonify(r)

@app.route('/inference',  methods=['POST'])
def infer():
    r = request.get_json()
    print(r['width'])
    print(r['height'])
    print(len(r['data']))
    result = inference.from_json(r)
    return jsonify(result)