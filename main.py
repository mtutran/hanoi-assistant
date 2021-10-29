import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.12, minNeighbors=12, minSize=(100, 100))
        for x, y, w, h in faces:
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(3)
        if (key & 0xFF) == ord('q'):
            break
    cv2.destroyAllWindows()
