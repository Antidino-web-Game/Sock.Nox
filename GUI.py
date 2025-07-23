import tkinter as tk
from tkinter import messagebox
from client_connection import client
import threading
import socket
class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sock.Nox client")
        self.message = "Bienvenue dans Sock.Nox !\nVeuillez saisir votre pseudo :"
        self.pseudo = ""
        self.label = tk.Label(master, text=self.message)
        self.label.pack(pady=40)
        self.button = tk.Button(master, text="Envoyer", command=self.send_pseudo)
        self.button.pack(pady=10)
        self.entry = tk.Entry(master)
        self.entry.pack(pady=10)
        self.entry.focus()

    def send_pseudo(self):
        self.pseudo = self.entry.get()
        self.cl = client()
        self.cl.__init__(self.pseudo)
        self.message = f"Bienvenue {self.pseudo} !\nVous pouvez maintenant commencer à discuter."
        self.label.config(text=self.message)
        self.entry.delete(0, tk.END)
        self.button.config(text="Envoyer Message", command=self.send_pseudo)
        self.entry.focus()
        thread_recv = threading.Thread(target=self.recevoir, daemon=True)
        thread_recv.start()
        
    def update_message(self, new_message):
        self.message = new_message
        self.label.config(text=self.message)
    def recevoir(self):
        while True:
            try:
                data = self.cl.recv(1024)
                if not data:
                    self.update_message("Déconnexion du serveur.")
                    print("Déconnexion du serveur.")
                    break
                    self.update_message(f"\n[Serveur] : {data.decode('utf-8')}")
                print("Entrez votre message (ou '/help' pour les commandes) : ",end="" ,flush=True)
            except Exception as e:
                print(f"\nErreur lors de la réception : {e}")
                break
    
         
gui = GUI(master=tk.Tk())
gui.master.mainloop()