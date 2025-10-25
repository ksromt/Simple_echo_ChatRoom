#!/usr/bin/env python3
"""
Simple Echo Chat Room Client
Connects to the chat server and allows sending/receiving messages
"""

import socket
import threading
import sys

# Server configuration
SERVER_HOST = '127.0.0.1'  # Server address (localhost for testing)
SERVER_PORT = 8888          # Server port


def receive_messages(client_socket):
    """
    Continuously receive and display messages from the server
    
    Args:
        client_socket: Socket connected to the server
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("\n[DISCONNECTED] Connection to server lost")
                break
            print(f"\n{message}")
            print("> ", end="", flush=True)
        except Exception as e:
            print(f"\n[ERROR] {e}")
            break


def send_messages(client_socket):
    """
    Continuously read user input and send to the server
    
    Args:
        client_socket: Socket connected to the server
    """
    while True:
        try:
            message = input("> ")
            
            if not message:
                continue
            
            # Check for quit command
            if message.lower() in ['/quit', '/exit', '/q']:
                print("[INFO] Disconnecting from server...")
                break
            
            client_socket.send(message.encode('utf-8'))
            
        except Exception as e:
            print(f"[ERROR] {e}")
            break


def start_client():
    """
    Start the chat room client and connect to server
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        print(f"[CONNECTING] Connecting to server {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[CONNECTED] Successfully connected to the server!")
        print("[INFO] Type your messages and press Enter to send")
        print("[INFO] Type /quit to disconnect\n")
        
        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Start sending messages (in main thread)
        send_messages(client_socket)
        
    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {SERVER_HOST}:{SERVER_PORT}")
        print("[INFO] Make sure the server is running")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print("[DISCONNECTED] Disconnected from server")


if __name__ == "__main__":
    # Allow custom server address as command line argument
    if len(sys.argv) >= 2:
        SERVER_HOST = sys.argv[1]
    if len(sys.argv) >= 3:
        SERVER_PORT = int(sys.argv[2])
    
    start_client()

