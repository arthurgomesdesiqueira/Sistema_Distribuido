import socket, sys, os
from threading import Thread
import time
import random
import numpy as np

#HOST = 'localhost'
#PORT = 4567

#numero de processos(hosts)
NUMEROS_DE_PROCESSOS = 3

#todos os hosts que temos registrados e vamos utilizar
VARIABLES = [(0, 'localhost', 4567), (1, 'localhost', 4568), (2, 'localhost', 4569)] # (id, host, port)
idNotUse = 2 #id do host e port que nao usaremos
HOST = 'localhost' #HOST que estamos usando
PORT = 4569 #PORT que estamos usando


#atualizar o clock
def atualizarClock(clockLocal, msgClock):
    return max(clockLocal, msgClock) + 1

#propabilidade de 25%
def sleepAndGetProbability():
    time.sleep(5)
    randomNumber = random.randint(0, 100)
    print("randomNumber: ", str(randomNumber))
        
    if  0 <= randomNumber and randomNumber <= 25: 
        return True

    return False 

#somar +1 nos processos dentro da queue que tem mensagem(queue[i][0]) == msg
#retorna a qtd de processos com a mesma mensagem dentro da queue(value)
def calcularQtdDeProcessos(queue, msg):
    value = 1
    for i in range(len(queue)):
        if queue[i][0] == msg:
            queue[i][2] += 1
            value = queue[i][2]

    return value


#antes de enviar o send
def beforeSend(idLocal,clockLocal, queue):
    
    for i in range(0,12):
        #if sleepAndGetProbability() == True: #se quiser usar sleepAndGetProbability, descomente essa linha e comenta a de baixo
        msg = input('Clique ENTER para enviar a mensagem\n')    
        send(idLocal, False, clockLocal, 7, queue)


#se todas as mensagens chegaram a seu destino
#e o numero de processos na queue chegou ao maximo(NUMEROS_DE_PROCESSOS)
def deleteElem(queue):

    print("Queue:\n")
    print(queue)
    qtd = len(queue)
    item = 0
    for i in range(0, qtd):
        if queue[item][2] == NUMEROS_DE_PROCESSOS:
            del queue[item]
            print(queue)
        else:
            item += 1

def addInQueueAndSortQueue(queue, value_queue):
    queue.append(value_queue) #id, tempo, numero de processos, ack ou normal
    print("Adicionou queue: " + value_queue[0] + " " + str(value_queue[1]) + " " + str(value_queue[2]) + " " + value_queue[3])
    queue.sort(key=lambda x:x[1]) #ordenamos de acordo com o tempo


def createConnectionAndSendMessage(Host, Port, msg):
    server_address = (Host, Port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    
    sock.sendto(msg.encode(),server_address)
    
    sock.close()


#mandar mensagem
def send(message, sendAck, clockLocal, timer, queue):
    
    #quando é um evento novo, ele soma o clock local   
    clockLocal[0] = atualizarClock(clockLocal[0], -1)
    
    #quando a mensagem é normal, enviamos so a mensagem(id) com o valor do clock
    if(sendAck == False):
        msg = message + " " + str(clockLocal[0]) 
    else:
        msg = message + " " + str(clockLocal[0]) + " " + "ack"

    value = calcularQtdDeProcessos(queue, message)
    
    print("Criando um evento de envio")
    print("Clock atual: " + str(clockLocal[0]))
    if sendAck == True:
        value_queue = [message, clockLocal[0], value, 'ack'] #id, tempo, numero de processos, ack ou normal
        
    else:
        value_queue = [message, clockLocal[0], value, 'normal'] #id, tempo, numero de processos, ack ou normal
        
    addInQueueAndSortQueue(queue, value_queue)
    
    
    for idHost,Host,Port in VARIABLES:

        if(idHost == idNotUse):
            continue

        createConnectionAndSendMessage(Host, Port, msg)

        time.sleep(timer)

    
def receiver(idLocal, clockLocal, queue):
    
    print("Esse processo tem o id: ", idLocal)
    print("Esse processo tem o clockLocal: ", str(clockLocal[0]))
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.bind(server_address)
    
    while True:
        sock.listen(1)
        connection, client_address = sock.accept()
        data = connection.recv(64)
        if not data: break
        mensagem = data.decode()
        mensagemSplit = mensagem.split(' ')

        print("Criando um evento de receber")
        
        clockRecebido = int(mensagemSplit[1])
        clockLocal[0] = atualizarClock(clockLocal[0], int(clockRecebido))
        print("Clock atual: " + str(clockLocal[0]))

        Message = mensagemSplit[0]
        
        print("Mensagem recebida: " + str(mensagemSplit))

        value = calcularQtdDeProcessos(queue, Message)

        
        if(len(mensagemSplit) == 3): #mensagem ack
            value_queue = [Message, clockRecebido, value, 'ack'] #id, tempo, numero de processos, ack ou normal
            
        else: #mensagem normal
            value_queue = [Message, clockRecebido, value, 'normal'] #id, tempo, numero de processos, ack ou normal


        addInQueueAndSortQueue(queue, value_queue)


        if(len(mensagemSplit) != 3): #mensagem normal
            print("Enviando mensagem ack para todos os processos")
            send(Message, True, clockLocal, 0.5, queue)
        

        deleteElem(queue)
    

    connection.close()

def startMulticast(idLocal, clockLocal, queue):
    
    Thread(target=receiver, args=(idLocal, clockLocal, queue)).start()  
    #Antes de apertar ENTER, abre 3 terminais diferentes, modifique as variaveis la em cima HOST, PORT, VARIABLES e idNotUse
    #Verifique se todos os servidores estão ligados
    #Todos precisam estar na tela de Clique ENTER para enviar a mensagem
    input('Pode startar?\n')
    Thread(target=beforeSend, args=(idLocal, clockLocal, queue)).start()

#fila    
queue = [] #id, tempo, numero_de_processos repetidos, ack ou normal
auxClockLocal = input('Valor do nosso clockLocal:\n')
idLocal = input('Valor do nosso id\n')

clockLocal = [int(auxClockLocal)]

startMulticast(idLocal, clockLocal, queue)

