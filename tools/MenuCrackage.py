import hashlib
import os

def crackage_menu():
    os.system('cls')
    choix = ''
    while (choix != '4'):
        print()
        print("---------------Menu Crackage--------------")
        print("1- Cracker un message hache avec MD5")
        print("2- Cracker un message hache avec SHA-1")
        print("3- Cracker un message hache avec SHA256")
        print("4- Revenir au menu principal")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == '1'):
            trouve = False
            message_hache = input("Entrer un message hache:\n> ")
            with open('insat.dic', 'r') as f:
                for line in f:
                    if (hashlib.md5(line.rstrip('\n').encode()).hexdigest() == message_hache):
                        print("E-mail cracke.")
                        print(f"E-mail : {line}")
                        trouve = True
                        break
                if not trouve:
                    print("Crackage echoue.")
                
        if (choix == '2'):
            trouve = False
            message_hache = input("Entrer un message hache:\n> ")
            with open('insat.dic', 'r') as f:
                for line in f:
                    if (hashlib.sha1(line.rstrip('\n').encode()).hexdigest() == message_hache):
                        print("E-mail cracke.")
                        print(f"E-mail : {line}")
                        trouve = True
                        break
                if not trouve:
                    print("Crackage echoue.")
        if (choix == '3'):
            trouve = False
            message_hache = input("Entrer un message hache:\n> ")
            with open('insat.dic', 'r') as f:
                for line in f:
                    if (hashlib.sha256(line.rstrip('\n').encode()).hexdigest() == message_hache):
                        print("E-mail cracke.")
                        print(f"E-mail : {line}")
                        trouve = True
                        break
                if not trouve:
                    print("Crackage echoue.")
        if (choix == '4'):
            os.system('cls')
            break
