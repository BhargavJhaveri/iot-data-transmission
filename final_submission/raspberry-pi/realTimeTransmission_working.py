import RPi.GPIO as GPIO
import time
from datetime import datetime
import socket

TCP_IP = '0.0.0.0'
TCP_PORT_PC1 = 6124
TCP_PORT_PC2 = 6125
BUFFER_SIZE_PC1 = 1
BUFFER_SIZE_PC2 = 1

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
    PC1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PC1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    PC1.bind((TCP_IP, TCP_PORT_PC1))
    PC1.listen(1)
    conn_PC1, addr_PC1 = PC1.accept()
    print "PC1 Connected"
except:
    print 'Socket Connection could not be setup: PC2'

try:
    PC2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PC2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    PC2.bind((TCP_IP, TCP_PORT_PC2))
    PC2.listen(1)
    conn_PC2, addr_PC2 = PC2.accept()
    print "PC2 Connected"
except:
    print 'Socket Connection could not be setup: PC2'

outputFile = open("tempOut.txt", "w")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

GPIO.output(7, 0)
time.sleep(2)
#print 'starting now'
while True:
	#a = 'abcdef'
        buffer = conn_PC1.recv(BUFFER_SIZE_PC1)
#        print "Buffer: ", buffer
#        print "length: ", str(len(buffer))
        if len(buffer) == 0: #signifies end of file
	     """GPIO.output(7,1)
	     time.sleep(sleep)
	     for i in range(48):
		GPIO.output(7,0)
		time.sleep(sleep)
	     break;"""
             continue
	c = ''
	for i in range (len(buffer)):
	     c = calculateParity(buffer)
#	     print c
	     #c = c + string_to_bits(a[i])
#	GPIO.output(7,1)
#	time.sleep(sleep)
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
	     ack = conn_PC2.recv(BUFFER_SIZE_PC2)
	     count = count + 1
#             print ack

#   	     print 'ACK =' +ack
	     #ack = '1'
