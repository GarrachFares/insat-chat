import os
from chat.Registration import Registration
from chat.Authentification import Authentification


def authentifier_choix():
    
    
    print("   𝔸𝕦𝕥𝕙𝕖𝕟𝕥𝕚𝕗𝕚𝕔𝕒𝕥𝕚𝕠𝕟  ")
    print()
    print("1- S'inscrire ")
    print("2- Se connecter ")
    print("3- Quitter")
    print()
    print()
    choix = input("Donner le numero du choix:\n> ")
    authentifie = False
    while (not authentifie):
        if (choix == '1'):
            registration = Registration()
            authentifie, utilisateur = registration.registrer()
            return utilisateur
        if (choix == '2'):
            authentification = Authentification()
            authentifie, utilisateur = authentification.authentifier()
            return utilisateur
        if (choix == '3'):
            exit()
