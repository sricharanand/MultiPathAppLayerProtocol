# Application-Layer Multipath Routing and Reconstruction Protocol

This project implements a custom application-layer protocol over TCP that enables
session-based multipath data transmission and deterministic reconstruction at the server.

The system demonstrates how multiple concurrent TCP connections can be unified
into a single logical session, allowing data to be split across paths while preserving
correctness at the application layer.

---

## Key Concepts

- **Application-Layer Framing**  
  TCP provides a byte stream without message boundaries. All protocol messages are
  explicitly framed using newline delimiters and reconstructed using byte buffers.

- **Session Establishment (Control Plane)**  
  A server-assigned 'session_id' is negotiated via a lightweight control handshake.
  This allows multiple TCP connections to be associated with the same logical session.

- **Multipath Data Transfer (Data Plane)**  
  Application data is chunked and transmitted across multiple TCP sockets concurrently.
  The server reconstructs messages by unifying state at the session level.

- **State Unification Across Connections**  
  All connections belonging to a session share reconstruction state, enabling correct
  reassembly even when chunks arrive via different paths.

---

## Architecture Overview

### Control Plane
- Client initiates a session using 'SESSION|NEW'
- Server assigns a unique session identifier
- Additional connections attach using the same session ID

### Data Plane
- Messages are split into fixed-size chunks
- Chunks are framed as: [item_id|chunk_id|total_chunks|payload]
- Chunks are routed deterministically across multiple sockets
- Server reconstructs the original message once all chunks arrive

---

## Files

- `server.py` — Session management, framing, and reconstruction logic
- `client.py` — Session handshake, chunking, and multipath transmission

---

## Future Work

Future extensions could include secret sharing, encryption of chunks,
adaptive routing policies, and performance evaluation under failure conditions.

---

## Motivation

This project was developed to explore foundational networking concepts relevant to
resilient and post-quantum communication systems, including session management,
multipath routing, and application-layer protocol design.

  
