/*
  DigitalReadSerial
 Reads a digital input on pin 2, prints the result to the serial monitor 
 
 This example code is in the public domain.
 */
#include <TimerOne.h>

// digital pin 2 has a pushbutton attached to it. Give it a name:
int pushButton = 2;
volatile int counter;
volatile int bits_read;
volatile byte buttonState;
volatile byte byte_read;
volatile int charshift;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
  counter = 0;
  attachInterrupt(0,start_sync,RISING);
  
}

void start_sync() {
  counter++;
  //Serial.println(counter);
}

void readbit() {
  buttonState = digitalRead(pushButton);    
  byte_read <<= 1;
  byte_read = byte_read | buttonState;
  charshift++;  
}

// the loop routine runs over and over again forever:
void loop() {
  if(counter) {
    Serial.println("Inturrupt caught, start reading bitstream");
    detachInterrupt(0);
    charshift = 0;
    byte_read = 0;    
    delay(8);
    buttonState = digitalRead(pushButton);    
    byte_read <<= 1;
    byte_read = byte_read | buttonState;
    charshift++;  

    Timer1.initialize(20000);
    Timer1.attachInterrupt( readbit );
    while(!Serial.available()) {
      if(charshift >=8 ){
        Serial.println(byte_read);
        byte_read = 0;
        charshift = 0;
      }
      continue;
    }
    counter = 0;
    Serial.read();
    Serial.println("Pausing, waiting for another interrupt");
    attachInterrupt(0,start_sync,RISING);
  }
}

