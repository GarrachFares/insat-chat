from getpass import getpass
import hashlib
import re
import sqlite3
from tabnanny import check
from chat.Utilisateur import Utilisateur


class Authentification:
    def __init__(self):
        self.connection = sqlite3.connect("utilisateurs_bd.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='UTILISATEUR';")
        if (self.cursor.fetchone()[0] != 'UTILISATEUR'):
            print("Pas de compte trouvé.")
            exit()

    def authentifier(self):
        utilisateur = Utilisateur()
        essais = 0
        email_input = ''
        mdp_input = ''
        credentials_valides = False
        while (not credentials_valides and essais < 3):
            email_input = input("Entrer votre email:\n> ")
            while (not self.verifier_email_valide(email_input)):
                print("Email invalide.")
                email_input = input("Entrer votre email de nouveau:\n> ")
            utilisateur.setEmail(email_input)
            mdp_input = getpass("Entrer votre mot de passe:\n> ")
            motdepasse = hashlib.sha256(mdp_input.encode()).hexdigest()
            utilisateur.setMotdepasse(motdepasse)
            essais += 1
            credentials_valides, utilisateur = self.trouver_utilisateur(
                utilisateur)
        return credentials_valides or essais == 3, utilisateur

    def verifier_email_valide(self, email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(regex, email)

    def trouver_utilisateur(self, utilisateur: Utilisateur):
        sql_query = 'SELECT * FROM utilisateur WHERE email=? and motdepasse=?;'
        utilisateur_a_trouver=(
            utilisateur.email,
            utilisateur.motdepasse
        )
        self.cursor.execute(sql_query, utilisateur_a_trouver)
        if (self.cursor.fetchall() == []):
            print("Credentials invalides.")
            return False, None
        token=input("Entrer le token secret associe a ce compte:\n> ")
        if (not self.verifier_token(token,utilisateur.email)):
            print("Credentials invalides.")
            return False, None

        self.cursor.execute(sql_query, utilisateur_a_trouver)
        utilisateur_trouve=self.cursor.fetchone()
        utilisateur.setPrenom(utilisateur_trouve[0])
        utilisateur.setNom(utilisateur_trouve[1])
        return True, utilisateur

    def verifier_token(self, token, email):
        sql_query='SELECT * FROM utilisateur WHERE token=? and email=?'
        self.cursor.execute(sql_query, (token,email,))
        return self.cursor.fetchall() != []
