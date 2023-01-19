from Crypto.Cipher import DES
import os
from tools.MenuEncodage import encodage_menu
from tools.MenuHachage import hachage_menu
from tools.MenuSymetrique import symetrique_menu
from tools.MenuAsymetrique import asymetrique_menu

def tool_menu():
    os.system('cls')
    choix = ''
    while(choix != '3'): 
        print()
        print()
        print("𝕆𝕦𝕥𝕚𝕝𝕤")
        print()
        print("1- Encodage et Decodage d'un message")
        print("2- Hachage d'un message")
        print("3- Chiffrement et déchiffrement symétrique d'un message")
        print("4- Chiffrement et déchiffrement asymétrique d'un message")
        print("5- back")
        print()
        choix = input("Donner le numero du choix:\n> ")
        if (choix == '1'):
            encodage_menu()
        if (choix == '2'):
            hachage_menu()
        if (choix == '3'):
            symetrique_menu()
        if (choix == '4'):
            asymetrique_menu()
        if (choix == '5'):
            os.system('cls')
            break    

