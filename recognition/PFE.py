import json
import cv2 # type: ignore
import face_recognition # type: ignore
import numpy as np # type: ignore
   # Charger les encodages depuis le fichier JSON
with open("encodings.json", "r") as json_file:
    data = json.load(json_file)

known_encodings = []
known_names = []
for name, encoding in data.items():
    known_encodings.append(np.array(encoding))
    known_names.append(name)
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra.")
    exit()
while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Erreur : Impossible de lire la vidéo.")
            break
        frame=cv2.flip(frame,1)
        frame_d = cv2.resize(frame, (640, 480))
        # Conversion de l'image en RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Détection des visages
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        if face_locations:
           face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
           print(f"Nombre de visages détectés : {len(face_encodings)}")
           for (top, right, bottom, left),face_encoding in zip(face_locations,face_encodings):
                # Comparaison des encodages avec ceux connus
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                name = "Inconnu"
                 # Si un match est trouvé, récupérer le nom correspondant
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]

                # Affichage du nom et du rectangle
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            print("Aucun visage détecté.")
            # Affichage de la vidéo avec la détection
    

        # Afficher la vidéo
        cv2.imshow('Reconnaissance faciale', frame_d)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_capture.release()
cv2.destroyAllWindows()
