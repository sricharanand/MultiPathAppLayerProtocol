# Application Layer Framing (ALF):
# - TCP provides a reliable, in-order byte stream
# - Application defines message boundaries and meaning
# - Messages are chunked and reconstructed at receiver
# - Required for multi-path transmission and performance analysis

# Frame format:
# Item ID | Chunk ID | Total Chunks | Payload


import socket
from math import ceil

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

item_id = 0
chunk_size = 16 #hard-coded

while True:
    message = input("Type your message (type 'exit' or nothing to quit): ")
    if message.lower() == "exit" or not message: # blanks or exit
        client_socket.close()
        break
    else:
        message_length = len(message) # Later, chunk bytes, not chars
        total_chunks = ceil(message_length / chunk_size)

        pointer = 0
        for chunk_id in range(total_chunks):
            payload = message[pointer:pointer+chunk_size]
            frame = f"{item_id}|{chunk_id}|{total_chunks}|{payload}\n"

            client_socket.sendall(frame.encode('utf-8')) # Usual for TCP vs .send()
            # \n is the chunk delimiter now
            pointer += chunk_size

        item_id += 1