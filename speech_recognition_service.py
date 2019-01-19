from flask import Flask, jsonify, make_response, request, abort, redirect
import logging
from json import loads
from base64 import b64decode
from processer import speech_recognition

app = Flask(__name__)

@app.route('/')
def index():
    return redirect("http://tradersupport.club", code=302)

@app.route('/speechRecognition', methods=['POST'])
def upload():
    try:
        data = request.data
        data = data.decode('utf8')
        data = loads(data)
        audio_base = b64decode(data['audio'])
        result = speech_recognition(audio_base)
        if len(result) == 0:
            result = "<<Cannot Recognition>>" 
        return make_response(jsonify(result), 200)
    except Exception as err:
        logging.error('An error has occurred whilst processing the file: "{0}"'.format(err))
        abort(400)

@app.errorhandler(400)
def bad_request(erro):
    return make_response(jsonify({'error': 'We cannot process the file sent in the request.'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource no found.'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8090)