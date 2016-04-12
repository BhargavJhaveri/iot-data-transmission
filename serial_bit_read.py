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
def bits_to_string(binary_data):
        # n = int(binary_data,2)
        # return binascii.unhexlify('%x' % n)
        return ''.join(chr(int(binary_data[i:i + 8], 2)) for i in xrange(0, len(binary_data), 8))

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
    print bits_to_string(arr)
    #print datetime.now()
