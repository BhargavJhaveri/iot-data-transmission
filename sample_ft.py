import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

sleep = 1/200.0000
GPIO.setup(7,GPIO.OUT)

GPIO.output(7,0)



def sendPacket(binString):
    for i in range(len(binString)):
	GPIO.output(7, int(binString[i]))
	#if i%8 == 0:
		#print ' '
	#print int(binString[i])
        time.sleep(sleep)


f = open('hello.txt','rb')
l = f.read(8);
#print l
bindata = ''.join(bin(ord(ch))[2:].zfill(8) for ch in l)
sendPacket('11001001')
sendPacket(bindata)
GPIO.output(7, 0)

time.sleep(1/2.0)
print "Done"






























































































































































































