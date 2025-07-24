import tkinter as tk
from tkinter import messagebox
from client_connection import client
import winsound
import threading
import time
from PIL import Image, ImageTk
import ast
import socket
class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sock.Nox client")
        self.master.resizable(False, False)
        self.master.geometry("300x200")
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message = "Bienvenue dans Sock.Nox !\nVeuillez saisir votre pseudo :"
        self.pseudo = "null"
        self.label = tk.Label(left_frame, text=self.message)
        self.label.pack(pady=40)
        self.button = tk.Button(left_frame, text="Envoyer", command=self.send_pseudo)
        self.button.pack(pady=10)
        self.to_btn = tk.Button(right_frame,text="Message privé",command=self.to)
        self.to_btn.pack()
        self.listbox = tk.Listbox(right_frame, bg="#1e1e2f", fg="#ffffff", font=("Segoe UI", 10))
        self.listbox.pack()
        self.entry = tk.Entry(left_frame)
        self.entry.pack(pady=10)
        self.entry.focus()
        self.listbox.insert(tk.END,"Aucun utilisateur \nconnecté")
        self.listbox.bind('<<ListboxSelect>>',self.private_message)

    def to(self):
        messagebox.showwarning("Attention","Veuillez selectionnez un destinataire")

    def send_pseudo(self):
        self.pseudo = self.entry.get()
        if not self.pseudo:
            messagebox.showerror("Erreur", "Veuillez entrer un pseudo.")
            return
        self.cl = client(self.pseudo)
        time.sleep(0.9)
        winsound.MessageBeep()
        self.message = f"Bienvenue {self.pseudo} !\nVous pouvez maintenant commencer à discuter."
        self.master.geometry("500x200")
        self.label.config(text=self.message)
        self.entry.delete(0, tk.END)
        self.button.config(text="Envoyer Message", command=self.send)
        self.button.update()
        self.entry.focus()
        thread_recv = threading.Thread(target=self.recevoir, daemon=True)
        thread_recv.start()
    import ast

    def nettoyer_liste(self,chaine):

        return str(chaine).replace("connecté", "").strip()

    def debug(self):
        while True:
            print(self.entry.get())    
    def private_message(self,e):
        liste = self.listbox.get('active')
        desitataire = self.nettoyer_liste(list)
        messagebox.showinfo("message privé",f"vous parler maintenant à {desitataire}")
    def update_message(self, new_message):
        self.message = new_message
        self.label.config(text=self.message)

    def update_connection_list(self,pseudos):
        self.listbox.delete(0, tk.END)
        if pseudos :
            for pseudo in pseudos:
                self.listbox.insert(tk.END, f"{pseudo} connecté")
        else:
            self.listbox.insert(tk.END,"Aucun utilisateur \nconnecté")
    def recevoir(self):
        while True:
            try:
                data = self.cl.cl.recv(1024)
                if not data:
                    self.update_message("Déconnexion du serveur.")
                    print("Déconnexion du serveur.")
                    break
                data = data.decode("utf-8")
                try :
                    liste = ast.literal_eval(data)
                    liste.remove(self.pseudo)
                    print(f"pseudo updated {liste}")
                    self.update_connection_list(liste)
                except Exception as E:
                    self.update_message(f"\n[Serveur] : {data.decode('utf-8')}")
            except Exception as e:
                print(f"\nErreur lors de la réception : {e}")
                break
    def send(self):
        mesage = self.entry.get()
        self.entry.delete(0,tk.END)
        self.cl.send_message(mesage)
    
         
gui = GUI(master=tk.Tk())
gui.master.mainloop()