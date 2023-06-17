import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from flask import Flask
import numpy as np

root_path = os.path.dirname(os.path.abspath(__file__))
face_classifier = cv2.CascadeClassifier(f'{root_path}/static/haarcascade.xml')
classifier = load_model(f'{root_path}/model.h5')
emotion_labels = ['Happy', 'Neutral', 'Sad']


class Video(object):
    def __init__(self):
        self.emotionParameters = {}
        if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
            self.camera = cv2.VideoCapture(0)
            if not (self.camera.isOpened()):
                print("Could not open video device")
            # Set the resolution
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def __del__(self):
        self.camera.release()

    def get_frame(self, reset_predictions):
        try:
            success, frame = self.camera.read()
            if success:
                # Ger faces from frame
                faces = face_classifier.detectMultiScale(frame, 1.3, 5)
                #convert to gray scale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                for x, y, w, h in faces:
                    # find the largest face in the image

                    areas = [w*h for x, y, w, h in faces] # get areas of all faces
                    max_index = np.argmax(areas) # index of largest face
                    x, y, w, h = faces[max_index]  
                    x1, y1 = x+w, y+h
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 1)

                    cv2.line(frame, (x, y), (x+30, y), (255, 0, 255), 6)
                    cv2.line(frame, (x, y), (x, y+30), (255, 0, 255), 6)

                    cv2.line(frame, (x1, y), (x1-30, y), (255, 0, 255), 6)
                    cv2.line(frame, (x1, y), (x1, y+30), (255, 0, 255), 6)

                    cv2.line(frame, (x, y1), (x+30, y1), (255, 0, 255), 6)
                    cv2.line(frame, (x, y1), (x, y1-30), (255, 0, 255), 6)

                    cv2.line(frame, (x1, y1), (x1-30, y1), (255, 0, 255), 6)
                    cv2.line(frame, (x1, y1), (x1, y1-30), (255, 0, 255), 6)

                    roi_gray = gray[y:y + h, x:x + w]
                    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA) # resize to 48x48
                    if np.sum([roi_gray]) != 0: # check if the face is detected
                        roi = roi_gray.astype('float') / 255.0 # normalize
                        roi = img_to_array(roi) # convert to array
                        roi = np.expand_dims(roi, axis=0) # reshape to 1, 48, 48, 1
                        prediction = classifier.predict(roi)[0] # predict the emotion on the face
                        label = emotion_labels[prediction.argmax()] # get the label with max accuracy
                    else:
                        label = "None"

                    if label in self.emotionParameters:
                        self.emotionParameters[label] += 1
                    elif reset_predictions:
                        self.emotionParameters.clear()
                    else:
                        self.emotionParameters[label] = 1

                    ret, jpg = cv2.imencode('.jpg', frame) # encode the frame in JPEG format
                    return jpg.tobytes() # return the encoded frame
        except Exception as exp:
            print(exp)

    def get_label(self):
        return self.emotionParameters

    def reset_label(self):
        return self.emotionParameters.clear()
