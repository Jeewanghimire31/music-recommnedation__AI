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


@app.route("/videoapi", methods=["GET", "POST"])
def videoapi():
    return camera.get_label()

if __name__ == "__main__":
    app.run(debug=True)

