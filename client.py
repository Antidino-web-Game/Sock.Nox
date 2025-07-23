import socket
import threading
import os
from GUI import GUI
import tkinter as tk
from client_connection import client

# Initialisation de la fenêtre GUI
gui = GUI(tk.Tk())
# Démarrer la boucle principale de la GUI dans un thread séparé
gui.master.after(0, gui.master.mainloop)

commandes = {
    '/pseudo': "liste les pseudos",
    '/exit': "quitte le chat",
    '/help': "affiche cette aide",
    '/clear': "efface l'écran",
    '/to' : "envoie un message privé à un utilisateur",
}




# Démarrer le thread de réception
thread_recv = threading.Thread(target=recevoir, daemon=True)
thread_recv.start()

while True:
    try:
        message = input("Entrez votre message (ou 'exit' pour quitter) : ")
        if any(message.startswith(cmd) for cmd in commandes.keys()):
            if message.startswith('/pseudo'):
                gui.cl.sendall('/pseudo'.encode('utf-8'))
            elif message.startswith('/exit'):
                gui.cl.sendall('/exit'.encode('utf-8'))
                gui.cl.close()
                print("Déconnexion du serveur.")
                exit()
            elif message.startswith('/help'):
                print("Commandes disponibles :")
                for cmd, desc in commandes.items():
                    print(f"{cmd} : {desc}")
            elif message.startswith('/clear'):
                os.system('cls' if os.name == 'nt' else 'clear')
            elif message.startswith('/to'):
                message= input("Entrez le pseudo du destinataire : ")
                message += " " + input("Entrez votre message privé : ")
                gui.cl.sendall(("#"+message).encode('utf-8'))    
        else:
            gui.cl.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")
