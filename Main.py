import cv2
from detection import detect_people
import time
from PID import PID 
from Serial import setTurretPower

def initialize():
    cap.set(3, 1280) # WIDTH
    cap.set(4, 720) # HEIGHT
    time.sleep(5)

cap = cv2.VideoCapture(1)
turnPID = PID(100, 0, 0)
turnPID.setTarget(0.5)
initialize()

while True:
    time.sleep(0.33)
    _, frame = cap.read()
    #cv2.imshow("PIC", frame)
    result = detect_people(frame)

    if result is None:
        setTurretPower(0)
        print("NOPE")
        continue
    else: 
        # Dislpay CV view
        personX = int(result[0] * frame.shape[1])
        personY = int(result[1] * frame.shape[0])
        cv2.rectangle(frame, (personX-25, personY-25), (personX + 25, personY + 25), (0,0,50), 2)
        cv2.putText(frame, "person", (personX, personY - 5), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,0,255) , 2, cv2.LINE_AA)
        cv2.imshow("frame", frame)
        cv2.waitKey(1)

    power = turnPID.step(result[0], 0.33)
    setTurretPower(power)