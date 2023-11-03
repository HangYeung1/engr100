import cv2
from detection import detect_people
import time


def initialize():
    cap.set(3, 1280) # WIDTH
    cap.set(4, 720) # HEIGHT
    time.sleep(5)

print("WASSUP")
cap = cv2.VideoCapture(1
                       )
initialize()
while True:
    print("MOREHI")
    time.sleep(0.33)
    _, frame = cap.read()
    cv2.imshow("PIC", frame)
    result = detect_people(frame)

    if result is None:
        print("NOPE")
        continue

    print(result)


