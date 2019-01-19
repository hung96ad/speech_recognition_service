import speech_recognition as sr
import subprocess
import uuid
import os

def speech_recognition(audio):
    results = ""
    audio_path, file_name = split_audio()
    list_audio = os.listdir(audio_path)
    list_audio.sort()
    for id_path in list_audio:
        result = speech_recognition_by_path(audio_path + id_path)
        if len(result) > 0:
            results += " " + result
        print(id_path)
    command = 'rm -rf %s'%file_name
    subprocess.call(command, shell=True)
    return results

def split_audio(audio):
    file_name = str(uuid.uuid1())
    command = 'mkdir %s %s/audio_split'%(file_name, file_name)
    subprocess.call(command, shell=True)
    with open('%s/audio.wav'%file_name, 'wb') as f: 
        f.write(audio) 
    command = "ffmpeg -i %s/audio.wav -acodec pcm_s16le -ac 1 -ar 16000 %s/out.wav"%(file_name,file_name)
    subprocess.call(command, shell=True)
    command = "ffmpeg -i %s/out.wav -f segment -segment_time 120 -c copy %s/audio_split/%s003d.wav"%(file_name,file_name,'%')
    subprocess.call(command, shell=True)
    audio_path = '%s/audio_split/'%file_name
    return audio_path, file_name

def speech_recognition_by_path(path):
    r = sr.Recognizer()
    audio_base = sr.AudioFile(path)
    with audio_base as source:
        audio = r.record(source, duration=120)
    try:
        return r.recognize_google(audio)
    except:
        return ""