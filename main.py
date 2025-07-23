import socket
import threading
from users import Users

users = Users()

class Srv:
    def __init__(self):
        pass

    def send_message(self, client_socket, message):
        try:
            client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")

    def is_pseudo_taken(self, pseudo):
        return pseudo in users.get_all_pseudos()

    def notify_users(self, message, exclude_pseudo=None):
        for user_addr, user_info in users.users.items():
            if user_info["pseudo"] != exclude_pseudo:
                self.send_message(user_info["socket"], message)

    def handle_client(self, client_socket, addr):
        try:
            data = client_socket.recv(1024).decode('utf-8').strip()
            print(f("[{addr}]: {data}"))
            if data.startswith("#"):
                if self.is_pseudo_taken(data):
                    self.send_message(client_socket, "Pseudo déjà utilisé. Veuillez en choisir un autre.")
                    client_socket.close()
                    return
                users.add_user(data, addr, client_socket)
                print(f"Connexion de {addr} avec le pseudo {data}")
            else:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    if message.startswith('/'):
                        if message == '/pseudo':
                            self.send_message(client_socket, f"Pseudos connectés : {', '.join(users.get_all_pseudos())}")
                        continue
                    print(f"Reçu de {data}({addr}): {message}")
                    self.notify_users(f"[{data}] : {message}", exclude_pseudo=data)
        except Exception as e:
            print(f"Erreur avec {data}({addr}) : {e}")
        finally:
            print("a")

    def start(self, host='127.0.0.1', port=12345):
        srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_socket.bind((host, port))
        srv_socket.listen()
        print(f"Serveur en écoute sur {host}:{port}...")

        try:
            while True:
                client_socket, addr = srv_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.start()
        except KeyboardInterrupt:
            print("Arrêt du serveur.")
        finally:
            srv_socket.close()

if __name__ == "__main__":
    serveur = Srv()
    serveur.start()
