import RPi.GPIO as GPIO
import time
from datetime import datetime
import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 6019
BUFFER_SIZE = 1

TCP_PC1 = '10.139.60.128'
PORT_PC1 = 6020

sleep = 1/250.000000

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)

def calculateParity(characterString):
    bitString = ''
    for i in range (len(characterString)):
         bits = string_to_bits(characterString[i])
         parity = 1
         for j in range (len(bits)):
              if j == 0:
                   continue
              else:
                   parity = parity ^ int(bits[j]) 
         bitString = bitString + str(parity) + bits[1] + bits[2] + bits[3] + bits[4] + bits[5] + bits[6] + bits[7]
    return bitString
   

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
except:
    print 'Socket Connection could not be setup'

try:
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect(TCP_PC1,PORT_PC1)
    f = open('test.txt','w')
    l = s1.recv(1024)
    while l:
	f.write(l)
	l = s1.recv(1024)
    f.close()
 	
except:
    print 'failed to connect to pc1'

f = open('test.txt', 'r')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

GPIO.output(7, 0)
time.sleep(2)
#print 'starting now'
while True:
	#a = 'abcdef'
	a = f.read(6)
        if len(a) == 0: #signifies end of file
		GPIO.output(7,1)
		time.sleep(sleep)
		for i in range(48)
			GPIO.ouput(7,0)
			time.sleep(sleep)	     
		break;
	c = ''
	for i in range (len(a)):
	     c = calculateParity(a)
	     #c = c + string_to_bits(a[i])
	#GPIO.output(7,1)
	#time.sleep(sleep)
	count = 0        
	ack = '0'
	while ack == '0' and count < 5:
	     	GPIO.output(7,1)
		time.sleep(sleep)
		for j in range (len(c)):
                  	GPIO.output(7, int(c[j]))
                  	time.sleep(sleep)
             	GPIO.output(7, 0)
             	time.sleep(3*sleep)
	     	ack = conn.recv(BUFFER_SIZE)
		count += 1   	     	
		#print 'ACK =' +ack
	     	ack = '1'
print "file is over"












