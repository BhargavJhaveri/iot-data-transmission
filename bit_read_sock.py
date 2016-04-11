import serial
import socket
import sys
import time
from datetime import datetime
import thread
import os
from Queue import Queue
"""
myQ=Queue()

def read_ser(threadname,):
    ser = serial.Serial('/dev/ttyACM1',9600)
    while True:
        s = ser.readline()
        #print s
        myQ.put(s[0])


def write_file(thhrd,):
    print "file open"
    f = open('out.txt','w')
    i=0
    while True:
        if (myQ.empty() == 0):
            w = myQ.get()
            #print "read char",w
            f.write(w)
    f.close()

if __name__ == '__main__':
    print "launching thread"
    thread.start_new_thread(read_ser,("ser",))
    print "launching thread2"
    thread.start_new_thread(write_file,("fil",))
    while True:
        pass
"""
f = open('out.txt','w')
serverIP = '10.139.66.186'
serverPort = 6005
Buffer_size = 1

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))


def bits_to_string(binary_data):
    # n = int(binary_data,2)
    # return binascii.unhexlify('%x' % n)
    return ''.join(chr(int(binary_data[i:i + 8], 2)) for i in xrange(0, len(binary_data), 8))

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)

def removeParity(arr):
    retstr = ""
    for i in range(6):
        retstr += '0' + arr[8*i+1] + arr[8*i+2] + arr[8*i+3] + arr[8*i+4]+ arr[8*i+5]+ arr[8*i+6] + arr[8*i+7] 
        print bits_to_string(retstr)
    #print bits_to_string(retstr)
    return bits_to_string(retstr)

def calculateParity(arr):
    for i in range(6):
        parity = 0
        for j in range(8):
            parity = parity ^ int(arr[i*6+j])
        if parity == 0:
            return False
    return True
    

def check_parity(arr):
    #if parity ok, remove msb, write to file,send ack
    faultFlag = False
    for i in range(6):
        #if not calculateParity(arr):
        #    faultFlag = True
        #    break
        pass
    if faultFlag == True:
        clientSocket.send("0")
    else:
        clientSocket.send("1")
        f.write(removeParity(arr))
    


packet_size = 6*8 + 2
arr = ""
ct = 0
ser = serial.Serial('/dev/ttyACM3',115200)


   
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
            #print ord(s)-ord('0')
            sumbits += (ord(s)-ord('0'))
        #print ct,':',sumbits
        if i >= packet_size - 2:
            continue
        if sumbits > 1:
            arr += '1'
        else :
            arr += '0'
        #print arr, len(arr)
    #print bits_to_string(arr)
    print removeParity(arr)
    check_parity(arr)
    #print datetime.now()
