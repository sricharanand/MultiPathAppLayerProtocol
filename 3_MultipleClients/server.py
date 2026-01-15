import socket
import threading #To handle multiple connections

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

def start():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.bind((HOST, PORT))
    serverSocket.listen()

    return serverSocket

def handle_client(communication_socket, address):
    applicationBuffer = ""
    fragment = ""

    while True:
        fragment = communication_socket.recv(8)
        if not fragment:
            break

        applicationBuffer += fragment.decode('utf-8')
        while '\n' in applicationBuffer:
            msg, applicationBuffer = applicationBuffer.split('\n', 1)
            print(f"[{address}]: {msg}")

    communication_socket.close()
    print(f"Connection with {address} ended")

def main():
    listeningSocket = start()

    while True:
        communicationSocket, address = listeningSocket.accept()
        thread = threading.Thread(target = handle_client, args = (communicationSocket, address))
        thread.start()
        print(f"Active Connections: {threading.active_count() - 1}")

main()
