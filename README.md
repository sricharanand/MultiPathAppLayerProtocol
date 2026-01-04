# Networks Playground

This repository is a small experimental playground for understanding application-layer networking concepts using Python sockets.

# What This Explores

- TCP as a byte stream (not message-based)

- Client–server communication using Python sockets

- Message framing using delimiters (\n)

- Fragmentation and partial recv() behavior

- Application-layer buffering and message reconstruction

- Basic protocol design decisions (when to send, when to close)

# Current State

- Single client ↔ single server (TCP)

- Messages are sent as a stream and reconstructed on the server

- Server processes complete messages while handling partial reads

- Simple request → response → close protocol

# Why this Exists

- This project is intentionally minimal and experimental.
The goal is to build intuition about how real networked systems behave, rather than to provide a production-ready implementation.

# Next Steps (planned)

- Clean protocol finalization

- Multiple message handling

- Multi-client support

- Simulated delay / loss