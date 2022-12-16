import socket,threading,sys,signal
from threading import Thread
from PyQt5.QtWidgets import *


#Lecture du fichier serveur 
def lectureFichierServeur():
    try:
        fichier = open("serveur.txt", "r")
        serveur = fichier.read()
        serveur = serveur.split("\n")
        fichier.close()
        return serveur
    except Exception as e:
        EcranPrincipal.InfoBox("Impossible de lire le fichier serveur.txt{0}".format(e), "Erreur")
        return []


#Fermeture du client
def fermerClient(self):
    print("Fermeture du client...")
    self.client.send(b"fin")
    self.client.close()
    sys.exit(0)

#Gestion des ports utilisés
usedport = []
def port():
    portuse = 1024
    for i in usedport:
        if portuse == i:
            portuse = portuse + 1
            usedport.append(portuse)
    return portuse

#GUI
signal.signal(signal.SIGINT, fermerClient)
class EcranPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Selection du serveur")
        self.etat = QLabel("Etat de la connexion :")
        grid.addWidget(self.etat, 0, 0)
        self.etat2 = QLabel("Non connecté")
        grid.addWidget(self.etat2, 1, 0)
        self.listesrv = QComboBox()
        lectureFichierServeur()
        self.listesrv.addItems(lectureFichierServeur())
        grid.addWidget(self.listesrv, 2, 0)
        #Ajout de Machine
        self.boutonajout = QPushButton("Ajouter un serveur")
        self.boutonajout.clicked.connect(self.add)
        grid.addWidget(self.boutonajout, 4, 0)
        #Suppretion de Machine
        self.bouton_retire = QPushButton("Retirer un serveur")
        self.bouton_retire.clicked.connect(self.remove)
        grid.addWidget(self.bouton_retire, 5, 0)
        #Bouton de deconnexion
        self.deconnexion = QPushButton("Deconnexion")
        self.deconnexion.clicked.connect(self.deco)
        grid.addWidget(self.deconnexion, 8, 0)
        #Connexion
        self.bouton = QPushButton("Connexion")
        self.bouton.clicked.connect(self.connexion)
        grid.addWidget(self.bouton, 3, 0)
        #Logs des commandes
        self.logs = QLabel("Logs :")
        grid.addWidget(self.logs, 1, 1)
        self.logs2 = QTextBrowser()
        grid.addWidget(self.logs2, 2, 1, 3, 3)
        #Affichage de la console
        self.console = QLabel("Console :")
        grid.addWidget(self.console, 6, 1)
        self.console2 = QTextBrowser()
        grid.addWidget(self.console2, 7, 1, 3, 3)
        #Ligne de commande
        self.commande = QLineEdit()
        grid.addWidget(self.commande, 9, 1, 1, 3)
        #Envoie des Commandes
        self.bouton_commande = QPushButton("Envoyer")
        self.bouton_commande.clicked.connect(self.envoyer)
        grid.addWidget(self.bouton_commande, 11, 1, 1, 3)
        #Netoyage de la console
        self.clear = QPushButton("Clear")
        self.clear.clicked.connect(self.console2.clear)
        grid.addWidget(self.clear, 12, 1, 1, 3)
        #Netoyage des Logs
        self.clear = QPushButton("Clear")
        self.clear.clicked.connect(self.logs2.clear)
        grid.addWidget(self.clear, 5, 1, 1, 3)
        #Quitter le client
        self.bouton2 = QPushButton("Quitter")
        self.bouton2.clicked.connect(self.stop)
        grid.addWidget(self.bouton2, 6, 0)
        #Bouton de rafraichissement
        self.bouton_refresh = QPushButton("Rafraichir")
        self.bouton_refresh.clicked.connect(self.rafraichir)
        grid.addWidget(self.bouton_refresh, 7, 0)
    #Envoie des commandes
    def envoyer(self):
        try:
            commande = self.commande.text()
            self.client.send(commande.encode())
            self.logs2.append("Commande envoyée : " + commande)
            self.commande.clear()
        except Exception as e:
            self.InfoBox("Erreur d'envoi de commande : " + str(e))

    #connexion au serveur
    def connexion(self):
        widget = QWidget()
        grid = QGridLayout()    
        widget.setLayout(grid)
        IP = self.listesrv.currentText()
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((IP, port()))
        except Exception as e:
            self.InfoBox("Erreur de connexion : " + str(e))
        print("Connexion établie avec le serveur sur le port {}".format(port()))
        self.etat2.setText("Connecté")
        self.logs2.append("Connexion établie avec le serveur " + IP + " sur le port {}".format(port()))
        self.setWindowTitle("Stats du serveur " + IP)
        self.show()
        self.stats()

    #Afichage des messages d'erreurs
    def InfoBox(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()

    #rafraichissement des stats
    def rafraichir(self):
        try:
            self.stats()
        except Exception as e:
            self.InfoBox("Imposible de rafraîchir : " + str(e))

    #Affichage des stats
    def stats(self):
        self.client.send(b"cpu")
        cpu = str("CPU: " + self.client.recv(1024).decode())
        self.console2.append(cpu + "%")
        self.client.send(b"ram")
        ram = str("RAM: " + self.client.recv(1024).decode())
        self.console2.append(ram)
        self.client.send(b"disk")
        disk = str("DISK: " + self.client.recv(1024).decode())
        self.console2.append(disk)
        self.client.send(b"os")
        os = self.client.recv(1024).decode()
        if os == "Darwin":
            os = "MacOS"
        elif os == "Linux":
            os = "Linux"
        elif os == "Windows":
            os = "Windows"
        self.console2.append(str("OS: " + os))
        self.client.send(b"uptime")
        uptime = str("UPTIME: " + self.client.recv(1024).decode())
        self.console2.append(uptime)
        self.client.send(b"hostname")
        hostname = str("HOSTNAME: " + self.client.recv(1024).decode())
        self.console2.append(hostname)
        self.client.send(b"ip")
        ip = str("IP: " + self.client.recv(1024).decode())
        self.console2.append(ip)

    #deconexion du serveur
    def deco(self):
        self.client.send(b"fin")
        self.client.close()
        self.etat2.setText("Non connecté")
        self.logs2.setText("Déconnexion du serveur ")
        self.setWindowTitle("Selection du serveur")

    #Test d'affichage
    '''def affichage(self):
        while True:
            donnes = self.client.recv(1024).decode()
            if donnes == "1.1.1.1.info":
                self.console2.append(donnes)'''

    #Fermeture du client
    def stop(self):
        sys.exit(0)

    #Ajout de machine
    def add(self):
        self.close()
        self.ecran2 = AjoutMachine()
        self.ecran2.show()

    #Suppression de machine
    def remove(self):
        self.close()
        self.ecran3 = RemoveMachine()
        self.ecran3.show()

    #Fermeture du client
    def stop(self):
        sys.exit(0)

#Classe pour l'ajout de machine
class AjoutMachine(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Ajout Machine")
        self.ip = QLineEdit(self)
        self.ip.setPlaceholderText("IP")
        self.port = QLabel(self)
        self.port.setText("Port : {}".format(port()))
        self.ajout = QPushButton(self)
        self.ajout.setText("Ajouter")
        self.ajout.clicked.connect(self.ajout)
        self.retour = QPushButton(self)
        self.retour.setText("Retour")
        self.retour.clicked.connect(self.retour)
        grid.addWidget(self.ip, 1, 1)
        grid.addWidget(self.port, 1, 2)
        grid.addWidget(self.ajout, 2, 1)
        grid.addWidget(self.retour, 2, 2)
    
    #Fonction pour afficher les erreurs
    def InfoBox2(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()

    #Ajout de machine
    def ajout(self):
        try:
            if self.ip.text() == "":
                QMessageBox.about(self, "Erreur", "Veuillez remplir tous les champs")
            else:
                with open("serveur.txt", "a") as fichier:
                    fichier.write("\n" + self.ip.text())
                self.QMessageBox = QMessageBox()
                self.QMessageBox.setText("Machine ajoutée")
                self.QMessageBox.exec_()
        except Exception as e:
            self.InfoBox2("Erreur : " + str(e))

    #Retour à l'écran principal
    def retour(self):
        self.close()
        self.ecran1 = EcranPrincipal()
        self.ecran1.show()

#Classe pour la suppression de machine
class RemoveMachine(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Suppression de Machine")
        self.listesrv = QComboBox()
        lectureFichierServeur()
        self.listesrv.addItems(lectureFichierServeur())
        grid.addWidget(self.listesrv, 0, 0)
        self.port = QLabel(self)
        self.port.setText("Port :{}".format(port()))
        self.ajout = QPushButton(self)
        self.ajout.setText("Supprimer")
        self.ajout.clicked.connect(self.suppr)
        self.retour = QPushButton(self)
        self.retour.setText("Retour")
        self.retour.clicked.connect(self.retour)
        grid.addWidget(self.listesrv, 1, 1)
        grid.addWidget(self.port, 1, 2)
        grid.addWidget(self.ajout, 2, 1)
        grid.addWidget(self.retour, 2, 2)
    
    #Fonction pour afficher les erreurs
    def InfoBox3(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()

    #Suppression de machine
    def suppr(self):
        try:
            if self.listesrv.currentText() == "":
                QMessageBox.about(self, "Erreur", "Veuillez remplir tous les champs")
            else:
                with open("serveur.txt", "r") as fichier:
                    data = fichier.read()
                    data = data.split("\n")
                    data.remove(self.listesrv.currentText())
                with open("serveur.txt", "w") as fichier:
                    fichier.write("\n".join(data))
                QMessageBox.about(self, "Suppression", "Suppression effectuée")
        except Exception as e:
            self.InfoBox3("Erreur : " + str(e))

    #Retour à l'écran principal
    def retour(self):
        self.close()
        self.ecran1 = EcranPrincipal()
        self.ecran1.show()

'''
class consoletraitement(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.deamon = True
        self.start()
        def traitment(self):
            while True:
                self.client.send("")
                datatrait = self.client.recv(1024).decode()
                print(datatrait)
                data1 = datatrait.split(".info")
                for i in data1:
                    if i!= "":data1 = str(i)
                if datatrait > data1:
                    EcranPrincipal.console2.append(data1)
                else:
                    print("marchepas")
'''
#Fonction pour lancer le programme
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EcranPrincipal()
    '''consoletraitement()'''
    window.show()

    app.exec()