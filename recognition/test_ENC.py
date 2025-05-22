import dlib 
import face_recognition 
import cv2 
connu=face_recognition.load_image_file("Personnes\\Rachid El ouali\\3.jpg")
encodage=face_recognition.face_encodings(connu)[0]
unconnu=face_recognition.load_image_file("Personnes\\Rachid El ouali\2.jpg")
unencodage=face_recognition.face_encodings(connu)[0]
results = face_recognition.compare_faces([encodage], unencodage)
if results[0]:
    print("Les visages correspondent !")
else:
    print("Les visages ne correspondent pas.")