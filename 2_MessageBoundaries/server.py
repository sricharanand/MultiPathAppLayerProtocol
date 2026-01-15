import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname())

PORT = 9999

serverSocket.bind((HOST, PORT))

serverSocket.listen()

while True:
    communication_socket, address = serverSocket.accept()
    print(f"Connected to {address}")

    # Just having a small buffer size (like 8) will just send the first 8 bytes and call it.

    # We need to have this in place:-
    # TCP sends bytes
    # APPLICATION accumulates them
    # Application protocol decides when the message is complete
    # Then process (print or store)
    # So, need a Receive Loop + Application buffer

    #You never throw away bytes
    #You never assume alignment
    #You never stop at first message

    applicationBuffer = ""
    fragment = ""
    fragmentCount = 0

    while True:
        fragment = communication_socket.recv(8).decode('utf-8')
        fragmentCount += 1
        print(f"This is fragment number {fragmentCount} of size {len(fragment)} bytes.")

        # Termination condition
        # TCP signals - FIN received
        if not fragment:
            break

        applicationBuffer += fragment

        # Sending multiple messages, extract
        while '\n' in applicationBuffer:
            msg, applicationBuffer = applicationBuffer.split('\n', 1)
            print(f"Received message: {msg}")
            # Array. GET THE REST OF THE STRING (2nd param 1), the rest of the string could have more \n

    communication_socket.send(f"Got your message. Thank you!".encode('utf-8'))
    communication_socket.close()

    print(f"Connection with {address} ended")

    break

    # Usually, bytes are fragmented, not strings.
    # IRL - The messages are length prefix - <length><Message> -> Read 'length' bytes and process
