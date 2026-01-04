import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname())

PORT = 9999

serverSocket.bind((HOST, PORT))

serverSocket.listen()

while True:
    communication_socket, address = serverSocket.accept()
    print(f"Connected to {address}")

    # Change it up, gonna introduce fragmenting
    # Just having a small buffer size (like 8) will just send the first 8 bytes and call it.

    # We need to have this in place:-
    # TCP sends bytes
    # APPLICATION accumulates them
    # Application protocol decides when the message is complete
    # Then process
    # So, need a Receive Loop + Application buffer

    # While Connected:
    #   Recv Fragment
    #   Append to buffer
    #   While buffer contains '\n':
    #       Extract ONE message (upto the \n)
    #       Leave remainder in the buffer

    #You never throw away bytes
    #You never assume alignment
    #You never stop at first message

    applicationBuffer = ""
    fragment = ""

    while True:
        fragment = communication_socket.recv(8).decode('utf-8')

        # Termination condition
        # TCP signals - FIN received
        if not fragment:
            break

        applicationBuffer += fragment

        if '\n' in applicationBuffer:
            message = applicationBuffer.split('\n') # Array. Elements separated by \n.
            applicationBuffer = message[1] # Keep everything after the first delimiter
            # This is a bit inaccurate, could be more than 2 \n, but leave it for now.

    communication_socket.send(f"Got your message. Thank you!".encode('utf-8'))
    communication_socket.close()

    print(f"Connection with {address} ended")

    break


    # IRL - The messages are length prefix - <length><Message> -> Read 'length' bytes and process
