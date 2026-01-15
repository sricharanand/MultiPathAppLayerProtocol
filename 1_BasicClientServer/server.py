import socket

# Making the socket... not known it's a server yet... need to bind to host and port
# AF_INET = internet socket
# SOCK_STREAM -> tcp, DGRAM is UDP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname()) # PRIVATE local IP address
#Same computer => just local host -> 127.0.0.1

PORT = 9999 # don't choose smth well known (80 for HTTP, 22 for SSH). Same port in client and server

serverSocket.bind((HOST, PORT)) #tuple

serverSocket.listen() # pass a number to accept the number of connections, optional

while True:
    # Accepting connections
    # Address of incoming connection
    # THE SERVER SOCKET ISN'T USED TO COMMUNICATE (server socket just listens accepts).
    # Each connection => Get a new socket
    communication_socket, address = serverSocket.accept()
    print(f"Connected to {address}")

    # Receiving. Waits if client doesn't send
    # Need to decode when receiving
    # Data is split by buffering, chunked transmission
    message = communication_socket.recv(1024).decode('utf-8') # buffer size -> 1024 bytes
    # Won't care about number of packets or wtv sent.
    # TCP is byte-stream, so it will receive upto 1024 bytes

    print(f"Message from client is: {message}")

    # Sending, need to encode so it's sent as byte streams
    communication_socket.send(f"Got your message. Thank you!".encode('utf-8'))
    communication_socket.close() # can not do it and send more messages

    print(f"Connection with {address} ended")


# Can't handle multiple connections at once -> Multithreading

# 1 socket to host - running, listening, accepting connections
# 1 socket for each client accepted


# Should loop over recv for real data - TCP won't deliver in the chunks I defined (network buffers etc)
