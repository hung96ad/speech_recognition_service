from flask import Flask, jsonify, make_response, request, abort, redirect
import logging
from json import loads
from base64 import b64decode
import speech_recognition as sr
import subprocess
import uuid
import os

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

def speech_recognition(audio):
    r = sr.Recognizer()
    file_name = str(uuid.uuid1())
    command = 'mkdir %s %s/audio_split'%(file_name, file_name)
    subprocess.call(command, shell=True)
    with open('%s/audio.wav'%file_name, 'wb') as f: 
        f.write(audio) 
    command = "ffmpeg -i %s/audio.wav -f segment -segment_time 60 -c copy %s/audio_split/%03d.wav"%(file_name,file_name)
    subprocess.call(command, shell=True)
    audio_path = '%s/audio_split'%file_name
    results = ""
    for id_path in os.listdir(audio_path):
        result = speech_recognition_by_path(audio_path + '/' + id_path)
        if len(result) > 0:
            results += " " + result
    return results

def speech_recognition_by_path(path):
    audio_base = sr.AudioFile('path')
    with audio_base as source:
        audio = r.record(source, duration=60)
    try:
        return r.recognize_google(audio)
    except Exception as identifier:
        logging.error('An error has occurred whilst processing the file: "{0}"'.format(err))
        return ""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8084)