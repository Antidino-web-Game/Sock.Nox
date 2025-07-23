import socket
import threading
from users import Users

users = Users()

class srv():
    def __init__(self):
        pass
    def send_message(client_socket, message):
        """Envoie un message à un client."""
        try:
            client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")

    def is_pseudo_taken(pseudo):
        return pseudo in users.get_all_pseudos()

    def notify_users(self,message, exclude_pseudo=None):
        """Envoie un message à tous les utilisateurs sauf éventuellement un."""
        for user_addr, user_info in users.users.items():
            if user_info["pseudo"] != exclude_pseudo:
                self.send_message(user_info["socket"], message)

    def handle_client(self,client_socket, addr):
        """Gère la connexion et la communication avec un client."""
        pseudo = client_socket.recv(1024).decode('utf-8').strip()
        #if is_pseudo_taken(pseudo):
        #    send_message(client_socket, "Pseudo déjà utilisé. Veuillez en choisir un autre.")
        #    client_socket.close()
        #    return
        users.add_user(pseudo, addr, client_socket)
        print(f"Connexion de {addr} avec le pseudo {pseudo}")

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                if message.startswith('/'):
                    if message == '/pseudo':
                        self.send_message(client_socket, f"Les pseudos sont : {', '.join(users.get_all_pseudos())}")
                    continue
                else:
                    print(f"Reçu de {pseudo}({addr}): {message}")
                    self.notify_users(f"[{pseudo}] : {message}", exclude_pseudo=pseudo)
        except Exception as e:
            print(f"Erreur avec {pseudo}({addr}) : {e}")

        print(f"Déconnexion de {pseudo}({addr})")
        users.remove_user(pseudo)
        client_socket.close()

    def start(self,host='127.0.0.1', port=12345):
        """Démarre le serveur et accepte les connexions entrantes."""
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind((host, port))
        srv.listen()
        print("Serveur en écoute...")

        while True:
            client_socket, addr = srv.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            thread.start()

if __name__ == "__main__":
    serveur = srv()
    serveur.start()