# WebSocket From Scratch — Implementing the WebSocket Protocol with Python

## Project Overview

WebSocket From Scratch is a systems programming project that implements a WebSocket communication system from the ground up in Python without relying on external WebSocket libraries. The project focuses on understanding the WebSocket protocol at a low level, including TCP socket communication, HTTP upgrade mechanisms, the WebSocket handshake, WebSocket frame construction and parsing, masking and unmasking operations, message parsing, and bidirectional client-server communication. The implementation uses only Python's standard library modules including socket, hashlib, base64, os, threading, and unittest.

## Problem Context

WebSocket is commonly used through high-level libraries that hide the underlying networking and protocol mechanisms. While these libraries make development easier, they can make it difficult to understand what actually happens when a WebSocket connection is established and how messages are transmitted between a client and server. This project was created to address this gap by providing a hands-on implementation that reveals the protocol internals and enables a deeper understanding of network communication.

## Primary Objectives

The main objectives were to understand how WebSockets work internally, implement the WebSocket handshake, work directly with TCP sockets, implement WebSocket frame encoding and decoding, handle payload lengths, implement masking and unmasking, handle WebSocket opcodes, manage connection establishment and termination, build a reusable socket abstraction, separate protocol logic from networking logic, build a WebSocket client and server, and write comprehensive tests for the implementation. A major objective was to avoid high-level WebSocket libraries and understand the protocol directly using Python's standard library.

## System Architecture

### Layered Architecture

The project is organized into several distinct layers that separate concerns and make the implementation easier to understand and maintain. At the highest level, the application layer contains client and server implementations that use the WebSocket protocol. Below this, the WebSocket protocol layer handles handshake validation, frame encoding and decoding, and message management. The socket layer provides low-level TCP communication with connection management, byte handling, and read-write operations.

The source code is separated into dedicated packages including core for socket abstractions and adapters, protocol for handshake, frame, and WebSocket logic, exceptions for custom error handling, and utils for helper functions. This separation makes the project easier to understand and maintain, with each component having a clear responsibility.

### WebSocket Handshake

The connection begins with an HTTP upgrade request from the client containing the Sec-WebSocket-Key header. The server processes this request, validates the handshake, generates the appropriate acceptance key using SHA-1 hashing and Base64 encoding, and responds with HTTP 101 Switching Protocols and the Sec-WebSocket-Accept header. Once the handshake is complete, the WebSocket connection is established and bidirectional communication can begin. The handshake layer is implemented independently in the protocol/handshake.py module.

### Frame Architecture

After the handshake, communication happens through WebSocket frames with a specific binary structure. Each frame contains a FIN bit indicating whether this is the final fragment, an opcode specifying the frame type, a MASK bit indicating whether the payload is masked, a payload length field with support for extended lengths, an optional masking key, and the payload data. The project implements the frame layer separately in protocol/frame.py, handling all aspects of frame construction and parsing.

### Client and Server

The repository contains executable examples for both the client and server sides. The server example provides a complete runnable server implementation that can accept WebSocket connections, receive messages, and send responses. The client provides the corresponding client-side interaction, demonstrating how to initiate connections and exchange messages with the server.

## Technology Stack

### Programming Language
Python serves as the programming language, providing the standard library modules needed for networking, cryptography, and testing.

### Networking
TCP sockets provide the underlying transport mechanism, with Python's socket module enabling client-server networking, connection management, and bidirectional communication.

### Web Protocol
The WebSocket protocol handles HTTP upgrade mechanisms, the WebSocket handshake process, frame construction and parsing, opcode handling, payload processing, and masking and unmasking operations.

### Cryptography and Encoding
SHA-1 hashing generates handshake acceptance keys, Base64 encoding transforms binary data for the handshake, and random masking keys ensure client-to-server masking.

### Concurrency
Python threading enables concurrent connection handling, allowing the server to manage multiple clients simultaneously.

### Testing
The unittest module provides automated testing capabilities for validating the protocol implementation.

### Dependencies
The implementation deliberately avoids external dependencies, with everything implemented using the Python standard library as confirmed by the requirements file.

## Model Implementation

No machine-learning model is used in this project. This is a low-level networking and systems project focused on implementing the communication protocol itself rather than using an existing WebSocket framework. The project can be described as protocol engineering and systems programming rather than an AI or machine-learning project.

## Data Flow

No dataset is required for this project. The project operates on network messages rather than a machine-learning dataset. The main data flowing through the system consists of client messages that are encoded into WebSocket frames, transmitted over TCP connections to the server, decoded back into frames, and delivered as application messages. This data flow demonstrates the complete lifecycle of WebSocket communication.

## Implementation Responsibilities

As the Backend and Systems Engineer for this project, responsibilities included designing the project architecture, implementing low-level TCP socket communication, implementing the WebSocket handshake, implementing HTTP upgrade handling, implementing WebSocket frame construction, implementing frame parsing, handling payload lengths, implementing masking and unmasking, handling WebSocket opcodes, implementing connection management, designing reusable socket abstractions, building client and server examples, creating automated tests, and structuring the project into independent protocol and networking modules. The repository contains dedicated implementations for the socket and core layer, handshake, frames, WebSocket logic, utilities, and tests.

