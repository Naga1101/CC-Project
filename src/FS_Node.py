import threading
import select
import socket
import pickle
import sys
import os

from Metodo_Transf import *

MTU = 1200
ID_SIZE = 4
CHECK_SUM = 2
TamanhoBloco = MTU - (ID_SIZE + CHECK_SUM)
udpAtivo = True

blocos_recebidos = {}

# Método utilizado no caso de um node já ter uma parte do ficheiro que pretende transferir
# desta forma apenas irá pedir os blocos que lhe faltam
def blocos_para_pedir(nomeFile, numBlocos):
    blocos = {num for num, _ in blocos_recebidos.get(nomeFile, [])}
    blocos_por_pedir = [num for num in range(1, numBlocos + 1) if num not in blocos]
    return blocos_por_pedir

# Método que desliga a socket udp de um node que foi desconectado 
def set_udp_false():
    global udpAtivo
    udpAtivo = False

# Configuração do cliente
if len(sys.argv) != 4:
    print("Uso: python cliente.py <IP do host> <Número da Porta> <Pasta com os ficheiros>")
    sys.exit(1)

host = sys.argv[1]  # Endereço IP do servidor
port = int(sys.argv[2])  # Porta que o servidor está ouvindo

# Métodos que prepara a lista dos ficheiros e os blocos que um node têm e vai colocar na mensagem de conexão ao tracker
def calcula_num_blocos(caminho_ficheiro):
    tamanhoFicheiro = os.path.getsize(caminho_ficheiro)
    numBlocos = tamanhoFicheiro // TamanhoBloco
    
    if tamanhoFicheiro % TamanhoBloco != 0:
        numBlocos += 1

    return numBlocos

def calcula_blocos_por_ficheiro(caminho_pasta):
    ficheiros_comBlocos = []
    
    for filename in os.listdir(caminho_pasta):
        caminho_ficheiro = os.path.join(caminho_pasta, filename)
        blocosTotais = calcula_num_blocos(caminho_ficheiro)
        ficheiros_comBlocos.append((filename, blocosTotais))
        
    return ficheiros_comBlocos
        
# Cria uma lista com o nome dos ficheiros e o número de blocos ocupados dentro de uma pasta
caminho_pasta = sys.argv[3] 
ficheiros_comBlocos = calcula_blocos_por_ficheiro(caminho_pasta)   
 
# Fim dos métodos de construção da lista de blocos e ficheiros

# Método que estabelece a comunicação de um Node com o Tracker    
def tracker_protocol():
    # Cria um socket do tipo TCP
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta-se ao servidor
    socketTCP.connect((host, port))
    
    # Cria a mensagem que é enviada assim que o node conecta ao tracker
    mensagemFiles = f"files/" + ' | '.join([f"{file}-{blocks}" for file, blocks in ficheiros_comBlocos]) + '\n'
    socketTCP.send(mensagemFiles.encode())
    
    print("Escreva 'comandos' em caso de dúvida")
    
    while True:
        user_input = input("Selecione um comando: ")
        comando = user_input.strip().lower().split(' ')
        
        if comando[0] == "quit":
            socketTCP.send("quit/\n".encode())
            print("Desligada a conexão ao servidor")
            set_udp_false()
            break
        
        elif comando[0] == "get":
            nomeFicheiro = comando[1]  # Obtém o nome do arquivo
            mensagemGet = f"get/{nomeFicheiro}\n"
            socketTCP.send(mensagemGet.encode())
            fileInfo_bytes = b""
            while True:
                chunk = socketTCP.recv(1024)
                if chunk == b'END_TRANSMISSION':
                    break
                fileInfo_bytes += chunk

            fileInfo = pickle.loads(fileInfo_bytes)
            if fileInfo == "None":
                print("O ficheiro que está a tentar transferir não existe")
            else:
                blocos_por_pedir = []
                if nomeFicheiro in blocos_recebidos:
                    numBlocos = int(fileInfo[0])
                    blocos_por_pedir = blocos_para_pedir(nomeFicheiro, numBlocos)
                sucesso = transf_file(fileInfo, caminho_pasta,  nomeFicheiro, blocos_recebidos, blocos_por_pedir, socketTCP, port)
                if sucesso == 0:
                    mensagemUpdate = f"updfin/{nomeFicheiro}\n"
                    socketTCP.send(mensagemUpdate.encode())
                else: 
                    print("O ficheiro não foi totalmente transferido, tente novamente.")
       
        elif comando[0] == "comandos":
            print("\tquit: Desligar a ligação ao servidor.")
            print("\tget 'file_name': Digite o nome do file que pretende transferir no lugar de file_name.")
            print("\tcomandos: Lista os comandos existentes.")
        
    socketTCP.close()
    
# Método que mantém a porta udp de um node aberta à espera de pedidos de transferência 
def transfer_protocol():
    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketUDP.bind(('0.0.0.0', 9090)) 
    
    while udpAtivo:
        ready, _, _ = select.select([socketUDP], [], [], 1.0)
        
        if ready:
            data, addr = socketUDP.recvfrom(1024)
            infoFile = data.decode()
            if infoFile == "Ping":
                reply = "Pong"
                socketUDP.sendto(reply.encode(), addr)
            else:
                fileName, numBloco = infoFile.split("|")
                if fileName in blocos_recebidos:
                    env_FileIncl(blocos_recebidos, fileName, int(numBloco), socketUDP, addr)
                else:
                    env_FileCmpl(caminho_pasta, fileName, int(numBloco), socketUDP, addr)
            ready = False
   
udp_thread = threading.Thread(target = transfer_protocol)
udp_thread.start()
tracker_thread = threading.Thread(target = tracker_protocol)
tracker_thread.start()