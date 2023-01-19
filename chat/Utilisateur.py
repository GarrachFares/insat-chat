class Utilisateur:
    def __init__(self):
        self.prenom = None
        self.nom = None
        self.email = None
        self.motdepasse = None
        self.token = None

    def setPrenom(self, prenom):
        self.prenom = prenom

    def setNom(self, nom):
        self.nom = nom

    def setEmail(self, email):
        self.email = email

    def setMotdepasse(self, motdepasse):
        self.motdepasse = motdepasse

    def setToken(self, token):
        self.token = token

    def afficher(self):
        print()
        print("Bienvenue " + self.prenom + " " + self.nom + " :D")
