import socket
from threading import Thread
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")
PORT = 5588

def receive_messages(client):
    """ Continuously listen for messages """
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if not msg:
                break
            print(msg)
        except:
            break
    print("Disconnected from the server.")
    client.close()

def send_messages(client):
    """Continuously take user input and send to server"""
    while True:
        msg = input()
        if msg.lower() == "quit":
            client.send(msg.encode("utf-8"))
            break
        client.send(msg.encode("utf-8"))
    client.close()

def main():
    # Create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Connected to the server!")
        name = input("Please enter your name: ")
        client.send(name.encode("utf-8"))

        Thread(target=receive_messages, args=(client,), daemon=True).start()
        send_messages(client)
    except:
        print("Server is disconnected.")
    finally:
        client.close()

if __name__ == "__main__":
    main()