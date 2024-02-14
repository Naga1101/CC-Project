import threading
import socket
import pickle

from Struct_FileNodes import *

# criar um diconário para relembrar em que node está cada ficheiro
node_threads = {}

# Configuração do servidor
domain_prefix = socket.gethostname()
domain_suffix = ".CC2023"
domain = f"{domain_prefix}{domain_suffix}"
host = socket.gethostbyname(domain)  # Endereço IP do servidor
port = 9090       # Porta que o servidor irá ouvir

print(f"{domain} está escutando em {host}: porta {port}")

# Cria um socket do tipo TCP
socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula o socket ao endereço e à porta
socketTCP.bind((host, port))

# Começa a ouvir por conexões
socketTCP.listen()

x = 0

# Método que interage diretamente com o Node
def handle_node(node_socket):
    trackerAtivo = True
    nodeIP = node_socket.getpeername()[0]
    hostname, _, _ = socket.gethostbyaddr(nodeIP)
    buffer = b''
    while trackerAtivo:    
        data = node_socket.recv(1024)
        if not data:
            relembrar_nota(hostname)
            remover_info_node(hostname)
            node_socket.close()
            break
        buffer += data
        messages = buffer.split(b'\n') 
        buffer = messages.pop()

        for message in messages:
            message_str = message.decode()
            format = message_str.split("/")
            key = format[0]
        
            if key == "quit":
                print("Node desconectado")
                relembrar_nota(hostname)
                remover_info_node(hostname)
                # remover_info_node('10.0.0.2')
                node_socket.close()
                trackerAtivo = False
                break
                
            elif key == "files":
                if len(format) == 2:
                    data = format[1]
                    if data:
                        guarda_Localizacao(data, hostname)
                        # guarda_Localizacao("file3.txt-2", "10.0.0.5")
                        # update_info_file("file3.txt", "10.0.0.2", [2])
                else:
                    print("Ocorreu um erro a enviar os ficheiros.")
                    
            elif key == "get":
                if len(format) == 2:
                    nomeFile = format[1]
                    localizacao = procurar_file(nomeFile)
                    #print(localizacao, "localizacao")
                    
                    if localizacao is not None:
                        numBlocos = int(localizacao[0])
                        hostsIndv = len(localizacao[1]) + len(localizacao[2])  # numero máximo de blocos que se pode transferir
                        node_info = (numBlocos, localizacao[1], localizacao[2], hostsIndv)
                        response = pickle.dumps(node_info)
                    else:
                        response = "None"
                        response = pickle.dumps(response)

                    node_socket.send(response)
                    end_message = "END_TRANSMISSION"
                    node_socket.send(end_message.encode())
                else:
                    print("Ocorreu um erro a pedir o file")

            elif key == "updlst":
                if len(format) == 2:
                    nomeFile = format[1]
                    localizacao = procurar_file(nomeFile)
                    
                    if localizacao is not None:
                        numBlocos = int(localizacao[0])
                        node_info = (numBlocos, localizacao[1], localizacao[2], hostsIndv)
                        response = pickle.dumps(node_info)
                    else:
                        response = "None"
                        response = pickle.dumps(response)
                    
                    node_socket.send(response)
                    end_message = "END_TRANSMISSION"
                    node_socket.send(end_message.encode())

            elif key == "updblc":
                if len(format) == 5:
                    nomeFile = format[1]
                    num = format[2]
                    peso = int(format[3])
                    hostnamePeso = format[4] 
                    numBlocos = [int(x) for x in num.strip("[]").split(",")]
                    update_info_file(nomeFile, hostname, numBlocos, hostnamePeso, peso)
                    
            elif key == "updfin":
                if len(format) == 2:
                    nomeFile = format[1]
                    update_info_file(nomeFile, hostname, [], 0, 0)
                
while True:
    # Aceita uma conexão de um cliente
    node_socket, node_address = socketTCP.accept()

    x = x+1
    
    node_thread = threading.Thread(target = handle_node, args = (node_socket,))
    node_thread.start()
    
    node_threads[x] = node_thread
    
# Fecha o socket do servidor
socketTCP.close()

# lsof -i :9090 // caso não seja possivel ligar o servidor mata quem estiver a usar a porta