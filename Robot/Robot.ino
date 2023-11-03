#include <Servo.h>

const int MAX_INPUT_LENGTH = 15;
int command = 0; 

Servo releaser;
Servo slider;
Servo leftTurret;
Servo rightTurret;
Servo winch;

void setup() {
  releaser.attach(9);
  releaser.writeMicroseconds(500);

  slider.attach(15);
  leftTurret.attach(8);
  rightTurret.attach(10);
  winch.attach(16);
  Serial.begin(9600);
}

// input: [-100, 100]
void setTurretPower(int power){
  leftTurret.writeMicroseconds(1500 + power * 5);
  rightTurret.writeMicroseconds(1500 - power * 5);
}

// 200
void release(){
  releaser.writeMicroseconds(1000);
  delay(1500);
  releaser.writeMicroseconds(500);
}

// 300
void rewind(){
  winch.writeMicroseconds(2000);
  delay(2000);
  winch.writeMicroseconds(1500);
}

// 400
void addPayload(){
  slider.writeMicroseconds(2000);
  delay(1000);
  slider.writeMicroseconds(1500);
}

void processByte(const byte input){
  static char inputLine[MAX_INPUT_LENGTH];
  static unsigned int index = 0;

  if(input == 'r'){
    return;
  }

  if(input == '\n'){
    inputLine[index] = 0;  
    index = 0;  
    command = atoi(inputLine);
  }

  if (index < MAX_INPUT_LENGTH - 1){
    inputLine[index++] = input;
  } 
} 

void loop() {
  delay(10);
  if(!Serial.available()){
    return;
  }
  
  while(Serial.available()){
    int data = Serial.read();
    processByte(data);
  }

  if(command == 200){
    release();
  }

  // if(command == 300){
  //   rewind();
  // }

  // if(command == 400){
  //   addPayload();
  // }

  if(command >= -100 && command <= 100){
    setTurretPower(command);
  }




}
