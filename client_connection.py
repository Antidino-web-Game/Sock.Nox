import socket
import ssl

class client:
    def __init__(self,pseudo):
        # 1) créez un socket vierge
        host = "127.0.0.1"
        port = 12345
        underlying = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2) enveloppez-le en SSL AVANT connect()
        self.context = ssl._create_unverified_context()   # ou create_default_context()
        self.cl = self.context.wrap_socket(
            underlying,
            server_hostname=host
        )

        # 3) enfin, connectez-vous
        self.cl.connect((host, port))

        # 4) et envoyez votre pseudo
        self.cl.sendall(pseudo.encode('utf-8'))
        self.commandes = {
            '/pseudo': "liste les pseudos",
            '/exit': "quitte le chat",
            '/help': "affiche cette aide",
            '/clear': "efface l'écran",
            '/to' : "envoie un message privé à un utilisateur",
        }
        self.pseudos = []
    def send_message(self, message):
        print(f"Envoi du message : {message}")
        self.cl.sendall(message.encode('utf-8'))      
    def update_pseudo(self,new_pseudo):
        self.pseudos = new_pseudo