import re
import secrets
import sqlite3
import hashlib
import string
from chat.Utilisateur import Utilisateur
from getpass import getpass


class Registration:
    def __init__(self):
        self.connection = sqlite3.connect("utilisateurs_bd.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='UTILISATEUR';")
        if (self.cursor.fetchall() == []):
            self.cursor.execute(
                "CREATE TABLE UTILISATEUR(prenom VARCHAR2, nom VARCHAR2, email VARCHAR2, motdepasse VARCHAR2, token VARCHAR2)")

    def registrer(self):
        utilisateur = Utilisateur()
        email_input = input("Entrer votre email:\n> ")
        utilisateur_existe = self.verifier_utilisateur_existant(email_input)
        while (not self.verifier_email_valide(email_input) or utilisateur_existe):
            if (not self.verifier_email_valide(email_input)):
                print("Email invalide.")
            if (utilisateur_existe):
                print("Email existe deja.")
            email_input = input("Entrer votre email de nouveau:\n> ")
            utilisateur_existe = self.verifier_utilisateur_existant(
                email_input)
        utilisateur.setEmail(email_input)

        prenom_input = input("Entrer votre prenom:\n> ")
        while (not self.verfier_nom(prenom_input)):
            print("Prenom invalide.")
            prenom_input = input("Entrer votre prenom de nouveau:\n> ")
        utilisateur.setPrenom(prenom_input)

        nom_input = input("Entrer votre nom:\n> ")
        while (not self.verfier_nom(nom_input)):
            print("Nom invalide.")
            nom_input = input("Entrer votre nom de nouveau:\n> ")
        utilisateur.setNom(nom_input)

        mdp_input = 'none'
        mdp2_input = 'none2'

        while(mdp_input != mdp2_input):

            mdp_input = getpass("Entrer votre mot de passe:\n> ")

            while(not self.verifier_motdepasse(mdp_input)):
                print("Le mot de passe doit contenir 1 caractere majuscule, 1 caractere minuscule, 1 chiffre et de taille minimale de 8")
                mdp_input = getpass(
                    "Entrer votre mot de passe de nouveau:\n> ")
            mdp2_input = getpass("Verifier votre mot de passe:\n> ")
            if (mdp_input != mdp2_input):
                print("Verification eronnee.")
        motdepasse = hashlib.sha256(mdp_input.encode()).hexdigest()
        utilisateur.setMotdepasse(motdepasse)

        token = self.generer_token()
        utilisateur.setToken(token)

        print()
        print("Le token associé à ce compte est: ", utilisateur.token)

        with open("./tokens", 'a') as f:
            f.write(''+utilisateur.prenom+' '+utilisateur.nom+': '+utilisateur.token+"\n")
        self.enregistrer_bd(utilisateur)

        return True, utilisateur

    def verifier_email_valide(self, email):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(regex, email)

    def verfier_nom(self, nom):
        regex = re.compile(r'^[a-zA-Z]+$')
        return re.fullmatch(regex, nom)

    def verifier_motdepasse(self, passwd):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$')
        return re.fullmatch(regex, passwd)

    def verifier_utilisateur_existant(self, email):
        self.cursor.execute(
            'SELECT * FROM utilisateur WHERE email=?', (email,))
        return self.cursor.fetchall() != []

    def enregistrer_bd(self, utilisateur: Utilisateur):
        sql_query = 'INSERT INTO utilisateur VALUES(?,?,?,?,?);'
        utilisateur_insertion = (
            utilisateur.prenom,
            utilisateur.nom,
            utilisateur.email,
            utilisateur.motdepasse,
            utilisateur.token
        )
        self.cursor.execute(sql_query, utilisateur_insertion)
        self.connection.commit()

    def generer_token(self):
        num = 8
        token = ''.join(secrets.choice(string.ascii_letters +
                                       string.digits) for x in range(num))
        return token
