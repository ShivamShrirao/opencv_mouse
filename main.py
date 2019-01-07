import cv2

face_cascade = cv2.CascadeClassifier('/usr/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml')
licence_cascade = cv2.CascadeClassifier('/usr/lib/python3.7/site-packages/cv2/data/haarcascade_licence_plate_rus_16stages.xml')

cam = cv2.VideoCapture(0)

while True:
	ret, img = cam.read()
	img = cv2.flip(img, 1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	plates = licence_cascade.detectMultiScale(gray, 1.3, 5)
	for zip((x,y,w,h),(a,b,c,d)) in faces,plates:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		cv2.rectangle(img,(a,b),(a+c,b+d),(0,0,255),2)
		eye_gray = gray[y:y+h,x:x+w]
		eye_col = img[y:y+h,x:x+w]
		eyes = eye_cascade.detectMultiScale(eye_gray)
		for (x,y,w,h) in eyes:
			cv2.rectangle(eye_col, (x,y), (x+w,y+h),(0,255,0),2)
	cv2.imshow('webcam', img)
	if cv2.waitKey(1) & 0xff == 27:
		break

cv2.destroyAllWindows()