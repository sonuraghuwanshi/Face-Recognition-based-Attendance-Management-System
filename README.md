# Face Recognition based Attendance Management System

Problem:  Suppose there are 60 students in the class and it took 8-10 second for the attendance of each so total 600 sec(10 min) in a lecture.
          So, generally in a day there is minimum 6 lectures. So, total 60min (1 hour) of a day goes in attendance.
          Challenge is to reduce this time.
          
Idea:     The idea is to implement the Face Recognition system. As our application recognise the face of the student it marks the attendance.

Requirements: Python 3, OpenCV, SQLite

How this works: Before moving on matching the faces, the biggest task is to let you machine know where is face in the picture. To encounter this,
                I have changed the image captured from camera to the grey scale image. Then using OpenCV module I have detected the face and created
                a rectangle around it. (in the FACEDETECT.py)
                
                Now its time to let your machine know who's face is this. As we know for training our machines we need a data set. So we have Entered
                a name and roll number and the clicked few (50-100) images of the student and this is how our data set is ready (in the datasetCreator.py)
                
                [you can check data set in Data set directory]
                
                Now its time to train the machine. So, using the dataset we are training our machine (in the tranner.py)
                
                [you can check trained data in the Recogniser directory]
                
                Now our machine is ready to detect the face from an image(frame of a video) and match that face in the dataset. But the problem is
                where we will store the attendance. For this we have used SQLite database management system. We have created a database with all our
                subject names, there total attendace, attendance of student and Enrollment number is used as primary key.
                
                So now we detect the face and matching it with the dataset. If face matches then it marks the attendance in the particular subject.(in the detector.py)
                
                start.py is the file from where program execution begins.
                
Features:       1) Add the student to the dataset
                2) Train the machine
                3) Take attendance
                4) View the attendance
 
Future Scope: We can train our machine to read the motion of students. Through these movements we can generate a report where we can calculate the interest of
              students in the particular class.