## Project Results

The project successfully produced a functional WebSocket implementation built without an external WebSocket package. Main achievements include implementing a WebSocket server that can accept and manage connections, implementing a WebSocket client that can initiate and maintain connections, implementing the complete WebSocket handshake process, implementing WebSocket frame processing with proper encoding and decoding, implementing masking and unmasking operations as required by the protocol, implementing payload processing for various length formats, implementing protocol-level message handling, building reusable networking abstractions for socket management, adding client and server examples for demonstration, adding unit tests for reliability verification, and maintaining zero external runtime dependencies. The repository currently contains the src directory with the complete implementation, examples directory with runnable code, tests directory with automated tests, and requirements.txt confirming the use of standard library only.

## Key Challenges

### Understanding the WebSocket Handshake
The first challenge was understanding how WebSocket starts on top of HTTP. The server must correctly process the client's upgrade request and generate the appropriate WebSocket acceptance response. This requires proper validation of the Upgrade and Connection headers, extraction and processing of the Sec-WebSocket-Key, generation of the correct acceptance key using SHA-1 and Base64, and returning HTTP 101 Switching Protocols to establish the WebSocket connection.

### Working with Raw TCP Sockets
Instead of using a WebSocket abstraction, the project works directly with sockets. This means explicitly dealing with connections, bytes, buffers, reads, writes, and connection termination. Working at this level provides a much deeper understanding of network communication compared to using high-level libraries.

### Binary Frame Parsing
WebSocket frames are binary structures rather than simple strings. The implementation must correctly interpret the FIN bit, opcode, MASK bit, payload length, extended payload lengths, masking key, and payload. A small mistake in byte offsets can corrupt the entire message, requiring careful attention to the binary format specification.

### Masking Implementation
WebSocket clients mask transmitted payloads using a masking key. The implementation must apply the unmasking algorithm to recover the original payload from the encoded payload and masking key. Understanding and implementing this byte-level operation was one of the more interesting and challenging parts of the project.

### Protocol versus Application Logic
Another challenge was keeping the implementation modular and well-separated. Instead of putting everything into one server file, the project separates socket handling, handshake logic, frame processing, WebSocket management, and application logic. This separation makes the implementation easier to test, debug, and extend with new features.

## Lessons Learned

### High-Level Libraries Hide Engineering Complexity
Using libraries such as ws or Socket.IO makes development much faster, but they hide the protocol internals. Building the protocol yourself exposes the real complexity and makes those abstractions much easier to understand. This understanding is valuable for debugging and optimizing applications that use WebSocket libraries.

### Protocols Are Fundamentally About Bytes
At the application level, developers think about strings and messages. At the networking level, the system actually handles bytes, bits, headers, and payload. Understanding this distinction is extremely valuable for backend and systems engineering, enabling better debugging and optimization of network communications.

### Separation of Concerns Matters
The project demonstrates a clean separation between networking, protocol, and application concerns. This makes low-level systems easier to debug and extend, as each layer has a clear responsibility and can be modified independently without affecting other layers.

### Standards Should Be Understood, Not Only Consumed
Instead of simply calling websocket.send, the project explores what happens underneath that abstraction. That mindset is transferable to many technologies including HTTP, TCP, WebSocket, TLS, databases, LLMs, and Transformers. Understanding the underlying mechanisms enables better design and debugging.

### Building from Scratch Exposes Real Complexity
The project reinforced an important engineering principle: if you can build a simplified version yourself, you understand the abstraction much better when you eventually use the production library. This hands-on approach to learning is more effective than simply reading documentation.

## Engineering Philosophy — Building from Scratch

A recurring theme across my projects is the commitment to building things from scratch to understand how they actually work internally. Rather than only using existing abstractions, I intentionally recreate simplified versions of fundamental technologies. Examples include WebSocket implemented from TCP sockets, Transformers and GPT with attention and embedding implementations, BPE tokenizer logic implementation, LLM agents with state, tools, routing, memory, and agent workflows, and the complete data pipeline for the AIoT platform from wearable devices through streaming, machine learning, and agents.

This is an important part of my engineering approach: I don't want to only know how to use a technology, I want to understand what is happening underneath it. This approach helps me understand abstractions at a deeper level, debug systems more effectively, and design better architectures. Understanding the underlying mechanisms enables better decision-making when using high-level libraries and frameworks.

## GitHub Repository

The project repository is available at [https://github.com/Mohamedaminesaadd/web-socket-from-scratch](https://github.com/Mohamedaminesaadd/web-socket-from-scratch?utm_source=chatgpt.com). The repository currently contains the complete protocol implementation with core socket abstractions, handshake processing, frame construction and parsing, WebSocket logic, utilities, client and server examples demonstrating the implementation in action, and automated tests for validating the protocol implementation. This comprehensive implementation serves as a reference for understanding WebSocket protocol internals and systems programming with Python.