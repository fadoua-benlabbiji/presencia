import cv2
import numpy as np
#import face_recognition
import os
path ='Personnes' #définit simplement le chemin
images=[]
classNames=[]
personsList=os.listdir(path)#Liste les fichiers dans un répertoire donné.
print(path)
camera=cv2.VideoCapture(0)
while True :
    ret ,frame =camera.read()
    if not ret : 
        break
    frame=cv2.flip(frame,1)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Webcam",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()

