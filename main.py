import cv2
import numpy as np
import cv2

# Ouvrir la webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la webcam.")
    exit()

while True:
    # Acquisition de l'image
    ret, frame = cap.read()
    
     # Vérifier si l'acquisition de l'image a réussi
    if not ret:
        print("Erreur: Impossible de capturer l'image.")
        break
    
    # Afficher l'image acquise
    cv2.imshow("Image", frame)
    
    # Quitter la boucle si l'utilisateur appuie sur la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fermer la fenêtre d'affichage
cv2.destroyAllWindows()
# Libérer la ressource de la webcam
cap.release()


