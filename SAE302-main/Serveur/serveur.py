import psutil,subprocess,signal,time,threading,socket,platform,sys


#Gèrer les connexions et les commandes
def commandeduclt(conn, addr):
    print("Connexion de %s:%s" % (addr[0], addr[1]))
    while True:
        try:
            data = conn.recv(1024)
        except:
            print("Connexion de %s:%s perdue" % (addr[0], addr[1]))
            ouvrirSocket()
        print(data.decode())
        cmd = data.startswith(b"CMD") or data.startswith(b"cmd")
        if data == b"fin":
            conn.close()
            print("Connexion de %s:%s fermée" % (addr[0], addr[1]))
            ouvrirSocket()
        elif data == b"Reset":
            resetServeur()
        elif data == b"cpu":
            conn.send(str(psutil.cpu_percent(interval=1)).encode())
        elif data == b"ram":
            print("ram-envoyé")
            conn.send((str(round(psutil.virtual_memory().total / (1024.0 **3))).encode()) + b" Go") #ram totale
        elif data == b"disk":
            print("disk-envoyé")
            conn.send(str(round(psutil.disk_usage('/').total / (1024.0 **3))).encode() + b" Go") #disk totale
        elif data == b"uptime":
            print("uptime-envoyé")
            conn.send(str(round(time.time() - psutil.boot_time())).encode())
        elif data == b"os":
            print("os-envoyé")
            conn.send(platform.system().encode())
        elif data == b"hostname":
            print("hostname-envoyé")
            conn.send(platform.node().encode())
        elif data == b"ip":
            print("ip-envoyé")
            conn.send(socket.gethostbyname(socket.gethostname()).encode())
            conn.send(b",")
        elif data == b"ip.info":
            print("ip.info-envoyé")
            donne = "1.1.1.1.info"
            conn.send(donne.encode())
            conn.send(b",")
        elif data == b"users":
            print("users-envoyé")
            conn.send(str(len(psutil.users())).encode())
        elif data == b"process":
            print("process-envoyé")
            conn.send(str(len(psutil.pids())).encode())
        elif cmd == True:
            commande(data)
        elif data == b"":
            conn.send(b"")
        elif data == b"kill":
            conn.send(b"Shutdown en cours")
            fermetureSrv()
        elif data == b"help":
            conn.send(b"cpu, ram, disk, uptime, os, hostname, ip, users")
        elif data == b"os-cmd":
            conn.send(b"OSX")
        else:
            conn.send(b"Commande inconnue")
    
#Reset le serveur
def resetServeur():
    conn.send(b"Reset en cours")
    serveur.close()
    ouvrirSocket()

#Ouvre les sockets
def ouvrirSocket():
    global serveur
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("0.0.0.0", port()))
    serveur.listen(5)
    print("Serveur prêt, en attente de requêtes ...")

#Ferme le serveur
def fermetureSrv():
    print("Fermeture du serveur en cours...")
    serveur.close()
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

#Traitement des commandes
def commande(data):
    global cmd
    cmd = data[4:]
    cmd = cmd.decode()
    cmd = cmd.split(" ")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output, errors = p.communicate()
    conn.send(output)
    conn.send(errors)


#Menu principal
signal.signal(signal.SIGINT, fermetureSrv)
ouvrirSocket()
while True:
    conn, addr = serveur.accept()
    print("Connexion en cours...")
    thread = threading.Thread(target = commandeduclt, args = (conn, addr))
    thread.start()
