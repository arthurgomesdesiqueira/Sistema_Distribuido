import threading
import time
import struct
import socket
import sys
import random

MYPORT = 9876
MYGROUP_4 = '225.0.0.250'
MYTTL = 1 # Increase to reach other networks
NUMPROCESS = 4

def createSocketMulticast():
    # Procura o endereço do grupo de multicast no servidor de nomes e descubre a versão do IP
    addrinfo = socket.getaddrinfo(MYGROUP_4, None)[0]

    # Cria um socket UDP
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Permite que mais de um socket utilize o mesmo endereço na mesma máquina
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Conecta por localhost e porta fornecida
    s.bind(('localhost', MYPORT))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    
    # Entra no grupo
    mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return(s)

def imprimeFila(fila):
    print("Fila de processos: ")
    print("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
    print(fila)
    print("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")

# Responsável por realizar a entrega das mensagens à aplicação
def delive(lista):
        while len(lista) != 0 and lista[0][2] and lista[0][3] == NUMPROCESS:
            print("\nMensagem '" + lista[0][0] + "' entregue à aplicação!")
            del lista[0]
            imprimeFila(repr(lista))
            print("")

# Atualiza o clock lógico do processo
def updateClock(mensagemSplit, clockInicial):
    if(int(mensagemSplit[1][:-3]) > clockInicial[0]):
        clockInicial[0] = int(mensagemSplit[1][:-3]) + 1
    else:
        clockInicial[0] = clockInicial[0]+1

def processMessage(idPross, clockInicial, lista, mensagem):
    # simula o atraso de recebimento de pacotes pela rede
    mensagemSplit = mensagem[:-1].split()
    time.sleep(random.randint(5, 30))

    # Atualiza a o relógio lógico
    updateClock(mensagemSplit, clockInicial)
    
    if len(mensagemSplit) == 2:
        print("Mensagem: '" + mensagemSplit[0] + "' | Marca de tempo: " + mensagemSplit[1])

        existe = False
        for i in range(len(lista)):
            if lista[i][1] == mensagemSplit[1]:
                lista[i][0] = mensagemSplit[0];
                lista[i][2] = True
                existe = True
                break

        if existe == False:
            lista.append([mensagemSplit[0], mensagemSplit[1], True, 0])
            lista.sort(key=lambda x:x[1])

        imprimeFila(lista)
        print("")
        print("")

        clockInicial[0] += 1 
        mensagemACK = mensagemSplit[1] + " " + str(clockInicial[0]).zfill(3)+str(idPross).zfill(3) + " ACK"
        sender(mensagemACK)
        
    else:
        existe = False  
        for i in range(len(lista)):
            if lista[i][1] == mensagemSplit[0]:
                lista[i][3] += 1
                existe = True
                break

        if existe == False:
            lista.append(["-", mensagemSplit[0], False, 1])
            lista.sort(key=lambda x:x[1])

        for i in range(len(lista)):
            if lista[i][1] == mensagemSplit[0]:
                print("ACK de: " + lista[i][1] + " | Marca de tempo(ACK): " + mensagemSplit[1])

        imprimeFila(lista)
        print("")

        delive(lista)

def receiver(idPross, clockInicial, lista):
    contadorACK = 0

    print("\nClock Inicial: " + str(clockInicial[0]))
    imprimeFila(repr(lista))

    s = createSocketMulticast()

    # Loop, printing any data we receive
    while True:
        data, source = s.recvfrom(1500)
        print("recebi")
        while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        mensagem = data.decode('utf-8')

        t = threading.Thread(target=processMessage, args=(idPross, clockInicial, lista, mensagem))
        t.start()
        print("executado")
        

def sender(message):
    # Procura o endereço do grupo de multicast no servidor de nomes e descubre a versão do IP
    addrinfo = socket.getaddrinfo(MYGROUP_4, None)[0]

    # Cria socket UDP
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Time-to-live (optional). Não permitir que o pacote alcance se espalhe para a rede externa
    ttl_bin = struct.pack('@i', MYTTL)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

    # Enviar a mensagem 
    data = message.encode('utf-8') + b'\0'
    s.sendto(data, (addrinfo[4][0], MYPORT))
    time.sleep(0.5)

# Inicio programa
lista=[]
idPross = input("Digite o id do processo: ")
clockInicial = input("Digite o clock inicial: ")
clockInicial = [int(clockInicial)]

# Cria thead responśvel por receber as mensagens
t = threading.Thread(target=receiver, args=(idPross, clockInicial, lista))
t.start()

# Thread principal é responsável por enviar os pacotes e "entregá-los" à aplicação
#while(True):
#    time.sleep(0.5);
#    input()
#    message =  input("Digite a mensagem: ")
#    print("")
#    message = message + " " + str(clockInicial[0]+1).zfill(3) + str(idPross).zfill(3)
#    sender(message)
#    print("")