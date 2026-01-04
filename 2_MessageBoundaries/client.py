import socket

HOST = '192.168.68.108'

PORT = 9999

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((HOST, PORT))

clientSocket.send("Hello World\n".encode('utf-8'))
clientSocket.send("This is the second message\n".encode('utf-8'))

print(clientSocket.recv(1024).decode('utf-8')) # recv won't wait for more bytes to get to 1024