import serial
import time

ARDUINO_PORT = '/dev/cu.usbmodem21301'
ARDUINO_BAUD_RATE = 9600

ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE)

def releaseCatapult():
    ser.write(("200\n").encode())

def setTurretPower(power):
    ser.write((str(power) + '\n').encode())

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