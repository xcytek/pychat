#!/usr/bin/python

import socket
import threading
import chat

s = socket.socket()
s.bind((socket.gethostbyname(socket.gethostname()), 9999 ))
s.listen(10)

while(True):
    sc, addr = s.accept()
    chat.chatPrincipal(sc).start()

sc.close()
s.close()
