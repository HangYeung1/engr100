import serial
import time

ARDUINO_PORT = '/dev/cu.usbmodem11101'
ARDUINO_BAUD_RATE = 9600

ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE)

def setTurretPower(power):
    ser.write((str(-power) + '\n').encode())
    
def releaseCatapult():
    ser.write(("200\n").encode())

def loadTrooper():
    ser.write(("400\n").encode())



if __name__ == '__main__':
    try:
        while True:
            choice = input('Input: ').lower()

            if choice == 'end':
                ser.close()
                break

            ser.write((str(choice) + '\n').encode())

                
    except KeyboardInterrupt:
        ser.close()