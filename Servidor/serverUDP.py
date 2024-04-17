import socket
import time
import hashlib

def calculate_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

HOST = 'localhost'
PORT = 50000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((HOST, PORT))
print(f"Servidor rodando no host {HOST} e porta {PORT}")
udp.settimeout(15)

try:
    while True:     
        request, END_cliente = udp.recvfrom(1024)
        request = request.decode()

        if request.startswith("GET"):
            nome_arquivo = request.split()[1][1:]
            try: 
                with open(nome_arquivo, "rb") as arquivo:
                    pacote = 1
                    janela_deslizante = {}
                    while True:
                        ler_buffer = arquivo.read(1024)
                        if not ler_buffer:
                            break
                        checksum = calculate_sha256(ler_buffer)
                        janela_deslizante[pacote] = (ler_buffer, checksum)
                        pacote += 1

                    # Enviar pacotes e reenviar os não confirmados
                    for seq_num, (data, sha256_hash) in janela_deslizante.items():
                        while True:
                            udp.sendto(data + sha256_hash, END_cliente)
                            print(f"Pacote {seq_num}: enviado {len(data)} bytes para o cliente {END_cliente}")
                            try:
                                ack, _ = udp.recvfrom(1024)
                                ack = ack.decode()
                                if ack == f"ACK {seq_num}":
                                    break
                            except socket.timeout:
                                print(f"Timeout ao aguardar ACK para o pacote {seq_num}. Reenviando...")
                    
                    print(f"Arquivo de {pacote - 1} pacotes enviado para o cliente {END_cliente}")   
            except FileNotFoundError:
                print("Erro ao localizar arquivo")
                erro = "Arquivo não encontrado"
                udp.sendto(erro.encode(), END_cliente)
except KeyboardInterrupt:
    print("Servidor encerrado pelo usuário")
finally:
    udp.close()
