import socket

class client:
    def __init__(self,pseudo):
        self.cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cl.connect(('127.0.0.1', 12345))
        self.cl.sendall(pseudo.encode("utf-8"))
        self.commandes = {
            '/pseudo': "liste les pseudos",
            '/exit': "quitte le chat",
            '/help': "affiche cette aide",
            '/clear': "efface l'écran",
            '/to' : "envoie un message privé à un utilisateur",
        }
    def send_message(self, message):
        print(f"Envoi du message : {message}")
        self.cl.sendall(message.encode('utf-8'))      