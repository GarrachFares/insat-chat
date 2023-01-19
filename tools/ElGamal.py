import random  
from math import pow
import pickle
import os

def elgamal_menu():
    os.system('cls')
    choix = ''
    while (choix != '4'):
        print()
        print("---------------Menu ElGamal--------------")
        print("1- Chiffrer un message")
        print("2- Dechiffrer un message")
        print("3- Generer des cles")
        print("4- Revenir au menu Chiffrement/Dechiffrement Asymetrique")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == '1'):
            elgamal_encrypt_proc()
        if (choix == '2'):
            el_gamal_decrypt_proc()
        if (choix == '3'):
            generate_keys()
        if (choix == "4"):
            os.system('cls')
            break
  
a = random.randint(2, 10) 
  
def gcd(a, b): 
    if a < b: 
        return gcd(b, a) 
    elif a % b == 0: 
        return b; 
    else: 
        return gcd(b, a % b) 
  
def gen_key(q): 
  
    key = random.randint(pow(10, 20), q) 
    while gcd(q, key) != 1: 
        key = random.randint(pow(10, 20), q) 
  
    return key 
  
def power(a, b, c): 
    x = 1
    y = a 
  
    while b > 0: 
        if b % 2 == 0: 
            x = (x * y) % c; 
        y = (y * y) % c 
        b = int(b / 2) 
  
    return x % c 
  
def encrypt(msg, q, h, g): 
  
    en_msg = [] 
  
    k = gen_key(q) 
    s = power(h, k, q) 
    p = power(g, k, q) 
      
    for i in range(0, len(msg)): 
        en_msg.append(msg[i]) 
  
    for i in range(0, len(en_msg)): 
        en_msg[i] = s * ord(en_msg[i]) 
  
    return en_msg, p 
  
def decrypt(en_msg, p, key, q): 
  
    dr_msg = [] 
    h = power(p, key, q) 
    for i in range(0, len(en_msg)): 
        dr_msg.append(chr(int(en_msg[i]/h))) 
          
    return dr_msg  


def elgamal_encrypt_proc():
    message = input("Entrer un message:\n> ")
    with open("keys/elgamal_pubkeys.pem", 'rb') as f:
        pubKey, q, g = pickle.load(f)
    enc_message, u = encrypt(message, q, pubKey, g)
    message_path = input("Donner le path du fichier pour sauvegarder le texte chiffre:\n> ")
    with open(message_path, 'wb') as f:
        pickle.dump((enc_message, u, q), f)

def el_gamal_decrypt_proc():
    message_path = input("Donner le path du fichier contenant le texte chiffre:\n> ")
    with open("keys/elgamal_privkey.pem", 'rb') as f:
        privKey, q, g = pickle.load(f)
    with open(message_path, 'rb') as f:
        enc_message, u, o = pickle.load(f)
        dr_message = decrypt(enc_message, u, privKey, o)
    print("Message dechiffre: " + ''.join(dr_message))

def generate_keys():
    q = random.randint(pow(10, 20), pow(10, 50)) 
    g = random.randint(2, q) 
    privKey = gen_key(q)
    with open("keys/elgamal_privkey.pem", 'wb') as f:
        pickle.dump((privKey, q, g),f)
    pubKey = power(g, privKey, q)
    with open("keys/elgamal_pubkeys.pem", 'wb') as f:
        pickle.dump((pubKey, q, g),f)
    print("Cles generes.")
