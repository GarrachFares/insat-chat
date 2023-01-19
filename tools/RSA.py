import rsa
import os

def rsa_menu():
    os.system('cls')
    choix = ''
    while (choix != '6'):
        print()
        print("---------------Menu RSA--------------")
        print("1- Chiffrer un message")
        print("2- Dechiffrer un message")
        print('3- Signer un message')
        print('4- Verifier la signature')
        print("5- Generer des cles")
        print("6- Revenir au menu Chiffrement/Dechiffrement Asymetrique")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == '1'):
            encrypt_menu()
        if (choix == '2'):
            decrypt_menu()
        if (choix == '3'):
            sign_menu()
        if (choix == '4'):
            verify_menu()
        if (choix == '5'):
            generate_keys()
        if (choix == "6"):
            os.system('cls')
            break


def load_public_key(path):
    try:
        with open(path, 'rb') as f:
            pubKey = rsa.PublicKey.load_pkcs1(f.read())
        return pubKey
    except:
        print("Cle introuvable.")
    
def load_private_key(path):
    try:
        with open(path, 'rb') as f:
            privKey = rsa.PrivateKey.load_pkcs1(f.read())
        return privKey
    except:
        print("Cle introuvable.")
    
def encrypt_menu():
    message = input("Entrer un message a chiffrer:\n> ")
    pubKey = load_public_key("keys/rsa_pubkeys.pem")
    if (pubKey):
        encrypted_message = encrypt(message, pubKey)
        print("Message chiffre: ", encrypted_message)
        file_path = input("Donner le path du fichier pour sauvegarder le texte chiffre:\n> ")
        with open(file_path, 'wb') as f:
            f.write(encrypted_message)

def decrypt_menu():
    file_path = input("Donner le path du fichier contenant le texte chiffre:\n> ")
    privKey = load_private_key('keys/rsa_privkey.pem')
    with open(file_path, 'rb') as f:
        enc_message = f.read()
    if (privKey):
        message = decrypt(enc_message, privKey)
        print("Message Dechiffre: ", message)
    
def sign_menu():
    message = input("Donner le message a signer:\n> ")
    privKey = load_private_key('keys/rsa_privkey.pem')
    if (privKey):
        signature = sign_sha1(message, privKey)
        print("Signature: ", signature)
        with open('keys/rsa_signature.sign', 'wb') as f:
            f.write(signature)

def verify_menu():
    message = input("Entrer le message chiffre a verifier:\n> ")
    pubKey = load_public_key("keys/rsa_pubkeys.pem")
    with open('keys/rsa_signature.sign', 'rb') as f:
        signature = f.read()
    if verify_sha1(message, signature, pubKey):
        print('Signature verifiee!')
    else:
        print('Signature non verifiee')

def generate_keys():
    (pubKey, privKey) = rsa.newkeys(2048)
    with open('keys/rsa_pubkeys.pem', 'wb') as f:
        f.write(pubKey.save_pkcs1('PEM'))

    with open('keys/rsa_privkey.pem', 'wb') as f:
        f.write(privKey.save_pkcs1('PEM'))
    print("Cles generes.")

def encrypt(msg, key):
    return rsa.encrypt(msg.encode('ascii'), key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False

def sign_sha1(msg, key):
    return rsa.sign(msg.encode('ascii'), key, 'SHA-1')

def verify_sha1(msg, signature, key):
    try:
        return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-1'
    except:
        return False
