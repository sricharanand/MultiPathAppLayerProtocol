import socket
import threading #To handle multiple connections

HOST = "0.0.0.0" # Listening on all network interfaces
PORT = 9999

# Global session state:
# session_id -> items dictionary
# Shared across multiple TCP connections belonging to the same logical session

sessions = dict()

def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    return server_socket

def recv_line(sock):
    """
    Read from TCP socket until a newline-delimited application frame is received.
    TCP provides a byte stream, so explicit framing is required at the application layer.
    """
    buffer = b""
    while b"\n" not in buffer:
        data = sock.recv(8)
        if not data:
            return None
        buffer += data
    line, _ = buffer.split(b"\n", 1)
    return line.decode("utf-8")

def handle_client(communication_socket, address, session_id):
    """
    Handle data-plane communication for a single TCP connection.
    All connections with the same session_id share reconstruction state.
    """
    items = sessions[session_id]

    byteBuffer = b""

    while True:
        fragment = communication_socket.recv(8)
        if not fragment:
            break

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

            items[item_id]["chunks"][chunk_id] = payload

            # Rcvd all frames -> Reconstruct
            if len(items[item_id]["chunks"]) == items[item_id]["total_chunks"]:
                message = "".join(items[item_id]["chunks"][i]
                    for i in range(total_chunks)
                )

                print(f"[{address}]: {message}")
                sessions[session_id] = items

    communication_socket.close()
    print(f"Connection with {address} ended")

def main():
    listening_socket = start()

    new_session_id = 0

    while True:
        communication_socket, address = listening_socket.accept()

        # Control-plane handshake
        line = recv_line(communication_socket)
        cmd, value = line.split("|", 1)

        if value == "NEW":
            session_id = new_session_id
            sessions[session_id] = {}
            communication_socket.sendall(
                f"SESSION|{session_id}\n".encode("utf-8")
            )
            new_session_id += 1
        else:
            session_id = int(value)

        # Ensure session identity in the state by sending it in the function
        thread = threading.Thread(
            target = handle_client,
            args = (communication_socket, address, session_id)
        )
        thread.start()

        print(f"Connection with {address} started")
        print(f"Active Connections: {threading.active_count() - 1}")
main()
