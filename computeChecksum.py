import struct

def carry_around_add(a,b):
    carry = a+b
    return (carry & 0xffff) + (carry >> 16)

def compute_checksum(message):
    i = 0
    while i < len(message)-1:
        temp = hex(ord(message[i])).lstrip("0x")
        msg = msg + temp + ' '
        i = i + 1
    temp = hex(ord(message[i])).lstrip("0x")
    msg = msg + temp

    print "Msg is : "
    print msg
    msg = msg.split()
    msg = map(lambda x: int(x,16), msg)
    print msg

    msg = struct.pack("%dB" % len(msg), *msg)
    for i in range(0,len(msg), 2):
        word = ord(msg[i]) + (ord(msg[i+1]) << 8)
        sum_words = carry_around_add(sum_words,word)
    return ~sum_words & 0xffff

