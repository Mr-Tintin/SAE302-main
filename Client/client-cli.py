import time
import socket
import threading
import sys
import os
import signal

# Fonction qui permet de fermer proprement le client
def fermerClient(signum, frame):
    print("Fermeture du client...")
    client.send(b"fin")
    client.close()
    sys.exit(0)

# Fonction qui permet de se connecter au serveur de test
def seConnecter():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 4269))
    print("Connexion établie avec le serveur sur le port 4269")

# Menu principal
signal.signal(signal.SIGINT, fermerClient)
seConnecter()
while True:
    msg = input("Entrez une commande: ")
    data = client.recv(1024)
    print(data.decode())
    client.send(msg.encode())
    if msg == "fin":
        client.send(b"FIN")
        break
