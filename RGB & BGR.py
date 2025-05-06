import cv2

img = cv2.imread("Personnes\Selena Gomez.jpg")
img = cv2.resize(img, (640, 480)) 
cv2.imshow("Webcam",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

