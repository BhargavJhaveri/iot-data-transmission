/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  /*analogWrite(3,32);
  //Serial.print("For 32:\n");
  for(int i=0;i<5;i++) {
    int sensorValue = analogRead(A0)-75;
    Serial.println(sensorValue);
    delay(25);
  }
  analogWrite(3,224);
  //Serial.print("For 224: \n");
  for(int i=0;i<5;i++) {
    int sensorValue = analogRead(A0)-75;
    Serial.println(sensorValue);
    delay(10);
  }
  analogWrite(3,96);
  //Serial.print("For 96:");
  for(int i=0;i<5;i++) {
    int sensorValue = analogRead(A0)-75;
    Serial.println(sensorValue);
    delay(25);
  }
  analogWrite(3,160);
  //Serial.print("For 160:");
  for(int i=0;i<5;i++) {
    int sensorValue = analogRead(A0)-75;
    Serial.println(sensorValue);
    delay(25);
  }
  // print out the value you read:
  //Serial.println(sensorValue);
  //delay(50);        // delay in between reads for stability
  */
  int sensorValue = analogRead(A0)-75;
  Serial.println(sensorValue);
  delay(5);
}
