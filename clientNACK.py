import socket

serverIP = '192.168.0.22'
serverPort = 8000
Buffer_size = 20

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

print 'Data not received successfully'

NACK = '00001111'
#NACK = message(4), '0000'
clientSocket.send(NACK)
Info = clientSocket.recv(Buffer_size)

print 'From Server:', Info
clientSocket.close()


