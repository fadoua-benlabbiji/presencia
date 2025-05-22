import json
import time
import cv2 # type: ignore
import face_recognition # type: ignore
import numpy as np # type: ignore
   # Charger les encodages depuis le fichier JSON
def encoding():
    with open("encodings.json", "r") as json_file:
        data = json.load(json_file)
    known_encodings = []
    known_names = []
    for name, encoding in data.items():
        known_encodings.append(np.array(encoding))
        known_names.append(name)
    return known_encodings , known_names
def systeme_Recognition(video_capture, known_encodings, known_names):
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
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
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
    
    return frame_d
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

