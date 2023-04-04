import face_recognition as fr
from API import DataBase
import cv2
import numpy as np
import os

db = DataBase()
path = "./train/"


known_names = [] #aadhar card number
known_name_encodings = [] #database photos encodings


def train():
    #db.retrieve_images(path=path)

    images = os.listdir(path)
    for _ in images:
        image = fr.load_image_file(path + _)
        image_path = path + _
        encoding = fr.face_encodings(image)[0]

        known_name_encodings.append(encoding)
        known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())
        print("Image done.")

#print(known_names)



# test_image = "./test/test.jpg"
# image = cv2.imread(test_image)
# image = cv2.resize(image, (160, 160))
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# #
# face_locations = fr.face_locations(image)
#face_encodings = fr.face_encodings(image, face_locations)

def test(frame):

    #cap = cv2.VideoCapture(0)
    haar_cascade = cv2.CascadeClassifier(r"D:/Project/Winter Interim Semester 1/Project Exhibition/cass.xml")
    mouth_cascade = cv2.CascadeClassifier(r"D:/Project/Winter Interim Semester 1/Project Exhibition/mouth_cass.xml")
    while True:
        #ret,frame = cap.read()
        face_locations = fr.face_locations(frame)
        face_encodings = fr.face_encodings(frame, face_locations)
        faces_rect = haar_cascade.detectMultiScale(frame,1.1,20)
        #image = cv2.resize(image, (160, 160))
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_name_encodings, face_encoding)
            name = ""
            mouth_rect = mouth_cascade.detectMultiScale(frame,1.1,70)
            face_distances = fr.face_distance(known_name_encodings, face_encoding)
            best_match = np.argmin(face_distances)

            if matches[best_match]:
                name = known_names[best_match]


            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            if(len(mouth_rect)!=0):
                cv2.putText(frame,'NO mask detected',(frame.shape[0]//2,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,cv2.LINE_AA)
                for (mx,my,mw,mh) in mouth_rect:
                    cv2.rectangle(frame,(mx,my),(mx+mw,my+mh),(0,255,0),thickness=3)
        #cv2.imshow("Result", frame)
        return frame
