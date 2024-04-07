import socket

HOST = 'localhost'
PORT = 50000

udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp.bind((HOST,PORT))
print(f"Servidor UDP rodando no endereço {HOST} e porta {PORT}")

Arquivo = open("arquivorecebido.txt",'wb')
pacote = 1
while True:
    ler_buffer, END_cliente = udp.recvfrom(1024)
    
    if not ler_buffer:
        break

    Arquivo.write(ler_buffer)

    #print(f"Pacote {pacote}: recebido {len(ler_buffer)} bytes do cliente {END_cliente}")
    if len(ler_buffer) < 1024:
        break
    pacote += 1
Arquivo.close()
print(f"Arquivo recebido do cliente {END_cliente} Total de pacotes:{pacote}")
udp.close()
print("Socket UDP fechado.")

#Mensagem_Recebida, END_cliente = udp.recvfrom(1024)
#print ("Recebi = " ,Mensagem_Recebida, " , Do cliente", END_cliente)

