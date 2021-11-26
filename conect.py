import json
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5559


class Server:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))

    def send_data(self, data):
        self.sock.sendall(json.dumps(data).encode("utf-8"))

    def get_data(self):
        return json.loads(self.sock.recv().decode("utf-8"))

    def init_connect(self, id, count):
        return

