import time
import sys
import os
import signal
import threading
import socket
import platform
import psutil
import subprocess



# Fonction qui permet de fermer proprement le serveur
def fermerServeur():
    print("Fermeture du serveur...")
    serveur.close()
    sys.exit(0)

def resetServeur(connexion):
    connexion.send(b"Reset en cours")
    serveur.close()
    ouvrirSocket()

# Fonction qui permet de gérer les connexions entrantes

def gererConnexion(connexion, adresse):
    print("Connexion de %s:%s" % (adresse[0], adresse[1]))
    while True:
        data = connexion.recv(1024)
        print(data.decode())
        cmd = data.startswith(b"CMD") or data.startswith(b"cmd")
        if data == b"Reset":
            resetServeur()
        elif data == b"cpu":
            connexion.send(platform.processor().encode())
        elif data == b"ram":
            connexion.send((str(round(psutil.virtual_memory().total / (1024.0 **3))).encode()) + b" Go") #ram totale
        elif data == b"disk":
            connexion.send(str(round(psutil.disk_usage('/').total / (1024.0 **3))).encode() + b" Go") #disk totale
        elif data == b"uptime":
            connexion.send(str(round(time.time() - psutil.boot_time())).encode())
        elif data == b"os":
            connexion.send(platform.system().encode())
        elif data == b"hostname":
            connexion.send(platform.node().encode())
        elif data == b"ip":
            connexion.send(socket.gethostbyname(socket.gethostname() + ".info").encode())
            hostname=socket.gethostname()   
            print(socket.gethostbyname(hostname))
            connexion.send(b",")
        elif data == b"users":
            connexion.send(str(len(psutil.users())).encode())
        elif data == b"process":
            connexion.send(str(len(psutil.pids())).encode())
        elif cmd == True:
            commande(data)
        elif data == b"":
            connexion.send(b"")
        elif data == b"kill":
            connexion.send(b"Shutdown en cours")
            fermerServeur()
        elif data == b"help":
            connexion.send(b"cpu, ram, disk, uptime, os, hostname, ip, users")
        elif data == b"os-cmd":
            connexion.send(b"OSX")
        else:
            connexion.send(b"Commande inconnue")
    

# Fonction qui permet d'ouvrir les sockets
def ouvrirSocket():
    global serveur
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("", port()))
    serveur.listen(5)
    print("Serveur prêt, en attente de requêtes ...")

# Gestions des commandes envoyée à distance

def commande(data, connexion):
    global cmd
    cmd = data[4:]
    cmd = cmd.decode()
    cmd = cmd.split(" ")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output, errors = p.communicate()
    connexion.send(output)
    connexion.send(errors)

# Gestion des ports utilisés

usedport = []
def port():
    portuse = 1024
    for i in usedport:
        if portuse == i:
            portuse = portuse + 1
            usedport.append(portuse)
    return portuse

# Menu principal

signal.signal(signal.SIGINT, fermerServeur)
ouvrirSocket()
while True:
    connexion, adresse = serveur.accept()
    print("Connexion en cours...")
    thread = threading.Thread(target=gererConnexion, args=(connexion, adresse))
    thread.start()
