class Users:
    def __init__(self):
        self.users = {}

    def add_user(self, pseudo, addr, client_socket):
        """Ajoute un utilisateur avec son pseudo et son adresse."""
        self.users[addr] = {"pseudo": pseudo, "socket": client_socket}

    def remove_user(self, pseudo):
        for addr, info in list(self.users.items()):
            if info["pseudo"] == pseudo:
                self.users.pop(addr)
                break

    def get_all_pseudos(self):
        return list(self.users.keys())

    def get_addr_by_pseudo(self, pseudo):
        return self.users.get(pseudo)
    def get_all_pseudos(self):
        """Retourne la liste des pseudos connectés."""
        return [user_info["pseudo"] for user_info in self.users.values()]
