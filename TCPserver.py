#!/usr/bin/env python
import socket
 
TCP_IP = '10.139.61.61'
TCP_PORT_PC1 = 5005
TCP_PORT_PC2 = 5006
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

PC1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PC1.bind((TCP_IP,TCP_PORT_PC1))
PC1.listen(1)

connPC1, addrPC1 = PC1.accept()

PC2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PC2.bind((TCP_IP, TCP_PORT_PC2))
PC2.listen(1)

connPC2, addrPC2 = PC2.accept()

# print 'Connection address:', addr
while 1:
	data1 = connPC1.recv(BUFFER_SIZE)
        print "received data1:", data1
        data2 = connPC2.recv(BUFFER_SIZE)
        print "received data2:", data2
       #do pwm
       #wait for ack
       #respond to ack    
 #  conn.send(data)  # echo
conn.close()

# def doPWM():
