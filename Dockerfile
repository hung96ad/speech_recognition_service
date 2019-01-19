FROM debian:latest

RUN apt-get -y update && apt-get install -y python3-pip python3-dev python3-tk procps curl cmake ffmpeg

RUN pip3 install Flask SpeechRecognition

ADD . /speech_recognition_service

WORKDIR speech_recognition_service

ENV PYTHONPATH=$PYTHONPATH:src
ENV SPEECH_RECOGNITION_PORT=8090
EXPOSE $SPEECH_RECOGNITION_PORT

ENTRYPOINT ["python3"]
CMD ["speech_recognition_service.py"]
