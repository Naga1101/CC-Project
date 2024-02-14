import copy

# Método que recebe a informação dos Nodes relativa a cada ficheiro e transforma num array com a lista dos ips dos Nodes que contêm os blocos na posição do array nº bloco - 1
def blocos_por_node(fileCompl, fileIncpl, numBlocos):   # [('127.0.0.1', 0)]  [(('127.0.0.1', 0), [1, 1, 1, 0])]] 4
    blocosIps = []
    array_node = []
    i = 0
    
    while i < numBlocos:
        for ip in fileCompl:
            array_node.append(ip)
            
        
        for tpl in fileIncpl:
            if tpl[1][i] == 1:
                array_node.append(tpl[0])
        
        blocosIps.append(array_node)
        array_node = []
        i += 1
 
    return blocosIps

# Método que compara os nodes todos que têm blocos do ficheiro pretendido 
# e verifica se têm todos a mesma pontuação ou se existe algum node com prioridade
def verifica_existe_prioridade(listaIps, ipsIndv):
    aux = 0
    for lista, bloco in listaIps:
        ipsVerificados = set() 
        aux2 = lista[0][1]

        if aux > ipsIndv:
            return 0

        for tpl in lista:
            if aux >= ipsIndv:
                return 0

            if tpl not in ipsVerificados:
                aux += 1
                if tpl[1] != aux2:
                    return 1
                else:
                    ipsVerificados.add(tpl)

    return 0

# Método que recebendo a lista dos blocos ordenada pela ordem dos blocos reorganiza a lista
# de forma a que os primeiros blocos a ser pedidos são os que se encontram em menor número de nodes
def ordena_por_nodes(listaIps):
   tam = len(listaIps)
   blocos_nodes = []
   aux = 0

   while (len(blocos_nodes) != tam):
      i = 0
      for array in listaIps:
         if len(array) == aux:
            blocos_nodes.append((array, i))
         i += 1
      aux += 1

   return blocos_nodes

# Algoritmo de round robin por pesos que escolhe dentro de uma lista de nodes o que têm o maior peso para ser pedido o bloco
def weighted_round_robin(listaIps):  # listaIps = [('ip1', 4), ('ip2', 7), ('ip3', -3)] res = ('ip2', 7)
   listaIps.sort(key=lambda x: x[1], reverse=True)
   melhorIp = listaIps[0]

   return melhorIp

# Função que utilizando o algoritmo de round robin decide a que node vai ser pedido cada bloco 
# sendo que recebe um N que é o número máximo de blocos que cada node pode enviar sem ficar sobre carregado 
# No caso de haverem blocos por pedir guarda numa lista que voltará a ser processada futuramente
def escolhe_nodes(listaIps, ipsIndv, N):
   ipsEscolhidos = []
   aux = []
   blocos_por_pedir = []
   listaIpsAux = copy.deepcopy(listaIps)

   try:
      for tuple in listaIpsAux:
         ip = weighted_round_robin(tuple[0])
         if aux.count(ip) >= N and ipsIndv > 1:
            aux2 = tuple[0]
            aux2.remove(ip)
            ip2 = weighted_round_robin(aux2)
            if aux.count(ip2) >= N:
               while aux.count(ip2) >= N:
                  aux2.remove(ip2)
                  ip2 = weighted_round_robin(aux2)
                  aux.append(ip2)
                  ipsEscolhidos.append((ip2, tuple[1]))
            else:
               aux.append(ip2)
               ipsEscolhidos.append((ip2, tuple[1]))
         else:
            aux.append(ip)
            ipsEscolhidos.append((ip, tuple[1]))
   except Exception as e: # lista de blocos que ainda não foram pedidos
      blocos_por_pedir = [tpl for tpl in listaIps if not any(tpl[1] == bloco[1] for bloco in ipsEscolhidos)]
      return ipsEscolhidos, blocos_por_pedir

   return ipsEscolhidos, []

# Método que recebe a lista final organizada pelos blocos e o node a que vão ser pedidos cada bloco
# e coloca tudo numa lista que irá conter cada node ligado a uma lista dos blocos que lhe serão pedidos
# Passa [(ip1, 1), (ip2, 3), (ip1, 4), (ip2, 2), (ip1, 5)] para [(ip1, [1,4,5]), (ip2, [3,2])]
def lista_pedir_blocos(listaIps):
   aux = {}

   for ip, bloco in listaIps:
      aux.setdefault(ip, []).append(bloco+1)
   ipBlocos = [(ip, blocos) for ip, blocos in aux.items()]

   return ipBlocos

# Método que verifica se ainda existem blocos que não foram recebidos
def verifica_lista(blocos):
   if blocos == []:
      return False
   return True

# Método que filtra a lista de Nodes de modo a apenas aparecerem aqueles que têm os blocos em falta
def filtraLista (listaIps, listaBlocosemFalta):
   lista_final = []
   for tup in listaIps:
      if listaBlocosemFalta.count(tup[1]+1) == 1:
         lista_final.append(tup)
   return lista_final