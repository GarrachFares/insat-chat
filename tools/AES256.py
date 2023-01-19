import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os

def aes():
    os.system('cls')
    choix =''
    while(choix != '3'):
        print()
        print("---------------Menu AES256--------------")
        print("1- Chiffrer un message")
        print("2- Dechiffrer un message")
        print("3- Revenir au menu Chiffrement/Dechiffrement Symetrique")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == "1"):
            key = input("Entrer la cle :\n> ")
            message = input("Entrer un message:\n> ")
            aescipher = AESCipher(key)
            ciphertext = aescipher.encrypt(message)
            print("Le texte chiffre est: ", ciphertext.decode())
            filename = input("Donner le path du fichier pour sauvegarder le texte chiffre:\n> ")
            with open(filename, 'wb') as f:
                f.write(ciphertext)
            continue
        if (choix == "2"):
            key = input("Entrer la cle :\n> ")
            filename = input("Donner le path du fichier contenant le texte chiffre:\n> ")
            with open(filename, 'rb') as f:
                enc_message = f.read()
            aescipher = AESCipher(key)
            plaintext = aescipher.decrypt(enc_message)
            print("Le texte dechiffre est: ", plaintext)
            continue
        if (choix == "3"):
            os.system('cls')
            break

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
