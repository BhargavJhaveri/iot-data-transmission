import socket

serverIP = '192.168.0.22'
serverPort = 8000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverIP,serverPort))
serverSocket.listen(1)
print 'THe server is ready to receive'

while 1:
        connectionSocket, addr = serverSocket.accept()

        ACK = connectionSocket.recv(1024)

        if ACK == '11110000':
                print 'Received ACK:',ACK
                msg = 'ACK Received'
                print msg
                connectionSocket.send(msg)

        else:
                print 'Received NACK:',ACK
                msg = 'NACK Received. Retransmitting data'
                print msg
                connectionSocket.send(msg)


connectionSocket.close()



