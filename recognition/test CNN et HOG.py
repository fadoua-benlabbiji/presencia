import cv2
import face_recognition
import time

# Capture une image depuis la webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

# Redimensionner pour accélérer les tests
frame = cv2.resize(frame, (640, 480))
rgb_frame = frame[:, :, ::-1]

# 🕒 Test avec HOG
start_time = time.time()
face_locations_hog = face_recognition.face_locations(rgb_frame, model="hog")
end_time = time.time()
hog_time = end_time - start_time
print(f"Temps de traitement avec HOG: {hog_time:.4f} secondes")

# 🕒 Test avec CNN
start_time = time.time()
face_locations_cnn = face_recognition.face_locations(rgb_frame, model="cnn")
end_time = time.time()
cnn_time = end_time - start_time
print(f"Temps de traitement avec CNN: {cnn_time:.4f} secondes")
