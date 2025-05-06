import cv2  # type: ignore
import face_recognition  # type: ignore
import numpy as np  # type: ignore
import json

      # Charger les encodages depuis le fichier JSON
with open("encodings.json", "r") as json_file:
    data = json.load(json_file)

known_encodings = []
known_names = []
for name, encoding in data.items():
    known_encodings.append(np.array(encoding))
    known_names.append(name)

# Initialiser la caméra (0 = caméra par défaut)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur: Impossible d'accéder à la webcam")
    exit()

while True:
    # Lire une frame
    ret, frame = cap.read()
    if not ret:
        print("Erreur: Lecture de frame échouée")
        break

    # Redimensionner et appliquer un effet miroir
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)
for (top, right, bottom, left), encod in zip(faces, face_encodings):
            distances = face_recognition.face_distance(known_encodings, encod)
            min_distance = np.min(distances) 
           if len(distances) > 0 else None

            if min_distance is not None and min_distance < 0.5:
                index = np.argmin(distances)
                name = known_names[index]
            else:
                name = "Inconnu"

            # Dessiner un rectangle autour du visage
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, bottom + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
          else:
        print("Aucun visage détecté.")


    # Convertir BGR vers RGB
    rgb_frame = frame[:, :, ::-1]

    # Détecter les visages
    faces = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, faces)
    if len(face_encodings) == 0:
        print("Échec de l'encodage du visage.")
    
    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
