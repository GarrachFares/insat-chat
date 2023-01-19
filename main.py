import os
from chat.MenuAuthentification import authentifier_choix
from chat.Chatroom import chatroom_menu
from tools.menu import tool_menu


def main():
    os.system('cls')
    print()

    
    choix = ''
    while True:
        print("   ＩＮＳＡＴ     ＣＨＡＴ   ")
        
        print()
        print("𝕄𝕖𝕟𝕦 𝕡𝕣𝕚𝕟𝕔𝕚𝕡𝕒𝕝")
        print()
        print("1- tools")
        print("2- Chatroom")
        print("3- Quitter")
        print()
        choix = input("Donner le numero du choix:\n> ")
        if (choix == '1'):
            tool_menu()
        if (choix == '2'):
            utilisateur = authentifier_choix()
            utilisateur.afficher()
            chatroom_menu(utilisateur)
        if (choix == '3'):
            exit()


if __name__ == "__main__":
    main()
 
