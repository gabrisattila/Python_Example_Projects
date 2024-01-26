import sys
from socket import socket, AF_INET, SOCK_STREAM
from os import system, name
import hashlib
from typing import final

def clear():
    	if name == 'nt':
    		_ = system('cls')

clear()

srv_ip = sys.argv[1]
srv_port = sys.argv[2]
chsum_srv_ip = sys.argv[3]
chsum_srv_port = sys.argv[4]
file_azon = sys.argv[5]
file_nev = sys.argv[6]

server_addr = (srv_ip, int(srv_port))
checksumb = 0

with socket(AF_INET, SOCK_STREAM) as client:
    with open(file_nev, "rb") as f:
        client.connect(server_addr)
        l = f.read(10)
        m = hashlib.md5(l)
        size = m.digest_size
        checksumb = checksumb + size
        ch = m.hexdigest()
        checksum = ch
        while l:
            client.sendall(l)
            l = f.read(10)
            m = hashlib.md5(l)
            size = m.digest_size
            checksumb = checksumb + size
            ch = m.hexdigest()
            checksum = checksum + ch
        
c_server_addr = (chsum_srv_ip, int(chsum_srv_port))

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(c_server_addr)
    client.sendall(b'BE|'+file_azon.encode()+b'|60|'+(str(checksumb)).encode()+b'|'+checksum.encode())
    #print(client.recv(200).decode())

'''
py netcopy_cli.py localhost 11000 localhost 10000 7 ../in.txt
'''
