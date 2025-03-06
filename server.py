import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 5588

# dictionary to store client information
clients = {}


def handle_clients(conn, addr):
    # get client name and add them to dictionary
    name = conn.recv(1024).decode("utf-8")
    clients[conn] = name
    print(f"{name} has connected from {addr}")

    # send new client a welcome message
    welcome_msg = f"Welcome to the chat {name}"
    conn.send(welcome_msg.encode("utf-8"))

    # Create message to tell all users that the client has joined
    join_msg = f" {name} has joined the chat"
    broadcast(join_msg, conn)

    while True:
        try:
            msg = conn.recv(1024).decode("utf-8")
            if not msg or msg.lower() == "quit":
                break
            else:
                print (f"{name}: {msg}")
                broadcast(f"{name}: {msg}", conn)
        except:
            break

    print(f"{name} has left the chat.")
    conn.close()
    del clients[conn]
    broadcast(f"{name} has left the chat.")

def send_server_message():
    while True:
        msg = input()
        if msg.lower() == "quit":
            print("Server shutting down...")
            broadcast("Server is shutting down... ", "Server: ")
            break
        broadcast(msg, "Server: ")

def broadcast(msg, sender=None):
    if sender == "Server: ":
        msg = sender + msg
    # send message to all clients except the sender
    for client in clients:
        try:
            if client != sender:
                client.send(msg.encode("utf-8"))
        except:
            client.close()
            del clients[client]

def start_server():
    # create socket object
    # because of with , no need to call close()
    # Constants passed: AF_INET is internet address family for IPv4, SOCK_STREAM is socket type for TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # set configuration so that many clients can request on one port.
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind method associates the socket with specific network interface and port num
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started on port {PORT}")

        Thread(target=send_server_message, daemon=True).start()

        while True:
            conn, addr = server.accept()
            Thread(target=handle_clients, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()