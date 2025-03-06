import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 5588

# dictionary to store client information
clients = {}
# Global flag to control server shutdown
server_running = True


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

    while server_running:
        try:
            msg = conn.recv(1024).decode("utf-8")
            if not msg or msg.lower() == "quit":
                break
            print (f"{name}: {msg}")
            broadcast(f"{name}: {msg}", conn)
        except:
            break

    print(f"{name} has left the chat.")
    conn.close()
    del clients[conn]
    broadcast(f"{name} has left the chat.")

def send_server_message():
    global server_running
    while server_running:
        msg = input()
        if msg.lower() == "quit":
            print("Server shutting down...")
            broadcast("Server is shutting down... ", "Server: ")
            server_running = False

            # Close all client connections
            for client in list(clients.keys()):
                try:
                    client.close()
                except:
                    pass
            break
        broadcast(msg, "Server: ")

def broadcast(msg, sender=None):
    # create correct formatting if it is a server message
    if sender == "Server: ":
        msg = sender + msg
    # collected disconnected clients to remove
    disconnected_clients = []

    # send message to all clients except the sender
    for client in clients:
        try:
            if client != sender:
                client.send(msg.encode("utf-8"))
        except:
            disconnected_clients.append(client)
    # Remove the disconnected clients from the dictionary
    for client in disconnected_clients:
        del clients[client]

def start_server():
    global server_running
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

        while server_running:
            try:
                """allows accept to wait up to 1 second for new client connections.
                If there is none, it throws timeout exception and server_running is
                checked again
                """
                server.settimeout(1.0)
                conn, addr = server.accept()
                Thread(target=handle_clients, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue
    print("Server has shut down.")

if __name__ == "__main__":
    start_server()