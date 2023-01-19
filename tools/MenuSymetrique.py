import os
from tools.AES256 import aes
from tools.DES import des

def symetrique_menu():
    os.system('cls')
    choix = ''
    while(choix != '3'):
        print()
        print("---------------Menu Chiffrement/Dechiffrement Symetrique--------------")
        print("1- DES")
        print("2- AES256")
        print("3- Revenir au menu principal")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == "1"):
            des()
        if (choix == "2"):
            aes()
        if (choix == "3"):
            os.system('cls')
            break
