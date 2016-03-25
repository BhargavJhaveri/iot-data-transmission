import serial
import sys

ser_port = serial.Serial('/dev/ttyACM0',9600,timeout=1)
first_packet = 1
last_packet = 0
size_mask = 0x3f
f = open('output_file', 'wb')
pa_size = 1
message = 'A'

def carry_around_add(a,b):
    carry = a+b
    return (carry & 0xffff) + (carry >> 16)

def calChecksum():
    global ser_port
    global pa_size
    global message
    sum_words = 0
    word = 0
    """ Forming bytearray of payload by removing first 3 bytes
    1 sync/size byte and 2 checksum bytes"""
    message = bytearray(ser_port.read())
    if pa_size == 4:
        a = ser_port.read()
        message.append(a[0])
        a = 0x00
        message.append(a[0])
    else:
        while pa_size > 4:
            a = ser_port.read()
            message.append(a[0])
            pa_size = pa_size - 1

    for i in range(0,len(message), 2):
        word = ord(message[i]) + (ord(message[i+1]) << 8)
        sum_words = carry_around_add(sum_words,word)
    return ~sum_words & 0xffff

def detectError():
    global ser_port
    global pa_size
    #checksum_firstbyte = ser_port.read()		
    #checksum_secondbyte = ser_port.read()		
    ''' Extracting 16 bits checksum'''
    checksum = ser_port.read()
    a = ser_port.read()
    checksum.append(a[0])
   
    if calChecksum() == checksum:
        return 1
    else
        return 0
    
while True:
    first_byte = ser_port.read()
    if first_packet == 0:
        pa_size = first_byte & size_mask

        if pa_size == 1:
            last_packet = 1
            f.close()
        else:
            if detectError() == 1:
 	        sendNACK()
	    else:
                sendACK()
                f.write(message)
                
                                 
    if first_packet == 1:
        pa_size = first_byte & size_mask
        if pa_size == 1:
            last_packet = 1
            f.close()
        else:
	    while pa_size > 1:
	        first_oct = ser_port.read()
	        second_oct = ser_port.read()
	    	third_oct = ser_port.read()
	    	fourth_oct = ser_port.read()
            	pa_size = pa_size - 4
 			
	    first_packet = 0
        
	
