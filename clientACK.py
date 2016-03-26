import socket

serverIP = '192.168.0.22'
serverPort = 8000
Buffer_size = 20

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

ACK = '11110000'
#ACK = message(4), '1111'
clientSocket.send(ACK)
Info = clientSocket.recv(Buffer_size)

print 'From Server:', Info
clientSocket.close()


