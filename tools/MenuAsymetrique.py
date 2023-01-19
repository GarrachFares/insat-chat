import os
from tools.RSA import rsa_menu
from tools.ElGamal import elgamal_menu

def asymetrique_menu():
    os.system('cls')
    choix = ''
    while(choix != '3'):
        print()
        print("---------------Menu Chiffrement/Dechiffrement Asymetrique--------------")
        print("1- ElGamal")
        print("2- RSA")
        print("3- Revenir au menu principal")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == "1"):
            elgamal_menu()
        if (choix == "2"):
            rsa_menu()
        if (choix == "3"):
            os.system('cls')
            break
