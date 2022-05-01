from socket  import *
from constCS import * #-

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT)) # connect to server (block until accepted)

userData = input('Digite os dois numeros e a operacao:\nOperacoes validas: add, subtract, divide, multiply.\n')

s.send(userData.encode())  # send some data
data = s.recv(1024)     # receive the response
print (bytes.decode(data))            # print the result
s.close()               # close the connection
