from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket
import os
import threading
import requests
from flask import Flask, request, send_file

PEERS = []

DISCOVERY_SERVER = "127.0.0.1"  # Change this if running on another machine
DISCOVERY_PORT = 5000
PEER_PORT = 8001  # Change for different peers

root=Tk()
root.title("ShareIt")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

def select_file():
    print()

def sender():
    print()

def server():
    print()
    client()

# CLIENT FUNCTION
def register_peer():
    #   Registers this peer with the discovery server
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

def client():

    register_peer()

    # CLIENT WINDOW GUI
    main=Toplevel(root)
    main.title("Client")
    main.geometry('450x560+500+200')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)
    image_icon=PhotoImage(file="images/receive.png")
    main.iconphoto(False, image_icon)
    Label(main, text="OPTIONS", font=('Press Start 2P', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
    Frame(main, width=400, height=2, bg='#f3f5f6').place(x=25, y=80)
    Button(main, text="VIEW AVALAIBLE FILES", width=30, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="#fff", command=select_file).place(x=110, y=70)
    Button(main, text="UPLOAD A FILE", width=30, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="#fff", command=select_file).place(x=110, y=120)
    Button(main, text="DOWNLOAD A FILE", width=30, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="#fff", command=select_file).place(x=110, y=170)
    Button(main, text="VIEW LIST OF PEERS", width=30, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="#fff", command=select_file).place(x=110, y=220)
    Button(main, text="EXIT", width=30, height=2, font=('Roboto', 10, 'bold'), bg="blue violet", fg="#fff", command=select_file).place(x=110, y=270)



    main.mainloop()

#icon
image_icon=PhotoImage(file="images/icon.png")
root.iconphoto(False, image_icon)

Label(root, text="P2P FILE TRANSFER", font=('Press Start 2P', 15, 'bold'), bg="#f4fdfe").place(x=50, y=30)
Frame(root, width=400, height=2, bg='#f3f5f6').place(x=25, y=80)

Button(root, text="START", width=10, height=2, font=('Press Start 2P', 10, 'bold'), bg="dark turquoise", fg="#fff", command=server).place(x=150, y=70)

background=PhotoImage(file="images/background.png")
Label(root, image=background).place(x=-2, y=323)





root.mainloop()