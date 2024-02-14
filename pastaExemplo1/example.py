import copy

def weighted_round_robin(ip_list):
   ip_list.sort(key=lambda x: x[1], reverse=True)

   highest_weight_ip = ip_list[0]

   return highest_weight_ip

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

def ordena_por_nodes(listaIps):
   tam = len(listaIps)
   blocos_nodes = []
   aux = 1

   while (len(blocos_nodes) != tam):
      i = 0
      for array in listaIps:
         if len(array) == aux:
            blocos_nodes.append((array, i))
         i += 1
      aux += 1
   
   return blocos_nodes

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

def lista_pedir_blocos(listaIps, blocos):
   aux = {}

   for ip, bloco in listaIps:
      if(blocos.count(bloco+1) == 0):
         aux.setdefault(ip[0], []).append(bloco + 1)
   ipBlocos = [(ip, blocos) for ip, blocos in aux.items()]

   return ipBlocos

blocos = [1,2]
ipsIndv = 3
listaIps1 = [[('ip1', 4), ('ip2', 7), ('ip3', -3)], [('ip2', 7)]] 
listaIps2 = [[('ip1', 0), ('ip2', 0)], [('ip2', 0), ('ip3', 0)]]
listaIps7 = [[('ip1', 2), ('ip2', 2), ('ip3', 2)], [('ip2', 2)]] 
#listaIps3 = [[('ip1', 0), ('ip2', 0)], [('ip1', 0), ('ip2', 0), ('ip3', 0)], [('ip3', 0)]]
#listaIps4 = [[('ip1', 0), ('ip2', 0)], [('ip1', 0), ('ip2', 0), ('ip3', 0)], [('ip3', 0)], [('ip1', 0), ('ip2', 0),], [('ip2', 0), ('ip3', 0), ('ip1', 0)], [('ip2', 0), ('ip3', 0), ('ip1', 0)]]
#ip_list = [('ip1', 4), ('ip2', 7), ('ip3', -3)]
#print(weighted_round_robin(ip_list)) # Output: 'ip2'
print()
teste2 = ordena_por_nodes(listaIps2)
print(teste2, "ips2")
print(teste2[0][0][0][1])
print(verifica_existe_prioridade(teste2, ipsIndv), "Têm de ser 0")
teste1 = ordena_por_nodes(listaIps1)
print(verifica_existe_prioridade(teste1, ipsIndv), "Têm de ser 1")
#teste11 = escolhe_nodes(teste1, ipsIndv)
#print(teste1, "2 0 1")
#print(teste11)
#print(lista_pedir_blocos(teste11, blocos))
#print()
#teste2 = ordena_por_nodes(listaIps2)
#teste21 = escolhe_nodes(teste2, ipsIndv)  
#print(teste2, "0 1")
#print(teste21)
#print(lista_pedir_blocos(teste21,blocos))
#print()
teste7 = ordena_por_nodes(listaIps7)
print(teste7)
print(teste7[0][0][0][1])
print(verifica_existe_prioridade(teste7, 3), "tem de ser 0")
#teste71 = escolhe_nodes(teste7, ipsIndv)
#print(teste71)
#print(lista_pedir_blocos(teste71, blocos))
#teste3 = ordena_por_nodes(listaIps1)
#print(teste3, "1 0")
#print(escolhe_nodes(teste3))
#teste4 = ordena_por_nodes(listaIps4)
#print(teste4, "2 0 3 1 4 5")
#print(escolhe_nodes(teste4))

listaIps5 = [[('ip1', 0), ('ip2', 0)],  #0
    [('ip1', 0), ('ip2', 0), ('ip3', 0)], #1
    [('ip3', 0)],#2
    [('ip2', 0), ('ip3', 0)], #3
    [('ip1', 0)], #4
    [('ip1', 0), ('ip2', 0), ('ip3', 0)], #5
    [('ip1', 0), ('ip2', 0), ('ip3', 0)], #6
    [('ip2', 0), ('ip3', 0)], #7
    [('ip1', 0), ('ip3', 0)], #8
    [('ip1', 0), ('ip2', 0), ('ip3', 0)], #9
    [('ip3', 0), ('ip2', 0), ('ip1', 0)], #10
    [('ip1', 0)], #11
    [('ip2', 0)], #12
    [('ip2', 0), ('ip1', 0), ('ip3', 0)], #13
    [('ip2', 0), ('ip1', 0), ('ip3', 0)], #14
    [('ip1', 0), ('ip2', 0)], #15
    [('ip3', 0), ('ip2', 0)]] #16

#teste5 = ordena_por_nodes(listaIps5)
#print(teste5)
#teste51, aux = escolhe_nodes(teste5, 3, 4)
#print(teste51, "Lista a pedir")
#print(aux, "tuples por pedir")
#print(lista_pedir_blocos(teste51, []))
#print(aux, "ordenado")
#aux1, aux2 = escolhe_nodes(aux, 3, 4)
#print(aux1)
#print(lista_pedir_blocos(aux1, []), "Pede")
#print(aux2, "Aux2")

#listaIps6 = [[('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)], [('ip1', 0)]]

#teste6 = ordena_por_nodes(listaIps6)
#print(teste6, "teste")
#print(escolhe_nodes(teste6, 1, 4))
#print(lista_pedir_blocos(escolhe_nodes(teste6, 1)))
#lista = [([('ip2', 0)], 15), ([('ip2', 0), ('ip3', 0)], 1), ([('ip2', 0), ('ip3', 0)], 5), ([('ip2', 0), ('ip3', 0)], 6), ([('ip2', 0), ('ip3', 0)], 9)]
#aux4, aux6 = escolhe_nodes(lista, 3, 4)
#print(aux4, "teste")
#lista1 = [([('10.1.1.1', 28), ('10.1.1.2', 19)], 0), ([('10.1.1.1', 28), ('10.1.1.2', 19)], 1), ([('10.1.1.1', 28), ('10.1.1.2', 19)], 2),([('10.1.1.1', 28), ('10.1.1.2', 19)], 3), ([('10.1.1.1', 28), ('10.1.1.2', 19)], 4), ([('10.1.1.1', 28), ('10.1.1.2', 19)], 5), ([('10.1.1.1', 28), ('10.1.1.2', 19)], 6)] 
#aux, aux1 = escolhe_nodes(lista1, 2, 3)
#print(aux)
#print(aux1)