import cv2

face_cascade = cv2.CascadeClassifier('/usr/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml')

cam = cv2.VideoCapture(0)

redHigh = (0xff,0x0,0x0)
redLow = (0xdd,0x52,0x78)

while True:
	ret, img = cam.read()
	img = cv2.flip(img, 1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		eye_gray = gray[y:y+h,x:x+w]
		eye_col = img[y:y+h,x:x+w]
		eyes = eye_cascade.detectMultiScale(eye_gray)
		for (x,y,w,h) in eyes:
			cv2.rectangle(eye_col, (x,y), (x+w,y+h),(0,255,0),2)

	img = imutils.resize(img, width=600)
	blurred = cv2.GaussianBlur(img, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, redLow, redHigh)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	cv2.imshow('webcam', img)
	if cv2.waitKey(1) & 0xff == 27:
		break

cv2.destroyAllWindows()