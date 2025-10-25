# Echo_Simple_ChatRoom

A very simple TCP echo practice project. This is a basic chat room application that allows multiple users to communicate in real-time through terminal interface using TCP protocol.

## 📋 What is This?

This is a simple implementation of TCP echo server/client for learning network programming. It consists of:
- **Server (`server.py`)**: Accepts multiple client connections and broadcasts messages
- **Client (`client.py`)**: Connects to server and allows chatting

**Current Status**: Only supports **local connections** (localhost/127.0.0.1)

## 📦 Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## 🚀 How to Use

### Step 1: Start the Server

Open a terminal and run:
```bash
python server.py
```

You will see: `[LISTENING] Server is listening for connections...`

### Step 2: Start Client(s)

Open **another terminal** (keep server running) and run:
```bash
python client.py
```

### Step 3: Enter Username

When prompted, enter your username (e.g., `Alice`)

### Step 4: Start Chatting!

Now you can type messages after the `>` prompt and press Enter to send.


## 💻 Basic Commands

- **Type message** → Press Enter to send
- **`/quit`** → Disconnect from server
- **Ctrl+C** → Stop the server


## 🔧 How It Works

**Server:** Creates TCP socket → Accepts connections → Broadcasts messages to all clients

**Client:** Connects to server → Sends/receives messages in real-time



## ⚠️ Limitations

- **Local only**: Currently only supports localhost connections
- No encryption (plain text communication)
- No authentication
- No message history
