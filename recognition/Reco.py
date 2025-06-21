import json
import os
import time
import cv2 # type: ignore
import face_recognition # type: ignore
import numpy as np # type: ignore
   # Charger les encodages depuis le fichier JSON
frame_count = 0
def encoding():
    base_path = os.path.dirname(__file__)
    json_path = os.path.abspath(os.path.join(base_path,'encodages.json'))
    print(f"Chemin JSON utilisé : {json_path}")
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    known_encodings = []
    known_names = []
    for name, encoding_list in data.items():
        for encoding in encoding_list:
            known_encodings.append(np.array(encoding))
            known_names.append(name)
    return known_encodings , known_names
def systeme_Recognition(frame, known_encodings, known_names):
    global frame_count, dernier_noms_detectes
    frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) 
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')

    nombre_visages_detectes = len(face_locations)

    if nombre_visages_detectes == 0:
        return frame, [], nombre_visages_detectes
    elif nombre_visages_detectes > 1:
        return frame, [], nombre_visages_detectes

    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    noms_detectes = []

    if frame_count % 3 == 0:
        for face_encoding in face_encodings:
            name = "Inconnu"
            if known_encodings:
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(distances)
                if distances[best_match_index] < 0.5:
                    name = known_names[best_match_index]
            noms_detectes.append(name)
        dernier_noms_detectes = noms_detectes
    else:
        noms_detectes = dernier_noms_detectes

    for (top, right, bottom, left), name in zip(face_locations, noms_detectes):
        top *= 4; right *= 4; bottom *= 4; left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    frame_count += 1
    return frame, noms_detectes, nombre_visages_detectes



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
