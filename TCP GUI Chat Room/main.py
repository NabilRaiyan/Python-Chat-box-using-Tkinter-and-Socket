import socket
import threading

host = socket.gethostbyname((socket.gethostname()))
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
client_list = []
nickname_list = []


def broadcast(message):
    for client in client_list:
        client.send(message)


def handle(client):
    global nickname_list
    while True:
        try:
            message = client.recv(1024)
            print(f"{nickname_list[client_list.index(client)]}: {message}\n")
            broadcast(message)
        except:
            index = client_list.index(client)
            client_list.remove(client)
            client.close()

            nickname = nickname_list[index]
            nickname_list.remove(nickname)
            break




def receive():
    while True:
        client, address = server.accept()
        print(f"Connnected with {str(address)}!\n")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024)

        client_list.append(client)
        nickname_list.append(nickname)

        print(f"Nickname of the client is {nickname}.\n")
        broadcast(f"Nickname {nickname} join the chat!".encode("utf-8"))
        print('\n')
        client.send("Connected to the server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

print("Server Running.....")
receive()