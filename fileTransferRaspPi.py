#!/usr/bin/env python 
import socket
import RPi.GPIO as GPIO
import time
import sys

def GPIO_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7,0)

def sendPacket(binString):
    for i in range(len(binString)):
	GPIO.output(7, int(binString[i]))
        time.sleep(sleep)
  #  	print int(charBin[i])

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)


sleep = 1/100.0000

TCP_IP = '10.139.67.91'
TCP_PORT_PC1 = 6000
TCP_PORT_PC2 = 6001
BUFFER_SIZE = 256
ACK = '11110000'
NACK = '00001111'

GPIO_init()

try:
    PC1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PC1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    PC1.bind((TCP_IP, TCP_PORT_PC1))
    PC1.listen(1)
    connPC1, addrPC1 = PC1.accept()
except:
    print 'TCP CONNECTION ERR - PC1'
    e = sys.exc_info()[0]
    print e
    PC1.shutdown(socket.SHUT_RDWR)
    PC1.close()
    sys.exit(1)

try:
    PC2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PC2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    PC2.bind((TCP_IP, TCP_PORT_PC2))
    PC2.listen(1)
    connPC2, addrPC2 = PC2.accept()
    connPC2.settimeout(20)
except:
    print 'TCP CONNECTION ERR - PC2'
    PC1.close()
    PC2.close()
    sys.exit(1)


while 1: #we need to finalize the protocol
    dataToTransmit = connPC1.recv(BUFFER_SIZE)
    ack =  None
    retransmit = 0
    packetCount = 0
    print "new packet"
    sendPacket(dataToTransmit)
    GPIO.output(7, 0)
    try:
         ack = connPC2.recv(BUFFER_SIZE)
         print "received1:", ack
    except socket.timeout:
	 retransmit = 1
	 print 'Socket timeout'
         pass	
    if ack == NACK or retransmit == 1:
         sendPacket(dataToTransmit)
         GPIO.output(7, 0)
         try:
              ack = connPC2.recv(BUFFER_SIZE)
              print "received2:", ack
         except socket.timeout:
              retransmit = 0
              print 'Socket timeout'
              pass
    else
        connPC1.send("1")