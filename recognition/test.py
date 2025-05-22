import cv2
import numpy as np
# 1. Création d'une image 5x5 pixels avec 3 canaux (BGR)
# Format : (hauteur, largeur, canaux) - Ici 5x5x3
image_data = np.array([
    # Ligne 1 (5 pixels)
    [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255], [0, 0, 0]],  # BGR
    # Ligne 2
    [[128, 0, 0], [0, 128, 0], [0, 0, 128], [128, 128, 128], [64, 64, 64]],
    # Ligne 3
    [[255, 255, 0], [255, 0, 255], [0, 255, 255], [100, 200, 50], [50, 100, 200]],
    # Ligne 4
    [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255]],
    # Ligne 5
    [[100, 100, 100], [150, 150, 150], [200, 200, 200], [250, 250, 250], [255, 255, 255]]
], dtype=np.uint8)  # Important : type uint8 (0-255)

# 2. Affichage de la matrice
print("Matrice NumPy de l'image (5x5x3) :")
print(image_data)

# 3. Agrandissement x100 pour mieux voir les pixels
image_agrandie = cv2.resize(image_data, (500,500), interpolation=cv2.INTER_NEAREST)

cv2.imshow('Image agrandie 100x (5x5 pixels originaux)', image_agrandie)
cv2.waitKey(0)
cv2.destroyAllWindows()