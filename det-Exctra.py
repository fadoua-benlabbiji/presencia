import face_recognition
import cv2 # type: ignore
img=cv2.imread("C:\\Users\\ELITEBOOK\\Pictures\\R.jpg")
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
small = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
visage=face_recognition.face_locations(small,model="cnn")
encodage = face_recognition.face_encodings(image, visage)
for (top ,right,bottom,left)in visage:
   cv2.rectangle((img),(left,top),(right,bottom),(0,255,0),2)
#for encodage in zip(visage,encodage):
     #ch=str(encodage)
     #print(ch)
#face_encodings = face_recognition.face_encodings(image, visage)
#for (top, right, bottom, left), encoding in zip(visage, face_encodings):
    # Dessiner un rectangle autour du visage
    #cv2.rectangle(image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)

    # Afficher un résumé de l'encodage (facultatif)
    #print("Encodage facial (résumé):", encoding[:5], "...")
cv2.imshow("Visage détecté",img)
cv2.waitKey(0)
cv2.destroyAllWindows()