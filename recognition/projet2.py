from mtcnn.mtcnn import MTCNN
import cv2

# Lire une image
image = cv2.imread('ton_image.jpg')

# Convertir l'image en RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialiser le détecteur MTCNN
detector = MTCNN()

# Détecter les visages
resultats = detector.detect_faces(image_rgb)

# Dessiner les rectangles sur les visages détectés
for face in resultats:
    x, y, largeur, hauteur = face['box']
    cv2.rectangle(image, (x, y), (x + largeur, y + hauteur), (0, 255, 0), 2)

cv2.imshow("Visages détectés", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
