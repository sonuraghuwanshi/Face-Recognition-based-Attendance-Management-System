from tkinter import *
import os
import cv2
import numpy as np
from PIL import Image
import sqlite3
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);

def takeatt():
    #ok()
    rec=cv2.face.LBPHFaceRecognizer_create();
    rec.read("recognizer\\trainningData.yml")
    id=0
    font=cv2.FONT_HERSHEY_SIMPLEX
    while(True):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            profile=getProfile(id)
            if(profile!=None):
                cv2.putText(img,str(profile[1]),(x,y+h),font,1,255,2);
                cv2.putText(img,str(profile[2]),(x,y+h+30),font,1,255,2);
                cv2.putText(img,str(profile[3]),(x,y+h+60),font,1,255,2);
                cv2.putText(img,str(profile[4]),(x,y+h+90),font,1,255,2);
        cv2.imshow("Face",img);
        if(cv2.waitKey(1)==ord('q')):
            break;
    cam.release()
    cv2.destroyAllWindows()
    

def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name="+str(Name)+"WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO People(ID,Name) Values("+str(Id)+","+str(Name)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

def getImagesWithID(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print(ID)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return IDs, faces

    

def add_stu():
    fn=StringVar()
    window=Tk()
    window.title("Register Student")
    window.geometry("600x400")
    label2=Label(window,text="Student Registration Successful",fg='blue',font=("arial",16,"bold")).place(x=190,y=60)
    id=input('enter user id')
    name=input('enter your name')
    insertOrUpdate(id,name)
    sampleNum=0;
    while(True):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            sampleNum=sampleNum+1;
            cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.waitKey(100);
        cv2.imshow("Face",img);
        cv2.waitKey(1);
        if(sampleNum>20):
            break;
    cam.release()
    cv2.destroyAllWindows()


def take_att():
    window=Tk()
    window.title("Take Attendance")
    window.geometry("600x400")
    var=StringVar(window)
    label2=Label(window,text="Attendance Successfully Completed",fg='blue',font=("arial",16,"bold")).place(x=190,y=30)
    list1=['Operating System','Data Structure','Database Management','Algorithm','Digital Circuit']
    var.set("Select Subject")
    droplist=OptionMenu(window,var,*list1)
    droplist.config(width=20)
    droplist.place(x=200,y=150)
    button_ta=Button(window,text="Take Attendance",fg='White',command=takeatt,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
    button_ta.place(x=200,y=200)
    window.mainloop()
    def ok():
        print(var.get()) 


def view_att():
    window=Tk()
    window.title("View Attendance")
    window.geometry("600x400")
    label2=Label(window,text="View Attendance",fg='blue',font=("arial",16,"bold")).place(x=190,y=30)


def train_data():
    print("Machine Trained Successfully")
    recognizer=cv2.face.LBPHFaceRecognizer_create();
    path='dataSet'
    Ids,faces=getImagesWithID(path)
    recognizer.train(faces,np.array(Ids))
    recognizer.save('recognizer/trainningData.yml')
    cv2.destroyAllWindows()
    

window=Tk()
window.geometry("800x600")
window.title("aiAttendanceManagement")

label1=Label(window,text="Welcome to Attendance Management",fg='blue',font=("arial",16,"bold")).place(x=190,y=30)

button1=Button(window,text="Add Student",fg='White',command=add_stu,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button1.place(x=352,y=100)

button2=Button(window,text="Take Attendance",fg='White',command=take_att,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button2.place(x=335,y=180)

button3=Button(window,text="View Attendance",fg='White',command=view_att,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button3.place(x=335,y=260)

button4=Button(window,text="Train Machine",fg='White',command=train_data,bg='brown',relief=GROOVE,font=("arial",12,"bold"))
button4.place(x=335,y=340)


window.mainloop()
