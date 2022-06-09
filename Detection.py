import cv2
import os
from main import Main
from playsound import playsound
import time

main = Main()
webcam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
currentChar = ''
previousChar = ''
message = ''
is_message_final = False

def countdown(time_sec): #5 sec
    """A timer before the sound alarm is
    triggered and followed by a voice response"""
    while time_sec:
        mins, secs = divmod(time_sec, 60) #5/ 60 = 0min , 5 sec
        timeformat = '{:02d}'.format( secs)
        print(timeformat, end='\r\n')
        time.sleep(1)
        time_sec -= 1
        if State == "Awake":
            break
    song=playsound('alarm.mp3')
    main.voice_action("Stop by and get some sleep, or you can stop and have a cup of coffee")
    os.remove("main/tmp.mp3")
    
while True:
    # We get a new frame from the webcam
    ret , frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    main.refresh(frame)
    

    frame = main.annotated_frame()
    

    if main.pupils_located:
        State = "Awake"
        currentChar = " "
        
    elif main.blink_action():
        State = "sleep"
        currentChar = "/"

    else:
        State = "sleep"
        currentChar = "/"
        
    #detect eye pupile
    cv2.putText(frame, State, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.0, (147, 58, 31), 2)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    left_pupil = main.pupil_left_coords()
    right_pupil = main.pupil_right_coords()
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around the face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
    cv2.imshow("Our Frame", frame)
    if (currentChar != previousChar) and not is_message_final:
            print(currentChar)
            message = message + currentChar
            if message.endswith('/////////////////////////////////'):
                countdown(5)
                
                
    
    cv2.imshow("Demo", frame)


    if cv2.waitKey(1) == 27:
        break
        break
   
webcam.release()
cv2.destroyAllWindows(q)
