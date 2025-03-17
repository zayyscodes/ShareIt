import socket
import threading

# Store active peers
PEERS = []

def handle_client(conn, addr):
    """Handles communication with peers"""
    global PEERS
    print(f"New connection from {addr}")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data == "GET_PEERS":
                conn.send(str(PEERS).encode())  # Send list of active peers
            elif data.startswith("REGISTER"):
                peer_address = data.split(" ")[1]
                if peer_address not in PEERS:
                    PEERS.append(peer_address)
                conn.send(b"Registered")
    except:
        pass

    conn.close()

def start_discovery_server(port=5000):
    """Starts the discovery server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Discovery Server Running on Port {port}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_discovery_server()
