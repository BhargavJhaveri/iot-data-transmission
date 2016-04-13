import serial
import socket
import sys
import time
from datetime import datetime
import thread
import os
from Queue import Queue

#f = open('out.txt','w')
serverIP = '192.168.43.245'
serverPort = 6072
Buffer_size = 1

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))


def bits_to_string(binary_data):
    return ''.join(chr(int(binary_data[i:i + 8], 2)) for i in xrange(0, len(binary_data), 8))

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)

def removeParity(arr):
    retstr = ""
    for i in range(6):
        retstr += '0' + arr[8*i+1] + arr[8*i+2] + arr[8*i+3] + arr[8*i+4]+ arr[8*i+5]+ arr[8*i+6] + arr[8*i+7] 
    print bits_to_string(retstr)
    return bits_to_string(retstr)

def calculateParity(arr):
    for i in range(6):
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
        
packet_size = 6*8 + 2
arr = ""
ct = 0
ser = serial.Serial('/dev/ttyACM0',115200)

   
f = open('output.txt','w')

def lastPacket(arr):
    sum_of_bits = 0
    count = 0
    for i in range(len(arr)):
        count = count + 1
        if i%8 == 0:
            continue
        sum_of_bits = sum_of_bits + int(arr[i])
        if count == 8:
            if sum_of_bits == 0:
                print "last packet ", sum_of_bits
       	        return sum_of_bits
            else:
                count = 0
                sum_of_bits = 0
    return 1 

num_of_bits = 0
isTimeToStart = 0
start_time = datetime.now()
end_time = datetime.now()
trackLastPacket = 0

while True:   
    arr = ""
    for j in range(5):
        s = ser.readline()
        if isTimeToStart == 0:
            start_time = datetime.now()
            print "Start time Timestamp " ,start_time
            isTimeToStart = 1
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
                
        
    #print arr 
    if lastPacket(arr) == 0:
        f.close()
        end_time = datetime.now()
        total_time = end_time - start_time
        #transfer_speed = num_of_bits / total_time
        print "File transfer is completed"
        print "Number of bits transferred " , num_of_bits
        print "End time Timestamp " ,end_time
        print "Total time taken " , total_time 
        #print "Transfer speed in bits/second ", transfer_speed
        sys.exit(1)
       
    if check_parity(arr):
        num_of_bits = num_of_bits + len(arr)
        f.write(removeParity(arr))
   
