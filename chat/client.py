import os, datetime
import json, socket, threading

from termcolor import colored
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode


class Client:
    def __init__(self, server, port, username):
        self.server = server
        self.port = port
        self.username = username
        self.isStopped = False

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server, self.port))
        except Exception as e:
            print(colored('[!] ' + e.__str__(), 'red'))

        self.s.send(self.username.encode())
        print(colored('[+] Connecte avec succes!', 'green'))
        print(colored('[+] Echangement de cles...', 'yellow'))

        self.create_key_pairs()
        self.exchange_public_keys()
        global secret_key
        secret_key = self.handle_secret()

        print(colored('[+] Initiation complete', 'green'))
        print(colored('[+] Vous pouvez echanger des messages', 'green'))

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()
        while not self.isStopped:
            continue

    def handle_messages(self):
        while not self.isStopped:
            message = self.s.recv(1024).decode()
            if message:
                key = secret_key
                decrypt_message = json.loads(message)
                iv = b64decode(decrypt_message['iv'])
                cipherText = b64decode(decrypt_message['ciphertext'])
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                msg = cipher.decrypt(cipherText)
                current_time = datetime.datetime.now()
                print(colored(current_time.strftime('%Y-%m-%d %H:%M:%S ') + msg.decode(), 'green'))
            else:
                print(colored('[!] Connection au serveur perdue', 'red'))
                print(colored('[!] Fermeture de connection', 'red'))
                self.s.shutdown(socket.SHUT_RDWR)
                self.isStopped = True

    def input_handler(self):
        while True:
            message = input('> ')
            if message == "EXIT":
                break
            else:
                key = secret_key
                cipher = AES.new(key, AES.MODE_CFB)
                message_to_encrypt = self.username + ": " + message
                msgBytes = message_to_encrypt.encode()
                encrypted_message = cipher.encrypt(msgBytes)
                iv = b64encode(cipher.iv).decode('utf-8')
                message = b64encode(encrypted_message).decode('utf-8')
                result = json.dumps({'iv': iv, 'ciphertext': message})
                self.s.send(result.encode())

        self.s.shutdown(socket.SHUT_RDWR)
        self.isStopped = True

    def handle_secret(self):
        secret_key = self.s.recv(1024)
        private_key = RSA.importKey(open(f'chatroom_keys/{self.username}_private_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(secret_key)

    def exchange_public_keys(self):
        try:
            print(colored('[+] Recevoir la cle publique du serveur', 'yellow'))
            server_public_key = self.s.recv(1024).decode()
            server_public_key = RSA.importKey(server_public_key)

            print(colored('[+] Envoyement de cle publique au serveur', 'yellow'))
            public_pem_key = RSA.importKey(open(f'chatroom_keys/{self.username}_public_key.pem', 'r').read())
            self.s.send(public_pem_key.exportKey())
            print(colored('[+] Echangement complete!', 'green'))

        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... ' + str(e), 'red'))

    def create_key_pairs(self):
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_pem = private_key.exportKey().decode()
            public_pem = public_key.exportKey().decode()
            with open(f'chatroom_keys/{self.username}_private_key.pem', 'w') as priv:
                priv.write(private_pem)
            with open(f'chatroom_keys/{self.username}_public_key.pem', 'w') as pub:
                pub.write(public_pem)

        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... ' + e.__str__(), 'red'))


def initialize_and_start_client(username):
    client = Client('127.0.0.1', 8081, username)
    client.create_connection()
