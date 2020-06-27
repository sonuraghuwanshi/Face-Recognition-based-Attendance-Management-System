import cv2
import numpy as np
import sqlite3
import time

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer\\trainningData.yml")
id=0
font=cv2.FONT_HERSHEY_SIMPLEX

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

while(True):
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if(profile!=None):
            if id in checkset:
                print(profile[1]+" attendance marked")
            else:
                checkset.add(id)
                #print(checkset)
                print("Attendance Marked")
                conn=sqlite3.connect("FaceBase.db")
                cmd2="UPDATE People SET Attendance= Attendance+1 WHERE ID="+str(id)
                conn.execute(cmd2)
                conn.commit()
                conn.close()
                #time.delay(5)
            cv2.putText(img,str(profile[1]),(x,y+h),font,1,255,2);
            cv2.putText(img,str(profile[2]),(x,y+h+30),font,1,255,2);
            cv2.putText(img,str(profile[3]),(x,y+h+60),font,1,255,2);
            cv2.putText(img,str(profile[4]),(x,y+h+90),font,1,255,2);
            cv2.putText(img,str(profile[5]),(x,y+h+120),font,1,255,2);
    cv2.imshow("Face",img);
    if(cv2.waitKey(1)==ord('q')):
        break;
cam.release()
cv2.destroyAllWindows()
