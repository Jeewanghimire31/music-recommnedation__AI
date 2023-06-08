import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import mediapipe as mp

camera = cv2.VideoCapture(0)
detector = FaceMeshDetector()

while True:
    success, img = camera.read()
    img, faces = detector.findFaceMesh(img, draw=False)

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
            cvzone.putTextRect(img, f'Distace: {int(d)}cm' , (face[10][0]-100,face[10][1]-50),scale=2)
                            
        
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    # close the screen when i press q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
