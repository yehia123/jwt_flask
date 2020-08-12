import cv2
import mtcnn
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import face_recognition

imagePath = "./img/jessica-wilson-nx3N6enkY_k-unsplash.jpg"
cascPath = "./haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

cap = cv2.VideoCapture(0)

face_locations = []


while True:
    ret, frame = cap.read()

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rgb_frame = frame[:, :, ::-1]

    #find all locations
    facelocations = face_recognition.face_locations(rgb_frame)

    for top, right, bottom, left in facelocations:
        cv2.rectangle(frame, (left, top), (right,bottom), (0,0,255), 2)

    cv2.imshow('video', frame)

    k = cv2.waitKey(30) & 0xff
    if k==27:
        break


cap.release()
cv2.destroyAllWindows()
