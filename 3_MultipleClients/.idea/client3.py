import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))

while True:
    message = input("Type your message (type 'exit' or nothing to quit: ")
    if message.lower() == "exit" or not message:  # blanks or exit
        clientSocket.close()
        break
    else:
        clientSocket.sendall((message + '\n').encode('utf-8')) # Usual for TCP vs .send()