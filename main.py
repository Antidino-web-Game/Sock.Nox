import socket
import threading
from users import Users
import tkinter as tk
import ssl
import os

users = Users()

class Srv:
    def __init__(self):
        self.gui = ""
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")


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
            pseudo = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Pseudo reçu : {pseudo}")  # ✅ Affiche le pseudo
            if self.is_pseudo_taken(pseudo):
                self.send_message(client_socket, "Pseudo déjà utilisé. Veuillez en choisir un autre.")
                client_socket.close()
                return

            users.add_user(pseudo, addr, client_socket)
            self.gui.update_connection_list()
            print(f"Connexion de {addr} avec le pseudo {pseudo}")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Déconnexion de {pseudo}({addr})")
                    break
                message = data.decode('utf-8')
                print(f"Message reçu de {pseudo}: {message}")  # ✅ Affiche le message reçu

                if message.startswith('/'):
                    if message == '/pseudo':
                        self.send_message(client_socket, f"Pseudos connectés : {', '.join(users.get_all_pseudos())}")
                    elif message.startswith('/to '):
                        # Envoi de message privé
                        target_pseudo, msg_private = message.split(" ", 1)[1].split(" ", 1)
                        print(f"Message privé vers {target_pseudo} : {msg_private}")
                        self.send_private_message(target_pseudo, msg_private, exclude_pseudo=pseudo)
                    continue

                print(f"Reçu de {pseudo}({addr}): {message}")
                self.notify_users(f"[{pseudo}] : {message}", exclude_pseudo=pseudo)
        
        except ConnectionResetError as e:
            if e.errno == 10054:
                print(f"Connexion perdue avec {pseudo}({addr}) : {e}")
                users.remove_user(pseudo)
                self.gui.update_connection_list()

            else:
                print(f"Erreur de connexion avec {pseudo}({addr}) : {e}")
        except Exception as e:
            print(f"Erreur inattendue avec {pseudo}({addr}) : {e}")

        finally:
            users.remove_user(pseudo)
            client_socket.close()
    def send_private_message(self, target_pseudo, message, exclude_pseudo=None):
        """Envoie un message privé à un utilisateur si ce pseudo existe."""
        for user_addr, user_info in users.users.items():
            if user_info["pseudo"] == target_pseudo and user_info["pseudo"] != exclude_pseudo:
                self.send_message(user_info["socket"], f"Message privé : {message}")
                return
        # Si le pseudo n'est pas trouvé
        self.send_message(exclude_pseudo, f"Utilisateur {target_pseudo} non trouvé.")


    def start(self, host='127.0.0.1', port=12345):

        srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_socket.bind((host, port))
        srv_socket.listen()
        print(f"Serveur en écoute sur {host}:{port}...")
        try:
            while True:
                raw_client_socket, addr = srv_socket.accept()
                client_socket = self.context.wrap_socket(raw_client_socket, server_side=True)
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.start()
        except KeyboardInterrupt:
            print("Arrêt du serveur.")
        finally:
            srv_socket.close()
class GUI:
    def __init__(self,master,srv,users):
        self.users=users
        self.master = master
        self.master.title("Sock.Nox serveur")
        #self.master.resizable(False, False)
        self.master.geometry("300x200")
        self.serveur = srv
        #GUI organisation avec des frame
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        #compteur d'utilisateur
        self.counter = tk.IntVar(value=0)
        self.counter_label = tk.Label(right_frame, textvariable=self.counter, fg="#ffffff", bg="#1e1e2f", font=("Segoe UI", 10, "bold"))
        self.counter_label.pack(pady=(10, 0))
        self.label = tk.Label(left_frame, text="Bienvenue dans Sock.Nox !")
        self.label.pack(pady=40)
        self.button = tk.Button(left_frame, text="Démarrer serveur", command=self.start)
        self.button.pack(pady=10)
        self.listbox = tk.Listbox(right_frame, bg="#1e1e2f", fg="#ffffff", font=("Segoe UI", 10))
        self.listbox.pack(pady=5, fill=tk.BOTH, expand=True)

    def start(self):
        self.label.config(text="le serveur a démaré\nSur écoute...")
        threading.Thread(target=self.serveur.start, daemon=True).start()
    def update_connection_list(self):
        self.listbox.delete(0, tk.END)
        pseudos = self.users.get_all_pseudos()
        if pseudos :
            for pseudo in pseudos:
                self.listbox.insert(tk.END, f"{pseudo} connecté")
                self.counter.set(len(pseudos))
        else:
            self.counter.set(0)
        self.serveur.notify_users(f"#{self.users.get_all_pseudos()}")


if __name__ == "__main__":
    serveur = Srv()
    gui=GUI(tk.Tk(),serveur,users)
    serveur.gui=gui
    gui.master.mainloop()
    
