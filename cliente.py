#!/usr/bin/python

#*************************************
#           Super Chat               *
#    version 1.0 By Dionys Rosario   *
#   Top contributors: Gadiel Reyes   *
# 2012@copyleft all wrongs reversed  *
#*************************************

import socket, os, sys, threading 

sc = socket.socket()
sc.connect((raw_input('Digite la direccion del chat:\n'), 9999))

class redactar(threading.Thread):
    def __init__(self, sc):
        threading.Thread.__init__(self)
        self.mensaje = ''
        self.sc = sc
    def run(self):
        while True:
            self.mensaje = raw_input()
            self.sc.send(self.mensaje)
        self.conn.close()

class recibir(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.mensaje = ''
        self.sc = sc
    def run(self):
        while True:
            self.mensaje = self.sc.recv( 1024 )
            print(self.mensaje)
        self.sc.close()


print '**************************************'
print '*          Super Chat                *'
print '*  version 1.0 By Dionys Rosario     *'
print '* 2012@copyleft all wrongs reversed  *'
print '**************************************'
print ''
print """\n--->comandos:
[usuarios] ver usuarios conectados
[nick] entrar en el chat
[@nickname] para mensajes privados
[chgnick] para cambiar el nickname
[salir] para salir del chat
[ayuda] ver ayuda\n"""
print ""
print "--- Escriba el comando a ejecutar ---"

redactar(sc).start()
recibir(sc).start()
