import json
import socket
from collections import deque
from threading import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5560
print(f"host: {HOST} port: {PORT}")
server_socket.bind((HOST, PORT))


class Client:
    def __init__(self, socket, address, id):
        self.id = id
        self.sock = socket
        self.addr = address
        self.data = deque([], 100)

    def collect_data_break(self):
        self.sock.setblocking(0)
        try:
            _data = self.sock.recv(1024).decode("utf-8")
            self.data.append(json.loads(_data[_data.rfind('#')+1:]))
        except socket.error:  # данных нет
            print("passed")

    def send_data(self, stk):
        try:
            self.sock.sendall(json.dumps(stk).encode("utf-8"))
        except:
            pass

    def connect(self, id, count):
        self.send_data({"type": "hello", "your_id": id, "pl_count": count})


players = []


def get_player(id, *args):
    try:
        clientsocket, address = server_socket.accept()
        client = Client(clientsocket, address, id)
        client.connect(id, *args)
        print(f"client {id} joined")
        players[id] = client
    except Exception as e:
        print(e)


def get_players(count=2):
    global players
    players = [None] * count
    server_socket.listen(count)
    _buf = []
    print('server started and listening')
    for i in range(count):
        _ = Thread(target=get_player, args=(i, count))
        _.start()
        _buf.append(_)
    for i in _buf:
        i.join()
    print('lobby is full! Lets game!\n', players)
    return players
