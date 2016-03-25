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
    message = message.pack("%dB" % len(message), *message)
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


ser_port.write(chr(65))
while True:
    a = readByte()
    if not a:
        continue
    print "New character is seen with length : "+ " "+ a +" " + str(len(a))

    first_byte = bytearray()
    first_byte.extend(a)

    if first_packet == 0:
        pa_size = ord(first_byte) & size_mask
        print "\nPacket size is :" + str(pa_size)

        if pa_size == 1:
            last_packet = 1
            f.close()
        else:
            print "Checking checksum"
    
            if detectError() == 1:
 	        #sendNACK()
                print "send NACK"
	    else:
                #sendACK()
                print "send ACK"
                f.write(message)
                 
                                 
    if first_packet == 1:
        pa_size = ord(first_byte) & size_mask
        print "First Packet size is :" + str(pa_size)
        if pa_size == 1:
            last_packet = 1
            f.close()
        else:
	    while pa_size > 1:
                first_oct = ord(readByte())
                second_oct = ord(readByte())
                third_oct = ord(readByte())
                fourth_oct = ord(readByte())
                serverIP = str(first_oct)+'.'+str(second_oct)+'.'+str(third_oct)+'.'+str(fourth_oct)
                print "ServerIP is : " + serverIP
            	pa_size = pa_size - 4
 			
	    first_packet = 0
        
