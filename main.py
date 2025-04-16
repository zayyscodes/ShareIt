from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket
import os
import threading
import requests
from flask import Flask, request, send_file

PEERS = []

root=Tk()
root.title("ShareIt")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

def select_file():
    print()

def sender():
    print()

def Send():
    window=Toplevel(root)
    window.title("Send File")
    window.geometry('450x560+500+200')
    window.configure(bg='#f4fdfe')
    window.resizable(False, False)
    image_icon=PhotoImage(file="images/send.png")
    window.iconphoto(False, image_icon)

    Sbackground=PhotoImage(file='images/sender.png')
    Label(window, image=Sbackground).place(x=-2, y=0)

    Mbackground=PhotoImage(file='images/id.png')
    Label(window, image=Mbackground, bg='#f4fdfe').place(x=100, y=260)

    host = socket.gethostname()
    Label(window, text=f"ID: {host}", bg='white', fg='black').place(x=140, y=290)

    Button(window, text="+ select file", width=10, height=1, font="arial 14 bold", bg="#fff", fg="#000", command=select_file).place(x=160, y=150)
    Button(window, text="SEND", width=8, height=1, font='arial 14 bold', bg="#000", fg="#fff", command=sender).place(x=300, y=150)





    window.mainloop()

def Receive():
    main=Toplevel(root)
    main.title("Send File")
    main.geometry('450x560+500+200')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)
    image_icon=PhotoImage(file="images/receive.png")
    main.iconphoto(False, image_icon)

    main.mainloop()

#icon
image_icon=PhotoImage(file="images/icon.png")
root.iconphoto(False, image_icon)

Label(root, text="File Transfer", font=('Press Start 2P', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg='#f3f5f6').place(x=25, y=80)

send_image=PhotoImage(file="images/send.png")
send = Button(root, image=send_image, bg="#f4fdfe", bd=0, command=Send)
send.place(x=50, y=100)

recv_image=PhotoImage(file="images/receive.png")
recv = Button(root, image=recv_image, bg="#f4fdfe", bd=0, command=Receive)
recv.place(x=300, y=100)

#label
Label(root, text="Send", font=('Press Start 2P', 12, 'bold'), bg="#f4fdfe").place(x=60, y=200)
Label(root, text="Receive", font=('Press Start 2P', 12, 'bold'), bg="#f4fdfe").place(x=290, y=200)

background=PhotoImage(file="images/background.png")
Label(root, image=background).place(x=-2, y=323)





root.mainloop()