import socket

HOST = 'localhost'
PORT = 50000

soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
soc.bind((HOST,PORT))
print(f"Servidor UDP rodando no endereço {HOST} e porta {PORT}")

Mensagem_Recebida, END_cliente = soc.recvfrom(1024)

print ("Recebi = " ,Mensagem_Recebida, " , Do cliente", END_cliente)

soc.close()