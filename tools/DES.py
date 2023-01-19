import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import DES
import os

def des():
    os.system('cls')
    choix = ''
    while(choix != '3'): 
        print()
        print("---------------Menu DES--------------")
        print("1- Chiffrer un message")
        print("2- Dechiffrer un message")
        print("3- Revenir au menu Chiffrement/Dechiffrement Symetrique")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == "1"):
            key = input("Entrer une cle (il faut une taille de 8):\n> ")
            message = input("Entrer un message:\n> ")
            descipher = DESCipher(bytes(key.encode()))
            ciphertext = descipher.encrypt(bytes(message.encode()))
            print("Le texte chiffre est: ", ciphertext.hex())
            filename = input("Donner le path du fichier pour sauvegarder le texte chiffre:\n> ")
            with open(filename, 'wb') as f:
                f.write(ciphertext)
            continue
        if (choix == "2"):
            key = input("Entrer une cle (il faut une taille de 8):\n> ")
            filename = input("Donner le path du fichier contenant le texte chiffre:\n> ")
            with open(filename, 'rb') as f:
                enc_message = f.read()
            descipher = DESCipher(bytes(key.encode()))
            plaintext = descipher.decrypt(enc_message)
            print("Le texte dechiffre est: ", plaintext)
            continue
        if (choix == "3"):
            os.system('cls')
            break

class DESCipher(object):
    
    def __init__(self, key):
        self.bs = DES.block_size
        self.key = key

    def encrypt(self, message):
        cipher = DES.new(self.key, DES.MODE_ECB)
        padded_message = self.pad(message)
        ciphertext = cipher.encrypt(padded_message)
        return ciphertext

    def decrypt(self, ciphertext):
        cipher = DES.new(self.key, DES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()
    
    def pad(self, message):
        while (len(message) % 8 != 0):
            message += b'\x00'
        return message
