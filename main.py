import cv2
import numpy as np

cam = cv2.VideoCapture(0)

redLow = np.array([166, 186, 58])
redHigh = np.array([180, 231, 192])

while True:
	ret, img = cam.read()
	img = cv2.flip(img, 1)
	blurred = cv2.GaussianBlur(img, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(blurred, redLow, redHigh)
	cv2.imshow('webcam', img)
	# mask = cv2.erode(mask, None, iterations=2)
	# mask = cv2.dilate(mask, None, iterations=2)

	if cv2.waitKey(1) & 0xff == 27:
		break

cam.release()
cv2.destroyAllWindows()