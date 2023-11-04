import cv2
import numpy as np
import face_recognition
import os
import smtplib
from datetime import datetime

def create_know_faces():
    Person_name = input("Tell me your name:")
    cam = cv2.VideoCapture(0)

    while True:
        _, frame = cam.read()
        cv2.imshow("DoorCamera", frame)
        if cv2.waitKey(1) == ord('w'):
            filename = 'KnownFaces/'+Person_name+'.jpg'
            cv2.imwrite(filename, frame)
            print("saved as:",filename)
            break
    cam.release()
    cv2.destroyAllWindows()

def send_warning():
    server = 'smtp.gmail.com'
    port = 587
    email = 'donttextme88@gmail.com'
    password = 'qlbo xign lgci airh'
    
    email_address = "e0122028@sret.edu.in" 

    subject = 'HOUSE WARNING'
    body = 'There is an INTRUDER IN YOUR HOUSE! AT: '+str(datetime.now().strftime("%H:%M:%S"))

    server = smtplib.SMTP(server, port)
    server.starttls()
    server.login(email, password)

    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(email, email_address, message)

    server.quit()

def findEncImg(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


# to do; upload the recording and then trigger the ending of code properly. 
def face_detection():
    path = 'KnownFaces'
    knownimgs = []
    classes = []

    for Current_Frame in os.listdir(path):
        image = cv2.imread(f'{path}/{Current_Frame}')
        knownimgs.append(image)
        classes.append(os.path.splitext(Current_Frame)[0])

    scale = 0.25
    box_multiplier = 1/scale

    knownEncodes = findEncImg(knownimgs)

    cam = cv2.VideoCapture(0)
    triggerend = False

    while True:
        if cv2.waitKey(1) == ord('w') or triggerend:
            break

        temp , Current_Frame = cam.read()  

        Current_image_Resized = cv2.resize(Current_Frame,(0,0),None,scale,scale)
        Current_image_Resized = cv2.cvtColor(Current_image_Resized, cv2.COLOR_BGR2RGB)

        face_loc = face_recognition.face_locations(Current_image_Resized, model='cnn')  
        face_enc = face_recognition.face_encodings(Current_image_Resized,face_loc)

        for encodefc,faceLoc in zip(face_enc,face_loc):
            matches = face_recognition.compare_faces(knownEncodes,encodefc, tolerance=0.6)
            faceDis = face_recognition.face_distance(knownEncodes,encodefc)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classes[matchIndex].upper()
                print("Unlocked door for:"+name)
                triggerend = True
            else:
                name = 'Unknown'
                password = input("Enter the Password!: ")
                while True:
                    if password == "HEllo":
                        print("Unlocked")
                        triggerend = True
                        break
                    elif password == "BREAK":
                        print("INTRUDER")
                        send_warning()
                        triggerend = True
                        break
                    else:
                        print("Try again")

            # y1,x2,y2,x1 = faceLoc
            # y1, x2, y2, x1 = int(y1*box_multiplier),int(x2*box_multiplier),int(y2*box_multiplier),int(x1*box_multiplier)

            # cv2.rectangle(Current_Frame,(x1,y1),(x2,y2),(0,255,0),2)
            # cv2.rectangle(Current_Frame,(x1,y2-20),(x2,y2),(0,255,0),cv2.FILLED)
            # cv2.putText(Current_Frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)

        # cv2.imshow('DoorCamera',Current_Frame)

    cam.release()
    cv2.destroyAllWindows()

print("Hello User")
i = input("Do you want to enroll yourself for the house security system or trigger the face detection (1/2):")
if i =='1':
    create_know_faces()
elif i == '2':
    face_detection()