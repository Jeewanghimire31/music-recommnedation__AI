import glob
import os
import random

from flask import Flask, Response, render_template
from flask_cors import CORS

from camera import Video

app = Flask(__name__)
CORS(app)
root_path = os.path.dirname(os.path.abspath(__file__))
folders = ["Happy", "Sad", "Neutral"]
global folder_count

# imported video object from camera.py
camera = Video()

def generate_video():
    while True:
        try:
            # getting the label from camera.py
            frame = camera.get_frame(reset_predictions=False) # \get frame from camera
            print(camera.get_label()) 

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concat frame one by one and show result 
        except Exception as e:
            continue


@app.route("/video", methods=["GET", "POST"])
def video():
    return Response(generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/emotion-parameters", methods=["GET", "POST"])
def getEmotionParameters():
    return camera.get_label()

@app.route("/ping", methods=["GET"])
def ping():
    return "Pong!"

@app.route("/initialize", methods=["GET"])
def initialize():
    camera.emotionParameters={}
    return "Initialized"


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5001)


