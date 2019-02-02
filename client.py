# coding: utf-8

import socket as sockett
import threading
import sys

hote = "localhost"
port = 15555

Con = False
socket = None

def Exit():
    if socket is not None:
        socket.close()
    print("Close")
    sys.exit(0)

def connect(hote=hote, port=port) :
    global Con
    global socket

    try:
        socket = sockett.socket(sockett.AF_INET, sockett.SOCK_STREAM)
        socket.setsockopt(sockett.SOL_SOCKET, sockett.SO_REUSEADDR, 1)
        socket.connect((hote, port))
        Con = True
        print ("Connection on {}".format(port))

        # Create new threads
        threadR = myThreadRevived(socket)
        # Start new Threads
        threadR.start()

    except:
        socket.close()
        print ('erreur, Connexion immpossible')

##Tread recive##
class myThreadRevived (threading.Thread):
    def __init__(self, thread):
        threading.Thread.__init__(self)
        self.daemon = True
        self.thread = thread
    def run(self):
        print("ok")
        try:
            response = self.thread.recv(255)
        except KeyboardInterrupt:
            Exit()
        if (response.decode()) == "/stop":
            global Con
            Con = False
            print (" Connexion Fermée")
            Exit()
        print(response.decode())

def send(inp):
    global Con

    try:
        socket.send(str.encode(inp))
    except:
        print("erreur, Connexion disparue")
        Con = False

def close():
    global Con
    global Run

    if Con == True:
        send("/stop")
    Con = False
    Run = False

def loop_connection():
    global Con

    while Con:
        inp = input()
        if inp == "/close":
            close()
        else:
            send(inp)
Run = True
while Run:
    try:
        inp = input()
    except (KeyboardInterrupt, SystemExit):
        raise

    if inp == "/close":
        close()
        Run = False
    elif inp == "/connect":
        connect()
        if Con:
            loop_connection()
    else:
        print("cmd inconnue")



