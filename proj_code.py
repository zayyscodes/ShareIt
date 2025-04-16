from tkinter import *
from tkinter import filedialog, simpledialog
import socket
import os
import threading
import requests
from flask import Flask, request, send_file
import random

# ========= CONFIG ==========
DISCOVERY_SERVER = "127.0.0.1"
DISCOVERY_PORT = 5000
PEER_PORT = random.randint(8001, 8999)

FILES_DIR = "shared_files"
os.makedirs(FILES_DIR, exist_ok=True)

DOWNLOAD_DIR = "downloaded"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Flask(__name__)

# ========== FLASK PEER ENDPOINTS ==========
@app.route('/files', methods=['GET'])
def list_files():
    return {"files": os.listdir(FILES_DIR)}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400
    file = request.files['file']
    file.save(os.path.join(FILES_DIR, file.filename))
    return {"message": f"File '{file.filename}' uploaded successfully"}

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(FILES_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return {"error": "File not found"}, 404

# ========== NETWORKING LOGIC ==========
def start_flask_server():
    app.run(host='0.0.0.0', port=PEER_PORT)

def request_file_from_peer(peer, filename):
    url = f"http://{peer}/download/{filename}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(DOWNLOAD_DIR, filename), 'wb') as f:
                f.write(response.content)
            log_message(f"[DOWNLOADED] '{filename}' from {peer} to '{DOWNLOAD_DIR}' folder")
        else:
            log_message(f"[ERROR] Failed to download '{filename}': {response.json()}")
    except Exception:
        log_message(f"[ERROR] Could not connect to peer {peer}")

def register_peer():
    peer_address = f"127.0.0.1:{PEER_PORT}"
    try:
        log_message(f"[DEBUG] Registering peer: {peer_address}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((DISCOVERY_SERVER, DISCOVERY_PORT))
        s.send(f"REGISTER {peer_address}".encode())
        response = s.recv(1024).decode()
        log_message(f"[SUCCESS] Registered with discovery server")
        s.close()
    except Exception as e:
        log_message(f"[ERROR] Could not connect to discovery server.\nReason: {e}")

def get_peer_list():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((DISCOVERY_SERVER, DISCOVERY_PORT))
        s.send(b"GET_PEERS")
        peers = s.recv(4096).decode()
        s.close()
        peers = eval(peers) if peers else []

        # Filter out the current peer itself
        self_address = f"127.0.0.1:{PEER_PORT}"
        peers = [peer for peer in peers if peer != self_address]

        # Validate active peers
        valid_peers = []
        for peer in peers:
            try:
                response = requests.get(f"http://{peer}/files", timeout=2)
                if response.status_code == 200:
                    valid_peers.append(peer)
            except:
                continue  # skip unreachable peer

        if valid_peers:
            log_message("[RETRIEVED] Active Peers:\n" + "\n".join(valid_peers))
        else:
            log_message("[INFO] No active peers found.")
        return valid_peers

    except Exception as e:
        log_message(f"[ERROR] Failed to retrieve peer list.\nReason: {e}")
        return []

# ========== FILE ACTIONS ==========
def upload_files():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        dest = os.path.join(FILES_DIR, file_name)
        os.rename(file_path, dest)
        log_message(f"[UPLOADED] {file_name}")

def download_file_gui():
    peers = get_peer_list()
    if not peers:
        return
    all_files = {}

    for peer in peers:
        try:
            response = requests.get(f"http://{peer}/files")
            if response.status_code == 200:
                files = response.json().get("files", [])
                all_files[peer] = files
        except Exception:
            continue

    options = []
    for peer, files in all_files.items():
        for file in files:
            options.append(f"{file} from {peer}")

    if not options:
        log_message("[NOT FOUND] No files found on peers.")
        return

    selected = simpledialog.askstring("Download", "Select file:\n" + "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options)))
    if not selected:
        return
    try:
        index = int(selected.split('.')[0]) - 1
        peer_info = options[index]
        filename, _, peer = peer_info.partition(" from ")
        request_file_from_peer(peer, filename.strip())
    except Exception as e:
        log_message("[ERROR] Invalid selection.")

def show_local_files():
    files = os.listdir(FILES_DIR)
    if files:
        log_message("[SUCCESS] Files:\n" + "\n".join(files))
    else:
        log_message("[NOT AVAILABLE] No files available.")

# ========== LOGGING ==========
def log_message(msg):
    output_box.config(state=NORMAL)
    output_box.insert(END, msg + '\n\n')
    output_box.config(state=DISABLED)
    output_box.see(END)

def start_network():
    threading.Thread(target=start_flask_server, daemon=True).start()
    register_peer()
    log_message("[CLIENT STARTED] Peer server running and registered.")

# ========== GUI ==========

root = Tk()
root.title("ShareIt")
root.geometry("500x650+500+150")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

image_icon = PhotoImage(file="icon.png")
root.iconphoto(False, image_icon)

Label(root, text="P2P FILE TRANSFER", font=('Press Start 2P', 13, 'bold'), bg="#f4fdfe").pack(pady=20)
Frame(root, width=400, height=2, bg='#f3f5f6').pack()

Button(root, text="START NETWORK", width=25, height=2, font=('Roboto', 10, 'bold'), bg="dark turquoise", fg="white", command=start_network).pack(pady=10)
Button(root, text="VIEW LOCAL FILES", width=25, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="white", command=show_local_files).pack(pady=5)
Button(root, text="UPLOAD A FILE", width=25, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="white", command=upload_files).pack(pady=5)
Button(root, text="DOWNLOAD A FILE", width=25, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="white", command=download_file_gui).pack(pady=5)
Button(root, text="VIEW PEERS", width=25, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="white", command=get_peer_list).pack(pady=5)
Button(root, text="EXIT", width=25, height=2, font=('Roboto', 10, 'bold'), bg="tomato", fg="white", command=root.destroy).pack(pady=5)

Label(root, text="LOGS / OUTPUT", font=('Roboto', 12, 'bold'), bg="#f4fdfe").pack(pady=10)

output_box = Text(root, height=12, width=60, font=('Consolas', 10), state=DISABLED, bg="#fff")
output_box.pack(pady=5)

root.mainloop()
