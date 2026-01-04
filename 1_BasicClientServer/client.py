import socket

# HOST for client.py is the IP of the server
# If this is on the internet, we need to specify the PUBLIC IP address (from website myip.is)
# Here, on same computer => Same
HOST = '192.168.68.108'

# PORT is same as server
PORT = 9999

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Not hosting. Connect
clientSocket.connect((HOST, PORT))

# Sends a request to the server, who must accept

clientSocket.send("Hello World".encode('utf-8'))
clientSocket.send("This is the second message.".encode('utf-8')) # Second message.

# Observation in server -> "Hello WorldThis is the second message"
# No newline character or any boundary <- TCP IS BYTESTREAM PROTOCOL (sends continuous stream of bytes)
# Applications need to define the boundaries of 'messages' (\n, length, an application lvl protocol etc)
# TCP just says "Give me upto 1024 bytes and imma send it"
# TCP, however, preserves order and reliability

print(clientSocket.recv(1024).decode('utf-8')) #b prefixing in terminal => Not decoded


# Instead of Hello World, we'll have data chunks - multiple chunks, or encoded shares
# We'll have multiple sockets and paths instead of a single connection

# Some application-layer methods to define boundaries
# 1) Delimiters -> \n
# 2) Fixed sized chunks
# 3) LENGTH PREFIXING - Send <4 bytes length><message bytes> -> Read length then that many bytes
# This is the principle of chunking, secret sharing, and reconstruction (imp for the project)