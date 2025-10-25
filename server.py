#!/usr/bin/env python3
"""
Simple Echo Chat Room Server
Handles multiple clients and broadcasts messages to all connected users
"""

import socket
import threading
import sys

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8888       # Port to listen on

# Store all connected clients
clients = []
clients_lock = threading.Lock()


def broadcast(message, sender_socket=None):
    """
    Send message to all connected clients except the sender
    
    Args:
        message: The message to broadcast
        sender_socket: Socket of the sender (to exclude from broadcast)
    """
    with clients_lock:
        for client_socket, client_address, client_name in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    # Remove client if sending fails
                    remove_client(client_socket)


def remove_client(client_socket):
    """
    Remove a client from the clients list
    
    Args:
        client_socket: Socket of the client to remove
    """
    with clients_lock:
        for client in clients:
            if client[0] == client_socket:
                clients.remove(client)
                break


def handle_client(client_socket, client_address):
    """
    Handle communication with a single client
    
    Args:
        client_socket: Socket object for the client
        client_address: Address tuple (ip, port) of the client
    """
    print(f"[NEW CONNECTION] {client_address} connected")
    
    # Get client username
    try:
        client_socket.send("Enter your username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        if not username:
            username = f"User_{client_address[1]}"
        
        # Add client to the list
        with clients_lock:
            clients.append((client_socket, client_address, username))
        
        # Notify all clients about the new user
        join_message = f"[SYSTEM] {username} joined the chat room!"
        print(join_message)
        broadcast(join_message, client_socket)
        
        # Send welcome message to the new user
        welcome_msg = f"[SYSTEM] Welcome to the chat room! Online users: {len(clients)}"
        client_socket.send(welcome_msg.encode('utf-8'))
        
        # Handle messages from this client
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                break
            
            # Format and broadcast the message
            formatted_message = f"[{username}] {message}"
            print(formatted_message)
            broadcast(formatted_message, client_socket)
            
    except Exception as e:
        print(f"[ERROR] {client_address}: {e}")
    
    finally:
        # Client disconnected
        remove_client(client_socket)
        leave_message = f"[SYSTEM] {username} left the chat room."
        print(leave_message)
        broadcast(leave_message)
        client_socket.close()
        print(f"[DISCONNECTED] {client_address} disconnected")


def start_server():
    """
    Start the chat room server
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[STARTING] Server is starting on {HOST}:{PORT}")
        print(f"[LISTENING] Server is listening for connections...")
        print(f"[INFO] Press Ctrl+C to stop the server\n")
        
        while True:
            # Accept new client connection
            client_socket, client_address = server_socket.accept()
            
            # Create a new thread to handle the client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
            
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN] Server is shutting down...")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    finally:
        server_socket.close()
        print("[STOPPED] Server stopped")


if __name__ == "__main__":
    start_server()

