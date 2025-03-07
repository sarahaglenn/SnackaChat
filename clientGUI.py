import socket
from threading import Thread
from dotenv import load_dotenv
import os
import tkinter
from tkinter import *

load_dotenv()

HOST = os.getenv("HOST")
PORT = 5590

# Create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client.connect((HOST, PORT))
print("Connected to the server!")

def receive_messages(client):
    """ Continuously listen for messages """
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if not msg:
                break
            msg_list.insert(tkinter.END, msg)
        except:
            break
    print("Disconnected from the server.")
    client.close()

def send_messages():
    """Continuously take user input and send to server"""
    while True:
        msg = my_msg.get()
        my_msg.set("")
        if msg.lower() == "quit":
            client.send(msg.encode("utf-8"))
            break
        client.send(msg.encode("utf-8"))
    root.quit()

def submit_name():
    """Send the username to the server"""
    global name_window
    name = name_var.get()
    if name:
        client.send(name.encode("utf-8"))
        name_window.destroy()
        start_chat()

def start_chat():
    Thread(target=receive_messages, args=(client,), daemon=True).start()
    root.deiconify()

    # try:
    #     name = Entry(root, "Please enter your name: ")
    #     name.pack()
    #     client.send(name.encode("utf-8"))

    #     send_messages(client)
    # except:
    #     print("Server is disconnected.")
    # finally:
    #     client.close()


root = Tk()
root.title("Snacka Chat")
root.configure(bg="pink")
root.withdraw()

message_frame = Frame(root, height=100, width=100, bg='white')
message_frame.pack()

my_msg = StringVar()
msg_input = Entry(root, textvariable=my_msg, width=50)
msg_input.pack()

msg_list = Listbox(message_frame, height=15, width=100, bg='white')
msg_list.pack()

send_button = Button(root, text='Send', font="Arial", fg="black", bg="red", command=send_messages)
send_button.pack()

name_window = Toplevel(root)
name_window.title("Entering the chat")

Label(name_window, text="Please enter your name: ").pack()

name_var = StringVar()
name_entry = Entry(name_window, textvariable=name_var, width=30)
name_entry.pack()

name_button = Button(name_window, text="Submit", command=submit_name)
name_button.pack()

root.mainloop()
