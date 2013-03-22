#!/usr/bin/python

import string, threading, socket, os

usuarios = {'nick':[], 'source':[]}

nopermitido = ('nick', 'nickname')

class chatPrincipal(threading.Thread):
    
    def __init__(self, sc):
        threading.Thread.__init__(self)
        self.sc = sc
        self.conectado = False
        self.datos = ''

    def testNick(self, nick):
        if nick in usuarios['nick']:
            self.sc.send('nickname ya esta en uso, intenta con otro')
            return False
        elif nick == '':
            self.sc.send('debe escribir un nickname')
            return False
        elif nick in nopermitido or ' ' in nick:
            self.sc.send(nick + ' no esta permitido ni nickname con espacios en blanco')
            return False
        else:
            return True

    
    def run(self):
        while True:
            self.datos = self.sc.recv(1024)
            if 'nick' == self.datos[:4]:
                if(self.conectado == False):
                    nick = self.datos[5:]
                    if self.testNick(nick) == True:
                        self.conectado = True
                        usuarios['nick'].append(self.datos[5:])
                        usuarios['source'].append(self.sc)
                        self.sc.send('Bienvenido al chat')
                        for s in usuarios['source']:
                            if s != self.sc:
                                s.send(nick+" ah entrado al chat")
                else:
                    self.sc.send('ya estas en el chat')

            elif ('usuarios' == self.datos[:8]) and (self.conectado == True):
                self.sc.send('\n--- Lista de usuarios conectados ---')
                for u in usuarios['nick']:
                        self.sc.send(u + '\n')
                        
            elif ('ayuda' == self.datos[:5]):
                self.sc.send("\n--->comandos:\n[usuarios] ver usuarios conectados\n[nick] entrar en el chat\n[@nickname] para mensajes privados\n[chgnick] para cambiar el nickname\n[salir] para salir del chat\n[ayuda] ver ayuda\n")
  
            elif ('salir' == self.datos[:5]):
                if (self.conectado == True):
                    for u in usuarios['source']:
                        if u == self.sc:
                            nick = usuarios['nick'][usuarios['source'].index(u)]
                            usuarios['nick'].remove(nick)
                            usuarios['source'].remove(u)
                            self.conectado = False
                    for u in usuarios['source']:
                        if u != self.sc:        
                            u.send(nick+" salio del chat")

            elif ('chgnick' == self.datos[:7]):
                if (self.conectado == True):
                    nick = self.datos[8:]
                    if self.testNick(nick) == True:
                        usuarios['nick'][usuarios['source'].index(self.sc)] = nick
                        self.sc.send('Su nick ha sido cambiad correctamente')
                    
            
            elif self.conectado == True:
                cont = 0
                for u in usuarios['nick']:
                    if '@'+u in self.datos:
                        cont += 1
                        usuarios['source'][usuarios['nick'].index(u)].send(usuarios['nick'][usuarios['source'].index(self.sc)] + '> ' + self.datos)
                if cont == 0:
                    for u in usuarios['source']:
                        if u != self.sc:
                            u.send(usuarios['nick'][usuarios['source'].index(self.sc)] + '-> ' + self.datos)
        self.sc.close()
