import socket
import threading
import os

commandes = {
    '/pseudo': "liste les pseudos",
    '/exit': "quitte le chat",
    '/help': "affiche cette aide",
    '/clear': "efface l'écran",
    '/to' : "envoie un message privé à un utilisateur",
}

def recevoir():
    while True:
        try:
            data = cl.recv(1024)
            if not data:
                print("\nConnexion fermée par le serveur.")
                break
            print(f"\n[Serveur] : {data.decode('utf-8')}")
            print("Entrez votre message (ou '/help' pour les commandes) : ",end="" ,flush=True)
        except Exception as e:
            print(f"\nErreur lors de la réception : {e}")
            break

cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl.connect(('127.0.0.1', 12345))
print("Connexion établie avec le serveur.")
pseudo = input("Entrez votre pseudo : ")
cl.sendall(pseudo.encode('utf-8'))

# Démarrer le thread de réception
thread_recv = threading.Thread(target=recevoir, daemon=True)
thread_recv.start()

while True:
    try:
        message = input("Entrez votre message (ou 'exit' pour quitter) : ")
        if any(message.startswith(cmd) for cmd in commandes.keys()):
            if message.startswith('/pseudo'):
                cl.sendall('/pseudo'.encode('utf-8'))
            elif message.startswith('/exit'):
                cl.sendall('/exit'.encode('utf-8'))
                cl.close()
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
                cl.sendall(("#"+message).encode('utf-8'))    
        else:
            cl.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")