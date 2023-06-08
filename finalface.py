import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from flask import Flask
import numpy as np

# from facedetection 
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import mediapipe as mp

camera = cv2.VideoCapture(0)


root_path = os.path.dirname(os.path.abspath(__file__))
face_classifier = cv2.CascadeClassifier(f'{root_path}/static/haarcascade.xml')
classifier = load_model(f'{root_path}/static/model.h5')
emotion_labels = ['Happy', 'Neutral', 'Sad']
detector = FaceMeshDetector()

class Video(object):
    def __init__(self):
        self.folder_count = {}
        if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
            self.camera = cv2.VideoCapture(0)
            if not (self.camera.isOpened()):
                print("Could not open video device")
            # Set the resolution
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            # from facedepth measurement

    def __del__(self):
        self.camera.release()

    def get_frame(self, reset_predictions):
        try:
            success, img = camera.read()
            if success:
                img, faces = detector.findFaceMesh(img, draw=False)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                if faces:
                    for i , face in enumerate(faces):
                        face = faces[i]
                        pointLeft = face[145]
                        pointRight = face[374]
                        cv2.line(img,pointLeft,pointRight,(0,255,0),3)
                        cv2.circle(img,pointLeft,5,(0,0,255),cv2.FILLED)
                        cv2.circle(img,pointRight,5,(0,0,255),cv2.FILLED)
                        w,_ = detector.findDistance(pointLeft,pointRight)
                        # Finding the focal length
                        W = 6.3 # width of the eyes in cm
                        # d = 50 # distance between the camera and the eyes in cm
                        # f = (w * d) / W
                        # print(f)
                        # Finding distance
                        f = 700 # focal length
                        d = (W * f) / w
                        # print(d)
                        # cvzone.putTextRect(img, f'Distace: {int(d)}cm' , (face[10][0]-100,face[10][1]-50),scale=2)
                        roi_gray = gray[20:200, 140:380]
                        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA) # resize to 48x48
                        if np.sum([roi_gray]) != 0: # check if the face is detected
                            roi = roi_gray.astype('float') / 255.0 # normalize
                            roi = img_to_array(roi) # convert to array
                            roi = np.expand_dims(roi, axis=0) # reshape to 1, 48, 48, 1
                            prediction = classifier.predict(roi)[0] # predict the emotion on the face
                            label = emotion_labels[prediction.argmax()] # get the label with max accuracy
                        else:
                            label = "None"
            

            
            
        except Exception as exp:
            print(exp)

    def get_label(self):
        return self.folder_count

    def reset_label(self):
        return self.folder_count.clear()

