import serial
import sys
import struct
import socket
import time

serverIP = '10.139.61.61'
serverPort = 6020
Buffer_size = 1

ser_port = serial.Serial('/dev/ttyACM1',9600)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
f = open('out.txt','w')
#print "Open file",time.time()

while True:
    r=ser_port.read()
    temp = ord(r) - 128
    ser_port.write(chr(65))
    if(ord(r) == 255) :
        f.close()
        print "File trasnfer complete"
        #print time.time()
        clientSocket.send(r)
        time.sleep(0.5)
        break
        #sys.exit(1)
    elif(temp > 0) :
        #print chr(temp),r,temp
        time.sleep(1/100.0)
        clientSocket.send(chr(temp))
        print chr(temp)
        f.write(chr(temp))
        
    else:
        print "temp is less than zero"
        clientSocket.send('\0')

clientSocket.close()
