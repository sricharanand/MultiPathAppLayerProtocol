import socket
import threading #To handle multiple connections

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    return server_socket

def handle_client(communication_socket, address):
    items = dict() # key is the item_id, value is the dict with chunks
    byteBuffer = b""

    while True:
        fragment = communication_socket.recv(8)
        if not fragment:
            break

        # TCP Fragments bytes
        # Application Layer reconstructs records (frames)
        # Decode only AFTER the record is obtained

        byteBuffer += fragment

        while b'\n' in byteBuffer:
            frame_bytes, byteBuffer = byteBuffer.split(b'\n', 1)

            frame = frame_bytes.decode('utf-8')
            item_id, chunk_id, total_chunks, payload = frame.split('|', 3)
            item_id = int(item_id)
            chunk_id = int(chunk_id)
            total_chunks = int(total_chunks)

            if item_id not in items:
                items[item_id] = {
                    "total_chunks": total_chunks,
                    "chunks": {}
                }

            # we don't "add" to the payload, it's a new chunk
            items[item_id]["chunks"][chunk_id] = payload

            # Rcvd all frames -> Reconstruct
            if len(items[item_id]["chunks"]) == items[item_id]["total_chunks"]:
                message = "".join(items[item_id]["chunks"][i]
                    for i in range(total_chunks)
                )

                print(f"[{address}]: {message}")

    communication_socket.close()
    print(f"Connection with {address} ended")

def main():
    listening_socket = start()

    while True:
        communication_socket, address = listening_socket.accept()
        thread = threading.Thread(target = handle_client, args = (communication_socket, address))
        thread.start()
        print(f"Active Connections: {threading.active_count() - 1}")

main()
