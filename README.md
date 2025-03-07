# 💬 Snacka Chat App

The purpose of this project was the learn about network communication. I explored sending data over a TCP connection using the Python socket library to create a real-time chat application. The app allows multiple users to connect to a server and participate in a multi-way conversation. I also implemented multithreading to both the clients and the server to send and receive messages simultaneously.

## 🚀 How to Use
1️⃣ **Set up the environment**
  - Create a .env file in the server and client(s) environments with the server IP address as HOST.
  - Install dependencies using requirements.txt

2️⃣ **Start the Server**
  - Run the server script. Once started, it listens for incoming client connections

3️⃣ **Connect Clients**
  - Run the client script on any machine and connect to the chat.
  - The server broadcasts messages to/from all clients

The server also notifies users when someone joins or leaves the chat.

## 🎥 [Software Demo Video](http://youtube.link.goes.here)

# 🌎 Network Communication

✅ Architecture: Client/Server  
✅ Protocol: TCP  
✅ Port: 5588  
✅ Message Format: UTF-8 encoded strings

The app uses multithreading to allow multiple simultaneous actions, such as:
  * Sending adn receiving messages in real-time
  * Listening for new client connections without blocking other tasks.

# 🛠️ Development Environment

* IDE: Visual Studio Code
* Language: Python 3.12.2
* Libraries:
    * socket
    * threading
    * dotenv

# 🕸️ Useful Websites

* [Python Docs: Socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)
* [Real Python: Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
* [The Simplest Python Chat You Can Build](https://www.youtube.com/watch?v=Ar94t2XhKzM&ab_channel=NeuralNine)
* [Medium: Chat Room Application in Python](https://medium.com/@jkishan421/chat-room-application-in-python-part-i-9193d768dc64)
* [Beej’s Guide to Network Programming](https://beej.us/guide/bgnet/pdf/bgnet_usl_c_1.pdf)

# 🔮 Future Work

  📌 Add GUI to improve the user experience  
  📌 Add formatting to make it clearer which messages are out-going  
  📌 Put code that is common between server and client in a separate module

P.S. 🇸🇪 In Swedish, "snacka" means to chit chat!