#!/usr/bin/env python

import socket


TCP_IP = '10.139.57.24'
TCP_PORT = 5006
BUFFER_SIZE = 1  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    ch = conn.recv(BUFFER_SIZE)
    print ch
    print ord(ch)
    if ch == 'q':
    	break
    print "in"
    for i in range (10000000):
    	x = 0
    print "out"

    # print "received data:", data
    # conn.send(data)  # echo
 #    conn, addr = s.accept()
	# print 'Connection address:', addr
# conn.close()
s.close()
sys.exit()