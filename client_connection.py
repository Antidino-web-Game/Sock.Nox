import socket

class client:
    def __init__(self):
        self.cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cl.connect(('127.0.0.1', 12345))
        self.commandes = {
            '/pseudo': "liste les pseudos",
            '/exit': "quitte le chat",
            '/help': "affiche cette aide",
            '/clear': "efface l'écran",
            '/to' : "envoie un message privé à un utilisateur",
        }
    def send_message(self, message):
        print(message)
        try:
            if any(message.startswith(cmd) for cmd in self.commandes.keys()):
                if message.startswith('/pseudo'):
                    self.cl.sendall('/pseudo'.encode('utf-8'))
                elif message.startswith('/exit'):
                    self.cl.sendall('/exit'.encode('utf-8'))
                    self.cl.close()
                    print("Déconnexion du serveur.")
                    exit()
                elif message.startswith('/help'):
                    print("Commandes disponibles :")
                    for cmd, desc in self.commandes.items():
                        print(f"{cmd} : {desc}")
                elif message.startswith('/clear'):
                    return "clear"
            else:
                    self.cl.sendall(message.encode('utf-8'))
        except Exception as e:
                print(f"Erreur lors de l'envoi du message : {e}")