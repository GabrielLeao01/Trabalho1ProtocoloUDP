import socket

IP_Servidor = 'localhost'
Porta_Servidor = 50000

soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

DESTINO = (IP_Servidor,Porta_Servidor)

Mensagem = input()

soc.sendto (bytes(Mensagem,"utf8"), DESTINO)

soc.close()

