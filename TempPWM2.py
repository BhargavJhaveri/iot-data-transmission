import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

GPIO.setup(7,GPIO.OUT)

GPIO.output(7,0)
sleep = 1/100.000000

#a = [0,1,0,0,0,0,0,1]
a = [0,0,0,0,1,1,1,1]
GPIO.output(7,0)
time.sleep(1/2.0)

#while True:
	#GPIO.output(7,1)
	#time.sleep(sleep)
	#GPIO.output(7,0)
	#time.sleep(sleep)
for j in range (100):
	i = 0
	for i in range (8):
		GPIO.output(7, a[i])
		time.sleep(sleep)
		print str(datetime.now())
	
time.sleep(1/2.0)































































































































































































