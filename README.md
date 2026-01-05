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

- Single client ↔ single server communication over TCP

- Application-layer message framing using delimiter-based parsing

- Correct handling of TCP byte-stream fragmentation and partial reads

- Explicit connection lifecycle management (receive → process → respond → close)

# Why this Exists

- This project is intentionally minimal and experimental.
- The goal is to build intuition about how real networked systems behave, rather than to provide a production-ready implementation.

# Next Steps (planned)

- Formalize protocol semantics (message boundaries, termination rules)

- Extend to persistent connections with multiple message exchanges

- Add multi-client support (concurrent connections)

- Introduce simulated delay and packet loss for resilience testing
