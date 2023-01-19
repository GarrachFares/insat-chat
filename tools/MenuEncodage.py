import base64
import os

def encodage_menu():
    os.system('cls')
    choix = ''
    while True:
        print()
        print("---------------Menu Encodage--------------")
        print("1- Encodage d'un message")
        print("2- Decodage d'un message")
        print("3- Revenir au menu principal")
        print("-------------------------------------------")
        choix = input("> ")
        if (choix == '1'):
            message = input("Entrer un message a encoder:\n> ")
            message_encode = encode(message)
            print (f"Message Encode en Base64: {message_encode}")
        if (choix == '2'):
            message = input("Entrer un message a decoder:\n> ")
            message_decode = decode(message)
            print (f"Message Decode en Base64: {message_decode}")
        if (choix == '3'):
            os.system('cls')
            break


def encode(message):
    enc_message = message.encode('ascii')
    base64_enc_message = base64.b64encode(enc_message)
    base64_message = base64_enc_message.decode('ascii')
    return base64_message

def decode(message):
    enc_message = message.encode('ascii')
    base64_dec_message = base64.b64decode(enc_message)
    base64_message = base64_dec_message.decode('ascii')
    return base64_message

def encode_base64(message: str):
    return base64.encode(message.encode('ascii'))

def decode_base64(coded_message: str):
    return base64.decode(coded_message.encode('ascii'))
