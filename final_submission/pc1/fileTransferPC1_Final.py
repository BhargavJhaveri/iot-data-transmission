import os
import binascii
import struct
import socket

try:
    data_file = open('hello.txt','rb')
except:
    print "error opening file"
    sys.exit(1)


TCP_IP_RaspPi = '192.168.43.245'
TCP_PORT_RaspPi = 6047
BUFFER_SIZE = 8192

# Socket Connection setup.
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP_RaspPi, TCP_PORT_RaspPi))
except:
    print 'Socket Connection could not be setup'


# Read the source file in chunks.
def read_in_chunks(input_file, chunk_size=BUFFER_SIZE):
    chunk = input_file.read(chunk_size)
    return chunk


# Transmit the data.
def transmit_bin_data():
    raw_data = 'START'

    while raw_data:

        # Read data in chunks. The data which is actually read is of the size, lesser than the packet size.
        raw_data = read_in_chunks(data_file, data_size)
        if len(raw_data) == 0:
            break;

        # Transmit and wait for the ACK.
        if transmit_data_over_tcp(raw_data):
            continue
    transmit_data_over_tcp(chr(127))
    print "File Sent"


# def setup_connection():


# Transfer data over TCP to the Raspberry Pi.
def transmit_data_over_tcp(data):
    s.send(data)
    return True




