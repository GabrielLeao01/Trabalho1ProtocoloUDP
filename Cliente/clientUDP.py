import socket

IP_Servidor = 'localhost'
Porta_Servidor = 50000

udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

DESTINO = (IP_Servidor,Porta_Servidor)

arquivo = open("Teste2.txt","rb")
ler_buffer = arquivo.read(1024)
pacote = 1
while(ler_buffer):
    udp.sendto(ler_buffer,DESTINO)
    print(f"Pacote {pacote}: enviado {len(ler_buffer)} bytes para o servidor {IP_Servidor}:{Porta_Servidor}")
    pacote += 1
    ler_buffer = arquivo.read(1024)
print(f"Arquivo de {pacote -1 } pacotes enviado para o servidor {IP_Servidor}:{Porta_Servidor}")    
udp.close()

