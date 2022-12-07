import time
import socket
import threading
import sys
import os
import signal  
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, QGridLayout, QMessageBox, QTextBrowser
#Lecture fichier serveur 
def lectureFichierServeur():
    fichier = open("serveur.txt", "r")
    serveur = fichier.read()
    serveur = serveur.split("\n")
    fichier.close()
    return serveur


# Fonction qui permet de fermer proprement le client
def fermerClient(signum, frame):
    print("Fermeture du client...")
    client.send(b"fin")
    client.close()
    sys.exit(0)

# Gestion des ports utilisés

usedport = []
def port():
    portuse = 1024
    for i in usedport:
        if portuse == i:
            portuse = portuse + 1
            usedport.append(portuse)
    return portuse

def infoServeur(self):
    global client
    info = client.recv(1024).decode()
    if ".info" in info:
        info = info.split(".info")
        infotreter = info
    
trheadinfo = threading.Thread(target=infoServeur)
trheadinfo.start()

# Menu principal
signal.signal(signal.SIGINT, fermerClient)

class EcranPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        # Titre fenêtre
        self.setWindowTitle("Selection du serveur")

        #Etat connexion
        self.etat = QLabel("Etat de la connexion :")
        grid.addWidget(self.etat, 0, 0)
        self.etat1 = QLabel("Non connecté")
        grid.addWidget(self.etat1, 0, 1)
        #Liste machine
        self.liste = QComboBox()
        lectureFichierServeur()
        self.liste.addItems(lectureFichierServeur())
        grid.addWidget(self.liste, 1, 0)

        #Ajout Machine
        self.bouton_add = QPushButton("Ajouter un serveur")
        self.bouton_add.clicked.connect(self.add)
        grid.addWidget(self.bouton_add, 3, 0)

        #Retirer Machine
        self.bouton_remove = QPushButton("Retirer un serveur")
        self.bouton_remove.clicked.connect(self.remove)
        grid.addWidget(self.bouton_remove, 4, 0)

        #Connexion
        self.bouton = QPushButton("Connexion")
        self.bouton.clicked.connect(self.connexion)
        grid.addWidget(self.bouton, 2, 0)

        # Logs Commande
        self.logs = QLabel("Logs :")
        grid.addWidget(self.logs, 1, 3)
        self.logs1 = QTextBrowser()
        grid.addWidget(self.logs1, 2, 3, 3, 3)
        #Clear Logs
        self.clear = QPushButton("Clear")
        self.clear.clicked.connect(self.logs1.clear)
        grid.addWidget(self.clear, 4, 3, 3, 3)

        #Console
        self.console = QLabel("Console :")
        grid.addWidget(self.console, 6, 3)
        self.console1 = QTextBrowser()
        grid.addWidget(self.console1, 7, 3, 3, 3)
        #Champ Commande
        self.commande = QLineEdit()
        grid.addWidget(self.commande, 9, 3, 3, 3)
        #Bouton Commande
        self.bouton_commande = QPushButton("Envoyer")
        self.bouton_commande.clicked.connect(self.envoyer)
        grid.addWidget(self.bouton_commande, 10, 3, 3, 3)
        #Clear Console
        self.clear = QPushButton("Clear")
        self.clear.clicked.connect(self.console1.clear)
        grid.addWidget(self.clear, 12, 3, 3, 3)


        # Quitter
        self.bouton2 = QPushButton("Quitter")
        self.bouton2.clicked.connect(self.stop)
        grid.addWidget(self.bouton2, 5, 0)

        #Statistiques du serveur
        self.stat = QLabel("Statistiques du serveur :")
        self.cpu = QLabel("CPU :")
        self.cpu1 = QLabel("")
        self.ram = QLabel("RAM :")
        self.ram1 = QLabel("")
        self.disk = QLabel("DISK :")
        self.disk1 = QLabel("")
        self.os = QLabel("OS :")
        self.os1 = QLabel("")
        self.uptime = QLabel("Uptime :")
        self.uptime1 = QLabel("")
        self.hostname = QLabel("Hostname :")
        self.hostname1 = QLabel("")
        self.ip = QLabel("IP :")
        self.ip1 = QLabel("")
        
        #Affichage sur le GUI
        grid.addWidget(self.stat, 6, 0)
        grid.addWidget(self.cpu, 7, 0)
        grid.addWidget(self.cpu1, 7, 1)
        grid.addWidget(self.ram, 8, 0)
        grid.addWidget(self.ram1, 8, 1)
        grid.addWidget(self.disk, 9, 0)
        grid.addWidget(self.disk1, 9, 1)
        grid.addWidget(self.os, 10, 0)
        grid.addWidget(self.os1, 10, 1)
        grid.addWidget(self.uptime, 11, 0)
        grid.addWidget(self.uptime1, 11, 1)
        grid.addWidget(self.hostname, 12, 0)
        grid.addWidget(self.hostname1, 12, 1)
        grid.addWidget(self.ip, 13, 0)
        grid.addWidget(self.ip1, 13, 1)
    def envoyer(self):
        commande = self.commande.text()
        client.send(commande.encode())
        self.logs1.append("Commande envoyée : " + commande)
        self.commande.clear()

    def connexion(self):
        widget = QWidget()
        grid = QGridLayout()    
        widget.setLayout(grid)
        IP = self.liste.currentText()
        print(IP)
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, port()))
        print("Connexion établie avec le serveur sur le port {}".format(port()))
        self.etat1.setText("Connecté")
        self.logs1.append("Connexion établie avec le serveur " + IP + " sur le port {}".format(port()))
        self.setWindowTitle("Stats du serveur " + IP)
        grid.removeWidget(self.bouton)
        self.bouton_refresh = QPushButton("Rafraichir")
        self.bouton_refresh.clicked.connect(self.rafraichir)
        grid.addWidget(self.bouton_refresh, 2, 0)
        self.deconnexion = QPushButton("Deconnexion")
        self.deconnexion.clicked.connect(self.deco)
        grid.addWidget(self.deconnexion, 3, 0)
        self.show()
        self.stats()

    def deco(self):
        widget = QWidget()
        grid = QGridLayout()
        widget.setLayout(grid)
        client.send(b"fin")
        client.close()
        self.removeWidget(self.bouton)
        self.bouton = QPushButton("Connexion")
        self.bouton.clicked.connect(self.connexion)
        grid.addWidget(self.bouton, 2, 0)
        self.etat1.setText("Non connecté")
        self.logs1.setText("Déconnexion du serveur ")
        self.setWindowTitle("Selection du serveur")

    def rafraichir(self):
        self.stats()

    def stats(self):
        client.send(b"cpu")
        cpu = client.recv(1024).decode()
        self.cpu1.setText(cpu)
        print(cpu)
        client.send(b"ram")
        ram = client.recv(1024).decode()
        self.ram1.setText(ram)
        print(ram)
        client.send(b"disk")
        disk = client.recv(1024).decode()
        self.disk1.setText(disk)
        print(disk)
        client.send(b"os")
        os = client.recv(1024).decode()
        if os == "Darwin":
            os = "MacOS X Darwin"
        elif os == "Linux":
            os = "Linux"
        elif os == "Windows":
            os = "Windows"
        self.os1.setText(os)
        print(os)
        client.send(b"uptime")
        uptime = client.recv(1024).decode()
        self.uptime1.setText(uptime)
        print(uptime)
        client.send(b"hostname")
        hostname = client.recv(1024).decode()
        self.hostname1.setText(hostname)
        print(hostname)
        client.send(b"ip")
        ip = client.recv(1024).decode()
        self.ip1.setText(ip)
        print(ip)
        
    def stop(self):
        sys.exit(0)
    
    def add(self):
        self.close()
        self.ecran4 = AjoutMachine()
        self.ecran4.show()

    def remove(self):
        self.close()
        self.ecran5 = RemoveMachine()
        self.ecran5.show()
    
    def infoServeur(self):
        global client
        info = client.recv(1024).decode()
        if ".info" in info:
            info = info.split(".info")
            self.console.append(info)


