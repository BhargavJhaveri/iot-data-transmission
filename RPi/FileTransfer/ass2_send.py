import os
import binascii
import struct
import socket

# import zipfile

<<<<<<< HEAD
data_file = open('/Users/bhargav/Study/Study/Sem-II/IoT/Homework/HW2/Codes/iot-data-transmission/TextFile/Hello.txt', 'rb')
=======
data_file = open('/Users/bhargav/Study/Study/Sem-II/IoT/Homework/HW2/TextFile/Hello.txt', 'rb')
>>>>>>> f06eed518a89ec532c1ae0d737ac5e37bf8878ff

# Packet size of 64 bytes.
# packet_size = 1

checksum_size = 2

# Actual data size.
data_size = 4

# RPI_IP = 172

<<<<<<< HEAD
TCP_IP = '10.139.70.173'
TCP_PORT = 6027
BUFFER_SIZE = 256

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
except:
    print 'Socket Connection could not be setup'
=======
TCP_IP = '10.139.69.226'
TCP_PORT = 6006
BUFFER_SIZE = 256

# try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((TCP_IP, TCP_PORT))
# except:
#     print 'Socket Connection could not be setup'
>>>>>>> f06eed518a89ec532c1ae0d737ac5e37bf8878ff


def read_in_chunks(input_file, chunk_size=1024 * 64):
    chunk = input_file.read(chunk_size)
    return chunk


def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)


def bits_to_string(binary_data):
    # n = int(binary_data,2)
    # return binascii.unhexlify('%x' % n)
    return ''.join(chr(int(binary_data[i:i + 8], 2)) for i in xrange(0, len(binary_data), 8))


def transmit_bin_data():
    raw_data = 'START'

    while raw_data:

        # Read data in chunks. The data which is actually read is of the size, lesser than the packet size.
        raw_data = read_in_chunks(data_file, data_size)

        # print raw_data

        # Create the data packet. This packet will be sent over TCP.
        data_packet = create_data_packet(raw_data)

        # Keep track of number of re-transmissions.
        retransmissions = 0

        # Transmit and wait for the ACK.
        if transmit_data_over_tcp(data_packet):
            continue
        else:
            is_transmitted = False
            while retransmissions < 5 and not is_transmitted:
                retransmissions += 1
                is_transmitted = transmit_data_over_tcp(data_packet)


# def setup_connection():


# Transfer data over TCP to the Raspberry Pi.
def transmit_data_over_tcp(data):
<<<<<<< HEAD
    s.send(data)

    print 'Waiting for an ACK'
    ack = s.recv(BUFFER_SIZE)
=======
    # transmission_data = create_data_packet(data)
    # s.send(data)

    print 'Waiting for an ACK'
    # ack = s.recv(BUFFER_SIZE)
>>>>>>> f06eed518a89ec532c1ae0d737ac5e37bf8878ff
    print 'Received an ACK'

    return True


# Create data packet by adding checksum to the data bits.
def create_data_packet(data):
    pack_size = 0
    seq = ''
    if len(data) == 0:
        pack_size = 1
        print "pack_size is " + str(pack_size)
        first_byte = 192 | pack_size
        sync_byte = bin(first_byte).lstrip("0b")
        print "sync_byte is "
        print sync_byte
        seq = sync_byte
    else:
        pack_size = 3 + len(data)
        first_byte = 192 | pack_size
        print "pack_size is " + str(pack_size)
        sync_byte = bin(first_byte).lstrip("0b")
        checksum = bin(compute_checksum(data)).lstrip("0b").zfill(16)
        # print len(checksum)
        # Add first byte ( sync bits plus packet size)

        seq = sync_byte + checksum + string_to_bits(data)
        print "Checksum: 0x%04x" % compute_checksum(data)
    print "seq is : " + seq
    return ''.join(seq)


def carry_around_add(a, b):
    carry = a + b
    return (carry & 0xffff) + (carry >> 16)


def compute_checksum(message):
    sum_words = 0
    word = 0

    msg = ""
    i = 0
    # print len(message)
    while i < len(message) - 1:
        temp = hex(ord(message[i])).lstrip("0x")
        msg = msg + temp + ' '
        i += 1
    temp = hex(ord(message[i])).lstrip("0x")
    msg += temp

    # print "Msg is : "
    # print msg
    msg = msg.split()
    msg = map(lambda x: int(x, 16), msg)
    # print msg

    msg = struct.pack("%dB" % len(msg), *msg)
    for i in range(0, len(msg), 2):
        word = ord(msg[i]) + (ord(msg[i + 1]) << 8)
        sum_words = carry_around_add(sum_words, word)
    return ~sum_words & 0xffff


if __name__ == '__main__':
    # setup_connection()
    # setup_socket_connection()
    transmit_bin_data()
