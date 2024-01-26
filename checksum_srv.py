from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import sys
from os import system, name
import hashlib
from select import select
import time

def clear():
    	if name == 'nt':
    		_ = system('cls')

clear()

chsum_srv_ip = sys.argv[1]
chsum_srv_port = sys.argv[2]

c_server_addr = (chsum_srv_ip, int(chsum_srv_port))

checksumok = [""]
chsize = 0

c_server = socket(AF_INET, SOCK_STREAM)
c_server.bind(c_server_addr)
c_server.listen(5)
end = False
while not end:
    try:
        client, client_addr = c_server.accept()
        data = client.recv(200).decode().split(sep="|")
        chsize = chsize + 3
        for i in range(0, chsize):
            if i % 3 == 0:
                checksumok.insert(i, data[1])
            elif i % 3 == 1:
                checksumok.insert(i, data[3])
            elif i % 3 == 2:
                checksumok.insert(i, data[4])
        client.sendall("OK".encode())
        client.close()
        counter = 1
        end = True
    except timeout:
        pass

server, server_addr = c_server.accept()
data = server.recv(200).decode().split(sep="|")
if data[1] in checksumok:
    for i in range(0, chsize):
        if checksumok[i] == data[1]:
            server.sendall((checksumok[i+1]+"|"+checksumok[i+2]).encode())
else:
    server.sendall("0|".encode())
server.close()

'''
py checksum_srv.py localhost 10000
'''
