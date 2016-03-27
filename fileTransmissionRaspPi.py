#!/usr/bin/env python 
import socket
import RPi.GPIO as GPIO
import time
import sys


def GPIO_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7, 0)


# Send the data in the form of light pulses.
def sendPacket(char):
    var = 0
    charBin = string_to_bits(char)
    charBin = [1, charBin[1], charBin[2], charBin[3], charBin[4], charBin[5], charBin[6], charBin[7]]
    for i in range(8):
        GPIO.output(7, int(charBin[i]))
        time.sleep(sleep)
        #  	print int(charBin[i])


# Convert the data from String to binary/bits.
def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)


# Sleep time for LED.
sleep = 1 / 100.0000

# Socket Connection fields.
TCP_IP = '10.139.64.106'
TCP_PORT_PC1 = 6004
TCP_PORT_PC2 = 6005
BUFFER_SIZE = 1

GPIO_init()

# PC1 connection.
try:
    PC1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PC1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    PC1.bind((TCP_IP, TCP_PORT_PC1))
    PC1.listen(1)
    connPC1, addrPC1 = PC1.accept()
    print 'PC1 Connected'
except:
    print 'TCP CONNECTION ERR - PC1'
    e = sys.exc_info()[0]
    print e
    PC1.shutdown(socket.SHUT_RDWR)
    PC1.close()
    sys.exit(1)

# PC2 connection.
try:
    PC2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PC2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    PC2.bind((TCP_IP, TCP_PORT_PC2))
    PC2.listen(1)
    connPC2, addrPC2 = PC2.accept()
    connPC2.settimeout(2)
    print 'PC2 connected'
except:
    print 'TCP CONNECTION ERR - PC2'
    PC1.close()
    PC2.close()
    sys.exit(1)

timeStart = time.time()
byteCount = 0
retransmissionCount = 0
errors = 0

while 1:
    # Receive the values from the sender.
    # It is a blocking call.
    dataToTransmit = connPC1.recv(BUFFER_SIZE)

    ack = None

    byteCount += 1
    timeoutCount = 0
    retransmit = 0
    currentError = 0

    print "input:", dataToTransmit
    if ord(dataToTransmit) != 127:
        sendPacket(dataToTransmit)
    else:
        sendPacket(dataToTransmit)
        timeEnd = time.time()
        serviceTime = timeEnd - timeStart
        print "Byte Count=", byteCount
        print "Retransmission Count =", retransmissionCount
        print "serviceTime =", serviceTime
        print "avg speed = (bps)", byteCount / serviceTime * 8
        print "Errors:", errors
        print "Error Rate:", errors * 1.0 / byteCount
        sys.exit(1)

    GPIO.output(7, 0)
    try:
        ack = connPC2.recv(BUFFER_SIZE)
        print "received1:", ack
    except socket.timeout:
        retransmit = 1
        print 'Socket timeout'
        pass

    # Check the ack. Compare with the transmitted bit and re-transmit accordingly.
    while ack != dataToTransmit and retransmit <= 3:
        # Check number of retransmission of the given character.
        sendPacket(dataToTransmit)
        GPIO.output(7, 0)
        try:
            ack = connPC2.recv(BUFFER_SIZE)
            if ack != dataToTransmit:
                retransmit += 1
            print "retransmission trials", retransmit
            print "received:", ack
        except socket.timeout:
            retransmit += 1
            print 'Socket timeout'
            pass
    # Increase the error count of, the transmission was not successful.
    if ack != dataToTransmit:
        errors += 1
