import socket
import threading
import requests
import os
from flask import Flask, request, send_file

# Peer Configuration
DISCOVERY_SERVER = "127.0.0.1"  # Change this if running on another machine
DISCOVERY_PORT = 5000
PEER_PORT = 8001  # Change for different peers

# Folder to store shared files
FILES_DIR = "shared_files"
os.makedirs(FILES_DIR, exist_ok=True)

app = Flask(__name__)

# ========== PEER DISCOVERY FUNCTIONS ==========
def register_peer():
    """Registers this peer with the discovery server"""
    peer_address = f"127.0.0.1:{PEER_PORT}"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((DISCOVERY_SERVER, DISCOVERY_PORT))
        s.send(f"REGISTER {peer_address}".encode())
        response = s.recv(1024).decode()
        print(f"Discovery Server Response: {response}")
        s.close()
    except:
        print("Failed to connect to discovery server.")

def get_peer_list():
    """Fetches the list of active peers from the discovery server"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((DISCOVERY_SERVER, DISCOVERY_PORT))
        s.send(b"GET_PEERS")
        peers = s.recv(4096).decode()
        s.close()
        return eval(peers) if peers else []
    except:
        print("Failed to retrieve peer list.")
        return []

# ========== FILE SHARING API ==========
@app.route('/files', methods=['GET'])
def list_files():
    """Lists all available files"""
    files = os.listdir(FILES_DIR)
    return {"files": files}

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file uploads"""
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400
    file = request.files['file']
    file.save(os.path.join(FILES_DIR, file.filename))
    return {"message": f"File '{file.filename}' uploaded successfully"}

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Allows downloading files"""
    file_path = os.path.join(FILES_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return {"error": "File not found"}, 404

# ========== CLIENT-SIDE FUNCTIONS ==========
def request_file_from_peer(peer, filename):
    """Requests a file from another peer"""
    url = f"http://{peer}/download/{filename}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(FILES_DIR, filename), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded '{filename}' from {peer}")
        else:
            print(f"Failed to download '{filename}' from {peer}: {response.json()}")
    except:
        print(f"Could not connect to peer {peer}")

def main():
    """Runs the peer"""
    register_peer()

    while True:
        print("\nOptions:")
        print("1. View available files")
        print("2. Upload a file")
        print("3. Download a file from another peer")
        print("4. View list of peers")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            print("Files:", os.listdir(FILES_DIR))

        elif choice == "2":
            file_path = input("Enter file path to upload: ").strip()
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                os.rename(file_path, os.path.join(FILES_DIR, file_name))
                print(f"Uploaded '{file_name}' to local peer storage.")
            else:
                print("Invalid file path!")

        elif choice == "3":
            peers = get_peer_list()
            print("Available peers:", peers)
            if not peers:
                print("No peers available.")
                continue

            peer = input("Enter peer address (IP:PORT): ").strip()
            filename = input("Enter filename to download: ").strip()
            request_file_from_peer(peer, filename)

        elif choice == "4":
            print("Active Peers:", get_peer_list())

        elif choice == "5":
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PEER_PORT)).start()
    main()
