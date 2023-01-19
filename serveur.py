import socket, threading
import os, datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from termcolor import colored



class Serveur:
    def __init__(self, port):

        self.host = '127.0.0.1'
        self.port = port
        self.isStopped = False

    def start_server(self):

        self.generate_keys()
        secret_key = get_random_bytes(16)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = []

        self.s.bind((self.host, self.port))
        self.s.listen(100)

        print(colored('Host: ' + str(self.host), 'white'))
        print(colored('Port: ' + str(self.port), 'white'))

        self.username_lookup = {}

        while not self.isStopped:
            c, addr = self.s.accept()
            if (self.isStopped):
                break
            username = c.recv(1024).decode()
            print(colored('[+] Nouvelle connection. Utilisateur: ' + str(username), 'yellow'))
            self.broadcast(' Nouvelle personne a joigne le chatroom. Utilisateur: ' + username)
            self.username_lookup[c] = username
            self.clients.append(c)
            client_pub_key = self.send_pub_key(c)
            encrypted_secret = self.encrypt_secret(client_pub_key, secret_key)
            self.send_secret(c, encrypted_secret)
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg):
        for connection in self.clients:
            print(colored('[+] Broadcast message: ' + msg, 'yellow'))

    def generate_keys(self):
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_key_pem = private_key.exportKey().decode()
            public_key_pem = public_key.exportKey().decode()
            with open('chatroom_keys/server_private_key.pem', 'w') as priv:
                priv.write(private_key_pem)
            with open('chatroom_keys/server_public_key.pem', 'w') as pub:
                pub.write(public_key_pem)
            return public_key

        except Exception as e:
            print(e)

    def encrypt_secret(self, client_pub_key, secret_key):
        try:
            cpKey = RSA.importKey(client_pub_key)
            cipher = PKCS1_OAEP.new(cpKey)
            encrypted_secret = cipher.encrypt(secret_key)
            return encrypted_secret

        except Exception as e:
            print(e)

    def send_secret(self, c, secret_key):
        try:
            c.send(secret_key)
            print(colored('[+] Cle secrete est envoye au client', 'yellow'))

        except Exception as e:
            print(e)

    def send_pub_key(self, c):
        try:
            public_key = RSA.importKey(open('chatroom_keys/server_public_key.pem', 'r').read())
            c.send(public_key.exportKey())
            client_pub_key = c.recv(1024)
            print(colored('[+] Cle publique du client recu', 'yellow'))
            return client_pub_key

        except Exception as e:
            print(e)

    def handle_client(self, c, addr):

        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                self.broadcast(str(self.username_lookup[c]) + ' est sorti.')
                break

            if msg.decode() != '':
                current_time = datetime.datetime.now()
                print(colored(current_time.strftime('%Y-%m-%d %H:%M:%S') + ' Message echange', 'blue'))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)
            else:
                print(colored('[+] ' + self.username_lookup[c] + ' est sorti du serveur.', 'red'))
                for conn in self.clients:
                    if conn == c:
                        self.clients.remove(c)
                break


def terminate(Serveur):
    while True:
        command = input('')
        if (command == 'TERMINATE'):
            for conn in Serveur.clients:
                conn.shutdown(socket.SHUT_RDWR)
            print(colored('[+] Tous les connections sont terminees', 'red'))
        break
    print(colored('[+] Serveur est ferme', 'red'))
    Serveur.isStopped = True
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((Serveur.host, Serveur.port))
    Serveur.s.close()


def initialize_and_start_server():
    serveur = Serveur(8081)
    t_terminate = threading.Thread(target=terminate, args=(serveur,))
    t_terminate.start()
    serveur.start_server()

