import hashlib
import os

def hachage_menu():
    os.system('cls')
    choix = ''
    while (choix != '4'):
        print()
        print("---------------Menu Hachage--------------")
        print("1- Hacher un message avec MD5")
        print("2- Hacher un message avec SHA-1")
        print("3- Hacher un message avec SHA256")
        print("4- Revenir au menu principal")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == '1'):
            message = input("Entrer un message a hacher:\n> ")
            message_hache = hashlib.md5(message.encode()).hexdigest()
            print(f"Message hache: {message_hache}")
        if (choix == '2'):
            message = input("Entrer un message a hacher:\n> ")
            message_hache = hashlib.sha1(message.encode()).hexdigest()
            print(f"Message hache: {message_hache}")
        if (choix == '3'):
            message = input("Entrer un message a hacher:\n> ")
            message_hache = hashlib.sha256(message.encode()).hexdigest()
            print(f"Message hache: {message_hache}")
        if (choix == '4'):
            os.system('cls')
            break	
