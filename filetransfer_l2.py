import serial
import sys
import struct
import socket
import time

serverIP = '10.139.64.106'
serverPort = 6005
Buffer_size = 1

ser_port = serial.Serial('/dev/ttyACM1',9600)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
f = open('out.txt','w')

while True:
    r=ser_port.read()
    temp = ord(r) - 128
    ser_port.write(chr(65))
    if(ord(r) == 255):
        print "File transfer complete"
        clientSocket.send(r)
        time.sleep(0.5)
        f.close()
        break
    if(temp > 0) :
        time.sleep(1/100.0)
        f.write(chr(temp))
        clientSocket.send(chr(temp))
    else:
        print "temp is less than zero",ord(r)
        clientSocket.send('\0')

print ord(r)
clientSocket.close()
