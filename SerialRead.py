import serial
import sys
import struct

ser_port = serial.Serial('/dev/ttyACM0',9600,timeout=1)
first_packet = 1
last_packet = 0
size_mask = 0x3f
f = open('output_file', 'wb')
pa_size = 1
message = 'A'

def bytes2int(str):
 return ord(str)

def carry_around_add(a,b):
    carry = a+b
    return (carry & 0xffff) + (carry >> 16)

def readByte():
    global ser_port
    return ser_port.read()

def calChecksum():
    global ser_port
    global pa_size
    global message
    sum_words = 0
    word = 0
    """ Forming bytearray of payload by removing first 3 bytes
    1 sync/size byte and 2 checksum bytes"""
    #message = bytearray()
    #message.extend(readByte())
    message = []
    if pa_size == 4:
        a = readByte()
        message.append(a)
        a = '0' 
        message.append(a[0])
    else:
        while pa_size > 4:
            a = readByte()
            message.append(a)
            pa_size = pa_size - 1
    data = message.pack("%dB" % len(data), *message)
    for i in range(0,len(message), 2):
        word = ord(message[i]) + (ord(message[i+1]) << 8)
        sum_words = carry_around_add(sum_words,word)
    return ~sum_words & 0xffff

def detectError():
    global ser_port
    global pa_size
    #checksum_firstbyte = readByte()		
    #checksum_secondbyte = readByte()		
    ''' Extracting 16 bits checksum'''
    checksum = bytearray()
    checksum.extend(readByte())
    a = readByte()
    checksum.extend(a)
   
    if calChecksum() == checksum:
        return 1
    else:
        return 0
    
while True:
    first_byte = bytearray()
    first_byte.extend(readByte())



    print first_byte
    if first_packet == 0:
        pa_size = ord(first_byte) & size_mask

        if pa_size == 1:
            last_packet = 1
            f.close()
        else:
            print "Checking checksum"
    """
            if detectError() == 1:
 	        #sendNACK()
                print "send NACK"
	    else:
                #sendACK()
                print "send ACK"
                f.write(message)
    """              
                                 
    if first_packet == 1:
        pa_size = ord(first_byte) & size_mask
        if pa_size == 1:
            last_packet = 1
            f.close()
        else:
	    while pa_size > 1:
                first_oct = bytearray()
	        first_oct.extend(readByte())
                second_oct = bytearray()
	        second_oct.extend(readByte())
                third_oct = bytearray()
	        third_oct.extend(readByte())
                fourth_oct = bytearray()
	        fourth_oct.extend(readByte())
                serverIP = str(first_oct)+'.'+str(second_oct)+'.'+str(third_oct)+'.'+str(fourth_oct)
            	pa_size = pa_size - 4
 			
	    first_packet = 0
        
	
