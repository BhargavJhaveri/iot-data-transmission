import serial
import sys
import struct
import socket
import time

serverIP = '10.139.66.146'
serverPort = 5071
Buffer_size = 1

ser_port = serial.Serial('/dev/ttyACM1',9600)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

while True:
    r=ser_port.read(1)
    temp = ord(r) - 128
    print "read character",r
    ser_port.write(chr(65))
    if(temp > 0) :
        print chr(temp),r,temp
        time.sleep(1/20.0)
        clientSocket.send(chr(temp))
        print "Sent ACK", chr(temp)
    else:
        print "temp is less than zero"
        clientSocket.send('\0')

clientSocket.close()
