import json
import os
import time
import cv2 # type: ignore
import face_recognition # type: ignore
import numpy as np # type: ignore
   # Charger les encodages depuis le fichier JSON

def encoding():
    base_path = os.path.dirname(__file__)
    json_path = os.path.abspath(os.path.join(base_path,'Encodages.json'))
    print(f"Chemin JSON utilisé : {json_path}")
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    known_encodings = []
    known_names = []
    for name, encoding in data.items():
        known_encodings.append(np.array(encoding))
        known_names.append(name)
    return known_encodings , known_names
def systeme_Recognition(frame, known_encodings, known_names):
    frame = cv2.flip(frame, 1)
    # Conversion de l'image en RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb_frame=cv2.resize(rgb_frame,(640,480))
    
    # Détection des visages
    face_locations = face_recognition.face_locations(rgb_frame, model='hog')

    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        nom_detecte=[]
        print(f"Nombre de visages détectés : {len(face_encodings)}")

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Inconnu"

            if known_encodings:  # Vérifie si la base contient des encodages
                # Comparaison avec les encodages connus
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
            nom_detecte.append(name)

            # Affichage du rectangle et du nom
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        print("Aucun visage détecté.")

    return frame,nom_detecte
def test_camera():
    known_encodings, known_names = encoding()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return

    previous_time = time.time()  # Temps de la première frame

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire la frame.")
            break

        current_time = time.time()
        delta_time = current_time - previous_time  # Temps entre 2 frames
        previous_time = current_time

        print(f"Temps entre deux frames : {delta_time:.3f} secondes")

        frame, noms_detectes = systeme_Recognition(frame, known_encodings, known_names)

        cv2.imshow("Reconnaissance Faciale", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Fonction pour tester la reconnaissance faciale avec la caméra