class AjoutMachine(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Ajout Machine")
        #Champ
        self.champ_ip = QLineEdit(self)
        self.champ_ip.setPlaceholderText("IP")
        self.port = QLabel(self)
        self.port.setText("Port :" + str(port()))
        
        #Bouton
        self.bouton_ajout = QPushButton(self)
        self.bouton_ajout.setText("Ajouter")
        self.bouton_ajout.clicked.connect(self.ajout)
        self.bouton_retour = QPushButton(self)
        self.bouton_retour.setText("Retour")
        self.bouton_retour.clicked.connect(self.retour)
        #Placement
        grid.addWidget(self.champ_ip, 1, 1)
        grid.addWidget(self.port, 1, 2)
        grid.addWidget(self.bouton_ajout, 2, 1)
        grid.addWidget(self.bouton_retour, 2, 2)
    
    def ajout(self):
        if self.champ_ip.text() == "":
            QMessageBox.about(self, "Erreur", "Veuillez remplir tous les champs")
        else:
            with open("serveur.txt", "a") as fichier:
                fichier.write("\n" + self.champ_ip.text())
            self.QMessageBox = QMessageBox()
            self.QMessageBox.setText("Machine ajoutée")
            self.QMessageBox.exec_()

    def retour(self):
        self.close()
        self.ecran1 = EcranPrincipal()
        self.ecran1.show()

class RemoveMachine(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Suppression Machine")
        #Champ
        self.liste = QComboBox()
        lectureFichierServeur()
        self.liste.addItems(lectureFichierServeur())
        grid.addWidget(self.liste, 0, 0)
        self.port = QLabel(self)
        self.port.setText("Port :" + str(port()))
        
        #Bouton
        self.bouton_ajout = QPushButton(self)
        self.bouton_ajout.setText("Supprimer")
        self.bouton_ajout.clicked.connect(self.suppr)
        self.bouton_retour = QPushButton(self)
        self.bouton_retour.setText("Retour")
        self.bouton_retour.clicked.connect(self.retour)
        #Placement
        grid.addWidget(self.liste, 1, 1)
        grid.addWidget(self.port, 1, 2)
        grid.addWidget(self.bouton_ajout, 2, 1)
        grid.addWidget(self.bouton_retour, 2, 2)
    
    def suppr(self):
        if self.liste.currentText() == "":
            QMessageBox.about(self, "Erreur", "Veuillez remplir tous les champs")
        else:
            with open("serveur.txt", "r") as fichier:
                data = fichier.read()
                data = data.split("\n")
                data.remove(self.liste.currentText())
            with open("serveur.txt", "w") as fichier:
                fichier.write("\n".join(data))
            
            QMessageBox.about(self, "Suppression", "Suppression effectuée")

    def retour(self):
        self.close()
        self.ecran1 = EcranPrincipal()
        self.ecran1.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    trheadinfo = threading.Thread(target=infoServeur, args=(EcranPrincipal))
    trheadinfo.start()
    window = EcranPrincipal()
    window.show()

    app.exec()