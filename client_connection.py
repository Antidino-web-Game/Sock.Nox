import socket
class client:
    def __init__(self,pseudo=""):
        self.cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cl.connect(('127.0.0.1', 12345))
        self.cl.sendall(pseudo.encode('utf-8'))