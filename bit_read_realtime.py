import serial
import socket
import sys
import time
from datetime import datetime

#f = open('out.txt','w')
serverIP = '192.168.43.245'
serverPort = 6125
Buffer_size = 1
packet_chars = 1

try:        
     clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     clientSocket.connect((serverIP, serverPort))
except:
     print "Error in connection"
     sys.exit(1)

def bits_to_string(binary_data):
    return ''.join(chr(int(binary_data[i:i + 8], 2)) for i in xrange(0, len(binary_data), 8))

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)

def removeParity(arr):
    retstr = ""
    for i in range(packet_chars):
        retstr += '0' + arr[8*i+1] + arr[8*i+2] + arr[8*i+3] + arr[8*i+4]+ arr[8*i+5]+ arr[8*i+6] + arr[8*i+7] 
    return bits_to_string(retstr)

def calculateParity(arr):
    for i in range(packet_chars):
        parity = 0
        for j in range(8):
            parity = parity ^ int(arr[8*i+j])
        if parity == 0:
            return False
    return True

def check_parity(arr):
    correct_parity = calculateParity(arr)
    if correct_parity:
        print "Sending ACK"
        clientSocket.send("1")
        return True
    else:
        print "Sending NACK"
        clientSocket.send("0")
        return False

packet_size = packet_chars*8 + 2
arr = ""
ct = 0
ser = serial.Serial('/dev/ttyACM0',115200)

while True:   
    arr = ""
    for j in range(5):
        s = ser.readline()
    for i in range(packet_size):
        sumbits = 0
        for k in range(5):
            s = ser.readline()
            s = s.strip()
            if k == 0 or k == 4:
                continue
            sumbits += (ord(s)-ord('0'))
        if i >= packet_size - 2:
            continue
        if sumbits > 1:
            arr += '1'
        else :
            arr += '0'

    if check_parity(arr) == 1:
    	print "Transferred character : ", removeParity(arr)
