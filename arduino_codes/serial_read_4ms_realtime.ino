#include <TimerOne.h>

// digital pin 2 has a pushbutton attached to it. Give it a name:
int pushButton = 2;
int dummy;
long sampling_interval = 810;
volatile int counter;
volatile int bits_read;
byte buttonState;
byte first_buttonstate;
volatile byte byte_read;
int no_of_char = 1;
int packet_size = (1 + 2 + 8*no_of_char)*5;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
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
  //Serial.print(bits_read);
  //Serial.print(":");
  Serial.println(buttonState);     
  bits_read++;
}

// the loop routine runs over and over again forever:
void loop() {
  if(counter) {
    //Serial.println("Inturrupt caught, start reading bitstream");
    detachInterrupt(0); //no more looking for rising edge
    bits_read = 0;      //no bits read till now, clear read byte
    byte_read = 0;    
    delay(1);
    first_buttonstate = digitalRead(pushButton);
    Timer1.initialize(sampling_interval);
    if(first_buttonstate){      //only if buttonState is 1, go continue sampling
      //Timer1.initialize(sampling_interval);    //Timer stuff, starts sampling from instance (0, 1, 2....)* sampling_interval
      //Serial.println("interrupt");
      Timer1.attachInterrupt( readbit );      
      while(bits_read != packet_size ){
        ;
      }
      //coming out of loop? ok, set everything as it was at the start
      
      //Serial.println("Pausing, waiting for another interrupt");

    }
    Timer1.detachInterrupt();
    Timer1.stop();
    counter = 0;                              
    delay(1);
    attachInterrupt(0,start_sync,RISING);
  }
}

