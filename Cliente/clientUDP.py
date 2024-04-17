import socket
import hashlib

def calculate_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

IP_Servidor = 'localhost'
Porta_Servidor = 50000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.settimeout(5)  

try:
    print("Para solicitar um arquivo do sistema digite o nome do arquivo")
    nome_arquivo = input()
    request = f"GET /{nome_arquivo}"
    udp.sendto(request.encode(), (IP_Servidor, Porta_Servidor))     
    pacote = 1

    with open(nome_arquivo, "wb") as arquivo:
        while True:
            try:
                data_with_sha256, server_address = udp.recvfrom(1024 + 32)  # 32 bytes para o hash SHA256
            except socket.timeout:
                print("Tempo limite de recepção atingido. Encerrando a conexão.")
                break

            ler_buffer = data_with_sha256[:-32]  
            sha256_received = data_with_sha256[-32:]
            sha256_calculated = calculate_sha256(ler_buffer)

            if sha256_received == sha256_calculated:
                print(f"Pacote {pacote}: recebido {len(ler_buffer)} bytes do servidor {IP_Servidor}:{Porta_Servidor} SHA256 recebido: {sha256_received.hex()} SHA256 calculado: {sha256_calculated.hex()}")
                arquivo.write(ler_buffer)
                udp.sendto(f"ACK {pacote}".encode(), (IP_Servidor, Porta_Servidor))  # Enviar ACK
            else:
                print('Erro de SHA256! Dados corrompidos.')            

            if len(ler_buffer) <= 992:  # Ajustado para 992 para considerar os 32 bytes do SHA256
                break
            pacote += 1

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    udp.close()
