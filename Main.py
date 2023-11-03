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

    power = turnPID.step(result[0], 0.33)
    setTurretPower(power)


