#!/usr/bin/env python 
import socket
import RPi.GPIO as GPIO
import time
import sys

def GPIO_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7,0)

def sendPacket(char):
    var = 0
    charBin = string_to_bits(char)
    '''print charBin'''
    charBin = [1, charBin[1], charBin[2], charBin[3], charBin[4], charBin[5], charBin[6], charBin[7]]
    '''print charBin'''
    for i in range(8):
	GPIO.output(7, int(charBin[i]))
        time.sleep(sleep)
  #  	print int(charBin[i])

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)


sleep = 1/100.0000

TCP_IP = '10.139.67.91'
TCP_PORT_PC1 = 5062
TCP_PORT_PC2 = 5063
BUFFER_SIZE = 1

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
    connPC2.settimeout(2)
except:
    print 'TCP CONNECTION ERR - PC2'
    PC1.close()
    PC2.close()
    sys.exit(1)


while 1: #we need to finalize the protocol
    dataToTransmit = connPC1.recv(BUFFER_SIZE)
    ack =  None
    timeoutCount = 0
    retransmit = 0
    print "input:",dataToTransmit
    sendPacket(dataToTransmit)
    GPIO.output(7, 0)
    try:
         ack = connPC2.recv(BUFFER_SIZE)
         print "received1:", ack
    except socket.timeout:
	 retransmit = 1
	 print 'Socket timeout'
         pass	
    if ack != dataToTransmit or retransmit == 1:
         sendPacket(dataToTransmit)
         GPIO.output(7, 0)
         try:
              ack = connPC2.recv(BUFFER_SIZE)
              print "received2:", ack
         except socket.timeout:
              retransmit = 0
              print 'Socket timeout'
              pass
