import socket
from math import ceil

def recv_line(sock):
    """
    Read a newline-delimited control message from the server.
    """
    buffer = b""
    while b"\n" not in buffer:
        data = sock.recv(8)
        if not data:
            return None
        buffer += data
    line, _ = buffer.split(b"\n", 1)
    return line.decode("utf-8")


HOST = socket.gethostbyname(socket.gethostname()) # Testing on the same PC, should point to the server IP
PORT = 9999

# Establish first connection
client_socket_A = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_A.connect((HOST, PORT))

# Request new session
client_socket_A.sendall(b"SESSION|NEW\n")

# Receive session ID (framed)
response = recv_line(client_socket_A)   # "SESSION|42"
_, session_id = response.split("|", 1)
session_id = int(session_id)

# Establish second connection and attach to the same session
client_socket_B = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_B.connect((HOST, PORT))
client_socket_B.sendall(f"SESSION|{session_id}\n".encode("utf-8"))

print(f"The session ID is {session_id}")

item_id = 0
chunk_size = 16 #hard-coded

while True:
    message = input("Type your message (type 'exit' or nothing to quit): ")
    if message.lower() == "exit" or not message:
        client_socket_A.close()
        client_socket_B.close()
        break
    else:
        message_length = len(message) # Later, chunk bytes, not chars
        total_chunks = ceil(message_length / chunk_size)

        pointer = 0
        for chunk_id in range(total_chunks):
            payload = message[pointer:pointer+chunk_size]
            frame = f"{item_id}|{chunk_id}|{total_chunks}|{payload}\n"

            # Deterministic multipath routing (even/odd chunks)
            if chunk_id % 2 == 0:
                print("Even Chunk")
                client_socket_A.sendall(frame.encode('utf-8'))
            else:
                print("Odd Chunk")
                client_socket_B.sendall(frame.encode('utf-8'))

            pointer += chunk_size

        item_id += 1