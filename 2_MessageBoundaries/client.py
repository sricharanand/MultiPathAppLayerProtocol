import socket

HOST = socket.gethostbyname(socket.gethostname())

PORT = 9999

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((HOST, PORT))

clientSocket.send("Hello World\n".encode('utf-8'))
clientSocket.send("This is the second message\n".encode('utf-8'))

clientSocket.close() #now important, else it will wait forever

#print(clientSocket.recv(1024).decode('utf-8')) # recv won't wait for more bytes to get to 1024