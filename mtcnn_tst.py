import cv2
from mtcnn import MTCNN
import numpy as np

# Initialisation du détecteur MTCNN
detector = MTCNN()

# Ouvrir la webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Erreur : Impossible de lire la vidéo.")
        break

    # Redimensionner pour accélérer le traitement
    frame_resized = cv2.resize(frame, (640, 480))

    # Convertir l'image en RGB
    rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    # Détecter les visages avec MTCNN
    faces = detector.detect_faces(rgb_frame)

    # Dessiner des rectangles autour des visages détectés
    for face in faces:
        x, y, width, height = face['box']
        cv2.rectangle(frame_resized, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Optionnel : afficher les points clés (landmarks) du visage
        for key in face['keypoints']:
            cv2.circle(frame_resized, face['keypoints'][key], 2, (0, 0, 255), 2)

    # Afficher la vidéo avec les visages détectés
    cv2.imshow('MTCNN Face Detection', frame_resized)

    # Quitter quand l'utilisateur appuie sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
video_capture.release()
cv2.destroyAllWindows()
