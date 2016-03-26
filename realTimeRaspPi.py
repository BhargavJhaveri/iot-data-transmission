#!/usr/bin/env python 
import socket
import RPi.GPIO as GPIO
import time

def GPIO_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7,0)

def TCPConn_inits():
    try:
        PC1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PC1.bind((TCP_IP, TCP_PORT_PC1))
        PC1.listen(1)
        connPC1, addrPC1 = PC1.accept()
    except:
        print 'TCP CONNECTION ERR - PC1'
        PC1.close()
        sys.exit(1)

    try:
    PC2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PC2.bind((TCP_IP, TCP_PORT_PC2))
    PC2.listen(1)
    connPC2, addrPC2 = PC2.accept()
    except:
        print 'TCP CONNECTION ERR - PC2'
        PC1.close()
        PC2.close()
        sys.exit(1)

def sendPacket(char):
    charBin = string_to_bits(char)
    for i in range(8):
	if i == 0:
	     GPIO.output(7, 1)
        else:
	     GPIO.output(7, charBin[i])
        time.sleep(sleep)

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)


sleep = 1/100.0000

TCP_IP = ''
TCP_PORT_PC1 = 5005
TCP_PORT_PC2 = 5006
BUFFER_SIZE = 1



GPIO_init()
TCPConn_inits()

while 1: #we need to finalize the protocol
    dataToTransmit = PC1.recv(BUFFER_SIZE)
    sendPacket(dataToTransmit)
    ack = PC2.recv(BUFFER_SIZE) #pc2 will return the data that it received
    while ack != dataToTransmit:
	sendPacket(dataToTransmit)


















