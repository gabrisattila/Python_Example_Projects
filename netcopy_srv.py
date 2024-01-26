from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import sys
from os import system, name
import hashlib
from select import select

def clear():
    	if name == 'nt':
    		_ = system('cls')

clear()

srv_ip = sys.argv[1]
srv_port = sys.argv[2]
chsum_srv_ip = sys.argv[3]
chsum_srv_port = sys.argv[4]
file_azon = sys.argv[5]
ki_file_nev = sys.argv[6]

server = socket(AF_INET, SOCK_STREAM)
checksum = socket(AF_INET, SOCK_STREAM)

server_addr = (srv_ip, int(srv_port))
c_server_addr = (chsum_srv_ip, int(chsum_srv_port))

server.bind(server_addr)
server.listen(5)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

end = False

while not end:
    try:
        client, client_addr = server.accept()
        data = client.recv(10)
        Data = data
        end1 = False
        with open(ki_file_nev, "wb") as f:
            while not end1:
                if data:
                    f.write(data)
                    data = client.recv(10)
                    Data = Data + (data)
                else:
                    client.close()
                    end1 = True
        m = hashlib.md5(Data)
        msize = m.digest_size
        end = True
    except timeout:
        pass    
end = False
while not end:
    checksum.connect(c_server_addr)
    checksum.sendall(b"KI|"+file_azon.encode())
    adat = checksum.recv(200).decode().split(sep="|")
    if len(adat) > 1:
        if adat[0] == msize and adat[1] == m:
            print("CSUM OK")
        else:
            print("CSUM CORRUPTED")
    else:
        print("CSUM CORRUPTED")
    end = True



                
                
'''
py netcopy_srv.py localhost 11000 localhost 10000 7 ../out.txt
'''
