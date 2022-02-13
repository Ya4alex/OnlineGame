import json
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5560


class Server:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))

    def send_data(self, data):
        self.sock.sendall(f"#{json.dumps(data)}".encode("utf-8"))

    def get_data(self):
        _data = self.sock.recv(3048).decode("utf-8")
        print(_data)
        try:
            self.get_data_res = json.loads(_data)
        except:
            self.get_data_res = {}
    def init_connect(self):
        _d = json.loads(self.sock.recv(512).decode("utf-8"))
        return {"id": int(_d.get("your_id")), "count": int(_d.get("pl_count"))}
